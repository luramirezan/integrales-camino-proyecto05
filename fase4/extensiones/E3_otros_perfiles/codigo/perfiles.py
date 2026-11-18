"""perfiles.py -- E3 (Fase 4, proyecto 05): otros perfiles de apantallamiento.

Unidades hbar = m = g = 1. Todos los perfiles se comportan como -1/r + W(r) cerca del origen, con W acotado y
suave, y decaen exponencialmente con escala 1/delta:

  yukawa : V = -e^{-d r}/r                         W = (1 - e^{-d r})/r                    W(0) = d
  ecsc   : V = -e^{-d r} cos(d r)/r                W = (1 - e^{-d r} cos(d r))/r           W(0) = d
  hulthen: V = -d e^{-d r}/(1 - e^{-d r})          W = 1/r - d/(e^{d r} - 1)               W(0) = d/2
  hatomo : V = -(1/r + d/2) e^{-d r}               W = (1 - e^{-d r})/r + (d/2) e^{-d r}  ... (ver W_hatomo)
           (potencial electrostatico de un atomo de hidrogeno 1s con radio de Bohr 2/d, visto por una carga
           unidad: con d = 2 es el potencial estatico e-H en unidades atomicas, V = -(1 + 1/r) e^{-2r}).

Herramientas (todas sin malla, con solve_ivp DOP853):
  inv_a(V, d)        1/a de la solucion de energia cero (convencion del grupo: u ~ r - a, a > 0 si hay ligado)
  cero(V, d)         dict con 1/a, r_e (formula de Bethe con la solucion de energia cero) y la integral de
                     Hellmann-Feynman c_HF = 2 int dV/dd u0^2 dr (normalizada u0 -> 1 - r/a)
  kcot(V, d, k)      k cot delta_0 por empalme con sin/cos fuera del alcance
  ligado(V, d)       kappa del 1s por disparo con empalme a la cola e^{-kappa r}, nodos y <r>, <r^2>
  caja(V, d, R)      E0 de la caja de Dirichlet de radio R por disparo (u(R) = 0), sin malla
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

R0 = 1e-6          # punto de arranque (serie de Frobenius u = r - r^2 + c3 r^3)
RTOL, ATOL = 1e-13, 1e-30


# ----------------------------------------------------------------------------------------------- potenciales
def _yuk(d):
    return lambda r: -np.exp(-d * r) / r


def _ecsc(d):
    return lambda r: -np.exp(-d * r) * np.cos(d * r) / r


def _hul(d):
    return lambda r: -d / np.expm1(d * r)


def _hat(d):
    return lambda r: -(1.0 / r + 0.5 * d) * np.exp(-d * r)


def _dyuk(d):        # dV/d(delta)
    return lambda r: np.exp(-d * r)


def _decsc(d):
    return lambda r: np.exp(-d * r) * (np.cos(d * r) + np.sin(d * r))


def _dhul(d):
    # V = -d/(e^{x}-1), x = d r: dV/dd = -1/(e^x-1) + d r e^x/(e^x-1)^2
    def f(r):
        x = d * r
        em = np.expm1(x)
        return -1.0 / em + x * np.exp(x) / em**2
    return f


def _dhat(d):
    # V = -(1/r + d/2) e^{-d r}: dV/dd = -(1/2) e^{-dr} + (1 + d r/2) e^{-d r} = (1/2 + d r/2) e^{-d r}
    return lambda r: 0.5 * (1.0 + d * r) * np.exp(-d * r)


def _wyuk(d):
    return lambda r: np.where(r > 1e-12, -np.expm1(-d * r) / np.maximum(r, 1e-300), d)


def _wecsc(d):
    # W = (1 - e^{-x} cos x)/r = d (1 - e^{-x} cos x)/x; serie para x pequeno: 1 - x^2/3 + x^3/6 - x^4/30 ...
    def W(r):
        r = np.asarray(r, dtype=float)
        x = d * r
        with np.errstate(divide="ignore", invalid="ignore"):
            directo = (1.0 - np.exp(-x) * np.cos(x)) / r
        # e^{-x} cos x = 1 - x + x^3/3 - x^4/6 + x^5/30 + 0 x^6 - x^7/630 ...
        serie = d * (1.0 - x**2 / 3 + x**3 / 6 - x**4 / 30 + x**6 / 630)
        return np.where(x < 1e-3, serie, directo)
    return W


def _whul(d):
    def W(r):
        r = np.asarray(r, dtype=float)
        x = d * r
        serie = d * (0.5 - x / 12 + x**3 / 720 - x**5 / 30240)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            directo = 1.0 / r - d / np.expm1(x)
        return np.where(x < 1e-3, serie, directo)
    return W


def _what(d):
    # W = V + 1/r = (1 - e^{-x})/r - (d/2) e^{-x} = d [ (1-e^{-x})/x - e^{-x}/2 ];  W(0) = d/2
    def W(r):
        r = np.asarray(r, dtype=float)
        x = d * r
        with np.errstate(divide="ignore", invalid="ignore"):
            directo = -np.expm1(-x) / r - 0.5 * d * np.exp(-x)
        serie = d * (0.5 + 0.0 * x - x**2 / 12 + x**3 / 24)   # (1-e^-x)/x = 1 - x/2 + x^2/6 - x^3/24; e^-x/2 = 1/2 - x/2 + x^2/4 - x^3/12
        return np.where(x < 1e-3, serie, directo)
    return W


PERFILES = {
    "yukawa":  dict(V=_yuk,  dV=_dyuk,  W=_wyuk,  W0=lambda d: d,       nombre="Yukawa",
                    formula=r"$-e^{-\delta r}/r$", bracket=(1.15, 1.25)),
    "ecsc":    dict(V=_ecsc, dV=_decsc, W=_wecsc, W0=lambda d: d,       nombre="ECSC",
                    formula=r"$-e^{-\delta r}\cos(\delta r)/r$", bracket=(0.69, 0.75)),
    "hulthen": dict(V=_hul,  dV=_dhul,  W=_whul,  W0=lambda d: d / 2,   nombre="Hulthén",
                    formula=r"$-\delta e^{-\delta r}/(1-e^{-\delta r})$", bracket=(1.9, 2.1)),
    "hatomo":  dict(V=_hat,  dV=_dhat,  W=_what,  W0=lambda d: d / 2,   nombre="átomo H (estático)",
                    formula=r"$-(1/r+\delta/2)e^{-\delta r}$", bracket=(1.5, 3.0)),
}


def rmax(d, factor=60.0):
    """Radio donde |V| < e^{-factor}/r: fuera de ahi el potencial es despreciable (e^{-60} ~ 1e-26)."""
    return factor / d


def _arranque(W0, E=0.0):
    """Valores iniciales en R0 desde la serie de Frobenius de u'' = 2 (V - E) u con V = -1/r + W0 + O(r):
    u = r + c2 r^2 + c3 r^3, u'' = 2 c2 + 6 c3 r = -2 - 2 c2 r + 2 (W0 - E) r + O(r^2), de donde
    c2 = -1 y c3 = (2 + 2 W0 - 2E)/6. El error relativo en R0 = 1e-6 es O(R0^3)."""
    c2 = -1.0
    c3 = (-2.0 * c2 + 2.0 * (W0 - E)) / 6.0
    r = R0
    return [r + c2 * r**2 + c3 * r**3, 1.0 + 2 * c2 * r + 3 * c3 * r**2]


def _integrar(V, W0, E, rf, extra=None, dense=False):
    if extra is None:
        f = lambda r, y: [y[1], 2.0 * (V(r) - E) * y[0]]
        y0 = _arranque(W0, E)
    else:
        f = lambda r, y: [y[1], 2.0 * (V(r) - E) * y[0]] + list(extra(r, y))
        y0 = _arranque(W0, E) + [0.0] * 3
    return solve_ivp(f, [R0, rf], y0, method="DOP853", rtol=RTOL, atol=ATOL, dense_output=dense)


# ----------------------------------------------------------------------------------------------- energia cero
def inv_a(perfil, d, rf=None):
    p = PERFILES[perfil]
    rf = rmax(d) if rf is None else rf
    s = _integrar(p["V"](d), p["W0"](d), 0.0, rf)
    u, up = s.y[0, -1], s.y[1, -1]
    alfa = u - rf * up            # u = alfa + beta r fuera del alcance
    return float(-up / alfa)


def delta_c(perfil, xtol=1e-14):
    a, b = PERFILES[perfil]["bracket"]
    return brentq(lambda d: inv_a(perfil, d), a, b, xtol=xtol, rtol=1e-15)


def cero(perfil, d, rf=None):
    """1/a, r_e (Bethe: r_e = 2 int (psi^2 - phi^2), psi = 1 - r/a, phi = u/alfa) y c_HF = 2 int dV phi^2."""
    p = PERFILES[perfil]
    rf = rmax(d) if rf is None else rf
    V, dV = p["V"](d), p["dV"](d)
    s = _integrar(V, p["W0"](d), 0.0, rf)
    u, up = s.y[0, -1], s.y[1, -1]
    alfa = u - rf * up
    ia = -up / alfa
    # segunda pasada con las integrales (misma EDO, mismo arranque)
    def extra(r, y):
        phi = y[0] / alfa
        psi = 1.0 - r * ia
        return [psi**2 - phi**2, dV(r) * phi**2, r * phi**2]
    s2 = _integrar(V, p["W0"](d), 0.0, rf, extra=extra)
    # el tramo [0, R0] es despreciable (phi ~ r/alfa, psi ~ 1): aporta 2 R0 a r_e
    re = 2.0 * (s2.y[2, -1] + R0)
    cHF = 2.0 * s2.y[3, -1]          # = -d(1/a)/dd evaluado con la solucion normalizada a 1 - r/a
    ia2 = -s2.y[1, -1] / (s2.y[0, -1] - rf * s2.y[1, -1])
    return dict(delta=float(d), inv_a=float(ia), inv_a_2=float(ia2), r_e=float(re), c_HF=float(cHF),
                a=float(1.0 / ia) if ia != 0 else float("inf"), rf=float(rf))


def kcot(perfil, d, k, rf=None):
    """k cot delta_0 empalmando u = A sin(kr) + B cos(kr) en rf (V despreciable): tan delta_0 = B/A."""
    p = PERFILES[perfil]
    rf = rmax(d) if rf is None else rf
    s = _integrar(p["V"](d), p["W0"](d), 0.5 * k * k, rf)
    u, up = s.y[0, -1], s.y[1, -1]
    sn, cs = np.sin(k * rf), np.cos(k * rf)
    A = u * sn + up * cs / k
    B = u * cs - up * sn / k
    return float(k * A / B)


# ----------------------------------------------------------------------------------------------- estado ligado
def _G(perfil, d, kap, rf):
    p = PERFILES[perfil]
    s = _integrar(p["V"](d), p["W0"](d), -0.5 * kap * kap, rf)
    u, up = s.y[0, -1], s.y[1, -1]
    return (up + kap * u) / np.hypot(u, up)


def ligado(perfil, d, kap_guess=None, rf=None, observables=True):
    """kappa del estado fundamental: raiz de u'(rf) + kappa u(rf) = 0 (sin componente creciente e^{kappa r})."""
    rf_fijo = rf
    rf = rmax(d) if rf is None else rf

    def rfk(k):
        # para estados profundos la solucion creciente e^{kappa r} desborda si kappa rf > ~700: se acorta rf a
        # 600/kappa sin bajar de 40/delta (|V(rf)| < e^{-40}/rf). Cerca del umbral (kappa pequeno) rf = 60/delta.
        return rf if rf_fijo is not None else min(rf, max(40.0 / d, 600.0 / k))
    import warnings

    def g(k):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            return _G(perfil, d, k, rfk(k))
    if kap_guess is None:
        ks = np.geomspace(1e-7, 2.0, 120)
    else:
        ks = np.geomspace(max(kap_guess / 3, 1e-9), kap_guess * 3, 40)
    vals = [g(k) for k in ks]
    raices = []
    for i in range(len(ks) - 1):
        if np.isfinite(vals[i]) and np.isfinite(vals[i + 1]) and np.sign(vals[i]) != np.sign(vals[i + 1]):
            raices.append(brentq(g, ks[i], ks[i + 1], xtol=1e-16, rtol=1e-15))
    if not raices:
        return None
    kap = max(raices)            # el fundamental es el mas ligado
    rf = rfk(kap)
    out = dict(rf=float(rf), delta=float(d), kappa=float(kap), E0=float(-0.5 * kap**2), raices=[float(x) for x in raices])
    if observables:
        out.update(_observables_ligado(perfil, d, kap, rf))
    return out


