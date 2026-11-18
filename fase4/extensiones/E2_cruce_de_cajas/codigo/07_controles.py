"""07_controles.py -- tabla de controles de E2 (criterios fijados antes en criterios_previos.md), generada desde los JSON.
Escribe resultados/07_controles.json y el archivo controles.md de la carpeta. Determinista, < 1 min.
"""
import json, os, sys
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.optimize import brentq
import e2comun as c

sys.stdout = c.Tee("07_controles")
T = c.cargar("01_teoria"); D = c.cargar("02_disparo"); RA = c.cargar("03_radial"); X = c.cargar("05_cruces")
A6 = c.cargar("06_artefacto")
Rt = X["R_transferencia"]
TR = {R: c.cargar(f"04_transferencia_R{R}")["celdas"] for R in Rt}
filas = []


def fila(k, nombre, criterio, valor, pasa, script, nota=""):
    filas.append(dict(id=k, control=nombre, criterio=criterio, valor=valor, pasa=bool(pasa), script=script, nota=nota))
    print(f"{k}: {'PASA' if pasa else 'NO PASA'} | {valor}")


celdas = [(d, R) for R in Rt for d in c.DELTAS]
# K1
pm = min(TR[R][f"{d:g}"]["perron_min"] for d, R in celdas)
res = max(TR[R][f"{d:g}"]["residuo_max"] for d, R in celdas)
fila("K1", "Perron-Frobenius (autovector de signo constante)", "min(v)/max|v| >= -1e-12 en todas las celdas",
     f"mínimo {pm:+.1e} en {len(celdas)} celdas x 6 (h, eps); residuo máximo {res:.1e}", pm >= -1e-12, "04")
# K2
p = np.array([TR[R][f"{d:g}"]["orden_trotter"] for d, R in celdas])
ok = np.mean((p >= 1.8) & (p <= 2.2))
malos = [(d, R, round(TR[R][f"{d:g}"]["orden_trotter"], 3)) for d, R in celdas
         if not 1.8 <= TR[R][f"{d:g}"]["orden_trotter"] <= 2.2]
fila("K2", "Orden de Trotter", "1.8 <= p <= 2.2 en >= 90 % de las celdas",
     f"{100 * ok:.1f} % (p entre {p.min():.3f} y {p.max():.3f}); fuera: {malos[:6]}{' ...' if len(malos) > 6 else ''}",
     ok >= 0.9, "04")
# K3
comp = [TR[R][f"{d:g}"]["compatible"] for d, R in celdas]
fila("K3", "Transferencia frente a radial h = 1/40 en cada celda", "|E_tr - E_rad| <= 2 (err_tr + err_rad)",
     f"{sum(comp)}/{len(comp)} compatibles", all(comp), "04")
# K4
r4 = []
for d, R in celdas:
    t = TR[R][f"{d:g}"]; e = D["celdas"][f"{d:g}"][f"R{R}"]["E0"]
    r4.append((abs(t["E_mejor"] - e) / t["err"], abs(t["E_mejor"] - e) / abs(e)))
r4 = np.array(r4)
fila("K4", "Transferencia frente a disparo sin malla en cada celda", "|E_tr - E_disp| <= 2 err_tr",
     f"{int(np.sum(r4[:, 0] <= 2))}/{len(r4)}; máximo |dif|/err = {r4[:, 0].max():.3f}; máximo |dif|/|E| = {r4[:, 1].max():.1e}",
     np.all(r4[:, 0] <= 2), "02, 04")
# K5
for nm in ("h40", "h160"):
    q = []
    for d in c.DELTAS:
        for R in c.RS:
            x = RA["celdas"][nm][f"{d:g}"][f"R{R}"]; e = D["celdas"][f"{d:g}"][f"R{R}"]["E0"]
            q.append(abs(x["E0"] - e) / x["err"])
    q = np.array(q)
    fila(f"K5{'a' if nm == 'h40' else 'b'}", f"Radial {'1/40' if nm == 'h40' else '1/160'} frente a disparo",
         "|E_rad - E_disp| <= 2 err_rad en cada celda", f"{int(np.sum(q <= 2))}/{len(q)}; máximo |dif|/err = {q.max():.3f}",
         np.all(q <= 2), "02, 03")
