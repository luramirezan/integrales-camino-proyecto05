# 17. Registro de prompts e interacción con la IA (bitácora de IA de la Fase 2)

**Proyecto 05, umbral de ligadura en el potencial de Yukawa** · Fase 2 · Bloque 17 · 27 de octubre de 2026

Formato del profesor: "la bitácora mínima conserva fecha, consulta, respuesta utilizada, decisión humana, comprobación y corrección posterior". Formato del grupo: el del registro de la Fase 1 (`fase1/secciones/10_registro_ia.md`): tabla resumen, fichas, correcciones posteriores, supuestos implícitos, anomalías, modificaciones de los prompts y pendientes.

**Reglas de este registro.** (1) Solo se registra lo que consta en la carpeta del proyecto (secciones, salidas, informes V1 a V3, archivos de `fuentes_control/`) o en el encargo que recibió el agente que escribe este registro. (2) Los encargos de los agentes del flujo los escribió un guion de orquestación a partir del pedido de Lucho; no se guardaron como archivos en la carpeta. Aquí se resumen con fidelidad a partir de lo que consta (el contexto común que recibió cada agente y su informe final); donde algo no consta, se dice. (3) Donde no consta una decisión humana se escribe **"pendiente de confirmar por el equipo"**; no se inventa ninguna. (4) Todo el trabajo de la Fase 2 lo ejecutó la IA. Los roles humanos (formulación física y verificación, Juan Sebastián Calixto; implementación, Luis Felipe Ramírez) son los aprobados el 21-10-2026, pero ningún humano revisó todavía lo que hizo la IA en esta fase.

## 17.1 Datos de la sesión y roles

| Campo | Valor |
|---|---|
| Fechas | 26-10-2026 (fuentes de control pedidas por el profesor tras la presentación de la Fase 1; nota sobre una auditora de otra IA). 27-10-2026, de 01:20 a ~03:30 UTC (flujo de agentes de toda la Fase 2) |
| IA | Claude (Anthropic), modelo Claude Opus 5.5 en este agente. Varios agentes (instancias separadas) coordinados por un guion de flujo de trabajo: radial, transferencia, PIGS, controles, cajas, verificación V1, auditoría V2, correcciones V3, presentación y bitácora |
| IA auditora | Claude (otras instancias del mismo modelo: V1 y V2). **No se usó otro modelo** (supuesto S1, 17.4). Se recomienda una auditoría con otra IA según `fase2/fuentes_control/auditor_otra_ia.md` |
| Integrantes | Juan Sebastián Calixto y Luis Felipe Ramírez (grupo de dos desde el 13-10-2026) |
| Roles humanos en la Fase 2 | Formulación física y verificación: Juan Sebastián Calixto. Implementación: Luis Felipe Ramírez (rotación de 9.12, aprobada por Lucho el 21-10-2026, decisión 6 de `fase1/decisiones_pendientes.md`) |
| Quién lo pidió | Luis Felipe Ramírez (Lucho), mensaje del 27-10-2026 a las 01:20 UTC en el hilo del proyecto (ficha F2-03) |
| Quién ejecutó | La IA, de punta a punta. Las decisiones humanas están todas pendientes (`decisiones_fase2.md`) |

## 17.2 Registro de consultas

### Tabla resumen

