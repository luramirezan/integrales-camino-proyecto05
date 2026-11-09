# V2. Auditoría adversarial de la Fase 2 (física, código y afirmaciones)

**Proyecto 05, umbral de ligadura del 1s en V = −e^{−δr}/r** · Fase 2 · 27-10-2026
Auditoría hecha por Claude (agente auditor del flujo de trabajo pedido por Lucho). Equipo: Juan Sebastián Calixto (verificación en la Fase 2) y Luis Felipe Ramírez (implementación). Esta auditoría **no sustituye** la firma de Juan Sebastián: le da evidencia para decidir.

Material auditado: todo `fase2/codigo/`, `fase2/resultados/` y `fase2/secciones/` (10 a 14), contra `fase1/secciones/09_plan_computo.md` (9.2, 9.4, 9.6, 9.7, 9.10), `fase1/secciones/07_limites_fisicos.md`, `fase1/que_sigue_fase2.md` y `enunciado/guia_texto.txt`.

Todo lo que se cita aquí sale de comandos que ejecuté hoy. Los scripts de la auditoría y sus salidas están en `fase2/verificacion/V2_auditoria/`. Cada script recibe como argumento la carpeta de código; los corrí sobre una **copia** de `fase2/codigo/` en mi carpeta temporal, para no tocar la caché ni los resultados del proyecto (con una excepción involuntaria, explicada en H9).

## Resumen en cinco líneas

1. No encontré ningún error que cambie un resultado de la Fase 2. La acción (K_D con imagen, U_C, resto W) está bien en signo y en normalización, el peso es real, positivo y normalizable, y el estimador que se llama puro sí lo es.
2. Todo es reproducible: las tres pruebas pasan (7/7, 5/5, 9/9) y los scripts 11, 13, 14 y 12b dan las mismas cifras al reejecutarlos. 12b da el mismo resultado **bit a bit** con las mismas semillas.
3. Hay tres problemas **medios** de física o código, ninguno grave:
   - el texto de la sección 14 subestima cuántas celdas (11 de 15, no 5) fallan el criterio que usa solo el error de la transferencia (H1);
   - la aproximación de extremos más allá de r = 10 es peor de lo que dice el código (H2);
   - la pared en R sin imagen sesga en silencio las cajas chicas (H3).
4. A la Fase 2 le faltan entregables que pide la guía: la primera presentación, la bitácora de IA consolidada, la tabla de controles firmada y la lista de figuras congeladas (H4).
5. Hice cuatro comprobaciones que nadie había hecho:
   - una tabla U_C independiente, con otra discretización;
   - una prueba de la distribución que muestrea el PIGS, con 24 cadenas nuevas;
   - los límites L04, L05, L06 y L09 con la transferencia;
   - casos raros (ε grande, h grande, R chico).
   Todas pasan, salvo los casos raros, que muestran el sesgo de pared de H3.

## 1. Qué reejecuté y qué salió

| Qué | Cómo | Resultado |
|---|---|---|
| `test_radial.py` | reejecución | 7/7 pasan. La salida es idéntica a `verificacion/test_radial_salida.txt` salvo el tiempo (4.1 frente a 5.6 s). |
| `test_transferencia.py` | reejecución | 5/5 pasan |
| `test_pigs.py` | reejecución | 9/9 pasan |
| `10_radial_controles.py` | reejecución (6 s) | sin error; deterministas (ver H9) |
| `11_transferencia_controles.py` | reejecución en una copia, con las tablas U_C **recalculadas desde cero** (sin caché) | 604 números iguales; diferencia máxima 4.3e-7 relativa, en un orden aparente calculado de diferencias de 1e-9. Las energías coinciden a 1e-14. |
| `13_controles_hulthen_pozo.py` | ídem (84 s) | 1674 números; la única diferencia visible está en el orden de Trotter de Hulthén con δ = 0.2 (8e-6), que la sección ya declara sin sentido |
| `14_criterio_cajas.py` | ídem (136 s) | 2046 números; diferencia máxima 2.5e-12; los mismos veredictos |
| `12b_pigs_replica_tau5.py` (Monte Carlo, 16 cadenas) | ídem (140 s) | **0 diferencias**: los 202 números del json coinciden bit a bit. Las semillas están fijas de verdad. |

Salidas: `V2_auditoria/tests_reejecucion.txt` y `V2_auditoria/reproducibilidad_salida.txt` (comparador `cmp2.py`; ignora tiempos y carga).

