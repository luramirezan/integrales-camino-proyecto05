"""07_controles.py -- E5: tabla de controles generada desde los JSON (criterios fijados en criterios_previos.md).
Salida: controles.md y resultados/07_controles.json."""
import json
import os

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(AQUI, "../resultados")
J = {k: json.load(open(os.path.join(RES, f"{k}.json"))) for k in
     ["01_referencia_edo", "02_validacion_mc", "03_colas", "04_importancia", "05_cerca_umbral", "04b_extrapolacion",
      "08_verificacion"]}
X4 = J["04b_extrapolacion"]["delta"]
V8 = J["08_verificacion"]
R1, R2, R3, R4, R5 = (J[k] for k in ["01_referencia_edo", "02_validacion_mc", "03_colas", "04_importancia",
                                     "05_cerca_umbral"])
filas = []


def fila(n, control, criterio, valor, pasa, script, nota=""):
    filas.append(dict(n=n, control=control, criterio=criterio, valor=valor, pasa=pasa, script=script, nota=nota))


SI, NO, NA, INF = "sí", "**no pasa**", "no aplicable", "medido"
D7 = ["1.2", "1.3", "1.5", "2", "2.5", "3", "4"]

m1 = max(abs(R1["a_delta"][d]["dif_rel_M2"]) for d in D7)
fila("C1", "a(δ): disparo frente a fase variable (7 δ)", "dif. rel. < 1e-8", f"máx {m1:.1e}", SI if m1 < 1e-8 else NO, "01")
a12 = R1["a_delta"]["1.2"]["a_M1_disparo"]
fila("C2", "a(1.20) frente a −142.9 de la Fase 3", "|Δa| < 0.05", f"{a12:.4f} (|Δa| = {abs(a12 + 142.9):.3f})",
     SI if abs(a12 + 142.9) < 0.05 else NO, "01")
pm = {d: R1["perfil"][d]["dif_max_abs"] for d in D7}
mal = [d for d in D7 if pm[d] >= 1e-5]
fila("C3", "Perfil φ(r): disparo frente a Nyström", "máx |Δφ| < 1e-5 (r ≤ 8)",
     "; ".join(f"δ={d}: {pm[d]:.1e}" for d in D7), SI if not mal else NO, "01",
     ("no pasa en δ = " + ", ".join(mal) + ". Causa: el núcleo 1/max(r, r') tiene un quiebre en r' = r y los puntos de "
      "la rejilla del MC no son nodos de Nyström; el error absoluto escala con φ (≈ 250 en δ = 1.2). El error relativo "
      f"en δ = 1.2 es {V8['nystrom']['1.2'][1]['dif_max_rel']:.1e} con 600 paneles y baja a "
      f"{V8['nystrom']['1.2'][2]['dif_max_rel']:.1e} con 1200 (08_verificacion); a coincide a "
      f"{abs(V8['nystrom']['1.2'][1]['dif_rel_a']):.1e}. Es un error del método de control, no del disparo.") if mal else "")
m4 = max(abs(R1["identidad_estimador"][d]["dif_rel"]) for d in D7)
fila("C4", "Identidad a = −(2/δ²) E_Γ[φ]", "dif. rel. < 1e-8", f"máx {m4:.1e}", SI if m4 < 1e-8 else NO, "01")
m5 = max(max(abs(c["err_p"]), abs(c["err_w"])) for c in R1["ciesielski_taylor"])
fila("C5", "Mezcla de exponenciales frente a Ciesielski–Taylor (k = 1..5)", "err. rel. < 1e-6", f"máx {m5:.1e}",
     SI if m5 < 1e-6 else NO, "01")
dc = R1["delta_c_desde_polos"]
ok6 = abs(dc["err_rel_dc1"]) < 1e-7 and abs(dc["err_rel_dc2"]) < 1e-7
fila("C6", "δ/p_1 = δ_c(1s), δ/p_2 = δ_c(2s)", "err. rel. < 1e-7",
     f"{dc['dc1_medio']:.12f} ({dc['err_rel_dc1']:.1e}); {dc['dc2_medio']:.10f} ({dc['err_rel_dc2']:.1e})",
     SI if ok6 else NO, "01")
ex = R2["extrapolacion"]
v7 = [ex[d]["dev_extrap_sigmas"] for d in ["3", "4"]]
pf = [x["dev_sigmas"] for d in ["3", "4"] for x in R2["perfil"][d]]
ok7 = all(abs(v) < 3 for v in v7 + pf)
fila("C7", "MC libre δ = 3, 4: a extrapolado (η⁴) y φ(r) en 7 radios", "|MC − EDO| < 3σ",
     f"a: {v7[0]:+.2f}σ, {v7[1]:+.2f}σ; φ(r): máx |dev| {max(abs(x) for x in pf):.2f}σ", SI if ok7 else NO, "02")
