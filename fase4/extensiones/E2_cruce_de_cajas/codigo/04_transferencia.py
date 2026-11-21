"""04_transferencia.py -- integral de camino (matriz de transferencia con accion de pares de Coulomb) en la rejilla de
E2, con la receta COMPLETA de la Fase 3 (comun3.celda): h = 0.02 y 0.04 (Richardson h^4), eps = 0.2, 0.1, 0.05
(ley eps^2), error = suma lineal de malla + Trotter + |sesgo de pared extrapolado| (decision 5: la pared solo en
el error). Cada celda guarda tambien los seis E0 crudos (para el metodo B del cruce) y los chequeos de Perron y residuo.
Uso: python 04_transferencia.py 50 100 200 400 800   (un proceso; cada llamada < 20 min).
Salida: resultados/04_transferencia_R<R>.json (una por caja) y 04_transferencia_<Rs>_salida.txt
"""
import os, sys, time, warnings
import e2comun as c

warnings.simplefilter("ignore")      # el aviso de pared de transferencia.resolver no aplica: la receta ya la estima
Rs = [int(x) for x in sys.argv[1:]] or [50, 100, 200, 400, 800]
sys.stdout = c.Tee("04_transferencia_" + "_".join(map(str, Rs)))
MAXD = int(os.environ.get("MAXD", "999"))   # maximo de deltas nuevos por llamada (para no pasar de ~20 min)
for R in Rs:
    T0 = time.perf_counter()
    try:
        out = c.cargar(f"04_transferencia_R{R}")       # incremental: solo calcula los deltas que faltan
    except FileNotFoundError:
        out = dict(script="04_transferencia.py", R=R, celdas={}, tiempo_s=0.0)
    hechos = 0
    for d in c.DELTAS:
        if f"{d:g}" in out["celdas"] or hechos >= MAXD:
            continue
        out["celdas"][f"{d:g}"] = c.comun3.celda(d, R)
        hechos += 1
        out["deltas"] = sorted(float(k) for k in out["celdas"])
        out["fecha"] = c.ahora()
        c.guardar(f"04_transferencia_R{R}", out)       # se guarda tras cada celda
    out["tiempo_s"] = out.get("tiempo_s", 0.0) + time.perf_counter() - T0
    c.guardar(f"04_transferencia_R{R}", out)
    print(f"R={R}: {hechos} celdas nuevas, tiempo {time.perf_counter() - T0:.0f} s; faltan "
          f"{sum(f'{d:g}' not in out['celdas'] for d in c.DELTAS)}", flush=True)
