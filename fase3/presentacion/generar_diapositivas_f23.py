"""generar_diapositivas_f23.py -- Presentacion de las Fases 2 y 3 (proyecto 05), 11-11-2026, 15 min, dos expositores.
Construye diapositivas_fase2_3.pptx (python-pptx) y guion_fase2_3.md. Cifras leidas de fase3/resultados/*.json y
fase2/resultados/*.json. Estilo de las Fases 1 y 2: 16:9, Calibri, titulos 1B2A41, acento C0392B."""
import json, os
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

AQUI = os.path.dirname(os.path.abspath(__file__))
F3 = os.path.dirname(AQUI); F2 = os.path.join(os.path.dirname(F3), "fase2")
J3 = lambda n: json.load(open(os.path.join(F3, "resultados", n)))
J2 = lambda n: json.load(open(os.path.join(F2, "resultados", n)))
NAVY, RED, GRAY, LIGHT, WHITE = (RGBColor(0x1B, 0x2A, 0x41), RGBColor(0xC0, 0x39, 0x2B), RGBColor(0x55, 0x5F, 0x6B),
                                 RGBColor(0xF2, 0xF4, 0xF7), RGBColor(0xFF, 0xFF, 0xFF))
FONT = "Calibri"

CJ, B, CV, F119, T24 = J3("20_cajas.json"), J3("21_barrido.json"), J3("22_convergencia.json"), J3("20c_umbral_119_fino.json"), J3("24_tabla_controles.json")
cnt = T24["cuenta"]
r119 = F119["radial"]["R25600"]
c119 = CJ["celdas"]["1.19"]
A = B["ajuste_kappa"]["A"]

prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BL = prs.slide_layouts[6]
GUION = []


def caja(s, x, y, w, h, texto, size=18, color=NAVY, bold=False, fill=None):
    if fill is not None:
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill; sh.line.fill.background(); tf = sh.text_frame
    else:
        tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    lineas = texto if isinstance(texto, list) else [texto]
    for i, l in enumerate(lineas):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        b = bold
        if l.startswith("**"):
            l, b = l.strip("*"), True
        r = p.add_run(); r.text = l
        r.font.size, r.font.name, r.font.bold, r.font.color.rgb = Pt(size), FONT, b, color
        p.space_after = Pt(6)
    return tf


def lamina(titulo, quien, notas, bullets=None, img=None, img_w=None, bx=0.6, bw=None, tag=None, abajo=False):
    s = prs.slides.add_slide(BL)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.0))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    caja(s, 0.5, 0.15, 11.0, 0.8, titulo, 28, WHITE, True)
    if tag:
        caja(s, 11.3, 0.25, 1.9, 0.5, tag, 14, WHITE, True, fill=RED)
    if abajo:
        from PIL import Image
        W, H = Image.open(img).size
        h = 7.5 - 1.25 - 0.55 - (0.42 * len(bullets) + 0.35)
        w = min(12.6, h * W / H); h = w * H / W
        caja(s, 0.6, 1.2, 12.3, 0.42 * len(bullets) + 0.3, ["• " + b if not b.startswith("**") else b for b in bullets], 17, NAVY)
        s.shapes.add_picture(img, Inches((13.333 - w) / 2), Inches(6.95 - h), width=Inches(w))
        bullets, img = None, None
    if bullets:
        caja(s, bx, 1.25, bw or (5.6 if img else 12.0), 5.8, ["• " + b if not b.startswith("**") else b for b in bullets], 17, NAVY)
    if img:
        w = img_w or 6.9
        s.shapes.add_picture(img, Inches(13.333 - w - 0.35), Inches(1.3), width=Inches(w))
    caja(s, 0.5, 7.0, 9, 0.4, f"Proyecto 05 · Fases 2 y 3 · {quien}", 11, GRAY)
    s.notes_slide.notes_text_frame.text = notas
    GUION.append((titulo, quien, notas))
    return s


fig2 = lambda n: os.path.join(F2, "figuras", n)
fig3 = lambda n: os.path.join(F3, "figuras", n)
JS, LF = "Juan Sebastián", "Luis Felipe"

