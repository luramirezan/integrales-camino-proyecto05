# Revisión adversarial de E4 (R4), 17-11-2026

Revisor: un agente de Claude distinto del que escribió E4, con el encargo de buscar errores. Rehíce a mano las derivaciones de `teoria.md`. Recalculé los números con un método **independiente**: colocación espectral de Chebyshev con la malla r = c·sinh(s) (`espectral.py`), sin diferencias finitas, sin integrador de EDO y sin importar `comun4.py`. Comprobé la acción de pares con una suma espectral de Chebyshev y con la transformada de Hankel. Volví a buscar las fuentes con WebSearch y WebFetch. Todo se corrió con un proceso (`OMP_NUM_THREADS=1`; los cinco scripts suman unos 2 minutos).

Scripts y resultados (`revision/`):

| Script | Qué hace | Tiempo |
|---|---|---|
| `r41_comparacion.py` | Umbrales con 6 mallas; constantes del umbral; 3 puntos de cada barrido; pendiente del logaritmo del 2p | 10 s |
| `r43_cajas.py` | Y(R) y y(R) en δ_c; energía de la caja en el R_c de E4; sensibilidad del Y(2560) del 3d | 13 s |
| `r44_accion_pares.py` | K_ℓ frente a la transformada de Hankel; semigrupo; U₁ espectral frente a la tabla de E4 | 4 s |
| `r45_camino_independiente.py` | Método (a) con ε = 0.15 y 0.075 y h = 0.03 y 0.01; método (b) con ε hasta 0.0125 | 44 s |
| `r45b_sesgo_tabla.py` | Coulomb 2p con la tabla U₁ refinada (h_tab = 0.005 y 0.0025) | 31 s |

## Hallazgos

