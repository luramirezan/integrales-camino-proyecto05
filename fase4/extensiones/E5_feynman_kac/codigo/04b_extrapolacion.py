"""04b_extrapolacion.py -- E5: revision de la extrapolacion en eta del muestreo por importancia (sin simular nada nuevo).

En 04 la extrapolacion de Richardson uso p = 3.20, el promedio de los ordenes observados en (0.4/0.2, 0.2/0.1) en
delta = 3 y 1.5. Esos pares son preasintoticos: el par mas fino de delta = 3 (0.1/0.05) da 1.93, y el paso de Euler
de la deriva tiene error debil O(dt) = O(eta^2). Con p = 3.2 el extrapolado de delta = 3 queda a 3.85 sigma de la EDO.
Aqui se recalcula con p = 2 (el orden teorico) y se informan los dos. Esta revision se hizo DESPUES de ver los datos
y se dice asi en controles.md y verificacion.md; C13 se evalua con la regla original de 04.
Salida: resultados/04b_extrapolacion.json, resultados/04b_extrapolacion_salida.txt.
"""
import json
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(AQUI, "../resultados")
R4 = json.load(open(os.path.join(RES, "04_importancia.json")))
LOG = []
out = dict(p_04=R4["orden_extrapolacion"], p_revisado=2.0, delta={})
for d, P in R4["produccion"].items():
    a2, a1 = P["eta"]["0.2"]["a_mc"], P["eta"]["0.1"]["a_mc"]
    e2, e1 = P["eta"]["0.2"]["err"], P["eta"]["0.1"]["err"]
    fila = dict(a_edo=P["a_edo"])
    for nombre, p in [("p_04", R4["orden_extrapolacion"]), ("p2", 2.0)]:
        f = 1 / (2 ** p - 1)
        a0 = a1 + (a1 - a2) * f
        e0 = float(np.sqrt((e1 * (1 + f)) ** 2 + (e2 * f) ** 2))
        fila[nombre] = dict(p=p, a_extrap=a0, err=e0, dev_sigmas=(a0 - P["a_edo"]) / e0, dif_rel=(a0 - P["a_edo"]) / abs(P["a_edo"]))
    out["delta"][d] = fila
    s = (f"delta={d}: EDO {P['a_edo']:+.6f}; p={fila['p_04']['p']:.2f}: {fila['p_04']['a_extrap']:+.6f} +- "
         f"{fila['p_04']['err']:.6f} ({fila['p_04']['dev_sigmas']:+.2f} sigma); p=2: {fila['p2']['a_extrap']:+.6f} +- "
         f"{fila['p2']['err']:.6f} ({fila['p2']['dev_sigmas']:+.2f} sigma, dif_rel {fila['p2']['dif_rel']:+.1e})")
    print(s)
    LOG.append(s)
o = R4["sesgo_eta"]["3"]["ordenes"]
s = f"ordenes observados en delta = 3: {np.round(o, 2).tolist()} (el ultimo, 0.1/0.05, es el mas cercano al asintotico)"
print(s)
LOG.append(s)
json.dump(out, open(os.path.join(RES, "04b_extrapolacion.json"), "w"), indent=1)
open(os.path.join(RES, "04b_extrapolacion_salida.txt"), "w").write("\n".join(LOG) + "\n")