# 1 portada
s = prs.slides.add_slide(BL)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height); bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
caja(s, 0.8, 1.6, 11.5, 1.4, "Umbral de ligadura en el potencial de Yukawa", 40, WHITE, True)
caja(s, 0.8, 2.9, 11.5, 1.2, "Fases 2 y 3: acción de pares, controles exactos, barrido en el apantallamiento y prueba de cajas", 22, WHITE)
caja(s, 0.8, 4.4, 11.5, 1.6, ["V(r) = −g e^(−μr)/r   ·   δ = μħ²/(mg)   ·   referencia δc = 1.1906124211",
                             "Juan Sebastián Calixto · Luis Felipe Ramírez", "Introducción a la Investigación Teórica · 11 de noviembre de 2026"], 18, WHITE)
n1 = ("Buenos días. Somos Juan Sebastián y Luis Felipe, proyecto 05. La pregunta es en qué apantallamiento deja de existir el estado ligado 1s del potencial de Yukawa. "
      "Todo depende de un número, delta igual a mu por h barra al cuadrado sobre m g. Hoy mostramos las Fases 2 y 3: cómo calculamos con una integral de camino que trata bien la singularidad, cómo la validamos y qué dice el barrido cerca del umbral.")
s.notes_slide.notes_text_frame.text = n1; GUION.append(("Portada", JS, n1))

lamina("La pregunta y lo que traíamos de la Fase 1", JS,
       "En la Fase 1 adimensionalizamos, acotamos el umbral entre 1.19055 y 1.24305 con cotas variacional y de Bargmann, y obtuvimos la referencia 1.1906124211 por integración a energía cero. "
       "Vimos dos riesgos. Primero, la integral de camino ingenua no sirve con menos uno sobre r: el peso crece como e a la épsilon sobre r y no es normalizable. Segundo, cerca del umbral el estado se vuelve enorme y una caja finita puede inventar la conclusión. "
       "Por eso diseñamos un criterio que compara varias cajas y mira si el estado está localizado, no solo el signo de la energía.",
       ["Ecuación radial (ℓ = 0): −u''/2 − e^(−δr)/r · u = E u, u(0) = u(R) = 0",
        "Cotas analíticas: 1.19055 ≤ δc ≤ 1.24305 (variacional, Bargmann)",
        "Referencia numérica: δc = 1.1906124211",
        "Riesgo 1: la acción primitiva da peso e^(ε/r), no normalizable",
        "Riesgo 2: cerca del umbral el estado es más grande que la caja",
        "**Fase 2: dos métodos que coincidan en un punto fuertemente ligado. Fase 3: barrer μ y la caja, convergencia temporal y auditoría de autovalores cercanos a cero."])

lamina("La acción de pares: la singularidad va en la parte exacta", JS,
       "Separamos el potencial en Coulomb más un resto W, que es suave y está entre cero y delta. El eslabón de tiempo imaginario es el núcleo libre con una imagen en el origen, por el factor exacto de Coulomb, por el resto repartido mitad y mitad. "
       "Toda la singularidad queda en la parte exacta, que se tabula una vez. El precio es un error de Trotter de orden épsilon al cuadrado, que eliminamos extrapolando. "
       "La guía pide declarar el peso: es real, positivo, con cero elementos negativos, y normalizable, porque U_C es finita en el origen. No suavizamos el potencial. "
       "Lo evaluamos de dos formas: como matriz de transferencia, sin ruido, y como Monte Carlo PIGS.",
       ["V = −1/r + W(r),  W = (1 − e^(−δr))/r ∈ [0, δ]",
        "T(r,r';ε) = K_D · e^(−U_C) · e^(−ε[W(r)+W(r')]/2)",
        "U_C: acción de pares EXACTA de Coulomb (tabulada)",
        "Sesgo de Trotter O(ε²) → extrapolación ε → 0",
        "Peso real, positivo (0 negativos) y normalizable (U_C(0.01,0.01) = −1.13; la primitiva daría e²⁰)",
        "Dos evaluaciones: matriz de transferencia (E0 = −ln λ0/ε) y PIGS (Monte Carlo)",
        "Referencia: solucionador radial de diferencias finitas"])

