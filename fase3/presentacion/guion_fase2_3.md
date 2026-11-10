# Guion de la presentación de las Fases 2 y 3

Proyecto 05 · 11 de noviembre de 2026 · 15 minutos · Juan Sebastián Calixto (JS) y Luis Felipe Ramírez (LF).
Tiempos a 140 palabras por minuto. Las notas del orador de cada lámina tienen el mismo texto.

| # | Lámina | Quién | Palabras | Tiempo |
|---|---|---|---|---|
| 1 | Portada | Juan Sebastián | 74 | 32 s |
| 2 | La pregunta y lo que traíamos de la Fase 1 | Juan Sebastián | 98 | 42 s |
| 3 | La acción de pares: la singularidad va en la parte exacta | Juan Sebastián | 116 | 50 s |
| 4 | Fase 2: los tres métodos coinciden en δ = 0.2 | Juan Sebastián | 100 | 43 s |
| 5 | Fase 2: controles con solución exacta | Juan Sebastián | 123 | 53 s |
| 6 | Fase 3: qué pide la guía y qué fijamos antes de calcular | Luis Felipe | 102 | 44 s |
| 7 | Convergencia temporal y espacial | Luis Felipe | 112 | 48 s |
| 8 | Barrido en el apantallamiento: E0(δ) y ⟨r⟩(δ) | Luis Felipe | 114 | 49 s |
| 9 | Prueba de cajas cerca del umbral | Luis Felipe | 92 | 39 s |
| 10 | Un autovalor cercano a cero: δ = 1.19 | Luis Felipe | 151 | 65 s |
| 11 | Controles de la Fase 3 y auditoría con otra IA | Luis Felipe | 159 | 68 s |
| 12 | Conclusiones y qué sigue | Juan Sebastián | 106 | 45 s |
| 13 | Respaldo: tabla de veredictos | (respaldo) | 0 | 0 s |
| 14 | Respaldo: lo que no pasa y por qué | (respaldo) | 0 | 0 s |
| 15 | Respaldo: uso de IA | (respaldo) | 0 | 0 s |

**Total expuesto:** 1347 palabras, unos 9.6 min (de 15; queda margen para señalar figuras y para preguntas). Juan Sebastián: 617 palabras (4.4 min), Luis Felipe: 730 palabras (5.2 min).

## 1. Portada (Juan Sebastián)

Buenos días. Somos Juan Sebastián y Luis Felipe, proyecto 05. La pregunta es en qué apantallamiento deja de existir el estado ligado 1s del potencial de Yukawa. Todo depende de un número, delta igual a mu por h barra al cuadrado sobre m g. Hoy mostramos las Fases 2 y 3: cómo calculamos con una integral de camino que trata bien la singularidad, cómo la validamos y qué dice el barrido cerca del umbral.

## 2. La pregunta y lo que traíamos de la Fase 1 (Juan Sebastián)

En la Fase 1 adimensionalizamos, acotamos el umbral entre 1.19055 y 1.24305 con cotas variacional y de Bargmann, y obtuvimos la referencia 1.1906124211 por integración a energía cero. Vimos dos riesgos. Primero, la integral de camino ingenua no sirve con menos uno sobre r: el peso crece como e a la épsilon sobre r y no es normalizable. Segundo, cerca del umbral el estado se vuelve enorme y una caja finita puede inventar la conclusión. Por eso diseñamos un criterio que compara varias cajas y mira si el estado está localizado, no solo el signo de la energía.

## 3. La acción de pares: la singularidad va en la parte exacta (Juan Sebastián)

Separamos el potencial en Coulomb más un resto W, que es suave y está entre cero y delta. El eslabón de tiempo imaginario es el núcleo libre con una imagen en el origen, por el factor exacto de Coulomb, por el resto repartido mitad y mitad. Toda la singularidad queda en la parte exacta, que se tabula una vez. El precio es un error de Trotter de orden épsilon al cuadrado, que eliminamos extrapolando. La guía pide declarar el peso: es real, positivo, con cero elementos negativos, y normalizable, porque U_C es finita en el origen. No suavizamos el potencial. Lo evaluamos de dos formas: como matriz de transferencia, sin ruido, y como Monte Carlo PIGS.

