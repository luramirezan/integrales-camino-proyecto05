"""12b_pigs_replica_tau5.py -- replica independiente del punto tau = 5 de 12_pigs_produccion.py.

Motivo: en la ejecucion de produccion, E_mixto(tau=5) por PIGS quedo a -3.2 sigma de la transferencia
(unico valor fuera de 2 sigma de los 12 comparados). Esta replica usa 16 semillas NUEVAS
(20262050..20262065), 8 cadenas de 3e4 + 500 barridos cada una por tanda (dos tandas), el mismo
eps = 0.1, tau = 5, interpolacion bicubica, y compara de nuevo con la transferencia.
No sustituye al resultado original: se reportan los dos.
Salida: resultados/12b_pigs_replica.json
"""
import os
import sys
import json
import time
import multiprocessing as mp
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pares, pigs, transferencia  # noqa: E402,E401

T0 = time.perf_counter()
EPS, TAU, DL = 0.1, 5.0, 0.2
TAB = pares.tabla_richardson(EPS)
U = pigs.interpolador(TAB, "bicubica")
SEMS = [20262050 + k for k in range(16)]


def det(h):
    T, r = transferencia.matriz_T(40.0, h, EPS, W=transferencia.W_yukawa(DL), tabla=TAB)
    uT = r * np.exp(-r); HuT = (pigs.W_yukawa(DL)(r) - 0.5) * uT
    x = uT.copy()
    for _ in range(int(round(TAU / EPS)) // 2):
        x = T @ x; x /= np.abs(x).max()
    rp = float((r * x**2).sum() / (x**2).sum())
    for _ in range(int(round(TAU / EPS)) // 2):
        x = T @ x; x /= np.abs(x).max()
    return float((HuT @ x) / (uT @ x)), rp


(e2, r2), (e4, r4) = det(0.02), det(0.04)
Edet, rdet = (16 * e2 - e4) / 15, (16 * r2 - r4) / 15
print(f"transferencia tau=5 (Richardson h^4): E_mixto={Edet:.9f}  <r>_puro={rdet:.7f}")


def correr(s):
    return pigs.cadena(DL, TAU, EPS, 30000, s, U, L=10, ntherm=500, nscale=4)


with mp.get_context("fork").Pool(4) as pool:
    outs = pool.map(correr, SEMS, chunksize=1)
res = {}
for nombre, sub in (("tanda_A", outs[:8]), ("tanda_B", outs[8:]), ("las_16", outs)):
    cE = pigs.combinar([o["EL"] for o in sub]); cr = pigs.combinar([o["rmid"] for o in sub])
    sE = (cE["media"] - Edet) / cE["err"]; sr = (cr["media"] - rdet) / cr["err"]
    res[nombre] = dict(E=cE, r=cr, sigma_E=sE, sigma_r=sr, semillas=[o["seed"] for o in sub])
    print(f"{nombre}: E={cE['media']:.6f} +- {cE['err']:.6f} ({sE:+.2f} sigma)   <r>={cr['media']:.4f} +- {cr['err']:.4f} "
          f"({sr:+.2f} sigma)")
out = dict(script="fase2/codigo/12b_pigs_replica_tau5.py", eps=EPS, tau=TAU, delta=DL, E_det=Edet, r_det=rdet,
           replica=res, tiempo_s=time.perf_counter() - T0)
with open(os.path.join(os.path.dirname(AQUI), "resultados", "12b_pigs_replica.json"), "w") as f:
    json.dump(out, f, indent=1)
print(f"tiempo {out['tiempo_s']:.1f} s")
