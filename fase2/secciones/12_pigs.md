# 12. PIGS radial: módulo, producción y comparación con la transferencia

Fase 2, tarea 4 (y parte de la 8). Fecha: 27-10-2026. Responsable de la implementación: Luis Felipe Ramírez; verificación: Juan Sebastián Calixto.

Código:
- `fase2/codigo/pigs.py`: el módulo.
- `fase2/codigo/test_pigs.py`: sus pruebas; pasan las 9 (salida en `verificacion/test_pigs_salida.txt`).
- `fase2/codigo/12_pigs_produccion.py`: la producción (salida en `verificacion/12_pigs_salida.txt`).
- `fase2/codigo/12b_pigs_replica_tau5.py`: una réplica con semillas nuevas (salida en `verificacion/12b_pigs_replica_salida.txt`).

Resultados en `resultados/12_pigs.json`, `resultados/12b_pigs_replica.json` y `resultados/12_pigs_series.npz`. Figuras: `figuras/12_pigs_tau.png` y `figuras/12_pigs_delta02.png`.

Todas las cifras de esta sección salen de esos scripts ejecutados. Unidades: ħ = m = g = 1, V = −e^{−δr}/r. En toda la sección se usa ε = 0.1.

## 12.1 Algoritmo

**Peso.** Se muestrean caminos abiertos r_0, …, r_M, con M = τ/ε eslabones y r continuo y positivo. El peso es

P[r] ∝ u_T(r_0) · ∏_k T(r_k, r_{k+1}) · u_T(r_M),  con u_T(r) = r e^{−r},

T(a,b) = K_D(a,b;ε) · e^{−U_C(a,b;ε)} · e^{−ε[W(a)+W(b)]/2},  donde W = (1 − e^{−δr})/r ∈ [0, δ].

Es la misma acción aprobada que usa la transferencia (sección 11):
- núcleo libre con imagen K_D, que impone u(0) = 0;
- acción de pares exacta de Coulomb U_C, tomada de `pares.py` con Richardson entre h_tab = 0.01 y 0.005;
- resto acotado W.

El peso es real, positivo y normalizable. El exponente nunca contiene 1/r desnudo (no hay acción primitiva).

**Interpolación de U_C.** Como r es continuo, U_C se interpola en la tabla. La producción usa la interpolación bicúbica (spline de `TablaPares`, error máximo 9e-9 según la sección 11). La bilineal se usa como control. Respecto a la Fase 1 hay una corrección: por debajo del primer nodo (r < 0.01) la bilineal extrapola linealmente, en lugar de quedarse constante. Para r > 10 se usa la aproximación de extremos. Si |r − r'| supera la banda (7√ε), el movimiento se rechaza (peso < e^{−24.5}).

**Movimientos.** Todos son de Metropolis y cumplen balance detallado.
1. *Rebrote de segmentos por puente browniano (L = 10).* Los 9 puntos interiores se proponen con la parte gaussiana libre exacta: B_k = W_k − (k/L) W_L, con W una caminata de paso √ε. La aceptación usa solo el resto: imagen, U_C y W. Hay dos rejillas de segmentos, desplazadas L/2 entre sí.
2. *Rebrote de extremos.* Los L/2 = 5 eslabones de cada punta se proponen como caminata libre desde r_5 (o r_{M−5}). La aceptación usa el resto y el cociente de u_T en la punta.
3. *Escala global r → λr.* Se toma ln λ ~ N(0, (0.7/√M)²), una propuesta simétrica en ln λ. El jacobiano es λ^{M+1}. Se hacen 4 intentos por barrido.

Una propuesta con algún r ≤ 0 se rechaza. Cada barrido hace los tres tipos de movimiento. Se mide en todos los barridos, después de 500 de termalización. Aceptaciones medidas en δ = 0.2 y τ = 20: puentes 0.819, extremos 0.728, escala 0.715.

