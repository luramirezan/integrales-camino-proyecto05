# 10. Registro de prompts e interacción con la IA (bitácora de IA de la Fase 1)

**Proyecto 05, Umbral de enlace en el potencial de Yukawa** · Fase 1 · Bloque 10

Formato del profesor: "la bitácora mínima conserva fecha, consulta, respuesta utilizada, decisión humana, comprobación y corrección posterior". Formato del grupo: el de las bitácoras 1 y 2 (registro de prompts, modificaciones de los prompts y motivo, errores y correcciones).

**Reglas de este registro.** (1) Solo se registran consultas que constan: en la bitácora de la primera ronda (`bitacora_fase1.md` y sus registros de revisión), en las secciones de la segunda ronda o en el encargo de la propia revisión. (2) Si el texto literal de una consulta no se conservó, se dice y se da solo lo que consta. (3) Donde no consta una decisión humana se escribe "pendiente de confirmar por el equipo"; no se inventa ninguna.

## 10.1 Datos de la sesión y roles

| Campo | Valor |
|---|---|
| Fechas | Primera ronda: 12-10-2026 (fecha de la bitácora y de los registros de revisión de las secciones 5 y 6). Segunda ronda: 12-10-2026. Cambios posteriores: 13-10-2026 (R2-11), 19-10-2026 (R2-12) y 21-10-2026 (verificación independiente y registro de las decisiones del equipo, R2-13) |
| IA | Claude (Anthropic) en las dos rondas. La bitácora de la primera ronda no nombra la IA; que fuera Claude consta en la auditoría de la segunda ronda |
| IA auditora | Claude. Los registros de la primera ronda hablan de revisiones "independientes", pero no consta que se usara otro modelo (ver 10.4, supuesto S1) |
| Integrantes | Juan Sebastián Calixto y Luis Felipe Ramírez. Grupo de dos: Valentina Isabel Burbano se retiró del equipo (confirmado por Lucho el 13-10-2026; ver R2-11) |
| Roles humanos | Fase 1: Juan Sebastián Calixto, formulación física; Luis Felipe Ramírez, implementación y verificación (confirmado por Lucho el 21-10-2026, decisión 6 de `decisiones_pendientes.md`). Fase 2: Juan Sebastián, formulación y verificación; Luis Felipe, implementación (rotación de 9.12, aprobada el mismo día). Referencia de las bitácoras 1 y 2, cuando el grupo era de tres: prompts y línea principal, la integrante que después se retiró; cuestionador, Juan Sebastián Calixto; revisor y verificador, Luis Felipe Ramírez |
| Quién pidió la segunda ronda | Luis Felipe Ramírez (Lucho) |

## 10.2 Registro de consultas

Las fichas R1 son de la primera ronda; las R2, de la segunda. En la primera ronda los prompts literales no se conservaron en la carpeta del proyecto: se registra el encargo que se deduce de lo que consta en cada sección y en sus registros de revisión.

### Tabla resumen

