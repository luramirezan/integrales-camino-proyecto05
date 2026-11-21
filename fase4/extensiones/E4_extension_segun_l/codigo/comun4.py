"""comun4.py -- utilidades de la extension E4 (como crece la extension espacial segun l).

Proyecto 05 (Yukawa V = -e^{-delta r}/r), unidades hbar = m = g = 1. Ecuacion radial para la onda parcial l:

    -u''/2 + [V(r) + l(l+1)/(2 r^2)] u = E u,   u(0) = 0.

Contenido
---------
1. Diferencias finitas (reutiliza fase2/codigo/radial.py SIN modificarlo): basta pasarle el potencial efectivo
   V_ef = V + l(l+1)/(2r^2), porque radial.resolver construye la matriz tridiagonal 1/h^2 + V_ef(r_j).
       fd(V, l, R, h, nev)            una malla
       fd_rich(V, l, R, h, nev)       mallas h y h/2 con Richardson de orden 2 (orden medido en 40_*)
2. Disparo de alta precision sin caja (segundo metodo):
       ligado(l, delta, kappa_guess, ...)   estado ligado con E < 0: integracion hacia afuera desde la serie de
                                            Frobenius (8 terminos, r0 = 1e-3) hasta r_m y hacia adentro desde r_ext,
                                            donde se impone la solucion exacta fuera del potencial
                                            u = e^{-kappa r} sum_j c_j r^{-j} (r k_l(kappa r), Bessel esferica
                                            modificada); para Coulomb (delta = 0) la de Whittaker W_{1/kappa,l+1/2}.
                                            Momentos <r^n> y <e^{-delta r}> con la cola exterior en forma cerrada.
       caja_disparo(l, delta, R, E_lo, E_hi)  autovalor con u(R) = 0 (pared de Dirichlet) por disparo.
       umbral(l, a, b)                     delta_c: coeficiente B de r^{l+1} en la solucion de energia cero = 0.
       estado_umbral(l, delta_c)           constantes de la solucion de energia cero en el umbral (A, S, C0, ...).
3. Utilidades: Tee (salida impresa a archivo), guardar_json.

r_ext = 42/delta: alli e^{-delta r} = 5.7e-19, de modo que el potencial es despreciable frente a la precision
del integrador (rtol = 1e-13). Todo es determinista.
"""
import json
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))      # /mnt/project-files
F2 = os.path.join(RAIZ, "fase2", "codigo")
F3 = os.path.join(RAIZ, "fase3", "codigo")
sys.path.insert(0, F2)
import radial  # noqa: E402

RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

DELTA_C_1S_REF = 1.1906124210606          # Fases 1-3
PRED = {"2p": 0.22021681, "3d": 0.09134512, "2s": 0.31020928}   # valores del encargo (prototipo de la propuesta)
ESTADOS = {"1s": dict(l=0, nr=0, br=(1.1, 1.3)), "2s": dict(l=0, nr=1, br=(0.25, 0.4)),
           "2p": dict(l=1, nr=0, br=(0.18, 0.26)), "3d": dict(l=2, nr=0, br=(0.07, 0.12))}
RTOL = 1e-13
ATOL = 1e-200
GAMMA_E = 0.57721566490153286


# ============================================================================ salida
class Tee:
    """Copia todo lo que se imprime a resultados/<nombre>_salida.txt."""

    def __init__(self, nombre):
        self.f = open(os.path.join(RES, nombre + "_salida.txt"), "w")
        self.o = sys.stdout
        sys.stdout = self

    def write(self, s):
        self.o.write(s)
        self.f.write(s)

    def flush(self):
        self.o.flush()
        self.f.flush()


def _limpiar(x):
    if isinstance(x, dict):
        return {str(k): _limpiar(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_limpiar(v) for v in x]
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, np.ndarray):
        return _limpiar(x.tolist())
    if isinstance(x, float) and not math.isfinite(x):
        return None if math.isnan(x) else ("inf" if x > 0 else "-inf")
    return x


def guardar_json(nombre, datos):
    fn = os.path.join(RES, nombre + ".json")
    with open(fn, "w") as f:
        json.dump(_limpiar(datos), f, indent=1, ensure_ascii=False)
    return fn


