# Material para auditoría (parte 2 de 3)

Responde solo "Recibido".

## controles.md

# Controles de E3 (generado por `codigo/08_tabla_controles.py` desde `resultados/*.json`)

Los criterios se fijaron antes de correr cada script (están en su docstring). Las filas marcadas "(posterior)" se añadieron después de ver un fallo y no cambian el veredicto de la fila original.

Resumen: 32 filas; 29 pasan, 2 no pasan, el resto medido.

| # | control | criterio fijado antes | valor | ¿pasa? | script |
|---|---|---|---|---|---|
| U1 | δ_c por energía cero estable ante r_f y rtol | estabilidad de delta_A: rf 60/d vs 80/d < 1e-11; rtol 1e-13 vs 1e-11 < 1e-10 | máx 2.0e-12 | pasa | `01_umbrales.py` |
| U2 | δ_c por energía cero (A) frente a extrapolación de κ(δ) (B, cúbico, s = 0.002..0.03) | |delta_A - delta_B| < 1e-8 (cuatro perfiles) | Yukawa 1.5e-10; ECSC -5.5e-07; Hulthén -1.0e-14; átomo H estático -1.1e-10 | **no pasa** (ECSC: el cúbico no sigue la curvatura de κ(δ); residuo 3.5e-07) | `01_umbrales.py` |
| U2b | (posterior) B con s = 1e-4..2e-3 | mismo umbral 1e-8 (añadido después de ver U2) | Yukawa -7.8e-15; ECSC -7.1e-12; Hulthén -2.4e-15; átomo H estático 3.1e-15 | pasa | `01_umbrales.py` |
| U3 | Hulthén exacto y Yukawa de referencia | Hulthen |delta_A - 2| < 1e-10; Yukawa |delta_A - 1.1906124210606| < 1e-10 | -1.3e-14; 2.4e-15 | pasa | `01_umbrales.py` |
| U4 | Hulthén: κ del disparo = 1 − δ/2 | Hulthen: |kappa_disparo - (1 - delta/2)| < 1e-11 | 2.4e-14 | pasa | `01_umbrales.py` |
| S1 | 1/a y r_e: energía cero frente a desfasajes (k ≤ 0.1δ, grado 3) | |1/a_1 - 1/a_2| < 1e-9 y |r_e1 - r_e2| < 1e-5 (energia cero frente a desfasajes) | máx |Δ(1/a)| 1.3e-09, máx |Δr_e| 1.5e-06 | **no pasa** (truncación del polinomio en k²) | `02_dispersion.py` |
| S1b | (posterior) igual con k = (0.005..0.05)δ, grado 4 | (posterior) igual que S1 con k = (0.005..0.05) delta y grado 4 | máx |Δ(1/a)| 4.4e-14, máx |Δr_e| 1.1e-09 | pasa | `02_dispersion.py` |
| S2 | Hulthén: a(δ) frente a la fórmula con digamma | Hulthen: |a - a_exacto|/|a_exacto| < 1e-9 (|a| < 1e6) | 7.4e-11 | pasa | `02_dispersion.py` |
| S3 | c = −d(1/a)/dδ: Hellmann–Feynman frente a diferencias | |c_HF - c_dif|/c < 1e-7 | máx 1.2e-11 | pasa | `02_dispersion.py` |
| S5 | 1/a monótona y con un solo cero | 1/a monotona decreciente en delta y con un solo cambio de signo, en delta_c | 4 perfiles | pasa | `02_dispersion.py` |
| L1 | κ = (1 − √(1 − 2r_e/a))/r_e | |kappa_ERE - kappa|/kappa < 1e-4 para s <= 0.01 | máx 1.2e-05 | pasa | `03_ligados_virtuales.py` |
| L2 | pendiente medida A frente a c predicha | |A - c|/c < 1e-5 | Yukawa 5.2e-10; ECSC -4.6e-06; Hulthén -3.9e-12; átomo H estático -2.6e-10 | pasa | `03_ligados_virtuales.py` |
| L3 | κa → 1 y ⟨r⟩κ → 1/2 | s = 1e-5: |kappa a - 1| < 1e-3 y |<r> kappa - 1/2| < 1e-3 | máx 7.9e-06 | pasa | `03_ligados_virtuales.py` |
| L4 | pendiente de ⟨r⟩κ frente a κ = r_e/2 | pendiente d(<r>kappa)/dkappa (s <= 1e-3) frente a r_e/2: diferencia relativa < 2e-2 | Yukawa -3.2e-08; ECSC -6.9e-05; Hulthén -2.2e-08; átomo H estático -2.5e-08 | pasa | `03_ligados_virtuales.py` |
| L5 | polo virtual: rango efectivo frente a cálculo directo | |kappa_v(ERE) - kappa_v(directo)|/kappa_v < 1e-4 para s <= 0.01 | máx 1.4e-05 | pasa | `03_ligados_virtuales.py` |
| L6 | un solo ligado s, sin nodos | ligados sin nodos y una sola raiz | 64 puntos | pasa | `03_ligados_virtuales.py` |
| K1 | punto fijo 1/4 y su corrección (1/4)(1 + r_e/R) | |2R^2E0/pi^2 - pred(*)|/(1/4) < 1e-3 (R >= 200) y signo(valor - 1/4) = signo(r_e) (todo R) | máx 2.0e-10 | pasa | `04_cajas_universalidad.py` |
| K2 | sentido del cruce = signo de r_e | signo(delta* - delta_c) = signo(r_e) (todos los pares); |cruce - pred(*)| < 0.1|cruce - delta_c| (R1 >= 200) | máx |δ*−pred|/|δ*−δ_c| (R₁ ≥ 200) 1.9e-07 | pasa | `04_cajas_universalidad.py` |
| K3 | ⟨r⟩/R → 1/2 − 2/π² en δ_c | |<r>/R - (1/2 - 2/pi^2)| < 0.02 en R = 1600 | máx 3.9e-04 | pasa | `04_cajas_universalidad.py` |
| K4 | polo virtual desde las cajas | |kappa_v(caja) - kappa_v(directo)|/kappa_v < 1e-3 | máx 8.0e-04 | pasa | `04_cajas_universalidad.py` |
| K5 | radial (Fase 2) frente al disparo, R = 200 | |E0 radial - E0 disparo| < 2 err_radial + 1e-10 (R = 200) | máx 6.3e-09 | pasa | `04_cajas_universalidad.py` |
| T1 | W del ECSC acotado y positivo | W_ECSC en (0, delta] y finito en [1e-8, 400] | mín 2.50e-03 | pasa | `05_transferencia_ecsc.py` |
| T2 | integral de camino frente al disparo y al radial | |E_tr - E_disparo(R)| <= 2 err_tr + 1e-12 (y frente al radial: <= 2(err + err_rad)) | máx |dif|/σ 0.61 | pasa | `05_transferencia_ecsc.py` |
| T3 | orden de Trotter | orden de Trotter en [1.8, 2.2] (informativo si toca la pared) | 1.975 a 2.009 | pasa | `05_transferencia_ecsc.py` |
| T4 | Perron y residuo | Perron min(v)/max|v| > -1e-10 y residuo < 1e-8 | mín -1.9e-17, residuo máx 8.6e-16 | pasa | `05_transferencia_ecsc.py` |
| T5 | Hulthén 1.8 exacto por la integral de camino | Hulthen 1.8: |E_tr + 0.005| <= 2 err_tr + 1e-12 | -2.4e-09 (σ 7.5e-08) | pasa | `05_transferencia_ecsc.py` |
| T6 | reproduce comun3 (Fase 3) | Yukawa 1.18 R=200 (h 0.04, eps 0.1): |E - E_comun3| < 1e-13 | 0.0e+00 | pasa | `05_transferencia_ecsc.py` |
| V1 | tercer método (fase variable, LSODA) | |delta_c(fase variable, LSODA) - delta_A| < 1e-9 | máx 3.1e-12 | pasa | `07_verificacion.py` |
| V2 | disparo frente al radial de la Fase 3 (Yukawa) | |E_disparo - E_radial(Fase 3)| < 2 err_radial + 1e-9 | máx |dif| 6.6e-09 | pasa | `07_verificacion.py` |
| V3 | Hulthén ⟨r⟩ exacto | Hulthen |<r> - exacto|/exacto < 1e-9 | máx 5.5e-13 | pasa | `07_verificacion.py` |
| V4 | Hulthén: polo virtual κ_v = δ/2 − 1 (observación) | informativo: kappa_v de Hulthen frente a delta/2 - 1 | 9.1e-10 | medido | `07_verificacion.py` |
| V5 | Yukawa: c y B frente a la Fase 3 | |c - 0.7411| < 5e-4 y |B_pred - 0.059| < 0.01 (Yukawa, Fase 3) | c = 0.741192 (A = 0.741131); B = 0.0565 (0.0585) | pasa | `07_verificacion.py` |


