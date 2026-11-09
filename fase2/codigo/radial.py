"""radial.py -- solucionador radial de referencia (Fase 2, proyecto 05).

Ecuacion radial l=0 en unidades hbar=m=1:  -u''/2 + V(r) u = E u,  u(0)=0,  u(R)=0 (caja de Dirichlet).

Contenido
---------
resolver(V, R, h=None, N=None, nev=2)
    Diferencias finitas de 2o orden en la malla r_j = j*hh, j=1..N, hh=R/(N+1).
    Devuelve autovalores E0, E1, ..., el autovector u normalizado (int u^2 dr = 1 con la regla
    del trapecio, que aqui es hh*sum u_j^2 porque u(0)=u(R)=0) y los observables
    <r>, <r^2>, <r^2>^1/2, F_1/2 = int_0^{R/2} u^2 / int_0^R u^2 (trapecio, peso 1/2 en r=R/2
    si cae en la malla) y <r>/R.
resolver_rich(V, R, h=1/40, nev=2, p=2, N=None)
    Corre la malla hh y hh/2 (N y 2N+1 puntos interiores, mismo R) y extrapola con Richardson
    X = (2^p X_{h/2} - X_h)/(2^p - 1). p=2 es el orden de la discretizacion para V suave
    (tambien para Coulomb -1/r, que se comprueba en test_radial.py). Devuelve tambien las cifras
    de cada malla y |E_h - E_{h/2}|.
orden_aparente(V, R, hs, clave="E0", exacto=None)
    Orden aparente p con tres mallas (sin exacto) o con pares de mallas frente al valor exacto.
pendiente_energia_cero(V, R, r0=1e-8, quiebres=())
    Integra u'' = 2 V(r) u a E=0 desde r0 (u=r0, u'=1) hasta R (solve_ivp DOP853, rtol 1e-13)
    y devuelve u'(R). Fuera del alcance del potencial u = A + B r; el umbral de un nuevo
    estado ligado (l=0) es B = 0, es decir u'(R) = 0 (resonancia de energia cero).
    'quiebres': puntos donde V es discontinuo; se integra por tramos.
umbral(familia, a, b, R=200.0, quiebres=())
    brentq sobre el parametro lam en [a,b] de pendiente_energia_cero(familia(lam), R).
caja_recomendada(E0, Rmin=60, factor=25)
    R = max(Rmin, factor/kappa), kappa = sqrt(-2 E0) (receta de la seccion 5.1 de la Fase 1).

Potenciales listos: V_yukawa(delta), V_coulomb(), V_hulthen(delta), V_pozo(V0, a).
Soluciones exactas de control: hulthen_exacto(delta, n), pozo_exacto(V0, a) (usan sympy).
Pruebas: test_radial.py. Cifras de referencia: 10_radial_controles.py -> fase2/resultados/10_radial.json.
Solo usa numpy y scipy. No fija semillas porque es determinista.
"""
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

DELTA_C_REF = 1.1906124211  # Fase 1, seccion 5.3 (condicion de energia cero)


# ----------------------------------------------------------------------------- potenciales
def V_yukawa(delta):
    """V = -e^{-delta r}/r (g=1)."""
    return lambda r: -np.exp(-delta * r) / r


def V_coulomb():
    return lambda r: -1.0 / r


def V_hulthen(delta):
    """V = -delta/(e^{delta r}-1); tiende a -1/r + delta/2 en r->0 y a -delta e^{-delta r} lejos."""
    if delta == 0:
        return V_coulomb()
    return lambda r: -delta / np.expm1(delta * r)


def V_pozo(V0, a=1.0, borde="estricta"):
    """Pozo esferico cuadrado: V = -V0 para r < a, 0 para r > a.
    borde="estricta": V(a) = 0 (r<a); borde="media": V(a) = -V0/2 si r=a cae en la malla
    (valor medio del salto; es la convencion que recupera orden 2 cuando a es nodo de la malla)."""
    def V(r):
        r = np.asarray(r, dtype=float)
        v = np.where(r < a, -V0, 0.0)
        if borde == "media":
            v = np.where(np.abs(r - a) <= 1e-12 * a, -V0 / 2, v)
        return v
    return V


# ----------------------------------------------------------------------------- diferencias finitas
def _malla(R, h=None, N=None):
    if N is None:
        N = int(round(R / h)) - 1
    hh = R / (N + 1)
    return N, hh, hh * np.arange(1, N + 1)


