"""01_teoria.py -- comprobaciones numericas de teoria.md (E2, criterio de cruce de cajas). Determinista, ~2 min.

1. Puntos fijos de alcance cero: F(0) = 1/4, G(0) = 1/2 - 2/pi^2, F(1) = 0, F(-inf) = 1.
2. Caso exacto: pozo cuadrado de alcance b dentro de la esfera dura, a fijo, b/R -> 0: y -> F(R/a) con error ~ r_e/R.
3. Constantes del Yukawa en el umbral: r_e, m1 = int r (1 - u0^2) dr, c = -d(1/a)/d delta, y las predicciones
   de orden dominante y siguiente para el cruce:
     delta*_y(R, 2R) - delta_c = pi^2 r_e / (16 c R^2) + 3 pi^2 r_e^2 / (32 c R^3) + O(R^-4)
     y* = 1/4 + 3 r_e/(8R) + 27 r_e^2/(64 R^2)
     delta*_rho(R, 2R) - delta_c = -k1 r_e / (c R^2),  k1 = pi^2 (4 + pi^2) / (16 (pi^2 - 12))
     rho(delta_c, R) = 1/2 - 2/pi^2 + (1/4 + 1/pi^2) r_e / R
4. Modelo de rango efectivo "completo" (ERE): x cot x = R/a(delta) - r_e(delta) x^2/(2R), con a y r_e calculados a
   energia cero en cada delta; rho = (I1 - m1/R^2)/(I0 - r_e/(2R)). Cruces del modelo para cada par (R, 2R).
5. Corrimiento de la pared de la transferencia (pared sin imagen en R + BETA sqrt(eps), extrapolada en eps):
   c_w = BETA * ext_eps(sqrt 0.1, sqrt 0.05); prediccion delta*_tr - delta*_exacto ~ -pi^2 c_w / (8 c R^2).
Salida: resultados/01_teoria.json
"""
import sys, time
import numpy as np
from scipy.optimize import brentq
import e2comun as c

sys.stdout = c.Tee("01_teoria")
T0 = time.perf_counter()
out = dict(script="01_teoria.py", fecha=c.ahora())
PI2 = np.pi**2

# ---------------------------------------------------------------- 1. puntos fijos
out["puntos_fijos"] = dict(F0=c.F_escala(0.0), G0=c.G_escala(0.0), G0_cerrado=c.RHO_FIJO, F1=c.F_escala(1.0),
                           G1=c.G_escala(1.0), F_menos_inf=c.F_escala(-1e8), G_menos_inf=c.G_escala(-1e8),
                           pendiente_F_en_0=(c.F_escala(1e-5) - c.F_escala(-1e-5)) / 2e-5, pendiente_F_teorica=-2 / PI2,
                           pendiente_G_en_0=(c.G_escala(1e-4) - c.G_escala(-1e-4)) / 2e-4,
                           pendiente_G_teorica=2 * (PI2 - 12) / np.pi**4)
print("puntos fijos:", out["puntos_fijos"])


# ---------------------------------------------------------------- 2. pozo cuadrado (caso exacto)
def pozo_a(K, b):
    return b - np.tan(K * b) / K


def pozo_y(K, b, R):
    """Estado base del pozo -V0 (r<b), V0 = K^2/2, en la esfera dura R. Variable s = 2E = k^2.
    Condicion sin polos: g(s) = K' cos(K'b) S(s) + sin(K'b) C(s) = 0, con S = sin(kL)/k, C = cos(kL), L = R - b
    (para s < 0 se usa la forma hiperbolica dividida por cosh(qL), sin desbordes). Estado base = raiz mas baja."""
    L = R - b
    def g(s):
        Kp = np.sqrt(K * K + s)
        if s > 0:
            k = np.sqrt(s); return Kp * np.cos(Kp * b) * np.sin(k * L) / k + np.sin(Kp * b) * np.cos(k * L)
        if s < 0:
            q = np.sqrt(-s); return Kp * np.cos(Kp * b) * np.tanh(q * L) / q + np.sin(Kp * b)
        return Kp * np.cos(Kp * b) * L + np.sin(Kp * b)
    lo, hi = -K * K * (1 - 1e-12), (np.pi / L)**2
    ss = np.concatenate([-np.geomspace(K * K * (1 - 1e-12), 1e-14, 3000), np.linspace(0, hi, 3001)[1:]])
    gs = np.array([g(s) for s in ss])
    i = int(np.nonzero(np.sign(gs[1:]) != np.sign(gs[:-1]))[0][0])
    s = brentq(g, ss[i], ss[i + 1], xtol=1e-20, rtol=1e-15)
    return s * R * R / PI2        # y = 2R^2E/pi^2 = R^2 s / pi^2


