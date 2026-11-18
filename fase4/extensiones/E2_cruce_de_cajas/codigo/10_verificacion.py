"""10_verificacion.py -- comprobaciones independientes de los resultados de E2 (para verificacion.md). ~5 min, un proceso.

V1. Cruces SIN interpolacion: brentq en delta sobre y(delta, R) - y(delta, 2R) calculando el disparo en cada delta pedido
    (no usa la rejilla ni el spline). Se compara con los cruces del disparo interpolado (05) y con el modelo ERE (01).
V2. delta_c por energia cero recalculado aqui (brentq sobre 1/a(delta)), frente a la referencia 1.1906124210606.
V3. Sensibilidad del disparo a r0 (1e-7 frente a 1e-6) y a rtol (1e-12 frente a 1e-13) en las celdas del cruce mayor.
V4. Convergencia del radial en la malla en delta = 1.1906, R = 800: h = 1/40, 1/80, 1/160, 1/320, 1/640 frente al disparo.
V5. Monotonia de Dirichlet: E0(R) decrece con R en todas las celdas de las tres fuentes.
V6. Estabilidad de la barra Monte Carlo: se repite el cruce de la transferencia (par mayor) con otra semilla.
Salida: resultados/10_verificacion.json
"""
import sys, time
import numpy as np
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline
import e2comun as c

sys.stdout = c.Tee("10_verificacion")
T0 = time.perf_counter()
out = dict(script="10_verificacion.py", fecha=c.ahora())
X = c.cargar("05_cruces"); TEO = c.cargar("01_teoria")


def y_disp(d, R, obs="y"):
    a = c.energia_cero(d)["a"]
    Eg = c.F_escala(R / a) * np.pi**2 / (2 * R * R)
    x = c.disparo_E0(d, R, Eg, ancho=abs(Eg) * 0.05 + 1e-14)
    return c.y_de(x["E0"], R) if obs == "y" else x["r_sobre_R"]


# V1
v1 = []
for obs in ("y", "rho"):
    for f in X["fuentes"]["disparo"][obs]["pares"]:
        R = f["R"]
        g = lambda d: y_disp(d, R, obs) - y_disp(d, 2 * R, obs)
        w = 2e-5 + abs(f["delta"] - c.DELTA_C_REF)
        dd = brentq(g, f["delta"] - w, f["delta"] + w, xtol=1e-12)
        v1.append(dict(obs=obs, R=R, sin_interp=dd, interpolado=f["delta"], ERE=f.get("prediccion_ERE"),
                       dif_interp=dd - f["delta"], dif_ERE=dd - f.get("prediccion_ERE", np.nan)))
        print(f"V1 {obs} {R}/{2*R}: sin interpolar {dd:.10f}  interpolado {f['delta']:.10f}  dif {dd - f['delta']:+.1e}  "
              f"ERE-dif {dd - f.get('prediccion_ERE', np.nan):+.1e}", flush=True)
out["V1_cruces_sin_interpolar"] = v1
# V2
dc0 = brentq(lambda d: 1.0 / c.energia_cero(d)["a"], 1.1906, 1.1907, xtol=1e-14)
out["V2_delta_c_energia_cero"] = dict(valor=dc0, dif_ref=dc0 - c.DELTA_C_REF)
print(f"V2 delta_c (1/a = 0) = {dc0:.13f}  dif ref {dc0 - c.DELTA_C_REF:+.1e}")
# V3
v3 = []
r0_orig = c.R0
for (d, R) in ((1.19061, 1600), (1.19061, 3200), (1.1906, 800)):
    base = c.disparo_E0(d, R, y_disp(d, R) * np.pi**2 / (2 * R * R), ancho=1e-12)
    c.R0 = 1e-6
    alt = c.disparo_E0(d, R, base["E0"], ancho=abs(base["E0"]) * 1e-4)
    c.R0 = r0_orig
    v3.append(dict(delta=d, R=R, E_r0_1e7=base["E0"], E_r0_1e6=alt["E0"], dif_rel=(alt["E0"] - base["E0"]) / base["E0"],
                   dif_y=c.y_de(alt["E0"] - base["E0"], R)))
    print(f"V3 d={d} R={R}: E(r0=1e-7)={base['E0']:.12e} E(r0=1e-6)={alt['E0']:.12e} dif_y={v3[-1]['dif_y']:+.1e}")
out["V3_r0"] = v3
# V4
d, R = 1.1906, 800
Ed = c.disparo_E0(d, R, 1.92e-6, ancho=1e-9)["E0"]
v4 = []
for k in (40, 80, 160, 320, 640):
    x = c.radial.resolver(c.radial.V_yukawa(d), R, h=1 / k, nev=1)
    v4.append(dict(h=f"1/{k}", E=x["E0"], dif=x["E0"] - Ed))
