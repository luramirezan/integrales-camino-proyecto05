---
title: "La Fase 2 explicada en sencillo"
subtitle: "Qué se hizo, qué salió, qué falló y qué hay que decidir · Proyecto 05 (umbral de ligadura del potencial de Yukawa)"
---

Para Luis Felipe Ramírez y Juan Sebastián Calixto · 9 de noviembre de 2026

Este documento es para leerlo de corrido, sin la bitácora al lado. Parte de lo que ya conocen de la Fase 1 y explica con palabras sencillas qué se construyó en la Fase 2, qué resultados salieron, qué no salió perfecto y qué significa cada una de las 10 decisiones que tienen que firmar. Las cifras son las de la bitácora (`fase2/bitacora_fase2.md`); cuando quieran el detalle, cada sección dice dónde buscar.

# 1. Recordatorio: de dónde venimos (Fase 1)

**La pregunta del proyecto.** Una partícula siente el potencial de Yukawa, $V(r) = -g\,e^{-\mu r}/r$. Es como el de Coulomb (el del átomo de hidrógeno), pero "apantallado": el factor $e^{-\mu r}$ lo apaga a distancias grandes. Si el apantallamiento $\mu$ es pequeño, la partícula queda ligada (hay un estado con energía negativa). Si $\mu$ crece demasiado, el pozo se vuelve tan corto que ya no la puede retener. **¿En qué valor de $\mu$ deja de existir el estado ligado?**

**Lo que ya dejamos hecho en la Fase 1:**

- **Adimensionalizamos.** Todo depende de un solo número, $\delta = \mu\hbar^2/(mg)$. Con $\delta = 0$ es Coulomb puro (energía exacta $-1/2$); al subir $\delta$ la energía sube hacia cero.
- **El umbral.** Con cotas analíticas (variacional y Bargmann) acotamos $1.19055 \le \delta_c \le 1.24305$, y con el solucionador numérico el valor de referencia es $\delta_c = 1.1906124211$.
- **El problema de la caja.** Cerca del umbral el estado se vuelve enorme: la partícula se aleja mucho. En una computadora la ponemos dentro de una esfera de radio $R$ (la "caja"). Si la caja es pequeña, puede engañarnos y hacernos decir "ligado" o "no ligado" sin razón. Por eso en la Fase 1 diseñamos un **criterio de cajas (9.6)**: no basta mirar el signo de la energía, hay que comparar varias cajas y mirar si el estado está localizado.
- **La integral de camino.** La guía pide resolver el problema también con una integral de camino en tiempo imaginario. En la Fase 1 vimos que la forma ingenua (la "acción primitiva") **no sirve** con $-1/r$: cerca del origen el peso crece como $e^{\epsilon/r}$ y explota. Decidimos usar la **acción de pares**, que mete la parte de Coulomb de forma exacta.
- **El plan de la Fase 2** (sección 9): qué métodos, qué parámetros y qué controles (9.7) tenía que cumplir el código.

# 2. Qué pedía la Fase 2

La guía del profesor dice, para nuestro proyecto: *"construir un solucionador radial y una formulación de tiempo imaginario que trate correctamente la singularidad; la primera exposición compara ambos en un punto fuertemente ligado"*.

En palabras simples:

1. Hacer **dos métodos completamente distintos** para calcular lo mismo: uno clásico (resolver la ecuación de Schrödinger) y otro con integrales de camino.
2. Ver que **coinciden** en un caso fácil, donde el estado está bien ligado. Elegimos $\delta = 0.2$.
3. Probarlos con **casos de control** cuya respuesta se conoce exactamente.
4. Declarar que el "peso" que se muestrea es **real, positivo y normalizable** (lo exige la guía para problemas con singularidades).
5. Entregar código que corra, el primer gráfico, la bitácora de IA y la primera presentación.

**Cómo se hizo.** Toda la Fase 2 la ejecutó la IA (Claude) el 27 de octubre, en un flujo de varios agentes. Después la revisaron otras dos instancias de Claude (V1 y V2) y, ya en noviembre, Gemini (otro modelo, que era lo que faltaba). **Ninguno de ustedes ha revisado todavía los resultados**, y por eso todas las "decisiones humanas" de la bitácora dicen "pendiente".