def leer_json(nombre):
    with open(os.path.join(RES, nombre + ".json")) as f:
        return json.load(f)


# ============================================================================ potenciales
def V_yukawa_np(delta):
    return lambda r: -np.exp(-delta * r) / r


def V_ef(V, l):
    c = 0.5 * l * (l + 1)
    return lambda r: V(r) + c / r**2


# ============================================================================ 1. diferencias finitas
def fd(V, l, R, h=None, N=None, nev=2):
    return radial.resolver(V_ef(V, l), R, h=h, N=N, nev=nev)


def fd_rich(V, l, R, h=1 / 40, nev=2, p=2):
    return radial.resolver_rich(V_ef(V, l), R, h=h, nev=nev, p=p)


# ============================================================================ 2. disparo
def frobenius(l, delta, E, K=10, coulomb=False):
    """Coeficientes a_k de u = r^{l+1} sum_k a_k r^k (a_0 = 1) para 2V - 2E = sum_{j>=-1} c_j r^j.
    Yukawa: -2 e^{-delta r}/r = sum_j -2 (-delta)^{j+1}/(j+1)! r^j. Recurrencia k(k+2l+1) a_k = sum_j c_j a_{k-2-j}."""
    c = {}
    for j in range(-1, K):
        c[j] = -2.0 if j == -1 else (0.0 if coulomb else -2.0 * (-delta)**(j + 1) / math.factorial(j + 1))
    c[0] += -2.0 * E
    a = [1.0]
    for k in range(1, K + 1):
        s = sum(c[j] * a[k - 2 - j] for j in range(-1, k - 1))
        a.append(s / (k * (k + 2 * l + 1)))
    return a


def _inicio(l, delta, E, r0, coulomb):
    a = frobenius(l, delta, E, coulomb=coulomb)
    u = sum(ak * r0**(k + l + 1) for k, ak in enumerate(a))
    up = sum(ak * (k + l + 1) * r0**(k + l) for k, ak in enumerate(a))
    return u, up


def _rhs(l, delta, E, coulomb, momentos):
    cl = l * (l + 1)
    if coulomb:
        def f2(r):
            return cl / (r * r) - 2.0 / r - 2.0 * E
    else:
        def f2(r):
            return cl / (r * r) - 2.0 * math.exp(-delta * r) / r - 2.0 * E
    if not momentos:
        return lambda r, y: [y[1], f2(r) * y[0]]
    if coulomb:
        return lambda r, y: [y[1], f2(r) * y[0], y[0]**2, r * y[0]**2, r * r * y[0]**2, 0.0]
    return lambda r, y: [y[1], f2(r) * y[0], y[0]**2, r * y[0]**2, r * r * y[0]**2,
                         math.exp(-delta * r) * y[0]**2]


def _nodo(r, y):
    return y[0]


def coef_ext(l, kappa):
    """c_j (j = 0..l) de w(r) = e^{-kappa r} sum_j c_j r^{-j}, normalizada a r^{-l} cuando kappa -> 0.
    b_j = (l+j)!/(j!(l-j)! 2^j) (polinomio de Bessel inverso), c_j = b_j kappa^{l-j}/b_l."""
    b = [math.factorial(l + j) / (math.factorial(j) * math.factorial(l - j) * 2**j) for j in range(l + 1)]
    return [b[j] * kappa**(l - j) / b[l] for j in range(l + 1)]


def w_ext(l, kappa, r, r_ref):
    """w y w' con el factor e^{-kappa (r - r_ref)} (escalado para no desbordar)."""
    c = coef_ext(l, kappa)
    P = sum(cj * r**(-j) for j, cj in enumerate(c))
    dP = sum(-j * cj * r**(-j - 1) for j, cj in enumerate(c))
    e = math.exp(-kappa * (r - r_ref))
    return e * P, e * (-kappa * P + dP)


def cola_ext(l, kappa, r_e, n):
    """int_{r_e}^inf r^n w(r)^2 dr con w = e^{-kappa (r - r_e)} sum_j c_j r^{-j} (forma cerrada, mpmath)."""
    import mpmath as mp
    mp.mp.dps = 30
    c = coef_ext(l, kappa)
    tot = mp.mpf(0)
    for i, ci in enumerate(c):
        for j, cj in enumerate(c):
            m = n - i - j
            if kappa == 0:
                if m >= -1:
                    return float("inf")
                J = mp.mpf(r_e)**(m + 1) / (-(m + 1))
            else:
                k2 = 2 * mp.mpf(kappa)
                J = mp.exp(k2 * r_e) * k2**(-(m + 1)) * mp.gammainc(m + 1, k2 * r_e)
            tot += ci * cj * J
    return float(tot)


