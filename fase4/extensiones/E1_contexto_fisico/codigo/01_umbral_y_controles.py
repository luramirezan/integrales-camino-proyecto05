"""01_umbral_y_controles.py -- umbrales delta_c(1s, 2s, 3s) con dos metodos y controles exactos.

Criterios FIJADOS ANTES DE CORRER (17-11-2026), copiados tal cual en controles.md:
  C1  |delta_c(A) - DELTA_C_REF| < 1e-9 y |delta_c(B) - DELTA_C_REF| < 1e-9
  C2  Coulomb (delta = 0): |E0 + 1/2| < 1e-9, |<r> - 3/2| < 1e-7, |<r^2> - 3| < 1e-6 con el metodo A;
      con el metodo B (R = 60): |E0 + 1/2| < 1e-6
  C3  Hulthen delta = 1 (exacto, radial.hulthen_exacto): |E0 - E_ex| < 1e-10, |<r> - ex| < 1e-8 (metodo A)
  C4  delta_c(2s), delta_c(3s): |A - B| < 1e-8
Salida: resultados/01_umbral.json
"""
import time

import numpy as np

import comun_e1 as c
import radial

log = c.Registro()
t0 = time.perf_counter()
out = {}

# --- 1s
dA = c.umbral_A(1.1, 1.3, R=200.0)
dB_list = c.umbral_B(hs=(1 / 200, 1 / 400, 1 / 800), a=1.15, b=1.25, R=60.0)
dB = dB_list[-1]
out["delta_c_1s"] = dict(A=dA, B=dB, B_por_h={"1/200": dB_list[0], "1/400": dB_list[1], "1/800": dB_list[2]},
                         B_dispersion_h=float(max(dB_list) - min(dB_list)), ref=c.DELTA_C_REF,
                         A_menos_ref=dA - c.DELTA_C_REF, B_menos_ref=dB - c.DELTA_C_REF,
                         A_R200_menos_R100=dA - c.umbral_A(1.1, 1.3, R=100.0))
log("delta_c(1s): A (solve_ivp, energia cero) =", f"{dA:.13f}", " B (Numerov propio) =", f"{dB:.13f}",
    " ref =", c.DELTA_C_REF)
log("   B por h:", ["%.13f" % x for x in dB_list])

# --- 2s y 3s (R mayor porque el estado es mas extenso)
d2A = c.umbral_A(0.25, 0.40, R=300.0)
d2B = c.umbral_B(hs=(1 / 400,), a=0.25, b=0.40, R=150.0)[0]
d3A = c.umbral_A(0.12, 0.17, R=400.0)
d3B = c.umbral_B(hs=(1 / 400,), a=0.12, b=0.17, R=250.0)[0]
out["delta_c_2s"] = dict(A=d2A, B=d2B, dif=d2A - d2B)
out["delta_c_3s"] = dict(A=d3A, B=d3B, dif=d3A - d3B)
log("delta_c(2s): A =", f"{d2A:.11f}", " B =", f"{d2B:.11f}")
log("delta_c(3s): A =", f"{d3A:.11f}", " B =", f"{d3B:.11f}")

# --- controles exactos
cA = c.estado_1s_disparo(0.0)
cB = c.estado_1s_caja(0.0, 60.0)
out["coulomb"] = dict(A=dict(E0=cA["E0"], r_med=cA["r_med"], r2_med=cA["r2_med"]),
                      B=dict(E0=cB["E0"], r_med=cB["r_med"], r2_med=cB["r2_med"]),
                      exacto=dict(E0=-0.5, r_med=1.5, r2_med=3.0))
log("Coulomb A:", cA["E0"], cA["r_med"], cA["r2_med"], " B:", cB["E0"], cB["r_med"], cB["r2_med"])
hA = c.estado_1s_disparo(1.0, "hulthen")
hx = radial.hulthen_exacto(1.0)
out["hulthen_1"] = dict(A=dict(E0=hA["E0"], r_med=hA["r_med"], r2_med=hA["r2_med"]),
                        exacto=dict(E0=hx["E"], r_med=hx["r_med"], r2_med=hx["r2_med"]))
log("Hulthen delta=1 A:", hA["E0"], hA["r_med"], hA["r2_med"], " exacto:", hx["E"], hx["r_med"], hx["r2_med"])

# --- evaluacion de controles (criterios de la cabecera)
ctl = []
ctl.append(dict(id="C1", control="delta_c(1s) con dos metodos frente a la referencia",
                criterio="|A-ref| < 1e-9 y |B-ref| < 1e-9",
                valor=f"A-ref = {dA - c.DELTA_C_REF:.1e}; B-ref = {dB - c.DELTA_C_REF:.1e}",
                pasa=bool(abs(dA - c.DELTA_C_REF) < 1e-9 and abs(dB - c.DELTA_C_REF) < 1e-9)))
okA = abs(cA["E0"] + 0.5) < 1e-9 and abs(cA["r_med"] - 1.5) < 1e-7 and abs(cA["r2_med"] - 3) < 1e-6
ctl.append(dict(id="C2", control="Coulomb exacto (delta = 0), metodos A y B",
                criterio="A: |E0+1/2|<1e-9, |<r>-3/2|<1e-7, |<r2>-3|<1e-6; B: |E0+1/2|<1e-6",
                valor=f"A: {cA['E0'] + 0.5:.1e}, {cA['r_med'] - 1.5:.1e}, {cA['r2_med'] - 3:.1e}; B: {cB['E0'] + 0.5:.1e}",
                pasa=bool(okA and abs(cB["E0"] + 0.5) < 1e-6)))
ctl.append(dict(id="C3", control="Hulthen exacto (delta = 1), metodo A",
                criterio="|E0-E_ex| < 1e-10, |<r>-<r>_ex| < 1e-8",
                valor=f"{hA['E0'] - hx['E']:.1e}; {hA['r_med'] - hx['r_med']:.1e}",
                pasa=bool(abs(hA["E0"] - hx["E"]) < 1e-10 and abs(hA["r_med"] - hx["r_med"]) < 1e-8)))
ctl.append(dict(id="C4", control="delta_c(2s) y delta_c(3s), A frente a B",
                criterio="|A-B| < 1e-8", valor=f"2s: {d2A - d2B:.1e}; 3s: {d3A - d3B:.1e}",
                pasa=bool(abs(d2A - d2B) < 1e-8 and abs(d3A - d3B) < 1e-8)))
out["controles"] = ctl
for k in ctl:
    log(k["id"], k["control"], "|", k["valor"], "|", "pasa" if k["pasa"] else "NO PASA")
out["t_s"] = time.perf_counter() - t0
log(f"tiempo {out['t_s']:.1f} s")
c.guardar("01_umbral", out, log.texto())