## 4. Fase 2: los tres métodos coinciden en δ = 0.2 (Juan Sebastián)

Este es el primer gráfico. En delta igual a 0.2 el radial da menos 0.3268085110. La transferencia, extrapolada en épsilon y en la malla, queda a 4 milmillonésimas, y su error baja como épsilon al cuadrado: orden medido 1.96. El PIGS coincide dentro de su barra de error en las tres magnitudes: 1.2, 0.6 y 0.4 sigma. El panel d muestra la proyección en tiempo imaginario: un punto, tau igual a 5, salió a menos 3.2 sigma. Lo repetimos dos veces y salió bien, pero las tres corridas juntas tienen p de 1 por ciento. No lo borramos: queda abierto.

## 5. Fase 2: controles con solución exacta (Juan Sebastián)

Para confiar en el código lo probamos con problemas cuya respuesta se conoce. Coulomb, delta igual a cero: el método es exacto y solo queda error de malla, 2 por 10 a la menos 7. Hulthén tiene la misma singularidad y la misma cola que el Yukawa y su energía es exacta: pasa por el mismo código sin cambiar nada y da la energía exacta a 10 a la menos 9, hasta tres cuartos del camino a su umbral. Es nuestro control más fuerte; la fuente es Cai, Cai e Inomata 1986. El pozo cuadrado, con un salto, da Trotter de orden 3 medios: enseña que el método depende de la suavidad del potencial, no de la singularidad. Lo usamos como control cualitativo.

## 6. Fase 3: qué pide la guía y qué fijamos antes de calcular (Luis Felipe)

La guía pide para la Fase 3 barrer mu y el tamaño de caja, estudiar la convergencia temporal y pedir a una IA una auditoría adversarial de autovalores cercanos a cero. Antes de ver ningún dato fijamos tres cosas. El umbral de la ley de caja para declarar no ligado: 0.1. La receta de extrapolación: Richardson en h con exponente 4 y épsilon al cuadrado. Y que la pared en R, que en el núcleo no tiene imagen, no se corrige: se mide y se suma a la barra de error. Cambiamos los roles: ahora implementa Juan Sebastián y verifica Luis Felipe.

## 7. Convergencia temporal y espacial (Luis Felipe)

Primero, convergencia. Medimos el error en cuatro deltas, con cuatro pasos de tiempo y tres mallas. El error de Trotter baja con pendiente 2 en todos los casos, de 1.96 a 1.99, y el de la malla con pendiente 4. El dato importante es que el sesgo crece hacia el umbral: con épsilon 0.1 es 4 diezmillonésimas de la energía en delta 0.2 y casi el 1 por ciento en 1.15. Sin extrapolar, cerca del umbral llega al 20 por ciento y siempre hacia abajo, o sea, podría fabricar un estado ligado. Extrapolado, el resultado queda a menos de 5 por 10 a la menos 9 del radial en los cuatro casos.

## 8. Barrido en el apantallamiento: E0(δ) y ⟨r⟩(δ) (Luis Felipe)

El barrido en delta, que es barrer mu a g fijo. A la izquierda la energía: los dos métodos coinciden en los ocho valores con diferencia máxima de 2 por 10 a la menos 8. En el centro la extensión: el radio medio pasa de 1.5 a más de mil al acercarse al umbral. A la derecha, kappa, la raíz de menos dos E, frente a la distancia al umbral: es una recta, kappa igual a 0.741 por delta c menos delta. Eso quiere decir que la energía se anula cuadráticamente, y radio medio por kappa tiende a un medio: el estado es su cola exponencial. Este es el avance de la Fase 4.

## 9. Prueba de cajas cerca del umbral (Luis Felipe)

Ahora la prueba de cajas: cinco deltas y siete cajas, de 50 a 3200. En las 35 celdas la integral de camino coincide con el radial. 1.15 y 1.18 salen ligados; 1.20 y 1.25, no ligados: en 1.20 la energía sigue la ley de una partícula libre en la caja con longitud de dispersión menos 143. Fíjense en 1.18, la curva verde: con cajas de 50 o 100 la energía es positiva y habríamos dicho no ligado. Con 200 a 800 se ve que está ligado. Por eso no basta el signo.