def _observables_ligado(perfil, d, kap, rf):
    """<r>, <r^2>, nodos y fraccion de norma en la cola r > rf.
    Si kappa rf <= 10, integracion hacia afuera hasta rf (el error de redondeo amplificado por e^{kappa rf} es
    < 1e-13 e^{20}). Si kappa rf > 10 (estados profundos), la integracion hacia afuera se detiene en r_m =
    min(rf/2, 4/kappa) y desde rf se integra HACIA ADENTRO la solucion decreciente u = e^{-kappa r} (estable),
    empalmando en r_m. Corregido el 17-11-2026 tras el control V3 (Hulthen delta = 1.0, kappa rf = 30)."""
    p = PERFILES[perfil]
    V = p["V"](d)
    E = -0.5 * kap * kap
    ext = lambda r, y: [y[0]**2, r * y[0]**2, r * r * y[0]**2]
    if kap * rf <= 10:
        s = _integrar(V, p["W0"](d), E, rf, extra=ext)
        uf = s.y[0, -1]
        I = s.y[2:5, -1]
        sd = _integrar(V, p["W0"](d), E, rf, dense=True)
        rr = np.linspace(R0, rf * 0.98, 20001)
        uu = sd.sol(rr)[0]
    else:
        rm = min(rf / 2, 4.0 / kap)
        # la integracion hacia adentro empieza en rf_o = min(rf, rm + 40/kappa): mas alla, la norma relativa es
        # < e^{-80} y se evita el desborde de e^{kappa (rf - rm)}
        rf = min(rf, rm + 40.0 / kap)
        so = _integrar(V, p["W0"](d), E, rm, extra=ext)
        f = lambda r, y: [y[1], 2.0 * (V(r) - E) * y[0], y[0]**2, r * y[0]**2, r * r * y[0]**2]
        si = solve_ivp(f, [rf, rm], [1.0, -kap, 0.0, 0.0, 0.0], method="DOP853", rtol=RTOL, atol=ATOL, dense_output=True)
        esc = so.y[0, -1] / si.y[0, -1]
        # las integrales hacia adentro salen con signo menos (se integra de rf a rm)
        I = so.y[2:5, -1] - esc**2 * si.y[2:5, -1]
        uf = esc * 1.0
        sd = _integrar(V, p["W0"](d), E, rm, dense=True)
        rr1 = np.linspace(R0, rm, 10001)
        rr2 = np.linspace(rm, rf * 0.98, 10001)
        uu = np.concatenate([sd.sol(rr1)[0], esc * si.sol(rr2)[0]])
        rr = np.concatenate([rr1, rr2])
    nodos = int(np.sum(np.sign(uu[1:]) != np.sign(uu[:-1])))
    # cola analitica u = uf e^{-kap (r - rf)} para r > rf
    t0 = uf**2 / (2 * kap)
    t1 = uf**2 * (rf / (2 * kap) + 1 / (4 * kap**2))
    t2 = uf**2 * (rf**2 / (2 * kap) + rf / (2 * kap**2) + 1 / (4 * kap**3))
    n0 = I[0] + t0
    return dict(r_med=float((I[1] + t1) / n0), r2_med=float((I[2] + t2) / n0), nodos=nodos, frac_cola=float(t0 / n0))


