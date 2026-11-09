# Guion de la Fase 1: umbral de enlace en el potencial de Yukawa

> Grupo de dos integrantes (Valentina Isabel Burbano se retiró del equipo).

**Presentan:** Juan Sebastián Calixto (JS) y Luis Felipe Ramírez (LF) · **Duración:** unos 14 min 55 s de exposición, más 5 min de discusión.

Versión de 15 minutos (19 de octubre de 2026), pedida por Lucho. Diapositivas: `diapositivas_fase1.pptx` (18 láminas; la 18 es de respaldo y no se expone). Cada cifra que se dice en voz alta sale de un script de `codigo/`, que se indica al final de cada bloque. Ritmo de referencia: unas 150 palabras por minuto.

| # | Diapositiva | Quién | Tiempo |
|---|---|---|---|
| 1 | Portada | Juan Sebastián | 25 s |
| 2 | La pregunta, el régimen y el criterio de cierre | Juan Sebastián | 55 s |
| 3 | Adimensionalización: todo depende de δ = μa | Juan Sebastián | 40 s |
| 4 | Condiciones de frontera | Juan Sebastián | 40 s |
| 5 | Límite de Coulomb δ → 0 | Juan Sebastián | 45 s |
| 6 | Toy model: Hulthén exacto y pozo esférico cuadrado | Juan Sebastián | 60 s |
| 7 | Cota inferior variacional: δc ≥ 1.19055 | Juan Sebastián | 60 s |
| 8 | Límites físicos propuestos por la IA y su verificación | Juan Sebastián | 70 s |
| 9 | Auditoría de la IA: qué se corrigió | Juan Sebastián | 60 s |
| 10 | Cotas superiores: δc ≤ 1.24305 | Luis Felipe | 50 s |
| 11 | Referencia numérica: δc = 1.1906124211 | Luis Felipe | 40 s |
| 12 | Acción euclídea y veredicto sobre el peso | Luis Felipe | 65 s |
| 13 | Por qué falla el peso primitivo y qué lo arregla | Luis Felipe | 70 s |
| 14 | El hallazgo de la caja finita | Luis Felipe | 70 s |
| 15 | Plan de cómputo: método, controles y costo | Luis Felipe | 55 s |
| 16 | Resultado de la Fase 1 | Luis Felipe | 30 s |
| 17 | Qué sigue en la Fase 2 | Luis Felipe | 60 s |
| 18 | Respaldo: fuentes y estado de verificación | (no se expone) | 0 s |

Reparto: Juan Sebastián 1 a 9 (7 min 35 s: pregunta, formulación, toy model, cota inferior e IA) · Luis Felipe 10 a 17 (7 min 20 s: cotas superiores, referencia, acción y peso, caja, plan y Fase 2). Total: 14 min 55 s (2224 palabras, unas 150 por minuto; los tiempos de cada lámina salen del número de palabras). El reparto concreto de bloques es una propuesta y queda pendiente de confirmar por el equipo (`decisiones_pendientes.md`, decisión 6).

Cambios respecto a la versión de 9 minutos: se añadieron el toy model (6), la auditoría de la IA (9), la divergencia del peso con la acción de pares (13), el hallazgo de la caja finita (14) y una lámina final explícita sobre la Fase 2 (17); la lámina de cotas se separó de nuevo en cota inferior (7) y cotas superiores (10), con la gráfica de cotas más grande; el plan (15) se centra ahora en método, controles y costo, porque el riesgo de la caja tiene lámina propia. Se corrigió el corte de "9/|E0|" en la lámina del plan.

## 1. Portada (Juan Sebastián, 25 s)

> Buenos días. Somos Juan Sebastián Calixto y Luis Felipe Ramírez, y presentamos la Fase 1 del proyecto 5: el umbral de enlace en el potencial de Yukawa. Si apantallamos la atracción de Coulomb con una exponencial, ¿cuándo deja de existir el estado ligado? Yo presento la formulación, las cotas por abajo y el trabajo con la IA; Luis Felipe, la acción, la caja y el plan.

