# Revisión adversarial independiente de E3 (revisor R3, 17-11-2026)

Revisé `CONTEXTO_COMUN.md` y toda la carpeta `E3_otros_perfiles/`: los once scripts, los JSON, las salidas y los seis
textos. Rehíce la teoría a mano y, en los puntos que lo admitían, también con sympy. Recalculé todo con un método
distinto, escrito desde cero, y verifiqué las fuentes en la web. Usé un solo proceso. Los scripts de esta carpeta son:

| Script | Qué hace | Tiempo |
|---|---|---|
| `r01_numerov.py` | Numerov de paso fijo desde r = 0 (numba) con Richardson h → h/2, Simpson para las integrales, ∂V/∂δ por diferencias (E3 la usa analítica). No importa nada de E3. | ~3 s |
| `r02_camino_ecsc.py` | Integral de camino del ECSC con otra pareja (h, ε): h ∈ {0.01, 0.03} y ε ∈ {0.05, 0.025}. Usa las tablas de pares ya guardadas, solo para leerlas (no escribe fuera de E3). La referencia es la caja calculada con Numerov. | ~20 s |
| `r03_teoria_simbolica.py` | sympy: Hulthén exacto, punto fijo a segundo orden, fórmula del cruce, cota de W del ECSC. | ~5 s |

**Veredicto:** no encontré errores numéricos ni de signo. Todas las cifras de E3 se reproducen con el método
independiente a 10⁻⁸ o mejor. Los hallazgos son de presentación, de fuentes y de rigor en un argumento, y los
corregí todos dentro de E3, salvo R3-07 y R3-08, que solo quedan anotados.

## Tabla de hallazgos

