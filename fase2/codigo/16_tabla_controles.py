"""16_tabla_controles.py -- Proyecto 05 (Yukawa), Fase 2: TABLA DE CONTROLES consolidada (V3, 27-10-2026).

No calcula fisica: lee los JSON de los scripts 10 a 15 y escribe
  fase2/secciones/15_tabla_controles.md   (tabla para firmar por quien verifica)
  fase2/resultados/16_tabla_controles.json (las mismas filas, legibles por maquina)
Cada cifra de la tabla sale de un JSON (se indica cual). Las figuras se "congelan" con su sha256.
"""
import hashlib
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
J = {k: json.load(open(os.path.join(RES, f))) for k, f in (
    ("10", "10_radial.json"), ("11", "11_transferencia.json"), ("12", "12_pigs.json"),
    ("12b", "12b_pigs_replica.json"), ("12c", "12c_pigs_coulomb_tau5.json"), ("13", "13_controles.json"),
    ("14", "14_cajas.json"), ("15", "15_limites.json"))}
SCR = {"10": "10_radial_controles.py / test_radial.py", "11": "11_transferencia_controles.py",
       "12": "12_pigs_produccion.py", "12b": "12b_pigs_replica_tau5.py", "12c": "12c_pigs_coulomb_tau5.py",
       "13": "13_controles_hulthen_pozo.py", "14": "14_criterio_cajas.py", "15": "15_limites.py"}
FJS = {"10": "10_radial.json", "11": "11_transferencia.json", "12": "12_pigs.json", "12b": "12b_pigs_replica.json",
       "12c": "12c_pigs_coulomb_tau5.json", "13": "13_controles.json", "14": "14_cajas.json", "15": "15_limites.json"}
filas = []


def fila(bloque, control, criterio, valor, pasa, fuente, clave=""):
    filas.append(dict(bloque=bloque, control=control, criterio=criterio, valor=valor, pasa=pasa,
                      script=SCR[fuente], json=FJS[fuente] + (f" ({clave})" if clave else "")))


def crit(fuente, pref):
    return [c for c in J[fuente]["criterios"] if c["control"].startswith(pref)]


def todos(fuente, pref):
    cs = crit(fuente, pref)
    return all(c["pasa"] for c in cs), "; ".join(c["valor"] for c in cs)


# ======================================================================= A. criterios de 9.7 aplicables a la Fase 2
j11, j12, j13, j14, j15 = J["11"], J["12"], J["13"], J["14"], J["15"]
p, v = todos("11", "Coulomb eps=")
fila("9.7", "Coulomb delta=0, transferencia (L02)", "|E+0.5|<1e-6 tras Richardson en h_tab; |<r>-1.5|<1e-4 (eps 0.2/0.1/0.05)",
     v, p, "11", "criterios")
c12 = {c["control"]: c for c in j12["criterios"]}
cc = [c12[k] for k in ("Coulomb PIGS <r> puro", "Coulomb PIGS <r^2> puro")]
fila("9.7", "Coulomb delta=0, PIGS, 1 cadena (plan)", "E_L = -0.5; <r>, <r^2> a < 2 sigma de 1.5 y 3",
     f"E_L: {c12['Coulomb PIGS E_L']['valor']} (tautologico: W=0); " + "; ".join(c["valor"] for c in cc),
     all(c["pasa"] for c in cc), "12", "criterios")
p, v = todos("12c", "(A) Coulomb")
fila("9.7", "Coulomb delta=0, PIGS, 8 cadenas + histograma (V3)", "<r>, <r^2> a < 2 sigma; histograma de r_{M/2} p > 1e-3",
     v, p, "12c", "A_coulomb")
p, v = todos("11", "delta=0.2 h=0.02")
fila("9.7", "delta=0.2 transferencia, h=0.02", "|E-E_rad|<1e-6, |<r>-<r>_rad|<1e-3", v, p, "11", "criterios")
p, v = todos("11", "delta=0.2 h=0.04")
fila("9.7", "delta=0.2 transferencia, h=0.04 (control)", "idem", v, p, "11", "criterios")
cc = [c12[k] for k in ("delta=0.2 PIGS E (mixto)", "delta=0.2 PIGS <r> (puro)", "delta=0.2 PIGS <r^2> (puro)")]
fila("9.7", "delta=0.2 PIGS (tau=20, 8 cadenas)", "E, <r>, <r^2> a < 2 sigma del radial; sigma = mayor de bloques y cadenas",
     "; ".join(c["valor"] for c in cc), all(c["pasa"] for c in cc), "12", "criterios")