**Qué estimador es mixto y cuál puro.**
- **Energía: estimador MIXTO** en los extremos. Se usa E_L(r) = (H u_T)/u_T = W(r) − 1/2. Es exacto para u_T = r e^{−r}, porque −u''/(2u) = 1/r − 1/2 y V = −1/r + W. Se promedia en r_0 y r_M. Su valor es ⟨u_T|T^M H|u_T⟩/⟨u_T|T^M|u_T⟩, que tiende a E_0 cuando τ → ∞. Para δ = 0, u_T es exacta y E_L ≡ −1/2 sin varianza. Para δ > 0, u_T tiene la cola equivocada (no es exacta), como pide la guía.
- **⟨r⟩ y ⟨r²⟩: estimador PURO** en el eslabón central r_{M/2}. Allí la densidad es ψ_{τ/2}(r)², que tiende a |u_0|². No es el mixto ⟨u_T|r|u_0⟩/⟨u_T|u_0⟩. Su sesgo de proyección decae como e^{−(E_1−E_0)τ/2}, más despacio que el del mixto (ver 12.4).

**Errores.**
- Cada cadena se parte en 20 bloques.
- Error por bloques combinado: √(Σ e_i²)/n.
- Error entre cadenas: desviación de las n medias dividida por √n.
- **Se reporta siempre el mayor de los dos** (regla 9.7).

El tiempo de autocorrelación integrado se mide de dos formas:
- con la ventana automática de Sokal (c = 6; método citado de memoria, sin referencia consultada: NO VERIFICADA; la prueba con un AR(1) da 4.51 frente al 4.5 exacto);
- a partir del error por bloques.

## 12.2 Referencias deterministas con el mismo ε

`12_pigs_produccion.py` reconstruye, sin muestreo, lo mismo que mide el PIGS, con la transferencia en banda de la sección 11:
- R = 40, h = 0.02 y 0.04, Richardson en h con exponente 4;
- E_mixto(τ) = ⟨u_T|T^M H u_T⟩/⟨u_T|T^M u_T⟩;
- el puro ⟨r⟩(τ) = Σ r x²/Σ x², con x = T^{M/2} u_T.

En δ = 0.2 da:

| | E | ⟨r⟩ | ⟨r²⟩ |
|---|---|---|---|
| radial (R = 40, Richardson) | −0.3268085052 | 1.5497218981 | 3.2259394422 |
| transferencia τ → ∞ (autovector) | −0.3268086227 (E_0(T)); mixto límite −0.3268086240 | 1.5497354673 | 3.2259787857 |
| transferencia τ = 20 | −0.3268083624 (mixto) | 1.5485514370 (puro) | 3.2195166492 (puro) |

En δ = 0 la transferencia da E_mixto = −0.5 en todas las τ y ⟨r⟩_puro = 1.5000000 tras Richardson en h.

## 12.3 Producción

**(1) Control Coulomb, δ = 0** (τ = 10, M = 100; 1 cadena de 5×10⁴ + 500 barridos; semilla 20262008; 1.46 ms por barrido en la reejecución de V3):
- E_L ≡ −0.5 en los 5×10⁴ barridos: varianza 0 y máx |E_L + 0.5| = 0. **Este control es tautológico** (H7 de V2): con δ = 0, W ≡ 0 y E_L = W − 1/2 vale −1/2 para cualquier camino, se muestree bien o mal. El control real de Coulomb son ⟨r⟩ y ⟨r²⟩ (abajo) y la prueba de histograma de la sección 12.V3.
- ⟨r⟩ = 1.49277 ± 0.01626, a −0.44σ de 1.5.
- ⟨r²⟩ = 2.97503 ± 0.07873, a −0.32σ de 3.
- τ_int: 9.3 barridos en ⟨r⟩ y 11.4 en ⟨r²⟩.
- Con una sola cadena no hay error entre cadenas: el σ es solo el de bloques. El plan asigna una única semilla a este control.

**(2) Punto fuertemente ligado, δ = 0.2** (τ = 20, M = 200; 8 cadenas de 5×10⁴ + 500 barridos; semillas 20262000 a 20262007; interpolación bicúbica; 2.00 ms por barrido en la reejecución de V3, 2.80 ms en la primera):