| ID | Gravedad | Descripción | Evidencia numérica | Corrección |
|---|---|---|---|---|
| R4-01 | Moderada | En el control T3 de 44, \|U_R − U_0.005\| mide el error de la tabla **sin extrapolar** (h_tab = 0.005), no el de la tabla U_R de Richardson que se usa. La sección del artículo convertía ese número en "error de red de hasta 1.3×10⁻⁴ en U₁". | U₁ espectral, con cambio de N = 700 a 900 de ≤ 3×10⁻¹², frente a U_R de E4: 1.1×10⁻⁶ a 1.8×10⁻⁶ en r = r′ = 0.01, ≤ 1.6×10⁻⁷ desde r = 0.05 y ≤ 5×10⁻¹¹ desde r = 1. Los errores de U_0.01 y U_0.005 son 3 a 5×10⁻⁴ y 0.8 a 1.3×10⁻⁴ (`r44_accion_pares.json`). | Corregidas la frase de Limitaciones de `seccion_articulo.md` y la causa en `verificacion.md` §3.5. El control sigue como "no pasa": su criterio estaba fijado antes y no se toca. |
| R4-02 | Moderada | Los seis resultados del método (a) quedan **todos** por encima de la referencia, en +4×10⁻¹¹ a +7×10⁻¹¹, con barras de 1 a 3×10⁻¹¹. El presupuesto de error de 45 no incluye el error de la tabla U₁. Los controles 114 a 124 pasan gracias al suelo heurístico de 2×10⁻¹¹ del radial y al factor 2. En Coulomb, donde la referencia es exacta, \|dif\| = 5.2×10⁻¹¹ frente a 2·err = 5.4×10⁻¹¹. | Con otros ε (0.15 y 0.075) y otras mallas (h = 0.03 y 0.01) el desfase reaparece: +5.5×10⁻¹¹ y +4.5×10⁻¹¹ (Coulomb), +5.0×10⁻¹¹ y +3.7×10⁻¹¹ (δ = 0.2, frente a la caja espectral). Al afinar la tabla a h_tab = (0.005, 0.0025), E(Coulomb, ε = 0.1, h = 0.02) cambia en −2.5×10⁻¹¹ (`r45b_sesgo_tabla.json`). | Documentado en `seccion_articulo.md` y en `verificacion.md` §4. No se volvió a correr 45: el efecto es de 4×10⁻¹⁰ relativo y no cambia ninguna conclusión. Recomendación: sumar al error un término de tabla, \|E(tabla fina) − E(tabla)\|. |
| R4-03 | Menor | Se afirmaba que el orden del método primitivo, 1.34 a 1.37, era "compatible con ε^{4/3}", sin ninguna derivación. | Con ε = 0.1, 0.05, 0.025 y 0.0125 (Coulomb 2p, h = 0.01, tablas ℓ = 0 nuevas) los órdenes locales son 1.373, 1.394 y 1.414: crecen. Un argumento heurístico da ε^{3/2}: la región r ≲ √ε pesa ∝ ε^{5/2} por paso en la onda p. | Corregido en `teoria.md` §6, `seccion_articulo.md` (resultados y discusión) y `LEEME.md`. |
| R4-04 | Menor | Y(2560) = 1.000006 para 3d no es significativo más allá de unos 10⁻³. Con E(2560) = 3.8×10⁻¹³, un error de 10⁻¹⁵ en δ_c cambia Y en 5.9×10⁻⁴, y la convergencia de δ_c(3d) declarada por E4 es de 2.1×10⁻¹⁵. | `r43_cajas.json`, `sens_3d_2560`. En R = 640 la sensibilidad es de 5.7×10⁻⁷ y la revisión reproduce Y = 1.000072, frente a 1.000074 de E4. | El texto da ahora Y(640) = 1.00007 para 3d y explica por qué no da Y(2560). El control 80 sigue pasando con margen. |
| R4-05 | Menor | En `teoria.md` §4 se decía, para ℓ = 2, "solo ⟨r³⟩ diverge". | Todo ⟨r^n⟩ con n ≥ 3 diverge: como logaritmo en n = 3 y como κ^{3−n} para n > 3 (es la ec. (4) de Riisager). | Corregido. |
| R4-06 | Menor | Se atribuía a Klaus y Simon (1980) el resultado concreto "autoestado normalizable y α = 1 para ℓ ≥ 1". No se pudo leer su texto, ni E4 ni la revisión. | Los artículos que lo citan (arXiv:0912.0418 y 1111.6788) solo confirman el desarrollo μ(k) = 1 − ak + O(k²) de su teorema 2.2. La frase α = 2 (ℓ = 0) y α = 1 (ℓ ≠ 0) sí está, literal, en Serra, Neirotti y Kais (1998). | `teoria.md`, `seccion_articulo.md` y `fuentes.md` atribuyen ahora el resultado concreto a Serra et al. y a Klaus y Simon solo el marco general. |
| R4-07 | Menor | "La corrección (5) reduce el error a 1.7×10⁻⁶ en el último punto": ese 1.7×10⁻⁶ es el suelo numérico, no el acierto de la fórmula. | En `42_barridos.json`, rel_E_refinada baja hasta 9.3×10⁻⁸ en Δ/δ_c = 3×10⁻⁸ y vuelve a subir a 1.7×10⁻⁶ en 10⁻⁹. Eso son unos 5×10⁻¹⁷ absolutos con \|E\| ≈ 3×10⁻¹¹. | Redacción corregida en `seccion_articulo.md` y `verificacion.md`. |
| R4-08 | Observación | Control 99 (cruce de y en 2p, ±10 %): pasa con 9.3 %, al borde. Con R = 80 no habría pasado (19.9 %). | La revisión deriva la corrección Y = 1 + (9/5)A²/R + O(R⁻²) de la energía de caja de ℓ = 1. Con ella, el desplazamiento relativo del cruce es ≈ (3/2)(9/5)A²/R: 11 % en R = 160 y 22 % en R = 80, que explica casi toda la diferencia. En δ_c da Y(2560) = 1.004648, frente a 1.004665 de E4 y 1.004654 de la revisión. | Añadido a `teoria.md` §5 y a `seccion_articulo.md`. Se recomienda comparar con la predicción corregida en vez de con un ±10 % fijo. |
| R4-09 | Observación | Control 126 (Coulomb 2p con \|E + 1/8\| < 10⁻⁷) es muy laxo frente a lo que se obtiene (5×10⁻¹¹). Estaba fijado antes, así que no es un ajuste a posteriori, pero no discrimina. Lo hace el 114. | | Sin cambio. |
| R4-10 | Observación (fuentes) | Misu et al. sí tiene revista confirmada: *Nucl. Phys. A* **614**(1), 44–70 (1997), según el repositorio de Lund. La entrada [26] de Riisager 2013 es Riisager, Jensen y Møller, *Nucl. Phys. A* **548**, 393 (1992). El EPL de 1992 no aparece por tercera vez; las bibliografías de los mismos autores citan en su lugar NPA 548 y PLB 312, 1 (1993). | | `fuentes.md` y la referencia de Misu en la sección, actualizadas. |