fila("C8", "Orden del sesgo con el trapecio", "entre 1.5 y 2.5", "media infinita para todo η (Prop. 3); a = "
     f"{R2['trapecio']['0.8']['a_trapecio']:.1e} (η = 0.8)", NA, "02",
     "El criterio presuponía un estimador con media finita; el trapecio no lo es (adenda 1 de criterios_previos.md).")
o8 = [ex[d][k] for d in ["2.5", "3", "4"] for k in ["p_obs_08_04", "p_obs_04_02"]]
fila("C8b", "Orden del sesgo con el esquema de puente (δ = 2.5, 3, 4)", "entre 3 y 5 (fijado tras prueba preliminar)",
     ", ".join(f"{x:.2f}" for x in o8), SI if all(3 <= x <= 5 for x in o8) else NO, "02")
c9 = R3["cola"]
fila("C9", "θ̂ = δ κ̂ (cola de X, 1 % superior) frente a δ/δ_c", "|θ̂ − δ/δ_c| < 3σ_θ",
     f"κ̂ = {c9['kappa']:.5f} ± {c9['err_kappa']:.5f} frente a 1/δ_c = {c9['kappa_pred']:.5f} ({c9['dev_sigmas']:+.2f}σ, "
     "igual para todos los δ)", SI if abs(c9["dev_sigmas"]) < 3 else NO, "03",
     "Los 7 δ comparten la muestra (covarianza de escala); no son 7 controles independientes.")
p9 = R3["partida_fija"]
fila("C9b", "θ̂ con partida fija r₀ = 1, δ = 1.5 (independiente)", "|θ̂ − δ/δ_c| < 3σ",
     f"{p9['theta_MC']:.4f} ± {p9['err']:.4f} frente a {p9['theta_pred']:.4f} ({p9['dev_sigmas']:+.2f}σ)",
     SI if abs(p9["dev_sigmas"]) < 3 else NO, "03")
k10 = R3["ks"]
fila("C10", "Ley de X frente a la mezcla (KS, x ≥ x_min)", "√N·D < 1.63",
     f"√N·D = {k10['sqrtN_D']:.2f} (x_min = {k10['x_min']:.4f})", SI if k10["sqrtN_D"] < 1.63 else NO, "03",
     "Una sola muestra universal vale para δ = 3 y 4 (y para todos los δ).")
S = R3["series"]
RF = R3.get("referencia_tamano_finito", {})
for d in ["1.5", "2"]:
    s = S[d]
    ok = abs(s["pend_var"] - s["pred_pend_var"]) < 0.15
    nota = ""
    if not ok:
        rf = RF.get(d)
        nota = ("Causa medida: el estadístico es preasintótico y muy ruidoso. Con muestras de la ley exacta del mismo "
                f"tamaño da {rf['media']:+.3f} ± {rf['desv']:.3f} (10 muestras); el MC queda a z = {rf['z']:+.2f}."
                if rf else "Ver verificacion.md.")
    fila(f"C11 (δ={d})", "Pendiente log-log de la varianza muestral", "±0.15 de 2/θ − 1",
         f"{s['pend_var']:+.3f} frente a {s['pred_pend_var']:+.3f}", SI if ok else NO, "03", nota)
for d in ["3", "4"]:
    s = S[d]
    fila(f"C11 (δ={d})", "Pendiente log-log de la varianza muestral", "|pendiente| < 0.1", f"{s['pend_var']:+.3f}",
         SI if abs(s["pend_var"]) < 0.1 else NO, "03")
P4 = R4["produccion"]
pmax = max(P4[d]["eta"][e]["peso_max"] for d in P4 for e in P4[d]["eta"])
pmax5 = max(R5["cerca"][d]["peso_max"] for d in R5["cerca"])
fila("C12", "MI con supersolución: pesos ≤ 1", "máx(peso) ≤ 1", f"{max(pmax, pmax5):.6f}",
     SI if max(pmax, pmax5) <= 1 else NO, "04, 05")
for d in ["3", "1.5", "1.3", "1.25", "1.2"]:
    p = P4[d]
    fila(f"C13 (δ={d})", "a_MI (η = 0.1) frente a la EDO", "|Δ| < 3σ (σ = estadística + sesgo medido)",
         f"{p['a_eta01']:+.5f} frente a {p['a_edo']:+.5f}: {p['dev_eta01_sigma_total']:+.2f}σ "
         f"(extrapolado p = {R4['orden_extrapolacion']:.2f}: {p['dev_extrap_sigmas']:+.2f}σ; p = 2: "
         f"{X4[d]['p2']['dev_sigmas']:+.2f}σ)", SI if abs(p["dev_eta01_sigma_total"]) < 3 else NO, "04",
         ("La extrapolación con el orden de la regla de 04 (p = 3.20, promedio de pares preasintóticos) queda a 3.85σ; "
          "con p = 2 (orden de Euler; par más fino observado 1.93) queda a "
          f"{X4[d]['p2']['dev_sigmas']:+.2f}σ. La revisión a p = 2 se hizo después de ver los datos (04b).")
         if d == "3" else "")