| | PIGS | error bloques | error entre cadenas | (entre/bloques)² | τ_int Sokal | radial | desviación |
|---|---|---|---|---|---|---|---|
| E (mixto) | −0.326725 ± 0.000068 | 5.15e-5 | 6.82e-5 | 1.75 | 5.3 | −0.32680851 | +1.22σ |
| ⟨r⟩ (puro) | 1.55374 ± 0.00711 | 7.11e-3 | 7.04e-3 | 0.98 | 11.7 | 1.54972 | +0.56σ |
| ⟨r²⟩ (puro) | 3.24260 ± 0.03894 | 3.58e-2 | 3.89e-2 | 1.18 | 14.2 | 3.22594 | +0.43σ |

El cociente (entre cadenas/bloques)² queda por debajo de 2 en las tres magnitudes; en la Fase 1 era 2.69. Aun así, se toma el mayor de los dos errores.

**Tiempo.** La primera ejecución completa duró 11.9 min de reloj en 4 procesos; la reejecución de V3, que es la que guarda `12_pigs.json`, 9.3 min. Fueron 41 cadenas: producción, control bilineal y barrido en τ. La máquina estaba compartida, con una carga de 4.8 a 7 por los demás agentes en la primera ejecución (3.0 al empezar la reejecución). No hizo falta reducir barridos.

## 12.4 Dependencia con la duración de proyección (δ = 0.2)

Para τ = 2, 5 y 10 se corrieron 8 cadenas de 3×10⁴ + 500 barridos (semillas 20262020+k, 20262030+k y 20262040+k). Para τ = 20 se usa la producción. La comparación es con la transferencia en el mismo ε y la misma τ (figura `12_pigs_tau.png`):

| τ | M | E_PIGS | E_transf. | σ | ⟨r⟩_PIGS | ⟨r⟩_transf. | σ | ⟨r²⟩ σ |
|---|---|---|---|---|---|---|---|---|
| 2 | 20 | −0.326713 ± 0.000071 | −0.326660 | −0.74 | 1.5210 ± 0.0058 | 1.5176 | +0.58 | +0.61 |
| 5 | 50 | −0.326955 ± 0.000060 | −0.326763 | **−3.19** | 1.5440 ± 0.0075 | 1.5321 | +1.58 | +1.55 |
| 10 | 100 | −0.326789 ± 0.000064 | −0.326801 | +0.19 | 1.5353 ± 0.0078 | 1.5428 | −0.97 | −0.92 |
| 20 | 200 | −0.326725 ± 0.000068 | −0.326808 | +1.22 | 1.5537 ± 0.0071 | 1.5486 | +0.73 | +0.59 |

**Resultado sin maquillar.** De los 12 valores, uno queda fuera de 2σ: E(τ = 5), a −3.19σ. Por eso el criterio «todos a menos de 2σ» **falla** en la ejecución de producción.

Para ver si era sesgo o fluctuación, `12b_pigs_replica_tau5.py` repitió τ = 5 con 16 semillas nuevas (20262050 a 20262065, 2 tandas de 8 cadenas × 3×10⁴ barridos, 161 s):

| Tanda | E | Desviación |
|---|---|---|
| A | −0.326780 ± 0.000093 | −0.18σ |
| B | −0.326742 ± 0.000061 | +0.34σ |
| Las 16 juntas | −0.326761 ± 0.000053 | +0.03σ |

En las 16 juntas, ⟨r⟩ = 1.5285 ± 0.0048 (−0.76σ). La réplica coincide con la transferencia. Por tanto, el −3.2σ original se interpreta como una fluctuación estadística: su probabilidad es de ~0.14 % por valor y ~2 % de que ocurra en alguno de los 12. No hay indicio de sesgo del muestreador. El valor original se conserva en el JSON y en la figura.

**Qué resuelve el PIGS de la proyección.**
- En el mixto, E_mixto(2) − E_mixto(20) vale +1.48×10⁻⁴ en la transferencia. Eso es solo ~1.5 errores estadísticos, y el PIGS no lo resuelve: da +1.2×10⁻⁵ ± 1.0×10⁻⁴.
- En el puro, ⟨r⟩(2) − ⟨r⟩(20) vale −0.0309 en la transferencia, y el PIGS lo resuelve: −0.0327, a −3.6σ de cero.

**Sesgo de proyección del estimador puro** (transferencia, valor en τ menos el límite τ → ∞):

