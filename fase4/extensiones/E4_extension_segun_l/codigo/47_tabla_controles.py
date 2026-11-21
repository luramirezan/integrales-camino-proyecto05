"""47_tabla_controles.py -- E4: genera controles.md desde los JSON (ninguna cifra escrita a mano).
Los criterios son los fijados en el docstring de cada script ANTES de correrlo (17-11-2026). Las filas sin criterio
previo se marcan "medido"."""
import os

import comun4 as c

J = {n: c.leer_json(n) for n in ("40_controles_radial_l", "40b_umbral_fd", "41_constantes_umbral", "42_barridos",
                                 "43_cajas_l", "44_tablas_l1", "45_transferencia_l1")}
filas = []


def f(control, criterio, valor, pasa, script):
    p = "medido" if pasa is None else ("sí" if pasa else "**no pasa**")
    filas.append((control, criterio, valor, p, script))


# ---------------------------------------------------------------- 40
for k, v in J["40_controles_radial_l"]["A_fd_coulomb"].items():
    f(f"FD con V_ef, Coulomb {k}: E frente a −1/(2n²) y orden de malla", "|ΔE| < 1e-8 y orden 1.8–2.2",
      f"ΔE = {v['dif_E']:+.1e}; orden {v['orden_aparente'][-1]:.3f}", v["pasa"], "40")
for k, v in J["40_controles_radial_l"]["B_disparo_coulomb"].items():
    f(f"Disparo (Frobenius + Whittaker), Coulomb {k}", "|ΔE| < 1e-12, |Δ⟨r⟩| < 1e-9, nodos",
      f"ΔE = {v['dif_E']:+.1e}; Δ⟨r⟩ = {v['dif_r']:+.1e}; nodos {v['nodos']}", v["pasa"], "40")
for k, v in J["40_controles_radial_l"]["C_umbrales"].items():
    f(f"δ_c({k}) = {v['delta_c']:.13f}: frente al encargo, convergencia numérica y ajuste FD de E(δ)",
      "encargo < 1e-8; numérica < 1e-11; ajuste FD < 1e-6",
      f"{v['dif_encargo']:+.1e}; {v['conv_num_max']:.1e}; ajuste FD {v['fd']['dif']:+.1e}", v["pasa"], "40")
for v in J["40_controles_radial_l"]["D_fd_vs_disparo"]:
    f(f"FD (h = 1/40) frente a disparo, {v['estado']} δ = {v['delta']:.6g}, R = {v['R']:.0f}",
      "E rel < 1e-6; ⟨r⟩ rel < 1e-5", f"E rel {v['dif_rel_E']:+.1e}" + (f"; ⟨r⟩ rel {v['dif_rel_r']:+.1e}" if "dif_rel_r" in v else ""),
      v["pasa"], "40")
for k, v in J["40b_umbral_fd"]["estados"].items():
    f(f"δ_c({k}) por la recurrencia de energía cero de las FD (Richardson doble)", "|dif| < 1e-9, orden 1.8–2.2",
      f"dif {v['dif']:+.1e}; orden {v['orden'][-1]:.3f}", v["pasa"], "40b")
for v in J["40b_umbral_fd"]["diagnostico_D40"]:
    f(f"Diagnóstico: FD h = 1/160 en {v['estado']} δ = {v['delta']:.6g} (fallo de la fila D)",
      "rel < 1e-4 y cociente de errores > 50", f"rel {v['rel_h160']:+.1e}; cociente {v['cociente']:.0f}", v["pasa"], "40b")
# ---------------------------------------------------------------- 41
u = J["41_constantes_umbral"]["universales"]
for k in ("I_N", "I_2", "M_1", "K_1"):
    f(f"Integral universal {k} (mpmath) frente a su forma cerrada", "sin criterio previo",
      f"{u[k]:.15f} frente a {u[k + '_exacto']:.15f}", None, "41")