# ----------------------------------------------------------------------------------------------- caja (disparo)
def _uR(perfil, d, E, R):
    p = PERFILES[perfil]
    s = _integrar(p["V"](d), p["W0"](d), E, R)
    return s.y[0, -1]


def caja(perfil, d, R, Elo=None, Ehi=None):
    """E0 de la caja de Dirichlet u(R) = 0 (estado sin nodos, u(R) > 0 por debajo de E0).
    Primero busca cerca del umbral, en [-2 pi^2/R^2, 1.05 pi^2/(2R^2)] (12 puntos); si no hay cambio de signo,
    barre desde Elo = -0.6 (escala logaritmica) hasta la energia libre."""
    Ehi = 1.05 * np.pi**2 / (2 * R**2) if Ehi is None else Ehi
    f = lambda E: _uR(perfil, d, E, R)
    if Elo is None:
        Es = np.linspace(-2 * np.pi**2 / R**2, Ehi, 12)
        vals = [f(E) for E in Es]
        if vals[0] > 0:
            for i in range(len(Es) - 1):
                if np.sign(vals[i]) != np.sign(vals[i + 1]):
                    return float(brentq(f, Es[i], Es[i + 1], xtol=1e-18, rtol=1e-15))
        Elo = -0.6
    Es = np.concatenate([-np.geomspace(-Elo, 1e-14, 60), np.linspace(0, Ehi, 25)[1:]])
    # muy por debajo de E0 la solucion crece como e^{sqrt(-2E) r} y desborda (inf o nan): su signo es +
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        vals = [f(E) for E in Es]
    vals = [v if np.isfinite(v) else np.inf for v in vals]
    for i in range(len(Es) - 1):
        if np.sign(vals[i]) != np.sign(vals[i + 1]):
            return float(brentq(f, Es[i], Es[i + 1], xtol=1e-18, rtol=1e-15))
    raise RuntimeError("no se encontro E0 en la caja")