| ID | Fecha | Consulta (resumen) | Respuesta utilizada | Decisión humana | Comprobación | Corrección posterior |
|---|---|---|---|---|---|---|
| R1-01 | 12-10-2026 | Adimensionalizar la ecuación radial | Sección 1 y `01_adimensionalizacion.py` | aprobado por Lucho el 21-10-2026, con la condición de verificar una vez más; verificación independiente hecha el mismo día (decisión 1; R2-13) | sympy (residuo 0), RK45, dos revisiones adversariales | R2: se quitó "factores del enunciado"; CODATA y Debye y Hückel marcados no verificados |
| R1-02 | 12-10-2026 | Límite de Coulomb y serie de $E_0(\delta)$ | Sección 2 y `02_limite_coulomb.py` | aprobado por Lucho el 21-10-2026, con la condición de verificar una vez más; verificación independiente hecha el mismo día (decisión 1; R2-13) | sympy, diagonalización, ajuste polinómico | R1: signo de Dalgarno-Lewis; interpretación del término $+\delta$. R2: ansatz de $F$ |
| R1-03 | 12-10-2026 | Cota inferior variacional | Sección 3 y `03_cota_variacional.py` | aprobado por Lucho el 21-10-2026, con la condición de verificar una vez más; verificación independiente hecha el mismo día (decisión 1; R2-13) | sympy, `quad`, DF independiente | R2: fila de $\delta=1$; cifra $10^{-9}$ sin salida; intervalo unificado |
| R1-04 | 12-10-2026 | Cotas superiores (Bargmann, Calogero, Schwinger) | Sección 4 y `04_cota_bargmann.py` | aprobado por Lucho el 21-10-2026, con la condición de verificar una vez más; verificación independiente hecha el mismo día (decisión 1; R2-13) | sympy, disparo a $E=0$ | R1: "factor $1/\delta$ del enunciado". R2: esa corrección no tenía objeto; curva de Calogero; nodos |
| R1-05 | 12-10-2026 | Referencia numérica independiente de $\delta_c$ | Sección 5 y `05_referencia_numerica.py` | aprobado por Lucho el 21-10-2026, con la condición de verificar una vez más; verificación independiente hecha el mismo día (decisión 1; R2-13) | cuatro métodos; independencia de $R$ | R1: matiz sobre el signo de $B$. R2: atribución a Rogers et al., coeficiente $c\approx0.741$ e intervalo unificado (aplicados en R2, ver 10.3) |
| R1-06 | 12-10-2026 | Verificar las referencias | Sección 6 y `06_fuentes.py` | aprobado por Lucho el 21-10-2026, con la condición de verificar una vez más; verificación independiente hecha el mismo día (decisión 1; R2-13) | Crossref, arXiv, INSPIRE, Europe PMC | R1: DOI de Bargmann (fascículo 11); segunda pasada (Edwards frente a Gebremedhin). R2: estado de Gebremedhin y Weatherford, cadena de cotas, ejemplo de caja de 2(c), Wikipedia, numeración (aplicados en R2, ver 10.3) |
| R1-07 | 12-10-2026 | Revisiones adversariales de cada bloque (matemática; física y numérica) | Registros de revisión de las secciones 1 a 6 y registro consolidado | aprobado por Lucho el 21-10-2026, con la condición de verificar una vez más; verificación independiente hecha el mismo día (decisión 1; R2-13) | re-ejecución de los scripts | R2: varias revisiones dijeron "sin errores" en bloques que sí los tenían (ver 10.5) |
| R2-01 | 12-10-2026 | Pedido de Lucho: completar y corregir la Fase 1 siguiendo la guía | Plan de la segunda ronda: auditoría, secciones 00 y 07 a 10, correcciones de 01 a 06 | el pedido mismo es la decisión humana de abrir la ronda; lo demás lo aprobó Lucho el 21-10-2026 (decisiones 1 a 6), salvo el material de presentación (decisión 7, pendiente) | n/d | n/d |
| R2-02 | 12-10-2026 | Auditoría de la Fase 1 contra la guía del profesor y la guía de bitácora | Lista de hallazgos con archivo, problema, criterio, corrección y gravedad | aprobado por Lucho el 21-10-2026 (decisión 2) | cada hallazgo cita el archivo y la línea; varios con cálculo propio | ver 10.5, anomalía A12 |
| R2-03 | 12-10-2026 | Lista de límites físicos que debe cumplir el algoritmo | Sección 7, lista L01 a L19 | sección 7: "adoptar la lista como batería de pruebas de la Fase 2 con las correcciones de 7.4"; aprobado por Lucho el 21-10-2026 (decisión 3) | `07_limites_fisicos.py`, ítem por ítem | L13 corregido; L10, L11 y L17 precisados |
| R2-04 | 12-10-2026 | Acción euclídea, peso y remedios | Sección 8 y `08_accion_euclidea.py` | aprobado por Lucho el 21-10-2026, con la elección de R1 (decisión 4) | prueba analítica y numérica de la divergencia; toy model | cinco errores de Claude corregidos al ejecutar (sección 8) |
| R2-05 | 12-10-2026 | Plan de cómputo de las Fases 2 a 4 | Sección 9 y `09_prueba_costos.py` | aprobado por Lucho el 21-10-2026: formulación (decisión 4); criterio de enlace, controles y calendario (decisión 5); roles (decisión 6) | prueba de concepto ejecutada; costos medidos | cinco errores de Claude corregidos al ejecutar (sección 9); la revisión adversarial de lo nuevo corrigió la explicación del quinto y encontró cuatro más (R2-09) |
| R2-06 | 12-10-2026 | Marco: pregunta, régimen, cierre, hipótesis, genealogía, toy model | Sección 0 y `00_toy_model.py` | aprobado por Lucho el 21-10-2026: pregunta, régimen, cierre y notación (decisión 2); Hulthén como control (decisión 5) | sympy (residuos 0), DF, disparo | tres correcciones menores (sección 0) |
| R2-07 | 12-10-2026 | Esta bitácora de IA consolidada | Sección 10 | pendiente de confirmar por el equipo (ninguna de las siete decisiones lo cubre; desde el 21-10-2026 recoge las decisiones 1 a 6, R2-13) | cotejo con la bitácora y las secciones | n/d |
| R2-08 | 12-10-2026 | Aplicar las correcciones de la auditoría a las secciones 01 a 06 | Registros "Corrección posterior (ronda 2 de auditoría, Claude, 12-10-2026)" de cada sección | aprobado por Lucho el 21-10-2026 (decisión 2) | re-ejecución de los scripts | ver 10.3 |
| R2-09 | 12-10-2026 | Revisión adversarial de las secciones nuevas (00, 08, 09, 10) y aplicación de sus correcciones | 12 hallazgos; decisiones en `correcciones_ronda2.md`, apartado "Revisión adversarial de lo nuevo" | aprobado por Lucho el 21-10-2026 (decisión 2) | cada hallazgo se comprobó con un cálculo propio antes de aplicarlo; scripts 08 y 09 re-ejecutados (09 dos veces) | K15 a K19 de 10.3 |
| R2-11 | 13-10-2026 | Pedido de Lucho: el grupo queda de dos; quitar a la integrante que se retiró de guion, diapositivas, bitácora y secciones, y repartir la exposición entre dos | Guion (1 a 6, Juan Sebastián; 7 a 11, Luis Felipe), portada y notas de las diapositivas, 0.0, 9.12, 10.1, 10.7, `correcciones_ronda2.md` y bitácora | la composición del grupo la confirmó Luis Felipe Ramírez (Lucho) el 13-10-2026; la rotación de 9.12 la aprobó Lucho el 21-10-2026 (decisión 6); el reparto de la exposición de 9 min lo sustituyó el de 15 min de R2-12 | búsqueda de texto sin coincidencias salvo la mención del retiro; PDF del guion, de la bitácora y de las diapositivas regenerados y revisados | n/d |
| R2-12 | 19-10-2026 | Pedido de Lucho: presentación de 15 minutos sobre la Fase 1, cerrar la Fase 1 y decir qué sigue en la Fase 2 | Diapositivas de 18 láminas (nuevas: toy model, cota inferior, auditoría de la IA, divergencia del peso y acción de pares, caja finita, Fase 2), guion de 15 min con reparto y preguntas ampliadas, `que_sigue_fase2.md` y `decisiones_pendientes.md` | el pedido es de Lucho; el 21-10-2026 aprobó el plan (decisión 5) y el reparto de la exposición (decisión 6); la aprobación de las diapositivas y el guion (decisión 7) sigue pendiente | cada cifra nueva sale de una salida de los scripts 00, 03, 06, 07, 08 y 09 (el 06 se re-ejecutó en una copia; sus umbrales de caja tenían error de malla y se corrigieron en R2-13); diapositivas renderizadas y revisadas lámina por lámina; PDF del guion y de la bitácora regenerados | n/d |
| R2-13 | 21-10-2026 | Pedido de Lucho: verificar una vez más los resultados antes de aprobarlos (condición de la decisión 1), y registrar las decisiones de `decisiones_pendientes.md` | Verificación independiente de las cifras de los bloques 1 a 9 (disparo con mpmath y DOP853, Chebyshev, cotejo de fuentes); corrección del umbral de caja de 6.2(c) y `06_fuentes.py`; correcciones de redacción del cotejo; decisiones 1 a 6 pasadas a esta tabla, a las fichas y a los registros de cada sección | la verificación la pidió Lucho; las decisiones 1 a 6 son suyas (21-10-2026); la 7 sigue pendiente; faltan las firmas de la hoja | todo coincidió salvo los umbrales de una sola caja de 6.2(c) (error de malla de unos $-2\times10^{-4}$); `06_fuentes.py` re-ejecutado; PDF de la bitácora y del guion regenerados; láminas cambiadas renderizadas | K20 de 10.3 |