## 2. La pregunta, el régimen y el criterio de cierre (Juan Sebastián, 55 s)

> La pregunta es esta: ¿para qué apantallamiento mu, con g, m y hbar fijos, deja de existir el estado fundamental ligado, y cómo se comportan su energía y su radio medio al acercarse? Todo depende de un solo número, delta igual a mu hbar cuadrado sobre m g. En unidades físicas el umbral es mu c igual a delta c por m g sobre hbar cuadrado. El régimen es no relativista, sin espín, con potencial estático y central, y solo onda s: si hay algún ligado, el 1s lo está. La fase se cierra con cotas y una referencia independiente de la caja, la lista de límites de la IA verificada, la acción con el peso declarado y el plan de cómputo. Lo único que falta es que el equipo confirme por escrito las decisiones del registro de IA.

## 3. Adimensionalización (Juan Sebastián, 40 s)

> Primero adimensionalizamos. La longitud natural es el radio de Bohr generalizado, a igual a hbar cuadrado sobre m g, y la energía es E H igual a g sobre a. Con cuatro parámetros y tres dimensiones, el teorema Pi deja un único número: delta igual a mu por a, el tamaño del átomo dividido por el alcance del potencial. La ecuación radial queda como ven, y sympy confirma que la diferencia con la original es exactamente cero. La figura muestra el potencial para varios delta: al crecer delta el pozo se acorta. Por eso el umbral es un número puro, delta c.

Cifras: `01_adimensionalizacion.py`.

## 4. Condiciones de frontera (Juan Sebastián, 40 s)

> Las condiciones de frontera salen de los extremos. Cerca del origen la solución regular va como x a la l más uno, así que w de cero es cero; para l igual a cero empieza como x menos x cuadrado. En el infinito decae como e a la menos kappa x, con kappa igual a la raíz de menos dos epsilon. En el umbral kappa tiende a cero y el radio medio diverge: el estado se vuelve un halo, y eso hace crítico el tamaño de la caja. Sigo con el límite de Coulomb.

## 5. Límite de Coulomb (Juan Sebastián, 45 s)

> Con delta igual a cero, w igual a x por e a la menos x y epsilon igual a menos un medio dan residuo exactamente cero, y el radio medio es tres medios: es el hidrógeno. Para delta pequeño, la teoría de perturbaciones da la serie que ven; el coeficiente de delta a la cuarta, menos once dieciseisavos, combina el primer orden y el segundo orden calculado con Dalgarno y Lewis. Pero la serie solo sirve cerca de cero: en delta igual a 0.3 la serie a segundo orden ya se desvía en una centésima, casi un 4 por ciento de la energía. No sirve para estimar el umbral.

Cifras: `02_limite_coulomb.py` (en δ = 0.3: orden 2, 9.861×10⁻³, 3.83 %; orden 4, 1.930×10⁻³, 0.75 %).

## 6. Toy model: Hulthén y pozo cuadrado (Juan Sebastián, 60 s)

> Antes de atacar el Yukawa resolvimos dos versiones exactas del mismo problema. La primera es el potencial de Hulthén: tiene la misma singularidad menos uno sobre r en el origen y la misma cola exponencial, pero se resuelve a mano. La energía es menos un medio por uno menos delta medios al cuadrado, así que el umbral exacto es delta igual a dos. Además, el Yukawa queda encerrado entre dos Hulthén, con delta y con dos delta: eso da una tercera prueba de que delta c está entre uno y dos. La segunda es el pozo esférico cuadrado, con umbral pi cuadrado octavos. La lección es que la forma de la ley de umbral es general: kappa crece linealmente con la distancia al umbral. El coeficiente, en cambio, depende del perfil: un medio en Hulthén, 0.741 en Yukawa. Y Hulthén nos servirá en la Fase 2 como control exacto con la misma singularidad.

