"""25_respuesta_gemini.py -- Proyecto 05, Fase 3: comprobaciones numericas de los hallazgos de la auditoria adversarial con
Gemini 3.1 Pro (10-11-2026, auditoria_gemini/conversaciones/G.md). Cada bloque responde a un hallazgo.
  G1/G4  orden real de la malla del radial en delta = 1.19 (h = 1/40 ... 1/640) y punto de cruce R_c(h) de E0(R) = 0;
         metodo SIN malla: disparo DOP853 desde la serie de Frobenius, con empalme a la cola e^{-kappa r} (E0 de caja infinita).
  G1/G3  conteo de nodos de la solucion a energia cero (Sturm: n nodos en (0, inf) <=> n estados ligados s), sin caja ni malla.
  G3     delta = 1.20 en cajas gigantes R = 6400 ... 51200: la desviacion de la ley de caja debe seguir bajando.
  G2     celda delta = 1.25, R = 50: extrapolacion con el orden observado p_obs en vez de p = 2, frente a la barra de error.
  G5     ajuste 2D E(h, eps) = E0 + c1 h^4 + c2 eps^2 + c3 h^4/eps con los 6 puntos crudos de cada celda de delta = 1.19.
  G6     sensibilidad (informativa, NO cambia el criterio fijado) del umbral 0.95 de F_1/2.
Salida: fase3/resultados/25_respuesta_gemini.json."""
import json, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

out = {}
T0 = time.perf_counter()
V = lambda d: c.radial.V_yukawa(d)

# ---------------- G1: orden de la malla del radial, delta = 1.19, R = 3200
d, R = 1.19, 3200
Es = []
N0 = int(round(R * 40)) - 1
N = N0
for k in range(5):                   # h = 1/40 ... 1/640
    Es.append(c.radial.resolver(V(d), R, N=N, nev=1)["E0"]); N = 2 * N + 1
p = [float(np.log2(abs(Es[i] - Es[i + 1]) / abs(Es[i + 1] - Es[i + 2]))) for i in range(3)]
rich = [(4 * Es[i + 1] - Es[i]) / 3 for i in range(4)]
out["G1_orden_malla_radial"] = dict(delta=d, R=R, h=["1/40", "1/80", "1/160", "1/320", "1/640"], E=Es, orden=p, richardson_p2=rich)
print("G1 orden malla radial (1.19, R=3200):", [f"{x:.4f}" for x in p], "E:", [f"{x:+.6e}" for x in Es], flush=True)


# ---------------- G1/G4: disparo sin malla (caja infinita) y nodos a energia cero
def u_out(dl, E, r1):
    f = lambda r, s: [s[1], 2 * (-np.exp(-dl * r) / r - E) * s[0]]
    r0 = 1e-6
    u0, up0 = r0 * (1 - r0), 1 - 2 * r0           # Frobenius: u = r - r^2 + ...  (V ~ -1/r)
    s = solve_ivp(f, [r0, r1], [u0, up0], method="DOP853", rtol=1e-12, atol=1e-30)
    return s.y[0, -1], s.y[1, -1]


def nodos_E0(dl, Rf=4000.0):
    f = lambda r, s: [s[1], 2 * (-np.exp(-dl * r) / r) * s[0]]
    s = solve_ivp(f, [1e-8, Rf], [1e-8, 1.0], method="DOP853", rtol=1e-12, atol=1e-20, dense_output=True)
    rr = np.linspace(1e-6, Rf, 400001); u = s.sol(rr)[0]
    return int(np.sum(np.sign(u[1:]) != np.sign(u[:-1]))), float(s.y[0, -1]), float(s.y[1, -1])


out["G3_nodos_energia_cero"] = {}
for dl in (1.18, 1.19, 1.1906, 1.1907, 1.20):
    n, uR, upR = nodos_E0(dl)
    out["G3_nodos_energia_cero"][f"{dl:g}"] = dict(nodos=n, u_4000=uR, up_4000=upR, a_s=4000 - uR / upR)
    print(f"G1/G3 energia cero delta={dl}: nodos en (0, 4000) = {n}, a_s = {4000 - uR/upR:+.1f}", flush=True)


def E_disparo(dl, Eg):
    """E0 en caja infinita: empalme de la derivada logaritmica en r1 con la cola exacta del regimen libre.
    Para r >> 1/delta el potencial es despreciable (e^{-delta r}/r < 1e-25 en r = 60): u ~ e^{-kappa r}."""
    r1 = 60.0
    g = lambda E: (lambda uu: uu[1] / uu[0] + np.sqrt(-2 * E))(u_out(dl, E, r1))
    a, b = Eg * 3, Eg / 3
    return brentq(g, a, b, xtol=1e-22, rtol=1e-14)


out["G1_disparo_caja_infinita"] = {}
for dl, Eg in ((1.18, -3.1e-5), (1.19, -1.03e-7)):
    E = E_disparo(dl, Eg)
    out["G1_disparo_caja_infinita"][f"{dl:g}"] = E
    print(f"G1 disparo sin malla (caja infinita) delta={dl}: E0 = {E:+.8e}", flush=True)