lamina("Fase 2: los tres métodos coinciden en δ = 0.2", JS,
       "Este es el primer gráfico. En delta igual a 0.2 el radial da menos 0.3268085110. La transferencia, extrapolada en épsilon y en la malla, queda a 4 milmillonésimas, y su error baja como épsilon al cuadrado: orden medido 1.96. "
       "El PIGS coincide dentro de su barra de error en las tres magnitudes: 1.2, 0.6 y 0.4 sigma. "
       "El panel d muestra la proyección en tiempo imaginario: un punto, tau igual a 5, salió a menos 3.2 sigma. Lo repetimos dos veces y salió bien, pero las tres corridas juntas tienen p de 1 por ciento. No lo borramos: queda abierto.",
       ["Radial: E0 = −0.3268085110, ⟨r⟩ = 1.5497",
        "Transferencia extrapolada: +4.4×10⁻⁹; orden de Trotter 1.96",
        "PIGS (τ = 20): +1.2σ (E), +0.6σ (⟨r⟩), +0.4σ (⟨r²⟩)",
        "τ = 5: −3.2σ; réplicas +0.03σ y +0.99σ; las tres corridas p ≈ 0.011 → queda abierta"],
       img=fig2("18_primer_grafico.png"), tag="Fase 2", abajo=True)

lamina("Fase 2: controles con solución exacta", JS,
       "Para confiar en el código lo probamos con problemas cuya respuesta se conoce. Coulomb, delta igual a cero: el método es exacto y solo queda error de malla, 2 por 10 a la menos 7. "
       "Hulthén tiene la misma singularidad y la misma cola que el Yukawa y su energía es exacta: pasa por el mismo código sin cambiar nada y da la energía exacta a 10 a la menos 9, hasta tres cuartos del camino a su umbral. Es nuestro control más fuerte; la fuente es Cai, Cai e Inomata 1986. "
       "El pozo cuadrado, con un salto, da Trotter de orden 3 medios: enseña que el método depende de la suavidad del potencial, no de la singularidad. Lo usamos como control cualitativo.",
       ["Coulomb (δ = 0): |E + 1/2| ≤ 2.2×10⁻⁷ (solo malla)",
        "Hulthén (misma singularidad, exacto): error ≤ 5×10⁻⁹ en δ = 0.2, 1.0, 1.5; orden 1.99",
        "Pozo cuadrado (salto): Trotter ε^(3/2) → control cualitativo",
        "Verificación: recálculo independiente (227/252 cifras, resto explicado), auditoría adversarial y auditoría con Gemini (otro modelo): sin errores de física",
        f"Tabla de controles Fase 2: 82 controles, 64 pasan, 9 no pasan con causa medida, 9 medidos"],
       img=fig2("13_controles.png"), img_w=6.3, bw=6.2, tag="Fase 2")

lamina("Fase 3: qué pide la guía y qué fijamos antes de calcular", LF,
       "La guía pide para la Fase 3 barrer mu y el tamaño de caja, estudiar la convergencia temporal y pedir a una IA una auditoría adversarial de autovalores cercanos a cero. "
       "Antes de ver ningún dato fijamos tres cosas. El umbral de la ley de caja para declarar no ligado: 0.1. La receta de extrapolación: Richardson en h con exponente 4 y épsilon al cuadrado. Y que la pared en R, que en el núcleo no tiene imagen, no se corrige: se mide y se suma a la barra de error. "
       "Cambiamos los roles: ahora implementa Juan Sebastián y verifica Luis Felipe.",
       ["Guía (proyecto 05): barrer μ y R, convergencia temporal, auditoría adversarial de autovalores cercanos a cero",
        "**Fijado antes de ver los datos (decisiones del equipo):",
        "Umbral de la ley de caja para \"no ligado\": 0.1",
        "Richardson en h (exponente 4) y extrapolación ε²",
        "Pared en R sin imagen: se mide (R + 0.5826√ε) y va a la barra de error",
        "**Criterio de cajas (terna R1 < R2 < R3): ligado si E < 0 estable, ⟨r⟩/R ↓ y F½ → 1; no ligado si E > 0, ⟨r⟩/R ↑ y E sigue π²/[2(R − a_s)²]; (c) los dos métodos dan el mismo veredicto"], tag="Fase 3")

lamina("Convergencia temporal y espacial", LF,
       "Primero, convergencia. Medimos el error en cuatro deltas, con cuatro pasos de tiempo y tres mallas. El error de Trotter baja con pendiente 2 en todos los casos, de 1.96 a 1.99, y el de la malla con pendiente 4. "
       "El dato importante es que el sesgo crece hacia el umbral: con épsilon 0.1 es 4 diezmillonésimas de la energía en delta 0.2 y casi el 1 por ciento en 1.15. Sin extrapolar, cerca del umbral llega al 20 por ciento y siempre hacia abajo, o sea, podría fabricar un estado ligado. "
       "Extrapolado, el resultado queda a menos de 5 por 10 a la menos 9 del radial en los cuatro casos.",
       ["Orden de Trotter: 1.96–1.99 (δ = 0.2 a 1.15)",
        "Orden de la malla Nyström: 4.00",
        "Sesgo con ε = 0.1: 4×10⁻⁷ |E0| (δ = 0.2) → 7×10⁻³ |E0| (δ = 1.15)",
        "Sin extrapolar, hasta 20 % de |E0| cerca del umbral, hacia abajo: falso \"ligado\"",
        "Extrapolado − radial: ≤ 5×10⁻⁹ en los 4 casos"],
       img=fig3("23_convergencia.png"), tag="Fase 3", abajo=True)