### Fichas

**R1-01 a R1-06. Redacción de los bloques de la primera ronda.**
- *Consulta:* texto literal no conservado. Por el contenido, a la IA se le encargó cada bloque con su script de verificación (sympy y numérico) y su figura. Los encabezados de bloque dicen "Fase 1 (parte analítica)".
- *Respuesta utilizada:* las secciones 1 a 6 y los scripts `01` a `06`, que se compilaron en `bitacora_fase1.md`, `bitacora_fase1.pdf`, el guion y las diapositivas.
- *Decisión humana:* Lucho aprobó los resultados de los bloques 1 a 6 el 21-10-2026, con la condición de verificarlos una vez más (decisión 1 de `decisiones_pendientes.md`). La verificación independiente se hizo ese mismo día (R2-13): todo coincidió salvo el ejemplo de caja de 6.2(c), que se corrigió.
- *Comprobación:* cada bloque tiene su script y al menos dos revisiones adversariales (R1-07).

**R1-07. Revisiones adversariales de la primera ronda.**
- *Consulta:* texto literal no conservado. Consta que cada bloque pasó por dos revisiones, una de "corrección matemática" y otra de "física y consistencia numérica", con re-ejecución de los scripts.
- *Respuesta utilizada y correcciones que constan:*
  1. Bloque 02: la ecuación de Dalgarno-Lewis estaba escrita como $[H_0,F]u_1=(W_2-\langle W_2\rangle)u_1$, inconsistente en signo con $F=r^2/4-3/4$; se cambió a $[F,H_0]$ y se añadió la EDO radial explícita.
  2. Bloque 02: la interpretación del término $+\delta$ decía "cerca del origen"; a primer orden es un desplazamiento constante global (válido donde $\delta r\ll1$). Se reformuló.
  3. Bloque 04: se "aclaró la interpretación del factor $1/\delta$ del enunciado (correcto: $2/\delta$)". La segunda ronda encontró que ningún documento contiene ese $1/\delta$ ni atribuye al enunciado el intervalo $[1,2]$ (anomalía A1).
  4. Bloque 06: DOI de Bargmann corregido (fascículo 11: 10.1073/pnas.38.11.961).
  5. Bloque 06, segunda pasada: se verificaron los metadatos de Gebremedhin y Weatherford (no su valor de $\delta_c$, que viene de una cita secundaria), Schwinger y Calogero, y se concluyó que el valor de Edwards et al. difiere en $2\times10^{-7}$ del de alta precisión, con el que coincide el cálculo propio. Se pasó a usar Gebremedhin y Weatherford como referencia principal.
  6. Observaciones sin cambio: escape de `minimize_scalar` a $b\to\infty$ (bloque 03); avisos de overflow (bloque 03); $N=16$ peor que $N=12$ (bloque 03); signo de $B$ (bloque 05).
- *Decisión humana:* aprobadas con los bloques 1 a 6 (Lucho, 21-10-2026, decisión 1, tras la verificación de R2-13).
- *Comprobación:* re-ejecución de los scripts por la propia IA.
- *Corrección posterior:* ver 10.3 y 10.5. Lo más importante: las revisiones no detectaron el error de la curva de Calogero, la fila de $\delta=1$ en la tabla de 3.2.3, la atribución de diez cifras a Rogers et al., ni la falta de bitácora de IA, acción, peso y plan.

**R2-01. Pedido de la segunda ronda.**
- *Consulta:* de Luis Felipe Ramírez (Lucho), 12-10-2026: completar y corregir la Fase 1 siguiendo la guía. Resumen del encargo; el texto literal no está en la carpeta del proyecto.
- *Respuesta utilizada:* la organización de la ronda en auditoría, secciones nuevas (00, 07, 08, 09, 10) y correcciones de las existentes.
- *Decisión humana:* el pedido mismo. Las decisiones sobre el resultado las tomó Lucho el 21-10-2026 (decisiones 1 a 6 de `decisiones_pendientes.md`); la 7, sobre el material de presentación, sigue pendiente.