| ID | Fecha | Consulta (resumen) | Respuesta utilizada | Decisión humana | Comprobación | Corrección posterior |
|---|---|---|---|---|---|---|
| F2-01 | 26-10-2026 | Lucho: "descargar esa base" de fuentes para Hulthén y el pozo cuadrado, que pidió el profesor | `fuentes_control/fuentes_control.md`, `verificacion_hulthen_2s.py`, `descargar_fuentes.ps1` | "Pendiente de revisión por el equipo" (consta en el archivo) | metadatos y resúmenes leídos en APS y arXiv el mismo día; 2s de Hulthén con sympy (residuo 0) | Y1: el 27-10-2026 se vio en arXiv el DOI 10.1063/1.5050621 (sin cambiar su estado) |
| F2-02 | 26-10-2026 | Si es viable usar otra IA (no Claude) como auditora | `fuentes_control/auditor_otra_ia.md` (plantilla de prompt y forma de registrarlo) | pendiente de confirmar por el equipo | n/d (es una propuesta de procedimiento) | n/d |
| F2-03 | 27-10-2026 | Pedido de Lucho: lanzar agentes y flujos para hacer toda la Fase 2, verificando | Plan del flujo: tareas 1 a 10 de `fase1/que_sigue_fase2.md`, dos verificaciones y una respuesta | el pedido mismo es la decisión de abrir la fase; lo demás, pendiente de confirmar por el equipo | n/d | n/d |
| F2-04 | 27-10-2026 | Agente radial: módulo `radial.py`, pruebas y cifras de referencia (tarea 1) | sección 10; `radial.py`, `test_radial.py`, `10_radial_controles.py` | pendiente de confirmar por el equipo | 7/7 pruebas; exactos de Coulomb, Hulthén y pozo; tablas 5.1 y 9.6 de la Fase 1 | V3: criterio δ = 0.2 a 5×10⁻⁹ no pasa frente al exacto (H4 de V1); ruta fija (H9 de V2) |
| F2-05 | 27-10-2026 | Agente transferencia: `pares.py`, `transferencia.py`, controles (tareas 2, 3 y 7) | sección 11 | pendiente de confirmar por el equipo | 5/5 pruebas (7/7 tras V3); 28 de 35 criterios; peso con 0 negativos | V3: Wigner-Kirkwood en U_C (H2 de V2), aviso de pared (H3 de V2), u'(0) (H6 de V1), proyección (H7 de V1) |
| F2-06 | 27-10-2026 | Agente PIGS: `pigs.py`, producción y τ (tareas 4 y parte de 8) | sección 12 | pendiente de confirmar por el equipo | 9/9 pruebas (14/14 tras V3); 10 de 11 criterios; réplica de τ = 5 | V3: Coulomb con 8 cadenas e histograma, segunda réplica, `ValueError` (H5, H7, H8, H12) |
| F2-07 | 27-10-2026 | Agente controles: Hulthén y pozo por la misma transferencia (tarea 5) | sección 13 | "pendiente de revisión por Juan Sebastián" (consta en la sección) | 21 pasan, 0 fallan, 5 medidos (22/1/5 tras V3) | V3: mallas del pozo con h = 0.005 (H2 de V1); errata −1.53e−6 (H11 de V2) |
| F2-08 | 27-10-2026 | Agente cajas: condición (c) de 9.6 con la transferencia | sección 14 | pendiente de confirmar por el equipo (umbral 0.1 de la ley de caja) | 90 autovalores; Perron en los 90; 15/15 celdas compatibles | V3: lista de celdas fuera de su error corregida (5 → 11 de 15; H1 de V1 y V2); término de pared en el error |
| F2-09 | 27-10-2026 | Verificación V1: recálculo independiente con código propio | `verificacion/V1_recalculo_independiente.md` | pendiente de confirmar por el equipo | 252 cifras: 227 coinciden, 25 no (explicadas); 7 hallazgos | V3 los reprodujo todos |
| F2-10 | 27-10-2026 | Auditoría V2: adversarial (reproducibilidad, casos raros, honestidad del error, entregables) | `verificacion/V2_auditoria_adversarial.md` | pendiente de confirmar por el equipo | reejecución de pruebas y scripts; Monte Carlo con 24 cadenas nuevas | V3 reprodujo 12 de 13; H10 rechazado |
| F2-11 | 27-10-2026 | Correcciones V3: responder a los 20 hallazgos recalculando | `verificacion/V3_respuesta_hallazgos.md`; scripts 12c, 15 y 16_tabla; tabla 15 | pendiente de confirmar por el equipo (tabla 15 sin firmar) | reejecución de 10 a 15 y de las tres pruebas | n/d |
| F2-12 | 27-10-2026 | Agente de presentación (constatado solo por sus archivos) | `codigo/18_figura_presentacion.py`, `figuras/18_primer_grafico.png`, `presentacion/diapositivas_fase2.pptx` y `.pdf`, `presentacion/guion_fase2.md` | pendiente de confirmar por el equipo | no comprobado por este registro | n/d |
| F2-13 | 27-10-2026 | Este agente: primer gráfico congelado, bitácora, registro de IA, qué sigue y hoja de decisiones | `16_primer_grafico.py`, `bitacora_fase2.md` y `.pdf`, este archivo, `que_sigue_fase3.md`, `decisiones_fase2.md` | pendiente de confirmar por el equipo | cifras leídas de los JSON y de una ejecución del script 16 (dos veces: misma huella) | ver 17.3, C14 a C16 |
| F2-14 | 27-10-2026 | Revisor final de coherencia: cotejar cifras de bitácora, guion, diapositivas y tabla 15 con los JSON; volver a ejecutar las pruebas; lista de revisión; estado de las citas; PDF; `LEEME.md` | correcciones en las secciones 11 a 15 y 17 y en la bitácora (17.3, C17 a C22); `fase2/LEEME.md`; PDF regenerado | pendiente de confirmar por el equipo | cotejo automático de unas 2700 cifras contra los JSON actuales y los de `archivo_pre_V3/`; tabla 15 regenerada en una copia (idéntica); pruebas 7/7, 7/7, 14/14 | n/d |

### Fichas

**F2-01. Fuentes para los potenciales de control (26-10-2026).**
- *Consulta:* de Lucho: "descargar esa base" de fuentes para Hulthén y el pozo esférico cuadrado que pidió el profesor después de la presentación de la Fase 1. Es lo que consta en el registro del propio archivo; el texto completo del pedido no está en la carpeta.
- *Respuesta utilizada:* la tabla de 10 referencias de Hulthén (H1 a H10), 4 del pozo (P1 a P4), 3 de técnicas (PI1 a PI3) y Y1, con estado VERIFICADA / CITA SECUNDARIA / NO VERIFICADA; la comprobación simbólica del 2s de Hulthén ($A=(1+\delta)/(\delta-1)$, $\delta_c(ns)=2/n^2$); un script para bajar los PDF de arXiv.
- *Decisión humana:* "pendiente de revisión por el equipo" (registro del archivo).
- *Comprobación:* metadatos y resúmenes leídos en APS o arXiv el 26-10-2026; no se pudo bajar ningún PDF (el proxy bloqueó arXiv y Crossref).
- *Corrección posterior:* el 27-10-2026 este agente abrió la página de resumen de arXiv de Y1 (1807.11898) con la herramienta de consulta web: confirma título y autores, y la página lista el DOI 10.1063/1.5050621 sin nombrar la revista; el resumen no da el valor de $\delta_c$. **No se cambió el estado** de Y1 (revista NO confirmada; $\delta_c$ no leído).