P = [p for p in B["puntos"] if "tr" in p]
lamina("Barrido en el apantallamiento: E0(δ) y ⟨r⟩(δ)", LF,
       "El barrido en delta, que es barrer mu a g fijo. A la izquierda la energía: los dos métodos coinciden en los ocho valores con diferencia máxima de 2 por 10 a la menos 8. En el centro la extensión: el radio medio pasa de 1.5 a más de mil al acercarse al umbral. "
       f"A la derecha, kappa, la raíz de menos dos E, frente a la distancia al umbral: es una recta, kappa igual a {A:.3f} por delta c menos delta. Eso quiere decir que la energía se anula cuadráticamente, y radio medio por kappa tiende a un medio: el estado es su cola exponencial. Este es el avance de la Fase 4.",
       [f"{len(P)} valores de δ: transferencia = radial (máx. dif. 1.8×10⁻⁸)",
        "⟨r⟩: 1.55 (δ = 0.2) → 1102 (δ = 1.19)",
        f"Cerca del umbral: κ ≈ {A:.3f} (δc − δ) → E0 ∝ −(δc − δ)²",
        "⟨r⟩κ → 1/2: domina la cola e^(−κr)"],
       img=fig3("23_barrido_delta.png"), tag="Fase 3", abajo=True)

lamina("Prueba de cajas cerca del umbral", LF,
       "Ahora la prueba de cajas: cinco deltas y siete cajas, de 50 a 3200. En las 35 celdas la integral de camino coincide con el radial. "
       "1.15 y 1.18 salen ligados; 1.20 y 1.25, no ligados: en 1.20 la energía sigue la ley de una partícula libre en la caja con longitud de dispersión menos 143. "
       "Fíjense en 1.18, la curva verde: con cajas de 50 o 100 la energía es positiva y habríamos dicho no ligado. Con 200 a 800 se ve que está ligado. Por eso no basta el signo.",
       ["35/35 cajas: integral de camino compatible con el radial",
        "δ = 1.15 y 1.18: ligados; δ = 1.20 y 1.25: no ligados",
        "δ = 1.18 con R ≤ 100: E > 0 → habría parecido \"no ligado\"",
        "δ = 1.20: ley de caja con a_s = −142.9, desviación 0.021",
        "**Hasta R = 3200, con los dos métodos y (c): 1.18 < δc < 1.20 (δ = 1.19 en la lámina siguiente)"],
       img=fig3("23_cajas.png"), tag="Fase 3", abajo=True)

lamina("Un autovalor cercano a cero: δ = 1.19", LF,
       "El caso difícil es 1.19, a seis diezmilésimas del umbral. Con caja 1600 la energía es positiva; con 3200 es negativa, y los dos métodos coinciden en las dos. ¿Es un estado o un artefacto? "
       "Lo decide la localización. Con el radial en cajas hasta 25600, la energía se estabiliza en menos 1.03 por 10 a la menos 7, el radio relativo baja de 0.23 a 0.04 y la fracción interior sube a 0.99999. El estado mide unas 1100 unidades, del orden de la longitud de dispersión, 2204: esa es la escala que la caja tiene que superar. "
       "Y la integral de camino también llega: cambiando el solucionador de autovalores por una factorización en banda, la evaluamos en cajas de 6400 y 12800. Los dos métodos dan ligado en la terna 3200, 6400, 12800 y la condición (c) se cumple: delta c está entre 1.19 y 1.20 con los dos métodos.",
       ["R = 1600: E0 = +1.5×10⁻⁷  ·  R = 3200: E0 = −7.1×10⁻⁸ (los dos métodos)",
        f"Radial hasta R = 25600: E0 → {r119['E0']:.3e}, ⟨r⟩ = {r119['r_med']:.0f}",
        "Integral de camino (LU en banda, N = 640 000): E0(6400) = −1.00×10⁻⁷, E0(12800) = −1.01×10⁻⁷, compatibles",
        "Terna 3200/6400/12800: ligado con los dos métodos, (c) se cumple; ⟨r⟩/R 0.23 → 0.09, F½ 0.90 → 0.997",
        "Escala que la caja debe superar: a_s = +2204; sin caja ni malla: a_s cambia de signo entre δ = 1.1906 y 1.1907",
        "**Dos métodos y (c): 1.19 < δc < 1.20"],
       img=fig3("23_delta119.png"), tag="Fase 3", abajo=True)