for pref, nom in (("Trotter delta=0.2 orden aparente (h=0.02", "Ley eps^2, delta=0.2, h=0.02 sin Richardson en h"),
                  ("Trotter delta=0.2 orden aparente (Richardson", "Ley eps^2, delta=0.2, Richardson h^4"),
                  ("Trotter delta=0.2 |extrapolado", "Extrapolado eps->0, delta=0.2"),
                  ("Trotter delta=1.0 orden aparente (h=0.02", "Ley eps^2, delta=1.0, R=174, h=0.02"),
                  ("Trotter delta=1.0 orden aparente (Richardson", "Ley eps^2, delta=1.0, Richardson h^4"),
                  ("Trotter delta=1.0 |extrapolado", "Extrapolado eps->0, delta=1.0")):
    p, v = todos("11", pref)
    fila("9.7", nom + " (L18)", "orden en [1.8, 2.2]; extrapolado < 1e-6 del radial", v, p, "11", "trotter")
p, v = todos("11", "Nystrom")
fila("9.7", "Tabulacion: estabilidad Nystrom 0.02 -> 0.04 (9 casos)", "|E(0.04)-E(0.02)| < 1e-6", v, p, "11",
     "estabilidad_nystrom")
o = j11["orden_nystrom"]
fila("9.7", "Tabulacion: orden de la malla Nystrom (propuesta: Richardson h^4)", "medido",
     ", ".join(f"{k}: {x['orden']:.2f}" for k, x in o.items()), None, "11", "orden_nystrom")
p, v = todos("11", "Proyeccion")
fila("9.7", "Proyeccion (L15), transferencia delta=0.2, eps=0.1", "variacion < 1e-6 de tau=20 a 30; limite del mixto - E0(T) < 1e-6",
     v + f"; con Richardson en h: {j11['proyeccion']['V3_malla']['limite_menos_E0T_rich_h4']:+.1e}", p, "11", "proyeccion")
c = c12["E_mixto(tau) y <r>,<r^2> puros (tau = 2, 5, 10, 20)"]
fila("9.7", "Proyeccion con PIGS frente a la transferencia (tau = 2, 5, 10, 20)", c["criterio"], c["valor"], c["pasa"], "12",
     "criterios")
c5 = J["12c"]["C_tau5_combinado"]
fila("9.7", "Anomalia tau=5: replica 1 (16 cadenas)", "< 2 sigma de la transferencia",
     f"E {J['12b']['replica']['las_16']['sigma_E']:+.2f} sigma; <r> {J['12b']['replica']['las_16']['sigma_r']:+.2f} sigma",
     abs(J["12b"]["replica"]["las_16"]["sigma_E"]) < 2 and abs(J["12b"]["replica"]["las_16"]["sigma_r"]) < 2, "12b", "replica")
p, v = todos("12c", "(B)")
fila("9.7", "Anomalia tau=5: replica 2 (16 cadenas, V3)", "< 2 sigma de la transferencia", v, p, "12c", "B_replica2_tau5")
L40 = c5["las_40"]
fila("9.7", "Anomalia tau=5: las 40 cadenas (informativo, V3)", "se reporta",
     f"ponderada {L40['sigma_ponderada']:+.2f} sigma, pesos iguales {L40['sigma_pesos_iguales']:+.2f} sigma; chi2 de las 3 corridas "
     f"{c5['chi2_corridas_vs_Edet']['chi2']:.2f}/3 (p={c5['chi2_corridas_vs_Edet']['p']:.3f}); chi2 por cadena "
     f"{L40['chi2_por_cadena']:.1f}/{L40['dof']} (p={L40['p_por_cadena']:.3f})", None, "12c", "C_tau5_combinado")
mx = max(max(c["malla_rel"].values()) for d in j14["celdas"].values() for c in d.values())
rad_max = max(c["dE_rel"] for d in J["10"]["cajas_9_6"].values() if isinstance(d, dict) for c in d.values() if isinstance(c, dict) and "dE_rel" in c)
fila("9.7", "Malla espacial h en cada caja (a')", "|E0(h)-E0(h/2)| < 0.1|E0|",
     f"transferencia (0.02 vs 0.04): max {mx:.1e}; radial (1/40 vs 1/80): max {rad_max:.3f}", mx < 0.1 and rad_max < 0.1, "14",
     "celdas/*/malla_rel; 10_radial.json cajas_9_6")
dec = []
for d, cel in j14["celdas"].items():
    Es = [cel[f"R{R}"]["E_mejor"] for R in (50, 100, 200, 400, 800)]
    dec.append(all(Es[i + 1] < Es[i] for i in range(4)))
