"""20_cajas_fase3.py -- Proyecto 05, Fase 3: barrido de tamano de caja cerca del umbral.
delta in {1.15, 1.18, 1.19, 1.20, 1.25}, R in {50, 100, 200, 400, 800, 1600, 3200}; ternas consecutivas.
Criterio 9.6 (Fase 1) con la condicion (c) (Fase 2): mismo veredicto con el radial y con la integral de camino
(transferencia extrapolada en h y eps, receta de comun3.py). Umbral de la ley de caja 0.1, fijado ANTES de ver
estos datos (decision 3, aprobada el 10-11-2026). Pared en R sin imagen: solo termino en el error (decision 5).
Determinista. Salida: fase3/resultados/20_cajas.json, fase3/figuras/20_cajas.png.
"""
import json, os, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

DELTAS = (1.15, 1.18, 1.19, 1.20, 1.25)
RS = (50, 100, 200, 400, 800, 1600, 3200)
TERNAS = [RS[i:i + 3] for i in range(len(RS) - 2)]


def trabajo(arg):
    d, R = arg
    import warnings; warnings.simplefilter("ignore")
    return (d, R, c.celda(d, R))


if __name__ == "__main__":
    T0 = time.perf_counter()
    tareas = [(d, R) for R in sorted(RS, reverse=True) for d in DELTAS]
    with Pool(int(os.environ.get("NPROC", "3"))) as p:
        res = p.map(trabajo, tareas, chunksize=1)
    cel = {d: {} for d in DELTAS}
    for d, R, x in res:
        cel[d][R] = x
    a_s = {d: c.long_dispersion(d) for d in DELTAS}
    out = dict(script="20_cajas_fase3.py", fecha="2026-11-10", umbral_ley_caja=c.UMBRAL_LEY_CAJA,
               decisiones="1 (Richardson h^4), 3 (umbral 0.1 fijado antes), 5 (pared solo en el error)",
               a_s={f"{d:g}": a_s[d] for d in DELTAS}, celdas={}, veredictos={})
    for d in DELTAS:
        out["celdas"][f"{d:g}"] = {f"R{R}": cel[d][R] for R in RS}
        V, ver, usada = {}, "indeterminado", None
        for t in TERNAS:
            rr, tt, cc = (c.evaluar(cel[d], t, "radial", a_s[d]), c.evaluar(cel[d], t, "transferencia", a_s[d]),
                          c.cond_c(cel[d], t, a_s[d]))
            V[str(tuple(t))] = dict(radial=rr, transferencia=tt, c=cc)
            print(f"d={d} terna={t}: radial lig={rr['ligado']} nolig={rr['no_ligado']} (signo,tend,ley)=({rr['nl_signo']},"
                  f"{rr['nl_tendencias']},{rr['nl_ley']}) dev={[round(x,3) for x in rr['dev_ley']]} | transf lig={tt['ligado']} "
                  f"nolig={tt['no_ligado']} | c={cc['c']}", flush=True)
            if ver == "indeterminado":
                if rr["ligado"] and tt["ligado"] and cc["c"]:
                    ver, usada = "ligado", t
                elif rr["no_ligado"] and tt["no_ligado"] and cc["c"]:
                    ver, usada = "no ligado", t
        out["veredictos"][f"{d:g}"] = dict(veredicto=ver, terna=usada, por_terna=V)
        print(f"  VEREDICTO delta={d}: {ver} (terna {usada})", flush=True)
    out["n_celdas"] = len(tareas)
    out["n_compatibles"] = int(sum(cel[d][R]["compatible"] for d in DELTAS for R in RS))
    out["perron_min_global"] = float(min(cel[d][R]["perron_min"] for d in DELTAS for R in RS))
    out["tiempo_total_s"] = time.perf_counter() - T0
    json.dump(out, open(os.path.join(c.RES3, "20_cajas.json"), "w"), indent=1, default=float)
    print(f"celdas compatibles transferencia-radial: {out['n_compatibles']}/{out['n_celdas']}; "
          f"Perron min {out['perron_min_global']:+.1e}; tiempo {out['tiempo_total_s']:.0f} s")