Cifras: `00_toy_model.py` (umbral 2s de Yukawa 0.310209 frente a 1/2; en δ = 0.5: −0.281250 ≤ −0.148117 ≤ −0.125000; κ/(δc − δ) = 0.7464 y 0.7435 en δ = 1.10 y 1.15); el 0.741 extrapolado sale de `07_limites_fisicos.py`.

## 7. Cota inferior variacional (Juan Sebastián, 60 s)

> Ahora encerramos el umbral por abajo. El principio variacional dice que cualquier función de prueba da una energía mayor o igual que la verdadera. Como el continuo empieza en cero, basta encontrar una prueba con energía negativa para demostrar que hay un estado ligado. Con la prueba hidrogenoide e a la menos r sobre b, la condición es un polinomio en b cuyo discriminante es menos sesenta y cuatro por delta menos uno: hay ligado para todo delta menor que uno. El uno no es del potencial, es de la prueba, que tiene una sola escala. Añadir un polinomio no ayuda: uno más c r equivale a cambiar b, y las energías coinciden a diez a la menos catorce. Lo que sí ayuda es añadir escalas, como en la tabla: con dos exponenciales la cota sube a 1.1476, y con doce a 1.19055, por debajo de la referencia, como debe ser. Ahora, la IA.

Cifras: `03_cota_variacional.py` (N = 2: 1.147636; N = 4: 1.184635; N = 8: 1.190195; N = 12: 1.190550; diferencia máxima 9.8×10⁻¹⁵ en δ ∈ [0, 0.99]).

## 8. Límites físicos propuestos por la IA (Juan Sebastián, 70 s)

> La guía pide pedirle a la IA una lista de límites físicos que el algoritmo debe cumplir, y verificarla. El 12 de octubre le pedimos a Claude esa lista, para el solucionador radial y para la integral de camino, y guardamos la respuesta antes de comprobar nada. Dio diecinueve ítems y verificamos cada uno con un script. El límite de Coulomb y Hellmann-Feynman se cumplen a seis cifras o más. En el umbral, la IA dijo que kappa crece linealmente con pendiente 0.75; el cálculo da 0.741, así que lo precisamos. El sesgo de caja sigue la ley 1.35 sobre R. La corrección importante es la L13: la IA dijo que un estado no ligado en una caja cumple E por R cuadrado igual a pi cuadrado medios. Con cajas accesibles es falso, porque falta la longitud de dispersión. El peso lo verá Luis Felipe, y el error de Trotter solo se puede probar en la Fase 2. Adoptar esta lista como batería de pruebas está pendiente de confirmar por el equipo.

Cifras: `07_limites_fisicos.py` (balance: 14 confirmados, 3 precisados, 1 corregido, 1 solo en Fase 2).

## 9. Auditoría de la IA: qué se corrigió (Juan Sebastián, 60 s)

> La guía también pide que cualquiera de nosotros pueda explicar por qué una afirmación de la IA era aplicable o errónea. En la primera ronda, cada bloque pasó por dos revisiones de la misma IA, y en varios bloques dijeron "sin errores". En la segunda auditamos contra la guía del profesor, y aparecieron errores reales. La IA atribuyó a un "enunciado" un factor uno sobre delta y el intervalo de uno a dos: ese texto no existe en la guía. La curva de Calogero de la figura tenía un factor raíz de dos de menos. Y la tabla de cajas usaba una malla gruesa sin Richardson, con un sesgo del 18 por ciento de la energía. Todo se corrigió y cada cifra sale ahora de un script. La lección es que una revisión hecha por el mismo modelo comparte sus sesgos. Luis Felipe sigue con las cotas por arriba.

Cifras: sección 10 (tabla 10.3, K5, K9, K11, K16; supuesto S1 en 10.4); el 18 % sale de `09_prueba_costos.py` (parte B, h = 1/20 frente a Richardson en δ = 1.18, R = 800).

