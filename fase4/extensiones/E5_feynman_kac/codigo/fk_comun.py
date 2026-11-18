"""fk_comun.py -- Proyecto 05, Fase 4, extension E5: utilidades comunes (EDO y Monte Carlo de caminos brownianos).

Unidades hbar = m = g = 1, generador (1/2) Laplaciano, V(r) = -e^{-delta r}/r. Escribimos q = -V = e^{-delta r}/r >= 0.

Representacion de Feynman-Kac a energia cero (delta > delta_c):
    phi(x) = E_x[ exp( int_0^inf q(B_t) dt ) ],   -1/2 Lap phi + V phi = 0,   phi(r) -> 1 - a/r,
    a = 2 int_0^inf r^2 V(r) phi(r) dr  (a < 0 sin ligado; convencion del grupo: a > 0 con ligado).
En radial: u = r phi, u'' = 2 V u = -2 q u, u(0) = 0. La solucion regular u~ (u~'(0) = 1) vale alpha (r - a) lejos,
y phi(r) = u~(r) / (alpha r).

Contenido
  * EDO: solucion regular u~ con DOP853 (metodo M1), fase variable de Calogero a'(r) = 2 V (r - a)^2 (metodo M2),
    ecuacion integral phi = 1 + G0 q phi resuelta por Nystrom (metodo M3, solo para el perfil).
  * Ley exacta de Lambda = int_0^inf q(B_t) dt: E_x[e^{p Lambda}] = phi_p(x) (solucion de energia cero de p q).
    Sus polos son p_k = 1/kappa_k (Birman-Schwinger), aqui p_k = delta / delta_c(k s). La ley de Lambda es la mezcla
    P(Lambda > lam) = sum_k w_k e^{-p_k lam},  w_k(r) = -u~_{p_k}(r) / (r alpha'(p_k) p_k).
  * Monte Carlo (nucleos compilados con numba, un camino tras otro, semilla fija): proceso radial de Bessel-3 con
    transicion EXACTA (norma de un gaussiano 3D) y paso adaptativo dt = eta^2 r^2. La integral de q en cada paso es la
    media EXACTA de int q sobre el puente browniano 3D entre los extremos (Yukawa promediado sobre la gaussiana del
    puente, cuadratura de 3 nodos en el tiempo). El trapecio simple NO sirve (media infinita, ver simular_libre).
    Cierre exacto fuera de R_in (si r > R_in, el camino vuelve a la esfera R_in con probabilidad R_in/r, y si vuelve se
    reinicia exactamente en R_in; si no, termina).
  * Muestreo por importancia (transformada h de Doob con phi_T): deriva grad ln phi_T (Euler en 3D), peso
    exp(-int E_L), E_L = (H phi_T)/phi_T. Con phi_T la solucion de energia cero de delta_T < delta, E_L = q_T - q >= 0.
    Cierre exacto: phi_T = 1 + A/r fuera de R_in, probabilidad de volver (R_in + A)/(r + A).
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

DELTA_C = 1.1906124210606       # 1s, referencia del proyecto (Fase 3)
DELTA_C2 = 0.31020928           # 2s, prototipos/umbrales_energia_cero.py (propuesta, seccion 3); se recalcula en 01


def q_yuk(r, d):
    return np.exp(-d * r) / r


# ----------------------------------------------------------------------------------------------- EDO, metodo M1
def regular(qfun, p=1.0, Rf=None, r_eval=None, rtol=1e-12, atol=1e-30, con_derivada_p=False, r0=1e-10, cortes=None):
    """Solucion regular de u'' = -2 p q(r) u, u(0) = 0, u'(0) = 1 (Frobenius: q ~ 1/r => u = r - p r^2).
    Devuelve dict con u, up en r_eval y en Rf; si con_derivada_p, tambien v = du/dp y v'."""
    if con_derivada_p:
        def f(r, s):
            qq = qfun(r)
            return [s[1], -2 * p * qq * s[0], s[3], -2 * qq * s[0] - 2 * p * qq * s[2]]
        y0 = [r0 - p * r0 ** 2, 1 - 2 * p * r0, -r0 ** 2, -2 * r0]
    else:
        def f(r, s):
            return [s[1], -2 * p * qfun(r) * s[0]]
        y0 = [r0 - p * r0 ** 2, 1 - 2 * p * r0]
    # integracion por tramos (cortes = discontinuidades de q, p. ej. el pozo cuadrado del control de Ciesielski-Taylor)
    bordes = [r0] + [c for c in (cortes or []) if r0 < c < Rf] + [Rf]
    sols = []
    for i in range(len(bordes) - 1):
        sol = solve_ivp(f, [bordes[i], bordes[i + 1]], y0, method="DOP853", rtol=rtol, atol=atol,
                        dense_output=r_eval is not None)
        sols.append(sol)
        y0 = sol.y[:, -1]
    out = dict(uR=sol.y[0, -1], upR=sol.y[1, -1], Rf=Rf)
    if con_derivada_p:
        out.update(vR=sol.y[2, -1], vpR=sol.y[3, -1])
    if r_eval is not None:
        re_ = np.asarray(r_eval, float)
        k = np.clip(np.searchsorted(bordes, re_, side="right") - 1, 0, len(sols) - 1)
        Y = np.empty((len(y0), re_.size))
        for i, s_ in enumerate(sols):
            m = k == i
            if m.any():
                Y[:, m] = s_.sol(re_[m])
        out.update(u=Y[0], up=Y[1])
        if con_derivada_p:
            out.update(v=Y[2], vp=Y[3])
    return out