**F2-02. Auditora de otra IA (26-10-2026).**
- *Consulta:* texto literal no conservado. Por la respuesta ("Respuesta corta: sí es viable y es buena idea"), se preguntó si se podía usar otra IA como auditora.
- *Respuesta utilizada:* `auditor_otra_ia.md`: elegir una IA que ejecute código, darle bloques cerrados sin decirle el resultado esperado, plantilla de prompt, guardar prompt y respuesta literales, resolver desacuerdos calculando, ficha A-01.
- *Decisión humana:* pendiente de confirmar por el equipo. **No se hizo todavía ninguna auditoría con otro modelo.**

**F2-03. Pedido de la Fase 2 completa (27-10-2026, 01:20 UTC).**
- *Consulta (literal, con su ortografía):* "Podrias lanzar agentes y wprkflows ára hacer toda la fase 2 completa verificando mejor dicho haciendo todo?" (Lucho, en el hilo del proyecto "Investigacion Torica"). Leído: "¿Podrías lanzar agentes y workflows para hacer toda la Fase 2 completa, verificando; mejor dicho, haciendo todo?".
- *Respuesta utilizada:* un flujo de agentes con un **contexto común** para todos: método aprobado sin cambios (acción de pares de Coulomb tabulada con $h_{\rm tab}=0.01$ y $0.005$ y Richardson, resto $W\in[0,\delta]$, prohibida la acción primitiva, suavizado solo como control), dos evaluaciones (transferencia en banda y PIGS desde $u_T=re^{-r}$), referencia radial, punto $\delta=0.2$ y control $\delta=0$, semillas $20262000+k$, scripts numerados desde 10 que imprimen sus cifras y guardan JSON y figuras, módulos con nombres fijos, máximo 4 procesos, "cada cifra que reportes debe salir de un script ejecutado" y "si algo falla o no cumple un criterio, dilo tal cual; no lo maquilles". Encargos: F2-04 a F2-13.
- *Decisión humana:* el pedido es la decisión de abrir la fase y delegar la ejecución. Sobre los resultados: pendiente de confirmar por el equipo.

**F2-04. Agente radial (tarea 1).**
- *Consulta (resumen del encargo):* convertir el método A de la sección 5 de la Fase 1 en un módulo `radial.py` para cualquier $V(r)$, con Richardson y observables $E_0$, $E_1$, $\langle r\rangle$, $\langle r^2\rangle$, $F_{1/2}$, $\langle r\rangle/R$; pruebas con Coulomb y la tabla 5.1; cifras de referencia de $\delta=0.2$, Hulthén, pozo y cajas.
- *Respuesta utilizada:* sección 10; `radial.py`, `test_radial.py` (7/7), `10_radial_controles.py`, `10_radial.json`.
- *Decisión humana:* pendiente de confirmar por el equipo.
- *Comprobación:* Coulomb a $6.1\times10^{-9}$; $\delta_c=1.1906124210606$ (a $3.9\times10^{-11}$ de la Fase 1); Hulthén exacto a $6\times10^{-9}$; orden 2 medido (1 en el pozo con $V(a)=0$).
- *Errores propios corregidos (del informe del agente):* Richardson $p=2$ con el pozo de orden 1 (corregido con el salto en un nodo con valor medio); caja $R=80$ demasiado chica para el pozo en $V_0=1.3$; aviso de raíz de un número negativo en `r_rms`; tolerancia de Hulthén en $\langle r^2\rangle$ **fijada después de ver el resultado** (de $10^{-6}$ absoluto, que fallaba por $2.0\times10^{-6}$, a $2\times10^{-7}$ relativo), declarada en 10.3; errata de la tabla 9.6 de la Fase 1 encontrada (no corregida en `fase1/`).
- *Corrección posterior:* V3 (H4 de V1): el criterio de $\delta=0.2$ a $5\times10^{-9}$ solo pasaba frente a la referencia redondeada; frente al exacto falla ($6.2\times10^{-9}$) y se dejó como "no pasa". H9 de V2: ruta absoluta fija cambiada a relativa.

