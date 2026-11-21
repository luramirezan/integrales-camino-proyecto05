"""r01_recalculo.py -- revision R2: recalculo independiente (elementos espectrales de Chebyshev + exterior exacto).
1. E0 y <r>/R en celdas de control, frente a 02_disparo.json (DOP853 de E2).
2. Seis cruces delta*(R, 2R) de y y de rho calculados SIN rejilla (brentq directo en delta).
3. delta_c, r_e, m1, c a energia cero; coeficientes alpha, beta predichos y ajustados.
4. Corrimiento de los cruces por una pared en R + c_w (transferencia), para y y para rho.
Salida: resultados/r01_recalculo.json y r01_recalculo_salida.txt. Un proceso, ~5 min.
"""
import json, sys, time
import numpy as np
from scipy.optimize import brentq
import espectral as s

class Tee:
    def __init__(self, fn): self.f = open(fn, "w"); self.o = sys.stdout
    def write(self, x): self.o.write(x); self.f.write(x); self.f.flush()
    def flush(self): self.o.flush(); self.f.flush()

sys.stdout = Tee("resultados/r01_recalculo_salida.txt")
T0 = time.perf_counter()
PI2 = np.pi**2
out = {}
dis = json.load(open("../resultados/02_disparo.json"))["celdas"]
cru = json.load(open("../resultados/05_cruces.json"))

# 1. celdas de control
cel = []
for d in (1.185, 1.19, 1.1906, 1.19062, 1.1912, 1.196):
    for R in (50, 200, 800, 3200):
        r = s.E0(d, R); c_ = dis[f"{d:g}"][f"R{R}"]
        cel.append(dict(delta=d, R=R, E0=r["E0"], E0_e2=c_["E0"], dif_rel=(r["E0"] - c_["E0"]) / abs(c_["E0"]),
                        rho=r["rho"], rho_e2=c_["r_sobre_R"], dif_rho=r["rho"] - c_["r_sobre_R"]))
        print(f"celda d={d:<8} R={R:<5} E0={r['E0']:+.12e} (E2 {c_['E0']:+.12e}) rel {cel[-1]['dif_rel']:+.1e} "
              f"rho={r['rho']:.10f} dif {cel[-1]['dif_rho']:+.1e}", flush=True)
out["celdas"] = cel
out["max_dif_rel_E0"] = max(abs(x["dif_rel"]) for x in cel)
out["max_dif_rho"] = max(abs(x["dif_rho"]) for x in cel)

# 3. energia cero
inva = lambda d: s.energia_cero(d)["inv_a"]
dc = brentq(inva, 1.1900, 1.1912, xtol=1e-16, rtol=1e-15)
u, up, n0, n1 = s.INT.resolver(dc, 0.0)
C = u
r_e = 2 * (s.RM - n0 / C**2)
m1 = s.RM**2 / 2 - n1 / C**2
hd = 1e-5
ua = {k: inva(dc + k * hd) for k in (-2, -1, 1, 2)}
cpend = -(8 * (ua[1] - ua[-1]) - (ua[2] - ua[-2])) / (12 * hd)
a119 = 1 / inva(1.19)
k1 = PI2 * (4 + PI2) / (16 * (PI2 - 12))
cons = dict(delta_c=dc, dif_ref=dc - 1.1906124210606, r_e=r_e, m1=m1, c=cpend, a_119=a119,
            alpha_y=PI2 * r_e / (16 * cpend), beta_y=3 * PI2 * r_e**2 / (32 * cpend), alpha_rho=-k1 * r_e / cpend)
out["constantes"] = cons
print("constantes:", cons, flush=True)

# 2. cruces sin rejilla
memo = {}
def Y(d, R, Rw=None, obs="y"):
    Rw = R if Rw is None else Rw
    k = (d, Rw)
    if k not in memo:
        memo[k] = s.E0(d, Rw)
    r = memo[k]
    if obs == "y":
        return 2 * R * R * r["E0"] / PI2
    return r["rho"] * Rw / R        # <r> medido en la caja Rw, dividido por el R nominal