def _whittaker(l, kappa, r):
    """W_{1/kappa, l+1/2}(2 kappa r) y su derivada en r (Coulomb puro), con mpmath."""
    import mpmath as mp
    mp.mp.dps = 30
    k, m = 1 / mp.mpf(kappa), mp.mpf(l) + mp.mpf(1) / 2
    f = lambda rr: mp.whitw(k, m, 2 * kappa * rr)
    return float(f(r)), float(mp.diff(f, r))


def _cola_whittaker(l, kappa, r_e, n):
    import mpmath as mp
    mp.mp.dps = 30
    k, m = 1 / mp.mpf(kappa), mp.mpf(l) + mp.mpf(1) / 2
    w0 = mp.whitw(k, m, 2 * kappa * r_e)
    return float(mp.quad(lambda rr: rr**n * (mp.whitw(k, m, 2 * kappa * rr) / w0)**2, [r_e, 2 * r_e, mp.inf]))


def r_externo(delta):
    return 42.0 / delta


class Disparo:
    """Problema de un estado ligado de la onda parcial l para Yukawa (delta > 0) o Coulomb (delta = 0)."""

    def __init__(self, l, delta, r0=1e-3, r_m=None, r_ext=None):
        self.l, self.delta = l, float(delta)
        self.coulomb = (delta == 0)
        self.r0 = r0
        self.r_ext_fijo = r_ext
        self.r_m_fijo = r_m

    def radios(self, kappa):
        if self.r_ext_fijo is not None:
            rext = self.r_ext_fijo
        elif self.coulomb:
            rext = 60.0 / kappa + 20.0
        else:
            rext = r_externo(self.delta)
            if kappa > 0:
                rext = min(rext, 60.0 / kappa + 2.0 / self.delta)
        if self.r_m_fijo is not None:
            rm = self.r_m_fijo
        elif self.coulomb:
            rm = 3.7 * (self.l + 1)**2
        else:
            rm = min(max(2.0 / self.delta, 2.0), rext / 3)
        return rm, rext

    def afuera(self, E, rm, momentos=False, nodos=False):
        u0, up0 = _inicio(self.l, self.delta, E, self.r0, self.coulomb)
        y0 = [u0, up0] + ([0.0] * 4 if momentos else [])
        if momentos:   # momentos de [0, r0] con el termino dominante r^{2l+2}
            p = 2 * self.l + 2
            y0[2:] = [self.r0**(p + 1) / (p + 1), self.r0**(p + 2) / (p + 2), self.r0**(p + 3) / (p + 3),
                      self.r0**(p + 1) / (p + 1)]
        s = solve_ivp(_rhs(self.l, self.delta, E, self.coulomb, momentos), [self.r0, rm], y0, method="DOP853",
                      rtol=RTOL, atol=ATOL, events=_nodo if nodos else None)
        return s

    def adentro(self, E, rm, rext, momentos=False, nodos=False):
        kappa = math.sqrt(-2 * E)
        if self.coulomb:
            w, wp = _whittaker(self.l, kappa, rext)
            w, wp = 1.0, wp / w
        else:
            w, wp = w_ext(self.l, kappa, rext, rext)
        y0 = [w, wp] + ([0.0] * 4 if momentos else [])
        s = solve_ivp(_rhs(self.l, self.delta, E, self.coulomb, momentos), [rext, rm], y0, method="DOP853",
                      rtol=RTOL, atol=ATOL, events=_nodo if nodos else None)
        return s, w

    def desajuste(self, kappa):
        E = -0.5 * kappa**2
        rm, rext = self.radios(kappa)
        so = self.afuera(E, rm)
        si, _ = self.adentro(E, rm, rext)
        uo, upo = so.y[0, -1], so.y[1, -1]
        ui, upi = si.y[0, -1], si.y[1, -1]
        return (upo * ui - uo * upi) / (math.hypot(uo, rm * upo) * math.hypot(ui, rm * upi)) * rm

    def resolver(self, kappa_guess, factor=1.05, xtol_rel=1e-14, nr=None):
        """Busca la raiz del desajuste en kappa cerca de kappa_guess (ampliando el intervalo)."""
        lo, hi = kappa_guess / factor, kappa_guess * factor
        flo, fhi = self.desajuste(lo), self.desajuste(hi)
        it = 0
        while flo * fhi > 0:
            it += 1
            if it > 40:
                raise RuntimeError("no se encontro cambio de signo")
            lo, hi = lo / factor, hi * factor
            flo, fhi = self.desajuste(lo), self.desajuste(hi)
        kap = brentq(self.desajuste, lo, hi, xtol=xtol_rel * kappa_guess * 1e-2, rtol=8.9e-16, maxiter=200)
        return self.estado(kap, nr=nr)

    def estado(self, kappa, nr=None):
        """Normalizacion, momentos y nodos de la solucion empalmada en kappa."""
        E = -0.5 * kappa**2
        rm, rext = self.radios(kappa)
        so = self.afuera(E, rm, momentos=True, nodos=True)
        si, w = self.adentro(E, rm, rext, momentos=True, nodos=True)
        uo, upo, ui, upi = so.y[0, -1], so.y[1, -1], si.y[0, -1], si.y[1, -1]
        so_ = 1.0 / math.hypot(uo, rm * upo)
        # escala de la solucion interior que la empalma con la exterior (minimos cuadrados en (u, r_m u'),
        # robusto aunque r_m caiga cerca de un nodo)
        si_ = so_ * (uo * ui + rm**2 * upo * upi) / (ui**2 + rm**2 * upi**2)
        I_o = so.y[2:, -1] * so_**2
        I_i = -si.y[2:, -1] * si_**2        # integrado de rext a rm: cambia el signo
        if self.coulomb:
            cola = np.array([_cola_whittaker(self.l, kappa, rext, n) for n in (0, 1, 2)] + [0.0]) * si_**2
        else:
            cola = np.array([cola_ext(self.l, kappa, rext, n) for n in (0, 1, 2)]
                            + [0.0]) * si_**2
        I = I_o + I_i + cola
        nodos = len(so.t_events[0]) + len(si.t_events[0])
        dlog = (upo * so_ - upi * si_) * rm      # salto de r_m u' entre las dos ramas (escala 1)
        out = dict(l=self.l, delta=self.delta, kappa=kappa, E=E, r_med=I[1] / I[0], r2_med=I[2] / I[0],
                   HF=I[3] / I[0], nodos=nodos, r_m=rm, r_ext=rext,
                   frac_cola=float(cola[0] / I[0]), frac_cola_r2=float(cola[2] / I[2]),
                   salto_dlog=float(dlog))
        if nr is not None and nodos != nr:
            raise RuntimeError(f"nodos = {nodos}, se esperaban {nr} (l={self.l}, delta={self.delta}, kappa={kappa})")
        return out