**F2-05. Agente transferencia (tareas 2, 3 y 7).**
- *Consulta (resumen):* módulos `pares.py` (tabla $U_C$ con caché) y `transferencia.py` (matriz en banda para un resto $W$ acotado cualquiera); controles 9.7 en $\delta=0$, 0.2 y 1.0; ley $\epsilon^2$; proyección; declaración del peso.
- *Respuesta utilizada:* sección 11 y sus scripts.
- *Decisión humana:* pendiente de confirmar por el equipo (redefinición del control de tabulación, 11.4; tratamiento del pozo, 11.7).
- *Comprobación:* Coulomb a $\le2.2\times10^{-7}$; $\delta=0.2$ extrapolado a $4.4\times10^{-9}$; peso con 0 elementos negativos y 0 no finitos; 28 de 35 criterios, los 7 que fallan con causa medida (error $h^4/\epsilon$ de la cúspide).
- *Errores propios corregidos:* signo del desplazamiento espectral en la primera `pares.py` ($U(9,9)=+0.0939$ frente a $-0.0111$ de la Fase 1); NaN en la banda con $\epsilon=0.05$; el spline de FITPACK no extrapolaba bajo el primer nodo (error $9.8\times10^{-3}$, luego $1.7\times10^{-4}$); un `assert` demasiado amplio.
- *Corrección posterior (V3):* el docstring decía error $<10^{-7}$ en $r\ge10$ y era $\epsilon^2/(6r^3)$ ($1.7\times10^{-6}$): se añadió el término de Wigner-Kirkwood. $u'(0)^2$ sesgado un 1.25 % (3.9502 en vez de 4). El residuo de $1.05\times10^{-7}$ del mixto era error de malla de $E_0(T)$, no del estimador.

**F2-06. Agente PIGS (tarea 4 y parte de la 8).**
- *Consulta (resumen):* `pigs.py` con la acción aprobada, estimadores mixto ($E$) y puro ($\langle r\rangle$, $\langle r^2\rangle$), errores por bloques y entre cadenas, producción en $\delta=0$ y 0.2, dependencia con $\tau$, sesgo de la interpolación.
- *Respuesta utilizada:* sección 12 y sus scripts.
- *Decisión humana:* pendiente de confirmar por el equipo (anomalía de $\tau=5$).
- *Comprobación:* $\delta=0.2$ a $+1.22\sigma$, $+0.56\sigma$, $+0.43\sigma$; repesado bilineal/bicúbico; réplica de $\tau=5$.
- *Errores propios corregidos:* un criterio inventado ("proyección visible en PIGS") que no se podía cumplir; se pasó a informativo **antes** de la producción. Probabilidad del $-3.19\sigma$ recalculada con scipy (0.14 % y 1.7 %, no 0.3 % y 3 %).
- *Corrección posterior (V3):* el control $E_L\equiv-0.5$ de Coulomb es tautológico (H7 de V2); se añadieron 8 cadenas e histograma ($p=0.004$); segunda réplica de $\tau=5$; $M$ ya no se trunca en silencio.

**F2-07. Agente controles (tarea 5).**
- *Consulta (resumen):* pasar Hulthén y el pozo cuadrado por la **misma** transferencia y por el radial, con criterios fijados antes de ejecutar, citando las fuentes con su estado sin cambiarlo.
- *Respuesta utilizada:* sección 13.
- *Decisión humana:* "pendiente de revisión por Juan Sebastián" (consta en la sección).
- *Comprobación:* Hulthén extrapolado a $\le5\times10^{-9}$ del exacto; orden de Trotter 1.99; pozo con orden medido $\approx1.5$.
- *Errores propios corregidos:* nombre de clave con puntos que rompía el script; Lanczos demasiado lento en $R=385$ (cambiado a desplazamiento-inversión y comprobado); $\langle r\rangle$ del pozo sin extrapolar.
- *Corrección posterior (V3):* el valor $h\to0$ del pozo no estaba convergido (H2 de V1); con $h=0.005$ B3 pasa de $+6.2\times10^{-6}$ a $+3.5\times10^{-6}$ y el nuevo B3b falla en $V_0=1.3$.

**F2-08. Agente cajas (condición (c) de 9.6).**
- *Consulta (resumen):* calcular con la transferencia $E_0$, $\langle r\rangle/R$ y $F_{1/2}$ en $\delta\in\{1.15,1.18,1.20\}$ y $R\in\{50,\dots,800\}$, comparar celda a celda con el radial y aplicar el criterio completo.
- *Respuesta utilizada:* sección 14.
- *Decisión humana:* pendiente de confirmar por el equipo (umbral 0.1 de la ley de caja, que fijó la IA).
- *Comprobación:* 90 autovalores con Perron-Frobenius; mismos veredictos que el radial en las 9 ternas.
- *Errores propios corregidos:* `which='LA'` sin desplazamiento no terminaba; hipótesis de la pared sin imagen formulada y comprobada contra el radial en $R+0.5826\sqrt\epsilon$; tiempos por autovalor corregidos a los de la ejecución final.
- *Corrección posterior (V3):* el texto decía que la transferencia salía de su error solo en 5 celdas; eran 11 de 15 (H1 de V1 y V2). Corregido y añadido el término de pared al error (15/15).