| ID | Gravedad | Descripción | Evidencia | Corrección |
|---|---|---|---|---|
| R3-01 | menor | La tabla 1 de la sección escribía las cifras de Roy como 1.19061 y 0.720524. Roy imprime 1.190610 y 0.7205240, pero `float()` en `09_textos.py` borraba el cero final. El texto sí decía "las 7 de Roy (0.7205240)", así que se contradecía con la tabla. | Lectura de arXiv:1904.11166, tabla I. | `09_textos.py` ahora escribe las cifras tal como están impresas. Regenerado. |
| R3-02 | menor | La columna "segundo método" de la tabla 1 muestra la variante posterior U2b (`delta_B2_post_hoc`) sin marcarla. El valor preregistrado del ECSC difiere en 5.5×10⁻⁷. El párrafo siguiente sí lo aclaraba. | `01_umbrales.json`: `delta_B` frente a `delta_B2_post_hoc`. | El encabezado dice ahora "segundo método (variante posterior U2b)". |
| R3-03 | moderada (rigor) | El texto decía "La causa es su zona repulsiva" de r_e < 0, como si el sobrepaso de φ₀ sobre 1 bastara. El sobrepaso es **necesario**: si V ≤ 0, entonces φ₀'' = 2Vφ₀ ≤ 0 con φ₀' → 0, así que φ₀ crece hacia 1 sin pasarlo y r_e(δ_c) = 2∫(1 − φ₀²) > 0. Pero **no es suficiente**: que el área con φ₀ > 1 pese más que la zona cercana al origen es un hecho numérico, no una consecuencia del signo. | Demostración arriba. Numerov da φ₀,max = 1.1562027 en δr = 1.023 (E3: 1.1562), r_e = −0.40996389. | Párrafo reescrito en `09_textos.py`: teorema para V ≤ 0, "necesario, no suficiente". E3 estuvo de acuerdo. |
| R3-04 | mejora | E3 presentaba "r_e = 3/δ_c" y "κ_v = δ/2 − 1" del Hulthén como observaciones sin referencia. Las dos son exactas. u = (1 − e^{−δr})e^{−κr} con κ = 1 − δ/2 resuelve la ecuación para todo δ (residuo simbólico 0). Para δ > 2 es la solución pura e^{+\|κ\|r} y regular en el origen, es decir, el polo virtual κ_v = δ/2 − 1. En δ = 2, φ₀ = 1 − e^{−2r} y r_e = 2∫(2e^{−2r} − e^{−4r})dr = 3/2. | `r03_teoria_simbolica.json`. Numerov: κ_v(2.04) = 0.0199999999937, κ_v(2.2) = 0.0999999999 (exactos 0.02 y 0.1). | Texto de `verificacion.md` (vía 09), `fuentes.md` y LEEME. |
| R3-05 | menor (fuentes) | Singh y Varshni, Stubbins, Nasser et al. y Gomes et al. figuraban como "[citada por Roy]" o "no encontrada". Además faltaba una fuente primaria que confirma el umbral del ECSC: Ikhdair y Sever, *Z. Phys. D* **28**, 1 (1993), DOI 10.1007/BF01437449, que da λ_c(1s) = 0.720 524 085 88. | Ver la sección de fuentes. 0.72052408588 frente a 0.7205240858820 de E3: diferencia 2×10⁻¹². | `fuentes.md` (filas 4 a 7 y fila 14 nueva), referencias y texto de la sección, LEEME. |
| R3-06 | observación | El 1.19061227 ± 0.00000004 de Gomes et al. (confirmado en su resumen) queda 1.5×10⁻⁷ por debajo de δ_c(Yukawa) = 1.1906124211, unas 4 veces su barra. E3 lo listaba sin comentario. Nuestro valor está confirmado por tres métodos de E3, por Numerov (1.19061242104) y por las Fases 1–3. | Diferencia −1.5×10⁻⁷. | Frase añadida en la sección. |
| R3-07 | menor, sin corregir | `registro_ia.md` (E3-07) cita el "control V6", que no tiene fila en `controles.md` (es informativo y está en `07_verificacion.json`). S4 aparece en los criterios de `02_dispersion.py` y tampoco tiene fila. | `controles.md`. | Solo se anota: son informativos y no cambian ningún veredicto. |
| R3-08 | observación (criterios) | Hay criterios laxos respecto a lo medido: K3 (0.02 frente a 3.9×10⁻⁴), L4 (2×10⁻² frente a 7×10⁻⁵), V5 en B (0.01). K3 comprueba el límite ½ − 2/π², no su corrección. K4 pasa justo (8.0×10⁻⁴ frente a 10⁻³, ECSC con s = 0.03). No hay forma de comprobar que los criterios se fijaron antes de correr: no hay git y solo constan en los docstrings. | `controles.md`, marcas de tiempo. | Sin cambio. Recomiendo decir en el texto que K3 y L4 son holgados a propósito. |
| R3-09 | observación | `perfiles.py` tiene fecha de modificación (21:52) posterior a los JSON de 01, 03 y 04. | Lo volví a correr con el `perfiles.py` actual: δ_c, κ y ⟨r⟩ salen bit a bit iguales a los JSON. | Sin efecto. |

## Lo verificado como correcto

### Teoría, rehecha a mano y con sympy

- **c = −d(1/a)/dδ = 2∫∂_δV φ₀².** El wronskiano de dos soluciones de energía cero con φᵢ → 1 − r/aᵢ da
  1/a₂ − 1/a₁ = 2∫(V₁ − V₂)φ₁φ₂. El término de borde en r = 0 se anula. Con δ₁ = δ + dδ se obtiene la fórmula, con φ₀
  normalizada a la asíntota 1 − r/a, que vale 1 en δ_c. El signo es correcto: ∂_δV > 0 en los cuatro perfiles, así
  que c > 0 y 1/a pasa de positivo (ligado) a negativo. Las cuatro ∂_δV analíticas de `perfiles.py` están bien, y las
  series de W (ECSC hasta x⁶/630, Hulthén con Bernoulli, átomo H) también.
- **Arranque de Frobenius:** c₂ = −1 y c₃ = (2 + 2W(0) − 2E)/6 son correctos.
- **r_e de Bethe:** r_e = 2∫(ψ² − φ²) con ψ = 1 − r/a es la fórmula estándar con esta convención (a > 0 con ligado).
- **κ = (1 − √(1 − 2r_e/a))/r_e.** Sale de imponer k cot δ = ik en k = iκ. La rama elegida es la que tiende a 1/a.
  La fórmula de κ_v (polo en k = −iκ_v) también es correcta.