def resolver(V, R, h=None, N=None, nev=2):
    """Un solo paso de malla. V: funcion vectorizada de r. Devuelve un dict."""
    N, hh, r = _malla(R, h, N)
    d = 1.0 / hh**2 + V(r)
    e = -0.5 / hh**2 * np.ones(N - 1)
    w, v = eigh_tridiagonal(d, e, select="i", select_range=(0, nev - 1))
    u = v[:, 0].copy()
    if u[np.argmax(np.abs(u))] < 0:
        u = -u
    u /= np.sqrt(hh * np.sum(u**2))          # int u^2 dr = 1 (trapecio con u(0)=u(R)=0)
    u2 = hh * u**2
    pesoF = np.where(r < R / 2 - 1e-12 * R, 1.0, 0.0)
    pesoF[np.abs(r - R / 2) <= 1e-9 * R] = 0.5  # trapecio: medio peso en r = R/2
    rm = float(np.sum(r * u2))
    r2 = float(np.sum(r**2 * u2))
    out = dict(R=float(R), N=int(N), h=float(hh), r=r, u=u,
               E=[float(x) for x in w], E0=float(w[0]),
               r_med=rm, r2_med=r2, r_rms=float(np.sqrt(r2)),
               F12=float(np.sum(pesoF * u2)), r_sobre_R=rm / R)
    if nev > 1:
        out["E1"] = float(w[1])
    return out


_ESCALARES = ("E0", "E1", "r_med", "r2_med", "F12", "r_sobre_R")


def resolver_rich(V, R, h=1 / 40, nev=2, p=2, N=None):
    """Mallas hh y hh/2 con el mismo R y Richardson de orden p en todos los observables."""
    if N is None:
        N = int(round(R / h)) - 1
    a = resolver(V, R, N=N, nev=nev)
    b = resolver(V, R, N=2 * N + 1, nev=nev)
    f = 2.0**p
    out = dict(R=float(R), h=a["h"], N=N, p=p)
    for k in _ESCALARES:
        if k in a:
            out[k] = (f * b[k] - a[k]) / (f - 1)
            out[k + "_h"] = a[k]
            out[k + "_h2"] = b[k]
    out["r_rms"] = float(np.sqrt(out["r2_med"])) if out["r2_med"] > 0 else float("nan")  # Richardson sin sentido -> nan
    out["dE"] = abs(a["E0"] - b["E0"])
    out["dE_rel"] = out["dE"] / abs(b["E0"]) if b["E0"] != 0 else np.inf
    out["u"] = b["u"]          # autovector de la malla fina, normalizado
    out["rgrid"] = b["r"]
    return out


def orden_aparente(V, R, hs, clave="E0", exacto=None, nev=2):
    """hs: lista de pasos con razon 2 (h, h/2, h/4, ...). Devuelve (valores, ordenes).
    Sin exacto: p_i = log2[(X_i - X_{i+1})/(X_{i+1} - X_{i+2})].
    Con exacto: p_i = log2[|X_i - X*| / |X_{i+1} - X*|]."""
    N0 = int(round(R / hs[0])) - 1
    Ns = [N0]
    for _ in hs[1:]:
        Ns.append(2 * Ns[-1] + 1)          # hh exactamente a la mitad, mismo R
    X = [resolver(V, R, N=n, nev=nev)[clave] for n in Ns]
    if exacto is None:
        p = [float(np.log2(abs((X[i] - X[i + 1]) / (X[i + 1] - X[i + 2])))) for i in range(len(X) - 2)]
    else:
        p = [float(np.log2(abs(X[i] - exacto) / abs(X[i + 1] - exacto))) for i in range(len(X) - 1)]
    return X, p


def caja_recomendada(E0, Rmin=60.0, factor=25.0, entera=False):
    """R = max(Rmin, factor/kappa). entera=True redondea R hacia arriba a un entero, para que
    r = 1 (u otros enteros, p. ej. el borde del pozo) caiga en un nodo de las mallas h = 1/40, 1/80."""
    R = max(Rmin, factor / np.sqrt(-2.0 * E0)) if E0 < 0 else np.inf
    return float(np.ceil(R)) if entera and np.isfinite(R) else R


# ----------------------------------------------------------------------------- energia cero y umbral
def pendiente_energia_cero(V, R, r0=1e-8, quiebres=()):
    """u'(R) de la solucion regular a E=0 (u(r0)=r0, u'(r0)=1)."""
    tramos = [r0] + sorted(q for q in quiebres if r0 < q < R) + [R]
    y = [r0, 1.0]
    f = lambda r, s: [s[1], 2.0 * float(V(np.array([r]))[0]) * s[0]]
    for a, b in zip(tramos[:-1], tramos[1:]):
        s = solve_ivp(f, [a, b], y, method="DOP853", rtol=1e-13, atol=1e-16)
        y = [s.y[0, -1], s.y[1, -1]]
    return y[1]