## 10. Cotas superiores (Luis Felipe, 50 s)

> Gracias. Por arriba usamos que el número de estados ligados está acotado. Bargmann dice que el número de estados s es menor que dos m sobre hbar cuadrado por la integral de r por el valor absoluto de V. Esa integral da g sobre mu, y el factor dos m sobre hbar cuadrado deja dos sobre delta: si delta es mayor o igual que dos no hay ligado. Ese dos importa: sin él saldría delta c menor o igual que uno, que es falso, porque en delta igual a uno todavía hay ligado. La cota de Schwinger, con la traza de K al cuadrado, baja a 1.24305. Calogero da 5.09 y no sirve aquí. Con la cota variacional, el umbral queda entre 1.19055 y 1.24305.

Cifras: `04_cota_bargmann.py` (Schwinger 1.243052; Tr K³ y Tr K⁴: 1.198384 y 1.192046; Calogero 16/π = 5.0930); `05_referencia_numerica.py` (ε0(1) = −0.0102858).

## 11. Referencia numérica (Luis Felipe, 40 s)

> Para comprobar las cotas resolvimos la ecuación radial. Integrando a energía cero obtenemos delta c igual a 1.1906124211, el mismo con cajas de 200 a 800. Numerov y diferencias finitas difieren en menos de una cien millonésima en valor absoluto, unos seis por diez a la menos nueve. La figura muestra la observable de localización: el radio medio crece de 1.5 a más de 30 y diverge en el umbral. Coincide con Gebremedhin y Weatherford, pero ese valor lo tomamos de una cita secundaria, así que nuestro número lo respalda pero no verifica la cita.

Cifras: `05_referencia_numerica.py` (Numerov frente a DF: 6.0×10⁻⁹, 2.7×10⁻⁹ y 5.7×10⁻⁹ en δ = 0, 0.5 y 1; ⟨r⟩ = 33.503 en δ = 1.170).

## 12. Acción euclídea y veredicto sobre el peso (Luis Felipe, 65 s)

> Ahora la acción. Partimos el tiempo imaginario beta en M pasos de tamaño epsilon e insertamos resoluciones de la identidad. Con la aproximación primitiva, cada paso aporta un término cinético, la distancia al cuadrado sobre dos epsilon, y uno de potencial, epsilon por V. La medida lleva un factor dos pi epsilon a la menos tres medios por eslabón, y en el límite continuo queda la integral de un medio de r punto al cuadrado más V. La guía pide decir si el peso es real, positivo y normalizable. Es real y positivo: no hay fases ni problema de signo. Pero no es normalizable: menos epsilon V es más epsilon sobre r, y la integral de r cuadrado por e a la epsilon sobre r diverge en el origen, para cualquier epsilon y cualquier delta. El núcleo exacto sí es normalizable, porque el hamiltoniano está acotado por abajo; el fallo es de la discretización, no de la física.

Cifras: `08_accion_euclidea.py` (sympy: lím r²e^(ε/r) = ∞ cuando r → 0).

## 13. Por qué falla el peso primitivo y qué lo arregla (Luis Felipe, 70 s)

> Aquí se ve la divergencia. Calculamos la integral sobre un eslabón cortando en un radio mínimo. Con epsilon igual a 0.2, el logaritmo de la integral pasa de menos 0.51 con corte en 0.1 a 74 con corte en una milésima. Y el peligro es que es invisible: con epsilon igual a 0.1 la integral no cambia entre 0.1 y 0.01, así que una simulación que no mire por debajo de 0.01 no lo nota. El apantallamiento no ayuda: solo multiplica por e a la menos epsilon delta c, y las curvas de delta cero y delta c casi coinciden. El remedio es la acción de pares: el núcleo exacto de Coulomb más un resto W que está acotado entre cero y delta. En el panel b, la acción exacta es finita en el origen y la primitiva se va a menos infinito. Y el sesgo baja como epsilon cuadrado: pendiente 1.99 en delta 0.5 y en delta 1. Suavizar el potencial no es buena alternativa: con radio 0.1 el umbral baja casi cinco centésimas.