**F2-09. Verificación V1 (recálculo independiente).**
- *Consulta (resumen):* recalcular las cifras de las secciones 10 a 14 sin importar código del proyecto, con métodos distintos.
- *Respuesta utilizada:* el informe y `verificacion/codigo_independiente/` (disparo DOP853, FEDVR, operador de Trotter continuo, Nyström con núcleo propio, reanálisis de las series).
- *Decisión humana:* pendiente de confirmar por el equipo.
- *Comprobación:* 252 cifras, 227 coinciden; las 25 discrepancias se explican y ninguna cambia veredictos ni $\delta_c$. Siete hallazgos (H1 a H7).
- *Limitación:* es otra instancia de Claude (S1).

**F2-10. Auditoría V2 (adversarial).**
- *Consulta (resumen):* buscar lo que el proyecto no vio: reproducibilidad, casos raros del peso, honestidad del error del Monte Carlo, entregables que faltan.
- *Respuesta utilizada:* el informe y `verificacion/V2_auditoria/`. Trece hallazgos (H1 a H13).
- *Decisión humana:* pendiente de confirmar por el equipo.
- *Comprobación:* reejecución de pruebas y scripts (diferencias $\le4.3\times10^{-7}$ relativo); 24 cadenas nuevas (semillas 20269000+k).
- *Corrección posterior:* H10 (JSON guardado como texto) no se reprodujo en V3 y se rechazó.

**F2-11. Correcciones V3.**
- *Consulta (resumen):* reproducir cada hallazgo de V1 y V2 con un cálculo propio antes de tocar nada; corregir lo real sin cambiar tolerancias; reejecutar; tabla de controles consolidada sin firmar.
- *Respuesta utilizada:* `V3_respuesta_hallazgos.md`; 19 de 20 hallazgos reproducidos; scripts nuevos 12c, 15 y 16_tabla; sección 15 (88 filas: 70 pasan, 9 no, 9 medidas).
- *Decisión humana:* pendiente de confirmar por el equipo (firma de Juan Sebastián).
- *Errores propios corregidos:* estimación del sesgo de pared 250 veces de más en su primera versión; prueba de potencia del histograma **cambiada después de ver el resultado** (declarado); L14 tomaba $E_2$ en lugar de $E_1$; criterio L16 mal planteado (se dejó como "no pasa"); dos errores de programación en 16_tabla; LU sin memoria (Cholesky en banda).

**F2-12. Agente de presentación.**
- *Consulta:* no consta en la carpeta ni en el encargo de este agente. Solo constan sus archivos: `18_figura_presentacion.py` (lee los JSON de 10 a 12c y dibuja E, ⟨r⟩ y E_mixto(τ) en δ = 0.2) y `18_primer_grafico.png`, escritos a las 03:08 UTC; y en `presentacion/` las diapositivas, su PDF, el guion y el script que las genera, escritos a las 03:16 UTC.
- *Decisión humana:* pendiente de confirmar por el equipo; la decisión 8 de `decisiones_fase2.md` pide elegir una sola figura para la exposición.

**F2-13. Este agente: primer gráfico, bitácora y hojas de cierre.**
- *Consulta (resumen fiel del encargo):* escribir el script `16_primer_grafico.py` con la figura congelada de la primera exposición ($\delta=0.2$: radial frente a transferencia y PIGS con barras de error en $E$, $\langle r\rangle$, $\langle r^2\rangle$, y $E_{\rm mixto}(\tau)$ determinista y PIGS), anotar el sha256 de cada figura y su script; escribir la bitácora de la Fase 2 según `enunciado/guia_bitacora.md` y el estilo de la Fase 1, con fuentes marcadas exactamente como constan, este registro de IA, `que_sigue_fase3.md`, `decisiones_fase2.md` y el PDF de la bitácora (pandoc y Chromium de Playwright), revisando las páginas renderizadas.
- *Respuesta utilizada:* esos archivos.
- *Decisión humana:* pendiente de confirmar por el equipo.
- *Comprobación:* el script 16 no calcula nada nuevo: lee los JSON; se ejecutó dos veces con la misma huella de la figura; cifras impresas en `verificacion/16_primer_grafico_salida.txt`. Las cifras de la bitácora salen de esa salida, de los JSON y de las secciones 10 a 15 (que remiten a sus scripts).
- *Errores propios corregidos:* ver 17.3 (C14 a C16).

**F2-14. Revisor final de coherencia (27-10-2026).**
- *Consulta (resumen fiel del encargo):* cotejar cada cifra de `bitacora_fase2.md`, `presentacion/guion_fase2.md`, el texto de `presentacion/diapositivas_fase2.pptx` y `secciones/15_tabla_controles.md` con `resultados/*.json` y corregir los documentos (no los JSON); volver a ejecutar todas las pruebas; recorrer la lista de revisión final de la guía y la evidencia de la Fase 2; comprobar que cada cita tiene su estado; regenerar el PDF si cambia la bitácora; escribir `fase2/LEEME.md`.
- *Respuesta utilizada:* un cotejo automático (cada cifra de 3 o más cifras significativas debe coincidir, al redondeo impreso, con algún número de los JSON actuales; las que solo coinciden con los JSON de antes de V3 se marcan como viejas) y revisión a mano de las que no coincidían. Se encontraron cifras de antes de V3 en las secciones 11 ($\delta=1.0$), 12 (valores deterministas a 10 cifras y tiempos) y 14 (tabla de la pared y órdenes de Nyström), y un doble redondeo en el pozo ($+3.55\times10^{-6}$ escrito como $+3.6\times10^{-6}$). Las correcciones están en 17.3 (C17 a C22).
- *Decisión humana:* pendiente de confirmar por el equipo.
- *Comprobación:* la tabla 15 regenerada en una copia con `16_tabla_controles.py` sale idéntica (solo añadiría dos filas de figuras, 16 y 18); el guion y las diapositivas no tienen ninguna cifra que no salga de los JSON; pruebas 7/7, 7/7 y 14/14 en la reejecución.
- *Errores propios corregidos:* el primer cotejo no leía los exponentes en superíndice (×10⁻⁴) y daba falsos avisos; se corrigió el lector antes de usar sus resultados.