def umbral(familia, a, b, R=200.0, quiebres=(), xtol=1e-13):
    """Parametro lam en [a,b] donde u'(R; lam) = 0 a energia cero. familia(lam) -> V."""
    g = lambda lam: pendiente_energia_cero(familia(lam), R, quiebres=quiebres)
    return brentq(g, a, b, xtol=xtol)


# ----------------------------------------------------------------------------- soluciones exactas de control
def hulthen_exacto(delta, n=1):
    """Hulthen V = -delta/(e^{delta r}-1), l=0: E_n = -(1/2)(1/n - n delta/2)^2 si 1/n > n delta/2.
    Para n=1, u_1 = (1-e^{-delta r}) e^{-kappa r}, kappa = 1 - delta/2; <r> y <r^2> analiticos
    (integrales con sympy, evaluadas a 30 cifras). Umbral del estado n: delta = 2/n^2."""
    import sympy as sp
    kap_n = 1.0 / n - n * delta / 2
    out = dict(delta=delta, n=n, kappa=kap_n, E=-0.5 * kap_n**2 if kap_n > 0 else None,
               umbral=2.0 / n**2)
    if n == 1 and kap_n > 0:
        r, d = sp.symbols("r delta", positive=True)
        k = 1 - d / 2
        u = (1 - sp.exp(-d * r)) * sp.exp(-k * r)
        # comprobacion simbolica de que u_1 resuelve la ecuacion con E_1
        res = sp.simplify(-sp.diff(u, r, 2) / 2 - d / (sp.exp(d * r) - 1) * u + k**2 / 2 * u)
        mom = [sp.integrate(sp.expand(r**j * u**2), (r, 0, sp.oo), conds="none") for j in (0, 1, 2)]
        val = [sp.N(m.subs(d, sp.nsimplify(delta)), 30) for m in mom]
        out.update(residuo_simbolico=str(res), r_med=float(val[1] / val[0]), r2_med=float(val[2] / val[0]),
                   r_med_formula=str(sp.simplify(mom[1] / mom[0])))
        out["r_rms"] = float(np.sqrt(out["r2_med"]))
    return out


def pozo_exacto(V0, a=1.0):
    """Pozo esferico cuadrado, l=0, estado base: k cot(k a) = -kappa, k = sqrt(2(V0+E)), kappa = sqrt(-2E).
    Hay estado ligado si V0 a^2 > pi^2/8. <r>, <r^2> con u = sen(k r) (r<a), sen(k a) e^{-kappa(r-a)} (r>a),
    integrados en forma cerrada con sympy."""
    import sympy as sp
    umb = np.pi**2 / (8 * a**2)
    out = dict(V0=V0, a=a, umbral_V0=umb)
    if V0 <= umb:
        out["E"] = None
        return out
    f = lambda E: np.sqrt(2 * (V0 + E)) / np.tan(np.sqrt(2 * (V0 + E)) * a) + np.sqrt(-2 * E)
    # la raiz del estado base tiene k a en (pi/2, pi)
    Elo = -V0 + (np.pi / 2 / a)**2 / 2 * (1 + 1e-14)
    Ehi = min(-1e-300, -V0 + (np.pi / a)**2 / 2 * (1 - 1e-14))
    E = brentq(f, Elo, Ehi, xtol=1e-16, rtol=4 * np.finfo(float).eps)
    r, k, q, A = sp.symbols("r k q a", positive=True)
    ui, uo = sp.sin(k * r), sp.sin(k * A) * sp.exp(-q * (r - A))
    mom = [sp.integrate(r**j * ui**2, (r, 0, A)) + sp.integrate(r**j * uo**2, (r, A, sp.oo), conds="none")
           for j in (0, 1, 2)]
    sub = {k: sp.Float(np.sqrt(2 * (V0 + E)), 30), q: sp.Float(np.sqrt(-2 * E), 30), A: sp.Float(a, 30)}
    val = [sp.N(m.subs(sub), 30) for m in mom]
    out.update(E=float(E), k=float(np.sqrt(2 * (V0 + E))), kappa=float(np.sqrt(-2 * E)),
               r_med=float(val[1] / val[0]), r2_med=float(val[2] / val[0]))
    out["r_rms"] = float(np.sqrt(out["r2_med"]))
    return out
