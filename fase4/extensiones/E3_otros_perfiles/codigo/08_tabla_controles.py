"""08_tabla_controles.py -- E3: genera ../controles.md y ../resultados/08_tabla.json (tabla comparativa) desde los JSON.
Ninguna cifra se escribe a mano: todo sale de resultados/*.json."""
import os

import comun_e3 as C

NOM = {"yukawa": "Yukawa", "ecsc": "ECSC", "hulthen": "Hulthén", "hatomo": "átomo H estático"}


def f(x, n=3):
    return f"{x:.{n}e}"


def main():
    U = C.cargar("01_umbrales"); D2 = C.cargar("02_dispersion"); D3 = C.cargar("03_ligados_virtuales")
    D4 = C.cargar("04_cajas_universalidad"); D5 = C.cargar("05_transferencia_ecsc"); V = C.cargar("07_verificacion")
    filas = []

    def fila(cid, desc, crit, valor, pasa, script):
        filas.append(f"| {cid} | {desc} | {crit} | {valor} | {pasa} | `{script}` |")

    si = lambda b: "pasa" if b else "**no pasa**"
    up, sp, lp, kp, tp, vp = U["pasa"], D2["pasa"], D3["pasa"], D4["pasa"], D5["pasa"], V["pasa"]
    P1, P2, P3, P4 = U["perfiles"], D2["perfiles"], D3["perfiles"], D4["perfiles"]
    fila("U1", "δ_c por energía cero estable ante r_f y rtol", U["criterios"]["U1"],
         "máx " + f(max(max(abs(p["delta_A_rf80"] - p["delta_A"]), abs(p["delta_A_rtol11"] - p["delta_A"])) for p in P1.values()), 1),
         si(up["U1"]), "01_umbrales.py")
    dif = {k: p["dif_AB"] for k, p in P1.items()}
    fila("U2", "δ_c por energía cero (A) frente a extrapolación de κ(δ) (B, cúbico, s = 0.002..0.03)", U["criterios"]["U2"],
         "; ".join(f"{NOM[k]} {f(v, 1)}" for k, v in dif.items()), si(up["U2"]) + " (ECSC: el cúbico no sigue la curvatura de κ(δ); residuo " +
         f(P1["ecsc"]["residuo_ajuste_B"], 1) + ")", "01_umbrales.py")
    fila("U2b", "(posterior) B con s = 1e-4..2e-3", "mismo umbral 1e-8 (añadido después de ver U2)",
         "; ".join(f"{NOM[k]} {f(p['dif_AB2'], 1)}" for k, p in P1.items()),
         si(all(abs(p["dif_AB2"]) < 1e-8 for p in P1.values())), "01_umbrales.py")
    fila("U3", "Hulthén exacto y Yukawa de referencia", U["criterios"]["U3"],
         f"{f(P1['hulthen']['delta_A'] - 2, 1)}; {f(P1['yukawa']['delta_A'] - C.DELTA_C_YUK_REF, 1)}", si(up["U3"]), "01_umbrales.py")
    fila("U4", "Hulthén: κ del disparo = 1 − δ/2", U["criterios"]["U4"], f(P1["hulthen"]["dif_kappa_exacto_max"], 1), si(up["U4"]), "01_umbrales.py")
    fila("S1", "1/a y r_e: energía cero frente a desfasajes (k ≤ 0.1δ, grado 3)", D2["criterios"]["S1"],
         "máx |Δ(1/a)| " + f(max(abs(c["inv_a_1"] - c["inv_a_2"]) for p in P2.values() for c in p["comparacion"]), 1) +
         ", máx |Δr_e| " + f(max(abs(c["r_e_1"] - c["r_e_2"]) for p in P2.values() for c in p["comparacion"]), 1),
         si(sp["S1"]) + " (truncación del polinomio en k²)", "02_dispersion.py")
    fila("S1b", "(posterior) igual con k = (0.005..0.05)δ, grado 4", D2["criterios"]["S1b"],
         "máx |Δ(1/a)| " + f(max(abs(c["inv_a_1"] - c["inv_a_2b"]) for p in P2.values() for c in p["comparacion"]), 1) +
         ", máx |Δr_e| " + f(max(abs(c["r_e_1"] - c["r_e_2b"]) for p in P2.values() for c in p["comparacion"]), 1), si(sp["S1b"]), "02_dispersion.py")
    fila("S2", "Hulthén: a(δ) frente a la fórmula con digamma", D2["criterios"]["S2"], f(P2["hulthen"]["err_rel_a_exacto_max"], 1), si(sp["S2"]), "02_dispersion.py")
    fila("S3", "c = −d(1/a)/dδ: Hellmann–Feynman frente a diferencias", D2["criterios"]["S3"],
         "máx " + f(max(abs(p["c_HF"] - p["c_dif"]) / p["c_HF"] for p in P2.values()), 1), si(sp["S3"]), "02_dispersion.py")
    fila("S5", "1/a monótona y con un solo cero", D2["criterios"]["S5"], "4 perfiles", si(sp["S5"]), "02_dispersion.py")
    fila("L1", "κ = (1 − √(1 − 2r_e/a))/r_e", D3["criterios"]["L1"],
         "máx " + f(max(abs(x["kappa_ERE"] - x["kappa"]) / x["kappa"] for p in P3.values() for x in p["ligados"] if x["s"] <= 0.01), 1),
         si(lp["L1"]), "03_ligados_virtuales.py")
    fila("L2", "pendiente medida A frente a c predicha", D3["criterios"]["L2"],
         "; ".join(f"{NOM[k]} {f(p['ajuste']['dif_rel_A_c'], 1)}" for k, p in P3.items()), si(lp["L2"]), "03_ligados_virtuales.py")
    fila("L3", "κa → 1 y ⟨r⟩κ → 1/2", D3["criterios"]["L3"],
         "máx " + f(max(max(abs(p["ligados"][0]["kappa_a"] - 1), abs(p["ligados"][0]["rk"] - 0.5)) for p in P3.values()), 1),
         si(lp["L3"]), "03_ligados_virtuales.py")
    fila("L4", "pendiente de ⟨r⟩κ frente a κ = r_e/2", D3["criterios"]["L4"],
         "; ".join(f"{NOM[k]} {f(p['rk_ajuste']['dif_rel'], 1)}" for k, p in P3.items()), si(lp["L4"]), "03_ligados_virtuales.py")
    fila("L5", "polo virtual: rango efectivo frente a cálculo directo", D3["criterios"]["L5"],
         "máx " + f(max(abs(x["kappa_v_ERE"] - x["kappa_v_dir"]) / x["kappa_v_dir"] for p in P3.values() for x in p["virtuales"] if x["s"] <= 0.01), 1),
         si(lp["L5"]), "03_ligados_virtuales.py")
    fila("L6", "un solo ligado s, sin nodos", D3["criterios"]["L6"], "64 puntos", si(lp["L6"]), "03_ligados_virtuales.py")
    fila("K1", "punto fijo 1/4 y su corrección (1/4)(1 + r_e/R)", D4["criterios"]["K1"],
         "máx " + f(max(abs(x["valor"] - x["pred"]) / 0.25 for p in P4.values() for x in p["punto_fijo"] if x["R"] >= 200), 1),
         si(kp["K1"]), "04_cajas_universalidad.py")
    fila("K2", "sentido del cruce = signo de r_e", D4["criterios"]["K2"],
         "máx |δ*−pred|/|δ*−δ_c| (R₁ ≥ 200) " + f(max(abs(c["delta_star"] - c["pred"]) / abs(c["dif"]) for p in P4.values() for c in p["cruces"] if c["R1"] >= 200), 1),
         si(kp["K2"]), "04_cajas_universalidad.py")
    fila("K3", "⟨r⟩/R → 1/2 − 2/π² en δ_c", D4["criterios"]["K3"],
         "máx " + f(max(abs(p["punto_fijo"][-1]["r_sobre_R"] - D4["r_sobre_R_universal"]) for p in P4.values()), 1), si(kp["K3"]), "04_cajas_universalidad.py")
    fila("K4", "polo virtual desde las cajas", D4["criterios"]["K4"],
         "máx " + f(max(abs(x["dif_rel"]) for p in P4.values() for x in p["virtual_caja"]), 1), si(kp["K4"]), "04_cajas_universalidad.py")
    fila("K5", "radial (Fase 2) frente al disparo, R = 200", D4["criterios"]["K5"],
         "máx " + f(max(abs(p["radial_R200"]["E0"] - p["radial_R200"]["disparo"]) for p in P4.values()), 1), si(kp["K5"]), "04_cajas_universalidad.py")
    cel = D5["celdas"]
    fila("T1", "W del ECSC acotado y positivo", D5["criterios"]["T1"],
         "mín " + f(min(v["min"] for v in D5["W_ecsc"].values()), 2), si(tp["T1"]), "05_transferencia_ecsc.py")
    fila("T2", "integral de camino frente al disparo y al radial", D5["criterios"]["T2"],
         "máx |dif|/σ " + f"{max(abs(c['dif_disparo']) / c['err_tr'] for c in cel):.2f}", si(tp["T2"]), "05_transferencia_ecsc.py")
    fila("T3", "orden de Trotter", D5["criterios"]["T3"],
         f"{min(c['orden_trotter'] for c in cel):.3f} a {max(c['orden_trotter'] for c in cel):.3f}", si(tp["T3"]), "05_transferencia_ecsc.py")
    fila("T4", "Perron y residuo", D5["criterios"]["T4"],
         f"mín {min(c['perron_min'] for c in cel):.1e}, residuo máx {max(c['residuo_max'] for c in cel):.1e}", si(tp["T4"]), "05_transferencia_ecsc.py")
    hul = [c for c in cel if c["perfil"] == "hulthen"][0]
    fila("T5", "Hulthén 1.8 exacto por la integral de camino", D5["criterios"]["T5"],
         f"{f(hul['E_tr'] - hul['E_exacta'], 1)} (σ {f(hul['err_tr'], 1)})", si(tp["T5"]), "05_transferencia_ecsc.py")
    yk = [c for c in cel if c["perfil"] == "yukawa"][0]
    fila("T6", "reproduce comun3 (Fase 3)", D5["criterios"]["T6"],
         f(abs(yk["E_comun3_h004_eps01"] - yk["crudo"]["h0.04_eps0.1"]["E0"]), 1), si(tp["T6"]), "05_transferencia_ecsc.py")
    fila("V1", "tercer método (fase variable, LSODA)", V["criterios"]["V1"],
         "máx " + f(max(abs(x["dif"]) for x in V["V1"].values()), 1), si(vp["V1"]), "07_verificacion.py")
    fila("V2", "disparo frente al radial de la Fase 3 (Yukawa)", V["criterios"]["V2"],
         "máx |dif| " + f(max(abs(x["dif"]) for x in V["V2"]), 1), si(vp["V2"]), "07_verificacion.py")
    fila("V3", "Hulthén ⟨r⟩ exacto", V["criterios"]["V3"], "máx " + f(max(abs(x["dif_rel"]) for x in V["V3"]), 1), si(vp["V3"]), "07_verificacion.py")
    fila("V4", "Hulthén: polo virtual κ_v = δ/2 − 1 (observación)", V["criterios"]["V4"], f(V["V4"]["max_dif_rel"], 1), "medido", "07_verificacion.py")
    fila("V5", "Yukawa: c y B frente a la Fase 3", V["criterios"]["V5"],
         f"c = {V['V5']['c']:.6f} (A = {V['V5']['A_fase3']:.6f}); B = {V['V5']['B_pred']:.4f} ({V['V5']['B_fase3']:.4f})", si(vp["V5"]), "07_verificacion.py")
    npasa = sum(1 for x in filas if "| pasa" in x)
    nno = sum(1 for x in filas if "no pasa" in x)
    cab = ["# Controles de E3 (generado por `codigo/08_tabla_controles.py` desde `resultados/*.json`)", "",
           "Los criterios se fijaron antes de correr cada script (están en su docstring). Las filas marcadas "
           "\"(posterior)\" se añadieron después de ver un fallo y no cambian el veredicto de la fila original.", "",
           f"Resumen: {len(filas)} filas; {npasa} pasan, {nno} no pasan, el resto medido.", "",
           "| # | control | criterio fijado antes | valor | ¿pasa? | script |", "|---|---|---|---|---|---|"]
    with open(os.path.join(C.BASE, "controles.md"), "w") as fh:
        fh.write("\n".join(cab + filas) + "\n")
    # tabla comparativa
    tab = {}
    for k in C.ORDEN:
        tab[k] = dict(delta_c=P1[k]["delta_A"], c_pred=P2[k]["c_HF"], A_medida=P3[k]["ajuste"]["A"], B_pred=P2[k]["B_pred"],
                      B_medida=P3[k]["ajuste"]["B"], r_e=P2[k]["r_e_c"], P_forma=P4[k]["P"],
                      rk_pendiente=P3[k]["rk_ajuste"]["pendiente"],
                      R1600_desv=P4[k]["punto_fijo"][-1]["R_por_desv"], cruce_800_1600=P4[k]["cruces"][-1]["dif"],
                      sentido_cruce="desde arriba" if P4[k]["cruces"][-1]["dif"] > 0 else "desde abajo")
    C.guardar("08_tabla", dict(script="08_tabla_controles.py", tabla=tab, n_filas=len(filas), n_pasa=npasa, n_no_pasa=nno))
    lineas = ["| perfil | δ_c | c predicha | A medida | B predicha | B medida | r_e(δ_c) | P | sentido del cruce |",
              "|---|---|---|---|---|---|---|---|---|"]
    for k, t in tab.items():
        lineas.append(f"| {NOM[k]} | {t['delta_c']:.10f} | {t['c_pred']:.8f} | {t['A_medida']:.8f} | {t['B_pred']:+.4f} | "
                      f"{t['B_medida']:+.4f} | {t['r_e']:+.6f} | {t['P_forma']:+.4f} | {t['sentido_cruce']} |")
    with open(os.path.join(C.RES, "08_tabla_comparativa.md"), "w") as fh:
        fh.write("\n".join(lineas) + "\n")
    print("\n".join(cab + filas)); print(); print("\n".join(lineas))


if __name__ == "__main__":
    main()
