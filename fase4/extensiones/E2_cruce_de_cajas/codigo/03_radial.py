"""03_radial.py -- radial de diferencias finitas (comun3.radial_ref = radial.resolver_rich, Richardson h, h/2) con
h = 1/40 (la malla de la Fase 3) y h = 1/160, en la rejilla de E2 (15 deltas x 7 cajas). Determinista. ~5 min.
Salida: resultados/03_radial.json
"""
import sys, time
import e2comun as c

sys.stdout = c.Tee("03_radial")
T0 = time.perf_counter()
out = dict(script="03_radial.py", fecha=c.ahora(), deltas=list(c.DELTAS), Rs=list(c.RS), hs=["1/40", "1/160"], celdas={})
for nombre, h in (("h40", 1 / 40), ("h160", 1 / 160)):
    out["celdas"][nombre] = {}
    for d in c.DELTAS:
        fila = {}
        for R in c.RS:
            x = c.comun3.radial_ref(d, R, h=h)
            x["y"] = float(c.y_de(x["E0"], R)); x["err_y"] = float(c.y_de(x["err"], R))
            fila[f"R{R}"] = x
            print(f"{nombre} d={d:<7g} R={R:<5} E0={x['E0']:+.12e}+-{x['err']:.1e} y={x['y']:.7f} "
                  f"<r>/R={x['r_sobre_R']:.7f}+-{x['err_r']:.1e}", flush=True)
        out["celdas"][nombre][f"{d:g}"] = fila
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("03_radial", out)
print(f"tiempo {out['tiempo_s']:.0f} s")