c15 = {(c["limite"], c["control"]): c for c in j15["criterios"]}
cL12 = c15[("L12", "caja delta=1.0")]
fila("9.7", "Caja: E0(R) decreciente (L12)", "decreciente en R (Dirichlet)",
     f"cajas 9.6 (15 celdas, transferencia): {sum(dec)}/3 delta decrecientes; delta=1.0: {cL12['valor']}",
     all(dec) and cL12["pasa"], "15", "L12; 14_cajas.json celdas")
for d in ("0.2", "0.5", "1.0"):
    c = c15[("L05", f"Hellmann-Feynman delta={d}")]
    fila("9.7", f"Hellmann-Feynman (L05) delta={d}", c["criterio"], c["valor"], c["pasa"], "15", "L05")
c = c15[("L06", "virial delta=0.2")]
fila("9.7", "Virial (L06) delta=0.2", c["criterio"], c["valor"], c["pasa"], "15", "L06")
c = c15[("L04", "cotas -1/2 <= E0 <= -1/2 + delta")]
fila("9.7", "Cotas (L04)", "-1/2 <= E0 <= -1/2 + delta", c["valor"], c["pasa"], "15", "L04")
c = c15[("L19", "delta=2 sin ligado")]
fila("9.7", "Sin ligado en delta >= 2 (L19)", c["criterio"], c["valor"], c["pasa"], "15", "L19")
V = j14["veredictos"]
fila("9.7", "Umbral (Fase 4; avance de la Fase 2)", "intervalo compatible con 1.1906124211 y dentro de [1.19055, 1.24305]",
     f"cajas: 1.15 {V['1.15']['veredicto']}, 1.18 {V['1.18']['veredicto']}, 1.2 {V['1.2']['veredicto']} => delta_c en [1.18, 1.20]; "
     "el intervalo final es de la Fase 4", None, "14", "veredictos")
co = [j12["pigs"][k]["EL"]["cociente"] for k in ("prod02", "tau2", "tau5", "tau10")]
fila("9.7", "Errores por bloques: regla del cociente", "si (err cadenas/err bloques)^2 > 2 se usa el de cadenas (siempre se usa el mayor)",
     "cocientes en E: " + ", ".join(f"{x:.2f}" for x in co) + " (prod, tau 2, 5, 10); se reporta siempre el mayor", True, "12",
     "pigs/*/EL/cociente")

# ======================================================================= B. Hulthen y pozo (13)
for c in j13["criterios"]:
    fila("Hulthen/pozo", c["control"], c["criterio"], c["valor"], c["pasa"], "13", "criterios")

# ======================================================================= C. Cajas (14)
st = j14["V3_criterio_estricto"]
nc = sum(X["c"]["c"] for d in V.values() for X in d["por_terna"].values())
fila("cajas", "Condicion (c) en las 9 ternas", "mismo signo, misma tendencia, E0 compatibles", f"{nc}/9", nc == 9, "14", "veredictos")
ncomp = sum(c["compatible"] for d in j14["celdas"].values() for c in d.values())
fila("cajas", "E0 transferencia frente al radial, celda a celda", "|dif| <= 2(err_tr + err_rad)", f"{ncomp}/15", ncomp == 15, "14", "celdas")
fila("cajas", "Idem con solo el error de la transferencia (V3, con sesgo de pared)", "|dif| <= err_tr",
     f"{st['pasan_con_pared']}/15 con el termino de pared; {st['pasan_sin_pared']}/15 sin el (fallan sin el: "
     + ", ".join(st["fallan_sin_pared"]) + ")", st["pasan_con_pared"] == 15, "14", "V3_criterio_estricto")
ords = [(d, R, c["orden_trotter"]) for d, cel in j14["celdas"].items() for R, c in cel.items()]
malos = [f"{d} {R}: {o:.2f}" for d, R, o in ords if not 1.8 <= o <= 2.2]
fila("cajas", "Orden de Trotter tras Richardson en h", "[1.8, 2.2]", f"{15-len(malos)}/15; fuera: " + ", ".join(malos),
     not malos, "14", "celdas/*/orden_trotter")
on = j14["orden_nystrom"]
fila("cajas", "Orden de la malla Nystrom cerca del umbral (delta=1.18, eps=0.1)", "4, como en 11.4",
     f"R=50: {on['R50']['orden']:.3f}; R=100: {on['R100']['orden']:.3f}", False, "14", "orden_nystrom")