p = [float(np.log2(v4[i]["dif"] / v4[i + 1]["dif"])) for i in range(len(v4) - 1)]
out["V4_malla_radial"] = dict(delta=d, R=R, E_disparo=Ed, filas=v4, orden=p)
print("V4 radial sin Richardson, dif frente al disparo:", [f"{v['h']}: {v['dif']:+.2e}" for v in v4], "orden", p)
# V5
D = c.cargar("02_disparo"); RA = c.cargar("03_radial")
viol = []
for dk in [f"{x:g}" for x in c.DELTAS]:
    Es = [D["celdas"][dk][f"R{R}"]["E0"] for R in c.RS]
    if any(Es[i + 1] > Es[i] for i in range(len(Es) - 1)): viol.append(("disparo", dk))
    for nm in ("h40", "h160"):
        Es = [RA["celdas"][nm][dk][f"R{R}"]["E0"] for R in c.RS]
        if any(Es[i + 1] > Es[i] for i in range(len(Es) - 1)): viol.append((nm, dk))
    Et = [c.cargar(f"04_transferencia_R{R}")["celdas"][dk]["E_mejor"] for R in X["R_transferencia"]]
    if any(Et[i + 1] > Et[i] for i in range(len(Et) - 1)): viol.append(("transferencia", dk))
out["V5_monotonia"] = dict(violaciones=viol)
print("V5 violaciones de monotonia:", viol)
# V6
Rt = X["R_transferencia"]; DEL = np.array(c.DELTAS)
TR = {R: c.cargar(f"04_transferencia_R{R}")["celdas"] for R in Rt}
R1, R2 = Rt[-2], Rt[-1]
y1 = np.array([c.y_de(TR[R1][f"{d:g}"]["E_mejor"], R1) for d in DEL]); s1 = np.array([c.y_de(TR[R1][f"{d:g}"]["err"], R1) for d in DEL])
y2 = np.array([c.y_de(TR[R2][f"{d:g}"]["E_mejor"], R2) for d in DEL]); s2 = np.array([c.y_de(TR[R2][f"{d:g}"]["err"], R2) for d in DEL])
f0 = [f for f in X["fuentes"]["transferencia"]["y"]["pares"] if f["R"] == R1][0]
sig = {}
for semilla in (1, 2):
    rng = np.random.default_rng(semilla)
    reps = []
    for k in range(4000):
        Dv = (y1 + s1 * rng.standard_normal(len(DEL))) - (y2 + s2 * rng.standard_normal(len(DEL)))
        cs = CubicSpline(DEL, Dv)
        xf = np.linspace(DEL[0], DEL[-1], 20001); vf = cs(xf)
        ii = np.nonzero(np.sign(vf[1:]) != np.sign(vf[:-1]))[0]
        if len(ii):
            m = ii[np.argmin(np.abs(xf[ii] - f0["delta"]))]; reps.append(xf[m])
    sig[semilla] = float(np.std(reps))
out["V6_semilla"] = dict(par=[R1, R2], sigma_mc_05=f0["sigma_mc"], sigma_semilla1=sig[1], sigma_semilla2=sig[2])
print(f"V6 par {R1}/{R2}: sigma MC en 05 {f0['sigma_mc']:.2e}; semillas 1 y 2 (4000 replicas): {sig[1]:.2e}, {sig[2]:.2e}")
# V7: ajuste en R sin pesos frente al ponderado (decision E2-04)
v7 = {}
for fu in ("transferencia", "radial_h160"):
    for obs in ("y", "rho"):
        pr = [f for f in X["fuentes"][fu][obs]["pares"] if f["R"] >= 100]
        Rr = np.array([f["R"] for f in pr], float); dd = np.array([f["delta"] for f in pr])
        A = np.column_stack([np.ones_like(Rr), Rr**-2, Rr**-3])
        coef = np.linalg.lstsq(A, dd, rcond=None)[0]
        v7[f"{fu}_{obs}"] = dict(sin_pesos=float(coef[0]), ponderado=X["fuentes"][fu][obs]["extrapolacion"]["ajuste_ab"]["delta_c"],
                                 barra=X["fuentes"][fu][obs]["extrapolacion"]["barra_total"])
        print(f"V7 {fu} {obs}: sin pesos {coef[0]:.10f}  ponderado {v7[f'{fu}_{obs}']['ponderado']:.10f}  barra {v7[f'{fu}_{obs}']['barra']:.1e}")
out["V7_pesos"] = v7
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("10_verificacion", out)
print(f"tiempo {out['tiempo_s']:.0f} s")
