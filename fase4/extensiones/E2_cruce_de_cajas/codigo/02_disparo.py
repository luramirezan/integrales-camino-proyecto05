"""02_disparo.py -- referencia sin malla: E0(R) y <r>/R por disparo (DOP853, rtol 1e-12; barra numerica = diferencia con rtol 1e-13) en la rejilla de E2,
y longitud de dispersion a_s(delta) y rango efectivo r_e(delta) a energia cero (para el colapso de datos, figura D).
Se anaden deltas fuera de la rejilla principal (1.16 a 1.24) solo para el colapso. Determinista. ~3 min.
Salida: resultados/02_disparo.json, resultados/02_disparo_salida.txt
"""
import sys, time
import numpy as np
import e2comun as c

sys.stdout = c.Tee("02_disparo")
T0 = time.perf_counter()
EXTRA = (1.16, 1.17, 1.175, 1.18, 1.20, 1.205, 1.21, 1.22, 1.24)
todos = sorted(set(c.DELTAS) | set(EXTRA))
out = dict(script="02_disparo.py", fecha=c.ahora(), metodo="disparo DOP853 rtol 1e-12 desde Frobenius r0=1e-7, brentq en E",
           deltas=todos, Rs=list(c.RS), celdas={}, energia_cero={})
re_c, k_c = c.rango_efectivo_umbral(c.DELTA_C_REF)
out["umbral"] = dict(delta_c=c.DELTA_C_REF, r_e=re_c, pendiente_u_sobre_C_en_Rf=k_c)
print(f"r_e en delta_c = {re_c:.6f}  (u'/C en Rf = {k_c:.1e}, debe ser ~0)")
for d in todos:
    ez = c.energia_cero(d)
    out["energia_cero"][f"{d:g}"] = ez
    a = ez["a"]
    fila = {}
    for R in c.RS:
        Eg = c.F_escala(R / a) * np.pi**2 / (2 * R * R)
        x = c.disparo_E0(d, R, Eg, ancho=abs(Eg) * 0.05 + 1e-14)
        x13 = c.disparo_E0(d, R, x["E0"], ancho=abs(x["E0"]) * 1e-4 + 1e-16, rtol=1e-13)
        x["E0_rtol13"] = x13["E0"]; x["r_sobre_R_rtol13"] = x13["r_sobre_R"]
        x["err_y"] = float(abs(c.y_de(x13["E0"] - x["E0"], R)))
        x["err_r"] = float(abs(x13["r_sobre_R"] - x["r_sobre_R"]))
        x["y"] = float(c.y_de(x["E0"], R))
        x["y_alcance_cero"] = float(c.F_escala(R / a))
        x["rho_alcance_cero"] = float(c.G_escala(R / a))
        fila[f"R{R}"] = x
        print(f"d={d:<7g} R={R:<5} E0={x['E0']:+.12e} y={x['y']:.7f} F(R/a)={x['y_alcance_cero']:.7f} "
              f"<r>/R={x['r_sobre_R']:.7f} G={x['rho_alcance_cero']:.7f} nodos={x['nodos']}", flush=True)
    out["celdas"][f"{d:g}"] = fila
    print(f"   a_s={a:+.6e}  r_e={ez['r_e']:.6f}", flush=True)
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("02_disparo", out)
print(f"tiempo {out['tiempo_s']:.0f} s")
