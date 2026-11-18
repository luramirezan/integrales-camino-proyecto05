"""11b_cifras_clave.py -- comprobacion explicita de las cifras clave del texto: para cada una se lee el valor en el JSON,
se formatea como en el texto y se comprueba (1) que el formato coincide y (2) que esa cadena aparece en el archivo.
Complementa a 11_cifras_texto.py, cuya busqueda automatica tiene coincidencias casuales con 3 o 4 cifras.
Salida: resultados/11b_cifras_clave.json y _salida.txt
"""
import os, sys
import numpy as np
import e2comun as c

sys.stdout = c.Tee("11b_cifras_clave")
X = c.cargar("05_cruces"); T = c.cargar("01_teoria"); D = c.cargar("02_disparo"); A6 = c.cargar("06_artefacto")
V = c.cargar("10_verificacion"); K = c.cargar("07_controles"); P12 = c.cargar("12b_trotter_eps0025")
TR = {R: c.cargar(f"04_transferencia_R{R}")["celdas"] for R in X["R_transferencia"]}


def sci(x, n=1):
    m, e = f"{x:.{n}e}".split("e")
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{m}×10{str(int(e)).translate(sup)}".replace("-", "−", 1) if x < 0 else f"{m}×10{str(int(e)).translate(sup)}"