# ---------------------------------------------------------------- 42
CR = J["42_barridos"]["criterios"]
for nom, e in J["42_barridos"]["estados"].items():
    for q, a in e["ajustes"].items():
        if a["p_pred"] is None:
            f(f"{nom}: exponente de potencia de ⟨r⟩ (ventana {e['ventana_Delta_rel'][0]:.0e}–{e['ventana_Delta_rel'][1]:.0e})",
              "no es potencia (ver fila del logaritmo)", f"p = {a['p']:+.4f} ± {a['err']:.1e}", None, "42")
        else:
            f(f"{nom}: exponente de {q} (ventana {e['ventana_Delta_rel'][0]:.0e}–{e['ventana_Delta_rel'][1]:.0e})",
              f"|p − {a['p_pred']:g}| < {CR['p']}", f"p = {a['p']:+.5f} ± {a['err']:.1e}", a["pasa"], "42")
    for q, v in e["coeficientes"].items():
        f(f"{nom}: coeficiente {q} en el último punto", "rel < 1e-3" if v["pasa"] is not None else "sin criterio previo",
          f"{v['med']:.8g} frente a {v['pred']:.8g} (rel {v['rel']:+.1e})", v["pasa"], "42")
    if "log" in e:
        lg = e["log"]
        f(f"{nom}: crecimiento logarítmico de ⟨r⟩", "exponente local monótono; pendiente ±1 % de A²; fórmula refinada < 1e-3",
          f"monótono {lg['exponente_local_monotono']}; pendiente {lg['pendiente']:.5f} (A² {lg['An2']:.5f}, rel "
          f"{lg['rel_pendiente']:+.1e}); fórmula {lg['max_rel_refinada_ventana']:.1e}", lg["pasa"], "42")
    for h in e["hellmann_feynman"]:
        f(f"{nom}: Hellmann–Feynman, Δ/δ_c = {h['Delta_rel']:.0e}", "rel < 1e-6", f"rel {h['rel']:+.1e}",
          bool(abs(h["rel"]) < CR["HF"]), "42")
    for z in e["fd"]:
        f(f"{nom}: FD (h = 1/40, R = {z['R']:.0f}) frente a disparo, Δ/δ_c = {z['Delta_rel']:.0e}", "E rel < 1e-5; ⟨r⟩ rel < 1e-4",
          f"E rel {z['rel_E']:+.1e}" + (f"; ⟨r⟩ rel {z['rel_r']:+.1e}" if "rel_r" in z else ""), z["pasa"], "42")
# ---------------------------------------------------------------- 43
C3 = J["43_cajas_l"]
for nom, v in C3["a_umbral"].items():
    last = v["filas"][-1]
    if nom == "1s":
        f("1s en δ_c: y = 2R²E/π² tiende a 1/4", "|y(R_max) − 1/4| < 0.01", f"y(2560) = {last['y']:.5f}", v["pasa"], "43")
    else:
        f(f"{nom} en δ_c: Y = 2R^(2l+1)E/((2l+1)A²) tiende a 1, |Y − 1| decrece", "|Y(R_max) − 1| < 0.01",
          f"Y(2560) = {last['Y']:.6f}; y(2560) = {last['y']:.2e}", v["pasa"], "43")
for z in C3["a_fd"]:
    if z["pasa"] is not None:
        f(f"FD (h = 1/160) frente a disparo en la caja, {z['estado']} R = {z['R']}", "|ΔE| < 1e-9",
          f"{z['dif160']:+.1e}", z["pasa"], "43")
for nom, v in C3["b_radio_cruce"].items():
    fl = v["filas"]
    if nom == "1s":
        val = "máx. rel frente a a_s " + f"{max(abs(x['rel_a_s']) for x in fl if 'rel_a_s' in x):.1e}"
        cr = "R_c frente a a_s < 1e-3"
    else:
        val = "máx. rel (Δ/δ_c ≤ 1e-4) " + f"{max(abs(x['rel']) for x in fl if x['Delta_rel'] <= 1.0001e-4):.1e}"
        cr = "R_c frente a ((2l+1)A²/(2SΔ))^(1/(2l+1)) < 1 %"
    f(f"{nom}: radio de cruce R_c(Δ)", cr, val, v["pasa"], "43")
for nom, v in C3["c_cruces"].items():
    z = v["filas"][-1]
    f(f"{nom}: cruce de y entre R = {z['R']} y {2 * z['R']}", "δ* y y* ±10 % de la predicción",
      f"rel δ*: {z['rel_dif']:+.2f}; rel y*: {z['rel_y']:+.2f}", v["pasa"], "43")