# ---------------- G4: punto de cruce R_c(h) en delta = 1.19
out["G4_cruce"] = {}
for hh in (1 / 40, 1 / 80, 1 / 160, 1 / 320):
    fR = lambda RR: c.radial.resolver(V(1.19), RR, h=hh, nev=1)["E0"]
    Rc = brentq(fR, 1600, 12800, xtol=0.5)
    out["G4_cruce"][f"1/{round(1/hh)}"] = Rc
    print(f"G4 cruce E0(R)=0 con h=1/{round(1/hh)}: R_c = {Rc:.1f}", flush=True)

# ---------------- G3: delta = 1.20 en cajas gigantes
a_s = c.long_dispersion(1.20)
out["G3_delta120"] = {}
for RR in (3200, 6400, 12800, 25600, 51200):
    x = c.radial_ref(1.20, RR)
    ley = np.pi**2 / (2 * (RR - a_s)**2)
    out["G3_delta120"][f"R{RR}"] = dict(E0=x["E0"], ley=ley, dev=abs(x["E0"] - ley) / ley, F12=x["F12"], r_sobre_R=x["r_sobre_R"])
    print(f"G3 delta=1.20 R={RR}: E0={x['E0']:+.4e} ley={ley:.4e} dev={abs(x['E0']-ley)/ley:.2e} F12={x['F12']:.4f}", flush=True)

# ---------------- G2: extrapolacion con p_obs (delta = 1.25, R = 50 y delta = 1.18, R = 50)
CJ = json.load(open(os.path.join(c.RES3, "20_cajas.json")))
out["G2_p_obs"] = {}
for dk, Rk in (("1.25", "R50"), ("1.18", "R50"), ("1.2", "R100")):
    C = CJ["celdas"][dk][Rk]
    EhR = {e: C["E_hRich"][e] for e in ("0.2", "0.1", "0.05")}
    pobs = C["orden_trotter"]
    E_p = EhR["0.05"] + (EhR["0.05"] - EhR["0.1"]) / (2**pobs - 1)
    out["G2_p_obs"][f"{dk}_{Rk}"] = dict(p_obs=pobs, E_p2=C["E_mejor"], E_pobs=E_p, err=C["err"], E_rad=C["radial"]["E0"],
                                         dif_pobs_rad=E_p - C["radial"]["E0"], dif_p2_rad=C["E_mejor"] - C["radial"]["E0"])
    print(f"G2 {dk} {Rk}: p_obs={pobs:.3f}  E(p=2)={C['E_mejor']:+.6e}  E(p_obs)={E_p:+.6e}  radial={C['radial']['E0']:+.6e}  err={C['err']:.1e}", flush=True)

# ---------------- G5: ajuste 2D en delta = 1.19
out["G5_ajuste2D"] = {}
for Rk in ("R1600", "R3200"):
    C = CJ["celdas"]["1.19"][Rk]
    pts = [(float(k.split("_")[0][1:]), float(k.split("_")[1][3:]), v["E0"]) for k, v in C["crudo"].items()]
    A = np.array([[1, h**4, e**2, h**4 / e] for h, e, _ in pts]); y = np.array([E for *_, E in pts])
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    dof = len(y) - 4
    s2 = float(np.sum((A @ coef - y)**2) / dof)
    cov = s2 * np.linalg.inv(A.T @ A)
    out["G5_ajuste2D"][Rk] = dict(E0_ajuste=float(coef[0]), err_estadistico=float(np.sqrt(cov[0, 0])), residuo_rms=float(np.sqrt(s2)),
                                  E_receta=C["E_mejor"], err_receta=C["err"], E_rad=C["radial"]["E0"])
    print(f"G5 1.19 {Rk}: ajuste 2D E0={coef[0]:+.4e} +- {np.sqrt(cov[0,0]):.1e} (rms {np.sqrt(s2):.1e}); receta {C['E_mejor']:+.4e} +- {C['err']:.1e}; radial {C['radial']['E0']:+.4e}", flush=True)

# ---------------- G6: sensibilidad del umbral 0.95 (informativa)
F119 = json.load(open(os.path.join(c.RES3, "20c_umbral_119_fino.json")))
out["G6_sensibilidad"] = {}
for thr in (0.75, 0.85, 0.95):
    res = {}
    for dk in ("1.18", "1.19", "1.2", "1.25"):
        C = {int(k[1:]): v for k, v in CJ["celdas"][dk].items()}
        Rs = sorted(C)
        ver = None
        for i in range(len(Rs) - 2):
            t = Rs[i:i + 3]
            E = [C[R]["radial"]["E0"] for R in t]; F = [C[R]["radial"]["F12"] for R in t]; rr = [C[R]["radial"]["r_sobre_R"] for R in t]
            eE = [C[R]["radial"]["err"] for R in t]
            a = E[1] < 0 and E[2] < 0 and abs(E[1]) > eE[1] and abs(E[2]) > eE[2] and abs(E[2] - E[1]) < 0.1 * abs(E[2])
            b = rr[0] > rr[1] > rr[2] and F[0] < F[1] < F[2] and F[2] > thr
            if a and b:
                ver = f"ligado {t}"; break
        res[dk] = ver or "no ligado o indeterminado (sin terna ligada)"
    out["G6_sensibilidad"][str(thr)] = res
    print(f"G6 umbral F12 > {thr}: {res}", flush=True)
out["tiempo_s"] = time.perf_counter() - T0
json.dump(out, open(os.path.join(c.RES3, "25_respuesta_gemini.json"), "w"), indent=1, default=float)
