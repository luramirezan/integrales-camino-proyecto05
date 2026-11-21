# E4 · Cómo crece la extensión espacial cerca del umbral según el momento angular ℓ

Proyecto 05 (Yukawa), Fase 4, extensión E4 (propuesta 2 de `fase4/propuesta_originalidad/ideas_fase4_y_final.md`). Cálculo y redacción: Claude (IA), 17-11-2026, por delegación de Lucho. Las decisiones están abajo y quedan pendientes de revisión del equipo.

## Qué pregunta responde

¿Cómo crecen E, ⟨r⟩ y ⟨r²⟩ cuando el apantallamiento se acerca al umbral de un estado con ℓ = 0 (1s, 2s), ℓ = 1 (2p) o ℓ = 2 (3d)? ¿Qué ve una caja de Dirichlet en cada caso? ¿Se puede hacer la integral de camino de la onda p con peso positivo?

## Resultados principales (cifras de `resultados/*.json`)

- **Umbrales:** δ_c(2s) = 0.3102092827139, δ_c(2p) = 0.2202168066066, δ_c(3d) = 0.0913451207717 (1s: 1.1906124210606). Un segundo método (recurrencia de energía cero de las diferencias finitas) da diferencias de 10⁻¹¹ o menos.
- **Energía:** exponentes medidos de 2.0000003 (1s), 2.0000007 (2s), 1.00009 (2p) y 0.9999999 (3d), con predicciones 2, 2, 1 y 1. Los coeficientes salen sin ajuste de la solución de energía cero: κ/Δ = 0.741192 (1s) y 1.316956 (2s); −E/Δ = 0.12602 (2p) y 0.22192 (3d), frente a S de Hellmann–Feynman.
- **Extensión:** ℓ = 0: ⟨r⟩κ = 0.5000001 y ⟨r²⟩κ² = 0.5000001. ℓ = 1: ⟨r²⟩ ∝ κ^{−0.99992} y ⟨r²⟩κ → 5A²/4 = 8.2627. ℓ = 2: ⟨r⟩ → 21.616 y ⟨r²⟩ → 766.9, finitos.
- **Logaritmo de la onda p:** el exponente local de ⟨r⟩ baja de 0.39 a 0.10, así que no es una potencia. ⟨r⟩ es lineal en ln(1/κ) con pendiente 6.597, frente a la predicción A² = 6.610 (la amplitud de la cola de la solución de energía cero normalizada). La fórmula sin parámetros libres, con la corrección de norma, acierta a 2.3×10⁻⁷.
- **Cajas:** en δ_c, 2R²E/π² → 1/4 solo para ℓ = 0; para ℓ ≥ 1 tiende a 0, y el punto fijo está en Y = 2R^{2ℓ+1}E/((2ℓ+1)A²) → 1 (1.0047 para 2p en R = 2560 y 1.00007 para 3d en R = 640; en 3d con R = 2560 la cifra depende de δ_c a 10⁻¹⁵, ver `revision/informe_revision.md`). El radio mínimo con signo correcto escala como Δ^{−1}, Δ^{−1/3} y Δ^{−1/5}. Con R = 100 el signo es fiable desde Δ/δ_c = 1.1×10⁻² (1s), pero ya desde 3.6×10⁻⁴ (2p) y 2.0×10⁻⁴ (3d).
- **Integral de camino para ℓ = 1:** se usa la transferencia radial con el núcleo libre exacto de la onda p y la acción de pares de Coulomb en la onda p (tablas nuevas). El peso es real, positivo y normalizable. Coulomb 2p da −1/8 + 5×10⁻¹¹, los seis casos son compatibles con el radial y el orden de Trotter es 2.00 (1.61 en δ = 0.219 por la pared, 2.00 con la pared corrida). La alternativa primitiva para el centrífugo converge con orden 1.34 a 1.37 (1.41 con ε = 0.0125, en la revisión) y deja errores de hasta 0.1 %.
- **Controles:** 129 en total; 105 pasan, 16 no pasan (todos con causa medida en `verificacion.md`) y 8 se midieron sin criterio previo.

## Cómo reproducir (desde `codigo/`, un proceso)