# 3. Las herramientas que se construyeron

## 3.1 El solucionador radial (la referencia)

Es el método "de libro": se escribe la ecuación radial $-\tfrac12 u'' + V u = E u$ con $u(0) = u(R) = 0$, se pone sobre una malla de puntos y se convierte en una matriz cuyo autovalor más bajo es la energía. Para el umbral se usa otro truco: integrar la ecuación con energía cero y buscar el $\delta$ donde la solución "se aplana" en el borde.

Es rápido y muy preciso, y por eso sirve de **referencia** para comparar el otro método. Resultados en $\delta = 0.2$: $E_0 = -0.3268085110$, $\langle r\rangle = 1.5497$ y $\langle r^2\rangle = 3.2259$. Pasa 7 de 7 pruebas (por ejemplo, da $-0.5$ en Coulomb con error de $6\times10^{-9}$).

## 3.2 La integral de camino: la idea en una página

En tiempo imaginario, el operador $e^{-\tau \hat H}$ funciona como un filtro: al aplicarlo durante un tiempo $\tau$ largo, todos los estados se apagan excepto el fundamental, que es el que decae más lento. Si se aplica muchas veces un paso pequeño $e^{-\epsilon \hat H}$, al final queda solo el estado fundamental, y de cuánto decae se lee su energía.