Cifras: `08_accion_euclidea.py` (log₁₀ I: −0.512 y 74.197 con δ = 0; −0.571 y 74.093 con δ = δc; I(δc)/I(0) = 0.88782 frente a e^(−εδc) = 0.88775; U(0.02) = −0.769 frente a εV = −5.000; pendiente 1.99; suavizado a = 0.1: δc(a) − δc = −4.7×10⁻²).

## 14. El hallazgo de la caja finita (Luis Felipe, 70 s)

> El riesgo principal del proyecto apareció al verificar, y no estaba en la respuesta de la IA. Cerca del umbral kappa tiende a cero. La tabla compara delta 1.18, que está ligado, con 1.20, que no lo está. En 1.18, las cajas de 50 y 100 dan energía positiva: con el signo como único criterio diríamos "no ligado", y es falso. Lo que sí separa los casos es la tendencia con la caja: en el ligado, el radio medio sobre R baja de 0.29 a 0.08; en el no ligado sube de 0.32 hacia un medio. La figura muestra que una sola caja sesga el umbral como 1.35 sobre R: con R igual a 100 el umbral aparente es 1.177 y con 800, 1.189. Por eso el criterio es: al menos tres cajas en razón dos, malla convergida con Richardson, el radio relativo y la fracción de densidad en la mitad interior. Si no se cumplen las condiciones de ligado ni las de no ligado, el punto queda indeterminado y no entra en el intervalo.

Cifras: `09_prueba_costos.py` (parte B, Richardson con h = 1/40 y 1/80: E0(1.18) = +3.38×10⁻⁴ y +3.21×10⁻⁵ con R = 50 y 100; ⟨r⟩/R de 0.293 a 0.081 en 1.18 y de 0.324 a 0.426 en 1.20); `06_fuentes.py` (1.17701 con R = 100, 1.18892 con R = 800, por disparo sin error de malla; corregido el 21-10-2026); `07_limites_fisicos.py` (L12, 1.35/R).

## 15. Plan de cómputo: método, controles y costo (Luis Felipe, 55 s)

> El plan para la Fase 2 usa la acción de pares evaluada de dos maneras: el autovalor de la matriz de transferencia, sin muestreo, y PIGS, que proyecta desde una función de prueba; las dos se comparan con el solucionador radial. El punto fuertemente ligado es delta igual a 0.2, con control en el hidrógeno. La prueba de concepto ya funciona: en 0.2 la transferencia queda a diez a la menos ocho del radial y PIGS a 0.3 sigmas. Aprendimos dos cosas del costo. El error por bloques subestimaba la varianza en un factor 2.7, así que usaremos al menos ocho cadenas. Y el tiempo de proyección crece como uno sobre la energía: cerca del umbral PIGS necesitaría decenas de miles de eslabones, así que lo usaremos hasta delta igual a uno y la transferencia cubrirá el umbral.

Cifras: `09_prueba_costos.py` (partes D, E y F: 1.5×10⁻⁸; −0.3σ; factor 2.69; M ≈ 8750 en δ = 1.0 y 39 349 en δ = 1.1 con τ = 9/|E0| y ε = 0.1).

## 16. Resultado de la Fase 1 (Luis Felipe, 30 s)

> En resumen: el problema depende solo de delta. El umbral está entre 1.19055 y 1.24305, dentro del intervalo elemental de uno a dos, que sale por tres vías, y la referencia es 1.1906124211. El peso es real y positivo pero no normalizable con la acción primitiva, y la acción de pares lo arregla. El riesgo principal es la caja, y ya tenemos un criterio que no depende del signo de la energía.

## 17. Qué sigue en la Fase 2 (Luis Felipe, 60 s)

