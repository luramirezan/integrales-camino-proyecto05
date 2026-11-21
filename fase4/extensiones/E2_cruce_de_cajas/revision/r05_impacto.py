"""r05_impacto.py -- revision R2: (1) metodo B de <r>/R con el termino de pared que le falta (corrimiento del cruce de
rho por la pared en R + c_w, calculado con el solucionador espectral en r01), reajuste ponderado igual que 05_cruces;
(2) clasificacion de delta = 1.19 con pocas cajas: los cruces solo acotan delta_c por ARRIBA (r_e > 0), asi que hace
falta la ley 1/R^2 (Richardson de dos pares) o los coeficientes predichos; (3) cifra 'tras restar la pared'.
Salida: resultados/r05_impacto.json"""
import json
import numpy as np
cru = json.load(open("../resultados/05_cruces.json"))
r01 = json.load(open("resultados/r01_recalculo.json"))
REF = 1.1906124210606
out = {}
# (1) B rho con pared
B = cru["transferencia_metodo_B"]["rho"]["pares"]
pw = {f["R"]: f["rho"]["corrimiento_pared"] for f in r01["pared"]["filas"]}
ex = {f["R"]: f["delta"] for f in r01["cruces"]["rho"]}
filas = []
for f in B:
    s_new = f["sigma"] + abs(pw[f["R"]])
    filas.append(dict(R=f["R"], delta=f["delta"], sigma_E2=f["sigma"], pared=pw[f["R"]], sigma_corregida=s_new,
                      B_menos_exacto=f["delta"] - ex[f["R"]],
                      cubre_E2=bool(abs(f["delta"] - ex[f["R"]]) <= f["sigma"]),
                      cubre_corregida=bool(abs(f["delta"] - ex[f["R"]]) <= s_new)))
def extrap(fs, key):
    u = [x for x in fs if x["R"] >= 100]
    Rs = np.array([x["R"] for x in u], float); ds = np.array([x["delta"] for x in u]); sg = np.array([x[key] for x in u])
    A = np.column_stack([np.ones_like(Rs), Rs**-2, Rs**-3]); W = 1 / sg
    co = np.linalg.lstsq(A * W[:, None], ds * W, rcond=None)[0]
    L = np.linalg.pinv(A * W[:, None])[0] * W
    sl = float(np.sum(np.abs(L) * sg))
    rich = (4 * u[-1]["delta"] - u[-2]["delta"]) / 3
    bar = sl + abs(co[0] - rich)
    return dict(delta_c=co[0], barra=bar, intervalo=[co[0] - bar, co[0] + bar], contiene=bool(abs(co[0] - REF) <= bar),
                dif_ref=co[0] - REF)
out["B_rho"] = dict(filas=filas, extrap_E2_recalculada=extrap(filas, "sigma_E2"), extrap_con_pared=extrap(filas, "sigma_corregida"),
                    extrap_E2_json=cru["transferencia_metodo_B"]["rho"]["extrapolacion"]["intervalo"])
# (2) delta = 1.19
T = json.load(open("resultados/r01_recalculo.json"))["constantes"]
d = {o: [p["delta"] for p in cru["fuentes"]["disparo"][o]["pares"]] for o in ("y",)}
dB = [p["delta"] for p in cru["transferencia_metodo_B"]["y"]["pares"]]
sB = [p["sigma"] for p in cru["transferencia_metodo_B"]["y"]["pares"]]
dA = [p["delta"] for p in cru["fuentes"]["transferencia"]["y"]["pares"]]
sA = [p["sigma"] for p in cru["fuentes"]["transferencia"]["y"]["pares"]]
out["delta119"] = dict(
    cruce_50_disparo=d["y"][0],
    cota_superior_solo=("delta* > delta_c para r_e > 0: delta* > 1.19 no implica delta_c > 1.19"),
    richardson_50_100_200_disparo=(4 * d["y"][1] - d["y"][0]) / 3,
    richardson_50_100_200_B=(4 * dB[1] - dB[0]) / 3, sigma_richardson_B=(4 * sB[1] + sB[0]) / 3,
    richardson_50_100_200_A=(4 * dA[1] - dA[0]) / 3, sigma_richardson_A=(4 * sA[1] + sA[0]) / 3,
    corregido_teoria_par50_disparo=d["y"][0] - T["alpha_y"] / 50**2 - T["beta_y"] / 50**3,
    corregido_teoria_par50_B=dB[0] - (T["alpha_y"] - np.pi**2 * r01["pared"]["c_w"] / (8 * T["c"])) / 50**2)
# (3) tras restar la pared (metodo B)
pr = [p["delta_pared_restada"] - e for p, e in zip(cru["transferencia_metodo_B"]["y"]["pares"],
                                                   [f["delta"] for f in r01["cruces"]["y"]])]
out["B_y_pared_restada_menos_exacto"] = pr
json.dump(out, open("resultados/r05_impacto.json", "w"), indent=1, default=float)
for k, v in out.items():
    print(k, json.dumps(v, indent=1, default=float))