lamina("Controles de la Fase 3 y auditoría con otra IA", LF,
       f"La tabla de controles de la Fase 3 tiene {len(T24['filas'])} controles distintos: {cnt['sí']} pasan, {cnt['**no**']} no pasan y {cnt['medido']} son medidos. Los tres que no pasan tienen causa medida. "
       "El más interesante: el orden de Trotter sale bajo en las cajas donde el estado toca la pared; al comparar con el radial en la caja corrida 0.58 raíz de épsilon vuelve a 1.99 en las nueve celdas probadas. "
       "La auditoría adversarial de los autovalores cercanos a cero se la pedimos a Gemini 3.1 Pro, un modelo distinto de Claude, como pide el profesor; nos dio siete hallazgos y comprobamos cada uno calculando. Seis no se sostienen: por ejemplo, decía que la malla fabricaba el estado ligado, pero el sesgo de la malla va hacia arriba y una integración sin malla da la misma energía. El séptimo era válido: la condición (c) no llegaba a cajas mayores de 3200. Lo resolvimos con la integral de camino en 6400 y 12800.",
       [f"{len(T24['filas'])} controles: {cnt['sí']} pasan, {cnt['**no**']} no pasan (causa medida), {cnt['medido']} medidos",
        "Orden de Trotter bajo en cajas que tocan la pared → 1.98–1.99 con la pared corregida (9/9)",
        "Perron-Frobenius en las 210 matrices; cotas analíticas y E0(δ) creciente",
        "Auditoría adversarial con Gemini 3.1 Pro: 7 hallazgos, cada uno comprobado calculando",
        "6 refutados (p. ej. malla: el sesgo va hacia arriba y el disparo sin malla da −1.0303×10⁻⁷); 1 válido: faltaba (c) en R > 3200 → resuelto",
        "Regla: un desacuerdo se resuelve calculando, no votando"], tag="Fase 3")

lamina("Conclusiones y qué sigue", JS,
       "En resumen. La acción de pares trata exactamente la singularidad con un peso real, positivo y normalizable, y reproduce los controles exactos a 10 a la menos 9. "
       "Con los dos métodos y el criterio de cajas, delta c está entre 1.19 y 1.20, compatible con la referencia; la solución a energía cero lo afina a entre 1.1906 y 1.1907. "
       "Lo que separa un estado débil de un artefacto es comparar cajas y mirar la localización, no el signo de un autovalor. "
       "Para la Fase 4: estudiar la ley de la extensión, cerrar la anomalía del PIGS y escribir el artículo; ya tenemos el borrador. Gracias.",
       ["Acción de pares: singularidad exacta, peso real, positivo y normalizable",
        "Controles exactos (Coulomb, Hulthén) a ~10⁻⁹",
        "**1.19 < δc < 1.20 (dos métodos y (c)) · 1.1906 < δc < 1.1907 (energía cero) · ref. 1.19061",
        "Caja y paso temporal son los sistemáticos dominantes: se controlan comparando cajas y extrapolando",
        "Fase 4: ley de ⟨r⟩(δ), PIGS cerca del umbral y τ = 5, artículo final"])

# respaldo
lamina("Respaldo: tabla de veredictos", "(respaldo)", "",
       ["δ = 1.15: ligado (50/100/200)", "δ = 1.18: ligado (200/400/800)", "δ = 1.19: indeterminado con R ≤ 3200; ligado con los dos métodos (3200/6400/12800)",
        "δ = 1.20: no ligado (200/400/800), desviación de la ley de caja 0.382 → 0.101 → 0.021", "δ = 1.25: no ligado (50/100/200)",
        "Condición (c): 24/25 ternas (la que falla: δ = 1.15 con F½ = 1 saturado, ruido 10⁻¹⁶)"], tag="Respaldo")