## 17.3 Correcciones posteriores (qué se afirmó, por qué estaba mal, cómo se corrigió)

| # | Afirmación | Por qué estaba mal | Corrección | Dónde |
|---|---|---|---|---|
| C1 | "error < 1e-7 en r ≥ 10" de la aproximación de extremos | el error es $\epsilon^2/(6r^3)$, $1.7\times10^{-6}$ en $r=10$ | término de Wigner-Kirkwood; $8\times10^{-9}$ | V2 H2, V1 H3; 11.1 |
| C2 | La transferencia sale de su error solo en 5 celdas de cajas | con los números del JSON eran 11 de 15 | texto corregido; término de pared en el error (15/15) | V1 H1, V2 H1; 14.4 |
| C3 | El criterio radial $\delta=0.2$ a $5\times10^{-9}$ pasa | solo frente a la referencia redondeada a 8 cifras | se reporta "no pasa" ($6.2\times10^{-9}$); $h=1/80,1/160$ pasa | V1 H4; 10.7 |
| C4 | $B3$ del pozo: $+6.2\times10^{-6}$, con $h\to0$ convergido | la extrapolación en $h$ (orden ~1) no estaba convergida | mallas hasta $h=0.005$: $+3.5\times10^{-6}$; B3b no pasa en $V_0=1.3$ | V1 H2; 13.3 |
| C5 | La réplica de $\tau=5$ cierra la anomalía | producción y réplica difieren $2.4\sigma$ | segunda réplica; χ² de las tres $p=0.011$; anomalía abierta | V1 H5, V2 H6; 12.V3 |
| C6 | $u'(0)^2=3.9502$ en Coulomb | sesgo $(1-r_1)^2$ | $u'(0)=\lim u/r$: 3.99992 | V1 H6; 11.4 |
| C7 | El límite del mixto difiere $1.05\times10^{-7}$ de $E_0(T)$ (propiedad del estimador) | es error de malla de $E_0(T)$ | con Richardson en $h$: $-1.3\times10^{-9}$ | V1 H7; 11.5 |
| C8 | $E_L\equiv-0.5$ prueba el muestreo de Coulomb | tautológico: con $W=0$ vale para cualquier camino | Coulomb con 8 cadenas e histograma | V2 H7; 12.V3 |
| C9 | (código) $M$ se trunca a múltiplo de $L$ y se guarda el $\tau$ pedido | podía dar un $\tau$ falso | `ValueError` y `tau_ef` | V2 H8 |
| C10 | (código) ruta fija en el script 10 | sobrescribió resultados al reejecutar desde una copia | ruta relativa | V2 H9 |
| C11 | $-1.53\times10^{-6}$ en la tabla de Hulthén | el JSON daba $-1.5249\times10^{-6}$ | $-1.52\times10^{-6}$ | V2 H11 |
| C12 | Los límites L04 a L09 se cumplen (sin comprobarlos con la integral de camino) | no había script | `15_limites.py`: pasan (L16 mal planteado, no pasa) | V2 H5 |
| C13 | Error del radial en $\langle r\rangle/R$ y $F_{1/2}$ igual a 0 | faltaba el error de malla | $|X_{\rm Rich}-X_{1/80}|$ | V2 H13 |
| C14 | (este agente) primera versión de la figura 16 | leyendas encima de barras de error y de la línea radial; diferencias de la transferencia invisibles en (a) sin aviso | leyendas y escalas recolocadas; nota con el tamaño de las diferencias; figura revisada como imagen | `16_primer_grafico.py` |
| C15 | (este agente) línea que leía una clave inexistente (`juntas`) del JSON de la réplica | error de programación, sin efecto en la salida | quitada antes de congelar | `16_primer_grafico.py` |
| C16 | (este agente) mapa figura → script sin la figura 18 | otro agente creó `18_primer_grafico.png` durante esta tarea | añadida con su script `18_figura_presentacion.py` | `16_primer_grafico.json` |
| C17 | Tabla de Trotter en $\delta=1.0$ (sección 11.3): $E=-0.0103195580$, $-0.0102943089$, $-0.0102878904$ | eran las cifras de antes de V3; el JSON actual (con Wigner-Kirkwood) da otras | $-0.0103194084$, $-0.0102942585$, $-0.0102878731$ y sus diferencias; nota de que suben $+1.5\times10^{-7}$, $+5.0\times10^{-8}$, $+1.7\times10^{-8}$ | revisión final; `11_transferencia.json` |
| C18 | Sección 12.2: $\langle r\rangle$, $\langle r^2\rangle$ deterministas a 10 cifras ($1.5497354681$, $3.2259787933$, $1.5485514376$, $3.2195166547$) y tiempos (11.9 min; 1.66 y 2.80 ms por barrido) | de la primera ejecución; el JSON es de la reejecución de V3 | $1.5497354673$, $3.2259787857$, $1.5485514370$, $3.2195166492$; 9.3 min y 1.46/2.00 ms (con los de la primera ejecución al lado) | revisión final; `12_pigs.json` |
| C19 | Sección 14.4: tabla de la pared corrida (órdenes 1.832/1.976, …) y "baja de 10 a 40 veces" | de antes de V3 | órdenes 1.837/1.985, 1.647/1.984, 1.919/1.991, 1.491/1.984, 1.787/1.991, 1.915/2.003; "de 12 a 16 veces"; residuo $0.8$–$2.1\times10^{-7}$ ($\le4.6\times10^{-4}$ de $|E_0|$) | revisión final; `14_cajas.json` (pared, celdas) |
| C20 | Orden Nyström cerca del umbral: 1.360 y 2.281 (y "1.36 y 2.28") | de antes de V3 | 1.361 y 2.287 ("1.36 y 2.29"), también en la tabla 15 y en su script | revisión final; `14_cajas.json` (orden_nystrom) |
| C21 | Pozo $V_0=2$, B3: $+3.6\times10^{-6}$ | doble redondeo de $+3.5486\times10^{-6}$ ($\to3.55\to3.6$) | $+3.5\times10^{-6}$ en las secciones 13, 17 y la bitácora (la presentación ya decía 3.5) | revisión final; `13_controles.json` |
| C22 | Citas sin estado: Broadie, Glasserman y Kou (en el texto de 14.4) y la ventana de Sokal (12.1) | faltaba el estado junto a la cita | marcadas NO VERIFICADA; Sokal añadido a XI.3 | revisión final |

