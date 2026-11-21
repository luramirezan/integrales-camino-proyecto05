"""04b_pared_rho.py -- sesgo de pared de <r>/R para la transferencia, con la misma receta que la Fase 3 usa para E0
(comun3.celda): la pared de la transferencia sin imagen se modela como una pared dura en R_w = R + BETA sqrt(eps);
se resuelve el radial h = 1/40 en R_w para eps = 0.1 y 0.05, se mide <r> y se divide por el R NOMINAL (como hace la
transferencia con r_sobre_R), se resta el radial en R (03_radial, h = 1/40, que es el mismo radial_ref de la receta) y se
extrapola en eps con la ley eps^2 (comun3.ext_eps):
    pared_rho(delta, R) = ext_eps(<r>_{R_w(0.1)}/R, <r>_{R_w(0.05)}/R) - <r>_R/R.
Se anadio tras la revision R2 (hallazgo R2-01): el metodo B de <r>/R no tenia termino de pared en la barra. Por la
decision 5 de la Fase 2 la pared solo entra en la barra, nunca en el valor central (05_cruces.py, metodo_B).
Determinista, un proceso. Salida: resultados/04b_pared_rho.json
"""
import sys, time
import numpy as np
import e2comun as c

sys.stdout = c.Tee("04b_pared_rho")
T0 = time.perf_counter()
rad = c.cargar("03_radial")["celdas"]["h40"]
BETA = c.comun3.BETA
EPS = (0.1, 0.05)
out = dict(script="04b_pared_rho.py", fecha=c.ahora(), beta=BETA, eps=list(EPS), h="1/40", deltas=list(c.DELTAS),
           Rs=list(c.RS), celdas={})
for d in c.DELTAS:
    V = c.radial.V_yukawa(d)
    fila = {}
    for R in c.RS:
        ref = rad[f"{d:g}"][f"R{R}"]["r_sobre_R"]
        rw = {}
        for e in EPS:
            Rw = R + BETA * np.sqrt(e)
            x = c.radial.resolver_rich(V, Rw, h=1 / 40, nev=1)
            rw[e] = x["r_med"] / R                      # <r> en la caja R_w, dividido por el R nominal
        ext = float(c.comun3.ext_eps(rw[0.1], rw[0.05]))
        fila[f"R{R}"] = dict(rho_R=ref, rho_Rw={f"{e:g}": float(v) for e, v in rw.items()}, rho_Rw_ext=ext,
                             pared_rho=float(ext - ref))
        print(f"d={d:<7g} R={R:<5} rho_R={ref:.9f} rho_Rw(ext)={ext:.9f} pared={ext - ref:+.3e}", flush=True)
    out["celdas"][f"{d:g}"] = fila
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("04b_pared_rho", out)
print(f"tiempo {out['tiempo_s']:.0f} s")