pozo = []
R = 100.0
for zobj in (-2.0, 0.0, 0.5, 2.0):
    for b in (4.0, 2.0, 1.0, 0.5, 0.25):
        # fijar a con K b cerca de pi/2: a = b - tan(Kb)/K = R/zobj  (zobj = 0: K b = pi/2 exacto)
        if zobj == 0.0:
            K = np.pi / (2 * b)
        else:
            aobj = R / zobj
            g = lambda K: pozo_a(K, b) - aobj
            K = brentq(g, (np.pi / 2 + 1e-12) / b, (np.pi - 1e-9) / b) if aobj > b else \
                brentq(g, 1e-6 / b, (np.pi / 2 - 1e-12) / b)
        a = np.inf if zobj == 0.0 else pozo_a(K, b)
        yv = pozo_y(K, b, R)
        Fz = c.F_escala(zobj)
        pozo.append(dict(z=zobj, b=b, K=K, a=a if np.isfinite(a) else "inf", y=yv, F=Fz, dif=yv - Fz))
        print(f"pozo z={zobj:+.1f} b={b:<5} y={yv:.8f} F(z)={Fz:.8f} dif={yv - Fz:+.3e}")
out["pozo_cuadrado"] = dict(R=R, filas=pozo,
                            razon_dif_por_mitad_b_z0=[pozo[i]["dif"] / pozo[i + 1]["dif"]
                                                      for i in range(5, 9)])
print("razon de la diferencia al dividir b por 2 (z = 0):", out["pozo_cuadrado"]["razon_dif_por_mitad_b_z0"])

# ---------------------------------------------------------------- 3. constantes del Yukawa en el umbral
dc = c.DELTA_C_REF
re_c, _ = c.rango_efectivo_umbral(dc)


def m1_umbral(delta, Rf=200.0):
    from scipy.integrate import solve_ivp
    f = lambda r, s: [s[1], -2.0 * np.exp(-delta * r) / r * s[0]]
    s = solve_ivp(f, [c.R0, Rf], [c.R0 * (1 - c.R0), 1 - 2 * c.R0], method="DOP853", rtol=1e-13, atol=1e-30,
                  dense_output=True)
    rr = np.linspace(c.R0, Rf, 400001)
    uu = s.sol(rr)[0]; C = uu[-1]
    return float(np.trapezoid(rr * (1 - (uu / C)**2), rr))


m1 = m1_umbral(dc)
hd = 1e-5
ua = {s: 1.0 / c.energia_cero(dc + s * hd)["a"] for s in (-2, -1, 1, 2)}
cpend = -(8 * (ua[1] - ua[-1]) - (ua[2] - ua[-2])) / (12 * hd)
u0 = 1.0 / c.energia_cero(dc)["a"]
a_s = {f"{d:g}": c.energia_cero(d)["a"] for d in (1.19, 1.1906, 1.1907, 1.20)}
k1_rho = PI2 * (4 + PI2) / (16 * (PI2 - 12))
cons = dict(delta_c=dc, r_e=re_c, m1=m1, c=cpend, u_en_delta_c=u0, a_s=a_s,
            alpha_y=PI2 * re_c / (16 * cpend), beta_y=3 * PI2 * re_c**2 / (32 * cpend),
            k1_rho=k1_rho, alpha_rho=-k1_rho * re_c / cpend,
            rho_eps=0.25 + 1 / PI2, cola_exp_R50=float(np.exp(-dc * 50)))
print("constantes:", cons)
out["constantes"] = cons


def pred_y(R):
    return dc + cons["alpha_y"] / R**2 + cons["beta_y"] / R**3


# ---------------------------------------------------------------- 4. modelo ERE completo
def xcotx(s):
    if s > 1e-14:
        x = np.sqrt(s); return x / np.tan(x)
    if s < -1e-14:
        q = np.sqrt(-s); return q / np.tanh(q)
    return 1.0 - s / 3.0


_cache = {}


def ez(delta):
    if delta not in _cache:
        _cache[delta] = c.energia_cero(delta)
    return _cache[delta]


