"""04_importancia.py -- E5: remedio por muestreo por importancia (difusion guiada a energia cero).

Guia phi_T = solucion de energia cero del Yukawa con delta_T. Regla fijada antes (criterios_previos.md): a_T = 1.25 a,
es decir delta_c < delta_T < delta (supersolucion: E_L = q_T - q >= 0, pesos exp(-int E_L) <= 1).
Estimador: a = -(2/delta^2) E_{r0 ~ Gamma(2, 1/delta)}[ phi_T(r0) exp(-int_0^inf E_L(X_t) dt) ], X la difusion guiada.

(2) Orden del sesgo en eta (0.4, 0.2, 0.1, 0.05) en delta = 3 y 1.5 (primero, porque fija el orden p de (1)).
(1) Produccion en delta = 3, 2, 1.5, 1.3, 1.25, 1.2 con eta = 0.1 y eta = 0.2; extrapolacion de Richardson con el orden
    p de (2). N se fija con un piloto determinista de 200 caminos para gastar ~ PRESUPUESTO pasos por corrida.
(3) Varianza relativa medida frente a la cota E[phi_T phi]/E[phi]^2 - 1; pendiente de la varianza muestral con n.
Lo que esta mas cerca del umbral (1.195, 1.192, 1.1907) y las guias que no son supersoluciones estan en 05.
Salida: resultados/04_importancia.json, resultados/04_importancia_salida.txt.
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
T0 = time.perf_counter()
LOG = []
PRESUPUESTO = 7.0e8          # pasos por corrida de produccion


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def corrida(d, dT, eta, N, sem, Rin=None):
    Rin = Rin if Rin is not None else 36.0 / min(d, dT)
    g = fk.Guia(d, dT, Rin)
    rng = np.random.default_rng(sem)
    r0 = rng.gamma(2.0, 1.0 / d, N)
    t = time.perf_counter()
    L, pas = fk.simular_guiado(r0, g, eta, sem + 1000, devolver_pasos=True)
    tt = time.perf_counter() - t
    Y = g.phiT(r0) * np.exp(-L)
    return g, r0, L, Y, pas, tt


def resumen(d, Y, a_edo):
    n = Y.size
    m = Y.mean()
    e = Y.std(ddof=1) / np.sqrt(n)
    a = -(2 / d ** 2) * m
    ea = 2 / d ** 2 * e
    return dict(a_mc=float(a), err=float(ea), a_edo=a_edo, dif_rel=float((a - a_edo) / abs(a_edo)),
                dev_sigmas=float((a - a_edo) / ea), var_rel=float(Y.var(ddof=1) / m ** 2))


def pendiente_var(Y, nrep=10):
    nb = Y.size // nrep
    if nb < 2000:
        return float("nan")
    ns = np.unique(np.geomspace(100, nb, 25).astype(int))
    V = []
    for i in range(nrep):
        b = Y[i * nb:(i + 1) * nb]
        c1, c2 = np.cumsum(b), np.cumsum(b * b)
        n_ = ns.astype(float)
        m = c1[ns - 1] / n_
        V.append((c2[ns - 1] - n_ * m * m) / (n_ - 1))
    vm = np.median(np.array(V), axis=0)
    return float(np.polyfit(np.log(ns), np.log(vm), 1)[0])


out = dict(presupuesto_pasos=PRESUPUESTO, produccion={}, sesgo_eta={})

# ------------------------------------------------------------------ (2) orden del sesgo en eta
for d, N in [(3.0, 400_000), (1.5, 100_000)]:
    a_edo = fk.a_disparo(d)
    dT = fk.dT_para_razon(d, 1.25)
    filas = []
    for k, eta in enumerate([0.4, 0.2, 0.1, 0.05]):
        sem = 202700 + int(100 * d) + k
        g, r0, L, Y, pas, tt = corrida(d, dT, eta, N, sem)
        res = resumen(d, Y, a_edo)
        res.update(eta=eta, N=N, semilla=sem, tiempo_s=tt, pasos_medios=float(pas.mean()))
        filas.append(res)
        log(f"(2) delta={d} eta={eta}: a_MI = {res['a_mc']:+.6f} +- {res['err']:.6f} ({res['dev_sigmas']:+.2f} sigma, "
            f"dif_rel {res['dif_rel']:+.2e}), {tt:.1f} s, pasos/camino {pas.mean():.0f}")
    b_ = np.array([f["dif_rel"] for f in filas])
    ordenes = [float(np.log2(abs(b_[i]) / abs(b_[i + 1]))) for i in range(3)]
    out["sesgo_eta"][f"{d:g}"] = dict(filas=filas, ordenes=ordenes)
    log(f"(2) delta={d}: ordenes observados (0.4/0.2, 0.2/0.1, 0.1/0.05) = {np.round(ordenes, 2).tolist()}")
# orden que se usa en la extrapolacion: el de 0.4/0.2 y 0.2/0.1 (donde el sesgo supera al ruido), promediado
p_ext = float(np.mean([out["sesgo_eta"][k]["ordenes"][i] for k in out["sesgo_eta"] for i in (0, 1)]))
out["orden_extrapolacion"] = p_ext
log(f"(2) orden usado en la extrapolacion de Richardson: p = {p_ext:.3f}")

# ------------------------------------------------------------------ (1) produccion con eta = 0.2 y 0.1
DS = [3.0, 2.0, 1.5, 1.3, 1.25, 1.2]
for j, d in enumerate(DS):
    a_edo = fk.a_disparo(d)
    dT = fk.dT_para_razon(d, 1.25)
    filas = {}
    for k, eta in enumerate([0.2, 0.1]):
        sem = 202650 + 10 * j + k
        _, _, _, _, pas0, _ = corrida(d, dT, eta, 200, sem + 5)        # piloto determinista
        N = int(min(1_000_000, max(2000, PRESUPUESTO / float(pas0.mean()))))
        g, r0, L, Y, pas, tt = corrida(d, dT, eta, N, sem)
        res = resumen(d, Y, a_edo)
        res.update(delta_T=dT, a_T=g.aT, N=N, semilla=sem, eta=eta, tiempo_s=tt, pasos_medios=float(pas.mean()),
                   pasos_p99=float(np.percentile(pas, 99)), pasos_max=int(pas.max()), ns_por_paso=1e9 * tt / pas.sum(),
                   L_min=float(L.min()), peso_max=float(np.exp(-L.min())),
                   cota_var_rel=REF["mi_regla"][f"{d:g}"]["cota_var_rel_gamma"], pendiente_var=pendiente_var(Y))
        filas[f"{eta:g}"] = res
        log(f"(1) delta={d} eta={eta}: delta_T={dT:.7f} a_T={g.aT:+.3f}; N={N}, {tt:.1f} s, pasos/camino "
            f"{pas.mean():.0f} (p99 {np.percentile(pas, 99):.0f}); a_MI = {res['a_mc']:+.6f} +- {res['err']:.6f} "
            f"({res['dev_sigmas']:+.2f} sigma, dif_rel {res['dif_rel']:+.2e}); var_rel = {res['var_rel']:.4f} "
            f"(cota {res['cota_var_rel']:.4f}); peso max = {res['peso_max']:.6f}; pendiente var = {res['pendiente_var']:+.3f}")
        del L, Y, r0, pas
    a2, a1 = filas["0.2"]["a_mc"], filas["0.1"]["a_mc"]
    e2, e1 = filas["0.2"]["err"], filas["0.1"]["err"]
    corr = (a1 - a2) / (2 ** p_ext - 1)
    a_ext = a1 + corr
    e_ext = float(np.sqrt((e1 * (1 + 1 / (2 ** p_ext - 1))) ** 2 + (e2 / (2 ** p_ext - 1)) ** 2))
    sig_tot = e1 + abs(corr)                       # criterio C13: estadistica + sesgo medido (suma lineal)
    resumen_d = dict(eta=filas, a_eta01=a1, sesgo_estimado_eta01=-corr, sigma_total_eta01=sig_tot,
                     dev_eta01_sigma_total=(a1 - a_edo) / sig_tot, a_extrap=a_ext, err_extrap=e_ext,
                     dev_extrap_sigmas=(a_ext - a_edo) / e_ext, a_edo=a_edo)
    out["produccion"][f"{d:g}"] = resumen_d
    log(f"(1) delta={d}: eta=0.1 a = {a1:+.6f}, sesgo estimado {-corr:+.2e}, sigma total {sig_tot:.2e} -> "
        f"{(a1-a_edo)/sig_tot:+.2f}; extrapolado {a_ext:+.6f} +- {e_ext:.6f} frente a {a_edo:+.6f} "
        f"({(a_ext-a_edo)/e_ext:+.2f} sigma)")

out["tiempo_s"] = time.perf_counter() - T0
log(f"tiempo total {out['tiempo_s']:.1f} s")
json.dump(out, open(os.path.join(RES, "04_importancia.json"), "w"), indent=1)
open(os.path.join(RES, "04_importancia_salida.txt"), "w").write("\n".join(LOG) + "\n")