**R2-02. Auditoría.**
- *Consulta:* auditar la Fase 1 (bitácora, secciones, scripts, guion y diapositivas) contra `guia_texto.txt`, `resumen_fases_proyecto05.md` y `guia_bitacora.md`, con archivo, ubicación, problema, criterio, corrección y gravedad por hallazgo.
- *Respuesta utilizada:* los hallazgos de gravedad alta fueron: faltaba la bitácora de IA; faltaban la acción euclídea y la declaración del peso; el objetivo no era una pregunta; no había criterio de cierre ni régimen de validez; la sección 07 no estaba integrada; no había plan de cómputo; se atribuía al "enunciado" un intervalo $[1,2]$ y un factor $1/\delta$ inexistentes; la curva de Calogero de la figura 04 tenía un factor $\sqrt2$ de menos; el guion y las diapositivas solo tenían dos integrantes y no tenían las diapositivas de límites, acción, peso y plan.
- *Decisión humana:* aprobada por Lucho el 21-10-2026 con las correcciones K1 a K19 (decisión 2).
- *Comprobación:* cada hallazgo cita el archivo y la línea; algunos traen un cálculo propio (por ejemplo, la divergencia $\int r^2e^{\epsilon/r}dr$ con sympy o la cota de Calogero con `quad`).
- *Corrección posterior:* dos hallazgos sobre la desviación de la serie en $\delta=0.3$ parecían contradecirse (A12); se resolvió.

**R2-03. Límites físicos (requisito explícito del profesor).**
- *Consulta literal:* la de la sección 7.1 ("Para la ecuación radial $-\tfrac12u''-e^{-\delta r}u/r=Eu$ ... dame una lista numerada de límites físicos y propiedades exactas ... Indica explícitamente si el peso que se pretende muestrear es real, positivo y normalizable.").
- *Respuesta utilizada:* la lista L01 a L19 (sección 7.2), guardada antes de verificar.
- *Decisión humana:* "adoptar la lista como batería de pruebas de la Fase 2 con las correcciones de 7.4" (sección 7); aprobado por Lucho el 21-10-2026 (decisión 3).
- *Comprobación:* `07_limites_fisicos.py`, ítem por ítem (sección 7.3): 14 confirmados tal cual, 3 precisados, 1 corregido y 1 que solo puede probarse en la Fase 2.
- *Corrección posterior:* L13 ($E_0R^2\to\pi^2/2$ solo para $R\to\infty$; falta la longitud de dispersión); L10 ($c\approx0.75$ es la pendiente secante; el coeficiente asintótico es $0.741$); L11 y L17 precisados (sección 7.4).

**R2-04. Acción euclídea y peso.**
- *Consulta:* la que consta en el registro de la sección 8 (deducir la integral de camino euclídea, analizar si el peso es real, positivo y normalizable, listar remedios, resolver un toy model).
- *Respuesta utilizada:* sección 8. Veredicto: el peso es real y positivo, pero no es normalizable con la acción primitiva; el núcleo exacto sí lo es. Recomendación: R1 (acción de pares de Coulomb).
- *Decisión humana:* aprobado por Lucho el 21-10-2026, con R1 como acción de la Fase 2 (decisión 4).
- *Corrección posterior:* cinco errores de Claude detectados al ejecutar (ajuste de sesgo con NaN, PIMC sin Metropolis, $E_0(a_s)$ con paso comparable a $a_s$, ventana de ajuste contaminada, método de imagen que no elimina la divergencia), registrados en la sección 8.

**R2-05. Plan de cómputo.**
- *Consulta:* la que consta en el registro de la sección 9.
- *Respuesta utilizada:* sección 9 (observables, referencia, formulación, parámetros, criterio de enlace con varias cajas, controles, presupuesto de errores, costo medido, calendario, riesgos, roles propuestos).
- *Decisión humana:* aprobado por Lucho el 21-10-2026: formulación (decisión 4), plan, criterio de enlace, controles y calendario (decisión 5) y roles (decisión 6).
- *Corrección posterior:* cinco errores de Claude registrados en la sección 9 (PIGS con movimientos locales, error por bloques subestimado, NaN en la matriz en banda, falta de Richardson en $h_{\rm tab}$, estimador mixto frente al autovalor). La explicación del quinto era errónea: la diferencia de $4.9\times10^{-5}$ entre el límite del mixto y el autovalor de la transferencia no es un sesgo $O(\epsilon^2)$, porque no cambia con $\epsilon$ y baja como $h^2$; es el error de malla del núcleo de Coulomb de diferencias finitas en $h=0.02$, y el mixto converge de forma monótona (revisión adversarial R2-09, K15).

**R2-09. Revisión adversarial de lo nuevo y sus correcciones.**
- *Consulta:* tarea asignada a Claude por el flujo de revisión: revisar de forma adversarial las secciones 00, 08, 09 y 10, y después aplicar los hallazgos comprobando cada uno antes de corregir.
- *Respuesta utilizada:* 12 hallazgos (K15 a K19 y la actualización de estados de 10.3, 10.4 y 10.7); todos se comprobaron y se aplicaron. La lista con la decisión de cada uno está en `correcciones_ronda2.md`.
- *Decisión humana:* aprobado por Lucho el 21-10-2026 (decisión 2: correcciones K15 a K19).
- *Comprobación:* scripts `08_accion_euclidea.py` y `09_prueba_costos.py` modificados y re-ejecutados; `02_limite_coulomb.py` re-ejecutado para A12; cotejo con las secciones 5 y 6, la bitácora y `correcciones_ronda2.md` para los estados.
- *Corrección posterior:* n/d por ahora.

**R2-06 y R2-07. Marco y esta bitácora.**
- *Consulta:* tarea asignada a Claude por el flujo de revisión (sección 0, "Registro de IA de este bloque").
- *Comprobación:* `00_toy_model.py` ejecutado; este registro se cotejó con `bitacora_fase1.md` y con los registros de las secciones 1 a 9.