def ligado(l, delta, kappa_guess, nr=None, **kw):
    return Disparo(l, delta, **kw).resolver(kappa_guess, nr=nr)


# ---------------------------------------------------------------------------- energia cero y umbral
def energia_cero(l, delta, rext=None, momentos=True, r0=1e-3):
    """Integra la solucion regular a E = 0 hasta rext y la descompone u = A r^{-l} + B r^{l+1} alli."""
    rext = r_externo(delta) if rext is None else rext
    u0, up0 = _inicio(l, delta, 0.0, r0, False)
    y0 = [u0, up0] + ([0.0] * 4 if momentos else [])
    if momentos:
        p = 2 * l + 2
        y0[2:] = [r0**(p + 1) / (p + 1), r0**(p + 2) / (p + 2), r0**(p + 3) / (p + 3), r0**(p + 1) / (p + 1)]
    s = solve_ivp(_rhs(l, delta, 0.0, False, momentos), [r0, rext], y0, method="DOP853", rtol=RTOL, atol=ATOL,
                  events=_nodo)
    u, up = s.y[0, -1], s.y[1, -1]
    A = ((l + 1) * u - rext * up) * rext**l / (2 * l + 1)
    B = (l * u + rext * up) * rext**(-l - 1) / (2 * l + 1)
    return dict(A=A, B=B, u=u, up=up, rext=rext, I=s.y[2:, -1] if momentos else None, nodos=s.t_events[0])