def a_disparo(d, Rf=None):
    """Longitud de dispersion por disparo lineal (M1). Rf con delta Rf = 60 (q(Rf) ~ 1e-28)."""
    Rf = Rf if Rf is not None else 60.0 / d
    s = regular(lambda r: q_yuk(r, d), Rf=Rf)
    return float(Rf - s["uR"] / s["upR"])


def a_fase_variable(d, Rf=None):
    """M2: fase variable a energia cero (Calogero): da/dr = 2 V(r) (r - a)^2, a(0) = 0. Independiente de M1."""
    Rf = Rf if Rf is not None else 60.0 / d
    f = lambda r, a: [-2.0 * q_yuk(r, d) * (r - a[0]) ** 2]
    s = solve_ivp(f, [1e-12, Rf], [0.0], method="DOP853", rtol=1e-13, atol=1e-14)
    return float(s.y[0, -1])


def phi_edo(d, r, Rf=None):
    """Perfil phi(r) = u~(r)/(alpha r) (M1) normalizado a 1 en el infinito."""
    Rf = Rf if Rf is not None else 60.0 / d
    r = np.atleast_1d(np.asarray(r, float))
    s = regular(lambda x: q_yuk(x, d), Rf=Rf, r_eval=np.maximum(r, 1e-9))
    alpha = s["upR"]
    return s["u"] / (alpha * np.maximum(r, 1e-9)), alpha


def phi_nystrom(d, r_eval, n_pan=600, n_gl=8, Rf=None):
    """M3: phi(r) = 1 + int_0^inf 2 r'^2 q(r') phi(r') / max(r, r') dr' (Green radial de -1/2 Lap), Nystrom con
    Gauss-Legendre compuesto en x = sqrt(r') (concentra nodos cerca del origen). Devuelve phi(r_eval) y a."""
    Rf = Rf if Rf is not None else 60.0 / d
    xg, wg = np.polynomial.legendre.leggauss(n_gl)
    edges = np.linspace(0, np.sqrt(Rf), n_pan + 1)
    X = ((edges[:-1, None] + edges[1:, None]) / 2 + (edges[1:, None] - edges[:-1, None]) / 2 * xg).ravel()
    WX = (np.broadcast_to((edges[1:, None] - edges[:-1, None]) / 2 * wg, (n_pan, n_gl))).ravel()
    R = X ** 2
    W = WX * 2 * X                          # dr = 2 x dx
    g = 2 * R ** 2 * q_yuk(R, d) * W        # 2 r'^2 q(r') dr'
    K = g[None, :] / np.maximum(R[:, None], R[None, :])
    # Sustraccion de la singularidad (el nucleo tiene un quiebre en r' = r): phi(r') = phi(r) + [phi(r') - phi(r)],
    # con S(r) = int_0^inf 2 r'^2 q(r') / max(r, r') dr' en forma cerrada.
    S = lambda x: 2 * (1 - np.exp(-d * x) * (1 + d * x)) / (d * d * x) + 2 * np.exp(-d * x) / d
    M = -K.copy()
    M[np.diag_indices_from(M)] += 1 - S(R) + K.sum(1)
    phi_n = np.linalg.solve(M, np.ones(len(R)))
    r_eval = np.atleast_1d(np.asarray(r_eval, float))
    Ke = g[None, :] / np.maximum(r_eval[:, None], R[None, :])
    # phi en r_eval por la propia ecuacion (r_eval no es nodo; error ~1e-7 por el quiebre)
    phi_r = 1 + (Ke * phi_n[None, :]).sum(1)
    a = -float((g * phi_n).sum())
    return phi_r, a


