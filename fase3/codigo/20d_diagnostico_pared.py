"""20d_diagnostico_pared.py -- Proyecto 05, Fase 3: por que el orden de Trotter sale fuera de [1.8, 2.2] en algunas cajas.
Hipotesis (de la Fase 2, seccion 14.4): la pared en R sin imagen corre la caja a R + 0.5826 sqrt(eps). Prueba: comparar
E_hRich(eps) de la transferencia con el radial en R + 0.5826 sqrt(eps) y medir el orden de esa diferencia.
Celdas: todas las que dan orden fuera de [1.8, 2.2] en 20_cajas.json con R <= 800 (el radial en R + beta sqrt(eps) es barato).
Salida: fase3/resultados/20d_pared.json."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

J = json.load(open(os.path.join(c.RES3, "20_cajas.json")))
out = {}
for d, C in J["celdas"].items():
    for Rk, x in C.items():
        R = int(Rk[1:])
        if 1.8 <= x["orden_trotter"] <= 2.2 or R > 800:
            continue
        dif = [x["E_hRich"][e] - c.radial.resolver_rich(c.radial.V_yukawa(float(d)), R + c.BETA * np.sqrt(float(e)), h=1 / 40, nev=1)["E0"]
               for e in ("0.2", "0.1", "0.05")]
        p = float(np.log2(abs(dif[0] - dif[1]) / abs(dif[1] - dif[2])))
        out[f"{d}_{Rk}"] = dict(orden_sin_corregir=x["orden_trotter"], orden_pared_corregida=p, dif=dif)
        print(f"delta={d} R={R}: orden {x['orden_trotter']:.3f} -> {p:.3f} con la pared en R + beta sqrt(eps)", flush=True)
json.dump(out, open(os.path.join(c.RES3, "20d_pared.json"), "w"), indent=1)
