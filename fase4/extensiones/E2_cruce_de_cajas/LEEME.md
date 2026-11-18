# E2: criterio de cruce de cajas (Fase 4, proyecto 05)

*Extensión E2, hecha por un agente de Claude el 17-11-2026 por delegación de Lucho. Nada fuera de esta carpeta se modificó:
los módulos de `fase2/codigo` y `fase3/codigo` se importan.*

## Qué pregunta responde

¿Se puede decidir "estado débil o artefacto" y acotar δ_c **solo con cajas finitas**, sin esperar a que R supere la
longitud de dispersión? Sí: en una esfera de pared dura, en el umbral s, 2R²E₀/π² vale 1/4 y ⟨r⟩/R vale 1/2 − 2/π² para
cualquier R grande, así que las curvas de cajas distintas se cruzan cerca de δ_c. La teoría (`teoria.md`) da la ley del
cruce, δ*(R, 2R) − δ_c = π²r_e/(16cR²) + 3π²r_e²/(32cR³), con r_e y c de la energía cero.

## Resultados principales (de `resultados/05_cruces.json`, `09_tablas.md`, `07_controles.json`)

- **Intervalo final con la integral de camino** (receta de la Fase 3, método A, observable 2R²E₀/π²):
  **1.19054410 < δ_c < 1.19067723** (centro 1.1906106662, barra 6.66×10⁻⁵). Aplicando la receta al cruce (método B):
  **1.19060859 < δ_c < 1.19061621** (centro 1.1906123995, barra 3.81×10⁻⁶). Con ⟨r⟩/R: [1.19054141, 1.19068003] (A) y
  [1.19059638, 1.19062781] (B; la barra de B de ⟨r⟩/R incluye el término de pared desde la revisión R2, hallazgo R2-01:
  pasó de 1.47×10⁻⁵ a 1.57×10⁻⁵; la de A, que tampoco lo tenía, pasó de 6.04×10⁻⁵ a 6.93×10⁻⁵, y con R ≤ 800 el
  intervalo A de ⟨r⟩/R es [1.19048891, 1.19073401]).
- **Radial h = 1/160:** [1.19059710, 1.19062756] (y) y [1.19059722, 1.19062761] (⟨r⟩/R). **Disparo sin malla:**
  1.1906124213 (y) y 1.1906124202 (⟨r⟩/R), con barra del modelo de extrapolación de 1.56×10⁻⁹ y 2.00×10⁻⁹.
- Los diez intervalos contienen la referencia 1.1906124210606. Con solo cajas R ≤ 800, la integral de camino da
  [1.19055557, 1.19066686] (A) y [1.19060344, 1.19062166] (B).
- **Cruces del disparo** (y): 1.191237550, 1.190764616, 1.190649967, 1.190621745, 1.190614744 y 1.190613001 para los pares
  50/100 a 1600/3200; reproducen los del prototipo y coinciden con el modelo de rango efectivo a 2×10⁻⁹ o mejor desde el par
  200/400. Cocientes de diferencias sucesivas 4.125, 4.062, 4.031, 4.016 (ley 1/R²).
- **Prueba de artefacto:** en δ = 1.19 los tres métodos dan E₀ > 0 hasta R = 1600 (el primer E₀ < 0 de la rejilla está en
  R = 3200), pero el cruce corregido por la ley predicha (δ* − α_y/R² − β_y/R³) queda por encima de 1.19 desde el par 50/100
  (1.1906131 con el disparo, 1.1905372 con la integral de camino; `codigo/13_cruce_corregido.py`), así que el cruce clasifica
  δ = 1.19 como ligado con R = 50 y 100. El cruce crudo solo no bastaría: con r_e > 0 es una cota superior de δ_c (auditoría
  externa, `fase4/extensiones/auditoria_gemini/E2/informe.md`). Controles negativos (repulsivo, no ligado, ligado profundo): ningún cruce.
- **La diferencia integral de camino menos disparo en el cruce es la pared sin imagen**, con el tamaño que predice la teoría
  (`verificacion.md`, sección 2).
- **Controles:** 27 de 31 pasan. No pasan K2 (orden de Trotter: pared en R = 50, orden superior en ε = 0.2 en R = 3200),
  K7-disparo y K7-disparo-inicial (PCHIP y cúbico local frente al spline en el par 50/100 de ⟨r⟩/R) y K11 (colapso
  evaluado a δ fijo en vez de z fijo). Las causas medidas están en `controles.md`.