| τ | ⟨r⟩ | ⟨r²⟩ | E_mixto |
|---|---|---|---|
| 10 | −6.9×10⁻³ | −3.6×10⁻² | +7.6×10⁻⁶ |
| 20 | −1.18×10⁻³ | −6.5×10⁻³ | +2.6×10⁻⁷ |
| 30 | −2.2×10⁻⁴ | −1.2×10⁻³ | +1.0×10⁻⁸ |

El puro decae como e^{−(E_1−E_0)τ/2}: el cociente de 20 a 30 da una tasa de 0.17 por unidad de τ, frente a (E_1−E_0)/2 = 0.157. Con τ = 20, el sesgo de ⟨r⟩ (1.2×10⁻³) es 6 veces menor que el error estadístico de la producción (7×10⁻³), así que no afecta al criterio. **Si en la Fase 3 se quiere ⟨r⟩ a 10⁻³ o mejor, hay que usar τ ≥ 30 para el estimador puro.** El criterio de proyección de 9.7 (cambio < 10⁻⁶ de τ a 1.5τ) solo lo cumple el mixto.

## 12.5 PIGS frente a transferencia en el mismo ε: sesgo de interpolación

**Bicúbica frente a la transferencia en nodos** (mismo ε = 0.1 y τ = 20):

| Magnitud | PIGS − transferencia | Desviación |
|---|---|---|
| E | +8.3×10⁻⁵ ± 6.8×10⁻⁵ | +1.22σ |
| ⟨r⟩ | +5.2×10⁻³ ± 7.1×10⁻³ | +0.73σ |
| ⟨r²⟩ | +2.3×10⁻² ± 3.9×10⁻² | +0.59σ |

**Bilineal frente a bicúbica, medido por repesado.** En cada configuración de la producción bicúbica se guardó ΔS = Σ_k [U_bil − U_bic]. Su media es −5.17×10⁻⁴ y su desviación 2.36×10⁻⁴. Repesando con e^{−ΔS} se obtiene la media bilineal sobre las mismas configuraciones. Al estar correlacionadas, el error es muy pequeño (jackknife de 20 bloques; se toma el mayor entre ese y el error entre cadenas):

| | bilineal − bicúbica (repesado) | repesado inverso (bicúbica − bilineal, desde la corrida bilineal) |
|---|---|---|
| E | +5.72×10⁻⁷ ± 9.1×10⁻⁹ | −5.69×10⁻⁷ ± 1.3×10⁻⁸ |
| ⟨r⟩ | −7.65×10⁻⁵ ± 1.6×10⁻⁶ | +7.44×10⁻⁵ ± 2.1×10⁻⁶ |
| ⟨r²⟩ | −3.03×10⁻⁴ ± 9.6×10⁻⁶ | +2.95×10⁻⁴ ± 1.2×10⁻⁵ |

Lectura:
- El sesgo de la bilineal es real y está medido con precisión: 5.7×10⁻⁷ en E y 7.6×10⁻⁵ en ⟨r⟩.
- Es 100 veces menor que el error estadístico actual. Esto cierra el riesgo de 9.10 («interpolación bilineal… no resuelta»).
- Las dos direcciones del repesado coinciden.
- Una corrida directa bilineal (8 cadenas de 2.5×10⁴ barridos; semillas 20262010 a 20262017) da E = −0.326597 ± 0.000094, ⟨r⟩ = 1.5435 ± 0.0099 y ⟨r²⟩ = 3.2041 ± 0.0478.
- Su diferencia directa con la bicúbica (+1.28×10⁻⁴ ± 1.2×10⁻⁴ en E) es compatible con el repesado: 1.10σ.
- Ojo: la E bilineal directa queda a +2.2σ del radial. No es un criterio, y el repesado muestra que no se debe a la interpolación (5.7×10⁻⁷). Es estadística de una corrida con la mitad de barridos.

Decisión: la producción usa la bicúbica. La bilineal vale igual a la precisión actual; su sesgo pasará a importar con errores por debajo de ~10⁻⁶ en E o ~10⁻⁴ en ⟨r⟩.

## 12.6 Tabla de criterios

