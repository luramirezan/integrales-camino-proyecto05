"""09_tablas.py -- tablas en markdown para seccion_articulo.md y LEEME.md, generadas desde 01, 05, 06 y 07.
Salida: resultados/09_tablas.md (se copia tal cual en los textos) y resultados/09_tablas.json.
"""
import sys
import e2comun as c

X = c.cargar("05_cruces"); T = c.cargar("01_teoria"); A6 = c.cargar("06_artefacto"); K = c.cargar("07_controles")
REF = c.DELTA_C_REF
L = []
ere = {f["R"]: f for f in T["modelo_ERE"]}


def e(x, n=2):
    return f"{x:.{n}e}".replace("e-0", "e-").replace("e+0", "e+")


for obs, nombre in (("y", "2R²E₀/π²"), ("rho", "⟨r⟩/R")):
    L.append(f"\n**Tabla: cruces δ*(R, 2R) de {nombre}** (barras: mayor de Monte Carlo y propagación lineal; método B: receta "
             "de la Fase 3 aplicada al cruce).\n")
    L.append("| Par | Integral de camino, A | Integral de camino, B | Radial h = 1/160 | Disparo sin malla | Teoría (modelo ERE) | valor en el cruce (disparo) |")
    L.append("|---|---|---|---|---|---|---|")
    pa = {f["R"]: f for f in X["fuentes"]["transferencia"][obs]["pares"]}
    pb = {f["R"]: f for f in X["transferencia_metodo_B"][obs]["pares"]}
    pr = {f["R"]: f for f in X["fuentes"]["radial_h160"][obs]["pares"]}
    pd = {f["R"]: f for f in X["fuentes"]["disparo"][obs]["pares"]}
    for R in sorted(pd):
        ta = f"{pa[R]['delta']:.7f} ± {e(pa[R]['sigma'], 1)}" if R in pa else "—"
        tb = f"{pb[R]['delta']:.7f} ± {e(pb[R]['sigma'], 1)}" if R in pb else "—"
        L.append(f"| {R}/{2*R} | {ta} | {tb} | {pr[R]['delta']:.7f} ± {e(pr[R]['sigma'], 1)} | {pd[R]['delta']:.9f} | "
                 f"{ere[R]['delta_y' if obs == 'y' else 'delta_rho']:.9f} | {pd[R]['valor']:.5f} |")
L.append("\n**Tabla: extrapolación en R** (ajuste δ* = δ_c + α/R² + β/R³ con los pares de R ≥ 100; barra = estadística + "
         "|ajuste − Richardson de los dos pares mayores|).\n")
L.append("| Fuente | Observable | δ_c | barra | intervalo | α (teoría) | ¿contiene 1.1906124210606? |")
L.append("|---|---|---|---|---|---|---|")
filas_ext = []
for fu, et in (("transferencia", "integral de camino, A"), ("transferencia_metodo_B", "integral de camino, B"),
               ("radial_h160", "radial h = 1/160"), ("radial_h40", "radial h = 1/40"), ("disparo", "disparo sin malla")):
    for obs, nm in (("y", "2R²E₀/π²"), ("rho", "⟨r⟩/R")):
        ex = (X["transferencia_metodo_B"] if fu == "transferencia_metodo_B" else X["fuentes"][fu])[obs]["extrapolacion"]
        at = T["constantes"]["alpha_y" if obs == "y" else "alpha_rho"]
        L.append(f"| {et} | {nm} | {ex['ajuste_ab']['delta_c']:.10f} | {e(ex['barra_total'])} | [{ex['intervalo'][0]:.8f}, "
                 f"{ex['intervalo'][1]:.8f}] | {ex['ajuste_ab']['alpha']:.3f} ({at:.3f}) | {'sí' if ex['contiene_referencia'] else 'no'} |")
        filas_ext.append(dict(fuente=fu, obs=obs, **{k: ex[k] for k in ("intervalo", "barra_total", "contiene_referencia")},
                              delta_c=ex["ajuste_ab"]["delta_c"]))
L.append("\n**Tabla: la misma extrapolación usando solo cajas R ≤ 800** (pares 100/200, 200/400 y 400/800).\n")
L.append("| Fuente | Observable | δ_c | barra | intervalo | ¿contiene la referencia? |")
L.append("|---|---|---|---|---|---|")
for fu, et in (("transferencia", "integral de camino, A"), ("transferencia_metodo_B", "integral de camino, B"),
               ("radial_h160", "radial h = 1/160"), ("disparo", "disparo sin malla")):
    for obs, nm in (("y", "2R²E₀/π²"), ("rho", "⟨r⟩/R")):
        ex = (X["transferencia_metodo_B"] if fu == "transferencia_metodo_B" else X["fuentes"][fu])[obs]["extrapolacion_R_hasta_800"]
        L.append(f"| {et} | {nm} | {ex['ajuste_ab']['delta_c']:.10f} | {e(ex['barra_total'])} | [{ex['intervalo'][0]:.8f}, "
                 f"{ex['intervalo'][1]:.8f}] | {'sí' if ex['contiene_referencia'] else 'no'} |")
d119 = A6["delta_119"]
L.append("\n**Tabla: δ = 1.19, el signo frente al cruce** (a_s = %.1f).\n" % d119["a_s"])
L.append("| R | E₀ disparo | E₀ radial 1/160 | E₀ integral de camino | 2R²E₀/π² |")
L.append("|---|---|---|---|---|")
for f in d119["filas"]:
    et = f"{f['E_transferencia']:+.4e} ± {e(f['err_transferencia'], 1)}" if f.get("E_transferencia") == f.get("E_transferencia") and "E_transferencia" in f else "—"
    L.append(f"| {f['R']} | {f['E_disparo']:+.4e} | {f['E_radial160']:+.4e} | {et} | {f['y_disparo']:.4f} |")
open(c.RES + "/09_tablas.md", "w").write("\n".join(L) + "\n")
c.guardar("09_tablas", dict(script="09_tablas.py", fecha=c.ahora(), extrapolaciones=filas_ext))
print("\n".join(L))