> ¿Qué sigue? La guía pide para la Fase 2 del proyecto 5 un solucionador radial y una formulación de tiempo imaginario que trate correctamente la singularidad, y que la primera exposición, en la semana 7, compare ambos en un punto fuertemente ligado. La evidencia es código ejecutable, un primer gráfico, la bitácora de IA y esa presentación. Nuestra propuesta: programar la tabla de la acción de pares, la transferencia y PIGS como módulos con prueba propia; pasar los controles de Coulomb y de delta 0.2, con Hulthén como control exacto; y llevar como primer gráfico la comparación de los tres métodos en 0.2 con barras de error. Los roles rotan: en la Fase 2, Juan Sebastián lleva formulación y verificación, y yo la implementación. Antes de empezar, los dos confirmamos por escrito las decisiones pendientes; con eso se cierra la Fase 1. Gracias, quedamos atentos a sus preguntas.

Cifras: sección 9 (9.4, 9.7, 9.11 y 9.12); detalle en `que_sigue_fase2.md`.

## 18. Respaldo: fuentes (no se expone)

Se muestra solo si preguntan por las referencias. [V] verificada (DOI, Crossref, Europe PMC, arXiv o INSPIRE); [M] solo metadatos verificados. El δc = 1.19061242106 de Gebremedhin y Weatherford (2023) se tomó de la tabla II de arXiv:2510.10420, porque el artículo de APS no se pudo abrir: los metadatos están verificados, la cifra no. Nuestro cálculo propio (1.1906124211) respalda el número, pero no verifica la cita. De Rogers et al. (1970) solo se cita δc ≈ 1.19. El DOI de la versión de 1935 de Yukawa no se confirmó.

## Preguntas probables y respuestas

La ronda incluye 5 min de discusión. Quién responde por defecto: Juan Sebastián (pregunta, unidades, fronteras, Coulomb, toy model, cota variacional, IA), Luis Felipe (cotas superiores, referencia, acción, peso, caja, plan, Fase 2). La defensa comprobará que cada integrante domina la pregunta, el algoritmo y los límites, así que los dos deben poder contestar cualquiera.

### Pregunta y formulación

**P: ¿Por qué un solo parámetro?**
R: Teorema Π: ħ, m, g y μ con tres dimensiones dejan un único número, δ = μħ²/(mg). A g fijo, μc = δc·mg/ħ².

**P: ¿Por qué solo onda s?**
R: En un potencial central atractivo el fundamental es ℓ = 0 y sin nodos; la barrera centrífuga solo sube la energía de ℓ > 0. Si hay algún ligado, el 1s lo está, y es el último en desligarse (hipótesis H5 de la sección 0.4).

**P: ¿Sirve la serie perturbativa para hallar δc?**
R: No. En δ = 0.3 la serie a orden 2 ya se desvía 9.9×10⁻³ (3.8 %) y la de orden 4, 1.9×10⁻³ (0.75 %), y δc ≈ 1.19 está muy fuera de su rango.

### Toy model y cotas

**P: ¿Para qué sirve el toy model si no es el Yukawa?**
R: Para tres cosas. (1) Da la energía y ⟨r⟩ exactos con la misma singularidad, así que es una prueba exacta del código de tiempo imaginario en todo δ < 2, también cerca de su propio umbral. (2) Encierra el Yukawa: V_H(δ) ≤ V_Y(δ) ≤ V_H(2δ), lo que da 1 ≤ δc ≤ 2 por una tercera vía. (3) Muestra que la forma de la ley de umbral (κ lineal, ⟨r⟩ ≈ 1/(2κ)) es general y que el coeficiente depende del perfil (1/2 frente a 0.741).

**P: ¿Por qué la cota variacional es una cota inferior para δc?**
R: Si una función de prueba da E < 0, el fundamental también tiene E < 0, luego hay ligado. Eso prueba existencia para δ < 1 (prueba hidrogenoide) y para δ < 1.19055 (12 exponenciales), es decir δc ≥ 1.19055.

