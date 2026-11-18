# Informe de la auditoría externa de E2 (Gemini, app web, modo "Pro", 17-11-2026)

Chat nuevo ("Auditoría Material Proyecto"); dos rondas (transcripción en `conversaciones/E2.md`, respuestas en `respuestas/`). Se envió también `teoria.md`. Gemini **no ejecutó código** y dio las referencias de memoria (lo dijo). Las cifras se comprobaron con un disparo propio sin malla, independiente del código de E2 (`respuestas/chk_e2_claude.py`).

| ID | Hallazgo de Gemini | Gravedad | Comprobación (con números) | Estado |
|---|---|---|---|---|
| E2-G1 | La ponderación 1/σ en la extrapolación α/R² + β/R³ subestima el sesgo O(R⁻⁴) de las cajas pequeñas | Media (Gemini) | Disparo extrapolado 1.1906124213 frente a 1.1906124210606 (2.4×10⁻¹⁰, barra 1.56×10⁻⁹). Resto O(R⁻⁴): 2.9×10⁻⁹ en 200/400 (mi cálculo) y ~5×10⁻⁸ en 100/200, frente a barras de la integral de camino de 6.7×10⁻⁵ (A) y 3.8×10⁻⁶ (B). Gemini aceptó | Refutado |
| E2-G2 | K7 mal diseñado (spline frente a PCHIP) | Baja | Ya declarado (V1: el spline coincide con el cruce sin interpolar); el criterio no se cambia | Sin cambios |
| E2-G3 | K11 planteado a δ fijo en vez de z fijo | Baja | Ya declarado en la sección y en `controles.md` | Sin cambios |
| E2-G4 | (Ronda 1) "La clasificación de δ = 1.19 es robusta al signo de r_e" | — | Falso para r_e > 0, que es el caso del Yukawa: el cruce crudo queda por encima de δ_c y es solo una cota superior. Un δ en (δ_c, δ*) también da y(R) > y(2R). La frase de la sección ("todos los cruces están por encima de 1.19: la prueba clasifica δ = 1.19 como ligado") omitía el paso que la justifica. Cruce corregido δ* − α_y/R² − β_y/R³: 1.1906131 (disparo, 50/100), 1.1905372 (integral de camino, 50/100), todos > 1.19 (margen mínimo 5.4×10⁻⁴). Gemini aceptó la reformulación en la ronda 2 | Válido en su forma reformulada (gravedad media) y corregido: nuevo `codigo/13_cruce_corregido.py` y su JSON; frase reescrita en `seccion_articulo.md` y `LEEME.md` |
| — | Deducciones (ecuación de la caja, F(0) = 1/4, dF/dz = −2/π², G(0) = ½ − 2/π², ley del cruce con segundo orden, O(R⁻⁴)) | — | Rehechas a mano; coinciden. Gemini también las rehizo | Sin error |
| — | Pared sin imagen: corrimiento −π²c_w/(8cR²) del cruce | — | Gemini lo rehízo y coincide con lo medido (−1.17×10⁻⁶ en 400/800) | Sin error |
| — | Números (Gemini no los calculó) | — | Cruce 200/400 por disparo propio = 1.1906499666 (E2: 1.190649967); δ* − δ_c = 3.7546×10⁻⁵ frente a la ley 3.7543×10⁻⁵ | Coinciden |
| — | Referencias (Borasoy et al. 2007, Busch et al. 1998, Nightingale 1976, Lüscher) | — | Gemini, de memoria; no es verificación. Valen las de `E2_cruce_de_cajas/fuentes.md` | Sin cambios |

**Resultado:** una corrección de razonamiento en la prueba de artefacto (la conclusión no cambia). Salió al refutar con cálculo un argumento erróneo de Gemini, no de un hallazgo correcto de Gemini.