ex = lambda fu, o: X["fuentes"][fu][o]["extrapolacion"]
exB = lambda o: X["transferencia_metodo_B"][o]["extrapolacion"]
pd = {f["R"]: f for f in X["fuentes"]["disparo"]["y"]["pares"]}
pB = {f["R"]: f for f in X["transferencia_metodo_B"]["y"]["pares"]}
pw = {f["R"]: f["corrimiento"] for f in T["pared_transferencia"]["filas"]}
v1 = {(f["obs"], f["R"]): f for f in V["V1_cruces_sin_interpolar"]}
C = [  # (archivo, cadena esperada en el texto)
    ("seccion_articulo.md", f"a_s = {D['energia_cero']['1.19']['a']:.1f}"),
    ("seccion_articulo.md", f"r_e = {T['constantes']['r_e']:.5f}"),
    ("seccion_articulo.md", f"c = −d(1/a)/dδ = {T['constantes']['c']:.6f}"),
    ("seccion_articulo.md", f"α = {T['constantes']['alpha_y']:.4f}"),
    ("seccion_articulo.md", f"β = {T['constantes']['beta_y']:.3f}"),
    ("seccion_articulo.md", f"α_ρ = {T['constantes']['alpha_rho']:.3f}"),
    ("seccion_articulo.md", f"R + {T['pared_transferencia']['c_w']:.4f}"),
    ("seccion_articulo.md", sci(pw[400], 2)),
    ("seccion_articulo.md", f"{len(c.DELTAS)} valores de δ"),
    ("seccion_articulo.md", f"({len(c.DELTAS) * len(c.RS)} celdas)"),
    ("seccion_articulo.md", "1.19054 < δ_c < 1.19068" if (round(ex('transferencia', 'y')['intervalo'][0], 5) == 1.19054
                                                          and round(ex('transferencia', 'y')['intervalo'][1], 5) == 1.19068) else "FALLA-A"),
    ("seccion_articulo.md", "1.190609 < δ_c < 1.190616" if (round(exB('y')['intervalo'][0], 6) == 1.190609
                                                            and round(exB('y')['intervalo'][1], 6) == 1.190616) else "FALLA-B"),
    ("seccion_articulo.md", f"[{X['fuentes']['transferencia']['y']['extrapolacion_R_hasta_800']['intervalo'][0]:.8f}, "
                            f"{X['fuentes']['transferencia']['y']['extrapolacion_R_hasta_800']['intervalo'][1]:.8f}] (A)"),
    ("seccion_articulo.md", f"[{X['transferencia_metodo_B']['y']['extrapolacion_R_hasta_800']['intervalo'][0]:.8f}, "
                            f"{X['transferencia_metodo_B']['y']['extrapolacion_R_hasta_800']['intervalo'][1]:.8f}] (B)"),
    ("seccion_articulo.md", "a 5×10⁻⁷ en el par 50/100" if round(abs(v1[('y', 50)]['dif_ERE']), 7) == 5e-7 else "FALLA-ERE50"),
    ("seccion_articulo.md", "a 2×10⁻⁹ o mejor desde el 200/400" if max(abs(v1[('y', R)]['dif_ERE']) for R in (200, 400, 800, 1600)) <= 2e-9 else "FALLA-ERE"),
    ("seccion_articulo.md", ", ".join(f"{r:.3f}" for r in ex("disparo", "y")["razones_dif_sucesivas"][:-1]) + " y "
     + f"{ex('disparo', 'y')['razones_dif_sucesivas'][-1]:.3f}"),
    ("seccion_articulo.md", ", ".join(sci(pB[R]["delta"] - pd[R]["delta"]) for R in (50, 100, 200)) + " y " + sci(pB[400]["delta"] - pd[400]["delta"])),
    ("seccion_articulo.md", ", ".join(sci(pw[R]) for R in (50, 100, 200)) + " y " + sci(pw[400], 2)),
    ("seccion_articulo.md", "a 2.4×10⁻⁷ o mejor" if max(abs(pB[R]["delta_pared_restada"] - pd[R]["delta"]) for R in (400, 800, 1600)) < 2.45e-7 else "FALLA-pared"),
    ("seccion_articulo.md", f"vale {sci(TR[800]['1.1906']['err'])}, {sci(TR[1600]['1.1906']['err'])} y {sci(TR[3200]['1.1906']['err'])}"),
    ("seccion_articulo.md", f"el menor es {min(min(v) for v in A6['delta_119']['cruces'].values()):.7f}"),
    ("seccion_articulo.md", f"pasan {K['n_pasa']} de {K['n']}"),
    ("seccion_articulo.md", f"{len(D['deltas'])} valores de δ y 7 cajas"),
    ("seccion_articulo.md", sci(max(f["dif_interp"] for f in X["fuentes"]["disparo"]["rho"]["pares"]))),
    ("seccion_articulo.md", f"(1.490 y {ex('disparo', 'y')['ajuste_ab']['alpha']:.4f} frente a {T['constantes']['alpha_y']:.4f}; "
                            f"{ex('radial_h160', 'rho')['ajuste_ab']['alpha']:.3f} y {ex('disparo', 'rho')['ajuste_ab']['alpha']:.4f} frente a {T['constantes']['alpha_rho']:.3f})"),
    ("seccion_articulo.md", f"{ex('radial_h160', 'y')['ajuste_ab']['alpha']:.3f} ({T['constantes']['alpha_y']:.3f})"),
    ("LEEME.md", f"**1.19054410 < δ_c < 1.19067723** (centro {ex('transferencia', 'y')['ajuste_ab']['delta_c']:.10f}, barra {sci(ex('transferencia', 'y')['barra_total'], 2)})"),
    ("LEEME.md", f"**{exB('y')['intervalo'][0]:.8f} < δ_c < {exB('y')['intervalo'][1]:.8f}** (centro {exB('y')['ajuste_ab']['delta_c']:.10f}, barra {sci(exB('y')['barra_total'], 2)})"),
    ("LEEME.md", ", ".join(f"{pd[R]['delta']:.9f}" for R in (50, 100, 200, 400, 800)) + f" y {pd[1600]['delta']:.9f}"),
    ("LEEME.md", f"{ex('disparo', 'y')['ajuste_ab']['delta_c']:.10f} (y) y {ex('disparo', 'rho')['ajuste_ab']['delta_c']:.10f} (⟨r⟩/R)"),
    ("LEEME.md", f"{sci(ex('disparo', 'y')['barra_total'], 2)} y {sci(ex('disparo', 'rho')['barra_total'], 2)}"),
    ("verificacion.md", f"es 2.084 frente a 2.384" if (round(P12['filas'][0]['p_01_005_0025'], 3) == 2.084 and round(P12['filas'][0]['p_02_01_005'], 3) == 2.384) else "FALLA-12b"),
    ("verificacion.md", f"difiere del de la receta en {sci(abs(P12['filas'][0]['dif_rel']))} relativo"),
    ("verificacion.md", f"1.1906091755 en vez de\n  {V['V7_pesos']['transferencia_y']['ponderado']:.10f}" if abs(V['V7_pesos']['transferencia_y']['sin_pesos'] - 1.1906091755) < 5e-11 else "FALLA-V7"),
    ("verificacion.md", f"da 1.1906124210606, a {sci(abs(V['V2_delta_c_energia_cero']['dif_ref']))}"),
    ("verificacion.md", f"es {sci(V['V6_semilla']['sigma_mc_05'], 2)} en el\n  script 05 y {sci(V['V6_semilla']['sigma_semilla1'], 2)} y {sci(V['V6_semilla']['sigma_semilla2'], 2)}"),
    # B de <r>/R con el termino de pared (revision R2-01)
    ("LEEME.md", f"Con ⟨r⟩/R: [{ex('transferencia', 'rho')['intervalo'][0]:.8f}, {ex('transferencia', 'rho')['intervalo'][1]:.8f}] (A)"),
    ("verificacion.md", f"[{X['fuentes']['transferencia']['rho']['extrapolacion_R_hasta_800']['intervalo'][0]:.8f}, "
                        f"{X['fuentes']['transferencia']['rho']['extrapolacion_R_hasta_800']['intervalo'][1]:.8f}]"),
    ("seccion_articulo.md", f"de {sci(X['fuentes']['transferencia']['rho']['sin_pared_A']['extrapolacion']['barra_total'], 2)} a\n"
                            f"{sci(ex('transferencia', 'rho')['barra_total'], 2)}"),
    ("LEEME.md", f"[{exB('rho')['intervalo'][0]:.8f}, {exB('rho')['intervalo'][1]:.8f}] (B; la barra de B de ⟨r⟩/R incluye"),
    ("seccion_articulo.md", f"| integral de camino, B | ⟨r⟩/R | {exB('rho')['ajuste_ab']['delta_c']:.10f} | {exB('rho')['barra_total']:.2e} | "
                            f"[{exB('rho')['intervalo'][0]:.8f}, {exB('rho')['intervalo'][1]:.8f}] |".replace("e-05", "e-5")),
    ("seccion_articulo.md", f"pasa de {sci(X['transferencia_metodo_B']['rho']['extrapolacion_sin_pared_R2_01']['barra_total'], 2)} a "
                            f"{sci(exB('rho')['barra_total'], 2)}, con intervalo [{exB('rho')['intervalo'][0]:.8f}, {exB('rho')['intervalo'][1]:.8f}]"),
    ("verificacion.md", ", ".join("+" + sci(f["err_pared"], 2) for f in X["transferencia_metodo_B"]["rho"]["pares"][:3]) + " y +"
                        + sci(X["transferencia_metodo_B"]["rho"]["pares"][3]["err_pared"], 2)),
    ("teoria.md", f"r_e(\\delta_c) = {T['constantes']['r_e']:.5f}"),
    ("teoria.md", f"m₁ = ∫₀^∞ r(1 − u₀²/C²) dr = {T['constantes']['m1']:.4f}"),
    ("teoria.md", f"c_w = β[√0.05 + (√0.05 − √0.1)/3] = {T['pared_transferencia']['c_w']:.4f}"),
    ("teoria.md", ", ".join(f"{r:.3f}" for r in T["pozo_cuadrado"]["razon_dif_por_mitad_b_z0"])),
    ("teoria.md", ", ".join(f"{r:.2f}" for r in T["razones_ERE_y"])),
    ("teoria.md", f"en R = 50 vale\n{sci(T['constantes']['cola_exp_R50'])}"),
]
res = []
for fn, s in C:
    txt = open(os.path.join(c.BASE, fn)).read()
    ok = s in txt or s.replace("\n  ", " ").replace("\n", " ") in txt.replace("\n  ", " ").replace("\n", " ")
    res.append(dict(archivo=fn, cadena=s, encontrada=bool(ok)))
    print(f"{'OK   ' if ok else 'FALTA'} {fn}: {s!r}")
n = sum(r["encontrada"] for r in res)
c.guardar("11b_cifras_clave", dict(script="11b_cifras_clave.py", fecha=c.ahora(), n=len(res), n_ok=n, filas=res))
print(f"{n}/{len(res)} cadenas encontradas")