**P: ¿Por qué la prueba (1 + cr)e⁻ʳᐟᵇ no mejora?**
R: A primer orden, añadir c equivale a cambiar b; la condición de estacionariedad coincide y la cota sigue en 1 (diferencia máxima entre ambas energías mínimas 9.8×10⁻¹⁵ en δ ∈ [0, 0.99], `03_cota_variacional.py`). Hacen falta varias escalas: con N = 2 ya 1.1476.

**P: ¿Por qué N = 16 da una cota algo peor que N = 12?**
R: La base es geométrica (aᵢ = a₁ρ^(i−1)) con solo dos parámetros no lineales; con N = 16 la optimización restringida no mejora (1.190546 frente a 1.190550). Es una limitación de la familia, no un error.

**P: ¿De dónde sale el 2/δ de Bargmann?**
R: Comprobación propia: ∫r|V|dr = g/μ; al multiplicar por 2m/ħ² queda 2/δ. Sin el factor 2 saldría δc ≤ 1, que contradice la cota variacional δc ≥ 1.19055. El intervalo elemental 1 ≤ δc ≤ 2 se propuso en la presentación previa del equipo, no en la guía del profesor, que solo pide derivar un criterio de estado ligado.

**P: ¿Por qué Schwinger es mejor que Bargmann?**
R: Las dos salen de la familia n₀ ≤ Tr Kᵖ del operador de Birman-Schwinger: p = 1 es Bargmann y p = 2 es Schwinger. Al subir p la cota se acerca a δc (Tr K³: 1.1984; Tr K⁴: 1.1920), y λmax(K) = 1 da 1.1906134 con 1500 nodos.

### IA

**P: ¿Qué hizo la IA y qué decidieron ustedes?**
R: Claude propuso la lista de límites (sec. 7) y redactó la acción y el plan (secs. 8 y 9) dentro del flujo de revisión. Cada afirmación se comprobó con un script. Las decisiones humanas (adoptar la lista, la acción de pares, el punto δ = 0.2, el criterio de cajas, el reparto) están reunidas en `decisiones_pendientes.md` para que las confirmemos los dos.

**P: Den un ejemplo de una afirmación de la IA que era errónea y cómo lo supieron.**
R: L13: "sin ligado, E₀R² → π²/2". Con δ = 1.3 medimos E₀R² = 4.028 (R = 100) y 4.672 (R = 400), lejos de 4.935. Falta la longitud de dispersión: con a_s = −11.58 la ley π²/[2(R − a_s)²] predice 3.964 y 4.661. Otro: el "1/δ del enunciado", que se buscó en la guía y no existe.

**P: ¿Por qué no bastaron las revisiones adversariales de la primera ronda?**
R: Las hizo el mismo modelo, que comparte sesgos, y solo comprobaban coherencia interna. No vieron K5, K7, K9 ni K11. Para la Fase 3 se propone que la auditoría de autovalores cercanos a cero la haga otro modelo (supuesto S1).

### Acción, peso y método

**P: ¿Cuál es la acción y cuál es la medida?**
R: S_E = Σₖ [|rₖ₊₁ − rₖ|²/(2ε) + εV(rₖ)], con un factor (2πε)^(−3/2) por eslabón; para Z, caminos cerrados r_M = r₀. En el límite continuo, S_E → ∫dτ [ṙ²/2 + V]. Coincide con la acción euclídea de Kleinert (cap. 2) con m = ħ = 1.

**P: ¿El peso es real, positivo y normalizable?**
R: Real y positivo, sí: no hay fases. Normalizable con la acción primitiva y el 1/r desnudo, no: el factor e^(+ε/r) hace divergir ∫r²e^(ε/r)dr en r → 0, para todo ε > 0 y todo δ (sympy y mpmath en `08_accion_euclidea.py`; Kleinert señala que la fórmula de cortes temporales diverge para Coulomb ya con dos cortes). El núcleo exacto sí es normalizable, porque Ĥ está acotado inferiormente (desigualdad de Hardy: Ĥ ≥ −2).

