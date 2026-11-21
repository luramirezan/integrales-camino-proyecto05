"""r41_comparacion.py -- revision R4: umbrales, constantes del umbral y puntos de los barridos de E4
recalculados con el metodo espectral independiente (espectral.py) y comparados con los JSON de E4.
Salida: revision/r41_comparacion.json y _salida.txt."""
import json, math, os, sys, time
import numpy as np
import espectral as s

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(AQUI), "resultados")
out = {}
log = open(os.path.join(AQUI, "r41_comparacion_salida.txt"), "w")
def p(*a):
    t = " ".join(str(x) for x in a); print(t, flush=True); log.write(t + "\n"); log.flush()

B42 = json.load(open(os.path.join(RES, "42_barridos.json")))["estados"]
C41 = json.load(open(os.path.join(RES, "41_constantes_umbral.json")))
EST = {"1s": (0, (1.1, 1.3)), "2s": (0, (0.25, 0.4)), "2p": (1, (0.18, 0.26)), "3d": (2, (0.07, 0.12))}
T0 = time.time()
# ---------------------------------------------------------------- umbrales
out["umbral"] = {}
for k, (l, br) in EST.items():
    vals = {}
    for N in (400, 500, 600):
        for c in (0.5, 1.0):
            vals[f"N{N}_c{c}"] = s.umbral(l, br[0], br[1], N=N, c=c)[0]
    v = np.array(list(vals.values()))
    dc = float(np.median(v)); disp = float(v.max() - v.min())
    e4 = B42[k]["delta_c"]
    out["umbral"][k] = dict(valores=vals, mediana=dc, dispersion=disp, E4=e4, dif=dc - e4)
    p(f"{k}: delta_c espectral = {dc:.15f} (dispersion {disp:.1e})  E4 = {e4:.15f}  dif = {dc-e4:+.1e}")
# ---------------------------------------------------------------- constantes
out["constantes"] = {}
for k, (l, br) in EST.items():
    dc = B42[k]["delta_c"]          # mismo delta_c que E4 para comparar las constantes
    a = s.constantes_umbral(l, dc, N=500)
    b = s.constantes_umbral(l, dc, N=600, c=0.5)
    ref = C41[k] if k in C41 else None
    out["constantes"][k] = dict(N500=a, N600=b)
    p(f"{k}: constantes {a}  (N=600,c=0.5: {b})")
p("constantes de E4 (41):", {k: {kk: C41[k][kk] for kk in C41[k] if kk in ("Sigma", "c0_pred", "An2", "S", "C0", "D0", "r_med0", "r2_med0")} for k in EST if k in C41})
# ---------------------------------------------------------------- puntos de los barridos
out["barridos"] = {}
objetivo = {0: (1e-2, 1e-4, 1e-6), 1: (1e-2, 1e-5, 1e-8), 2: (1e-2, 1e-5, 1e-8)}
for k, (l, br) in EST.items():
    pts = B42[k]["puntos"]
    lst = []
    for dr in objetivo[l]:
        q = min(pts, key=lambda z: abs(math.log(z["Delta_rel"] / dr)))
        kap = q["kappa"]
        res = {}
        for N in (500, 600):
            r = s.ligado(q["delta"], l, kap * 0.9, kap * 1.1, N=N)
            res[N] = r
        r = res[600]
        d = dict(Delta_rel=q["Delta_rel"], delta=q["delta"], E_esp=r["E"], E_E4=q["E"], rel_E=(r["E"] - q["E"]) / abs(q["E"]),
                 r_esp=r["r_med"], r_E4=q["r_med"], rel_r=(r["r_med"] - q["r_med"]) / q["r_med"],
                 r2_esp=r["r2_med"], r2_E4=q["r2_med"], rel_r2=(r["r2_med"] - q["r2_med"]) / q["r2_med"],
                 HF_esp=r["HF"], HF_E4=q["HF"], nodos=r["nodos"],
                 conv_N_E=(res[600]["E"] - res[500]["E"]) / abs(r["E"]), conv_N_r=(res[600]["r_med"] - res[500]["r_med"]) / r["r_med"])
        lst.append(d)
        p(f"{k} Delta/dc={q['Delta_rel']:.1e}: E rel {d['rel_E']:+.1e}  <r> rel {d['rel_r']:+.1e}  <r2> rel {d['rel_r2']:+.1e}  "
          f"(conv N: E {d['conv_N_E']:+.1e}, r {d['conv_N_r']:+.1e}; nodos {d['nodos']})")
    out["barridos"][k] = lst
# ---------------------------------------------------------------- pendiente del log en 2p (misma ventana que E4)
q2 = [z for z in B42["2p"]["puntos"] if 1e-9 * 0.999 <= z["Delta_rel"] <= 1e-7 * 1.001]
X, Y = [], []
for z in q2:
    r = s.ligado(z["delta"], 1, z["kappa"] * 0.9, z["kappa"] * 1.1, N=500)
    X.append(math.log(1 / r["kappa"])); Y.append(r["r_med"])
pend, ord_ = np.polyfit(X, Y, 1)
cst = out["constantes"]["2p"]["N500"]
# formula refinada (7') sin parametros libres
g = 0.5772156649015329
pred = [(cst["C0"] + cst["An2"] * (x + 1.25 - g - math.log(2))) * (1 + 1.5 * cst["An2"] * math.exp(-x)) for x in X]
maxrel = max(abs(a - b) / b for a, b in zip(pred, Y))
out["log_2p"] = dict(n=len(X), pendiente=pend, ordenada=ord_, An2=cst["An2"], rel=pend / cst["An2"] - 1,
                     pendiente_E4=B42["2p"]["log"]["pendiente"], max_rel_formula=maxrel)
p(f"2p log: {len(X)} puntos, pendiente {pend:.6f} (E4 {B42['2p']['log']['pendiente']:.6f}), A2 = {cst['An2']:.6f}, rel {pend/cst['An2']-1:+.2e}; "
  f"formula (7') max rel {maxrel:.1e}")
out["t"] = time.time() - T0
json.dump(out, open(os.path.join(AQUI, "r41_comparacion.json"), "w"), indent=1, default=float)
p(f"tiempo {out['t']:.0f} s")