**R2-08. Correcciones de la auditoría en las secciones 01 a 06.** Lo que consta en cada sección al escribir este registro se resume en 10.3.

**R2-11. Grupo de dos integrantes (13-10-2026).**
- *Consulta:* Lucho informó que el grupo es de dos y pidió quitar del material a la integrante que se retiró y repartir la exposición entre Juan Sebastián Calixto y Luis Felipe Ramírez con los mismos textos.
- *Respuesta utilizada:* reparto equilibrado de las 11 diapositivas expuestas (4 min 35 s y 4 min 15 s), rotación de roles entre dos en 9.12 y actualización de autoría en las secciones y la bitácora.
- *Decisión humana:* la composición del grupo (confirmada por Lucho). La rotación de 9.12 la aprobó Lucho el 21-10-2026 (decisión 6); el reparto de bloques de esta ficha lo sustituyó el de R2-12.
- *Comprobación:* búsqueda de texto en todos los archivos de `fase1`; PDF regenerados y revisados por páginas.
- *Corrección posterior:* n/d.

**R2-12. Presentación de 15 minutos, cierre de la Fase 1 y qué sigue (19-10-2026).**
- *Consulta:* Lucho pidió una presentación de 15 minutos sobre la Fase 1, decir qué hay que hacer para cerrarla por completo y qué sigue en la Fase 2.
- *Respuesta utilizada:* la exposición se amplió de 8 min 50 s a unos 14 min 55 s (2224 palabras a unas 150 por minuto) con contenido ya verificado de la bitácora que el guion de 9 minutos omitía: toy model (0.6), cota inferior y cotas superiores por separado (3 y 4), divergencia del peso y acción de pares (8.4, 8.5 y 8.7), caja finita (9.6, 7, L12) y auditoría de la IA (10.3 a 10.5). Se añadió una lámina final sobre la Fase 2. Reparto: Juan Sebastián, láminas 1 a 9 (7 min 35 s); Luis Felipe, 10 a 17 (7 min 20 s). Se escribieron `que_sigue_fase2.md` (pedido de la guía, plan de la sección 9 y tareas con responsable) y `decisiones_pendientes.md` (siete decisiones que cierran C9).
- *Decisión humana:* el pedido (Lucho). El 21-10-2026 Lucho aprobó el reparto de la exposición (decisión 6) y el plan de la Fase 2 (decisión 5) de `decisiones_pendientes.md`; la aprobación de las diapositivas y el guion (decisión 7) sigue pendiente.
- *Comprobación:* ninguna cifra nueva se inventó: todas se tomaron de las secciones y de las salidas de los scripts (el 06 se re-ejecutó en una copia: 1.17685 con R = 100 y 1.18870 con R = 800; esas cifras tenían un error de malla y el 21-10-2026 se corrigieron a 1.17701 y 1.18892, ver R2-13). Se renderizaron las 18 láminas y se corrigieron textos cortados, entre ellos el "9/|E0|" partido de la lámina del plan, y la gráfica de cotas pasó a ocupar media lámina.
- *Corrección posterior:* n/d. Aviso: la guía da 9 min de exposición por equipo; hay que confirmar con el profesor que la sesión admite 15 min.

**R2-13. Verificación independiente, cotejo y registro de las decisiones (21-10-2026).**
- *Consulta:* al rellenar `decisiones_pendientes.md`, Lucho aprobó la decisión 1 con la condición de verificar una vez más los resultados. Se pidió a Claude una verificación independiente de las cifras de la bitácora y un cotejo de las fuentes, corregir lo que no coincidiera y pasar las decisiones de la hoja al registro.
- *Respuesta utilizada:* la verificación recalculó las cifras principales por vías distintas de las de los scripts (disparo con mpmath y DOP853, método espectral de Chebyshev). Todo coincidió salvo los umbrales aparentes de una sola caja de 6.2(c): $1.17685$, $1.18366$, $1.18704$ y $1.18870$ se habían calculado con diferencias finitas de paso $h=0.02$ y mezclaban un error de malla de unos $-2\times10^{-4}$ con el sesgo de caja. Los valores exactos de la caja son $1.177013$, $1.183840$, $1.187233$ y $1.188924$, con $R(\delta_c-\delta_c(R))=1.360$, $1.355$, $1.352$ y $1.351$. El cotejo además corrigió la nota de método de la sección 6 (de Gebremedhin y Weatherford se verificaron los metadatos, no el valor) y confirmó en arXiv:2510.10420, tabla II, las cifras $1.19061242106061770534277710636105$ (Gebremedhin y Weatherford) y $1.1906122105(5)$ (Edwards et al.).
- *Decisión humana:* de Lucho, 21-10-2026: decisiones 1 (con la verificación ya hecha) a 6 aprobadas; roles de la Fase 1: Juan Sebastián Calixto, formulación física; Luis Felipe Ramírez, implementación y verificación; la decisión 7 (material de presentación) sigue pendiente. Las firmas de la hoja siguen en blanco.
- *Comprobación:* `06_fuentes.py` reescrito para calcular el umbral de caja por disparo con $u(R)=0$ y re-ejecutado: reproduce los valores de la verificación. Las cifras viejas se reemplazaron en 6.2(c), en `correcciones_ronda2.md`, en la bitácora, en el guion y en la lámina 14 del pptx; las cifras antiguas de los registros de revisión se conservan con una nota de valor actualizado. PDF de la bitácora y del guion regenerados y revisados por páginas.
- *Corrección posterior:* K20 de 10.3. Estados desactualizados de K5, K9, K12, N7, 10.7 y de los hallazgos 26, 29, 41 y 42 marcados como aplicados (19-10-2026, R2-12).