**P: ¿Por qué la acción de pares y no suavizar el potencial?**
R: La acción de pares trata la singularidad entera con el núcleo exacto de Coulomb, que no depende de δ (no hay circularidad), es exacta en δ = 0 para todo ε y deja un resto W = (1 − e^(−δr))/r acotado entre 0 y δ, con sesgo O(ε²) (pendiente medida 1.99). El suavizado V_a cambia la física: con a = 0.1 el umbral baja 4.7×10⁻², y solo se usa como control, con a declarado y extrapolado.

**P: ¿La tabla de pares no es circular con el solucionador radial?**
R: Se calcula con diferencias finitas, pero solo para δ = 0 (no contiene δ), se extrapola en su paso de malla y la integral de camino usa otra discretización. El plan B es una tabla obtenida por otra vía (sección 9.10).

### Caja y plan

**P: ¿Por qué importa la caja en la Fase 2?**
R: Cerca del umbral κ → 0 y ⟨r⟩ ≈ 1/(2κ) diverge. Una caja de Dirichlet sube la energía: con una sola caja el umbral aparente va de 1.17701 (R = 100) a 1.18892 (R = 800), y el sesgo baja como 1.35/R. En δ = 1.18, que está ligado, las cajas R = 50 y 100 dan E₀ > 0.

**P: ¿Cómo distinguirán un ligado débil de un estado de caja?**
R: Con al menos tres cajas en razón 2. Ligado: E₀ satura negativo, ⟨r⟩/R baja y la fracción de densidad en la mitad interior pasa de 0.95. No ligado: ⟨r⟩/R sube hacia 1/2 y E₀ sigue π²/[2(R − a_s)²], con a_s la longitud de dispersión. Si no se cumple ninguno, el punto queda indeterminado y no entra en el intervalo.

**P: ¿Y la malla? ¿Basta con agrandar la caja?**
R: No. Con h = 1/20 sin Richardson, en δ = 1.18 y R = 800 el sesgo es el 18 % de |E₀|: un E₀ que satura con R no está por eso convergido en h. Por eso el criterio exige además |E₀(h) − E₀(h/2)| < 0.1|E₀| y usar el valor con Richardson.

**P: ¿Por qué no usar PIGS hasta el umbral?**
R: El tiempo de proyección crece como 1/|E₀|: con τ = 9/|E₀| y ε = 0.1 harían falta M ≈ 8750 eslabones en δ = 1.0 y unos 39 000 en δ = 1.1. Cerca del umbral se usa la matriz de transferencia, que es la misma acción sin muestreo.

**P: ¿Por qué δ = 0.2 para la primera exposición?**
R: Es fuertemente ligado (E₀ = −0.32680851, ⟨r⟩ = 1.5497) y la brecha al 2s es grande (0.3147), así que la proyección converge pronto (τ = 20 basta) y la caja R = 40 sobra: ahí la comparación prueba el método sin que la caja interfiera. Además ya hay prueba de concepto en ese punto. Es una propuesta pendiente de confirmar por el equipo.

**P: ¿Qué falta para cerrar la Fase 1?**
R: Lo técnico (C1 a C8) está cumplido. Falta el criterio C9: que el equipo confirme o corrija por escrito las decisiones humanas registradas como pendientes (`decisiones_pendientes.md`).

**P: ¿Por qué no coinciden con Edwards et al. en la séptima cifra?**
R: Edwards et al. (2017) dan 1.1906122105; nuestro cálculo da 1.1906124211, igual al valor de Gebremedhin y Weatherford (2023), 1.19061242106. Ese último lo tomamos de una cita secundaria (arXiv:2510.10420, tabla II), así que el acuerdo con nuestro número no verifica la cita.