- **Originalidad:** ver `fuentes.md`. La ecuación de la caja es la del método de la pared esférica (Borasoy et al. 2007) y
  el valor universal en la unitariedad se usa en redes periódicas y en trampas armónicas; el escalamiento con tamaño finito
  del Yukawa existía con el tamaño de la base y con un radio de corte. No encontramos el cruce en una esfera dura aplicado al
  apantallamiento crítico, ni la ley con coeficientes predichos, ni el punto fijo de ⟨r⟩/R.

## Cómo reproducir (desde `codigo/`, un proceso, `export OMP_NUM_THREADS=1`)

| Orden | Script | Qué hace | Tiempo medido |
|---|---|---|---|
| 1 | `01_teoria.py` | Puntos fijos, pozo cuadrado exacto, r_e, c, modelo de rango efectivo, pared de la transferencia | 13 s |
| 2 | `02_disparo.py` | Disparo sin malla en la rejilla (y 9 δ más para el colapso), a_s y r_e | 56 s |
| 3 | `03_radial.py` | Radial h = 1/40 y 1/160 | 79 s |
| 4 | `04_transferencia.py 50 100 200 400 800 1600` | Integral de camino, receta completa de la Fase 3 | 19, 38, 77, 164, 360 y 876 s por caja |
| 5 | `MAXD=12 python 04_transferencia.py 3200` (dos veces) | R = 3200 en dos tandas de menos de 20 min | 2350 s en total |
| 5b | `04b_pared_rho.py` | Sesgo de pared de ⟨r⟩/R por celda (para la barra del método B; revisión R2-01) | 22 s |
| 6 | `05_cruces.py` | Cruces, Monte Carlo, métodos A y B, extrapolación | 31 s |
| 7 | `06_artefacto.py` | δ = 1.19 y controles negativos | 25 s |
| 8 | `12_diagnostico_trotter.py`, `12b_trotter_eps0025.py` | Causa de K2 | unos 3 min |
| 9 | `10_verificacion.py` | Verificaciones V1 a V7 | 41 s |
| 10b | `13_cruce_corregido.py` | Cruce corregido por la ley predicha en δ = 1.19 (añadido tras la auditoría externa) | segundos |
| 10 | `07_controles.py`, `08_figuras.py`, `09_tablas.py`, `11_cifras_texto.py`, `11b_cifras_clave.py` | Tabla de controles, figuras, tablas, cifras del texto (50 de 50 cifras clave comprobadas) | segundos |

`04_transferencia.py` es incremental (guarda tras cada celda). La salida impresa de cada script está en
`resultados/<nombre>_salida.txt`. Todo es determinista (Monte Carlo con semilla 20261117).

## Archivos

`teoria.md` (apéndice teórico), `seccion_articulo.md` (sección para el artículo), `controles.md` (generado),
`criterios_previos.md` (umbrales escritos antes de correr, con dos añadidos fechados), `fuentes.md`, `registro_ia.md`,
`verificacion.md`, figuras A a D en `figuras/`.

## Decisiones tomadas (para `fase4/extensiones/DECISIONES.md`; las revisa el equipo al final)

1. Rejilla de 23 valores de δ (15 iniciales y 8 añadidos tras el primer análisis, por el control K7) y 7 cajas hasta
   R = 3200; se hizo también R = 1600 y 3200 porque el costo lo permitió.
2. Intervalo final de la integral de camino: método A (la receta de la Fase 3 sin cambios, como se pidió). El método B se
   reporta al lado porque mide mejor cuánto se mueve el cruce.
3. Barra del cruce: la mayor entre Monte Carlo y propagación lineal (conservadora).
4. Extrapolación en R con la forma α/R² + β/R³ que da la teoría, pares con R ≥ 100, ajuste ponderado con 1/σ (decidido
   antes de tener R = 1600 y 3200 en la transferencia).
5. La pared de la transferencia queda en la barra (decisión 5 de la Fase 2); la variante con la pared restada es solo de
   sensibilidad.
6. Los controles que fallan se dejan como "no pasa" (también K11, cuyo criterio estaba mal planteado).

## Qué quedó sin hacer

- La auditoría con Gemini la hace otro agente (decisión D7).
- No se calculó el término O(R⁻⁴) del cruce (parámetro de forma y variación de r_e con δ).
- El segundo orden analítico de la ley de ⟨r⟩/R no se obtuvo en forma cerrada (sympy no terminó); se usa el modelo numérico.
- No se buscó en bases de datos de pago (Web of Science, Scopus); la búsqueda de originalidad es con buscadores abiertos.
- No se abrió Bethe (1949). La revista del trabajo de Serra (Phys. Lett. A 303, 20 (2002)) la encontró la revisión R2 en la
  lista del autor, sin verificar en el editor.