- **B = d₂ + r_e c²/2.** Correcto.
- **⟨r⟩κ = ½(1 + r_eκ) + O(κ²).** Con A_s² = 2κ/(1 − κρ), y el término interior de ∫ru² es O(1), así que entra en O(κ²).
- **Punto fijo.** −x cot x = r_e x²/(2R) da 2R²E₀/π² = ¼(1 + r_e/R + ¾ r_e²/R²) (sympy). Esto confirma el término
  de segundo orden que E3 añadió tras la auditoría con Gemini (E3-09).
- **Cruce.** δ* − δ_c = r_eπ²/(8cR₁R₂) (sympy, con la condición de igual x = kR).
- **⟨r⟩/R → ½ − 2/π²**, con u = cos(πr/2R).
- **Hulthén.** E = −½(1 − δ/2)². La solución exacta de R3-04 lo contiene.
- **W del ECSC** (`r03`, `r02`). W = δ f(x) con f = (1 − e^{−x}cos x)/x.
  - f > 0, porque 1 − e^{−x}cos x ≥ 1 − e^{−x} > 0.
  - f ≤ 1 equivale a g = x − 1 + e^{−x}cos x ≥ 0. Se tiene g(0) = 0 y g' = 1 − h con h = e^{−x}(cos x + sin x).
    Como h(0) = 1 y h' = −2e^{−x}sin x ≤ 0 en [0, π], h ≤ 1 ahí. Para x > π, h ≤ √2 e^{−x} < 1. Por tanto g' ≥ 0 y
    0 < W ≤ δ, con igualdad solo en r = 0. W es entera en r.
  - En una malla fina de x ∈ [10⁻¹⁰, 10⁴], el máximo de f es 1 y g_min = −1×10⁻¹⁶ (redondeo). Precisión: W decae
    como 1/r, así que el "mínimo 0.0025" que da E3 solo es el valor en r = 400.

### Recálculo independiente (Numerov, `r01_numerov.json`)

| Magnitud | Yukawa | ECSC | Hulthén | Átomo H |
|---|---|---|---|---|
| δ_c (R3) | 1.19061242104 | 0.72052408588 | 1.99999999999 | 1.82105875604 |
| δ_c (R3 − E3) | −1.8×10⁻¹¹ | −2.5×10⁻¹² | −1.0×10⁻¹¹ | −6.4×10⁻¹² |
| c (R3) | 0.7411917658 | 2.4710277192 | 0.5000000001 | 0.5508545071 |
| c (R3 − E3) | 4×10⁻¹⁰ | 7×10⁻¹⁰ | 6×10⁻¹¹ | 8×10⁻¹¹ |
| r_e(δ_c) (R3) | 1.780631862 | −0.409963885 | 1.499999998 | 1.508531623 |
| r_e (R3 − E3) | −1.1×10⁻⁸ | −7×10⁻⁹ | −1.8×10⁻⁹ | −2×10⁻⁹ |
| 1/a en δ_c(1 ± 0.01) y (1 ± 0.05), máx \|Δ\| | 3×10⁻¹¹ | 6×10⁻¹¹ | 1.3×10⁻¹¹ | 1.7×10⁻¹¹ |
| r_e en los mismos puntos, máx \|Δ\| | 1.5×10⁻⁸ | 3.7×10⁻⁸ | 3.9×10⁻⁹ | 5×10⁻⁹ |
| B predicha (R3 / E3) | 0.0565051 / 0.0565053 | −7.54200 / −7.54201 | ~10⁻⁷ / ~10⁻⁹ (exacto 0) | 0.0048847 / 0.0048848 |
| A del ajuste a κ (R3, otros puntos) | 0.7411919 | 2.4710227 | 0.5000000 | 0.5508545 |
| E₀(R = 200, 800) en δ_c, relativo | 2×10⁻⁹, 9×10⁻⁹ | 1×10⁻⁹, 5×10⁻⁹ | 7×10⁻¹⁰, 3×10⁻⁹ | 5×10⁻¹⁰, 2×10⁻⁹ |
| Cruce 100/200, δ* − δ_c (R3) | 1.52195×10⁻⁴ | −1.00921×10⁻⁵ | 1.89265×10⁻⁴ | 1.72790×10⁻⁴ |
| Cruce 100/200, R3 − E3 | 8×10⁻¹⁴ | 3×10⁻¹³ | 3×10⁻¹² | −2×10⁻¹² |
| Cruce 200/400, δ* − δ_c (R3) | 3.75455×10⁻⁵ | −2.54566×10⁻⁶ | 4.67871×10⁻⁵ | 4.27120×10⁻⁵ |
| Cruce 200/400, R3 − E3 | −4×10⁻¹³ | 5×10⁻¹⁴ | 1×10⁻¹² | 1×10⁻¹² |