# K6
re_ = T["constantes"]["r_e"]
for fu in ("disparo", "radial_h160", "transferencia"):
    pr = X["fuentes"][fu]["y"]["pares"]
    ys = [f["valor"] for f in pr]
    dec = all(ys[i + 1] < ys[i] for i in range(len(ys) - 1))
    rat = [(f["valor"] - 0.25) / (3 * re_ / (8 * f["R"])) for f in pr]
    r200 = [r for f, r in zip(pr, rat) if f["R"] >= 200]
    # el criterio del cociente se fijo solo para disparo y radial (criterios_previos.md); en la transferencia es informativo
    ok6 = abs(ys[-1] - 0.25) < 0.01 and dec and (fu == "transferencia" or all(0.8 <= r <= 1.2 for r in r200))
    fila(f"K6-{fu}", f"Valor en el cruce tiende a 1/4 ({fu})",
         "|y* - 1/4| < 0.01 en el par mayor; y* decrece con R; (y* - 1/4)/(3 r_e/8R) en [0.8, 1.2] para R >= 200"
         + (" (el criterio de cociente se fijó para disparo y radial; en la transferencia es informativo)" if fu == "transferencia" else ""),
         f"y* = {', '.join('%.5f' % v for v in ys)}; cocientes = {', '.join('%.3f' % r for r in rat)}",
         ok6, "05")
# K7 (rejilla final)
for fu in ("disparo", "radial_h160", "radial_h40", "transferencia"):
    peor = []
    for obs in ("y", "rho"):
        for f in X["fuentes"][fu][obs]["pares"]:
            lim = 1e-8 if fu == "disparo" else 0.2 * f["sigma"]
            peor.append((f["dif_interp"] / lim, obs, f["R"], f["dif_interp"]))
    w = max(peor)
    fila(f"K7-{fu}", f"Independencia de la interpolación ({fu}), rejilla final de {len(c.DELTAS)} nodos",
         "máx |spline - pchip|, |spline - local3| <= " + ("1e-8" if fu == "disparo" else "0.2 sigma del cruce"),
         f"peor caso: {w[1]} par {w[2]}: {w[3]:.1e} ({w[0]:.2f} veces el límite)", w[0] <= 1, "05")
# K7 con la rejilla inicial (disparo), recalculado aqui
DI = np.array(c.DELTAS_INICIAL)


def raiz(xs, Dv, met):
    s = np.sign(Dv); i = np.nonzero(s[1:] != s[:-1])[0][0]
    if met == "spline": f = CubicSpline(xs, Dv)
    elif met == "pchip": f = PchipInterpolator(xs, Dv)
    else:
        j0 = int(np.clip(i - 1, 0, len(xs) - 4)); pp = np.polyfit(xs[j0:j0 + 4] - xs[i], Dv[j0:j0 + 4], 3)
        f = lambda x: np.polyval(pp, x - xs[i])
    return brentq(lambda x: float(f(x)), xs[i], xs[i + 1], xtol=1e-14)


ini = []
for obs, key in (("y", "y"), ("rho", "r_sobre_R")):
    Y = np.array([[D["celdas"][f"{d:g}"][f"R{R}"][key] for R in c.RS] for d in DI])
    for j in range(len(c.RS) - 1):
        Dv = Y[:, j] - Y[:, j + 1]
        r = {m: raiz(DI, Dv, m) for m in ("spline", "pchip", "local3")}
        ini.append((max(abs(r["pchip"] - r["spline"]), abs(r["local3"] - r["spline"])), obs, c.RS[j]))
malos_ini = [(o, R, float("%.2g" % v)) for v, o, R in ini if v > 1e-8]
fila("K7-disparo-inicial", "Independencia de la interpolación (disparo), rejilla INICIAL de 15 nodos",
     "<= 1e-8", f"pares que no cumplen: {malos_ini}", len(malos_ini) == 0, "07",
     "motivó añadir 8 nodos (criterios_previos.md, 21:20)")
# K8
A = X["fuentes"]["transferencia"]["y"]["extrapolacion"]
s02 = X["sensibilidad_h_transferencia"]["h0.02"]["delta_c"]
fila("K8a", "Sensibilidad a h (transferencia)", "|delta_c(h = 0.02 sola) - delta_c(receta)| <= barra final (método A)",
     f"{abs(s02 - A['ajuste_ab']['delta_c']):.2e} frente a barra {A['barra_total']:.2e} "
     f"(h = 0.04 sola: {abs(X['sensibilidad_h_transferencia']['h0.04']['delta_c'] - A['ajuste_ab']['delta_c']):.2e})",
     abs(s02 - A["ajuste_ab"]["delta_c"]) <= A["barra_total"], "05")
for obs in ("y", "rho"):
    a40 = X["fuentes"]["radial_h40"][obs]["extrapolacion"]; a160 = X["fuentes"]["radial_h160"][obs]["extrapolacion"]
    dd = abs(a40["ajuste_ab"]["delta_c"] - a160["ajuste_ab"]["delta_c"])
    fila(f"K8b-{obs}", f"Sensibilidad a h (radial, {obs})", "|delta_c(1/40) - delta_c(1/160)| <= barra final del radial 1/160",
         f"{dd:.2e} frente a {a160['barra_total']:.2e}", dd <= a160["barra_total"], "05")
