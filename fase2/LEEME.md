# LEEME: Fase 2 del proyecto 05 (umbral de ligadura en el potencial de Yukawa)

Juan Sebastián Calixto y Luis Felipe Ramírez · 27 de octubre de 2026 · Unidades $\hbar=m=g=1$, $V=-e^{-\delta r}/r$, $\delta_c=1.1906124211$ (Fase 1).

Todo lo de esta carpeta lo hizo la IA (Claude) en un flujo de agentes el 27-10-2026. Ningún integrante lo ha revisado todavía. Las decisiones están **pendientes de confirmar por el equipo** (`decisiones_fase2.md`) y la tabla de controles está **sin firmar**.

## Resumen de resultados (10 líneas)

1. **Radial (referencia):** $E_0(\delta=0.2)=-0.3268085110$, $\langle r\rangle=1.54972190$, $\langle r^2\rangle=3.22593944$; $\delta_c=1.1906124210606$, a $4\times10^{-11}$ de la Fase 1.
2. **Peso:** real, positivo y normalizable. La matriz tiene 0 elementos negativos y 0 no finitos, y $U_C(0.01,0.01)=-0.788$ con $\epsilon=0.1$. La acción primitiva daría $e^{10}$.
3. **Transferencia en $\delta=0.2$:** $E-E_{\rm rad}=-4.5\times10^{-7}$, $-1.1\times10^{-7}$ y $-2.5\times10^{-8}$ con $\epsilon=0.2$, 0.1 y 0.05. Extrapolada queda a $+4.4\times10^{-9}$, con orden de Trotter 1.958 (Richardson en $h$).
4. **PIGS en $\delta=0.2$** ($\tau=20$, 8 cadenas): $E=-0.326725\pm0.000068$ ($+1.22\sigma$), $\langle r\rangle=1.55374\pm0.00711$ ($+0.56\sigma$), $\langle r^2\rangle=3.24260\pm0.03894$ ($+0.43\sigma$).
5. **Proyección desde $u_T=re^{-r}$ (no exacta):** $E_{\rm mixto}(\tau)$ baja monótona, y de $\tau=20$ a 30 cambia $2.5\times10^{-7}$. En $\tau=5$ el PIGS queda a $-3.19\sigma$; las réplicas dan $+0.03\sigma$ y $+0.99\sigma$, y las tres corridas solo concuerdan con $p=0.011$. Sigue abierta.
6. **Controles exactos:** Coulomb $|E+0.5|\le2.2\times10^{-7}$. Hulthén extrapolado a $\le5.1\times10^{-9}$ del exacto, con orden 1.99. Pozo cuadrado con Trotter $\epsilon^{3/2}$ (medido) y extrapolado a $+3.5\times10^{-6}$ ($V_0=2$).
7. **Cajas cerca del umbral (condición (c) de 9.6):** $\delta=1.15$ ligado, $\delta=1.18$ ligado y $\delta=1.20$ no ligado, por los dos métodos; (c) se cumple en 9 de 9 ternas. Por tanto $\delta_c\in[1.18,1.20]$.
8. **Errores descubiertos y medidos:**
   - malla Nyström de orden $h^4/\epsilon$ por la cúspide;
   - pared en $R$ sin imagen (la caja efectiva es $R+0.5826\sqrt\epsilon$);
   - aproximación de extremos de $U_C$ más allá de $r=10$, ya corregida con Wigner-Kirkwood.
9. **Tabla de controles:** 88 filas, de las que 70 pasan, 9 no pasan (cada una con su causa medida) y 9 son medidas.
10. **Pruebas:** `test_radial` 7/7, `test_transferencia` 7/7 y `test_pigs` 14/14 (vueltas a ejecutar en la revisión final). **Pendiente:** la firma de Juan Sebastián, las 10 decisiones y el ensayo y aprobación de la presentación.

## Índice de archivos

### Documentos (empezar por aquí)