for d in ("1.15", "1.18", "1.2"):
    X = V[d]
    t = X["terna"]
    fila("cajas", f"Veredicto 9.6 delta={d}", "criterio completo (a), (a'), (b), (c) o no ligado con ley de caja",
         f"{X['veredicto']}, terna {t}" + (f"; desviacion de la ley {[round(x, 3) for x in X['por_terna'][str(tuple(t))]['radial']['dev_ley']]}"
                                           if X["veredicto"] == "no ligado" else ""), True, "14", "veredictos")

# ======================================================================= D. limites (15) y radial (10)
for c in j15["criterios"]:
    fila("limites", f"{c['limite']} {c['control']}", c["criterio"], c["valor"], c["pasa"], "15", c["limite"])
y = J["10"]["yukawa_0.2"]["V3_referencia_fina"]
fila("radial", "delta=0.2 E0 radial (h=1/40, 1/80) frente al exacto", "< 5e-9",
     f"{y['error_h40_frente_fina']:+.2e}", y["criterio_5e9_h40_frente_exacto"], "10", "yukawa_0.2/V3_referencia_fina")
fila("radial", "delta=0.2 E0 radial (h=1/80, 1/160) frente al exacto", "< 5e-9 (test: 1e-9)",
     f"{y['error_h80_frente_fina']:+.2e}", y["criterio_5e9_h80_frente_exacto"], "10", "yukawa_0.2/V3_referencia_fina")

# ======================================================================= figuras congeladas
FIGD = os.path.join(BASE, "figuras")
figs = []
for fn in sorted(os.listdir(FIGD)):
    if fn.endswith(".png"):
        h = hashlib.sha256(open(os.path.join(FIGD, fn), "rb").read()).hexdigest()
        figs.append(dict(figura=fn, sha256=h, script=next((SCR[k] for k in SCR if fn.startswith(k + "_")), "")))

json.dump(dict(filas=filas, figuras=figs), open(os.path.join(RES, "16_tabla_controles.json"), "w"), indent=1,
          ensure_ascii=False, default=float)


# ======================================================================= markdown
def md(x):
    return str(x).replace("|", "\\|")


est = lambda p: "sí" if p is True else ("**no**" if p is False else "medido")
L = []
for b, tit in (("9.7", "A. Criterios de 9.7 aplicables a la Fase 2"), ("Hulthen/pozo", "B. Controles exactos: Hulthén y pozo cuadrado (sección 13)"),
               ("cajas", "C. Criterio de cajas 9.6 con la condición (c) (sección 14)"),
               ("limites", "D. Límites físicos L01–L19 comprobados con la integral de camino (script 15)"),
               ("radial", "E. Referencia radial (sección 10)")):
    F = [f for f in filas if f["bloque"] == b]
    L.append(f"\n### {tit}\n\n| # | Control | Criterio | Valor medido | ¿Pasa? | Script | Fuente (JSON) |\n|---|---|---|---|---|---|---|")
    for i, f in enumerate(F, 1):
        L.append(f"| {tit[0]}{i} | {md(f['control'])} | {md(f['criterio'])} | {md(f['valor'])} | {est(f['pasa'])} | "
                 f"`{f['script']}` | `{f['json']}` |")
n_si = sum(f["pasa"] is True for f in filas); n_no = sum(f["pasa"] is False for f in filas)
n_me = sum(f["pasa"] is None for f in filas)
FIGL = ["| Figura | Script que la produce | sha256 |", "|---|---|---|"] + [
    f"| `figuras/{g['figura']}` | `{g['script']}` | `{g['sha256'][:16]}…` |" for g in figs]
INTRO = f"""# 15. Tabla de controles de la Fase 2 (consolidada)

Fecha: 27-10-2026. Equipo: Juan Sebastián Calixto (verificación) y Luis Felipe Ramírez (implementación). Unidades $\\hbar=m=g=1$, $V=-e^{{-\\delta r}}/r$, $\\delta_c=1.1906124211$ (Fase 1).

**Estado: SIN FIRMAR.** Esta tabla la generó `fase2/codigo/16_tabla_controles.py` leyendo los JSON de los scripts 10 a 15 después de las correcciones de la respuesta V3 (`fase2/verificacion/V3_respuesta_hallazgos.md`). Ninguna cifra está escrita a mano: cada fila dice de qué script y de qué JSON sale. La firma de quien verifica (Juan Sebastián) va al final; un agente no puede firmar por él.

**Resumen:** {len(filas)} filas; **{n_si} pasan**, **{n_no} no pasan** y {n_me} son medidas o informativas (sin criterio de aceptación, o con decisión pendiente). Los que no pasan están en negrita en la columna "¿Pasa?" y se explican en la sección "Lo que no pasa".

Leyenda: "sí" = cumple el criterio fijado antes de ejecutar; "**no**" = no lo cumple (no se cambió la tolerancia después); "medido" = magnitud que el plan pide medir y declarar, o informativa.
"""