# K9
for fu, etiqueta in (("disparo", "disparo"), ("radial_h160", "radial 1/160"), ("transferencia", "transferencia, método A")):
    for obs in ("y", "rho"):
        e = X["fuentes"][fu][obs]["extrapolacion"]
        fila(f"K9-{fu}-{obs}", f"Intervalo final contiene la referencia ({etiqueta}, {obs})", "1.1906124210606 dentro",
             f"[{e['intervalo'][0]:.10f}, {e['intervalo'][1]:.10f}]; centro - ref = {e['dif_referencia']:+.1e}",
             e["contiene_referencia"], "05")
for obs in ("y", "rho"):
    e = X["transferencia_metodo_B"][obs]["extrapolacion"]
    fila(f"K9-B-{obs}", f"Intervalo final contiene la referencia (transferencia, método B, {obs})", "1.1906124210606 dentro",
         f"[{e['intervalo'][0]:.10f}, {e['intervalo'][1]:.10f}]; centro - ref = {e['dif_referencia']:+.1e}",
         e["contiene_referencia"], "05")
# K10
for obs in ("y", "rho"):
    pr = X["fuentes"]["disparo"][obs]["pares"]
    rr = X["fuentes"]["disparo"][obs]["extrapolacion"]["razones_dif_sucesivas"]
    rr100 = [r for f, r in zip(pr, rr) if f["R"] >= 100]
    fila(f"K10-{obs}", f"Ley 1/R^2 del cruce (disparo, {obs})", "cociente de diferencias sucesivas en [3, 5.5] para R >= 100",
         ", ".join("%.3f" % r for r in rr), all(3 <= r <= 5.5 for r in rr100), "05")
# K11
mx = {}
for R in c.RS:
    mx[R] = max(abs(D["celdas"][f"{d:g}"][f"R{R}"]["y"] - D["celdas"][f"{d:g}"][f"R{R}"]["y_alcance_cero"]) for d in c.DELTAS)
rat = [mx[c.RS[i]] / mx[c.RS[i + 1]] for i in range(len(c.RS) - 1)]
ok11 = all(mx[R] < 0.01 for R in c.RS if R >= 400) and all(1.6 <= r <= 2.5 for r, R in zip(rat, c.RS) if R >= 400)
fila("K11", "Colapso de datos y = F(R/a_s) (disparo, rejilla principal)",
     "max|y - F| < 0.01 para R >= 400 y cociente entre R y 2R en [1.6, 2.5] (ley 1/R)",
     "max|y - F| = " + ", ".join(f"{R}: {mx[R]:.1e}" for R in c.RS) + "; cocientes " + ", ".join("%.2f" % r for r in rat),
     ok11, "02")
# K11b (informativo, anadido despues de ver K11; revision R2-07: en la tabla se muestra "informativo", no "si"): el mismo colapso a z = R/a FIJO, |z| <= 2
mz = {}
for R in c.RS:
    v = [abs(D["celdas"][dk][f"R{R}"]["y"] - D["celdas"][dk][f"R{R}"]["y_alcance_cero"]) for dk in D["celdas"]
         if abs(R / D["energia_cero"][dk]["a"]) <= 2 and D["celdas"][dk][f"R{R}"]["nodos"] == 0]
    mz[R] = (max(v), len(v)) if v else (float("nan"), 0)
fila("K11b", "Colapso a z fijo (|z| <= 2), informativo", "sin criterio previo (añadido después de K11)",
     "max|y - F| = " + ", ".join(f"{R}: {mz[R][0]:.1e} (n = {mz[R][1]})" for R in c.RS) + "; R max|y - F| = "
     + ", ".join(f"{R * mz[R][0]:.2f}" for R in c.RS), True, "02", "informativo; no cuenta en el total")
# K12, K13
fila("K12", "Controles negativos: sin cruce si nunca liga o si liga profundo",
     "ningún cambio de signo de y(R) - y(2R)",
     f"repulsivo {A6['repulsivo']['cambios_de_signo_por_par']}, no ligado {A6['no_ligado']['cambios_de_signo_por_par']}, "
     f"ligado profundo {A6['ligado_profundo']['cambios_de_signo_por_par']}", A6["K12_pasa"], "06")
fila("K13", "Artefacto frente a estado débil (delta = 1.19)",
     "E0 > 0 en R <= 1600 (los tres métodos) y todos los delta* > 1.19",
     f"signo dice no ligado hasta 1600: {A6['delta_119']['signo_dice_no_ligado_hasta_1600']}; primer E0 < 0 (disparo) en "
     f"R = {A6['delta_119']['R_primer_E_negativo_disparo']}; menor delta* = "
     f"{min(min(v) for v in A6['delta_119']['cruces'].values()):.7f}", A6["K13_pasa"], "06")