lamina("Respaldo: lo que no pasa y por qué", "(respaldo)", "",
       ["A8 (c) 24/25: tendencia de F½ cuando F½ = 1 (redondeo)",
        "A9 orden de Trotter fuera de [1.8, 2.2] en cajas que tocan la pared → A10: 1.98–1.99 con R + 0.5826√ε",
        "D1 δ = 0.2: sesgo de Trotter ~10⁻⁹ del tamaño del residuo de la tabla U_C",
        "Fase 2: τ = 5 del PIGS (p ≈ 1 %) sigue abierta; tabla de la Fase 2 con 6 filas repetidas (82 controles distintos)"], tag="Respaldo")
lamina("Respaldo: uso de IA", "(respaldo)", "",
       ["Cálculo y redacción: Claude (Anthropic), dirigido por el equipo",
        "Decisiones humanas: umbral 0.1, pared en el error, Richardson h⁴ (fijadas antes de los datos)",
        "Verificación: recálculo independiente, auditoría adversarial interna, auditoría externa con Gemini (Flash por API y 3.1 Pro en la app)",
        "Gemini no ejecuta código en la app y dio referencias de memoria: ninguna entra sin verificar en la fuente",
        "Registro: fecha, consulta literal, respuesta usada, decisión humana, comprobación, corrección"], tag="Respaldo")

out = os.path.join(AQUI, "diapositivas_fase2_3.pptx"); prs.save(out)
pal = lambda t: len(t.split())
g = ["# Guion de la presentación de las Fases 2 y 3", "", "Proyecto 05 · 11 de noviembre de 2026 · 15 minutos · Juan Sebastián Calixto (JS) y Luis Felipe Ramírez (LF).",
     "Tiempos a 140 palabras por minuto. Las notas del orador de cada lámina tienen el mismo texto.", "", "| # | Lámina | Quién | Palabras | Tiempo |", "|---|---|---|---|---|"]
tot = {}
for i, (t, q, n) in enumerate(GUION, 1):
    w = pal(n); tot[q] = tot.get(q, 0) + w
    g.append(f"| {i} | {t} | {q} | {w} | {w/140*60:.0f} s |")
T = sum(v for k, v in tot.items() if k != "(respaldo)")
g += ["", f"**Total expuesto:** {T} palabras, unos {T/140:.1f} min (de 15; queda margen para señalar figuras y para preguntas). "
      + ", ".join(f"{k}: {v} palabras ({v/140:.1f} min)" for k, v in tot.items() if k != "(respaldo)") + ".", ""]
for i, (t, q, n) in enumerate(GUION, 1):
    if n:
        g += [f"## {i}. {t} ({q})", "", n, ""]
g += ["## Preguntas probables", "",
      "- **¿Por qué no basta el signo de la energía?** Porque en δ = 1.18 con R ≤ 100 y en δ = 1.19 con R ≤ 1600 el signo es positivo y el estado sí está ligado: lo que decide es comparar cajas y mirar ⟨r⟩/R y F½.",
      "- **¿Cómo llegó la integral de camino a R = 12800?** La factorización dispersa del modo shift-invert con N ≈ 320 000 y 313 diagonales no cabía en memoria. La matriz es de banda, así que usamos LU en banda de LAPACK e iteración inversa: misma acción y misma receta, solo cambia el álgebra lineal. R = 12800 (N = 640 000) tarda unos 3 minutos.",
      "- **¿Cómo saben que δ = 1.19 no es un artefacto de la malla?** El sesgo de la malla va hacia arriba (h = 1/40 da E > 0), así que puede esconder un ligado pero no inventarlo. Una integración sin malla ni caja da E0 = −1.0303×10⁻⁷, y la solución a energía cero tiene un nodo en r ≈ a_s = 2204.",
      "- **¿Qué hizo la IA y qué ustedes?** La IA calculó y redactó; nosotros fijamos la pregunta, el plan y las decisiones (umbral 0.1 antes de los datos, pared en el error), revisamos y firmamos. Gemini auditó.",
      "- **¿Qué pasa con τ = 5?** Sigue abierta (p ≈ 1 %); no se borró la corrida. Se estudia con la autocorrelación en la Fase 4.",
      "- **¿Por qué Hulthén?** Tiene la misma singularidad y la misma cola, y su energía es exacta: prueba el método completo donde sabemos la respuesta."]
open(os.path.join(AQUI, "guion_fase2_3.md"), "w").write("\n".join(g) + "\n")
print(out, tot, T)