# ------------------------------------------------------------------------------------- ley exacta de Lambda
def alpha_de_p(qfun, p, Rf, cortes=None):
    return regular(qfun, p=p, Rf=Rf, cortes=cortes)["upR"]


def polos(qfun, Rf, p_max, n_scan=400, cortes=None):
    """Ceros p_k de alpha(p) en (0, p_max): polos de E[e^{p Lambda}]. Barrido y brentq."""
    ps = np.linspace(1e-3, p_max, n_scan)
    al = np.array([alpha_de_p(qfun, p, Rf, cortes) for p in ps])
    raices = []
    for i in range(n_scan - 1):
        if np.sign(al[i]) != np.sign(al[i + 1]):
            raices.append(brentq(lambda p: alpha_de_p(qfun, p, Rf, cortes), ps[i], ps[i + 1], xtol=1e-14, rtol=1e-15))
    return raices


def pesos_mezcla(qfun, Rf, pk, r_eval, cortes=None):
    """w_k(r) = -u~_{p_k}(r) / (r alpha'(p_k) p_k) en los puntos r_eval (r_eval > 0)."""
    r_eval = np.atleast_1d(np.asarray(r_eval, float))
    s = regular(qfun, p=pk, Rf=Rf, r_eval=r_eval, con_derivada_p=True, cortes=cortes)
    dalpha = s["vpR"]
    return -s["u"] / (r_eval * dalpha * pk), float(s["upR"]), float(dalpha)


# ------------------------------------------------------------- Yukawa promediado sobre una gaussiana 3D
from scipy.special import erfc as _erfc, erfcx as _erfcx


def q_gauss(R, sig, d):
    """E[ e^{-d|X|}/|X| ] con X ~ N(m, sig^2 I_3), R = |m|. Forma cerrada (convolucion del Yukawa con la gaussiana):
    f = [e^{d^2 s^2/2 - d R} erfc((d s^2 - R)/(s sqrt2)) - e^{d^2 s^2/2 + d R} erfc((d s^2 + R)/(s sqrt2))] / (2R),
    escrita con erfcx para que no haya desbordes. Para R/s < 1e-5 se usa el valor en R = 0. Acotada por sqrt(2/pi)/s."""
    R = np.asarray(R, float)
    sig = np.asarray(sig, float) * np.ones_like(R)
    A = (d * sig ** 2 - R) / (sig * np.sqrt(2.0))
    B = (d * sig ** 2 + R) / (sig * np.sqrt(2.0))
    g = np.exp(-R ** 2 / (2 * sig ** 2))
    T1 = np.where(A <= 0, np.exp(np.minimum(d * d * sig ** 2 / 2 - d * R, 700)) * _erfc(np.minimum(A, 0)),
                  g * _erfcx(np.maximum(A, 0)))
    T2 = g * _erfcx(B)
    Rs = np.maximum(R, 1e-300)
    f = (T1 - T2) / (2 * Rs)
    f0 = np.sqrt(2 / np.pi) / sig * (1 - d * sig * np.sqrt(np.pi / 2) * _erfcx(d * sig / np.sqrt(2)))
    return np.where(R < 1e-5 * sig, f0, f)



# ------------------------------------------------------------------------------------- Monte Carlo (numba)
import math
from numba import njit

_GLT = np.array([(1 - math.sqrt(0.6)) / 2, 0.5, (1 + math.sqrt(0.6)) / 2])   # Gauss-Legendre de 3 nodos en (0, 1)
_GLW = np.array([5 / 18, 8 / 18, 5 / 18])
_SQ2 = math.sqrt(2.0)


@njit(cache=True)
def _q_gauss1(R, sig, d):
    """E[e^{-d|X|}/|X|], X ~ N(m, sig^2 I_3), R = |m| (forma cerrada; ver q_gauss)."""
    if R < 1e-5 * sig:
        x = d * sig / _SQ2
        return math.sqrt(2 / math.pi) / sig * (1 - d * sig * math.sqrt(math.pi / 2) * math.exp(x * x) * math.erfc(x))
    e = d * d * sig * sig / 2
    if R > 8.0 * sig:
        # lejos de la singularidad el Yukawa es autofuncion del laplaciano (Lap q = d^2 q): la media gaussiana es
        # exactamente q(R) e^{d^2 sig^2/2} salvo erfc(R/(sig sqrt2) - ...) < 1e-14 (mismo valor que la forma cerrada)
        return math.exp(e - d * R) / R
    A = (d * sig * sig - R) / (sig * _SQ2)
    B = (d * sig * sig + R) / (sig * _SQ2)
    T1 = math.exp(e - d * R) * math.erfc(A)
    T2 = math.exp(e + d * R) * math.erfc(B)
    return (T1 - T2) / (2 * R)


