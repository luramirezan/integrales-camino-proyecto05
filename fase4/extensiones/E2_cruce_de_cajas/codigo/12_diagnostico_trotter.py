"""12_diagnostico_trotter.py -- causa medida del control K2 (orden de Trotter fuera de [1.8, 2.2]).

Igual que fase3/codigo/20d_diagnostico_pared.py: la pared en R sin imagen anade a E(eps) un termino ~ sqrt(eps) que
compite con el error de Trotter ~ eps^2 y deforma el orden aparente. Se resta a cada E(eps) (Richardson en h) el
corrimiento medido con el radial, E_rad(R + BETA sqrt(eps)) - E_rad(R) (h = 1/40, mismo h en los dos), y se recalcula
p = log2(|E(0.2) - E(0.1)| / |E(0.1) - E(0.05)|) en todas las celdas que no pasaban K2.
Salida: resultados/12_diagnostico_trotter.json
"""
import sys
import numpy as np
import e2comun as c

sys.stdout = c.Tee("12_diagnostico_trotter")
EPS = (0.2, 0.1, 0.05)
filas = []
for R in c.RS:
    C = c.cargar(f"04_transferencia_R{R}")["celdas"]
    for dk, x in C.items():
        if 1.8 <= x["orden_trotter"] <= 2.2:
            continue
        d = float(dk)
        E0 = c.radial.resolver_rich(c.radial.V_yukawa(d), R, h=1 / 40, nev=1)["E0"]
        pared = {e: c.radial.resolver_rich(c.radial.V_yukawa(d), R + c.comun3.BETA * np.sqrt(e), h=1 / 40, nev=1)["E0"] - E0
                 for e in EPS}
        Eh = {e: float(x["E_hRich"][f"{e:g}"]) for e in EPS}
        Ec = {e: Eh[e] - pared[e] for e in EPS}
        p = float(np.log2(abs(Ec[0.2] - Ec[0.1]) / abs(Ec[0.1] - Ec[0.05])))
        filas.append(dict(delta=d, R=R, p_original=x["orden_trotter"], p_sin_pared=p))
        print(f"d={dk:<8} R={R:<5} p={x['orden_trotter']:.3f}  p sin pared={p:.3f}", flush=True)
ps = np.array([f["p_sin_pared"] for f in filas])
out = dict(script="12_diagnostico_trotter.py", fecha=c.ahora(), filas=filas, n=len(filas),
           n_en_rango_sin_pared=int(np.sum((ps >= 1.8) & (ps <= 2.2))), p_min=float(ps.min()), p_max=float(ps.max()))
c.guardar("12_diagnostico_trotter", out)
print(f"{out['n_en_rango_sin_pared']}/{out['n']} celdas en [1.8, 2.2] tras restar la pared; p en [{out['p_min']:.3f}, {out['p_max']:.3f}]")