| Archivo | Qué es |
|---|---|
| `bitacora_fase2.md` / `.pdf` | Bitácora completa de la Fase 2 según `enunciado/guia_bitacora.md`: objetivo, régimen y criterio de cierre (K1–K8), hipótesis, genealogía, controles, desarrollo, límites, recálculo V1, auditoría V2, respuesta V3, fuentes con su estado, registro de IA, cierre y anexos A–F (las secciones 10 a 15 completas). El PDF se regeneró en la revisión final (52 páginas). |
| `decisiones_fase2.md` | Las 10 decisiones que el equipo tiene que firmar. |
| `que_sigue_fase3.md` | Tareas propuestas para la Fase 3, con los roles invertidos. |
| `LEEME.md` | Este archivo. |
| `secciones/10_solucionador_radial.md` | Solucionador radial: método, pruebas, orden medido y cifras de referencia. |
| `secciones/11_accion_pares_transferencia.md` | Acción de pares de Coulomb, declaración del peso, matriz de transferencia, error de Nyström y proyección. |
| `secciones/12_pigs.md` | PIGS: algoritmo, producción, dependencia con $\tau$, sesgo de interpolación y anomalía de $\tau=5$. |
| `secciones/13_controles_hulthen_pozo.md` | Controles exactos de Hulthén y del pozo cuadrado con la misma transferencia. |
| `secciones/14_criterio_cajas.md` | Criterio de cajas 9.6 con la condición (c), pared sin imagen y veredictos. |
| `secciones/15_tabla_controles.md` | Tabla de controles consolidada (la genera `codigo/16_tabla_controles.py`), **sin firmar**. |
| `secciones/17_registro_ia.md` | Registro de IA: fichas F2-01 a F2-14, correcciones C1–C22, supuestos, anomalías y pendientes. |
| `presentacion/diapositivas_fase2.pptx` / `.pdf` | Primera presentación: 11 láminas y 5 de respaldo, con las notas del orador. |
| `presentacion/guion_fase2.md` | Guion con el reparto (JS láminas 1–6; LF láminas 7–11), el texto de cada lámina y 8 preguntas probables. Son unos 7 min 52 s estimados a 150 palabras por minuto (`tiempos_guion.json`); no se ensayó con cronómetro. |
| `fuentes_control/` | Fuentes de Hulthén y del pozo (26-10-2026) con su estado, y la nota sobre una auditora de otra IA. |

### Código (`codigo/`)

| Archivo | Qué hace |
|---|---|
| `radial.py` | Solucionador radial genérico (diferencias finitas, Richardson): $E_0$, $E_1$, $\langle r\rangle$, $\langle r^2\rangle$, $F_{1/2}$, $\langle r\rangle/R$, umbral por energía cero. |
| `pares.py` | Tabla de la acción exacta de Coulomb $U_C$ ($h_{\rm tab}=0.01$ y 0.005 con Richardson), con caché en `resultados/tablas/` y extremos con Wigner-Kirkwood para $r>10$. |
| `transferencia.py` | Matriz de transferencia en banda (Nyström) para un resto $W(r)$ acotado: autovalor, autovector, observables, estimador mixto y aviso de la pared. |
| `pigs.py` | PIGS radial con la misma acción: puentes brownianos, extremos, escala; estimador mixto y puro; errores por bloques y entre cadenas. |
| `test_radial.py`, `test_transferencia.py`, `test_pigs.py` | Pruebas con `assert` (7, 7 y 14). |
| `10_radial_controles.py` | Controles del radial (Coulomb, $\delta=0.2$, Hulthén, pozo, cajas 9.6). |
| `11_transferencia_controles.py` | Controles de la transferencia (Coulomb, $\delta=0.2$ y 1.0, Trotter, Nyström, proyección). |
| `12_pigs_produccion.py` | Producción del PIGS (Coulomb y $\delta=0.2$), barrido en $\tau$ y bilineal frente a bicúbica. |
| `12b_pigs_replica_tau5.py` | Réplica 1 de $\tau=5$ (16 cadenas). |
| `12c_pigs_coulomb_tau5.py` | Coulomb con 8 cadenas e histograma, réplica 2 de $\tau=5$ y combinación de las 40 cadenas. |
| `13_controles_hulthen_pozo.py` | Hulthén y pozo cuadrado por la transferencia y el radial. |
| `14_criterio_cajas.py` | Condición (c) de 9.6: 15 cajas × 3 $\epsilon$ × 2 $h$; diagnóstico de la pared. |
| `15_limites.py` | Límites L03–L19 con la integral de camino. |
| `16_tabla_controles.py` | Genera `secciones/15_tabla_controles.md` y `resultados/16_tabla_controles.json` a partir de los JSON. |
| `16_primer_grafico.py` | Primer gráfico congelado (`figuras/16_primer_grafico.png`). Solo lee JSON, no calcula nada nuevo. |
| `18_figura_presentacion.py` | Figura de respaldo para la presentación (`figuras/18_primer_grafico.png`). El equipo elige entre la 16 y la 18 (decisión 8). |
| `../presentacion/generar_diapositivas_fase2.py` | Construye el pptx y el guion leyendo los JSON y la tabla 15. |

### Resultados, figuras y verificación

- `resultados/NN_*.json` tiene todas las cifras de cada script, con todos sus dígitos. Además:
  - `10_radial_u_delta02.npz`: la $u(r)$ de $\delta=0.2$.
  - `12_pigs_series.npz`: las series del Monte Carlo.
  - `tablas/*.npz`: la caché de $U_C$, 31 MB.
  - `archivo_pre_V3/`: copia de antes de las correcciones V3; no se usa.