@njit(cache=True)
def _int_puente(r, z1, rho2, dt, d):
    sdt = math.sqrt(dt)
    tot = 0.0
    for j in range(3):
        t = _GLT[j]
        m = math.sqrt((r + t * sdt * z1) ** 2 + t * t * dt * rho2)
        tot += _GLW[j] * _q_gauss1(m, math.sqrt(t * (1 - t) * dt), d)
    return tot * dt


def integral_puente(r, z1, rho2, dt, d):
    """Version vectorizada (para pruebas) de la media de int q sobre el puente browniano."""
    sdt = np.sqrt(dt)
    tot = 0.0
    for t, w in zip(_GLT, _GLW):
        m = np.sqrt((r + t * sdt * z1) ** 2 + (t * t) * dt * rho2)
        tot = tot + w * q_gauss(m, np.sqrt(t * (1 - t) * dt), d)
    return tot * dt


@njit(cache=True)
def _kernel_libre(r0, d, eta, R_in, seed, metodo, max_pasos):
    np.random.seed(seed)
    N = r0.size
    Lam = np.empty(N)
    pasos = np.empty(N, dtype=np.int64)
    for i in range(N):
        r = r0[i]
        L = 0.0
        n = 0
        while True:
            dt = (eta * r) ** 2
            sdt = math.sqrt(dt)
            z = np.random.standard_normal()
            chi2 = -2.0 * math.log(1.0 - np.random.random())     # z2^2 + z3^2 (chi^2 con 2 grados)
            rn = math.sqrt((r + sdt * z) ** 2 + dt * chi2)
            if metodo == 0:
                L += _int_puente(r, z, chi2, dt, d)
            else:
                L += 0.5 * (math.exp(-d * r) / r + math.exp(-d * rn) / rn) * dt
            n += 1
            if rn > R_in:
                if np.random.random() < R_in / rn:
                    rn = R_in
                else:
                    break
            r = rn
            if n >= max_pasos:
                L = -1.0      # marca de camino truncado
                break
        Lam[i] = L
        pasos[i] = n
    return Lam, pasos


def simular_libre(r0, d, eta, R_in, seed, metodo="puente", max_pasos=200_000_000, devolver_pasos=False):
    """Lambda = int_0^inf q(B_t) dt para caminos que parten de los radios r0. Bessel-3 exacto con dt = eta^2 r^2.
      metodo = "puente":   media EXACTA de int q sobre el puente browniano entre los extremos;
      metodo = "trapecio": dt (q(r) + q(r'))/2. NO SIRVE: q(r') dt ~ eta^2 r^2 / r' y r' puede caer muy cerca del
                           origen; como la densidad de r' cerca de 0 va como r'^2, E[exp(c/r')] = infinito y la media
                           del estimador discretizado es infinita para todo eta > 0 (se documenta en 03).
    Cierre: si r > R_in, vuelve a R_in con probabilidad R_in/r (exacto para BM 3D) o termina."""
    L, p = _kernel_libre(np.ascontiguousarray(r0, dtype=np.float64), float(d), float(eta), float(R_in), int(seed),
                         0 if metodo == "puente" else 1, int(max_pasos))
    if (L < 0).any():
        raise RuntimeError(f"{int((L < 0).sum())} caminos truncados")
    return (L, p) if devolver_pasos else L


# ------------------------------------------------------------------------- muestreo por importancia (MI)
class Guia:
    """phi_T = solucion de energia cero normalizada del Yukawa con delta_T (delta_c < delta_T), tabulada en [0, R_in] en
    una rejilla uniforme (h = R_in/n_tab); fuera, phi_T = 1 + A/r con A = -a_T. Deriva b(r) = phi_T'/phi_T; energia
    local E_L = (H phi_T)/phi_T = q_T - q >= 0 para el Yukawa objetivo con delta > delta_T."""

    def __init__(self, d, dT, R_in, n_tab=400000):
        self.d, self.dT, self.R_in = d, dT, R_in
        Rf = max(60.0 / dT, R_in)
        self.h = R_in / n_tab
        self.rt = np.linspace(0, R_in, n_tab + 1)
        s = regular(lambda x: q_yuk(x, dT), Rf=Rf, r_eval=np.maximum(self.rt, 1e-9))
        alpha = s["upR"]
        self.aT = float(Rf - s["uR"] / s["upR"])
        self.A = -self.aT
        rr = np.maximum(self.rt, 1e-9)
        self.phiT_tab = s["u"] / (alpha * rr)
        self.b_tab = s["up"] / s["u"] - 1.0 / rr      # (u/r)'/(u/r)
        self.b_tab[0] = self.b_tab[1]                 # limite r -> 0 (cancelacion numerica en 1e-9)
        self.b1_tab = s["up"] / s["u"]                # u_T'/u_T: deriva del proceso RADIAL guiado (1/r + b)
        self.b1_tab[0] = self.b1_tab[1]
        self.rc = 1.0 / dT                            # cambio de imagen: 3D para r < rc, radial 1D para r >= rc
        self.alpha = alpha

    def phiT(self, r):
        r = np.asarray(r, float)
        return np.where(r <= self.R_in, np.interp(r, self.rt, self.phiT_tab), 1 + self.A / np.maximum(r, 1e-300))


