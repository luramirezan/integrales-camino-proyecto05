# Auditoría externa con Gemini de las extensiones de la Fase 4 (decisión D4)

- Herramienta: app web de Gemini en Chrome (cuenta del equipo), selector de modo "Pro", 17-11-2026. Un chat nuevo por extensión, material en tres partes (`EXT/trozos/`), hallazgos, respuesta calculada de los autores (`EXT/respuestas/`) y cierre con tabla final.
- Regla: un desacuerdo se resuelve calculando. Ningún dato de Gemini se aceptó sin comprobarlo con un script propio independiente del código de la extensión (`EXT/respuestas/chk_*_claude.py`) o con la fuente.
- Observación general: Gemini **no ejecutó código en ninguna auditoría** (lo dijo cada vez) y, cuando se le preguntó, admitió que sus confirmaciones bibliográficas eran de memoria. En la primera ronda tendió a repetir las cifras del texto como "recalculadas". Sus aportes útiles fueron analíticos.

## Resumen por extensión

| Extensión | Rondas | Hallazgos de Gemini | Válidos | Refutados con cálculo | Corrección aplicada |
|---|---|---|---|---|---|
| E1 contexto físico | 3 | 6 | 0 | E1-G3 (dirección del efecto de la degeneración: con k_BT/E_F = 0.71, λ/λ_De = 1.196, no menor que 1) | Ninguna. Mejora opcional anotada en `E1/informe.md` |
| E3 otros perfiles | 2 | 5 | E3-G4 (término 3r_e²/(16R²) del punto fijo de la caja) | — (E3-G1 y G2 eran citas de memoria: pendientes, no se usan) | `E3_otros_perfiles/codigo/09_textos.py` y `seccion_articulo.md` |
| E4 extensión según ℓ | 3 | 5 | 0 | E4-G1 (redondeo float64: es error O(h²), cociente 3.95), E4-G5 (sesgo FD en r⁴: u ∝ r², la red es exacta sobre r²; Richardson baja el error de U₁ a 1.4×10⁻⁶) | Ninguna |
| E2 cruce de cajas | 2 | 4 | E2-G4 en forma reformulada: con r_e > 0 el cruce crudo es solo cota superior de δ_c; la prueba de artefacto en δ = 1.19 necesita el cruce corregido por la ley (1.1906131 con el disparo, 1.1905372 con la integral de camino, ambos > 1.19). El argumento original de Gemini era el contrario y falso | E2-G1 (sesgo de la ponderación: 2.4×10⁻¹⁰ frente a barras de 10⁻⁵ a 10⁻⁹) | Nuevo `E2_cruce_de_cajas/codigo/13_cruce_corregido.py` y su JSON; frase reescrita en `seccion_articulo.md` y `LEEME.md` |
| E5 Feynman–Kac | 2 | 3 (+1 retirado en la ronda 2) | E5-G1 reformulado: la anulación de los estados con l ≥ 1 se debe a ⟨e_k, f⟩ = 0 (f = q^{1/2} radial), no a la partida. Propio: la figura e5_05 cortaba en 1.5 el pico de 3.70 que cita el texto | E5-G2 (forma de S(x): efecto en a ≤ 4×10⁻¹⁶; la forma de Gemini cancela más), E5-G3 (la frase del pico es correcta según `03_colas.json`), "c_k más rápido que 1/k⁴" (basta Σ k²|c_k| < ∞) | `E5_feynman_kac/teoria.md` (sec. 5) y `codigo/06_figuras.py` (figuras regeneradas). Mejora no aplicada: w̄₁ = δ_c/(2c) = 0.803174 |

Detalle de cada hallazgo, con sus números, en `EXT/informe.md`; transcripción en `EXT/conversaciones/EXT.md`. Cada auditoría quedó registrada en el `registro_ia.md` de su extensión.

Referencias: en E5 Gemini dio páginas que coinciden con `fuentes.md` (que tenía en el material) y dijo haberlas consultado, sin mostrar fuente; no cuenta como verificación. Ninguna cita de Gemini se incorporó a las extensiones.