## 10. Un autovalor cercano a cero: δ = 1.19 (Luis Felipe)

El caso difícil es 1.19, a seis diezmilésimas del umbral. Con caja 1600 la energía es positiva; con 3200 es negativa, y los dos métodos coinciden en las dos. ¿Es un estado o un artefacto? Lo decide la localización. Con el radial en cajas hasta 25600, la energía se estabiliza en menos 1.03 por 10 a la menos 7, el radio relativo baja de 0.23 a 0.04 y la fracción interior sube a 0.99999. El estado mide unas 1100 unidades, del orden de la longitud de dispersión, 2204: esa es la escala que la caja tiene que superar. Y la integral de camino también llega: cambiando el solucionador de autovalores por una factorización en banda, la evaluamos en cajas de 6400 y 12800. Los dos métodos dan ligado en la terna 3200, 6400, 12800 y la condición (c) se cumple: delta c está entre 1.19 y 1.20 con los dos métodos.

## 11. Controles de la Fase 3 y auditoría con otra IA (Luis Felipe)

La tabla de controles de la Fase 3 tiene 40 controles distintos: 28 pasan, 3 no pasan y 9 son medidos. Los tres que no pasan tienen causa medida. El más interesante: el orden de Trotter sale bajo en las cajas donde el estado toca la pared; al comparar con el radial en la caja corrida 0.58 raíz de épsilon vuelve a 1.99 en las nueve celdas probadas. La auditoría adversarial de los autovalores cercanos a cero se la pedimos a Gemini 3.1 Pro, un modelo distinto de Claude, como pide el profesor; nos dio siete hallazgos y comprobamos cada uno calculando. Seis no se sostienen: por ejemplo, decía que la malla fabricaba el estado ligado, pero el sesgo de la malla va hacia arriba y una integración sin malla da la misma energía. El séptimo era válido: la condición (c) no llegaba a cajas mayores de 3200. Lo resolvimos con la integral de camino en 6400 y 12800.

## 12. Conclusiones y qué sigue (Juan Sebastián)

En resumen. La acción de pares trata exactamente la singularidad con un peso real, positivo y normalizable, y reproduce los controles exactos a 10 a la menos 9. Con los dos métodos y el criterio de cajas, delta c está entre 1.19 y 1.20, compatible con la referencia; la solución a energía cero lo afina a entre 1.1906 y 1.1907. Lo que separa un estado débil de un artefacto es comparar cajas y mirar la localización, no el signo de un autovalor. Para la Fase 4: estudiar la ley de la extensión, cerrar la anomalía del PIGS y escribir el artículo; ya tenemos el borrador. Gracias.

## Preguntas probables

- **¿Por qué no basta el signo de la energía?** Porque en δ = 1.18 con R ≤ 100 y en δ = 1.19 con R ≤ 1600 el signo es positivo y el estado sí está ligado: lo que decide es comparar cajas y mirar ⟨r⟩/R y F½.
- **¿Cómo llegó la integral de camino a R = 12800?** La factorización dispersa del modo shift-invert con N ≈ 320 000 y 313 diagonales no cabía en memoria. La matriz es de banda, así que usamos LU en banda de LAPACK e iteración inversa: misma acción y misma receta, solo cambia el álgebra lineal. R = 12800 (N = 640 000) tarda unos 3 minutos.
- **¿Cómo saben que δ = 1.19 no es un artefacto de la malla?** El sesgo de la malla va hacia arriba (h = 1/40 da E > 0), así que puede esconder un ligado pero no inventarlo. Una integración sin malla ni caja da E0 = −1.0303×10⁻⁷, y la solución a energía cero tiene un nodo en r ≈ a_s = 2204.
- **¿Qué hizo la IA y qué ustedes?** La IA calculó y redactó; nosotros fijamos la pregunta, el plan y las decisiones (umbral 0.1 antes de los datos, pared en el error), revisamos y firmamos. Gemini auditó.
- **¿Qué pasa con τ = 5?** Sigue abierta (p ≈ 1 %); no se borró la corrida. Se estudia con la autocorrelación en la Fase 4.
- **¿Por qué Hulthén?** Tiene la misma singularidad y la misma cola, y su energía es exacta: prueba el método completo donde sabemos la respuesta.