def s_ERE(delta, R, Rw=None, con_re=True):
    """x^2 del modelo ERE en una caja de radio efectivo Rw (por defecto R)."""
    Rw = R if Rw is None else Rw
    e = ez(delta); z = Rw / e["a"]; re_ = e["r_e"] if con_re else 0.0
    f = lambda s: xcotx(s) - z + re_ * s / (2 * Rw)
    hi = PI2 * (1 - 1e-12)
    lo = -1.0
    while f(lo) < 0:
        lo *= 2
    return brentq(f, lo, hi, xtol=1e-15, rtol=1e-15)


def y_ERE(delta, R, Rw=None, con_re=True):
    Rw = R if Rw is None else Rw
    return s_ERE(delta, R, Rw, con_re) / PI2 * (R / Rw)**2


def I01(s):
    t = np.linspace(0.0, 1.0, 20001)
    if s > 0:
        x = np.sqrt(s); u = np.sin(x * (1 - t)) / np.sin(x)
    elif s < 0:
        q = np.sqrt(-s); u = np.sinh(q * (1 - t)) / np.sinh(q)
    else:
        u = 1 - t
    return np.trapezoid(u * u, t), np.trapezoid(t * u * u, t)


def rho_ERE(delta, R):
    s = s_ERE(delta, R)
    I0, I1 = I01(s)
    e = ez(delta)
    return (I1 - m1 / R**2) / (I0 - e["r_e"] / (2 * R))


def cruce(fun, R, lo=1.1895, hi=1.1935):
    return brentq(lambda d: fun(d, R) - fun(d, 2 * R), lo, hi, xtol=1e-12)


Rs = [50, 100, 200, 400, 800, 1600]
ere = []
for R in Rs:
    dy = cruce(y_ERE, R)
    dr = cruce(rho_ERE, R, 1.1896, 1.200)
    ere.append(dict(R=R, delta_y=dy, y_cruce=y_ERE(dy, 2 * R), delta_rho=dr, rho_cruce=rho_ERE(dr, 2 * R),
                    pred_serie_y=pred_y(R), y_umbral=y_ERE(dc, R), y_umbral_serie=0.25 * (1 + re_c / R),
                    rho_umbral=rho_ERE(dc, R), rho_umbral_serie=c.RHO_FIJO + cons["rho_eps"] * re_c / R,
                    pred_ystar_serie=0.25 + 3 * re_c / (8 * R) + 27 * re_c**2 / (64 * R * R),
                    pred_rho_orden1=dc + cons["alpha_rho"] / R**2))
    print(f"ERE R={R:<5}: delta*_y={dy:.10f} (serie {pred_y(R):.10f}) y*={ere[-1]['y_cruce']:.6f} | "
          f"delta*_rho={dr:.9f} (orden 1 {ere[-1]['pred_rho_orden1']:.9f}) rho*={ere[-1]['rho_cruce']:.6f}", flush=True)
out["modelo_ERE"] = ere

# ---------------------------------------------------------------- 5. pared de la transferencia
BETA = c.comun3.BETA
cw = BETA * c.comun3.ext_eps(np.sqrt(0.1), np.sqrt(0.05))
pared = []
for R in Rs:
    dy_w = brentq(lambda d: y_ERE(d, R, R + cw) - y_ERE(d, 2 * R, 2 * R + cw), 1.1895, 1.1935, xtol=1e-12)
    dy = [e_["delta_y"] for e_ in ere if e_["R"] == R][0]
    pared.append(dict(R=R, delta_y_con_pared=dy_w, corrimiento=dy_w - dy, pred_orden1=-PI2 * cw / (8 * cpend * R**2)))
    print(f"pared R={R:<5}: corrimiento del cruce {dy_w - dy:+.3e} (orden 1: {pared[-1]['pred_orden1']:+.3e})")
out["pared_transferencia"] = dict(c_w=cw, filas=pared)

# ---------------------------------------------------------------- 6. exponente efectivo de convergencia
dif = [ere[i]["delta_y"] - ere[i + 1]["delta_y"] for i in range(len(ere) - 1)]
out["razones_ERE_y"] = [dif[i] / dif[i + 1] for i in range(len(dif) - 1)]
print("razones de diferencias sucesivas (ERE, y):", out["razones_ERE_y"])
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("01_teoria", out)
print(f"tiempo {out['tiempo_s']:.0f} s")