Cada paso pequeño es un "eslabón" $T(r, r'; \epsilon)$: la probabilidad (sin normalizar) de ir de $r$ a $r'$ en un tiempo $\epsilon$. Encadenar eslabones es sumar sobre todos los caminos posibles; eso es la integral de camino.

**El problema de la singularidad.** La receta más simple para el eslabón multiplica el movimiento libre por $e^{-\epsilon V}$. Con $V = -1/r$ eso es $e^{+\epsilon/r}$, que explota en $r \to 0$: un camino que pase cerca del origen tendría un peso infinito. Esa es la "acción primitiva" que la Fase 1 descartó.

**La solución: la acción de pares.** Se separa el potencial en dos partes:
$$V = \underbrace{-\frac1r}_{\text{Coulomb}} + \underbrace{W(r)}_{\text{resto}}, \qquad W(r) = \frac{1 - e^{-\delta r}}{r}.$$

La parte de Coulomb tiene solución exacta conocida, así que su eslabón se calcula **exacto** una sola vez y se guarda en una tabla ($U_C$). El resto $W$ es suave y acotado (vale entre 0 y $\delta$), así que se puede tratar con la receta simple sin peligro. El eslabón final es:
$$T = \underbrace{K_D}_{\text{movimiento libre}} \times \underbrace{e^{-U_C}}_{\text{Coulomb exacto}} \times \underbrace{e^{-\epsilon[W(r)+W(r')]/2}}_{\text{resto, mitad y mitad}}.$$

$K_D$ es el movimiento libre con una "imagen" que obliga a que la función se anule en $r = 0$. Toda la singularidad queda dentro de la parte exacta, y **no hubo que suavizar el potencial**.

**El precio.** Separar en dos partes introduce un error pequeño que depende del paso: el **error de Trotter**, que va como $\epsilon^2$. Se elimina calculando con varios $\epsilon$ (0.2, 0.1, 0.05) y extrapolando a $\epsilon \to 0$.

**Declaración del peso (lo que pide la guía).** El peso es:

- **Real:** todo son exponenciales reales.
- **Positivo:** se revisó elemento por elemento y hay 0 negativos.
- **Normalizable:** la parte de Coulomb exacta es finita en el origen ($U_C \approx -1.13$ en $r = 0.01$, frente al $e^{20}$ de la acción primitiva).

## 3.3 Dos formas de usar ese eslabón

**a) Matriz de transferencia (determinista).** Se pone el eslabón sobre una malla de puntos y queda una matriz. Su autovalor más grande $\lambda_0$ da la energía: $E_0 = -\ln\lambda_0/\epsilon$. No tiene ruido estadístico; es el método "integral de camino" más preciso que tenemos, y el que se usará para el umbral.

**b) PIGS (Monte Carlo).** *Path Integral Ground State*: en vez de sumar todos los caminos, se **muestrean** al azar con el algoritmo de Metropolis. Se parte de una función de prueba ($u_T = r e^{-r}$, que no es la exacta) y se deja evolucionar un tiempo $\tau$. Da resultados con barras de error ($\pm\sigma$). Es el método "de verdad" de integrales de camino, el que se generaliza a muchos cuerpos, pero es más ruidoso y más lento.

# 4. Los resultados principales

## 4.1 La comparación en el punto fuertemente ligado ($\delta = 0.2$)

| Método | $E_0$ | Diferencia con el radial |
|---|---|---|
| Radial (referencia) | $-0.3268085110$ | — |
| Transferencia, $\epsilon = 0.2$ | $-0.3268089611$ | $-4.5\times10^{-7}$ |
| Transferencia, $\epsilon = 0.05$ | $-0.3268085356$ | $-2.5\times10^{-8}$ |
| Transferencia extrapolada a $\epsilon \to 0$ | $-0.3268085066$ | $+4.4\times10^{-9}$ |
| PIGS ($\tau = 20$, 8 cadenas) | $-0.326725 \pm 0.000068$ | $+1.22\sigma$ |

**Cómo leerlo.** La transferencia, una vez extrapolada, coincide con el radial en 8 cifras: el error es de 4 milmillonésimas. El error de Trotter baja como $\epsilon^2$ (se midió un orden de 1.958, y debería ser 2). El PIGS coincide dentro de sus barras de error en las tres magnitudes: $+1.22\sigma$ en $E$, $+0.56\sigma$ en $\langle r\rangle$ y $+0.43\sigma$ en $\langle r^2\rangle$. "A $1.2\sigma$" significa que la diferencia es 1.2 veces la barra de error, algo normal; preocupa a partir de 2 o 3. **Esto responde la pregunta de la Fase 2.**

![Primer gráfico ($\delta = 0.2$). (a) Error de la energía frente al paso $\epsilon$: transferencia, extrapolación y PIGS. (b) y (c) $\langle r\rangle$ y $\langle r^2\rangle$ de los distintos métodos. (d) La energía "mixta" frente al tiempo de proyección $\tau$, con el punto anómalo de $\tau = 5$ y sus dos réplicas.](16_primer_grafico.png){width=95%}

## 4.2 Los casos de control

Un control es un problema parecido cuya respuesta se conoce exactamente. Si el código falla ahí, sabemos que algo está mal.

- **Coulomb ($\delta = 0$).** Con $\delta = 0$ el resto $W$ es cero y el método debería ser exacto. Da $|E + 0.5| \le 2.2\times10^{-7}$, que es solo error de malla.
- **Hulthén.** $V_H = -\delta/(e^{\delta r} - 1)$ tiene la **misma** singularidad $-1/r$ y la misma cola que el Yukawa, pero su energía se conoce exacta: $E = -\tfrac12(1 - \delta/2)^2$, con umbral en $\delta = 2$. Pasa por el mismo código sin cambiar nada y da la energía exacta con error de $\sim10^{-9}$ en $\delta = 0.2$, 1.0 y 1.5, es decir, hasta 3/4 del camino al umbral. **Es el control más fuerte que tenemos.** Esta fuente la pidió el profesor después de la Fase 1, y la referencia que la respalda es Cai, Cai e Inomata (1986), que muestran que Hulthén es exacto dentro de la integral de camino.
- **Pozo cuadrado.** No tiene singularidad, pero sí un salto brusco. Sirvió para descubrir algo: con el salto, el error de Trotter va como $\epsilon^{3/2}$ y no como $\epsilon^2$. Eso enseña que el método depende de que el potencial sea **suave**, no de la singularidad (que ya está resuelta). Por eso se propone usarlo solo como control cualitativo (decisión 4).

## 4.3 Primer avance sobre el umbral: el criterio de cajas

Aunque el umbral es tarea de las Fases 3 y 4, en la Fase 2 se completó la condición (c) del criterio de cajas: **la integral de camino tiene que dar el mismo veredicto que el radial en las mismas cajas**.

Se calcularon $\delta = 1.15$, 1.18 y 1.20 en cajas de radio $R = 50$ a 800 y se miraron tres cosas: la energía, el tamaño del estado comparado con la caja ($\langle r\rangle/R$) y la fracción de la partícula que está en la mitad interior ($F_{1/2}$).

| $\delta$ | Qué se ve | Veredicto |
|---|---|---|
| 1.15 | Energía negativa y estable; el estado no crece con la caja | **Ligado** |
| 1.18 | Ligado, pero hacen falta cajas de 200 a 800 para verlo ($F_{1/2} = 0.998$) | **Ligado** |
| 1.20 | Energía positiva, el estado crece con la caja y la energía sigue la ley de una partícula libre en la caja | **No ligado** |

Resultado: **$\delta_c$ está entre 1.18 y 1.20, con dos métodos independientes**, compatible con la referencia 1.1906.

**Por qué importa (y por qué la guía insiste en las cajas).** Si hubiéramos mirado solo la caja de $R = 50$ o $100$, en $\delta = 1.18$ habríamos dicho "no ligado", y nos habríamos equivocado. Además, con un paso $\epsilon$ grueso la integral de camino baja la energía hasta un 20 % y podría inventar un estado ligado. **Cerca del umbral solo vale la transferencia extrapolada.**

![Criterio de cajas: energía, $\langle r\rangle/R$ y $F_{1/2}$ frente al radio de la caja para $\delta = 1.15$, 1.18 y 1.20. Líneas: radial; círculos: integral de camino (transferencia extrapolada).](14_cajas.png){width=95%}

# 5. Cómo se comprobó que todo esto es cierto

1. **Pruebas automáticas.** Cada módulo tiene sus pruebas: radial 7/7, transferencia 7/7 y PIGS 14/14. Todas pasan.
2. **V1, recálculo independiente.** Otra instancia de Claude rehízo los números con código propio, sin usar el nuestro: de 252 cifras, 227 coinciden y las 25 restantes están explicadas. Ningún veredicto cambia.
3. **V2, auditoría adversarial.** Otra instancia buscó errores a propósito y encontró 20 hallazgos. **V3** es la respuesta: se corrigieron los que eran reales y se reejecutó todo.
4. **Tabla de controles.** Es un listado de todas las pruebas, cada una con su criterio fijado *antes* de ejecutar, el valor medido y si pasa o no. La genera un script leyendo los resultados, así que ninguna cifra está escrita a mano.
5. **Auditoría con Gemini (otro modelo).** Primero con Gemini Flash por API (con ejecución de código) y luego con Gemini 3.1 Pro en la app (sin ejecutar código), en 10 puntos separados. **No encontró ningún error de física ni de signo.** Rehízo con su propio código el $\delta_c$, la energía de $\delta = 0.2$, el orden de convergencia y la estadística de $\tau = 5$. Sí encontró errores de documento (los de la sección 7 de este documento) y que la tabla cuenta 6 controles dos veces.

**Una advertencia sobre Gemini.** En la app no ejecuta código, y lo admitió cuando se le preguntó. Además, varias referencias que dio eran de memoria y algunas falsas: por ejemplo, dijo que Cai, Cai e Inomata salió en "J. Math. Phys.", cuando es Phys. Rev. A 34, 4621. Por eso cada cosa que dijo se comprobó antes de aceptarla, y ninguna cita suya entra a la bitácora sin verificarla.

# 6. Lo que no salió perfecto (y por qué no es grave)

La tabla tiene **82 controles distintos: 64 pasan, 9 no pasan y 9 son medidos** (magnitudes que solo se reportan). Los "no pasa" **no se escondieron ni se cambiaron las tolerancias para que pasaran**: quedan en la tabla con su causa medida. Se agrupan en cinco causas:

| Causa | Controles | Explicación sencilla |
|---|---|---|
| **La cúspide de Coulomb y la malla** | A5, A7, A13, E1 | En el origen la función de onda tiene una "punta" (cúspide). La regla del trapecio comete ahí un error pequeño, de orden $h^4/\epsilon$, mayor que la tolerancia de $10^{-6}$ que se había fijado. La causa está medida y confirmada por V1. Se arregla extrapolando en $h$ (Richardson), y con eso todo pasa. **Decisión 1.** |
| **La pared de la caja** | C4 | En el borde $R$ el eslabón no tiene "imagen", así que los caminos pueden asomarse un poco fuera entre dos pasos. La pared queda efectivamente en $R + 0.58\sqrt\epsilon$. En cajas pequeñas eso estropea el orden de convergencia, pero no cambia ningún veredicto. **Decisión 5.** |
| **La malla cerca del umbral** | C5 | Cerca del umbral la convergencia en $h$ no es de orden 4 sino 1.4 a 2.3. Solo obliga a usar mallas más finas en la Fase 3. |
| **La anomalía de $\tau = 5$ en el PIGS** | A16 | Un punto del PIGS quedó a $-3.2\sigma$, cuando lo normal es menos de 2. Se repitió dos veces con otras semillas y dio $+0.03\sigma$ y $+0.99\sigma$. Pero las tres corridas no son del todo compatibles entre sí ($p = 0.011$): probablemente es mala suerte estadística, aunque no se puede descartar que el error esté subestimado. **Decisión 2.** |
| **Criterios mal planteados o al límite** | B27, D19 | B27: un ajuste de robustez del pozo cuadrado (decisión 4). D19: se pidió una precisión de $10^{-10}$ a una suma que por construcción tiene error $h^2$; el criterio estaba mal puesto desde el principio. |

# 7. Las 10 decisiones: qué significa cada una

**Por qué hay que decidir.** La IA hizo todo, pero en el método científico (y en la guía del profesor) las decisiones las toma el equipo, y deben quedar registradas en la bitácora de IA como "decisión humana". Mientras no las firmen, la Fase 2 no está cerrada formalmente (criterios K4, K5 y K6 de la bitácora).

**Quién firma qué.** Por la regla de roles que aprobaron el 21-10-2026, quien implementa no verifica. En la Fase 2 implementó Lucho (a través de la IA) y verifica Juan Sebastián, así que las decisiones 1 a 7 son de Juan Sebastián y las 8 a 10, de los dos. En la Fase 3 se invierte.

## Decisión 1. Cambiar la forma de medir que la malla está bien

- **El problema:** el control decía "el resultado no debe cambiar más de $10^{-6}$ al pasar de la malla 0.04 a la 0.02". Falla en 4 de 9 casos por la cúspide de Coulomb (sección 6).
- **Lo que se propone:** en vez de exigir que dos mallas den lo mismo, extrapolar a malla cero (Richardson con exponente 4, que es el orden medido) y exigir que el valor extrapolado sea estable.
- **Si dicen Sí:** el control se redefine y pasa. Es lo correcto, porque el error tiene causa conocida y se corrige.
- **Si dicen No:** queda como "no pasa" y hay que explicarlo en la presentación.
- **Recomendación: Sí.**

## Decisión 2. Qué decir de la anomalía de $\tau = 5$

- **El problema:** el punto de $\tau = 5$ del PIGS quedó raro ($-3.2\sigma$); las repeticiones salieron bien, pero las tres corridas juntas no son del todo coherentes ($p = 0.011$, es decir, algo así pasaría por azar 1 de cada 100 veces).
- **Lo que se propone:** no esconderlo ni borrar la corrida mala (eso sería trampa), mostrar las tres en la presentación y dejarlo "abierto" para estudiarlo en la Fase 3.
- **Cambio por la auditoría:** la opción original decía "no hay sesgo del muestreador", y Gemini señaló, con razón, que eso es más de lo que los datos permiten afirmar. Redacción nueva: *"las corridas muestran heterogeneidad estadística; la causa (fluctuación poco probable o error subestimado) no se puede determinar con los datos actuales y queda abierta"*.
- **Recomendación: Sí, con la redacción nueva.**

## Decisión 3. El número que decide "no ligado"

- **El problema:** para declarar "no ligado" se compara la energía con la de una partícula libre dentro de la caja; si se parece, el estado no está ligado. Hacía falta un número para "se parece": la IA eligió una desviación menor que 0.1 (10 %), porque el plan no daba ninguno.
- **El detalle incómodo:** ese 0.1 se eligió **después** de ver los datos de la Fase 2. En $\delta = 1.20$ una de las ternas dio 0.101, justo al borde. El veredicto no depende de eso (otra terna da 0.021), pero en ciencia los criterios se fijan antes de mirar.
- **Lo que se propone:** aprobar el 0.1, **declarar** cómo se eligió y **dejarlo fijo desde ya para la Fase 3**, antes de ver sus datos.
- **Recomendación: Sí.** Es urgente, porque hay que fijarlo antes de calcular la Fase 3.

## Decisión 4. Qué papel tiene el pozo cuadrado

- **El problema:** con el pozo, el error no baja como se esperaba ($\epsilon^{3/2}$ en vez de $\epsilon^2$). La razón es el salto brusco del potencial. No tenemos demostración ni fuente para el 3/2, solo la medición.
- **Lo que se propone:** usar el pozo como control **cualitativo** (enseña que el problema es la suavidad del potencial y no la singularidad) y Hulthén como control **cuantitativo** (el que da los números exactos). No presentar el 3/2 como resultado demostrado.
- **Recomendación: Sí.**

## Decisión 5. La pared del borde de la caja

- **El problema:** en el origen el eslabón tiene una "imagen" que impide que los caminos crucen. En el borde $R$ no la tiene, así que la caja es efectivamente un poco más grande: $R + 0.58\sqrt\epsilon$.
- **Las opciones:**
    - **(a) Poner la imagen también en $R$.** Es más limpio, pero cambia el método aprobado y obliga a programarlo y validarlo de nuevo.
    - **(b) Dejarlo como está y sumar ese efecto a la barra de error.** Es lo que se hace hoy, y Gemini comprobó que los veredictos no dependen de esto.
- **Recomendación: (b) para la Fase 3**, por el poco tiempo; (a) puede quedar como mejora de la Fase 4. También es urgente, porque hay que decidirlo antes de calcular.

## Decisión 6. Una corrección técnica de la tabla de Coulomb

- **El problema:** la tabla exacta de Coulomb solo llega hasta $r = 10$. Más allá se usa una aproximación que tenía un error de $1.7\times10^{-6}$, no menor que $10^{-7}$ como decía el código. Se le añadió un término de corrección (Wigner-Kirkwood) y el error bajó a $8\times10^{-9}$.
- **Lo que se decide:** aceptar esa corrección como parte del método. No cambia nada dentro de $r \le 10$.
- **Recomendación: Sí.**

## Decisión 7. Firmar la tabla de controles

- **Lo que se decide:** que Juan Sebastián, como verificador, firme la tabla de controles.
- **Corrección de la auditoría:** la tabla dice 88 filas, pero 6 controles (Hellmann-Feynman en tres valores de $\delta$, el virial, las cotas y "no ligado en $\delta \ge 2$") aparecen dos veces, en los bloques A y D. Son **82 controles distintos: 64 pasan, 9 no, 9 medidos**. Se propone declararlo en el resumen sin borrar filas, para que no cambien los números de fila que cita la bitácora.
- **Recomendación: Sí, con el conteo corregido.**

## Decisión 8. Qué figuras se congelan

- **El problema:** "congelar" una figura significa que ya no se cambia, y se guarda su huella digital (sha256) para demostrarlo. Hay dos versiones del primer gráfico: la 16 (cuatro paneles, la de este documento) y la 18 (hecha para las diapositivas).
- **Lo que se decide:** congelar las figuras y escoger una de las dos para la presentación.
- **Recomendación: congelar todas y usar la 18 en las diapositivas**, añadiendo en el pie que algunos puntos están corridos en el eje x a propósito, para que no se tapen.

## Decisión 9. Aprobar la bitácora y el registro de IA

- **Lo que se decide:** si la bitácora de la Fase 2 y su registro de IA quedan aprobados como el registro oficial.
- **Recomendación: Sí, después de aplicar las correcciones de texto de la auditoría** y de añadir al registro las fichas de Gemini (qué modelo, qué se le preguntó, qué respondió y qué se hizo con eso). Con eso queda cumplido lo que pedía la guía: una auditoría hecha por un modelo distinto de Claude.

## Decisión 10. La presentación y la tabla de fuentes

- **Lo que se decide:** aprobar el material de la presentación después de ensayarlo, y aceptar la tabla de fuentes de los controles.
- **Presentación:** el miércoles 11-11, 15 minutos, la dan los dos, y cubre las Fases 2 y 3.
- **Dos notas en las fuentes:**
    - Roy cita $\delta_c = 1.19061227 \pm 4\times10^{-8}$; el nuestro, recalculado dos veces con códigos distintos, es 1.1906124211. Hay una pequeña discrepancia que conviene anotar, no esconder.
    - El año de la referencia H8 no cuadra (arXiv de 2001, revista de 2000) y hay que verificarlo.
- **Recomendación: Sí.**

# 8. Glosario rápido

| Término | Qué es |
|---|---|
| $\delta$ | Apantallamiento adimensional. Si es pequeño, está ligado; si es grande, no. El umbral está en $\approx 1.19$. |
| $\epsilon$ | Paso de tiempo imaginario de cada eslabón. Más pequeño es más preciso y más caro. |
| $\tau = M\epsilon$ | Tiempo total de proyección. Más largo filtra mejor el estado fundamental. |
| $h$ | Separación de la malla espacial. |
| $R$ | Radio de la caja esférica donde se encierra la partícula. |
| Error de Trotter | Error por separar el potencial en dos partes en cada paso; va como $\epsilon^2$. |
| Richardson / extrapolar | Calcular con dos o tres pasos distintos y deducir cuánto daría con paso cero, sabiendo cómo baja el error. |
| Orden (de convergencia) | La potencia con que baja el error: orden 2 significa que con la mitad del paso el error es 4 veces menor. |
| $\sigma$ | Barra de error estadística. "A $1.2\sigma$" significa que la diferencia es 1.2 barras de error: normal. Más de 3 es raro. |
| $p$ (valor p) | Probabilidad de ver algo así de raro por puro azar. $p = 0.01$ es 1 de cada 100. |
| $\chi^2$ | Número que mide qué tan compatibles son varias mediciones entre sí. |
| Cúspide | La "punta" que tiene la función de onda en el origen por culpa de $-1/r$. |
| $\langle r\rangle$, $F_{1/2}$ | Tamaño medio del estado y fracción de la partícula en la mitad interior de la caja. Sirven para saber si el estado está localizado. |
| $a_s$ | Longitud de dispersión. Cerca del umbral es enorme ($-143$ en $\delta = 1.20$) y dice cómo se comporta un estado no ligado en la caja. |

# 9. Preguntas que podría hacer el profesor

**¿Por qué dos métodos?**
Porque si dos métodos con supuestos completamente distintos dan lo mismo, es muy poco probable que los dos estén mal de la misma manera. Además, el radial es la referencia que pide la guía.

**¿Cómo trataron la singularidad?**
No la suavizamos: la parte $-1/r$ va en un eslabón exacto (la acción de pares) y solo el resto suave se aproxima. El peso es real, positivo y normalizable, y lo comprobamos elemento por elemento.

**¿Cómo saben que el código está bien?**
Por los controles exactos: Coulomb, y sobre todo Hulthén, que tiene la misma singularidad y la energía exacta, con error de $10^{-9}$. También por un recálculo independiente y por la auditoría de otro modelo.

**¿Qué pasó con $\tau = 5$?**
Un punto salió a $3\sigma$; lo repetimos dos veces y salió bien, pero las tres corridas juntas tienen $p \approx 1\%$. No lo borramos, lo mostramos y queda abierto para la Fase 3.

**¿Por qué tantas cajas?**
Porque cerca del umbral una caja pequeña engaña: en $\delta = 1.18$, con $R = 100$ habríamos dicho "no ligado" y está ligado.

**¿Qué hizo la IA y qué hicieron ustedes?**
Responderlo con honestidad: la IA hizo el cálculo y la redacción; ustedes definieron el problema y el plan en la Fase 1, revisan, deciden y firman. Gemini auditó. Todo queda en el registro de IA.

# 10. Qué sigue (Fase 3, en una línea)

La guía pide **barrer $\mu$ y el tamaño de caja, estudiar la convergencia temporal y pedir a la IA una auditoría adversarial de los autovalores cercanos a cero**, con un borrador del artículo, figuras con barras de error y la tabla de controles. Para arrancar hacen falta las decisiones 3 y 5. El plan está en `fase2/que_sigue_fase3.md` y en el documento "Fase 2 cerrada y arranque de Fase 3".
