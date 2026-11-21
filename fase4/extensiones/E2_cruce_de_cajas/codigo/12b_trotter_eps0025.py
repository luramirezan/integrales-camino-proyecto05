"""12b_trotter_eps0025.py -- causa medida de K2 en R = 3200: se anade eps = 0.025 (tabla de pares ya en la cache de la Fase 2)
en dos celdas y se miden los ordenes aparentes con las ternas (0.2, 0.1, 0.05) y (0.1, 0.05, 0.025).
Si el segundo es ~2, la desviacion viene de terminos de orden superior en eps = 0.2 (que la receta usa solo en la barra).
Salida: resultados/12b_trotter_eps0025.json
"""
import sys, warnings
import numpy as np
import e2comun as c
warnings.simplefilter("ignore")
sys.stdout = c.Tee("12b_trotter_eps0025")
out = dict(script="12b_trotter_eps0025.py", fecha=c.ahora(), filas=[])
for d, R in ((1.1906, 3200), (1.1906, 800)):
    E = {}
    Eg = c.cargar(f"04_transferencia_R{R}")["celdas"][f"{d:g}"]["E_mejor"]
    for h in (0.02, 0.04):
        for e in (0.2, 0.1, 0.05, 0.025):
            E[(h, e)] = c.comun3.resolver_tr(d, R, h, e, Eg)["E0"]
    EhR = {e: (16 * E[(0.02, e)] - E[(0.04, e)]) / 15 for e in (0.2, 0.1, 0.05, 0.025)}
    p1 = float(np.log2(abs(EhR[0.2] - EhR[0.1]) / abs(EhR[0.1] - EhR[0.05])))
    p2 = float(np.log2(abs(EhR[0.1] - EhR[0.05]) / abs(EhR[0.05] - EhR[0.025])))
    ext1 = c.comun3.ext_eps(EhR[0.1], EhR[0.05]); ext2 = c.comun3.ext_eps(EhR[0.05], EhR[0.025])
    out["filas"].append(dict(delta=d, R=R, EhR={f"{e:g}": v for e, v in EhR.items()}, p_02_01_005=p1, p_01_005_0025=p2,
                             E_ext_receta=ext1, E_ext_con_0025=ext2, dif_rel=(ext2 - ext1) / ext1))
    print(f"d={d} R={R}: p(0.2,0.1,0.05)={p1:.3f}  p(0.1,0.05,0.025)={p2:.3f}  E_ext receta={ext1:.10e}  con 0.025={ext2:.10e}", flush=True)
c.guardar("12b_trotter_eps0025", out)