## codigo/perfiles.py

```python
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

```

## codigo/04_cajas_universalidad.py

```python
"""04_cajas_universalidad.py -- E3: lo que ve una caja esferica dura en el umbral, para cada perfil.

Caja de Dirichlet u(R) = 0, E0(R) por disparo (sin malla). Fuera del alcance u = sin(k(R - r)), asi que
    k cot delta_0(k) = -k cot(kR)     (exacto si R >> 1/delta),
y con el desarrollo de rango efectivo k cot delta_0 = -1/a + r_e k^2/2 + P k^4, con x = kR:
    -x cot x = -R/a + r_e x^2/(2R) + P x^4/R^3.                                       (*)
Consecuencias que se comprueban:
  (1) Punto fijo: en delta_c (1/a = 0), x -> pi/2 y 2R^2E0/pi^2 -> 1/4; a primer orden
      2R^2E0/pi^2 = (1/4)(1 + r_e/R): el lado por el que se llega lo fija el signo de r_e.
  (2) Cruce de cajas R1, R2 (R1^2 E0(R1) = R2^2 E0(R2)): de (*) a primer orden 1/a* = -r_e pi^2/(8 R1 R2), es decir
      delta* - delta_c = r_e pi^2/(8 c R1 R2): con r_e > 0 el cruce llega desde arriba (Yukawa) y con r_e < 0 desde
      abajo (ECSC). Se compara el cruce medido con (*) completo (a, r_e, P del mismo delta) y con el primer orden.
  (3) <r>/R en delta_c -> 1/2 - 2/pi^2 (estado cos(pi r/2R) en el limite).
  (4) Polo virtual visto por la caja: en delta = delta_c (1 + s), s = 0.01 y 0.03, los E0(R) > 0 de R = 50..1600 dan
      k cot delta_0 = -k cot(kR); ajuste en k^2 (grado 2) -> a_caja, r_e,caja -> kappa_v; frente a 02/03.
Control de malla: radial.resolver_rich (diferencias finitas, Fase 2) frente al disparo en R = 200, delta = delta_c.

Criterios fijados ANTES de correr:
  K1 |2R^2E0/pi^2 - prediccion (*)| / (1/4) < 1e-3 para R >= 200, y signo(2R^2E0/pi^2 - 1/4) = signo(r_e) para todo R
  K2 signo(delta* - delta_c) = signo(r_e) en todos los pares (R, 2R); |cruce - prediccion (*)| < 0.1 |cruce - delta_c|
     para R1 >= 200
  K3 |<r>/R - (1/2 - 2/pi^2)| < 0.02 en R = 1600 (la correccion es O(r_e/R))
  K4 |kappa_v(caja) - kappa_v(directo)| / kappa_v < 1e-3 (s = 0.01 y 0.03)
  K5 |E0(radial) - E0(disparo)| < 2 err_radial + 1e-10 (err_radial = |E_h - E_h/2|), R = 200
"""
import sys

import numpy as np
from scipy.optimize import brentq

import comun_e3 as C
import perfiles as P

sys.path.insert(0, C.F2)
import radial  # noqa: E402

CRIT = {
    "K1": "|2R^2E0/pi^2 - pred(*)|/(1/4) < 1e-3 (R >= 200) y signo(valor - 1/4) = signo(r_e) (todo R)",
    "K2": "signo(delta* - delta_c) = signo(r_e) (todos los pares); |cruce - pred(*)| < 0.1|cruce - delta_c| (R1 >= 200)",
    "K3": "|<r>/R - (1/2 - 2/pi^2)| < 0.02 en R = 1600",
    "K4": "|kappa_v(caja) - kappa_v(directo)|/kappa_v < 1e-3",
    "K5": "|E0 radial - E0 disparo| < 2 err_radial + 1e-10 (R = 200)",
}
RS = [50, 100, 200, 400, 800, 1600]


def menos_xcotx(y):
    """-x cot x como funcion de y = x^2 (y < 0: x = i q, -x cot x = -q coth q)."""
    if y > 0:
        x = np.sqrt(y)
        return -x / np.tan(x)
    if y < 0:
        q = np.sqrt(-y)
        return -q / np.tanh(q)
    return -1.0


def E_pred(R, ia, re, Pf):
    """E0 de (*): raiz y en (-(R/a)^2*4 - 10, (pi)^2) del estado sin nodos."""
    f = lambda y: menos_xcotx(y) - (-R * ia + re * y / (2 * R) + Pf * y * y / R**3)
    hi = np.pi**2 * (1 - 1e-9)
    lo = -max(10.0, 4 * (R * ia)**2 + 10)
    return brentq(f, lo, hi, xtol=1e-15, rtol=1e-14) / (2 * R * R)


def ere(k, d):
    z = P.cero(k, d)
    ks = d * np.linspace(0.005, 0.05, 10)
    co = np.polyfit(ks**2, [P.kcot(k, d, x) for x in ks], 4)
    return z["inv_a"], z["r_e"], float(co[-3])


def caja_obs(k, d, R):
    E = P.caja(k, d, R)
    p = P.PERFILES[k]
    s = P._integrar(p["V"](d), p["W0"](d), E, R, extra=lambda r, y: [y[0]**2, r * y[0]**2, 0.0 * r])
    return E, float(s.y[3, -1] / s.y[2, -1] / R)


def main():
    T = C.Tee("04_cajas_universalidad")
    D2 = C.cargar("02_dispersion")["perfiles"]
    D3 = C.cargar("03_ligados_virtuales")["perfiles"]
    out = dict(script="04_cajas_universalidad.py", criterios=CRIT, perfiles={}, r_sobre_R_universal=0.5 - 2 / np.pi**2)
    ok = {k: True for k in CRIT}
    for k in C.ORDEN:
        dc, c = D2[k]["delta_c"], D2[k]["c_HF"]
        ia0, re0, P0 = ere(k, dc)
        T(f"\n== {k}: delta_c={dc:.12f} r_e={re0:+.6f} P={P0:+.4f} c={c:.6f}")
        fijo = []
        for R in RS:
            E, rR = caja_obs(k, dc, R)
            v = 2 * R * R * E / np.pi**2
            vp = 2 * R * R * E_pred(R, ia0, re0, P0) / np.pi**2
            v1 = 0.25 * (1 + re0 / R)
            fijo.append(dict(R=R, E0=E, valor=float(v), pred=float(vp), pred_1orden=float(v1), r_sobre_R=rR,
                             R_por_desv=float((v - 0.25) * R)))
            if R >= 200:
                ok["K1"] &= bool(abs(v - vp) / 0.25 < 1e-3)
            ok["K1"] &= bool(np.sign(v - 0.25) == np.sign(re0))
            T(f"   R={R:5d}  2R^2E/pi^2={v:.8f}  pred(*)={vp:.8f}  1/4(1+r_e/R)={v1:.8f}  R(v-1/4)={(v-0.25)*R:+.5f} "
              f"(r_e/4={re0/4:+.5f})  <r>/R={rR:.6f}")
        ok["K3"] &= bool(abs(fijo[-1]["r_sobre_R"] - (0.5 - 2 / np.pi**2)) < 0.02)
        # cruces
        cruces = []
        for R1 in RS[:-1]:
            R2 = 2 * R1
            g = lambda d: P.caja(k, d, R1) * R1**2 - P.caja(k, d, R2) * R2**2
            span = 0.02 * dc
            ds_ = np.linspace(dc - span, dc + span, 9)
            gv = [g(d) for d in ds_]
            dstar = None
            for i in range(8):
                if np.sign(gv[i]) != np.sign(gv[i + 1]):
                    dstar = brentq(g, ds_[i], ds_[i + 1], xtol=1e-14, rtol=1e-14)
                    break

            def gp(d):
                ia, re, Pf = ere(k, d)
                return E_pred(R1, ia, re, Pf) * R1**2 - E_pred(R2, ia, re, Pf) * R2**2
            dpred = brentq(gp, dc - span, dc + span, xtol=1e-13, rtol=1e-14)
            d1 = dc + re0 * np.pi**2 / (8 * c * R1 * R2)
            vstar = 2 * R2**2 * P.caja(k, dstar, R2) / np.pi**2
            cruces.append(dict(R1=R1, R2=R2, delta_star=float(dstar), dif=float(dstar - dc), pred=float(dpred),
                               pred_1orden=float(d1), valor_en_cruce=float(vstar)))
            ok["K2"] &= bool(np.sign(dstar - dc) == np.sign(re0))
            if R1 >= 200:
                ok["K2"] &= bool(abs(dstar - dpred) < 0.1 * abs(dstar - dc))
            T(f"   cruce {R1}/{R2}: delta*={dstar:.10f} (delta*-dc={dstar-dc:+.3e})  pred(*)={dpred-dc:+.3e}  "
              f"1er orden={d1-dc:+.3e}  2R^2E/pi^2 en el cruce={vstar:.6f}")
        # polo virtual desde la caja
        vir = []
        for s in (0.01, 0.03):
            d = dc * (1 + s)
            Es = np.array([P.caja(k, d, R) for R in RS])
            kk = np.sqrt(2 * Es)
            kc = -kk / np.tan(kk * np.array(RS))
            co = np.polyfit(kk**2, kc, 2)
            ia_b, re_b = -co[-1], 2 * co[-2]
            kv_b = (-1 + np.sqrt(1 - 2 * re_b * ia_b)) / re_b
            ref = [x for x in D3[k]["virtuales"] if abs(x["s"] - s) / s < 1e-6]
            if ref:
                kv_dir = ref[0]["kappa_v_dir"]
            else:   # s = 0.01, 0.03 no estan en la rejilla de 03: se calcula aqui con la misma rutina
                import importlib
                m3 = importlib.import_module("03_ligados_virtuales")
                kv_dir = m3.virtual(k, d, -ia_b)[0]
            z = P.cero(k, d)
            vir.append(dict(s=s, delta=float(d), E0_cajas=Es.tolist(), inv_a_caja=float(ia_b), r_e_caja=float(re_b),
                            inv_a=z["inv_a"], r_e=z["r_e"], kappa_v_caja=float(kv_b), kappa_v_dir=float(kv_dir),
                            E_virtual_caja=float(-0.5 * kv_b**2), dif_rel=float((kv_b - kv_dir) / kv_dir)))
            ok["K4"] &= bool(abs(kv_b - kv_dir) / kv_dir < 1e-3)
            T(f"   virtual s={s}: caja 1/a={ia_b:+.8f} (E=0: {z['inv_a']:+.8f}) r_e={re_b:+.5f} (E=0: {z['r_e']:+.5f})  "
              f"kappa_v caja={kv_b:.8e} directo={kv_dir:.8e} dif rel={(kv_b-kv_dir)/kv_dir:+.1e}")
        # control de malla con el radial de la Fase 2
        V = P.PERFILES[k]["V"](dc)
        rr = radial.resolver_rich(V, 200.0, h=1 / 40, nev=1)
        Esh = [x["E0"] for x in fijo if x["R"] == 200][0]
        err = abs(rr["E0_h"] - rr["E0_h2"])
        ok["K5"] &= bool(abs(rr["E0"] - Esh) < 2 * err + 1e-10)
        T(f"   radial FD R=200: E0={rr['E0']:.12e}  disparo={Esh:.12e}  dif={rr['E0']-Esh:+.1e}  err_radial={err:.1e}")
        out["perfiles"][k] = dict(delta_c=dc, r_e=re0, P=P0, c=c, punto_fijo=fijo, cruces=cruces, virtual_caja=vir,
                                  radial_R200=dict(E0=rr["E0"], err=err, disparo=Esh))
    out["pasa"] = ok
    T("controles:", ok)
    C.guardar("04_cajas_universalidad", out)
    T.cerrar()


if __name__ == "__main__":
    main()

```