for d, p in R5["cerca"].items():
    fila(f"C13 (δ={d}, inf.)", "a_MI (η = 0.2) cerca del umbral", "informativo (σ = estadística + sesgo de 04)",
         f"{p['a_mc']:+.2f} ± {p['sigma_total']:.2f} frente a {p['a_edo']:+.2f} ({p['dev_sigma_total']:+.2f}σ)", INF, "05")
for d in P4:
    p = P4[d]["eta"]["0.1"]
    vr, co, n = p["var_rel"], p["cota_var_rel"], p["N"]
    sv = vr * np.sqrt(2.0 / n) * 3  # cota gruesa del error de la varianza (pesos acotados): 3 sigma
    fila(f"C14 (δ={d})", "Varianza relativa medida frente a la cota", "medida ≤ cota + 3σ", f"{vr:.4f} ≤ {co:.4f}",
         SI if vr <= co + sv else NO, "04")
    pv, et = p["pendiente_var"], "0.1"
    if not np.isfinite(pv):           # N demasiado pequeno para 10 bloques de 2000: se usa la corrida con eta = 0.2
        pv, et = P4[d]["eta"]["0.2"]["pendiente_var"], "0.2"
    fila(f"C15 (δ={d})", "Varianza muestral estable con n (MI)", "|pendiente| < 0.1", f"{pv:+.3f} (η = {et})",
         SI if abs(pv) < 0.1 else NO, "04",
         "" if et == "0.1" else f"Con η = 0.1 solo hay N = {p['N']} caminos (menos de 10 bloques de 2000); se usa la "
                                 "corrida con η = 0.2.")
for e, u in R2["universal"].items():
    ok = abs(u["dev_E_X_sigmas"]) < 3
    fila(f"C16 (η={e})", "E[δΛ] = 1 (esquema de puente)", "|E − 1| < 3σ",
         f"{u['E_X']:.5f} ± {u['err_E_X']:.5f} ({u['dev_E_X_sigmas']:+.2f}σ)", SI if ok else NO, "02",
         "" if ok else "Causa: con η = 0.8 los pasos son tan largos que la cuadratura de 3 nodos en el tiempo del "
                       "puente no basta (la media del puente sí es exacta). Con η ≤ 0.4 pasa.")
u3 = R3["muestra"]
fila("C16 (03)", "E[δΛ] = 1 en la muestra de 03", "|E − 1| < 3σ",
     f"{u3['E_X']:.5f} ± {u3['err_E_X']:.5f}", SI if abs(u3["E_X"] - 1) < 3 * u3["err_E_X"] else NO, "03")

n_si = sum(f["pasa"] == SI for f in filas)
n_no = sum(f["pasa"] == NO for f in filas)
n_na = sum(f["pasa"] == NA for f in filas)
n_inf = sum(f["pasa"] == INF for f in filas)
L = ["# Tabla de controles de E5 (generada por `codigo/07_controles.py` desde los JSON)", "",
     "Los criterios se fijaron antes de correr los Monte Carlo (`criterios_previos.md`; las filas C8b, C16 y C9b y la "
     "restricción x ≥ x_min de C10 están en su adenda, escrita después de una prueba preliminar y antes de las corridas "
     "finales).", "",
     f"Resumen: {len(filas)} filas; {n_si} pasan, {n_no} no pasan (con su causa medida), {n_na} no aplicable, "
     f"{n_inf} informativas.", "",
     "| # | control | criterio fijado antes | valor | ¿pasa? | script |", "|---|---|---|---|---|---|"]
for f in filas:
    L.append(f"| {f['n']} | {f['control']} | {f['criterio']} | {f['valor']} | {f['pasa']} | {f['script']} |")
L.append("")
L.append("## Notas")
L.append("")
for f in filas:
    if f["nota"]:
        L.append(f"- **{f['n']}.** {f['nota']}")
open(os.path.join(AQUI, "../controles.md"), "w").write("\n".join(L) + "\n")
json.dump(dict(filas=filas, n_si=n_si, n_no=n_no, n_na=n_na, n_inf=n_inf), open(os.path.join(RES, "07_controles.json"), "w"),
          indent=1)
print("\n".join(L))