## 10.3 Correcciones posteriores (qué se afirmó, por qué estaba mal, cómo se corrigió)

| # | Dónde | Qué se afirmó | Por qué estaba mal | Corrección | Estado |
|---|---|---|---|---|---|
| K1 | 2.2 | $[H_0,F]u_1=(W_2-\langle W_2\rangle)u_1$ | signo inconsistente con $F$ | $[F,H_0]$ y EDO explícita | corregido en R1 |
| K2 | 2.2 | el término $+\delta$ actúa "cerca del origen" | a primer orden es una constante global | reformulado | corregido en R1 |
| K3 | 6 | DOI de Bargmann con fascículo 10 | es el 11 | 10.1073/pnas.38.11.961 | corregido en R1 |
| K4 | 6 y resumen | Edwards et al. como valor de referencia | difiere en $2\times10^{-7}$ del de alta precisión | se usa Gebremedhin y Weatherford | corregido en R1 y en R2 (la cadena de cotas de 6.2 cita ahora Gebremedhin y Weatherford y el método C) |
| K5 | 1, 2, 4, bitácora, guion, diapositiva 7 | "el enunciado decía $1/\delta$" y "intervalo pedido en el enunciado $1\le\delta_c\le2$" | ningún documento lo dice; la guía solo pide "derivar un criterio de estado ligado"; la presentación previa ya usaba $2/\delta$ | quitar la atribución; el factor 2 queda como comprobación propia | corregido en 1, 2, 4 y `bitacora_fase1.md` (R2); en el guion, las diapositivas y el PDF de la bitácora, aplicado el 19-10-2026 (R2-12): el guion ya no dice "corregimos el enunciado" |
| K6 | 2.2 | el ansatz $F=a_1r+a_2r^2$ da $F=r^2/4-3/4$ | el ansatz no tiene término constante | $F=a_0+a_1r+a_2r^2$ | corregido en R2 |
| K7 | 3.2.3 | en $\delta\ge1$, $b^*=\infty$ | en $\delta=1$ el mínimo es $E=0$ en $b=2$; el $\infty$ era un escape de `minimize_scalar` | fila separada; búsqueda acotada | corregido en R2 |
| K8 | 3.3 | coincidencia "a $10^{-9}$" | ningún script lo imprimía | se añadió el cálculo al script | corregido en R2 |
| K9 | 4, figura 04, diapositiva 7 | curva de Calogero $\sqrt{8/(\pi\delta)}$ | falta $\sqrt2$; la curva corta 1 en $8/\pi$ y no en $16/\pi$ | $4/\sqrt{\pi\delta}$; figura regenerada | corregido en 4 (R2); en las diapositivas (figura regenerada en la lámina 10 del pptx), aplicado el 19-10-2026 (R2-12) |
| K10 | 3.4, 4.5, 5.6 | tres intervalos distintos para $\delta_c$ | incoherencia | $1.19055\le\delta_c\le1.24305$ | corregido en 3, 4 y 5 (R2) |
| K11 | 5, 4.6, bitácora | $1.190612421$ atribuido a Rogers et al. (1970) | la sección 6 solo les atribuye $\approx1.19$ | atribuir las diez cifras solo a Gebremedhin y Weatherford | corregido en 3.4, 4.5, 4.6, 5 y `bitacora_fase1.md` (R2) |
| K12 | 6, bitácora, diapositiva 10 | "todas las referencias verificadas"; Crossref "da" $\delta_c$ | el valor se tomó de una cita secundaria (arXiv:2510.10420) | "metadatos verificados; valor no verificado en fuente primaria" | corregido en 0.7, 6 y `bitacora_fase1.md` (R2); en el guion, las diapositivas y el PDF de la bitácora, aplicado el 19-10-2026 (R2-12): el guion ya no dice "todas las referencias quedaron verificadas" |
| K13 | 5.4, bitácora | $c\approx0.75$ como ley de umbral | es la pendiente secante | $c\approx0.741$ (sección 7, L10) | corregido en 5.4 y en `bitacora_fase1.md` (R2) |
| K14 | 7, L13 (respuesta de la IA) | sin ligado, $E_0R^2\to\pi^2/2$ | solo si $R\to\infty$; falta la longitud de dispersión | ley $\pi^2/[2(R-a_{\rm sc})^2]$ | corregido en 7.4 |
| K15 | 9.5 D, 9.13 y registro de 9 | la diferencia de $4.9\times10^{-5}$ entre el mixto y el autovalor de $T$ es un sesgo $O(\epsilon^2)$; el mixto "no es monótono" | la diferencia no cambia con $\epsilon$ y baja como $h^2$ (error de malla del Coulomb de diferencias finitas en $h=0.02$); la serie impresa era $E_{\rm mixto}-E_0(T)$, no el mixto menos su límite | atribuir al error de malla; comparar tras Richardson en $h$ y extrapolar $\epsilon$; el mixto es monótono | corregido en R2 (R2-09) |
| K16 | 9.6 y 9.8 | tabla de cajas con $h=1/20$ sin Richardson tomada como energía del estado | sesgo del 18 % de $|E_0|$ en $\delta=1.18$ | tabla con Richardson en $h$; criterio (a') de convergencia en $h$; fila de malla en 9.8 | corregido en R2 (R2-09) |
| K17 | 8.6 | $-\partial_\beta\ln Z$ variando $M$ a $\epsilon$ fijo presentado como estimador termodinámico | esa derivada da la energía del autovalor; el estimador de 8.2.7 es a $M$ fijo | se dan las dos derivadas, con la forma cerrada $\tfrac12\theta'(\epsilon)\coth(M\theta/2)$ | corregido en R2 (R2-09) |
| K18 | 8.8 y 9.9 | costo de PIGS cerca del umbral con $\tau=5/|E_0|$ | 9.4 y 9.7 exigen $\tau\ge9/|E_0|$ (sección 7, L15) | $M=8750$ y 39349; costo 1.8 veces mayor | corregido en R2 (R2-09) |
| K19 | 8.4.2, 8, 9 y 10 | "cambian en la segunda cifra decimal"; tiempos únicos como "medidos"; $\kappa\lesssim0.004$ en $\delta=1.195$; $E_0(0.3)$ "recalculado en esta sección con $R=80$" | cambia en la primera cifra en $\epsilon=0.2$; los tiempos varían un factor 2 a 3; $\delta=1.195>\delta_c$; la cifra sale de `02_limite_coulomb.py` con $R=60$ | cifras y atribuciones corregidas; tiempos como rangos | corregido en R2 (R2-09) |
| K20 | 6.2(c), `06_fuentes.py`, `correcciones_ronda2.md`, bitácora, guion y lámina 14 | umbral aparente de una sola caja: $1.17685$ ($R=100$) a $1.18870$ ($R=800$), presentado como sesgo de caja | se calculó con diferencias finitas $h=0.02$: mezclaba un error de malla de unos $-2\times10^{-4}$ con el sesgo de caja | disparo a energía cero con $u(R)=0$, sin malla: $1.177013$, $1.183840$, $1.187233$, $1.188924$; $R(\delta_c-\delta_c(R))=1.360$ a $1.351$ | corregido el 21-10-2026 (R2-13) |

## 10.4 Supuestos implícitos de la IA y de las fuentes

| # | Supuesto | De quién | Cómo se comprobó | Estado |
|---|---|---|---|---|
| S1 | Que las dos revisiones adversariales de cada bloque eran independientes | IA, primera ronda | las hizo la misma IA (Claude); comparten sesgos. La prueba es que ninguna detectó K5, K7, K9 ni K11 | abierto: conviene una auditoría con otro modelo en la Fase 3 (la guía la pide) |
| S2 | Que existía un "enunciado" con $1/\delta$ y $[1,2]$ | IA, primera ronda | búsqueda en `guia_texto.txt` y en los materiales previos (auditoría) | falso; K5 |
| S3 | Que Rogers et al. dan diez cifras | IA, primera ronda | la sección 6 les atribuye $\approx1.19$ | falso; K11 |
| S4 | Que Crossref verifica el valor de $\delta_c$ | IA, primera ronda | Crossref solo da metadatos | falso; K12 |
| S5 | Que el $1s$ es el último estado en desligarse | IA, implícito en todas las secciones | en un potencial central el fundamental es $\ell=0$ y sin nodos | cierto; declarado como H5 (sección 0.4) |
| S6 | Que la caja de Dirichlet solo sube la energía | IA, secciones 5 y 6 | monotonía de Dirichlet; comprobado en 7, L12 | cierto; declarado como H6. Consecuencia no prevista: una caja pequeña puede dar un falso "no ligado" ($\delta=1.18$, $R=20$, sección 7.4) |
| S7 | Que una sola caja ($R=400$) basta para un "umbral numérico" | IA, sección 6.2(c) | 7, L12: el sesgo es lineal en $1/R$ | falso como criterio; resuelto en R2: 6.2(c) es ahora un ejemplo del sesgo de caja con cuatro cajas |
| S8 | Que la pendiente secante es el coeficiente asintótico | IA, 5.4 y la respuesta L10 | 7.3, L10 | precisado; K13 |
| S9 | Que la integral de camino primitiva sirve tal cual para $1/r$ | IA, "Qué pasa a la Fase 2" de la primera ronda | sección 8.4: el peso primitivo no es normalizable | falso; resuelto en la sección 8 |
| S10 | Que `minimize_scalar` halla el mínimo global | IA, sección 3 | K7 | falso en $\delta=1$; corregido |
| S11 | Que la transcripción por IA de Kleinert (cap. 2) y de Saporiti es fiel | fuentes del curso | sección 8.9: posible error en la medida (Kleinert, ec. 2.376) y en el estimador $F_K$ (Saporiti, ec. 24) | abierto: cotejar con el PDF |
| S12 | Que Wikipedia vale como vía de verificación | IA, sección 6 | la regla exige fuente primaria o índice bibliográfico | resuelto en R2: la sección 6 dice "Wikipedia no se usa como fuente de verificación" |
| S13 | Que el apantallamiento de Debye vale en todo plasma | fuentes y sección 1.5 | solo en acoplamiento débil | declarado en 0.2, punto 3 |
| S14 | Que Duru y Kleinert (1979) y Kustaanheimo y Stiefel (1965) dicen lo que Fujikawa resume | fuente del curso (Fujikawa 1996) | no se abrió la fuente primaria | no verificado; así se marca en 0.7 y 8.5 |

## 10.5 Anomalías y discrepancias

| # | Anomalía | Dónde | Explicación o estado |
|---|---|---|---|
| A1 | Factor "$1/\delta$" e intervalo "$[1,2]$" atribuidos al enunciado | 1, 2, 4, bitácora, guion | no existen en la guía; K5 |
| A2 | Edwards et al. difiere $2\times10^{-7}$ | 6 | explicado: su valor queda fuera del consenso de alta precisión; nuestro cálculo coincide con este |
| A3 | Ritz con $N=16$ da una cota peor que con $N=12$ | 3.4 | base geométrica restringida; anotado en R1 |
| A4 | $\delta_c\approx1.187$ con $R=400$ | 6.2(c) | sesgo de caja; ley lineal en $1/R$ (7, L12). Sin error de malla, $1.187233$ (K20) |
| A5 | Avisos de overflow de `lambdify` | 3 | inofensivos (R1) |
| A6 | $b^*=1.6\times10^5$ en $\delta=1$ | 3.2.3 | artefacto; K7 |
| A7 | La curva de Calogero corta en $8/\pi$ y el texto dice $16/\pi$ | 4 | K9 |
| A8 | $2\kappa\langle r\rangle=1.25$ en $\delta=1$ y no 1 | 7, L11 | la ley de halo es asintótica |
| A9 | Falso "no ligado" con signo equivocado ($E_0=+2.95\times10^{-3}$ en $\delta=1.18$, $R=20$) | 7.4 | justifica el criterio de varias cajas (9.6) |
| A10 | Signo y constante del estimador $F_K$ de Saporiti | 8.9 | abierto; S11 |
| A11 | Medida $dx_n/\sqrt{2\pi\beta/M}$ en el Markdown de Kleinert | 8.9 | abierto; S11 |
| A12 | Dos hallazgos de la auditoría daban desviaciones distintas de la serie en $\delta=0.3$: $9.86\times10^{-3}$ (3.8 %) y $1.93\times10^{-3}$ (0.75 %) | auditoría del guion y de la diapositiva 4 | no se contradicen: la primera es la serie truncada a orden $\delta^2$ y la segunda a orden $\delta^4$. Según la salida de `02_limite_coulomb.py` (DF con Richardson, $R=60$; la sección 10 no tiene script propio): $E_0(0.3)=-0.25763859$, desviaciones $9.86\times10^{-3}$ y $1.93\times10^{-3}$; la sección 2 ya da las dos cifras. El guion debe decir de qué orden habla |
| A13 | $a_s$ con dos significados (longitud de dispersión y radio de suavizado) | 7.4 y 8.5 | conflicto de notación; propuesta en 0.5 |

## 10.6 Modificaciones de los prompts y motivo

Reconstruidas a partir de lo que consta; los textos literales de la primera ronda no se conservaron.

| Paso | Cambio realizado | Motivo |
|---|---|---|
| 1 | Cada bloque se pidió con su script de verificación (sympy y numérico) y su figura | no aceptar una fórmula o una cifra solo porque la IA la afirma |
| 2 | Cada bloque pasó por dos revisiones con enfoques distintos (matemático; físico y numérico) | buscar tipos de error distintos |
| 3 | Segunda pasada bibliográfica (Crossref, Europe PMC, INSPIRE, arXiv) | Crossref limitó consultas (HTTP 429) y quedaron referencias sin verificar |
| 4 | En la segunda ronda, la auditoría se hizo contra la guía del profesor y la guía de bitácora, no contra el propio texto | las revisiones de la primera ronda solo comprobaban la coherencia interna y no vieron lo que faltaba ni el "enunciado" inexistente |
| 5 | La consulta de límites físicos se formuló como "consulta de derivación": pregunta delimitada, hipótesis explícitas, sin código; la respuesta se guardó antes de verificar | cumplir el requisito del profesor y evitar que la verificación contaminara la lista |
| 6 | Se pidió de forma explícita decir si el peso es real, positivo y normalizable | lo exige el protocolo del profesor para problemas con singularidades |
| 7 | Se pidió que cada cifra saliera de un script ejecutado y que el costo del plan se midiera, no se supusiera | en la primera ronda hubo cifras sin salida de script (K8) |
| 8 | Se prohibió inventar registros y decisiones; donde falte, "pendiente de confirmar por el equipo" | la bitácora de IA debe distinguir lo que hizo la IA de lo que decidió el equipo |

## 10.7 Pendientes para el equipo

1. Autoría: **resuelto** el 13-10-2026. El grupo es de dos, Juan Sebastián Calixto y Luis Felipe Ramírez (confirmado por Lucho; ver R2-11). Los roles de la Fase 1 (Juan Sebastián Calixto, formulación física; Luis Felipe Ramírez, implementación y verificación) y la rotación de 9.12 los confirmó Lucho el 21-10-2026 (decisión 6).
2. Confirmar o corregir cada "decisión humana" pendiente de la tabla 10.2, en especial la acción R1 (sección 8), el criterio de enlace (9.6) y la pregunta y el cierre (0.1 y 0.3). **Resuelto** el 21-10-2026 en lo que cubren las decisiones 1 a 6 (R2-13). Quedan pendientes la aprobación del material de presentación (decisión 7) y la entrada R2-07, que ninguna decisión cubre.
3. Aplicar en el guion, las diapositivas y el PDF de la bitácora lo que falta de K5, K9 y K12 (el texto de las secciones 1 a 6 y de `bitacora_fase1.md` ya está corregido), o registrar por qué no. **Aplicado** el 19-10-2026 (R2-12): el guion y las diapositivas ya no contienen "corregimos el enunciado" ni "todas las referencias quedaron verificadas", y la figura de Calogero corregida está en la lámina 10.
4. Planear para la Fase 3 la auditoría con un modelo distinto (S1).
5. Firmar `decisiones_pendientes.md` (19-10-2026), que reúne en siete decisiones los puntos 1 y 2 y la aprobación del guion y las diapositivas de 15 minutos. Al firmarla se cierra C9 y con él la Fase 1 (R2-12). **Estado al 21-10-2026:** Lucho la rellenó; las decisiones 1 a 6 están aprobadas (la 1, tras la verificación independiente de R2-13) y la 7 sigue pendiente, y con ella C10. Las firmas siguen en blanco.