Comprobé las 16 causas declaradas de los controles que no pasan:

- **Correctas** (9, 11, 20, 22, 27, 41, 42, 43, 54, 63, 75 y 125). Dos ejemplos:
  - En el control 63 el valor de Hellmann–Feynman, 0.1260252, coincide con S(1 + (3/2)A²κ) = 0.1260252. La que falla es la derivada numérica, como se dice.
  - En los controles 20, 22, 42, 43 y 54, el error fijo de malla, de unos 4×10⁻⁹, frente a E ∝ Δ², reproduce el 1.1×10⁻² observado.
- **Correctas pero mal interpretadas** (106, 107, 110 y 111): ver R4-01.

## Verificado como correcto

- **Teoría, rehecha a mano:**
  - Wronskiano d(1/a_s)/dδ = −2Σ, con el signo de la convención de las Fases 1 a 3, y c₀ = 2Σ, coherente con Hellmann–Feynman (2κΣ).
  - E = −SΔ para ℓ ≥ 1; I_N = −3/2, y de ahí la corrección (A²/2)(2SΔ)^{3/2}, equivalente a S A²√(2S) Δ^{3/2}.
  - ⟨r⟩ de 2p = C₀ + A²[ln(1/κ) + 5/4 − γ − ln 2], con la corrección de norma (1 + 3A²κ/2). La pendiente del logaritmo es A².
  - ⟨r²⟩κ → 5A²/4: comprobado, porque ∫(1+x)²e^{−2x}dx = 1/2 + 1/2 + 1/4 = 5/4. El término constante es D₀ + (15/8)A⁴.
  - I₂ = −35/36 y f₂² − 1 ≈ −x²/3.
  - Hadamard dE/dR = −u'(R)²/2, que da E(R) = (2ℓ+1)A²/(2R^{2ℓ+1}) e Y → 1.
  - B/A = −2SΔ/((2ℓ+1)A²) y el radio de cruce R_c, con escalas Δ⁻¹, Δ^{−1/3} y Δ^{−1/5}.
  - Cruce de dos cajas, ec. (13): signo y factores correctos.
  - K_ℓ = √(rr′)/ε · Ĩ_{ℓ+1/2}(rr′/ε) e^{−(r−r′)²/(2ε)}, con normalización 4π(2πε)^{−3/2}, que se reduce a K_D para ℓ = 0.
  - Argumento de positividad del peso.
- **Umbrales (espectral frente a E4):**

  | Estado | Diferencia | Dispersión entre mallas espectrales |
  |---|---|---|
  | 1s | −2.4×10⁻¹³ | 2×10⁻¹¹ |
  | 2s | −5.2×10⁻¹⁴ | 2.8×10⁻¹² |
  | 2p | +6.4×10⁻¹⁵ | 4.7×10⁻¹⁴ |
  | 3d | −7.6×10⁻¹⁶ | 1.4×10⁻¹⁴ |

  1/δ_c coincide con λ_c = 0.8399039(1) y 4.540980(3) de la tabla I de Serra et al., que releí.