# ---------------------------------------------------------------- 44
T = J["44_tablas_l1"]
f("ln K_l con l = 0 igual a pares.logKD", "< 1e-12", f"{max(T['T1'].values()):.1e}", T["T1_pasa"], "44")
for e, v in T["eps"].items():
    f(f"ε = {e}: núcleo libre de la red l = 1 frente a K_1 exacto", "cociente 3.5–4.5 y Richardson < 1e-5",
      f"cociente {v['T2_cociente']:.2f}; Richardson {v['T2_max_rich']:.1e}", v["T2_pasa"], "44")
    f(f"ε = {e}: |U_R − U_0.005| de la tabla l = 1", "< 1e-4", f"{v['T3_max']:.1e}", v["T3_pasa"], "44")
    f(f"ε = {e}: continuidad tabla / extremos + WK en r = 9–9.9", "< 1e-6", f"{v['T4_max']:.1e}", v["T4_pasa"], "44")
    f(f"ε = {e}: ρ_1 de la red positivo (peso real y positivo)", "0 elementos ≤ 0", f"{v['T5_no_positivos']}", v["T5_pasa"], "44")
# ---------------------------------------------------------------- 45
TR = J["45_transferencia_l1"]
for cs in TR["casos"]:
    m = cs["metodos"]["a"]
    nm = "Coulomb 2p" if cs["delta"] == 0 else f"δ = {cs['delta']:g}"
    f(f"Camino (a), {nm}, R = {cs['R']:.0f}: frente al radial", "|dif| ≤ 2(err + err_ref)",
      f"dif {m['dif_radial']:+.1e}, err {m['err']:.1e}", m["compatible"], "45")
    f(f"Camino (a), {nm}: orden de Trotter", "1.8–2.2",
      f"{m['orden_trotter']:.3f} (con la pared corrida: {m['orden_trotter_sin_pared']:.3f})",
      bool(1.8 < m["orden_trotter"] < 2.2), "45")
f("Camino (a), Coulomb 2p: E frente a −1/8", "< 1e-7", f"{TR['resumen_a']['coulomb_dif']:+.1e}",
  bool(abs(TR["resumen_a"]["coulomb_dif"]) < 1e-7), "45")
f("Camino (a): autovector de signo constante y T ≥ 0 en todas las corridas", "Perron ≥ −1e-12; min T ≥ 0",
  f"Perron mín {TR['resumen_a']['perron_min']:+.1e}; min T {TR['resumen_a']['min_T']:.1e}",
  bool(TR["resumen_a"]["perron_min"] >= -1e-12 and TR["resumen_a"]["min_T"] >= 0), "45")
f("Camino (b) primitivo: orden de Trotter", "solo se mide", ", ".join(f"{x:.3f}" for x in TR["resumen_b"]["trotter"]), None, "45")
f("Camino (b) primitivo: error relativo máximo tras extrapolar", "solo se mide", f"{TR['resumen_b']['max_dif_rel']:.1e}", None, "45")

n = len(filas)
npas = sum(1 for x in filas if x[3] == "sí"); nno = sum(1 for x in filas if x[3] == "**no pasa**")
nmed = sum(1 for x in filas if x[3] == "medido")
L = ["# Tabla de controles de E4 (generada por `codigo/47_tabla_controles.py` desde los JSON)", "",
     f"{n} controles: {npas} pasan, {nno} no pasan, {nmed} medidos sin criterio previo. Las causas medidas de los "
     "que no pasan están en `verificacion.md`, sección 3.", "",
     "| # | control | criterio fijado antes | valor | ¿pasa? | script |", "|---|---|---|---|---|---|"]
for i, (a, b, v, p, s) in enumerate(filas, 1):
    L.append(f"| {i} | {a} | {b} | {v} | {p} | {s} |")
open(os.path.join(c.BASE, "controles.md"), "w").write("\n".join(L) + "\n")
c.guardar_json("47_tabla_controles", dict(n=n, pasan=npas, no_pasan=nno, medidos=nmed,
                                          no_pasan_lista=[x[0] for x in filas if x[3] == "**no pasa**"]))
print(n, npas, nno, nmed)
for x in filas:
    if x[3] == "**no pasa**":
        print("NO PASA:", x[0], "|", x[2])