| # | Control | Criterio | Valor | ¿Pasa? |
|---|---|---|---|---|
| 1 | Coulomb PIGS, E_L | E_L = −0.5 con varianza nula | var = 0, máx\|E_L+0.5\| = 0 | sí (**tautológico**, ver 12.V3) |
| 2 | Coulomb PIGS, ⟨r⟩ puro | < 2σ de 1.5 | 1.49277 ± 0.01626 (−0.44σ) | sí |
| 3 | Coulomb PIGS, ⟨r²⟩ puro | < 2σ de 3 | 2.97503 ± 0.07873 (−0.32σ) | sí |
| 4 | δ = 0.2, E mixto | < 2σ del radial (σ el mayor de bloques y cadenas) | −0.326725 ± 0.000068 (+1.22σ) | sí |
| 5 | δ = 0.2, ⟨r⟩ puro | < 2σ del radial | 1.55374 ± 0.00711 (+0.56σ) | sí |
| 6 | δ = 0.2, ⟨r²⟩ puro | < 2σ del radial | 3.24260 ± 0.03894 (+0.43σ) | sí |
| 7 | E_mixto(τ), ⟨r⟩, ⟨r²⟩ puros, τ = 2, 5, 10, 20 | todos < 2σ de la transferencia | 11 de 12; E(τ = 5) a −3.19σ | **no** |
| 7b | Réplica de τ = 5 (16 semillas nuevas) | < 2σ | E +0.03σ, ⟨r⟩ −0.76σ | sí |
| 8 | Sesgo bilineal en E (repesado) | medido y < error estadístico | +5.72×10⁻⁷ ± 9.1×10⁻⁹ (error de producción 6.8×10⁻⁵) | sí |
| 9 | Repesado frente a corrida bilineal directa | compatibles a 2σ | 1.10σ | sí |
| 10 | PIGS bicúbica frente a transferencia, mismo ε y τ | E, ⟨r⟩, ⟨r²⟩ < 2σ | +1.22σ, +0.73σ, +0.59σ | sí |
| 11 | Tiempo de reloj | < 25 min | 11.9 min en la primera ejecución y 9.3 min en la de V3 (réplica: 2.7 y 2.3 min) | sí |
| 12 | Pruebas del módulo (`test_pigs.py`) | todas pasan | 9 de 9 | sí |

## 12.7 Limitaciones y pendientes

- El criterio 7 falla en la ejecución de producción por E(τ = 5). La réplica independiente pasa. Juan Sebastián debe decidir si basta la réplica o si prefiere más estadística en ese punto.
- El control de Coulomb usa una sola cadena: su σ es solo de bloques. Con 8 cadenas (semillas 20262008+) se aplicaría la regla completa.
- Errores actuales en δ = 0.2: 6.8×10⁻⁵ en E y 7×10⁻³ en ⟨r⟩. Bajar a 10⁻⁵ en E costaría ~46 veces más barridos.
- El estimador puro necesita τ ≥ 30 para ⟨r⟩ a ~2×10⁻⁴ (12.4).
- PIGS sigue limitado a δ ≤ 1.0 (riesgo 1 de 9.10). La autocorrelación en función de M aún no se ha medido cerca del umbral. Aquí τ_int de ⟨r⟩ pasa de 4.4 (M = 20) a 11.7 (M = 200), crece con M, y en δ = 1.0 hará falta M ~ 9000.
- Por debajo del primer nodo de la tabla (r < 0.01) la extrapolación tiene un error de 1.7×10⁻⁴ (sección 11). Los caminos casi no visitan esa zona (densidad ∝ r²), y el repesado no muestra efecto medible.

## 12.8 Registro de IA (esta tarea)

- Primera versión del criterio «proyección visible en PIGS» (exigía E_mixto(2) − E_mixto(20) > 2σ): lo escribí antes de comparar el tamaño de la señal (1.5×10⁻⁴) con el error (~10⁻⁴). En la prueba corta no se cumplía por pura estadística, así que lo pasé a magnitud informativa antes de la producción. No era un criterio aprobado en 9.7.
- La anomalía de τ = 5 (−3.2σ) apareció en la producción. No cambié el resultado ni la tolerancia: hice una réplica con semillas nuevas, que da +0.03σ, y reporto las dos.
- El módulo parte de la parte E de `fase1/codigo/09_prueba_costos.py`, con estos cambios:
  - extrapolación lineal de la bilineal bajo el primer nodo;
  - interpolación bicúbica para la producción;
  - el peso actual se recalcula una vez por barrido antes de los movimientos de escala (antes se recalculaba en cada intento; el resultado es el mismo);
  - se guarda ΔS para el repesado;
  - τ_int con ventana de Sokal.