## 17.4 Supuestos implícitos de la IA y de las fuentes

| # | Supuesto | De quién | Cómo se comprobó | Estado |
|---|---|---|---|---|
| S1 | Que V1 y V2 son verificaciones independientes | flujo de la Fase 2 | son otras instancias de Claude: comparten sesgos de entrenamiento. Usaron código propio (V1 sin importar nada del proyecto), lo que da independencia de **código**, no de **modelo** | abierto: auditoría con otra IA (`auditor_otra_ia.md`) en la Fase 3, que la guía pide para autovalores cercanos a cero |
| S2 | Que la malla Nyström es de orden alto | sección 11 (plan de 9.7) | medido: $h^4$ en $\delta\le1$ por la cúspide; 1.36 y 2.29 cerca del umbral; $h^1$ con el salto del pozo | falso en general; declarado |
| S3 | Que la ley de Trotter es $\epsilon^2$ siempre | plan 9.7, L18 | sí con resto suave (Yukawa, Hulthén); $\epsilon^{3/2}$ con el salto del pozo; se rebaja con la pared sin imagen | precisado; decisión 4 |
| S4 | Que la pared en $R$ la impone $K_D$ | sección 11 | solo en los nodos de tiempo: pared efectiva $R+0.5826\sqrt\epsilon$ | falso; decisión 5 |
| S5 | Que la aproximación de extremos vale $<10^{-7}$ fuera de $r=10$ | docstring de `pares.py` | V2: $\epsilon^2V''/12$ | falso; C1 |
| S6 | Que el error del Monte Carlo está bien estimado | sección 12 | V2 (24 cadenas, χ² 22.9/23) y V3 (40 cadenas, χ² 50.2/39) | razonable; dispersión entre corridas de $\tau=5$ con $p=0.011$ |
| S7 | Que el orden 3/2 del pozo viene de una capa $\sqrt\epsilon$ en el salto | sección 13 | no demostrado; sin fuente | plausible, no verificado |
| S8 | Que $\beta=0.5826$ (corrección de Broadie, Glasserman y Kou) se aplica aquí | sección 14 | medido contra el radial (orden vuelve a 1.97–1.99); la fuente **no se consultó** | dato de memoria de la IA; fuente NO VERIFICADA |
| S9 | Que $u_T=re^{-r}$ basta como función de prueba no exacta | plan 9.4 | cumple la cúspide; cola equivocada para $\delta>0$; mixto converge en $\tau=20$ a $2.6\times10^{-7}$ | cierto en $\delta=0.2$ |
| S10 | Que la tabla $U_C$ es independiente del radial | 9.10 de la Fase 1 | no: dentro de $r\le10$ usa la misma discretización por diferencias finitas (circularidad). Hulthén exacto y V1 (núcleo propio, FEDVR) rompen la circularidad | declarado |
| S11 | Que las fuentes de control dicen lo que su resumen dice | F2-01 | se leyeron resúmenes o lecturas automáticas del PDF, no los artículos completos | abierto; "antes de citar un número, verificarlo en el PDF" |
| S12 | Que una figura con huella sha256 queda congelada | este agente | regenerarla con el mismo script en este contenedor dio la misma huella dos veces; pero el archivo cambió de bytes (no de píxeles) cuando otro proceso volvió a ejecutar el script | **falso a nivel de bytes**: para la figura 16 se anota también la huella de los píxeles (XIV.2) |

