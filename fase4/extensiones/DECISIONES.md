# Registro de decisiones (las toma Claude por delegación de Lucho, 17-11-2026)

Lucho pidió hacer todas las extensiones y que las decisiones las tome Claude, registrándolas, para revisarlas al final.

| # | Fecha | Decisión | Motivo |
|---|---|---|---|
| D1 | 17-11-2026 | Cinco carpetas, de la más sencilla a la más difícil: E1 contexto físico, E2 cruce de cajas, E3 otros perfiles, E4 extensión según ℓ, E5 Feynman–Kac sin caja | Lucho pidió aislar cada idea y ordenarlas por dificultad |
| D2 | 17-11-2026 | Cada extensión la desarrolla un agente de Claude distinto, en paralelo, con un contexto común (`CONTEXTO_COMUN.md`) | Acelera el trabajo y separa las responsabilidades |
| D3 | 17-11-2026 | Después, otro agente de Claude, distinto del que hizo cada extensión, la revisa de forma adversarial: recalcula, relee el código y vuelve a verificar las fuentes | Lucho pidió revisar "una y otra vez"; un revisor que no escribió el código no queda anclado en él |
| D4 | 17-11-2026 | Auditoría externa con Gemini en la app, por Chrome, como en la Fase 3: un chat nuevo por extensión, con hallazgos, respuesta calculada y cierre | Igual que el procedimiento ya aceptado en `fase2/auditoria_gemini` y `fase3/auditoria_gemini` |
| D5 | 17-11-2026 | No se modifica ningún archivo de las Fases 1–3; las extensiones importan sus módulos | Mantener intacto lo ya entregado |
| D6 | 17-11-2026 | Además de un revisor por extensión, un agente aparte verifica toda la bibliografía del proyecto (`bibliografia/`) | Lucho pidió más paralelismo y verificación repetida de fuentes |
| D7 | 17-11-2026 | Todo el uso de Chrome/Gemini lo hace un solo agente, en serie, para que no choquen las pestañas | Dos agentes en el mismo navegador se pisan |
| D8 | 17-11-2026 | Los controles que fallan siguen como "no pasa" aunque la causa esté entendida (también cuando Gemini propone relajarlos) | Los criterios se fijaron antes de calcular; cambiarlos después sería ajustar a los datos |
| D9 | 17-11-2026 | Las correcciones de citas que encontró la verificación bibliográfica (p. ej. la cota 1.24305 es de Schwinger 1961, no de Bargmann; 1.68 es de Tulin, Yu y Zurek; Gebremedhin y Weatherford son D. y C.) se aplican en el artículo final, no en los archivos ya entregados de las Fases 1–3 | Mantener intacto lo entregado (D5) |
| D10 | 17-11-2026 | E2: rejilla de 23 δ (15 iniciales + 8 añadidas tras el control K7, sin cambiar su umbral) y 7 cajas hasta R = 3200 | El costo lo permitió; la adición queda declarada |
| D11 | 17-11-2026 | E2: el intervalo oficial de la integral de camino es el del método A (receta de la Fase 3 sin cambios); el método B se reporta al lado | No cambiar la receta aprobada; B solo mide cuánto se mueve el cruce |
| D12 | 17-11-2026 | E2: barra del cruce = la mayor entre Monte Carlo y propagación lineal; extrapolación en R con α/R² + β/R³ (forma teórica, fijada antes de tener R = 1600 y 3200) | Elegir lo conservador y fijar el modelo antes de ver los datos |
| D13 | 17-11-2026 | E2: la originalidad se declara baja-moderada: la cuantización en esfera dura y el valor universal en unitariedad ya existen (Borasoy et al. 2007; Lüscher; Busch et al.); lo nuevo es el cruce aplicado al apantallamiento crítico, la ley de convergencia con coeficientes predichos y el punto fijo de ⟨r⟩/R | Honestidad con lo que encontró la búsqueda |
| D14 | 17-11-2026 | E2: el sesgo de pared también entra en la barra de ⟨r⟩/R (métodos B y A), sin mover el valor central; ningún control cambia de estado (27 de 31) | Hallazgo R2-01 de la revisión; misma regla que la decisión 5 de la Fase 3 para E₀ |
| D15 | 17-11-2026 | Artículo final en `fase4/articulo_final/`: cuerpo con Fase 3 + E2 (aporte principal) + E4; E1 como motivación; E3 y E5 como secciones opcionales | La guía pide para la Fase 4 la extensión y la comparación de métodos; E3 y E5 quedan a elección del equipo |
| D16 | 17-11-2026 | Auditoría Gemini: se aceptan solo los hallazgos que se comprobaron con cálculo propio (E2-G4 reformulado: el cruce crudo es solo cota superior y se añade el cruce corregido; E3-G4: término de segundo orden; E5-G1 reformulado: los l ≥ 1 se anulan porque f es radial). Se refutan, con cálculo, E1-G3, E2-G1, E4-G1, E4-G5 y E5-G3. Las páginas de las citas que dio Gemini no cuentan como verificación | Gemini no ejecutó código y citó de memoria |
| D17 | 17-11-2026 | Se añade al artículo la predicción w̄₁ = δ_c/(2c) = 0.803174, que coincide con el 0.80317 medido en E5 | Sale de cifras ya verificadas y Gemini confirmó la derivación; es barato y une E3 con E5 |