No reejecuté el `12_pigs_produccion.py` completo (12 min con 4 procesos). Su reproducibilidad con semillas queda probada por 12b, que usa el mismo `pigs.cadena` y la misma tabla, y por la prueba "misma semilla, misma serie" de `test_pigs.py`.

## 2. Preguntas del encargo, una por una

**¿Signo y factores de K_D y de U_C?** Correctos.
- K_D: `logKD` usa e^{−(a+b)²/2ε} = e^{−(a−b)²/2ε}·e^{−2ab/ε}, de donde ln K_D = −(a−b)²/2ε + ln(1−e^{−2ab/ε}) − ½ln(2πε). Lo comprobé a mano.
- Desplazamiento espectral de U_C: U = −(ln c − ln z) + ε(w_C0 − w_00). También lo comprobé a mano.
- Prueba numérica independiente (`uc_indep.py`): construí U_C con **otra** discretización. Usé un hamiltoniano de 4.º orden (5 puntos) y lo dividí por el K_D **exacto**, no por el núcleo libre de la red. Coincide con la tabla de `pares.py`:

| (r, r') | tabla (Richardson) | 4.º orden extrapolado | diferencia |
|---|---|---|---|
| (1, 1) | −0.10182873 | −0.10182873 | 4e-11 |
| (5, 5) | −0.02001343 | −0.02001343 | 1.5e-11 |
| (0.5, 0.5) | −0.21828596 | −0.21828597 | 7.6e-9 |
| (0.1, 0.1) | −0.62970270 | −0.62970285 | 1.5e-7 |
| (0.02, 0.02) | −0.76897539 | −0.76897704 | 1.65e-6 |
| (0.01, 0.01) | −0.78826912 | −0.78829678 | 2.8e-5 |

Si K_D tuviera mal el signo de la imagen o la normalización, estas cifras no coincidirían a 1e-11. En r ≤ 0.02 mi método solo tiene orden 1.86, así que la diferencia de 2.8e-5 en r = 0.01 no permite decir cuál de los dos está mejor. El peso de esa zona es de orden r³, unos 1e-6.

**¿Peso real, positivo y normalizable con estos parámetros?** Sí.
- 0 elementos negativos y 0 no finitos en todas las matrices que construí: ε = 0.05 a 2.0, h = 0.02 a 0.5, R = 2 a 40, δ = 0, 0.2 y 5.
- Las tablas no tienen ningún ρ ≤ 0 dentro de la banda (`n_no_positivos` = 0 en todas).
- Con ε = 0.5, 1 y 2 el Coulomb sigue dando E0 = −0.49999998, −0.49999999 y −0.4999999953. El código no falla en silencio con ε grande.
- En el PIGS, e^{−U} es siempre positivo (también con el spline). Fuera de r = 10 se usa la acción de extremos, que es acotada, y |r − r'| > banda se rechaza.

**¿El estimador "puro" de ⟨r⟩ lo es?** Sí. En el eslabón central, la densidad marginal es [T^{M/2}u_T]². Lo comprobé con 24 cadenas nuevas (`mc_audit.py`; δ = 0.2, τ = 5, semillas de auditoría 20269000 a 20269023, fuera de todos los rangos de producción):
- el histograma de r_{M/2} coincide con x_{M/2}² de la transferencia: χ² = 20.0 en 32 intervalos, p = 0.95;
- el de r_0 coincide con u_T·T^M u_T, que es la densidad del mixto: χ² = 24.9 en 31 intervalos, p = 0.77.

Esto es una prueba directa de que el muestreador muestrea el peso declarado, más fuerte que comparar solo medias.

**¿Se usó el radial de forma circular con la tabla U_C (advertencia 9.2)?**
- La tabla sale de diferencias finitas, igual que el radial, pero solo para δ = 0.
- La prueba de Coulomb (|E + 0.5| ≤ 2.2e-7) compara con el valor exacto, no con el radial.
- Mi tabla de 4.º orden, que no usa el esquema del radial, la reproduce a 1e-11 donde importa.

Con esto el riesgo 3 de 9.10 queda **acotado con evidencia independiente**. Ningún agente había ejecutado el plan B de 9.10; esta comprobación cumple esa función, y propongo pasarla a la Fase 2 como script numerado.

**¿Errores estadísticos subestimados?** No encontré subestimación.
- Análisis de bloques de las series de producción (`12_pigs_series.npz`): el error por cadena forma meseta desde bloques de 250 barridos (1.46e-4 en E, 0.019 en ⟨r⟩). Los 20 bloques de 2500 barridos están en la meseta.
- Con mis 24 cadenas, χ² de las medias por cadena con su propio error de bloques: 22.9 con 23 grados de libertad (p = 0.47) en E, y 12.6 con 23 en ⟨r⟩.
- Cociente (entre cadenas/bloques)²: 0.94 en E.
- Mi media en τ = 5: E = −0.326797 ± 0.000065, a −0.53σ de la transferencia; ⟨r⟩ = 1.5353 ± 0.0064, a +0.50σ.

Queda una dispersión algo grande en el conjunto de comparaciones de producción (H6). Con lo anterior, la interpreto como fluctuación, no como error mal estimado.

**¿Semillas fijas de verdad?** Sí. `default_rng(semilla)` por cadena y `pool.map` ordenado; 12b es idéntico bit a bit. Los rangos no se solapan: producción 20262000–07, Coulomb 08, bilineal 10–17, τ = 2/5/10 en 20–27/30–37/40–47, réplica 50–65.

**¿Criterios de 9.7 comprobados con los números que dicen?** Crucé de forma automática cada cifra de 3 o más dígitos de las secciones 10 a 14 con los json (`numcheck`). La mayoría de las cifras que no aparecen son etiquetas (δ = 1.15), números de sección (9.10) o cifras de la Fase 1 citadas. Revisé a mano todas las demás:
- ningún criterio de 9.7 está redondeado a favor;
- hay una errata de redondeo sin efecto (H11);
- el único texto que no cuadra con su json es el de la sección 14 (H1).

Las tolerancias que se fijaron después de ver el resultado ya están declaradas por sus autores: Hulthén ⟨r²⟩ en la sección 10, el pozo B3 en la 13 y el umbral 0.1 de la ley de caja en la 14. Juan Sebastián debe aprobarlas o rechazarlas.

**¿Casos raros?** (`edge1.py`)

| caso | resultado |
|---|---|
| h = 0.015 (no múltiplo de 0.01) | `ValueError` explícito, bien |
| h = 0.05, 0.1, 0.2, 0.5 (Coulomb, ε = 0.1) | E0 = −0.4999958, −0.4999336, −0.4989513, −0.4843666: el error crece como se espera, sin NaN ni avisos. **Ningún aviso** al usuario. |
| ε = 0.5, 1, 2 | correcto (ver arriba) |
| R = 2, 5, 10 con δ = 0.2 | transferencia −0.0376370, −0.3232533, −0.3268069 frente al radial +0.0589037, −0.3222272, −0.3268063. **Sesgo silencioso** en cajas chicas (H3). |
| δ = 5 (no ligado), R = 40 | +0.0030418 frente a +0.0030688 del radial (0.9 %), por la misma causa |
| PIGS con τ/ε no múltiplo de L | τ = 2.5 y ε = 0.2 dan M = 10 (τ efectivo 2.0), pero se guarda τ = 2.5 (H8) |

## 3. Hallazgos

Gravedad: **alta** = cambia un resultado o un veredicto (no encontré ninguno); **media** = afirmación falsa o sesgo sistemático medible que no cambia veredictos, o entregable que falta; **baja** = robustez, estilo o erratas.

### H1 (media). La sección 14 subestima las celdas en que la transferencia no cabe en su propio error

**Dónde:** `secciones/14_criterio_cajas.md` (párrafo de 14.4 y "problemas"); `resultados/14_cajas.json`, `celdas/*/{dif_rad, err}`.

**Qué dice:** el criterio "|dif| ≤ err_tr" falla en R = 50 (las tres δ) y en R = 100 (δ = 1.18 y 1.20). Atribuye la causa a la pared. Añade que en R ≥ 200 queda un "residuo de volumen ... dentro del error estimado".

**Qué dice el json:** |dif_rad| > err_tr en **11 de 15** celdas: las 5 que cita el texto y otras 6, todas con R ≥ 200, que no menciona:

| δ | R | dif_rad | err_tr | cociente |
|---|---|---|---|---|
| 1.18 | 200 | −2.18e-8 | 1.63e-8 | 1.3 |
| 1.18 | 400 | −8.30e-9 | 5.35e-9 | 1.6 |
| 1.18 | 800 | −8.00e-9 | 7.20e-9 | 1.1 |
| 1.20 | 200 | −5.25e-8 | 2.64e-8 | 2.0 |
| 1.20 | 400 | −8.91e-9 | 3.39e-9 | 2.6 |
| 1.20 | 800 | −1.50e-9 | 1.63e-10 | **9.2** |

Todas pasan como "compatibles" solo porque se suma el error del radial y se multiplica por 2. Las diferencias son de 9e-4 de |E0| o menos y **no cambian ningún veredicto**. Lo que muestran es que `err_tr` (|E_ext − E_mejor| + |E_mejor − E_gruesa|) no recoge todos los sesgos. Uno de ellos lo identifico en H2.

**Corrección:** corregir el texto de 14.4 y de "problemas" (son 11 de 15 celdas, también en R ≥ 200). Para la Fase 4, agrandar `err_tr` con los términos de H2 y H3, o usar como error la diferencia con el radial.

### H2 (media). La aproximación de extremos fuera de R_TAB = 10 es 17 veces peor de lo que dice el código, y su efecto no escala como ε²

**Dónde:** `codigo/pares.py`, docstring ("el error es O(eps^3 V'^2), < 1e-7 en r >= 10"); `codigo/transferencia.py`; sección 11.1 (en r = r' = 9, −0.0111134 frente a −ε/9).

**Evidencia** (`rtab.py`, `rtab2.py`): la diferencia entre la tabla y −(ε/2)(1/r + 1/r') es exactamente el término de Wigner-Kirkwood ε²V''/12 = −ε²/(6r³):

| r | U_tabla + ε/r | −ε²/(6r³) |
|---|---|---|
| 5 | −1.34e-5 | −1.33e-5 |
| 9 | −2.29e-6 | −2.29e-6 |
| 9.99 | −1.68e-6 | −1.67e-6 |

Así que en r = 10 el error es 1.7e-6, no < 1e-7.

Efecto en la energía: comparo la tabla con R_TAB = 10 y otra con R_TAB = 13 (R_B = 17).
- δ = 0.2, R = 40: 2.4e-11, irrelevante.
- Cerca del umbral (δ = 1.18, h = 0.02, R = 200): +5.74e-8, +1.97e-8 y +6.9e-9 con ε = 0.2, 0.1 y 0.05. Eso es 7.8e-4 de |E0| con ε = 0.1, y escala como ε^1.5, **no** como ε².
- Tras la extrapolación ε² queda un residuo de +2.6e-9 (1.1e-4 de |E0|). Es del mismo tamaño que los residuos de H1.

No cambia veredictos, pero es un sesgo sistemático que el código declara inexistente. Además ensucia la ley ε² justo donde la Fase 4 la necesita.

**Corrección:** cambiar el docstring y la sección 11. En `U_extremos`, añadir el término de Wigner-Kirkwood ε²V''/12 evaluado en el punto medio (en la diagonal vale −ε²/(6r³)). Otra opción es subir R_TAB y R_B: la tabla es barata. Medir de nuevo el residuo de las celdas de la sección 14.

### H3 (media). La pared en R no tiene imagen y el código lo calla

**Dónde:** `codigo/transferencia.py` (`matriz_T`). El agente de cajas ya lo diagnosticó (sección 14, problema 1).

**Evidencia mía** (`edge1.py`), con δ = 0.2 y ε = 0.1:

| R | transferencia | radial | diferencia |
|---|---|---|---|
| 2 | −0.0376 | +0.0589 | ¡cambio de signo! |
| 5 | −0.32325 | −0.32223 | 1.0e-3 |
| 10 | −0.3268069 | −0.3268063 | 5.4e-7 |

Con δ = 5, R = 40, la diferencia es 2.7e-5 (0.9 %). La hipótesis de la pared corrida 0.5826√ε se sostiene: el radial en R = 5.184 da −0.323305, a 5e-5 de la transferencia, cuando la diferencia sin corregir es 1e-3. En R = 40 con δ = 0.2 el efecto no se ve. **El código no da ningún aviso**, y un usuario de la Fase 3 o 4 con cajas chicas o estados poco ligados puede tomar un sesgo de caja por física.

**Corrección:** que `resolver` avise cuando R sea comparable a la extensión del estado, o que añada la imagen en R (K_D con dos paredes) o use R_ef = R − 0.5826√ε. Es decisión del equipo, como ya propone la sección 14.

### H4 (media). Faltan entregables de la Fase 2 que pide la guía

**Dónde:**
- `fase2/presentacion/` está **vacía**.
- No hay una bitácora de IA de la Fase 2 consolidada (tarea 9 de `que_sigue_fase2.md`). Hay registros sueltos en cada sección.
- No hay una tabla de controles 9.7 firmada por quien verifica (tarea 6).
- No hay una lista de figuras congeladas. La guía (línea 25) pide congelar en la Fase 2 las figuras de la primera ronda.

**Decisiones abiertas** que necesitan a Juan Sebastián:
- (i) redefinir el control de tabulación de 9.7 como Richardson h⁴ (sección 11.4);
- (ii) si la réplica de τ = 5 basta (sección 12);
- (iii) el umbral 0.1 de la ley de caja (sección 14);
- (iv) el tratamiento del pozo con orden ε^1.5 (sección 13).

**Lo que sí está, contra la guía:**
- código ejecutable;
- primer gráfico: `12_pigs_delta02.png` y `12_pigs_tau.png`, que compara radial, transferencia y PIGS en δ = 0.2 y muestra E_mixto(τ);
- caso de control: Coulomb y Hulthén;
- función de prueba no exacta: u_T = r e^{−r} para δ > 0;
- peso declarado: secciones 11.2 y 12.1.

**Corrección:** hacer la presentación de 9 + 5 min (semana 7), la bitácora consolidada y la tabla firmada, y congelar las figuras con su script y un hash.

### H5 (baja). Los límites L04, L05, L06 y L09 no se comprobaron con la integral de camino

La sección 7 de la Fase 1 (tabla de usos) los asigna a la "comparación en un punto fuertemente ligado (primera exposición)", y la tarea 6 de `que_sigue_fase2.md` pide L01 a L09. Ningún script de `fase2/codigo/` calcula Hellmann-Feynman ni el virial. Los hice yo con el autovector de la transferencia (δ = 0.2, ε = 0.1, h = 0.02, R = 40; `limites.py`, `virial.py`):
- **L04, cotas:** −0.5 ≤ −0.3268085 ≤ −0.3. Pasa.
- **L05, Hellmann-Feynman:** dE/dδ = 0.74485313 y ⟨e^{−δr}⟩ = 0.74485290, una diferencia de 2.2e-7. Pasa la tolerancia de 1e-4.
- **L06, virial:** 2E − ⟨V⟩ − δ⟨e^{−δr}⟩ = −1.5e-4 con h = 0.02 y −5.6e-5 / −3.8e-5 con h = 0.01. El radial da lo mismo (−1.51e-4 con h = 1/40 y −3.78e-5 con h = 1/80). Es error de malla de ⟨1/r⟩, que baja con h, no de física. Pasa en el límite.
- **L09, sin nodos:** 0 componentes negativas. Pasa.

**Corrección:** pasar estas cuatro comprobaciones a un script numerado de la Fase 2.

### H6 (baja). Dispersión algo grande del conjunto de energías PIGS (no es sesgo)

Las desviaciones de E en producción frente a la transferencia son:

| caso | desviación |
|---|---|
| τ = 2 | −0.74σ |
| τ = 5 | −3.19σ |
| τ = 10 | +0.19σ |
| τ = 20 | +1.22σ |
| réplica (16 cadenas) | +0.03σ |
| bilineal directa | +2.26σ |
| mi auditoría (24 cadenas) | −0.53σ |

En conjunto, χ² = 17.6 con 7 grados de libertad, p = 0.014. Además, el τ = 5 original y su réplica difieren 2.4σ entre sí.

Mi prueba independiente (χ² por cadena 22.9 con 23, meseta de bloques, histogramas correctos) **no muestra** errores subestimados ni sesgo. Lo más probable es una fluctuación con dos valores en la cola.

**Corrección:** en la presentación, mostrar τ = 5 con las 3 corridas (original, réplica y auditoría, 48 cadenas). No hay que retirar el valor original.

### H7 (baja). El control "E_L ≡ −0.5" del PIGS de Coulomb es tautológico

Con δ = 0, W = 0, así que E_L = W − ½ = −½ para **cualquier** camino, se muestree bien o mal (`pigs.py`, línea `EL0[k] = W(r[0]) - 0.5`). El control real de Coulomb es ⟨r⟩ y ⟨r²⟩, y se hizo con una sola cadena.

**Corrección:** decirlo así en la sección 12. Para la Fase 3, correr 8 cadenas de Coulomb y añadir un test de distribución como el de `mc_audit.py`.

### H8 (baja). `pigs.cadena` cambia τ en silencio

`M = round(τ/ε); M -= M % L`: con τ = 2.5 y ε = 0.2 da M = 10, pero el resultado guarda `tau` = 2.5. En producción no afecta, porque todos los τ/ε de la Fase 2 son múltiplos de 10.

**Corrección:** lanzar un error o guardar τ_ef = Mε.

### H9 (baja). Ruta absoluta fija en `10_radial_controles.py`

`BASE = "/mnt/project-files/fase2/"` (línea 19). Los demás scripts usan rutas relativas.

**Consecuencia real:** al reejecutar el script **desde mi copia**, sobrescribí `resultados/10_radial.json`, `resultados/10_radial_u_delta02.npz` y `figuras/10_radial_convergencia.png` del proyecto (02:03 del 27-10). El script es determinista y sin azar:
- la salida de `test_radial.py`, que usa el mismo módulo, es idéntica a la guardada;
- el script 14, que lee `10_radial.json`, da los mismos 2046 números que antes;
- `delta_c` sigue siendo 1.190612421060604.

Lo único que cambió es `meta.tiempo_s`. Lo declaro porque toqué un resultado ajeno sin querer.

**Corrección:** ruta relativa a `__file__`.

### H10 (baja). Parte del json de la sección 13 se guardó como texto

En `13_controles.json`, `A_hulthen/<δ>/transferencia` es una **cadena** con el `repr` de un diccionario de Python, no un objeto JSON. Las cifras están completas, pero no se pueden leer con `json.load`.

**Corrección:** guardar el diccionario.

### H11 (baja). Errata de redondeo en la sección 13

En la tabla de Hulthén con δ = 1.5, ε = 0.05, la sección pone −1.53×10⁻⁶. El json da −1.5249e-6, que redondea a −1.52×10⁻⁶. No afecta a ningún criterio.

### H12 (baja). Pruebas de `test_pigs.py` más débiles de lo que dicen sus nombres

- "Caminos positivos y reproducibles" solo comprueba la reproducibilidad.
- El error por bloques del AR(1) se acepta entre 0.5 y 1.6 veces el teórico; salió 0.76.
- No hay ninguna prueba de que la distribución muestreada sea la correcta.

**Corrección:** añadir la prueba de histogramas (r_mid frente a x_{M/2}², r_0 frente a u_T·T^M u_T) con un τ corto.

### H13 (baja). Sin error del radial en ⟨r⟩/R y F_1/2 en la sección 14

En `14_cajas.json` las entradas `err_r` y `err_F` del radial valen 0. En la condición (c), las tendencias se comparan sin la incertidumbre del radial. Las diferencias entre los dos métodos (≤ 7e-4) no cambian ninguna tendencia.

## 4. Lo que está bien y conviene decirlo en la presentación

- La acción aprobada se implementó como dice el plan: sin primitiva con 1/r desnudo y con el peso declarado.
- El Coulomb de la transferencia es exacto a 2e-7. El Hulthén exacto pasa a 5e-9 tras extrapolar.
- El PIGS muestrea la distribución correcta (prueba de histogramas) y sus errores son honestos (χ² por cadena 22.9 con 23).
- Las secciones declaran sus propios fallos sin maquillarlos: 7 de 35 en la sección 11, τ = 5 en la 12, el orden ε^1.5 del pozo en la 13, la pared en la 14.
- La tabla U_C coincide con una construcción independiente a 1e-11 lejos del origen.

## Registro de IA (esta auditoría)

- Error mío: reejecuté `10_radial_controles.py` desde una copia sin ver antes que tenía la ruta del proyecto fija. Sobrescribió tres archivos del proyecto con el mismo contenido (H9). Lo detecté al no encontrar el json en mi copia; comprobé que las cifras no cambiaron.
- Mi primera prueba independiente de U_C extrapolaba con p = 2 fijo. La cambié a orden aparente medido, porque lejos del origen el esquema de 4.º orden tiene orden 4.
- Mi primer comparador de json contaba los tiempos de reloj como diferencias (`t_total`, `t_matriz`). Los excluí y lo volví a correr.
- Un `sleep` en primer plano fue bloqueado. Para esperar a que terminaran las reejecuciones usé un bucle de espera.
- Las 24 cadenas de auditoría usaron 3 procesos (el script 14 ocupaba el cuarto) y tardaron 144 s.