## 17.5 Anomalías y discrepancias

| # | Anomalía | Dónde | Explicación o estado |
|---|---|---|---|
| B1 | Estabilidad Nyström 0.02→0.04 falla ($1.5$–$3.2\times10^{-6}$) | 11.4 | error $h^4/\epsilon$ de la cúspide; V1 lo reproduce con núcleo exacto |
| B2 | Orden de Trotter 1.05 en $\delta=0.2$ sin Richardson en $h$ | 11.4 | el sesgo de Trotter es del tamaño del error de Nyström |
| B3 | E(τ = 5) del PIGS a $-3.19\sigma$ | 12.4 | réplicas $+0.03\sigma$ y $+0.99\sigma$; corridas en desacuerdo $p=0.011$; abierta |
| B4 | Histograma de Coulomb con $p=0.004$ | 12.V3 | pasa el umbral $10^{-3}$ por poco |
| B5 | Orden 1.38 de Hulthén en $\delta=0.2$ | 13.2 | residuo de tabla; V1 da 1.99 con el operador continuo |
| B6 | Pozo: orden $\epsilon^{3/2}$ y Nyström $O(h)$ | 13.3 | medido; sin fuente |
| B7 | Bordes medio y estricto del pozo aún difieren $2$–$3\times10^{-5}$ y $\sim10^{-4}$ | 13.3 | no está probado que tengan el mismo límite con estas mallas |
| B8 | Orden de Trotter 1.49–1.84 en $R=50$, 100 | 14.4 | pared sin imagen |
| B9 | Orden Nyström 1.36 y 2.29 en $\delta=1.18$ | 14.4 | no explicado; para la Fase 4, $h=0.02$ y 0.01 |
| B10 | Residuo de volumen $-8\times10^{-9}$ en $\delta=1.15$, $R\ge200$ | 14.4 | origen no identificado (del orden del residuo del radial) |
| B11 | Errata de la tabla 9.6 de la Fase 1: $E_0(1.18,400)$ | 10.3 | $-3.07\times10^{-5}$, no $-3.08\times10^{-5}$; confirmada por V1; `fase1/` no se tocó |
| B12 | La transferencia en cajas chicas ($R=2$) da $-0.0376$ frente a $+0.0589$ del radial | V2 H3 | pared sin imagen; ahora el código avisa |
| B13 | Dos figuras de "primer gráfico" (16 y 18) | este registro | dos agentes del mismo flujo; el equipo elige (decisión 8) |

## 17.6 Modificaciones de los prompts y motivo

| Paso | Cambio respecto a la Fase 1 | Motivo |
|---|---|---|
| 1 | Un contexto común idéntico para todos los agentes, con método, parámetros, estilo y reglas | evitar que cada agente reinterprete el método aprobado |
| 2 | "Cada cifra debe salir de un script ejecutado, nunca de memoria" y "si algo no cumple, dilo tal cual" | en la Fase 1 hubo cifras sin salida de script (K8) |
| 3 | Criterios de aceptación fijados **antes** de ejecutar (los agentes de controles y V3 lo hicieron explícito) | evitar ajustar tolerancias a los resultados; las dos excepciones se declaran |
| 4 | Dos verificaciones con enfoques distintos: V1 recálculo con código propio; V2 auditoría adversarial | en la Fase 1 las revisiones solo comprobaban coherencia interna |
| 5 | Una respuesta V3 que reproduce cada hallazgo antes de aceptarlo, con copia previa en `archivo_pre_V3/` | no aceptar un hallazgo solo porque la IA auditora lo afirma |
| 6 | Pedido de un campo `registro_ia` (errores propios) en el informe de cada agente | alimentar este registro |
| 7 | **Falta todavía:** guardar los prompts literales de cada agente en la carpeta | recomendación de `auditor_otra_ia.md`; hoy solo hay resúmenes |

## 17.7 Pendientes para el equipo

1. Firmar `decisiones_fase2.md` (10 decisiones) y la tabla de controles (sección 15). Hasta entonces, toda "decisión humana" de este registro sigue pendiente.
2. Auditoría con otra IA (S1), siguiendo `fuentes_control/auditor_otra_ia.md`, en la Fase 3.
3. Primera presentación (semana 7, 9 + 5 min): al empezar este registro `fase2/presentacion/` estaba vacía; otro agente del mismo flujo dejó a las 03:16 UTC un borrador (`diapositivas_fase2.pptx` y `.pdf`, `guion_fase2.md`); este registro no lo revisó y el equipo no lo ha aprobado.
4. Guardar desde ahora los prompts literales en la carpeta.
5. Revisar la tabla de fuentes de control (F2-01).