# K14 (adicional): reproducibilidad con la Fase 3
f3 = json.load(open(os.path.join(c.comun3.RES3, "20_cajas.json")))
pares14 = [(d, R) for d in ("1.19",) for R in (50, 100, 200, 400, 800, 1600) if R in TR]
dif14 = max(abs(TR[R][d]["E_mejor"] - f3["celdas"][d][f"R{R}"]["E_mejor"]) for d, R in pares14)
fila("K14", "Reproducción de la Fase 3 (adicional, criterio fijado al escribirlo)",
     "E_tr de delta = 1.19 igual al de fase3/resultados/20_cajas.json a 1e-15", f"máxima diferencia {dif14:.1e} en "
     f"{len(pares14)} celdas", dif14 <= 1e-15, "04")

# causas medidas de los controles que no pasan (de los JSON 10, 12 y 12b)
V = c.cargar("10_verificacion"); D12 = c.cargar("12_diagnostico_trotter"); D12b = c.cargar("12b_trotter_eps0025")
n50 = sum(1 for f in D12["filas"] if f["R"] == 50); n50ok = sum(1 for f in D12["filas"] if f["R"] == 50 and 1.8 <= f["p_sin_pared"] <= 2.2)
f3200 = [f for f in D12b["filas"] if f["R"] == 3200][0]
a11 = D["energia_cero"]["1.185"]["a"]; re11 = D["energia_cero"]["1.185"]["r_e"]; z11 = 3200 / a11
dy11 = D["celdas"]["1.185"]["R3200"]["y"] - D["celdas"]["1.185"]["R3200"]["y_alcance_cero"]
causa = {
    "K2": (f"Causa medida (scripts 12 y 12b): en R = 50 la pared sin imagen; al restar el corrimiento de la pared medido con el "
           f"radial, {n50ok} de {n50} celdas vuelven a [1.8, 2.2]. En R = 3200 no es la pared: con eps = 0.2 hay términos de orden "
           f"superior; con la terna (0.1, 0.05, 0.025) el orden en delta = 1.1906 baja de {f3200['p_02_01_005']:.3f} a "
           f"{f3200['p_01_005_0025']:.3f}. La receta solo usa eps = 0.2 en la barra."),
    "K7-disparo": (f"Causa medida (script 10, V1): el spline coincide con el cruce calculado sin interpolar a "
                   f"{max(abs(v['dif_interp']) for v in V['V1_cruces_sin_interpolar']):.0e} o mejor en todos los pares; "
                   "los que se separan son PCHIP y el cúbico local en el par 50/100 de rho, cuyo cruce (1.1945) cae donde los nodos "
                   "están a 1e-3. El par 50/100 no entra en la extrapolación."),
    "K7-disparo-inicial": "Se añadieron 8 nodos; ver K7-disparo.",
    "K11": ("Causa medida: el criterio se evaluó en la rejilla de delta, donde z = R/a crece con R. La corrección es O(r_e/R) a z "
            "fijo (figura D y K11b), pero en el lado ligado vale -z^3 r_e/(pi^2 R) (de q coth q = z + r_e q^2/(2R)); en "
            f"delta = 1.185 y R = 3200, z = {z11:.2f}, la estimación da {-z11**3 * re11 / (np.pi**2 * 3200):.4f} y lo medido es "
            f"{dy11:.4f}. El criterio estaba mal planteado; no se cambia."),
}
for f in filas:
    if f["id"] in causa:
        f["nota"] = causa[f["id"]]
filas_cuentan = [f for f in filas if f["id"] != "K11b"]
npasa = sum(f["pasa"] for f in filas_cuentan)
c.guardar("07_controles", dict(script="07_controles.py", fecha=c.ahora(), filas=filas, n=len(filas_cuentan), n_pasa=npasa,
                               no_pasan=[f["id"] for f in filas_cuentan if not f["pasa"]]))
L = ["# Controles de E2 (criterio de cruce de cajas)", "",
     f"*Generado por `codigo/07_controles.py` el {c.ahora()} desde los JSON de `resultados/`. Los criterios se fijaron antes de "
     "correr la rejilla (`criterios_previos.md`). Pasan " + f"{npasa} de {len(filas_cuentan)} (K11b es informativo y no cuenta).*", "",
     "| # | Control | Criterio fijado antes | Valor | ¿Pasa? | Script |", "|---|---|---|---|---|---|"]
for f in filas:
    esc = lambda t: t.replace("|", "\\|")
    v = esc(f["valor"]) + (f" ({esc(f['nota'])})" if f["nota"] else "")
    L.append(f"| {f['id']} | {esc(f['control'])} | {esc(f['criterio'])} | {v} | {('informativo (sin criterio)' if f['id'] == 'K11b' else 'sí') if f['pasa'] else '**no pasa**'} | {f['script']} |")
open(os.path.join(c.BASE, "controles.md"), "w").write("\n".join(L) + "\n")
print(f"pasan {npasa}/{len(filas_cuentan)}")