Otros resultados:

- φ₀,max = 1.000000000 en el Yukawa, el Hulthén y el átomo H, y 1.1562027 en el ECSC. Coincide con V6.
- Átomo H estático en δ = 2: a = −9.4471667 y r_e = 1.5335932, igual que E3.
- El ajuste de A en el ECSC depende de los puntos elegidos (C₃ ≈ 54). Eso explica el −4.6×10⁻⁶ de L2, y B medida
  frente a predicha (−7.526 frente a −7.542). E3 ya lo atribuye al truncado del ajuste. Es correcto.

### Integral de camino ECSC con otra pareja (h, ε) (`r02_camino_ecsc.json`)

| δ, R | E_tr (R3: h 0.01/0.03, ε 0.05/0.025) | E caja (Numerov) | Diferencia (barra R3) | E_tr de E3 | R3 − E3 |
|---|---|---|---|---|---|
| 0.5, 64 | −0.0776836770 | −0.0776836847 | 7.7×10⁻⁹ (1.2×10⁻⁷) | −0.0776836808 | 3.9×10⁻⁹ |
| 0.7, 522 | −0.0011504410 | −0.0011504427 | 1.8×10⁻⁹ (1.4×10⁻⁷) | −0.0011504417 | 7.9×10⁻¹⁰ |

Perron mínimo: +1.6×10⁻¹² y +1.4×10⁻¹³ (autovectores sin cambio de signo). El disparo de E3 y la caja de Numerov
coinciden a 2×10⁻¹⁵ en δ = 0.7. Hay una observación menor: con las dos parejas la integral de camino queda unos
10⁻⁹ por encima de la caja, siempre en el mismo sentido. Es un residuo sistemático de h y ε, muy dentro de la barra.

### Controles (punto 4)

- **U2 y S1.** El umbral numérico no se cambió. Las variantes U2b y S1b cambian solo el diseño: puntos más cerca del
  umbral en U2b, y k ≤ 0.05δ con grado 4 en S1b. Están marcadas como posteriores, y U2 y S1 se siguen reportando como
  "no pasa". No es engañoso. Lo único engañoso era la tabla 1, que mostraba U2b sin etiqueta (R3-02, corregido).
  S1 falla por poco (1.3×10⁻⁹ frente a 10⁻⁹), y la causa medida (truncado del polinomio en k²) es plausible.
- **V3.** Revisé el arreglo de `_observables_ligado`: integración hacia adentro de la solución decreciente desde
  r_m + 40/κ, empalmada en r_m = min(r_f/2, 4/κ). Es correcto. Un error en la condición inicial hacia adentro solo
  añade una componente que decae al integrar hacia el origen, así que no contamina. Solo actúa si κr_f > 10, así que
  los resultados cerca del umbral no cambian. Mis valores cerca del umbral coinciden con los de E3, lo que lo confirma.
  Una salvedad: la primera salida fallida no se conservó, y eso E3 ya lo dice.
- **Criterios laxos:** ver R3-08.

## Fuentes (punto 5)

