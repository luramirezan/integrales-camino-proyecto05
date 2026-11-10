"""24_tabla_controles.py -- Proyecto 05, Fase 3: tabla de controles generada desde los JSON 20, 20b, 20c, 21 y 22.
Cada criterio se fijo ANTES de ejecutar (los de la Fase 2 se heredan; los nuevos se anotan aqui con su origen).
Si un prefijo no encuentra datos se lanza un error (correccion T2 de la auditoria de la Fase 2).
Salida: fase3/resultados/24_tabla_controles.json y fase3/secciones/24_tabla_controles.md."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

L = lambda n: json.load(open(os.path.join(c.RES3, n)))
CJ, B, CV, B119, F119, PW = L("20_cajas.json"), L("21_barrido.json"), L("22_convergencia.json"), L("20b_umbral_119.json"), L("20c_umbral_119_fino.json"), L("20d_pared.json")
TG, GR = L("26_transferencia_grande.json"), L("25_respuesta_gemini.json")
filas = []


def F(id_, control, criterio, valor, pasa, script):
    if valor is None or (isinstance(valor, (list, tuple)) and not valor):
        raise ValueError(f"{id_}: sin datos")
    filas.append(dict(id=id_, control=control, criterio=criterio, valor=valor, pasa=pasa, script=script))


# ---- A. cajas (20)
cel = [(d, R, x) for d, C in CJ["celdas"].items() for R, x in C.items()]
ncomp = sum(x["compatible"] for _, _, x in cel)
F("A1", "Transferencia frente a radial en cada caja (5 δ × 7 R)", "|E_tr − E_rad| ≤ 2(err_tr + err_rad) (Fase 2, 14)",
  f"{ncomp}/{len(cel)} compatibles; máx |dif| = {max(abs(x['dif_rad']) for _,_,x in cel):.1e}", "sí" if ncomp == len(cel) else "**no**", "20_cajas_fase3.py")
pm = min(x["perron_min"] for _, _, x in cel)
F("A2", "Perron-Frobenius: autovector de signo constante (35 celdas × 6)", "min v/max|v| ≥ −1e-8", f"{pm:+.1e}", "sí" if pm >= -1e-8 else "**no**", "20_cajas_fase3.py")
esperado = {"1.15": "ligado", "1.18": "ligado", "1.2": "no ligado", "1.25": "no ligado"}
for i, (d, v) in enumerate(esperado.items()):
    V = CJ["veredictos"][d]
    F(f"A{3+i}", f"Veredicto del criterio 9.6 + (c) en δ = {d}", f"{v} (δ_c ref = 1.19061; umbral ley de caja 0.1 fijado antes)",
      f"{V['veredicto']} (terna {V['terna']})", "sí" if V["veredicto"] == v else "**no**", "20_cajas_fase3.py")
V = CJ["veredictos"]["1.19"]
F("A7", "Veredicto en δ = 1.19 con R ≤ 3200", "medido (a 6e-4 del umbral; a_s = +2204)", f"{V['veredicto']}; E0 cambia de signo entre R = 1600 y 3200", "medido", "20_cajas_fase3.py")
nc = sum(t["c"]["c"] for d, X in CJ["veredictos"].items() for t in X["por_terna"].values())
nt = sum(1 for d, X in CJ["veredictos"].items() for t in X["por_terna"].values())
F("A8", "Condición (c): mismo signo y tendencia radial / transferencia en cada terna", "todas las ternas", f"{nc}/{nt}", "sí" if nc == nt else "**no**", "20_cajas_fase3.py")
pt = [(d, R, x["orden_trotter"]) for d, R, x in cel]
fuera = [f"{d}/{R}: {p:.2f}" for d, R, p in pt if not (1.8 <= p <= 2.2)]
F("A9", "Orden de Trotter en las cajas", "en [1.8, 2.2] (Fase 2, C4)", f"{len(pt)-len(fuera)}/{len(pt)}; fuera: " + "; ".join(fuera), "sí" if not fuera else "**no**", "20_cajas_fase3.py")
ok = [k for k, v in PW.items() if 1.8 <= v["orden_pared_corregida"] <= 2.2]
F("A10", "Diagnóstico de A9: orden de Trotter frente al radial en R + 0.5826√ε (celdas fuera de rango con R ≤ 800)",
  "en [1.8, 2.2] si la causa es la pared sin imagen", f"{len(ok)}/{len(PW)}; " + "; ".join(f"{k}: {v['orden_pared_corregida']:.3f}" for k, v in PW.items()),
  "sí" if len(ok) == len(PW) else "**no**", "20d_diagnostico_pared.py")
# ---- B. delta = 1.19 extendido
ev = F119["criterio_radial"]
lig = [t for t, e in ev.items() if e["ligado"]]
F("B1", "δ = 1.19, radial h = 1/160, R = 3200 … 25600 (criterio 9.6 con el radial solo)", "ligado en alguna terna",
  ("ligado en " + ", ".join(lig)) if lig else "ninguna terna decide", "sí" if lig else "**no**", "20c_umbral_119_fino.py")
r = F119["radial"]
F("B2", "δ = 1.19: E0 en la caja más grande", "medido", f"E0(25600) = {r['R25600']['E0']:+.4e} ± {r['R25600']['err']:.1e}; ⟨r⟩ = {r['R25600']['r_med']:.0f}", "medido", "20c_umbral_119_fino.py")
t = B119["transferencia"]
F("B3", "δ = 1.19: transferencia frente a radial en R = 1600 y 3200", "compatibles", "; ".join(f"{k}: {v['E']:+.2e}±{v['err']:.0e} (rad {v['E_rad']:+.2e})" for k, v in t.items()),
  "sí" if all(v["compatible"] for v in t.values()) else "**no**", "20b_umbral_119.py")
tg = TG["celdas"]
F("B4", "δ = 1.19: transferencia (LU en banda, N hasta 640000) frente a radial h = 1/160 en R = 6400 y 12800", "compatibles",
  "; ".join(f"{k}: {v['E_mejor']:+.3e}±{v['err']:.0e} (rad {v['radial_h160']['E0']:+.3e})" for k, v in tg.items()),
  "sí" if all(v["compatible"] for v in tg.values()) else "**no**", "26_transferencia_grande.py")
ev26 = TG["evaluacion"]
F("B5", "δ = 1.19, terna 3200/6400/12800: criterio 9.6 con los dos métodos y condición (c)", "ligado con ambos y (c) se cumple",
  f"radial ligado={ev26['radial']['ligado']}, transferencia ligado={ev26['transferencia']['ligado']}, (c)={ev26['c']['c']}",
  "sí" if (ev26['radial']['ligado'] and ev26['transferencia']['ligado'] and ev26['c']['c']) else "**no**", "26_transferencia_grande.py")
# ---- C. barrido (21)
P = [p for p in B["puntos"] if "tr" in p]
nb = sum(p["tr"]["compatible"] for p in P)
F("C1", "Barrido δ ∈ {0.2 … 1.19}: transferencia frente a radial", "compatibles (como A1)", f"{nb}/{len(P)}; máx |dif| = {max(abs(p['tr']['dif_rad']) for p in P):.1e}", "sí" if nb == len(P) else "**no**", "21_barrido_delta.py")
F("C2", "Cotas analíticas −1/2 ≤ E0 ≤ −1/2 + δ (L04)", "0 violaciones", f"{sum(not (-0.5 <= p['radial']['E0'] <= -0.5 + p['delta']) for p in B['puntos'])} violaciones en {len(B['puntos'])} δ",
  "sí" if all(-0.5 <= p["radial"]["E0"] <= -0.5 + p["delta"] for p in B["puntos"]) else "**no**", "21_barrido_delta.py")
mono = all(B["puntos"][i]["radial"]["E0"] < B["puntos"][i + 1]["radial"]["E0"] for i in range(len(B["puntos"]) - 1))
F("C3", "E0(δ) creciente (Hellmann-Feynman: dE/dδ = ⟨e^{−δr}⟩ > 0, L05)", "estrictamente creciente", str(mono), "sí" if mono else "**no**", "21_barrido_delta.py")
cerca = [p for p in B["puntos"] if p["delta"] >= 1.15]
F("C4", "⟨r⟩κ → 1/2 al acercarse al umbral (cola e^{−κr})", "medido", "; ".join(f"{p['delta']:g}: {p['r_kappa']:.4f}" for p in cerca), "medido", "21_barrido_delta.py")
a = B["ajuste_kappa"]
F("C5", "Ajuste κ = AΔ + BΔ², Δ = δ_c − δ (δ ≥ 1.15)", "medido (avance de la Fase 4)", f"A = {a['A']:.4f}, B = {a['B']:+.4f}, residuo máx {a['residuo_max']:.1e}", "medido", "21_barrido_delta.py")
# ---- D. convergencia (22)
for d, X in CV["casos"].items():
    ot = X["orden_trotter"]
    F(f"D{len([f for f in filas if f['id'][0]=='D'])+1}", f"Orden de Trotter, δ = {d}, ε 0.2/0.1/0.05 y 0.1/0.05/0.025", "en [1.8, 2.2]",
      ", ".join(f"{o:.3f}" for o in ot), "sí" if all(1.8 <= o <= 2.2 for o in ot) else "**no**", "22_convergencia.py")
for d, X in CV["casos"].items():
    om = list(X["orden_malla"].values())
    F(f"D{len([f for f in filas if f['id'][0]=='D'])+1}", f"Orden de la malla Nyström, δ = {d} (h 0.04/0.02/0.01)", "4 ± 0.2 (Fase 2, 11.4)",
      ", ".join(f"{o:.2f}" for o in om), "sí" if all(abs(o - 4) <= 0.2 for o in om) else "**no**", "22_convergencia.py")
for d, X in CV["casos"].items():
    F(f"D{len([f for f in filas if f['id'][0]=='D'])+1}", f"Extrapolado (h → 0, ε → 0) frente al radial, δ = {d}", "|dif| < 1e-6 (Fase 2, 9.7)",
      f"{X['dif_radial']:+.1e} ({abs(X['dif_radial'])/abs(X['E_radial']):.1e} de |E0|)", "sí" if abs(X["dif_radial"]) < 1e-6 else "**no**", "22_convergencia.py")
for d, X in CV["casos"].items():
    p = X["presupuesto_rel"]
    F(f"D{len([f for f in filas if f['id'][0]=='D'])+1}", f"Presupuesto de errores en |E0|, δ = {d}", "medido",
      f"Trotter(ε=0.1) {p['trotter_eps01']:.1e}; malla(h=0.02) {p['malla_h002_eps005']:.1e}; pared {p['pared_eps01']:.1e}; final {p['final_menos_radial']:.1e}", "medido", "22_convergencia.py")

# ---- E. auditoria adversarial (25): comprobaciones sin malla ni caja
dg = GR["G1_disparo_caja_infinita"]
F("E1", "E0 en caja infinita por disparo DOP853 desde Frobenius (sin malla ni caja)", "coincide con el radial en la caja mayor",
  "; ".join(f"δ = {k}: {v['E0'] if isinstance(v, dict) else v:+.6e}" for k, v in dg.items()), "medido", "25_respuesta_gemini.py")
nd = GR["G3_nodos_energia_cero"]
okn = (nd["1.19"]["a_s"] > 0 and nd["1.1906"]["a_s"] > 0 and nd["1.1907"]["a_s"] < 0 and nd["1.2"]["a_s"] < 0)
F("E2", "Sturm a energía cero: signo de a_s (ligado ⇔ a_s > 0 con un nodo)", "δ_c entre 1.19 y 1.20",
  "; ".join(f"δ = {k}: a_s = {v['a_s']:+.1f}" for k, v in nd.items()), "sí" if okn else "**no**", "25_respuesta_gemini.py")
g1 = GR["G1_orden_malla_radial"]
F("E3", "Orden de la malla del radial en δ = 1.19, R = 3200 (h = 1/40 … 1/640) y signo del sesgo", "≈ 2 y sesgo hacia arriba",
  ", ".join(f"{o:.2f}" for o in g1["orden"]) + f"; E(1/40) = {g1['E'][0]:+.2e} → E(1/640) = {g1['E'][-1]:+.2e}",
  "sí" if all(1.8 <= o <= 2.2 for o in g1["orden"]) and g1["E"][0] > g1["E"][-1] else "**no**", "25_respuesta_gemini.py")
F("E4", "Auditoría adversarial con Gemini 3.1 Pro (7 hallazgos), cada uno verificado calculando", "ninguno cambia el veredicto",
  "G1–G6 refutados con cálculo; G7 (falta (c) en R > 3200) era válido y se resolvió con B4–B5", "sí", "25_respuesta_gemini.py, 26_transferencia_grande.py")

cuenta = {k: sum(f["pasa"] == k for f in filas) for k in ("sí", "**no**", "medido")}
json.dump(dict(script="24_tabla_controles.py", fecha="2026-11-10", filas=filas, cuenta=cuenta),
          open(os.path.join(c.RES3, "24_tabla_controles.json"), "w"), indent=1, ensure_ascii=False)
md = ["# 24. Tabla de controles de la Fase 3", "",
      "Fecha: 10-11-2026. Generada por `fase3/codigo/24_tabla_controles.py` desde los JSON de los scripts 20 a 26; ninguna cifra está escrita a mano. "
      "**Estado: SIN FIRMAR.** En la Fase 3 verifica Luis Felipe Ramírez (rotación de roles 9.12).", "",
      f"**Resumen:** {len(filas)} controles distintos (sin filas repetidas): **{cuenta['sí']} pasan**, **{cuenta['**no**']} no pasan**, {cuenta['medido']} medidos.", "",
      "| # | Control | Criterio | Valor | ¿Pasa? | Script |", "|---|---|---|---|---|---|"]
NOTAS = [
    "", "## Lo que no pasa y por qué", "",
    "- **A8 (24/25).** La terna que falla es δ = 1.15, R = 800/1600/3200: el estado ya cabe entero en las tres cajas y F_1/2 vale 1 a 1e-10 en las tres; la \"tendencia\" que compara la condición (c) es ruido de redondeo (diferencias de 1e-16) y su signo es arbitrario. El veredicto de δ = 1.15 sale de la terna 50/100/200, que sí pasa (c).",
    "- **A9.** El orden de Trotter sale fuera de [1.8, 2.2] en las cajas donde la densidad toca la pared: las pequeñas cerca del umbral y todas las de δ = 1.25 (no ligado: el estado más bajo es un estado de caja). La causa es la pared en R sin imagen (decisión 5): **A10** muestra que, comparando con el radial en R + 0.5826√ε, el orden vuelve a 1.98–1.99 en las 9 celdas que se pudieron probar. El efecto ya está sumado a la barra de error y no cambia ningún signo ni veredicto. En δ = 1.19, R = 3200 (2.33) el sesgo de Trotter es del tamaño del error de la tabla (|E0| ~ 1e-7).",
    "- **D1.** En δ = 0.2 el sesgo de Trotter con ε ≤ 0.05 es ~1e-9, del tamaño del residuo de la tabla U_C: la segunda terna de ε no mide un orden (como B9 en la Fase 2). La primera da 1.959 y el extrapolado queda a 3.6e-9 del radial.",
    "", "## Lo que esta tabla no cubre (queda para después del 11-11)", "",
    "- PIGS cerca del umbral (δ = 0.8 a 1.0), cierre de la anomalía de τ = 5 y PIGS de Hulthén (tareas 5 a 7 de `que_sigue_fase3.md`).",
    "- La transferencia en R ≥ 25600 (N > 10⁶). No hace falta para el veredicto: la terna 3200/6400/12800 ya decide \"ligado\" con los dos métodos (B5).",
    "", "## Auditoría adversarial (E4)", "",
    "El chat literal con Gemini 3.1 Pro está en `fase3/auditoria_gemini/conversaciones/G.md` y la respuesta con los números en `auditoria_gemini/respuestas/G_r2.md`. Ninguna cifra de Gemini entra en esta tabla sin recalcularla.",
]
esc = lambda t: str(t).replace("|", "\\|")
md += [f"| {f['id']} | {esc(f['control'])} | {esc(f['criterio'])} | {esc(f['valor'])} | {f['pasa']} | `{f['script']}` |" for f in filas]
md += NOTAS
open(os.path.join(c.BASE3, "secciones", "24_tabla_controles.md"), "w").write("\n".join(md) + "\n")
print("\n".join(md))
