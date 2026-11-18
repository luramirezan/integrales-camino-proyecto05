"""05_cerca_umbral.py -- E5: que tan cerca de delta_c llega el muestreo por importancia, y guias que no son supersoluciones.

(1) delta = 1.2, 1.195, 1.192, 1.1907 (a de -143 a ~ -1.5e4) con la regla a_T = 1.25 a y eta = 0.2 (con eta = 0.1 el costo
    se multiplica por ~4). Presupuesto fijo de pasos por delta; se mide el costo por camino frente a |a_T| y el error
    relativo alcanzado. El sesgo relativo de eta = 0.2 se toma de 04/04b: el maximo, en delta <= 1.5, de
    |a(eta = 0.2) - a_extrapolado(p = 2)|/|a|, y se suma (linealmente) al error estadistico.
(2) Guias que NO son supersolucion (delta_T > delta) en delta = 1.5: delta_T = 1.8 (dentro de la region de varianza
    finita del mapa de 01) y delta_T = 3.0 (fuera). Cola del peso: exponente medido frente al predicho, el menor p > 1
    con (1 - p) q_T + p q critico.
Salida: resultados/05_cerca_umbral.json, resultados/05_cerca_umbral_salida.txt.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import brentq

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fk_comun as fk  # noqa: E402

RES = os.path.join(AQUI, "../resultados")
REF = json.load(open(os.path.join(RES, "01_referencia_edo.json")))
MI4 = json.load(open(os.path.join(RES, "04_importancia.json")))
X4 = json.load(open(os.path.join(RES, "04b_extrapolacion.json")))["delta"]
T0 = time.perf_counter()
LOG = []
PRESUPUESTO = 1.5e9


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def corrida(d, dT, eta, N, sem):
    g = fk.Guia(d, dT, 36.0 / min(d, dT))
    rng = np.random.default_rng(sem)
    r0 = rng.gamma(2.0, 1.0 / d, N)
    t = time.perf_counter()
    L, pas = fk.simular_guiado(r0, g, eta, sem + 1000, devolver_pasos=True)
    return g, r0, L, g.phiT(r0) * np.exp(-L), pas, time.perf_counter() - t


out = dict(presupuesto_pasos=PRESUPUESTO, cerca={}, subsolucion={})
# sesgo relativo de eta = 0.2: maximo en delta <= 1.5 de |a(0.2) - a_extrap(p = 2)| / |a| (sin usar la EDO)
cand = {k: abs(MI4["produccion"][k]["eta"]["0.2"]["a_mc"] - X4[k]["p2"]["a_extrap"]) / abs(X4[k]["p2"]["a_extrap"])
        for k in ["1.5", "1.3", "1.25", "1.2"]}
sesgo02_rel = float(max(cand.values()))
out["sesgo_rel_eta02_candidatos"] = cand
out["sesgo_rel_eta02_usado"] = sesgo02_rel
log(f"sesgo relativo de eta = 0.2 (maximo de 04/04b en delta <= 1.5): {sesgo02_rel:.2e}; candidatos {cand}")

from scipy.special import roots_genlaguerre  # noqa: E402
xl, wl = roots_genlaguerre(120, 1)
for j, d in enumerate([1.2, 1.195, 1.192, 1.1907]):
    a_edo = fk.a_disparo(d)
    dT = fk.dT_para_razon(d, 1.25)
    sem = 202900 + 10 * j
    _, _, _, _, pas0, _ = corrida(d, dT, 0.2, 100, sem + 5)
    ppc = float(pas0.mean())
    N = int(min(200_000, max(200, PRESUPUESTO / ppc)))
    g, r0, L, Y, pas, tt = corrida(d, dT, 0.2, N, sem)
    m, e = Y.mean(), Y.std(ddof=1) / np.sqrt(N)
    a = -(2 / d ** 2) * m
    ea = 2 / d ** 2 * e
    sig = ea + sesgo02_rel * abs(a_edo)
    phT = fk.phi_edo(dT, xl / d)[0]
    ph = fk.phi_edo(d, xl / d)[0]
    cota = float(np.sum(wl * phT * ph) / np.sum(wl * ph) ** 2 - 1)
    res = dict(delta=d, delta_T=dT, a_T=g.aT, a_edo=a_edo, N=N, semilla=sem, tiempo_s=tt, pasos_medios=float(pas.mean()),
               pasos_p99=float(np.percentile(pas, 99)), a_mc=float(a), err=float(ea), sigma_total=float(sig),
               dev_sigma_total=float((a - a_edo) / sig), err_rel=float(ea / abs(a_edo)), var_rel=float(Y.var(ddof=1) / m ** 2),
               cota_var_rel=cota, peso_max=float(np.exp(-L.min())), ns_por_paso=1e9 * tt / pas.sum())
    out["cerca"][f"{d:g}"] = res
    log(f"(1) delta={d}: a_EDO={a_edo:+.2f}, delta_T={dT:.8f} (a_T={g.aT:+.2f}); N={N}, {tt:.0f} s, pasos/camino "
        f"{pas.mean():.0f}; a_MI = {a:+.3f} +- {ea:.3f} (rel {ea/abs(a_edo):.2e}; con sesgo {sig:.3f}: "
        f"{(a-a_edo)/sig:+.2f}); var_rel = {res['var_rel']:.3f} (cota {cota:.3f}); peso max = {res['peso_max']:.6f}")
    del L, Y, r0, pas
aT = np.array([abs(out["cerca"][k]["a_T"]) for k in out["cerca"]])
pp = np.array([out["cerca"][k]["pasos_medios"] for k in out["cerca"]])
pend = float(np.polyfit(np.log(aT), np.log(pp), 1)[0])
out["costo"] = dict(a_T=aT.tolist(), pasos_medios=pp.tolist(), pendiente_loglog=pend)
log(f"(1) pasos por camino frente a |a_T|: pendiente log-log = {pend:.3f} (prediccion 1)")

# ------------------------------------------------------------------ (2) guias que no son supersoluciones (delta = 1.5)
d = 1.5
a_edo = fk.a_disparo(d)
mapa = REF["mapa_varianza_MI"]
dTmax15 = float(np.interp(d, [m["delta"] for m in mapa], [m["delta_T_max"] for m in mapa]))


def alfa(qe):
    return fk.regular(qe, p=1.0, Rf=40.0)["upR"]


for k, dT in enumerate([1.8, 3.0]):
    F = lambda p, dT=dT: alfa(lambda r: (1 - p) * fk.q_yuk(r, dT) + p * fk.q_yuk(r, d))
    ps = np.linspace(1.0001, 12, 300)
    vals = np.array([F(p) for p in ps])
    ic = np.flatnonzero(np.sign(vals[1:]) != np.sign(vals[:-1]))
    th_pred = float(brentq(F, ps[ic[0]], ps[ic[0] + 1])) if ic.size else float("inf")
    N = 1_000_000
    sem = 202800 + k
    g, r0, L, Y, pas, tt = corrida(d, dT, 0.2, N, sem)
    G = -L
    u = np.quantile(G, 0.99)
    exc = G[G > u] - u
    th = 1 / exc.mean()
    m, e = Y.mean(), Y.std(ddof=1) / np.sqrt(N)
    out["subsolucion"][f"{dT:g}"] = dict(
        delta=d, delta_T=dT, a_T=g.aT, N=N, semilla=sem, tiempo_s=tt, a_mc=float(-(2 / d ** 2) * m),
        err_ingenuo=float(2 / d ** 2 * e), a_edo=a_edo, theta_pred=th_pred, theta_MC=float(th),
        err_theta=float(th / np.sqrt(exc.size)), delta_T_max_mapa=dTmax15, varianza_finita_pred=bool(th_pred > 2),
        peso_max=float(np.exp(G.max())), var_rel=float(Y.var(ddof=1) / m ** 2))
    log(f"(2) delta=1.5, delta_T={dT} (mapa: varianza finita si delta_T < {dTmax15:.3f}): a = {-(2/d**2)*m:+.5f} "
        f"(+- {2/d**2*e:.5f} ingenuo) frente a {a_edo:+.5f}; cola del peso theta_MC = {th:.3f} +- "
        f"{th/np.sqrt(exc.size):.3f}, predicho {th_pred:.3f}; peso max = {np.exp(G.max()):.3g}")

out["tiempo_s"] = time.perf_counter() - T0
log(f"tiempo total {out['tiempo_s']:.1f} s")
json.dump(out, open(os.path.join(RES, "05_cerca_umbral.json"), "w"), indent=1)
open(os.path.join(RES, "05_cerca_umbral_salida.txt"), "w").write("\n".join(LOG) + "\n")