| Fuente | Estado tras R3 | Qué se comprobó |
|---|---|---|
| Lam y Varshni, PRA **4**, 1875 (1971) | [V] en la página de APS | Título "Energies of s eigenstates in a static screened Coulomb potential": es del Yukawa. Confirma la corrección que hizo E3. |
| Lam y Varshni, PRA **6**, 1391 (1972) | [V] en Scilit con DOI | Título "Bound eigenstates of the exponential cosine screened Coulomb potential", páginas 1391–1399. δ_c del 1s por variacional de dos parámetros. La página de APS dio error. El 0.7115 está en la tabla I de Roy (nota d, ref. [37]). |
| Singh y Varshni, PRA **28**, 2606 (1983) | [V] en la página de APS | Título "Accurate eigenvalues and oscillator strengths for the exponential-cosine screened Coulomb potential", 6 a 8 cifras. 0.72052408 en Roy, tabla I, nota f, ref. [43]. Texto completo no abierto. |
| Roy, arXiv:1904.11166 | [V-arXiv] | Tabla I: Hulthén 2.00000000, Yukawa 1.190610, ECSC 0.7205240. Lista además 0.7115, 0.7131, 0.72052408 y 0.72055425 para el ECSC. |
| Stubbins, PRA **48**, 220 (1993) | [V] en la página de APS | "Bound states of the Hulthén and Yukawa potentials", variacional generalizado. |
| Nasser, Abdelmonem y Abdel-Hady, Phys. Scr. **84**, 045001 (2011) | [V] en el repositorio KFUPM con DOI | "J-Matrix approach for the exponential-cosine-screened Coulomb potential". El 0.72055425 sigue siendo cifra citada por Roy. |
| Gomes, Chacham y Mohallem, PRA **50**, 228 (1994) | [V] en Scilit con DOI | El resumen da 1.190 612 27 ± 0.000 000 04 (ver R3-06). |
| Bethe, PR **76**, 38 (1949) | [V] por E3 (Scilit) | La búsqueda devuelve link.aps.org/doi/10.1103/PhysRev.76.38 con el mismo título. La página de APS dio error. |
| Ikhdair y Sever, Z. Phys. D **28**, 1 (1993) (nueva) | [V] referencia en OUCI con DOI 10.1007/BF01437449 | Cifra leída en el PDF del repositorio staff.najah.edu (texto OCR): λ_c(1s) = 0.720 524 085 88. |

**Cifras atribuidas.** 0.72052408 (Singh y Varshni, vía Roy): sí, y es nuestro valor truncado (diferencia 5.9×10⁻⁹).
0.7205240 (Roy): sí. Ikhdair y Sever cierra la comparación a 11 cifras.

No encontré un valor publicado verificable de la longitud de dispersión estática e–H, así que esa comparación sigue abierta.

## Cambios hechos dentro de E3

1. `codigo/09_textos.py`. Copia previa en `revision/09_textos_antes_R3.py.txt`. Cambios:
   - cifras de Roy tal como están impresas (R3-01);
   - etiqueta U2b en la columna "segundo método" (R3-02);
   - Ikhdair y Sever, y la nota sobre Gomes (R3-05, R3-06);
   - argumento de r_e < 0 como condición necesaria (R3-03);
   - Hulthén exacto (R3-04);
   - referencias con DOI y "Qué quedó sin hacer" actualizado;
   - arreglo de un escape `\p` que daba SyntaxWarning.

   Después lo volví a correr, y eso regeneró `seccion_articulo.md`, `LEEME.md` y `verificacion.md`. No cambia
   ninguna cifra calculada.
2. `fuentes.md`. Copia previa en `revision/fuentes_antes_R3.md.txt`. Filas 4 a 7 actualizadas, fila 14 nueva y
   sección "Añadido por la revisión R3".
3. `registro_ia.md`: entrada E3-R3.

No modifiqué nada fuera de E3. Las tablas de pares de `fase2/resultados/tablas` solo se leyeron: siguen siendo los
mismos 8 archivos.
