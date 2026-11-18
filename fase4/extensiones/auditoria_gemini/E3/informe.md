# Informe de la auditoría externa de E3 (Gemini, app web, modo "Pro", 17-11-2026)

Chat nuevo "Material auditoría E3"; dos rondas (transcripción en `conversaciones/E3.md`, respuestas en `respuestas/`). Gemini **no ejecutó código** y reconoció que sus dos datos bibliográficos eran de memoria. Las cifras se comprobaron con un script propio independiente del código de E3 (`respuestas/chk_e3_claude.py`).

| ID | Hallazgo de Gemini | Gravedad (Gemini) | Comprobación (con números) | Estado |
|---|---|---|---|---|
| E3-G1 | Roy (2019) estaría publicado en Eur. Phys. J. Plus 135, 335 (2020) | Baja | La página de arXiv 1904.11166 no tiene Journal-ref ni DOI y el PDF no nombra revista; Crossref no accesible desde aquí. Gemini admitió que lo dio de memoria | Pendiente (no se cita) |
| E3-G2 | Mott y Massey (1965, p. 531) darían a ≈ −9.44 a₀ para el e–H estático | Baja | No se pudo abrir el libro; Gemini admitió que era de memoria. Nuestro cálculo independiente da a = −9.44717 a₀, igual al de E3 | Pendiente (no se cita) |
| E3-G3 | U2 y S1 no deberían figurar como "no pasa" | Baja | La causa ya está en `controles.md`; Gemini confundía U2 (ajuste cúbico de κ(δ)) con el rango efectivo y lo aceptó en la ronda 2. El criterio se fijó antes | Propuesta rechazada (sin cambios) |
| E3-G4 | La corrección del punto fijo tiene un término de segundo orden: 2R²E₀/π² = ¼(1 + r_e/R + ¾ r_e²/R²) | — | brentq sobre −x cot x = r_ex²/(2R): coeficiente 0.7526 (R = 200) y 0.7503 (R = 1600), 3/4. r_e/4 + 3r_e²/(16R) en R = 1600 da +0.4455, −0.1025, +0.3753, +0.3774, igual a lo medido (la tabla 2 solo comparaba con r_e/4) | Válido y corregido (`codigo/09_textos.py`, `seccion_articulo.md` regenerada) |
| E3-G5 | ⟨r⟩/R → ½ − 2/π² correcto | — | (¼ − 1/π²)/(½) = 0.29736 | Sin error |
| — | Deducciones (c por wronskiano, κ, κ_v, B, ecuación (*), cruce) | — | Rehechas; el cruce para el Yukawa, 1.7806·π²/(8·0.7412·800·1600) = 2.32×10⁻⁶, coincide con la tabla 2 | Sin error |
| — | Números (Gemini no los calculó) | — | δ_c = 1.190612421061, 0.720524085882, 2.000000000000, 1.821058756042; r_e = 1.78063, −0.40997, 1.50000, 1.50853; c = 0.74119177, 2.47102772, 0.5, 0.55085451; a(e–H, δ = 2) = −9.44717 | Coinciden con la sección |

**Resultado:** un hallazgo válido (E3-G4), de presentación: se añadió el término de segundo orden y la comparación con él. Nada cambia en los resultados.