NOPASA = "\n## Lo que no pasa y por qué\n\n" + "\n".join(
    f"- **{f['control']}** ({f['valor']}). Criterio: {f['criterio']}." for f in filas if f["pasa"] is False) + """

Lectura (detalle en las secciones 11 a 15 y en V3):
- Los fallos de la sección 11 (estabilidad de Nyström 0.02 → 0.04 y control con $h=0.04$) tienen una causa medida: error de extremo del trapecio en la cúspide de Coulomb, de orden $h^4/\\epsilon$. Con Richardson en $h$ (exponente 4) desaparecen. Cerca del umbral el orden de la malla no es 4 (1.36 y 2.29): para la Fase 4 hay que usar $h=0.02$ y $0.01$.
- La ley $\\epsilon^2$ sin Richardson en $h$ en $\\delta=0.2$ falla porque el sesgo de Trotter es del tamaño del error de Nyström; con Richardson en $h$ pasa, y en $\\delta=1.0$ pasa en las dos formas.
- El orden de Trotter en $R=50$ y $100$ lo rebaja la pared en $R$ sin imagen ($R+0.5826\\sqrt\\epsilon$).
- En el pozo, el ajuste a cinco puntos con la ley fija $\\epsilon^{3/2}$ falla en $V_0=1.3$, donde el orden todavía es preasintótico (1.67 → 1.52).
- La anomalía de $\\tau=5$ en el PIGS se mantiene en la producción; las réplicas y la combinación se dan en la parte A.
- L16: la suma del núcleo libre en la malla tiene un error $O(h^2)$ de extremo (medido), no $10^{-10}$ como se esperaba al fijar el criterio. Las propiedades exactas de $K_D$ ($K_D\\ge0$, $K_D(0,r')=0$) sí se cumplen; el criterio quedó mal planteado y se deja como "no pasa".

## Límites que no se comprueban todavía con la integral de camino

- **L01** (escalamiento): el código trabaja en unidades reducidas; se comprobó con el radial en la Fase 1 (sección 7.3). Probarlo con la transferencia exigiría reintroducir $m$ y $g$.
- **L10** (umbral) y **L11** (extensión cerca del umbral): Fase 4 y Fase 3. Avance: $\\delta_c\\in[1.18,1.20]$ por cajas (parte C).
- **L13** (no ligado en caja con $a_s$): cubierto por el veredicto de $\\delta=1.20$ (parte C) y por L19.
- **L15** con PIGS cerca del umbral y **L17** con suavizado: no se usa suavizado (el método aprobado no lo necesita); el peso de la transferencia es real, positivo y finito (`11_transferencia.json`, `peso`: 0 negativos, 0 no finitos).

## Decisiones pendientes de firma (Juan Sebastián)

1. Redefinir el control de tabulación de 9.7 como Richardson en $h$ con exponente 4 y estabilidad del valor extrapolado (sección 11.4).
2. Si la anomalía de $\\tau=5$ queda cerrada con las réplicas y la combinación (parte A; sección 12).
3. El umbral 0.1 de la desviación de la ley de caja para "no ligado" (sección 14.5).
4. El tratamiento del pozo con orden $\\epsilon^{3/2}$ y extrapolación en $h$ de orden ~1 (sección 13).
5. Si se corrige la pared en $R$ (imagen en $R$ o $R_{\\rm ef}$) en las Fases 3 y 4, o se mantiene el término de pared en el error (sección 14.4).
6. Si se acepta la corrección de Wigner-Kirkwood de $U_C$ fuera de $r=10$ como parte del método (sección 11.9).

## Figuras congeladas (Fase 2)

Huella sha256 de cada figura tal como quedó tras las ejecuciones de V3 (los 16 primeros caracteres; las completas en `resultados/16_tabla_controles.json`). Para regenerar una figura se ejecuta su script; si la huella cambia, la figura cambió.

"""

FIRMA = """
## Firma

| Rol | Nombre | Fecha | Firma |
|---|---|---|---|
| Verificación | Juan Sebastián Calixto | | (pendiente) |
| Implementación | Luis Felipe Ramírez | | (pendiente) |
"""
with open(os.path.join(BASE, "secciones", "15_tabla_controles.md"), "w") as f:
    f.write(INTRO + "\n".join(L) + "\n" + NOPASA + "\n".join(FIGL) + "\n" + FIRMA)
print(f"{len(filas)} filas: {n_si} pasan, {n_no} no pasan, {n_me} medidas/informativas; {len(figs)} figuras")