@njit(cache=True)
def _EL(r, d, dT):
    if r < 1e-12:
        return d - dT
    return math.exp(-dT * r) * (-math.expm1(-(d - dT) * r)) / r


@njit(cache=True)
def _kernel_guiado(r0, d, dT, R_in, A, h, btab, b1tab, rc, eta, seed, max_pasos):
    """Paso hibrido. Para r < rc (cerca del origen): imagen 3D, la parte de Bessel-3 es exacta (norma del gaussiano 3D)
    y la deriva acotada grad ln phi_T va por Euler. Para r >= rc: imagen radial 1D, Euler con la deriva total
    u_T'/u_T = 1/r + phi_T'/phi_T, que es pequena (~ 1/(r + A)) donde las dos derivas grandes (+1/r de Bessel y
    ~ -1/r de la guia) se cancelan; asi el error de Euler no se aplica a cada una por separado."""
    np.random.seed(seed)
    N = r0.size
    Lout = np.empty(N)
    pasos = np.empty(N, dtype=np.int64)
    nt = btab.size - 1
    for i in range(N):
        r = r0[i]
        L = 0.0
        n = 0
        er = _EL(r, d, dT)
        while True:
            dt = (eta * r) ** 2
            sdt = math.sqrt(dt)
            x = r / h
            k = int(x)
            z = np.random.standard_normal()
            if r < rc:
                f = x - k
                b = btab[k] * (1 - f) + btab[k + 1] * f
                chi2 = -2.0 * math.log(1.0 - np.random.random())
                rn = math.sqrt((r + b * dt + sdt * z) ** 2 + dt * chi2)
            else:
                if k >= nt:
                    b1 = 1.0 / (r + A)
                else:
                    f = x - k
                    b1 = b1tab[k] * (1 - f) + b1tab[k + 1] * f
                rn = r + b1 * dt + sdt * z
                if rn < 0.0:
                    rn = -rn
            en = _EL(rn, d, dT)
            L += 0.5 * (er + en) * dt        # E_L acotada (<= delta - delta_T): el trapecio no tiene problema aqui
            n += 1
            if rn > R_in:
                if np.random.random() < (R_in + A) / (rn + A):
                    rn = R_in
                    en = _EL(rn, d, dT)
                else:
                    break
            r = rn
            er = en
            if n >= max_pasos:
                L = np.nan     # marca de camino truncado (L puede ser negativo si E_L < 0)
                break
        Lout[i] = L
        pasos[i] = n
    return Lout, pasos


def simular_guiado(r0, guia, eta, seed, max_pasos=2_000_000_000, devolver_pasos=False):
    """Difusion guiada a energia cero: dX = grad ln phi_T dt + dB (paso hibrido, ver _kernel_guiado), dt = eta^2 r^2,
    log-peso -int E_L (trapecio). Devuelve Lg = int E_L dt (>= 0); el estimador es phi_T(r0) exp(-Lg) <= phi_T(r0)."""
    L, p = _kernel_guiado(np.ascontiguousarray(r0, dtype=np.float64), float(guia.d), float(guia.dT), float(guia.R_in),
                          float(guia.A), float(guia.h), guia.b_tab, guia.b1_tab, float(guia.rc), float(eta), int(seed),
                          int(max_pasos))
    if np.isnan(L).any():
        raise RuntimeError(f"{int(np.isnan(L).sum())} caminos guiados truncados")
    return (L, p) if devolver_pasos else L


def dT_para_razon(d, razon=1.25):
    """delta_T con a_T = razon * a (regla fijada antes: 1/a_T = 0.8/a)."""
    a = a_disparo(d)
    return brentq(lambda x: a_disparo(x) - razon * a, DELTA_C + 1e-7, d - 1e-9, xtol=1e-13)