## 12.V3 Correcciones y pruebas añadidas tras la verificación (27-10-2026)

Detalle en `fase2/verificacion/V3_respuesta_hallazgos.md`. Scripts nuevos o cambiados: `pigs.py`, `test_pigs.py`, `12c_pigs_coulomb_tau5.py` (resultados en `resultados/12c_pigs_coulomb_tau5.json`, salida en `verificacion/12c_pigs_coulomb_tau5_salida.txt`).

- **Reejecución.** `12_pigs_produccion.py` y `12b_pigs_replica_tau5.py` se volvieron a ejecutar con el código de V3 (U_C fuera de r = 10 con Wigner-Kirkwood). Las series de Monte Carlo salen **idénticas bit a bit** (mismas semillas; ningún camino cruzó r = 10 de modo que cambiara una aceptación) y las curvas deterministas de la transferencia cambian a lo sumo 2.4×10⁻⁹ en valor relativo. Todas las cifras de esta sección siguen valiendo; 12 tardó 9.3 min.
- **H8 de V2 (corregido).** `pigs.cadena` truncaba M en silencio a un múltiplo de L y guardaba el τ pedido. Ahora lanza `ValueError` si τ/ε no es un entero múltiplo de L y guarda `tau_ef = M ε`. En producción no cambia nada (todos los τ/ε eran múltiplos de 10).
- **H12 de V2 (corregido).** `test_pigs.py` tiene ahora 14 pruebas (antes 9), todas pasan: la antigua "caminos positivos y reproducibles" se separó en dos (reproducibilidad y positividad real de los caminos); prueba del `ValueError`; y una **prueba de la distribución**: con δ = 0.2, τ = 1, ε = 0.1 (M = 10), el histograma de r_{M/2} sigue [T^{M/2}u_T]² de la transferencia (χ² = 32.9 con 24 intervalos, p = 0.106), y la misma prueba rechaza una densidad con la escala de r cambiada un 5 % (p = 1.5×10⁻⁶²). La tolerancia 0.5–1.6 del error por bloques en el AR(1) no se cambió.
- **H7 de V2: Coulomb con 8 cadenas** (τ = 10, ε = 0.1, 3×10⁴ barridos, semillas 20262090–97). ⟨r⟩ = 1.49027 ± 0.00720 (−1.35σ de 1.5) y ⟨r²⟩ = 2.96787 ± 0.03430 (−0.94σ de 3); cocientes (cadenas/bloques)² 0.45 y 0.59. Histograma de r_{M/2} frente a x_{M/2}² de la transferencia: χ² = 57.7 con 32 intervalos, **p = 0.004**. Pasa el criterio fijado antes (p > 10⁻³), pero por poco; queda anotado.
- **H5 de V1 / H6 de V2: anomalía de τ = 5.** Segunda réplica (16 cadenas, semillas 20262070–85): E = −0.326718 ± 0.000045, **+0.99σ** de la transferencia (−0.326762633); ⟨r⟩ −0.45σ, ⟨r²⟩ −0.60σ. Por corrida: producción −3.19σ, réplica 1 +0.03σ, réplica 2 +0.99σ; χ² de las tres frente a E_det = 11.13 con 3 grados de libertad (**p = 0.011**): las corridas no concuerdan del todo entre sí. Las 40 cadenas juntas: −0.326785 ± 0.000027 (ponderada, −0.83σ) y −0.326783 ± 0.000033 (pesos iguales, −0.61σ); χ² por cadena 50.2 con 39 (p = 0.109); 20 de 40 cadenas por debajo de E_det. Con las 24 cadenas de la auditoría V2 (código anterior a V3, efecto despreciable en δ = 0.2): 64 cadenas, −0.97σ. **Lectura:** la combinación no muestra sesgo; la producción de τ = 5 sigue siendo un valor en la cola (p ≈ 1 % para la dispersión entre corridas). No se puede decir más sin más corridas; la decisión es de Juan Sebastián.