```
export OMP_NUM_THREADS=1
python 40_controles_radial_l.py   # ~140 s  Coulomb, umbrales, FD frente a disparo
python 41_constantes_umbral.py    # ~2 s    constantes de la solución de energía cero e integrales universales
python 40b_umbral_fd.py           # ~25 s   delta_c por la recurrencia FD; diagnóstico con h = 1/160 (usa 40)
python 42_barridos.py             # ~55 s   barridos sin caja cerca de los cuatro umbrales (usa 40 y 41)
python 43_cajas_l.py              # ~100 s  cajas en el umbral, radio de cruce, cruces de y (usa 40 y 41)
python 44_tablas_l1.py            # ~15 s   tablas U_1 (onda p) y sus controles; cache en resultados/tablas/
python 45_transferencia_l1.py     # ~30 s   integral de camino l = 1, métodos (a) y (b)
python 46_figuras.py; python 47_tabla_controles.py; python 48_verificar_cifras.py
```
Módulos: `comun4.py` (diferencias finitas con V_ef sobre `fase2/codigo/radial.py`, disparo, umbral, caja por disparo) y `pares_l.py` (K_ℓ, tablas U_ℓ y matriz de transferencia de la onda ℓ). Importan `fase2/codigo` y `fase3/codigo` sin modificarlos; las tablas de ℓ = 0 de la Fase 2 solo se leen de su caché. Todo es determinista.

## Archivos

`teoria.md` (derivaciones), `seccion_articulo.md` (sección para el artículo), `controles.md` (tabla generada), `verificacion.md`, `fuentes.md`, `registro_ia.md`, `figuras/46_*.png`, `resultados/*.json` y `*_salida.txt`.

## Decisiones de E4 (tomadas por Claude, para revisar)

| # | Decisión | Motivo |
|---|---|---|
| E4-D1 | Los barridos se hacen con un disparo sin caja (exterior exacto de Bessel modificada); las diferencias finitas solo controlan | Llegar a Δ/δ_c = 10⁻⁹ con FD exigiría cajas de R ∼ 10⁷ y el error fijo de malla domina (verificacion.md, sección 3) |
| E4-D2 | Integral de camino con la opción (a): núcleo libre exacto K_ℓ y acción de pares de Coulomb en la onda ℓ; (b) primitiva solo como comparación; (c) nodo fijo en 3D no se implementa | (a) es determinista, mantiene el orden ε² y su peso es positivo; (c) sería Monte Carlo con barras mayores que las energías cerca del umbral |
| E4-D3 | Ventana asintótica = las dos últimas décadas de Δ de cada barrido, fijada antes de correr | Evitar escoger la ventana a la vista de los datos |
| E4-D4 | La variable de caja para ℓ ≥ 1 es Y = 2R^{2ℓ+1}E/((2ℓ+1)A²) | Es la que tiene punto fijo (derivado en teoria.md, apartado 5) |
| E4-D5 | En 45 se usa el exponente 4 de Richardson en h (receta de la Fase 3), decidido después de ver que el orden no es medible | Las diferencias entre mallas son ≤ 2.3×10⁻¹¹; el cambio afecta a E en menos de 10⁻¹¹ (se guardan ambos) |

## Qué quedó sin hacer

- La auditoría externa con Gemini (decisión D4 del registro común) no la hizo este agente: corresponde al paso de auditoría del proyecto.
- La integral de camino se hizo para ℓ = 1, no para ℓ = 2 (el código lo admite cambiando L en 44 y 45).
- No se leyó el texto completo de Klaus y Simon (1980) ni el de Jensen et al. (2004), y no se encontró Riisager, Fedorov y Jensen, *Europhys. Lett.* (1992); ver `fuentes.md`. La revisión R4 tampoco pudo leer el texto de Klaus y Simon y volvió a buscar el EPL sin resultado.

## Revisión adversarial R4 (17-11-2026)

Un segundo agente rehízo la teoría y recalculó umbrales, constantes, barridos, cajas y acción de pares con un método espectral de Chebyshev independiente (`revision/`). Todo coincide. Se corrigieron afirmaciones del texto (error real de la tabla U₁, orden del método primitivo, Y(2560) de 3d, ⟨r^n⟩ de ℓ = 2, atribución a Klaus y Simon) y se documentó un desfase sistemático de +5×10⁻¹¹ en la integral de camino. Detalle en `revision/informe_revision.md`.
- No se repitió con ℓ ≥ 1 el criterio completo de cajas de la Fase 3 (ternas, F½, condición (c)); aquí solo el signo, el punto fijo y el radio de cruce.