def cruce(R, obs, cw=0.0, lo=None, hi=None):
    f = lambda d: Y(d, R, R + cw, obs) - Y(d, 2 * R, 2 * R + cw, obs)
    lo = lo or 1.1905; hi = hi or (1.1925 if obs == "y" else 1.1960)
    return brentq(f, lo, hi, xtol=1e-14, rtol=1e-15)

e2 = {o: [p["delta"] for p in cru["fuentes"]["disparo"][o]["pares"]] for o in ("y", "rho")}
Rs = [50, 100, 200, 400, 800, 1600]
cr = {}
for o in ("y", "rho"):
    cr[o] = []
    for i, R in enumerate(Rs):
        d = cruce(R, o)
        cr[o].append(dict(R=R, delta=d, e2=e2[o][i], dif=d - e2[o][i]))
        print(f"cruce {o:<3} {R}/{2*R}: {d:.12f}  E2 {e2[o][i]:.12f}  dif {d - e2[o][i]:+.2e}", flush=True)
out["cruces"] = cr
# ajuste alpha, beta (pares R >= 100, sin pesos, como E2 para el disparo)
for o in ("y", "rho"):
    RR = np.array([x["R"] for x in cr[o] if x["R"] >= 100], float); dd = np.array([x["delta"] for x in cr[o] if x["R"] >= 100])
    A = np.column_stack([np.ones_like(RR), RR**-2, RR**-3])
    co = np.linalg.lstsq(A, dd, rcond=None)[0]
    dif = [cr[o][k]["delta"] - cr[o][k + 1]["delta"] for k in range(5)]
    out[f"ajuste_{o}"] = dict(delta_c=co[0], alpha=co[1], beta=co[2], dif_ref=co[0] - 1.1906124210606,
                             razones=[dif[k] / dif[k + 1] for k in range(4)],
                             richardson=(4 * cr[o][-1]["delta"] - cr[o][-2]["delta"]) / 3)
    print(f"ajuste {o}:", out[f"ajuste_{o}"], flush=True)

# 4. pared en R + c_w
BETA = 0.5826                                  # -zeta(1/2)/sqrt(2 pi) = 0.58259...
from mpmath import zeta, sqrt, pi
BETA = float(-zeta(0.5) / sqrt(2 * pi))
cw = BETA * (np.sqrt(0.05) + (np.sqrt(0.05) - np.sqrt(0.1)) / 3)
pared = []
mB = {o: [p["delta"] for p in cru["transferencia_metodo_B"][o]["pares"]] for o in ("y", "rho")}
sB = {o: [p["sigma"] for p in cru["transferencia_metodo_B"][o]["pares"]] for o in ("y", "rho")}
for i, R in enumerate(Rs):
    fila = dict(R=R)
    for o in ("y", "rho"):
        dw = cruce(R, o, cw)
        fila[o] = dict(corrimiento_pared=dw - cr[o][i]["delta"], B_menos_exacto=mB[o][i] - cr[o][i]["delta"],
                       sigma_B=sB[o][i])
    pared.append(fila)
    print(f"pared R={R}: y {fila['y']['corrimiento_pared']:+.3e} (B-exacto {fila['y']['B_menos_exacto']:+.3e}, sB {sB['y'][i]:.2e}) | "
          f"rho {fila['rho']['corrimiento_pared']:+.3e} (B-exacto {fila['rho']['B_menos_exacto']:+.3e}, sB {sB['rho'][i]:.2e})", flush=True)
out["pared"] = dict(c_w=cw, beta=BETA, filas=pared)
out["tiempo_s"] = time.perf_counter() - T0
json.dump(out, open("resultados/r01_recalculo.json", "w"), indent=1, default=float)
print(f"tiempo {out['tiempo_s']:.0f} s")
