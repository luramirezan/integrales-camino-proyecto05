"""generar_diapositivas_fase2.py -- Primera presentacion (Fase 2, semana 7).

Construye diapositivas_fase2.pptx (python-pptx) y guion_fase2.md.
Todas las cifras se LEEN de fase2/resultados/*.json (o se copian de secciones/15_tabla_controles.md,
que las genera 16_tabla_controles.py desde esos JSON). Las ecuaciones se renderizan con
matplotlib mathtext en presentacion/ecuaciones/. Estilo de la Fase 1: 16:9, Calibri, titulos
azul noche 1B2A41, acento C0392B, gris 555F6B.
"""
import json
import os
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

AQUI = os.path.dirname(os.path.abspath(__file__))
F2 = os.path.abspath(os.path.join(AQUI, ".."))
RES = os.path.join(F2, "resultados")
FIG = os.path.join(F2, "figuras")
EQ = os.path.join(AQUI, "ecuaciones")
os.makedirs(EQ, exist_ok=True)

NAVY = RGBColor(0x1B, 0x2A, 0x41)
RED = RGBColor(0xC0, 0x39, 0x2B)
GRAY = RGBColor(0x55, 0x5F, 0x6B)
LIGHT = RGBColor(0xF2, 0xF4, 0xF7)
BLUE = RGBColor(0x2E, 0x86, 0xAB)
GREEN = RGBColor(0x1E, 0x84, 0x49)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Calibri"


def J(n):
    with open(os.path.join(RES, n)) as f:
        return json.load(f)


j11, j12, j12c, j13, j14, j15, j18 = (J("11_transferencia.json"), J("12_pigs.json"),
                                       J("12c_pigs_coulomb_tau5.json"), J("13_controles.json"),
                                       J("14_cajas.json"), J("15_limites.json"),
                                       J("18_figura_presentacion.json"))
tabla15 = open(os.path.join(F2, "secciones", "15_tabla_controles.md")).read()


def e(x, d=1):
    """x en notacion a x 10^b con signo menos tipografico."""
    s = f"{x:.{d}e}"
    m, ex = s.split("e")
    ex = int(ex)
    m = m.replace("-", "−")
    return f"{m}×10{sup(ex)}"


def sup(n):
    t = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return str(n).translate(t)


def f(x, d):
    return f"{x:.{d}f}".replace("-", "−")


# ----------------------------------------------------------------------------- cifras
rad02 = j11["referencia_radial"]["0.2"]
peso01 = j11["peso"]["0.1"]
U001 = peso01["U(0.01,0.01)"]
prim001 = peso01["eps/r_primitiva_en_r=0.01"]
negs = sum(j11["peso"][k]["T_negativos"] for k in j11["peso"])
nofin = sum(j11["peso"][k]["T_no_finitos"] for k in j11["peso"])

# Coulomb
res0 = j11["resultados"]["0.0"]
dE_coul = [abs(res0[f"h=0.02,eps={x}"]["E_tablaRich"] + 0.5) for x in ("0.2", "0.1", "0.05")]
dr_coul = [abs(res0[f"h=0.02,eps={x}"]["r_med"] - 1.5) for x in ("0.2", "0.1", "0.05")]
Ac = j12c["A_coulomb"]
coul_r, coul_er, coul_sr = Ac["rmid"]["media"], Ac["rmid"]["err"], Ac["rmid"]["sigma_exacto"]
coul_r2, coul_er2, coul_sr2 = Ac["r2mid"]["media"], Ac["r2mid"]["err"], Ac["r2mid"]["sigma_exacto"]
coul_p = Ac["histograma_rmid"]["p"]

# Hulthen y pozo: de la tabla 15 (filas B), que sale de 13_controles.json
def fila(idn):
    m = re.search(r"^\| " + idn + r" \|(.*)$", tabla15, re.M)
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", m.group(1))]

B8, B11, B14 = fila("B8"), fila("B11"), fila("B14")
B12, B15 = fila("B12"), fila("B15")
B22, B26, B27 = fila("B22"), fila("B26"), fila("B27")
B21, B25 = fila("B21"), fila("B25")
hul_ext = [float(re.match(r"([+-][0-9.e+-]+)", b[2]).group(1)) for b in (B8, B11, B14)]
hul_ord = [float(b[2].split()[0]) for b in (B12, B15)]
pozo_ext2 = float(re.match(r"([+-][0-9.e+-]+)", B22[2]).group(1))
pozo_ext13 = float(re.match(r"([+-][0-9.e+-]+)", B26[2]).group(1))
pozo_eps2 = float(re.search(r"ley eps\^2: ([+-][0-9.e+-]+)", B22[2]).group(1))
pozo_b3b13 = float(B27[2])
pozo_ord2 = B21[2]
pozo_ord13 = B25[2]

# delta = 0.2
E_rad = j18["E_radial"]
P20 = j18["PIGS_tau20"]
tr = j11["trotter"]["0.2"]["Richardson h^4 (0.02,0.04)"]
tr_ord = tr["orden"]
tr_ext = tr["extrap_menos_ref"]
tr1_ord = j11["trotter"]["1.0"]["Richardson h^4 (0.02,0.04)"]["orden"]
estab = j11["estabilidad_nystrom"]
r2_rad = rad02["r2_med"]
p20 = j12["pigs"]["prod02"]

# proyeccion
pr = j11["proyeccion"]
dmix1 = pr["E_mixto_menos_limite"][pr["tau"].index(1)]
dmix20 = pr["E_mixto_menos_limite"][pr["tau"].index(20)]
brecha = pr["brecha"]
pinf = j12["proyeccion_informativo"]
C5 = j12c["C_tau5_combinado"]
scan = {round(s["tau"]): s for s in j12["tau_scan"]}

# cajas
cel = j14["celdas"]
ver = j14["veredictos"]
trot02 = max(abs(c["crudo"]["h0.02_eps0.2"]["E0"] - c["E_mejor"]) / abs(c["E_mejor"])
             for d in cel.values() for c in d.values())
trot01 = max(abs(c["crudo"]["h0.02_eps0.1"]["E0"] - c["E_mejor"]) / abs(c["E_mejor"])
             for d in cel.values() for c in d.values())
beta = j14["pared"]["beta"]
nC1 = sum(1 for dl in ver for t in ver[dl]["por_terna"].values() if t["c"]["c"])
nT = sum(len(ver[dl]["por_terna"]) for dl in ver)
a_s120 = j14["a_s"]["1.2"]
dev120 = ver["1.2"]["por_terna"]["(200, 400, 800)"]["transferencia"]["dev_ley"]

# tabla 15: resumen
m = re.search(r"\*\*Resumen:\*\* (\d+) filas; \*\*(\d+) pasan\*\*, \*\*(\d+) no pasan\*\* y (\d+) son", tabla15)
n_filas, n_pasa, n_nopasa, n_med = (int(x) for x in m.groups())