def umbral(l, a, b, xtol=1e-15, r0=1e-3):
    rext = r_externo(a)

    def g(d):
        z = energia_cero(l, d, rext=rext, momentos=False, r0=r0)
        x = z["B"] * rext**(2 * l + 1)
        return x / math.hypot(z["A"], x)
    return brentq(g, a, b, xtol=xtol, rtol=8.9e-16, maxiter=200)


def estado_umbral(l, dc):
    """Constantes de la solucion de energia cero en el umbral, normalizada (l >= 1) o con u -> 1 (l = 0).
    l >= 1:  An2 = A^2/N (amplitud de la cola u0 -> A r^{-l} de la solucion normalizada), S = <e^{-delta r}>,
             l = 1: C0 = lim_L [int_0^L r u0^2 - An2 ln L]; <r^2> diverge;
             l = 2: <r>_0 y <r^2>_0 finitos.
    l = 0:   Sigma = int e^{-delta r} ubar^2 con ubar -> 1 (d(1/a)/d delta = -2 Sigma)."""
    rext = r_externo(dc)
    z = energia_cero(l, dc, rext=rext)
    A, I = z["A"], z["I"]
    out = dict(l=l, delta_c=dc, rext=rext, A_crudo=A, B_crudo=z["B"], B_sobre_A_rext=z["B"] * rext**(2 * l + 1) / A,
               nodos_internos=len(z["nodos"]))
    if l == 0:
        out["Sigma"] = I[3] / A**2
        out["c0_pred"] = 2 * out["Sigma"]
        return out
    N = I[0] + A**2 * rext**(1 - 2 * l) / (2 * l - 1)
    out["N"] = N
    out["An2"] = A**2 / N
    out["S"] = I[3] / N
    out["frac_cola_norma"] = A**2 * rext**(1 - 2 * l) / (2 * l - 1) / N
    if l == 1:
        out["C0"] = I[1] / N - out["An2"] * math.log(rext)
        out["D0"] = I[2] / N - out["An2"] * rext
    if l >= 2:
        out["r_med0"] = (I[1] + A**2 * rext**(2 - 2 * l) / (2 * l - 2)) / N
    if l >= 3 or l == 2:
        out["r2_med0"] = (I[2] + A**2 * rext**(3 - 2 * l) / (2 * l - 3)) / N
    return out


# ---------------------------------------------------------------------------- caja de Dirichlet por disparo
def u_en_R(l, delta, E, R, r0=1e-3, nodos=False):
    u0, up0 = _inicio(l, delta, E, r0, delta == 0)
    s = solve_ivp(_rhs(l, delta, E, delta == 0, False), [r0, R], [u0, up0], method="DOP853", rtol=RTOL, atol=ATOL,
                  events=_nodo if nodos else None)
    if nodos:
        return s.y[0, -1], len(s.t_events[0])
    return s.y[0, -1]


def caja_disparo(l, delta, R, E_lo, E_hi, r0=1e-3):
    """Autovalor de la caja [0, R] con u(R) = 0 en [E_lo, E_hi] (debe haber cambio de signo de u(R))."""
    f = lambda E: u_en_R(l, delta, E, R, r0)
    E = brentq(f, E_lo, E_hi, xtol=1e-300, rtol=8.9e-16, maxiter=300)
    return E


def nodo_energia_cero(l, delta, k, rmax, r0=1e-3):
    """Posicion del k-esimo nodo (k = 1, 2, ...) de la solucion regular a E = 0 en (0, rmax]; None si no hay.
    Por Sturm, es el radio de la caja de Dirichlet en el que el k-esimo nivel de la onda l pasa por E = 0."""
    u0, up0 = _inicio(l, delta, 0.0, r0, False)
    s = solve_ivp(_rhs(l, delta, 0.0, False, False), [r0, rmax], [u0, up0], method="DOP853", rtol=RTOL, atol=ATOL,
                  events=_nodo)
    t = s.t_events[0]
    return float(t[k - 1]) if len(t) >= k else None