- `figuras/`: 10 figuras, cada una con su script.
  - Huellas sha256 en `secciones/15_tabla_controles.md` y en la Parte XIV.2 de la bitácora.
  - La figura 16 se congela por la huella de sus píxeles (`ef843a83…`), porque los bytes del PNG cambian al regenerarla.
- `verificacion/`:
  - `V1_recalculo_independiente.md` y `codigo_independiente/`: el recálculo con código propio.
  - `V2_auditoria_adversarial.md` y `V2_auditoria/`: la auditoría adversarial.
  - `V3_respuesta_hallazgos.md`: la respuesta a los 20 hallazgos.
  - `*_salida.txt`: la salida impresa de cada script.
  - `revision_final_test_*.txt`: las pruebas de la revisión final.

## Cómo reproducir todo, en orden

Requisitos: Python 3 con numpy, scipy, matplotlib, sympy y python-pptx. En la revisión final se usaron Python 3.13, numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.2 y sympy 1.14.0. Para el PDF hacen falta pandoc y Chromium (Playwright). Todos los scripts usan rutas relativas a su propio archivo, fijan sus semillas (20262000+k) y usan como máximo 4 procesos.

Los tiempos son los de reloj medidos en la máquina compartida de 4 núcleos, con la caché de tablas $U_C$ ya creada. Si se borra `resultados/tablas/`, la primera ejecución recalcula las tablas y tarda más; ese tiempo no se midió.

| Paso | Orden (desde `fase2/codigo/`) | Tiempo aprox. | Necesita |
|---|---|---|---|
| 0 | `python test_radial.py`; `python test_transferencia.py`; `python test_pigs.py` | 5 s; 1 s; 34 s | nada |
| 1 | `python 10_radial_controles.py` | 6 s | — |
| 2 | `python 11_transferencia_controles.py` | 22 s | crea o usa `resultados/tablas/` |
| 3 | `python 12_pigs_produccion.py` | 9.3 min (4 procesos) | tablas |
| 4 | `python 12b_pigs_replica_tau5.py` | 2.3 min | tablas |
| 5 | `python 12c_pigs_coulomb_tau5.py` | 3.7 min | `12_pigs.json`, `12b_pigs_replica.json` |
| 6 | `python 13_controles_hulthen_pozo.py` | 2.2 min (3 procesos) | tablas |
| 7 | `python 14_criterio_cajas.py` | 1.7 min | `10_radial.json` |
| 8 | `python 15_limites.py` | 33 s | tablas |
| 9 | `python 16_tabla_controles.py` | segundos | JSON 10 a 15 |
| 10 | `python 16_primer_grafico.py`; `python 18_figura_presentacion.py` | segundos | JSON 10 a 12c |
| 11 | `python ../presentacion/generar_diapositivas_fase2.py` (y LibreOffice para el PDF) | no medido | JSON, tabla 15, figura 16 |
| 12 | PDF de la bitácora (ver abajo) | ~1 min | pandoc, Chromium |

Total: unos 20 minutos de cómputo. Las cadenas de Monte Carlo salen idénticas bit a bit con las mismas semillas (V2 y V3).

Dos avisos al reproducir:
- Si se vuelve a ejecutar `16_tabla_controles.py`, la tabla 15 suma dos filas de figuras (16 y 18), con el script vacío. El resto sale idéntico (comprobado en una copia en la revisión final).
- Al regenerar la figura 16 cambian los bytes del PNG pero no sus píxeles.

PDF de la bitácora (como se hizo en la revisión final):
1. Copiar `bitacora_fase2.md` y cambiar en la copia `\rm` por `\mathrm{...}`.
2. Convertir con `pandoc copia.md -t html5 -s --mathml --embed-resources --resource-path=fase2 --css estilo.css -o bit.html`.
3. Imprimir `bit.html` a A4 con Chromium (Playwright, `page.pdf`).

## Qué falta (lo humano)

- Firma de Juan Sebastián en `secciones/15_tabla_controles.md` y las 10 decisiones de `decisiones_fase2.md`:
  1. redefinir el control de tabulación (Richardson $h^4$);
  2. anomalía de $\tau=5$;
  3. umbral 0.1 de la ley de caja;
  4. pozo: ley $\epsilon^{3/2}$ y extrapolación en $h$;
  5. pared en $R$ sin imagen;
  6. corrección de Wigner-Kirkwood;
  7. firma de la tabla de controles;
  8. figuras congeladas (16 o 18);
  9. bitácora y registro de IA;
  10. presentación y fuentes de control.
- Ensayar la presentación con cronómetro (límite 9 + 5 min) y aprobarla.
- Auditoría con otra IA (`fuentes_control/auditor_otra_ia.md`): todavía no se hizo, y las dos verificaciones fueron otras instancias de Claude.