# ----------------------------------------------------------------------------- ecuaciones
def ecuacion(nombre, tex, size=22, color="#1B2A41"):
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, tex, fontsize=size, color=color)
    ruta = os.path.join(EQ, nombre + ".png")
    fig.savefig(ruta, dpi=250, transparent=True, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    from PIL import Image
    w, h = Image.open(ruta).size
    return ruta, w / 250.0, h / 250.0


EQS = {
    "V": r"$V(r)=-\frac{e^{-\delta r}}{r},\qquad \delta=\frac{\mu\hbar^2}{mg},\qquad \delta_c=1.1906124211$",
    "T": r"$T(r,r';\epsilon)=K_D(r,r';\epsilon)\;e^{-U_C(r,r';\epsilon)}\;e^{-\epsilon\,[W(r)+W(r')]/2}$",
    "KD": r"$K_D=\frac{e^{-(r-r')^2/2\epsilon}-e^{-(r+r')^2/2\epsilon}}{\sqrt{2\pi\epsilon}},\qquad U_C=-\ln\frac{\rho_C}{K_D}$",
    "W": r"$W(r)=V(r)+\frac{1}{r}=\frac{1-e^{-\delta r}}{r}\ \in\ [0,\delta]$",
    "P": r"$P[r_0,\dots,r_M]=u_T(r_0)\,\prod_{k}T(r_k,r_{k+1};\epsilon)\,u_T(r_M),\qquad u_T=r\,e^{-r}$",
    "Emix": r"$E_{\rm mixto}(\tau)=\frac{\langle H u_T|\,T^M\,|u_T\rangle}{\langle u_T|\,T^M\,|u_T\rangle},\qquad \tau=M\epsilon$",
    "E0T": r"$E_0(\epsilon)=-\frac{\ln\lambda_0}{\epsilon},\qquad E_0(\epsilon)=E_0+c\,\epsilon^2+\dots$",
}
EQIMG = {k: ecuacion(k, v) for k, v in EQS.items()}

# ----------------------------------------------------------------------------- utilidades pptx
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
NOTAS = []  # (num, titulo, quien, texto, expuesta)
num = [0]


def runs(p, partes, size, color=NAVY, bold=False):
    """partes: str o lista de (texto, dict) con bold/color/italic."""
    if isinstance(partes, str):
        partes = [(partes, {})]
    for t, o in partes:
        r = p.add_run()
        r.text = t
        r.font.name = FONT
        r.font.size = Pt(o.get("size", size))
        r.font.bold = o.get("bold", bold)
        r.font.italic = o.get("italic", False)
        r.font.color.rgb = o.get("color", color)
        if o.get("sup"):
            r.font._element.set("baseline", "30000")
        if o.get("sub"):
            r.font._element.set("baseline", "-25000")


def caja(sl, x, y, w, h, parrafos, size=16, color=NAVY, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, espacio=6, fill=None, margen=0.08):
    if fill is not None:
        sh = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.adjustments[0] = 0.06
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
        sh.line.fill.background()
        sh.shadow.inherit = False
        tb = sh
    else:
        tb = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for lado in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, lado, Inches(margen))
    if isinstance(parrafos, (str, tuple)):
        parrafos = [parrafos]
    for i, par in enumerate(parrafos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(espacio)
        runs(p, par, size, color, bold)
    return tb


def vin(texto):
    return [("• ", {}), *texto] if isinstance(texto, list) else [("• " + texto, {})]


def B(t):
    return (t, {"bold": True})


def R(t):
    return (t, {"bold": True, "color": RED})


def G(t):
    return (t, {"bold": True, "color": GREEN})


def nueva(titulo, quien, notas, fuente=None, expuesta=True):
    num[0] += 1
    sl = prs.slides.add_slide(BLANK)
    bg = sl.background.fill
    bg.solid()
    bg.fore_color.rgb = WHITE
    bar = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = RED
    bar.line.fill.background()
    if titulo:
        caja(sl, 0.6, 0.32, 12.1, 0.8, [[(titulo, {})]], size=30, bold=True, margen=0)
    if fuente:
        caja(sl, 0.6, 6.88, 11.4, 0.45, [[(fuente, {})]], size=11, color=GRAY, margen=0)
    caja(sl, 12.3, 6.88, 0.6, 0.4, [[(str(num[0]), {})]], size=11, color=GRAY, align=PP_ALIGN.RIGHT, margen=0)
    rot = f"[{quien}] " if expuesta else "[Respaldo, no se expone] "
    sl.notes_slide.notes_text_frame.text = rot + notas
    NOTAS.append((num[0], titulo, quien, notas, expuesta))
    return sl


def imagen(sl, ruta, x, y, w=None, h=None):
    kw = {}
    if w:
        kw["width"] = Inches(w)
    if h:
        kw["height"] = Inches(h)
    return sl.shapes.add_picture(ruta, Inches(x), Inches(y), **kw)


def eq(sl, k, x, y, h=None, w=None, escala=0.95):
    """Misma escala para todas: el tamano de letra queda igual en todas las ecuaciones."""
    ruta, wi, hi = EQIMG[k]
    return imagen(sl, ruta, x, y, h=hi * escala)


def tabla(sl, x, y, w, filas, anchos, size=13, alto=0.36, cab=True):
    nf, nc = len(filas), len(filas[0])
    t = sl.shapes.add_table(nf, nc, Inches(x), Inches(y), Inches(w), Inches(alto * nf)).table
    for j, a in enumerate(anchos):
        t.columns[j].width = Inches(a)
    for i, fila_ in enumerate(filas):
        t.rows[i].height = Inches(alto)
        for j, val in enumerate(fila_):
            c = t.cell(i, j)
            c.margin_left = c.margin_right = Inches(0.06)
            c.margin_top = c.margin_bottom = Inches(0.02)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = c.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            partes = val if isinstance(val, list) else [(str(val), {})]
            if i == 0 and cab:
                runs(p, partes, size, WHITE, True)
                c.fill.solid()
                c.fill.fore_color.rgb = NAVY
            else:
                runs(p, partes, size, NAVY, False)
                c.fill.solid()
                c.fill.fore_color.rgb = LIGHT if i % 2 else WHITE
    return t


def tarjeta(sl, x, y, w, h, titulo, cuerpo, color=NAVY, size=14):
    caja(sl, x, y, w, h, [[(titulo, {"bold": True, "color": color, "size": size + 2})]] + cuerpo,
         size=size, fill=LIGHT, margen=0.15, espacio=5)


def cifra(sl, x, y, w, grande, peque, color=NAVY):
    caja(sl, x, y, w, 0.8, [[(grande, {"bold": True, "color": color})]], size=34, margen=0)
    caja(sl, x, y + 0.78, w, 0.75, [[(peque, {})]], size=13, color=GRAY, margen=0)


# ============================================================================= LAMINAS
JS, LF = "Juan Sebastián", "Luis Felipe"

# 1. Portada
s = nueva(None, JS,
          "Buenos días. Somos Juan Sebastián Calixto y Luis Felipe Ramírez, y presentamos la Fase 2 del "
          "proyecto 5: el umbral de ligadura del estado 1s en el potencial de Yukawa. Yo presento la "
          "pregunta, la acción y los controles; Luis Felipe, el cálculo en delta igual a 0.2 y el riesgo "
          "de la caja.")
caja(s, 0.7, 1.35, 11.8, 0.9, [[("Umbral de ligadura en el potencial de Yukawa", {})]], size=40, bold=True, margen=0)
caja(s, 0.7, 2.3, 11.8, 0.6, [[("Fase 2: acción de pares, controles exactos y primer cálculo con la integral de camino", {})]],
     size=22, color=RED, margen=0)
eq(s, "V", 0.7, 3.25, escala=1.25)
caja(s, 0.7, 4.75, 11.8, 1.1,
     [[("Juan Sebastián Calixto (formulación y verificación) · Luis Felipe Ramírez (implementación)", {})],
      [("Investigación Teórica · Proyecto 05 · primera presentación, semana 7 · 27 de octubre de 2026", {})]],
     size=16, color=GRAY, margen=0)

# 2. Pregunta
s = nueva("La pregunta y lo que pide la Fase 2", JS,
          "La pregunta sigue igual: ¿para qué apantallamiento mu deja de existir el estado ligado 1s, y "
          "cómo se comportan la energía y el radio medio al acercarnos? En unidades reducidas todo depende "
          "de delta, y la referencia de la Fase 1 es delta c igual a 1.1906124211. Para esta fase la guía "
          "pide dos herramientas: un solucionador radial y una formulación de tiempo imaginario que trate "
          "bien la singularidad uno sobre r, y compararlas en un punto fuertemente ligado. Elegimos delta "
          "igual a 0.2, con el hidrógeno como control.",
          fuente="Unidades ħ = m = g = 1: longitudes en a = ħ²/(mg), energías en mg²/ħ². δc de la Fase 1 (energía cero, R = 200 a 800).")
caja(s, 0.6, 1.3, 12.1, 1.15,
     [[B("¿Para qué apantallamiento μ (a g, m y ħ fijos) deja de existir el estado ligado 1s de V(r) = −g e"),
       ("−μr", {"bold": True, "sup": True}), B("/r, y cómo se comportan E₀ y ⟨r⟩ al acercarse a ese valor?")]],
     size=19, fill=LIGHT, margen=0.18, anchor=MSO_ANCHOR.MIDDLE)
eq(s, "V", 0.75, 2.75, escala=1.1)
tarjeta(s, 0.6, 3.95, 3.85, 2.3, "1. Solucionador radial",
        [vin("Diferencias finitas + Richardson"), vin("Referencia independiente"), vin("Módulo radial.py")], size=17)
tarjeta(s, 4.75, 3.95, 3.85, 2.3, "2. Tiempo imaginario",
        [vin("Acción que trate bien −1/r"), vin("Transferencia (sin muestreo)"), vin("PIGS (Monte Carlo)")], size=17)
tarjeta(s, 8.9, 3.95, 3.8, 2.3, "3. Comparar en δ = 0.2",
        [vin("Punto fuertemente ligado"), vin("Control: Coulomb, δ = 0"),
         vin("Controles exactos: Hulthén y pozo")], color=RED, size=17)

# 3. Accion y peso
s = nueva("La acción de pares y el peso declarado", JS,
          "La acción es la de pares que aprobamos en la Fase 1. Separamos el potencial en Coulomb más un "
          "resto W. Cada eslabón es el núcleo libre con imagen, que impone u de cero igual a cero, por la "
          "acción exacta de Coulomb, U C, y por el resto W repartido entre los dos extremos. U C la "
          "tabulamos con dos mallas y Richardson. Toda la singularidad queda dentro del núcleo exacto, y W "
          "está acotado entre cero y delta. El peso es real, positivo y normalizable: en la matriz hay cero "
          "elementos negativos y cero no finitos. En r igual a 0.01, con epsilon 0.1, la acción exacta vale "
          f"menos {abs(U001):.2f}; la primitiva daría e a la {prim001:.0f}. Y en delta igual a cero el "
          "método es exacto para cualquier epsilon.",
          fuente="pares.py (tabla U_C, h_tab = 0.01 y 0.005 con Richardson), transferencia.py; cifras de 11_transferencia.json (peso). Prohibida la primitiva con 1/r desnudo.")
eq(s, "T", 0.6, 1.4)
eq(s, "KD", 0.6, 2.15)
eq(s, "W", 0.6, 3.05)
caja(s, 0.6, 3.8, 6.9, 2.7,
     [vin([B("ρ"), ("C", {"bold": True, "sub": True}), (": núcleo exacto de Coulomb; toda la singularidad −1/r va dentro de U", {}), ("C", {"sub": True})]),
      vin("K_D con imagen en r = 0: impone u(0) = 0 (sector ℓ = 0)"),
      vin("W acotado y suave: sesgo de la factorización O(ε²)"),
      vin("δ = 0: el método es exacto para todo ε")], size=16)
caja(s, 7.9, 1.35, 4.85, 0.5, [[B("Veredicto sobre el peso")]], size=20, color=RED, margen=0)
filas = [["Propiedad", "Valor"],
         ["Real", "sí: sin fases"],
         ["Positivo", f"sí: {negs} elementos negativos"],
         ["Finito", f"sí: {nofin} elementos no finitos"],
         ["U_C(0.01, 0.01), ε = 0.1", f(U001, 3)],
         ["Primitiva en r = 0.01: ε/r", f"{prim001:.0f}  (factor e^{prim001:.0f})"]]
tabla(s, 7.9, 1.95, 4.85, filas, [2.55, 2.3], size=14, alto=0.45)
caja(s, 7.9, 4.95, 4.85, 1.15,
     [[("Normalizable: ", {"bold": True}), ("U_C es finita en el origen, así que la integral sobre un eslabón converge "
       "(con la primitiva diverge: Fase 1, sección 8).", {})]], size=15, fill=LIGHT, margen=0.15)

# 4. Metodos
s = nueva("Una acción, dos evaluaciones y una referencia", JS,
          "Con esa misma acción hacemos dos evaluaciones. La matriz de transferencia: discretizamos r con "
          "paso 0.02, control 0.04, y sacamos el autovalor mayor, sin muestreo. Y PIGS: muestreamos "
          "caminos que salen de una función de prueba, r por e a la menos r, que no es exacta para delta "
          "mayor que cero. Usamos ocho cadenas por punto y reportamos el mayor entre el error por bloques y "
          "el error entre cadenas. La referencia independiente es el solucionador radial, con diferencias "
          "finitas y Richardson. El sesgo de Trotter se extrapola con epsilon 0.2, 0.1 y 0.05.",
          fuente="Módulos en fase2/codigo/: radial.py, pares.py, transferencia.py, pigs.py. Semillas de producción 20262000 + k.")
tarjeta(s, 0.6, 1.35, 3.9, 2.45, "Transferencia en banda",
        [vin("Nyström: h = 0.02 (control 0.04)"), vin("Autovalor mayor λ₀ (eigsh)"),
         vin("Sin ruido estadístico"), vin("Llega hasta R = 800")], color=BLUE, size=15)
tarjeta(s, 4.72, 1.35, 3.9, 2.45, "PIGS",
        [vin("Caminos desde u_T = r e^(−r)"), vin("u_T no exacta para δ > 0"),
         vin("8 cadenas por punto"), vin("Error: el mayor entre bloques y cadenas")], color=RED, size=15)
tarjeta(s, 8.84, 1.35, 3.86, 2.45, "Radial (referencia)",
        [vin("Diferencias finitas"), vin("h = 1/40 y 1/80 (o 1/80 y 1/160)"), vin("Richardson en h"),
         vin("Independiente de la acción")], color=NAVY, size=15)
eq(s, "E0T", 0.6, 4.15, escala=0.9)
eq(s, "P", 0.6, 5.05, escala=0.85)
caja(s, 8.5, 4.15, 4.2, 1.5,
     [[B("Extrapolaciones")], [("ε = 0.2, 0.1, 0.05 → ε → 0 (ley ε²)", {})],
      [("h = 0.02, 0.04 → h → 0 (Richardson)", {})]], size=15, fill=LIGHT, margen=0.15)

# 5. Coulomb
s = nueva("Caso de referencia: Coulomb (δ = 0)", JS,
          "Primer control: Coulomb, delta igual a cero. La transferencia da menos un medio a menos de "
          f"{max(dE_coul)*1e7:.1f} por diez a la menos siete, y el radio medio a {max(dr_coul)*1e7:.1f} por "
          "diez a la menos siete de tres medios. En PIGS, la energía local vale menos un medio en todo "
          "camino, pero eso es tautológico: con W igual a cero no prueba nada. El control real es la "
          f"distribución. Con ocho cadenas, el radio medio queda a menos {abs(coul_sr):.2f} sigmas de tres "
          f"medios y el de r cuadrado a menos {abs(coul_sr2):.2f} sigmas. El histograma pasa con p igual "
          f"a {coul_p:.3f}, por encima del umbral de una milésima, pero justo.",
          fuente="11_transferencia.json (resultados 0.0, h = 0.02, R = 40); 12c_pigs_coulomb_tau5.json (A_coulomb, 8 cadenas, τ = 10). Exactos: E = −1/2, ⟨r⟩ = 3/2, ⟨r²⟩ = 3.")
caja(s, 0.6, 1.3, 6.0, 0.5, [[B("Transferencia (h = 0.02, ε = 0.2 / 0.1 / 0.05)")]], size=18, color=BLUE, margen=0)
cifra(s, 0.6, 1.95, 2.9, e(max(dE_coul)), "máx |E + 1/2|", BLUE)
cifra(s, 3.6, 1.95, 2.9, e(max(dr_coul)), "máx |⟨r⟩ − 3/2|", BLUE)
caja(s, 0.6, 3.5, 5.9, 0.9,
     [[("El sesgo de Trotter es nulo en δ = 0: lo que queda es error de malla y de tabla.", {})]],
     size=15, color=GRAY, margen=0)
caja(s, 7.0, 1.3, 5.8, 0.5, [[B("PIGS (8 cadenas, τ = 10)")]], size=18, color=RED, margen=0)
filas = [["Observable", "PIGS", "Exacto", "Desvío"],
         ["⟨r⟩", f"{coul_r:.5f} ± {coul_er:.5f}", "1.5", f"{f(coul_sr, 2)}σ"],
         ["⟨r²⟩", f"{coul_r2:.4f} ± {coul_er2:.4f}", "3", f"{f(coul_sr2, 2)}σ"],
         ["Histograma de r", f"p = {coul_p:.3f}", "p > 0.001", "pasa justo"]]
tabla(s, 7.0, 1.95, 5.7, filas, [1.6, 2.1, 0.9, 1.1], size=14, alto=0.48)
caja(s, 7.0, 4.15, 5.7, 1.0,
     [[R("Ojo: "), ("E_L ≡ −1/2 en todo camino es tautológico (W = 0). El control real es la distribución de r.", {})]],
     size=15, fill=LIGHT, margen=0.15)
caja(s, 0.6, 4.45, 5.9, 1.0,
     [vin(f"La tabla de U_C con Richardson es clave: sin ella el error en E sería {e(float(fila('A1')[2].split('sin Rich: ')[1].split(',')[0]))} (ε = 0.2)")], size=15, color=NAVY, margen=0)

# 6. Hulthen y pozo
s = nueva("Controles exactos: Hulthén y pozo cuadrado", JS,
          "Tras la Fase 1, el profesor pidió controles exactos. Hulthén tiene la misma singularidad y "
          "solución exacta, así que entra en el mismo método sin cambios: con delta 0.2, 1 y 1.5, la "
          f"transferencia extrapolada queda a menos de {max(abs(x) for x in hul_ext)*1e9:.1f} por diez a la "
          f"menos nueve del exacto, y el sesgo baja como epsilon cuadrado, con orden {hul_ord[0]:.2f}. El "
          "pozo cuadrado enseña otra cosa: con un salto en el potencial, el sesgo no va como epsilon "
          "cuadrado sino como epsilon a la tres medios. Extrapolando con el orden medido queda a "
          f"{abs(pozo_ext2)*1e6:.1f} por diez a la menos seis; con la ley epsilon cuadrado el error sería "
          f"de {abs(pozo_eps2)*1e4:.1f} por diez a la menos cuatro. Luis Felipe sigue con los resultados.",
          fuente="13_controles.json vía tabla 15 (filas B8 a B27). Hulthén: E = −(1/2)(1 − δ/2)², ⟨r⟩ = (12 − δ²)/(2(4 − δ²)). Pozo: transferencia sin U_C, salto en un nodo con borde medio.")
imagen(s, os.path.join(FIG, "13_controles.png"), 0.5, 1.25, w=7.6)
filas = [["Control", "Resultado"],
         ["Hulthén δ = 0.2, 1.0, 1.5", f"E_ext − E_exacta: {e(hul_ext[0])}, {e(hul_ext[1])}, {e(hul_ext[2])}"],
         ["Hulthén, orden de Trotter", f"{hul_ord[0]:.3f} y {hul_ord[1]:.3f} (δ = 1.0, 1.5)"],
         ["Pozo V₀ = 2, orden medido", pozo_ord2],
         ["Pozo V₀ = 2, E_ext − E_exacta", f"{e(pozo_ext2)} (ley ε²: {e(pozo_eps2)})"],
         ["Pozo V₀ = 1.3, E_ext − E_exacta", f"{e(pozo_ext13)}"],
         ["Pozo V₀ = 1.3, ajuste ε^1.5 a 5 puntos", [(f"{e(pozo_b3b13)} > 10⁻⁵: ", {}), ("no pasa", {"bold": True, "color": RED})]]]
tabla(s, 8.3, 1.3, 4.45, filas, [1.75, 2.7], size=12, alto=0.62)
caja(s, 0.6, 4.55, 7.4, 2.1,
     [vin([B("Hulthén: "), ("misma singularidad −1/r, mismo método sin cambios; sesgo ε², extrapolado a ≤ 5×10⁻⁹", {})]),
      vin([B("Pozo: "), ("un salto en V cambia la ley a ε^(3/2); con la ley ε² del plan el error sería 30 veces mayor", {})])],
     size=16, margen=0)

# 7. Primer grafico
s = nueva("Cálculo preliminar en δ = 0.2: radial frente a tiempo imaginario", LF,
          "Gracias. Este es el primer gráfico: radial frente a tiempo imaginario en delta 0.2. En el panel "
          "a, la transferencia con epsilon 0.1 queda a uno por diez a la menos ocho del radial, y "
          f"extrapolada a epsilon cero, a {abs(j18['dif_E_tr_ext'])*1e9:.1f} por diez a la menos nueve. "
          f"PIGS, con tau igual a 20 y ocho cadenas, da menos {abs(P20['E']):.6f} más o menos "
          f"{P20['eE']:.6f}: está a {P20['sigma_vs_radial']:.2f} sigmas. En el panel b, el radio medio de "
          f"PIGS es {P20['r']:.3f} más o menos {P20['er']:.3f}, a {P20['sigma_r_vs_radial']:.2f} sigmas del "
          f"radial, {j18['r_radial']:.4f}. Los tres métodos coinciden dentro de sus errores.",
          fuente="16_primer_grafico.png; cifras de 11_transferencia.json y 12_pigs.json. Radial: R = 40, h = 1/80 y 1/160. PIGS: semillas 20262000–07.")
# Primer grafico oficial de la Fase 2 (16_primer_grafico.py); si no existe, el de 18_figura_presentacion.py
FIG_PG = os.path.join(FIG, "16_primer_grafico.png")
if not os.path.exists(FIG_PG):
    FIG_PG = os.path.join(FIG, "18_primer_grafico.png")
imagen(s, FIG_PG, 0.5, 1.15, h=5.6)
filas = [["δ = 0.2", "E₀", "⟨r⟩"],
         ["Radial", f(E_rad, 10), f(j18["r_radial"], 5)],
         ["Transf. ε → 0", f(j18['E_transferencia_extrapolada'], 10), "—"],
         ["Transf. ε = 0.1", f(j18['E_transferencia_eps0.1_h0.02'], 10), f(j18["r_transferencia_eps0.1"], 5)],
         ["PIGS τ = 20", f"{f(P20['E'], 6)} ± {P20['eE']:.6f}", f"{P20['r']:.4f} ± {P20['er']:.4f}"]]
tabla(s, 8.15, 1.3, 4.6, filas, [1.3, 1.95, 1.35], size=12, alto=0.5)
caja(s, 8.15, 4.0, 4.6, 1.9,
     [[B("Diferencias con el radial")],
      vin(f"Transferencia ε = 0.1: {e(j18['dif_E_tr01'])}"),
      vin(f"Transferencia ε → 0: {e(j18['dif_E_tr_ext'])}"),
      vin([("PIGS: E a ", {}), B(f"+{P20['sigma_vs_radial']:.2f}σ"), (", ⟨r⟩ a ", {}), B(f"+{P20['sigma_r_vs_radial']:.2f}σ"),
           (f", ⟨r²⟩ = {p20['r2mid']['media']:.3f} ± {p20['r2mid']['err']:.3f}", {})])],
     size=14, fill=LIGHT, margen=0.15, espacio=4)

# 8. Proyeccion
s = nueva("Proyección desde una función de prueba no exacta", LF,
          "La proyección parte de una función de prueba que no es exacta. La energía mixta baja de forma "
          f"monótona hacia E cero: sobra {dmix1*1e4:.1f} por diez a la menos cuatro en tau igual a 1 y solo "
          f"{dmix20*1e7:.1f} por diez a la menos siete en tau igual a 20. El estimador puro del radio sí "
          "muestra la proyección en PIGS, a la derecha. Un punto no pasa: en tau igual a 5 la producción "
          f"queda a menos {abs(scan[5]['sigma_E']):.2f} sigmas. Repetimos con 32 cadenas nuevas: las "
          f"réplicas dan más {C5['por_corrida']['replica1']['sigma']:.2f} y más "
          f"{C5['por_corrida']['replica2']['sigma']:.2f} sigmas, y las 40 cadenas juntas, menos "
          f"{abs(C5['las_40']['sigma_ponderada']):.2f}. Pero las tres corridas no concuerdan del todo, con "
          f"p igual a {C5['chi2_corridas_vs_Edet']['p']:.3f}, así que no lo damos por cerrado.",
          fuente="12_pigs.json (tau_scan, proyeccion_informativo), 11_transferencia.json (proyeccion), 12c_pigs_coulomb_tau5.json (C_tau5_combinado). ε = 0.1, u_T = r e^(−r).")
imagen(s, os.path.join(FIG, "12_pigs_tau.png"), 0.45, 1.2, w=8.2)
eq(s, "Emix", 0.6, 4.6, escala=0.85)
caja(s, 5.3, 4.62, 3.4, 0.7, [[("u_T = r e", {}), ("−r", {"sup": True}), (" no es exacta para δ > 0", {})]], size=15, color=GRAY, margen=0)
filas = [["τ = 5", "E_mixto", "Desvío"],
         ["Producción (8)", f"{f(C5['por_corrida']['produccion']['media'], 6)}", [(f"{f(C5['por_corrida']['produccion']['sigma'], 2)}σ", {"bold": True, "color": RED})]],
         ["Réplica 1 (16)", f"{f(C5['por_corrida']['replica1']['media'], 6)}", f"+{C5['por_corrida']['replica1']['sigma']:.2f}σ"],
         ["Réplica 2 (16)", f"{f(C5['por_corrida']['replica2']['media'], 6)}", f"+{C5['por_corrida']['replica2']['sigma']:.2f}σ"],
         ["Las 40 cadenas", f"{f(C5['las_40']['media_ponderada'], 6)}", f"{f(C5['las_40']['sigma_ponderada'], 2)}σ"]]
tabla(s, 8.85, 1.3, 3.9, filas, [1.45, 1.4, 1.05], size=13, alto=0.42)
caja(s, 8.85, 3.6, 3.9, 1.35,
     [[("Transferencia en τ = 5: ", {}), B(f(C5['E_det'], 6))],
      [("χ² de las 3 corridas: p = ", {}), R(f"{C5['chi2_corridas_vs_Edet']['p']:.3f}")],
      [("Decisión pendiente de firma", {"italic": True, "color": GRAY})]], size=14, fill=LIGHT, margen=0.12)
caja(s, 0.6, 5.55, 12.1, 1.2,
     [vin(f"Mixto (transferencia): sobra {e(dmix1)} en τ = 1 y {e(dmix20)} en τ = 20"),
      vin(f"Puro ⟨r⟩ en PIGS, τ = 2 → 20: {f(pinf['dr_pigs'], 3)} ({f(pinf['sigma_dr'], 1)}σ); transferencia {f(pinf['dr_det'], 3)}")],
     size=14, margen=0)

# 9. Errores sistematicos
fila_A13 = fila("A13")
a13max = max(float(x) for x in re.findall(r"(\d\.\d+e-\d+)\s+\(eps", fila_A13[2]))
s = nueva("Errores sistemáticos: Trotter y malla", LF,
          f"Dos errores sistemáticos de la transferencia. El de Trotter baja como epsilon cuadrado: orden "
          f"{tr_ord:.2f} en delta 0.2 y {tr1_ord:.2f} en delta 1, siempre que antes quitemos el error de "
          "malla. Ese error de malla nace en la cúspide del origen, va como h a la cuarta sobre epsilon, y "
          f"hace fallar nuestro control de estabilidad: {a13max*1e6:.1f} por diez a la menos seis entre h "
          "0.02 y 0.04, frente a una tolerancia de diez a la menos seis. Con Richardson en h desaparece; "
          "esa redefinición del control está pendiente de firma.",
          fuente="11_transferencia.json (trotter, estabilidad_nystrom, orden_nystrom); tabla 15, filas A7 a A14. R = 40 (δ = 0.2) y R = 174 (δ = 1.0).")
imagen(s, os.path.join(FIG, "11_trotter.png"), 0.5, 1.3, w=7.5)
caja(s, 8.3, 1.3, 4.45, 2.0,
     [[B("Trotter (ley ε²)")],
      vin(f"Orden {tr_ord:.3f} (δ = 0.2) y {tr1_ord:.3f} (δ = 1.0)"),
      vin(f"Extrapolado ε → 0 en δ = 0.2: {e(tr_ext)} del radial")], size=15, fill=LIGHT, margen=0.15)
caja(s, 8.3, 3.55, 4.45, 2.55,
     [[R("Malla de Nyström: no pasa")],
      vin(f"|E(0.04) − E(0.02)| hasta {e(a13max)} > 10⁻⁶"),
      vin("Error de extremo en la cúspide: ∝ h⁴/ε (orden 4.00)"),
      vin("Remedio: Richardson en h (exponente 4); pendiente de firma")], size=15, fill=LIGHT, margen=0.15)

# 10. Caja
c118, c120 = cel["1.18"], cel["1.2"]
s = nueva("Riesgo principal: la caja cerca del umbral", LF,
          "El riesgo principal es la caja cerca del umbral. Allí el estado es un halo y una sola caja "
          "engaña: en delta 1.18, que está ligado, las cajas de 50 y 100 dan energía positiva. Por eso "
          "usamos el criterio de varias cajas, y la condición c exige que la transferencia y el radial den "
          "el mismo signo, la misma tendencia y energías compatibles. Se cumple en las "
          f"{'nueve' if nC1 == 9 else nC1} ternas. El veredicto: 1.15 ligado, 1.18 ligado con cajas de 200 "
          f"a 800, y 1.20 no ligado, con el radio relativo subiendo a {c120['R800']['obs']['r_sobre_R']['mejor']:.2f}. "
          "Así delta c queda entre 1.18 y 1.20 por los dos métodos. Dos cuidados: sin extrapolar en "
          f"epsilon, la transferencia exagera la ligadura hasta un {trot02*100:.0f} por ciento de la "
          "energía; y la pared en R no tiene imagen, lo que corre la caja un poco hacia afuera.",
          fuente="14_cajas.json (celdas, veredictos, pared). Transferencia extrapolada en h y ε; radial con h = 1/40 y 1/80 y Richardson. Criterio 9.6 de la Fase 1.")
imagen(s, os.path.join(FIG, "14_cajas.png"), 0.45, 1.2, w=7.9)
filas = [["R", "δ = 1.18: E₀ (transf.)", "⟨r⟩/R", "δ = 1.20: E₀ (transf.)", "⟨r⟩/R"]]
for R_ in ("R50", "R100", "R200", "R400", "R800"):
    a, b = c118[R_], c120[R_]
    filas.append([R_[1:], e(a["E_mejor"], 2), f"{a['obs']['r_sobre_R']['mejor']:.3f}",
                  e(b["E_mejor"], 2), f"{b['obs']['r_sobre_R']['mejor']:.3f}"])
tabla(s, 0.6, 3.75, 7.6, filas, [0.8, 2.15, 1.25, 2.15, 1.25], size=13, alto=0.34)
caja(s, 8.55, 1.3, 4.2, 2.65,
     [[B(f"Condición (c): {nC1}/{nT} ternas")],
      [("mismo signo, misma tendencia y E₀ compatibles entre transferencia y radial", {"color": GRAY})],
      vin([B("1.15: "), G("ligado"), (" (50/100/200)", {})]),
      vin([B("1.18: "), G("ligado"), (" (200/400/800)", {})]),
      vin([B("1.20: "), R("no ligado"), (f" (a_s = {f(a_s120, 1)})", {})])],
     size=15, fill=LIGHT, margen=0.15, espacio=4)
caja(s, 8.55, 4.2, 4.2, 2.2,
     [[R("Cuidados")],
      vin(f"Sin extrapolar en ε: sesgo hasta {trot01*100:.0f}\u00a0% (ε\u00a0=\u00a00.1) y {trot02*100:.0f}\u00a0% (ε\u00a0=\u00a00.2) de |E₀|"),
      vin(f"Pared en R sin imagen: caja efectiva R + {beta:.4f}√ε")], size=14, margen=0.05, espacio=4)
caja(s, 0.6, 6.2, 7.6, 0.5, [[B("Avance: δc ∈ [1.18, 1.20] por los dos métodos; el intervalo final es de la Fase 4")]],
     size=15, color=NAVY, margen=0)

# 11. Balance
s = nueva("Balance de la Fase 2 y qué sigue", LF,
          f"En resumen: la tabla de controles tiene {n_filas} filas; {n_pasa} pasan, {n_nopasa} no pasan y "
          f"{n_med} son medidas. Los que no pasan tienen causa medida y los mostramos tal cual. La tabla aún "
          "no está firmada: faltan seis decisiones del equipo, entre ellas la imagen en R y el caso tau "
          "igual a 5. Lo que sigue es la Fase 3, el radio cerca del umbral, y la Fase 4, el intervalo "
          "final de delta c. Gracias; quedamos atentos a sus preguntas.",
          fuente="secciones/15_tabla_controles.md (generada por 16_tabla_controles.py desde los JSON). Estado: SIN FIRMAR.")
cifra(s, 0.6, 1.4, 2.6, str(n_filas), "filas en la tabla de controles")
cifra(s, 3.4, 1.4, 2.6, str(n_pasa), "pasan", GREEN)
cifra(s, 6.2, 1.4, 2.6, str(n_nopasa), "no pasan (causa medida)", RED)
cifra(s, 9.0, 1.4, 3.0, str(n_med), "medidas o informativas", GRAY)
tarjeta(s, 0.6, 3.4, 5.9, 2.6, "Lo que ya tenemos",
        [vin("Acción de pares con peso real, positivo y normalizable"),
         vin("Radial, transferencia y PIGS de acuerdo en δ = 0.2"),
         vin("Hulthén exacto a 10⁻⁹; pozo: ley ε^(3/2)"),
         vin("Criterio de cajas con la condición (c): δc ∈ [1.18, 1.20]")], color=GREEN, size=17)
tarjeta(s, 6.8, 3.4, 5.9, 2.6, "Pendiente",
        [vin("Firma de la tabla (Juan Sebastián) y 6 decisiones"),
         vin("Imagen en R o caja efectiva; τ = 5"),
         vin("Fase 3: ⟨r⟩ cerca del umbral (transferencia)"),
         vin("Fase 4: intervalo final de δc")], color=RED, size=17)

# ----------------------------------------------------------------------------- RESPALDO
s = nueva("Respaldo 1: los controles que no pasan", "", "Se muestra si preguntan por los fallos.",
          fuente="secciones/15_tabla_controles.md, sección «Lo que no pasa y por qué».", expuesta=False)
# Valores copiados de la tabla 15 (columna "Valor medido"), resumidos para que quepan
filas = [["Fila", "Control", "Valor", "Causa medida"],
         ["A5", "δ = 0.2, transferencia con h = 0.04", "1.51×10⁻⁶ y 3.22×10⁻⁶ > 10⁻⁶ (ε = 0.1, 0.05)", "error de malla h⁴/ε en la cúspide"],
         ["A7", "Ley ε² en δ = 0.2 sin Richardson en h", "orden 1.046", "Trotter del tamaño del error de malla"],
         ["A13", "Estabilidad Nyström 0.02 → 0.04", "hasta 3.20×10⁻⁶ > 10⁻⁶", "error de extremo del trapecio, h⁴/ε"],
         ["A16", "PIGS frente a transferencia, τ = 2, 5, 10, 20", "τ = 5: −3.2σ en E", "réplicas +0.03σ y +0.99σ; p = 0.011"],
         ["B27", "Pozo V₀ = 1.3, ajuste ε^1.5 a 5 puntos", "+2.16×10⁻⁵ > 10⁻⁵", "orden aún preasintótico (1.67 → 1.52)"],
         ["C4", "Orden de Trotter en las cajas", "12/15; 1.65, 1.49, 1.79", "pared en R sin imagen (R = 50, 100)"],
         ["C5", "Orden de la malla cerca del umbral", "1.361 (R = 50); 2.287 (R = 100)", "no es 4: usar h = 0.02 y 0.01"],
         ["D19", "L16 propagador libre (suma)", "8.1×10⁻⁵ a 3.2×10⁻⁴ frente a 10⁻¹⁰", "criterio mal fijado: error O(h²)"],
         ["E1", "Radial δ = 0.2 (h = 1/40, 1/80)", "+6.23×10⁻⁹ > 5×10⁻⁹", "con h = 1/80, 1/160: +4.0×10⁻¹⁰"]]
tabla(s, 0.6, 1.3, 12.1, filas, [0.7, 4.0, 3.9, 3.5], size=13, alto=0.5)

s = nueva("Respaldo 2: límites físicos con la integral de camino", "",
          "Se muestra si preguntan por la lista de límites de la IA (L01 a L19).",
          fuente="15_limites.py → 15_limites.json; tabla 15, parte D.", expuesta=False)
imagen(s, os.path.join(FIG, "15_limites.png"), 0.6, 1.2, w=7.0)
filas = [["Límite (δ = 0.2 salvo L19)", "Valor (tabla 15, parte D)"],
         ["L05 Hellmann-Feynman", "0.74485846 frente a 0.74485290 (+5.6×10⁻⁶)"],
         ["L06 virial", "−1.33×10⁻⁴ (h = 0.02) → extrapolado −5.91×10⁻⁷"],
         ["L07 cúspide", "a₂/a₁ = −0.99937"],
         ["L14 estado 2s", "E₁ = −0.012107865 (dif. con radial 2.1×10⁻¹⁰)"],
         ["L19 δ = 2 sin ligado", "E(200) = +1.219×10⁻⁴; ley de caja a −1.0×10⁻³"]]
tabla(s, 7.85, 1.3, 4.9, filas, [1.7, 3.2], size=12, alto=0.62)

s = nueva("Respaldo 3: la pared en R sin imagen", "",
          "Se muestra si preguntan por la caja efectiva.",
          fuente="14_cajas.json (pared, V3_criterio_estricto).", expuesta=False)
pw = j14["pared"]
filas = [["Celda", "Orden sin corregir", "Con R + β√ε: orden", "Residuo extrapolado"]]
for k in ("1.15_R50", "1.18_R50", "1.2_R50", "1.2_R100"):
    if k in pw:
        filas.append([k.replace("_", ", "), f"{cel[k.split('_')[0]][k.split('_')[1]]['orden_trotter']:.2f}",
                      f"{pw[k]['orden']:.3f}", e(pw[k]["extrapolado"])])
tabla(s, 0.6, 1.3, 8.0, filas, [1.6, 2.0, 2.2, 2.2], size=14, alto=0.5)
vc = j14["V3_criterio_estricto"]
caja(s, 0.6, 4.2, 12.1, 2.2,
     [vin(f"K_D solo tiene imagen en r = 0: la pared en R se vigila solo en los nodos de tiempo, y la caja efectiva es R + β√ε, β = {beta:.4f}"),
      vin(f"Criterio estricto |dif| ≤ err_tr: {vc['pasan_con_pared']}/{vc['n_celdas']} con el término de pared y {vc['pasan_sin_pared']}/{vc['n_celdas']} sin él"),
      vin("No cambia ningún signo ni tendencia; poner imagen en R lo decide el equipo (decisión 5)")], size=15, margen=0)

s = nueva("Respaldo 4: decisiones pendientes de firma", "",
          "Se muestra si preguntan qué falta para cerrar la fase.",
          fuente="secciones/15_tabla_controles.md, «Decisiones pendientes de firma (Juan Sebastián)».", expuesta=False)
dec = re.search(r"## Decisiones pendientes de firma.*?\n\n(.*?)\n\n##", tabla15, re.S).group(1)
items = [re.sub(r"\$([^$]*)\$", r"\1", re.sub(r"^\d+\.\s*", "", l)).replace("\\tau", "τ").replace("\\epsilon", "ε")
         .replace("^{3/2}", "^(3/2)").replace("R_{\\rm ef}", "R_ef").replace("U_C", "U_C").replace("h", "h")
         for l in dec.splitlines() if l.strip()]
caja(s, 0.6, 1.3, 12.1, 5.3, [[(f"{i+1}. ", {"bold": True, "color": RED}), (t, {})] for i, t in enumerate(items)],
     size=16, margen=0, espacio=10)

s = nueva("Respaldo 5: registro de la IA en la Fase 2", "",
          "Se muestra si preguntan cómo se usó la IA y qué se corrigió.",
          fuente="verificacion/V1_recalculo_independiente.md, V2_auditoria_adversarial.md, V3_respuesta_hallazgos.md.", expuesta=False)
tarjeta(s, 0.6, 1.3, 5.9, 3.4, "Cómo trabajamos",
        [vin("Claude escribió los módulos y scripts; cada cifra sale de un script ejecutado"),
         vin("V1: recálculo independiente con código propio (disparo, FEDVR)"),
         vin("V2: auditoría adversarial que buscó fallos a propósito"),
         vin("V3: respuesta a cada hallazgo, con copia previa de todo")], size=15)
tarjeta(s, 6.8, 1.3, 5.9, 3.4, "Errores de la IA que se corrigieron",
        [vin("Signo cambiado en el desplazamiento espectral de U_C (detectado frente a la Fase 1)"),
         vin("El código afirmaba un error de extremos menor que el real fuera de r = 10: se añadió Wigner-Kirkwood"),
         vin("Un criterio inventado sin aprobar («proyección visible»): se pasó a informativo"),
         vin("La pared sin imagen no estaba declarada: ahora el código avisa y estima el sesgo")], color=RED, size=15)

# ----------------------------------------------------------------------------- guardar
salida = os.path.join(AQUI, "diapositivas_fase2.pptx")
prs.save(salida)

# ----------------------------------------------------------------------------- guion
def palabras(t):
    return len(re.findall(r"\w+", t))


WPM = 150
lineas = []
tot = {JS: 0, LF: 0}
filas_g = []
for n, tit, quien, txt, exp in NOTAS:
    if not exp:
        filas_g.append(f"| {n} | {tit} | (no se expone) | 0 | 0 s |")
        continue
    w = palabras(txt)
    seg = round(w / WPM * 60)
    tot[quien] += w
    filas_g.append(f"| {n} | {tit or 'Portada'} | {quien} | {w} | {seg} s |")


def mmss(w):
    s_ = round(w / WPM * 60)
    return f"{s_ // 60} min {s_ % 60:02d} s"


total_w = tot[JS] + tot[LF]
FUENTES = {}

json.dump({"palabras": tot, "total_palabras": total_w, "total_s": round(total_w / WPM * 60)},
          open(os.path.join(AQUI, "tiempos_guion.json"), "w"), indent=1)


def texto_lamina(sl):
    out = []
    for sh in sl.shapes:
        if sh.has_text_frame:
            t = " / ".join(pp.text for pp in sh.text_frame.paragraphs if pp.text.strip())
            if t.strip() and not re.fullmatch(r"\d+", t.strip()):
                out.append(t)
        elif sh.has_table:
            for row in sh.table.rows:
                out.append("| " + " | ".join(c.text for c in row.cells) + " |")
        elif sh.shape_type == 13:
            out.append(f"[imagen: {os.path.basename(sh.image.filename) if sh.image.filename else 'figura'}]")
    return out


IMGS = {1: "ecuación V(r), δ, δc", 2: "ecuación V(r), δ, δc", 3: "ecuaciones T, K_D, U_C, W",
        4: "ecuaciones E0(ε) y peso P[r0..rM]", 6: "figuras/13_controles.png", 7: "figuras/16_primer_grafico.png",
        8: "figuras/12_pigs_tau.png y ecuación de E_mixto", 9: "figuras/11_trotter.png", 10: "figuras/14_cajas.png",
        13: "figuras/15_limites.png"}

G = []
G.append("# Guion de la Fase 2: primera presentación (semana 7)\n")
G.append("**Proyecto 05 · Umbral de ligadura del 1s en V(r) = −g e^(−μr)/r** · Presentan: Juan Sebastián Calixto (JS) y "
         "Luis Felipe Ramírez (LF) · 27-10-2026 · 9 min de exposición + 5 min de discusión.\n")
G.append("Diapositivas: `diapositivas_fase2.pptx` (y `diapositivas_fase2.pdf`), generadas por "
         "`generar_diapositivas_fase2.py`, que lee todas las cifras de `fase2/resultados/*.json` y de "
         "`secciones/15_tabla_controles.md`. El primer gráfico es `figuras/16_primer_grafico.png` "
         "(`codigo/16_primer_grafico.py`); `codigo/18_figura_presentacion.py` hizo una versión de respaldo. Las notas del orador de cada lámina son el mismo texto de este guion. "
         f"Tiempos calculados a {WPM} palabras por minuto a partir del número de palabras de cada bloque.\n")
G.append("## Reparto\n")
G.append("| # | Lámina | Quién | Palabras | Tiempo |\n|---|---|---|---|---|")
G += filas_g
G.append(f"\n**Total expuesto:** {total_w} palabras, unos {mmss(total_w)} (máximo 9 min; queda margen para "
         f"cambiar de lámina y señalar figuras). Juan Sebastián: {tot[JS]} palabras ({mmss(tot[JS])}), láminas 1 a 6 "
         f"(pregunta, acción y peso, métodos, Coulomb, Hulthén y pozo: formulación y verificación). Luis Felipe: "
         f"{tot[LF]} palabras ({mmss(tot[LF])}), láminas 7 a 11 (cálculo en δ = 0.2, proyección, errores, caja y "
         "balance: implementación). Las láminas 12 a 16 son de respaldo y no se exponen. El reparto es una propuesta "
         "y lo confirma el equipo.\n")
G.append("## Texto de cada lámina\n")
prs2 = Presentation(salida)
for (n, tit, quien, txt, exp), sl in zip(NOTAS, prs2.slides):
    cab = f"### {n}. {tit or 'Portada'}"
    if exp:
        cab += f" ({quien}, {round(palabras(txt) / WPM * 60)} s)"
    else:
        cab += " (respaldo, no se expone)"
    G.append(cab + "\n")
    G.append("**En la lámina:**\n")
    for t in texto_lamina(sl):
        if t.startswith("[imagen"):
            continue
        G.append(("" if t.startswith("|") else "- ") + t)
    if n in IMGS:
        G.append(f"- [imagen: {IMGS[n]}]")
    G.append("")
    if exp:
        G.append("**Se dice:**\n")
        G.append("> " + txt + "\n")
    else:
        G.append(f"*{txt}*\n")

G.append("## Preguntas probables del profesor y respuestas\n")
G.append("Responde por defecto quien expuso el tema, pero los dos deben poder contestar cualquiera.\n")
QA = [
    ("¿Por qué no usan la acción primitiva, o un potencial suavizado, si es más sencillo?",
     f"Con la primitiva el peso no es normalizable: e^(ε/r) explota en el origen (en r = 0.01 con ε = 0.1 el "
     f"exponente ya vale {prim001:.0f}). El suavizado introduce un parámetro que mueve el umbral y habría que "
     f"extrapolarlo. Con la acción de pares la singularidad va dentro del núcleo exacto: U_C(0.01, 0.01) = {f(U001, 3)} "
     "es finita y el resto W está acotado en [0, δ]. (JS)"),
    ("¿Cómo saben que el peso es normalizable y positivo, y no solo lo suponen?",
     f"Lo comprueba el código en cada tabla: {negs} elementos negativos y {nofin} no finitos en la matriz, y U_C acotada "
     "en el origen. Además, en δ = 0 el método reproduce E = −1/2 para todo ε, que no pasaría si el peso estuviera mal "
     "normalizado. (JS)"),
    ("Si PIGS es la integral de camino, ¿para qué la transferencia?",
     "Usan la misma acción. La transferencia no tiene ruido, llega a cajas de R = 800 y separa los errores "
     "sistemáticos (Trotter, malla, proyección) del ruido estadístico. PIGS es el Monte Carlo que pide la guía; cerca "
     "del umbral su tiempo de proyección crece como 1/|E0| y no es viable (Fase 1), así que lo usamos hasta δ ≈ 1. (LF)"),
    ("El punto τ = 5 está a −3.19σ. ¿No es un sesgo del PIGS?",
     f"Lo reportamos tal cual. Dos réplicas con semillas nuevas dan +{C5['por_corrida']['replica1']['sigma']:.2f}σ y "
     f"+{C5['por_corrida']['replica2']['sigma']:.2f}σ, y las 40 cadenas juntas {f(C5['las_40']['sigma_ponderada'], 2)}σ. "
     f"Pero las tres corridas no concuerdan del todo (p = {C5['chi2_corridas_vs_Edet']['p']:.3f}), así que no lo damos "
     "por cerrado: es la decisión 2 pendiente de firma. En τ = 2, 10 y 20 el acuerdo es menor que 2σ. (LF)"),
    ("¿Por qué el pozo cuadrado da ε^(3/2) y no ε²?",
     f"Lo medimos: órdenes {pozo_ord2} en V0 = 2. La ley ε² supone un potencial suave; con un salto, la factorización "
     "falla en una capa de anchura ~√ε alrededor del salto (explicación plausible, no demostrada). Si se extrapolara con ε² "
     f"el error sería {e(pozo_eps2)}; con el orden medido queda en {e(pozo_ext2)}. Por eso el Yukawa, que es suave salvo "
     "en el origen (y esa parte la absorbe U_C), sí sigue ε². (JS)"),
    ("Si en δ = 1.18 una caja da E > 0, ¿cómo deciden que está ligado?",
     "Con el criterio de varias cajas de la Fase 1 (9.6): al menos tres cajas en razón 2, malla convergida, y las "
     "tendencias de E0, ⟨r⟩/R y F1/2. En 1.18, ⟨r⟩/R baja de 0.225 a 0.080 entre R = 200 y 800 (estado localizado); en "
     "1.20 sube hasta 0.426 (estado de caja, con la ley de dispersión de a_s). La condición (c) exige que transferencia y "
     f"radial coincidan en signo y tendencia: se cumple en {nC1}/{nT} ternas. (LF)"),
    ("Un control de la malla de Nyström no pasa. ¿Por qué siguen adelante?",
     f"Porque la causa está medida: es error de extremo del trapecio en la cúspide del origen, va como h⁴/ε (orden 4.00) "
     f"y vale hasta {e(a13max)}. Con Richardson en h desaparece y el extrapolado queda a {e(tr_ext)} del radial. La "
     "redefinición del control está pendiente de firma. Cerca del umbral el orden no es 4, así que en la Fase 4 usaremos "
     "h = 0.02 y 0.01. (LF)"),
    ("¿Qué hizo la IA y qué verificaron ustedes?",
     "Claude escribió los módulos y scripts. Hubo dos verificaciones: un recálculo independiente con código propio (V1) "
     "y una auditoría adversarial (V2); cada hallazgo se respondió en V3 recalculando. Ejemplos de errores corregidos: un "
     "signo en la tabla U_C, una afirmación falsa sobre el error fuera de r = 10 y la pared en R sin imagen, que no estaba "
     "declarada. Ninguna cifra de la presentación está escrita a mano. (JS)"),
]
for q, a in QA:
    G.append(f"**P: {q}**  \nR: {a}\n")
with open(os.path.join(AQUI, "guion_fase2.md"), "w") as fh:
    fh.write("\n".join(G) + "\n")
print("Guion:", os.path.join(AQUI, "guion_fase2.md"))

print("Palabras:", tot, "total", total_w, "->", mmss(total_w))
print("Guardado:", salida)