- **Constantes del umbral** A², S, Σ, C₀, D₀, ⟨r⟩₀ y ⟨r²⟩₀: coinciden dentro de la dispersión espectral, de 10⁻⁸ relativo o mejor (A² del 3d, a 7×10⁻⁶).
- **Barridos:** en Δ/δ_c = 10⁻² y 10⁻⁴ (ℓ = 0), y en 10⁻² y 10⁻⁵ (ℓ ≥ 1), E, ⟨r⟩ y ⟨r²⟩ coinciden a 3×10⁻⁸ o mejor (con una excepción: ⟨r²⟩ del 3d en 10⁻⁵, a 1.4×10⁻⁷). En los puntos más cercanos al umbral la diferencia (3×10⁻⁵ en ℓ = 0 con Δ/δ_c = 10⁻⁶; 7×10⁻⁶ en ℓ ≥ 1 con 10⁻⁸) es del orden de la convergencia del propio método espectral, así que el límite es de la revisión, no de E4. Los nodos son correctos.
- **Pendiente del logaritmo del 2p**, con los mismos 9 puntos: 6.596959, frente a 6.596958 de E4 y A² = 6.610168. La fórmula (7′) sin parámetros libres acierta a 2.3×10⁻⁷.
- **Cajas en δ_c** (1s y 2p hasta R = 2560; 3d hasta R = 640): coinciden con E4 a ≤ 2.2×10⁻⁷, salvo en el R mayor (1.2×10⁻⁵ en 2p con R = 2560 y 2.7×10⁻⁶ en 3d con R = 640), donde la diferencia es del orden de la convergencia espectral. La energía de la caja en el R_c de E4 es de 10⁻¹⁰ a 10⁻⁸ veces la escala SΔ, de modo que R_c es correcto.
- **Integral de camino:**
  - K₁ y K₂ coinciden con la transformada de Hankel exacta a ≤ 9×10⁻¹⁵, y se cumple el semigrupo a 2×10⁻¹⁵.
  - El peso es positivo en todas las corridas nuevas: Perron mínimo > 0 y min T > 0, entre 5.4×10⁻¹⁵ y 4.5×10⁻¹³.
  - Con ε = 0.15 y 0.075 y la ley ε², Coulomb 2p da −1/8 + 5×10⁻¹¹ (ver R4-02).
  - Con δ = 0.2 el cociente de sesgos es 4.009, es decir, orden 2.
  - En Coulomb el cociente de sesgos entre ε = 0.15 y 0.075 es 3.49, no 4, porque el desfase constante de +5×10⁻¹¹ pesa frente a sesgos de 3×10⁻¹⁰.

## Cambios hechos en E4 por la revisión

1. `teoria.md`:
   - R4-05: ⟨r^n⟩ de ℓ = 2.
   - R4-06: atribución a Klaus y Simon.
   - R4-08: coeficiente (9/5)A²/R de la caja de ℓ = 1.
   - R4-03: orden del método primitivo.
2. `seccion_articulo.md`:
   - R4-06: motivación.
   - R4-04 y R4-08: cajas.
   - R4-02: desfase del método (a).
   - R4-03: orden de (b).
   - R4-07: energía del 2p.
   - R4-01: limitaciones.
   - R4-10: referencia de Misu.
3. `LEEME.md`: cifras de cajas y del método primitivo, y un apartado de la revisión.
4. `verificacion.md`: §2 (R4-07), §3.5 (R4-01) y §4 (R4-02).
5. `fuentes.md`: R4-06 y R4-10.
6. `codigo/48_verificar_cifras.py`: también lee `revision/*.json`. Se volvió a correr; todas las cifras nuevas tienen par en un JSON, salvo los datos bibliográficos.
7. `registro_ia.md`: entrada E4-06.

No se tocó ningún JSON ni ninguna figura de E4, y no se cambió ningún criterio de control. Las tablas nuevas de la revisión se calcularon sin caché, de modo que no se escribió nada en `resultados/tablas/`.

## Fuentes consultadas por la revisión

- CaltechAUTHORS, registro de Klaus y Simon (1980): authors.library.caltech.edu/records/95ns3-zwc43. Solo resumen y metadatos.
- Artículos que citan a Klaus y Simon: arXiv:0912.0418 (ar5iv), arXiv:1111.6788, arXiv:1905.10766 y arXiv:1909.00468 (ar5iv).
- Serra, Neirotti y Kais, PDF del grupo de Kais: www.chem.purdue.edu/kais/docs/papers/Physical-Review-1998.pdf. Se leyeron la cabecera (PRA 57, R1481), la tabla I y la frase sobre α.
- Riisager 2013: arxiv.org/abs/1208.6415 y su PDF. Se leyeron la ec. (4), la entrada [26] y la frase sobre las ondas s y p.
- Jensen et al. 2004: www.doi.org/10.1103/REVMODPHYS.76.215 y data.zhenzhi.com. Metadatos y resumen.
- Misu et al.: lup.lub.lu.se/record/10c7a49e-5689-402f-80cb-fc7d7fa8a1be (revista) y arXiv:nucl-th/9612016 (ec. (17) y bibliografía).
- EPL de 1992: búsquedas sin resultado; bibliografías de arXiv:1705.08718 y nucl-th/9612016.

Pendiente: la auditoría con Gemini en Chrome no la hizo esta revisión; no estaba en su encargo.
