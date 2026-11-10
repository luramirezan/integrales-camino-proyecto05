# Umbral de enlace en el potencial de Yukawa con integrales de camino

**Proyecto 05 · Introducción a la Investigación Teórica · 2026-II**
Grupo SLV: Juan Sebastián Calixto y Luis Felipe Ramírez.

Este repositorio reúne los códigos, las explicaciones, las figuras y las bitácoras del proyecto. La pregunta es:

> ¿Para qué valor del apantallamiento $\mu$ deja de existir el estado ligado $1s$ del potencial $V(r) = -g e^{-\mu r}/r$, y cómo se comportan su energía $E_0$ y su tamaño $\langle r\rangle$ al acercarse a ese valor?

Todo depende de un solo número sin unidades, $\delta = \mu\hbar^2/(mg)$. En unidades $\hbar = m = g = 1$ el potencial es $V = -e^{-\delta r}/r$ y el umbral de referencia (Fase 1) es $\delta_c = 1.1906124211$.

---

## Por dónde empezar

| Si quieres... | Lee |
|---|---|
| Entender la Fase 2 sin entrar en detalles | [`fase2/explicacion_sencilla/fase2_explicada.md`](fase2/explicacion_sencilla/fase2_explicada.md) (o el PDF al lado) |
| Ver el resumen técnico de la Fase 2 y el orden para reproducirla | [`fase2/LEEME.md`](fase2/LEEME.md) |
| Leer el código de la Fase 2 en orden | la guía de abajo, [Fase 2 script por script](#fase-2-script-por-script) |
| Leer la bitácora completa de la Fase 2 | [`fase2/bitacora_fase2.md`](fase2/bitacora_fase2.md) (o el PDF) |
| Ver la Fase 1 (planteamiento, cotas, plan) | [`fase1/bitacora_fase1_entrega.pdf`](fase1/bitacora_fase1_entrega.pdf) y [`fase1/secciones/`](fase1/secciones) |

---

## Estructura

```
.
├── README.md                  este archivo
├── requirements.txt           librerías de Python
├── enunciado/                 guía de bitácora del curso e índice de fuentes
├── bitacoras_estudio/         bitácoras 1 y 2 del grupo (LaTeX): trayectoria máxima y plan de estudio de integrales de camino
├── fase1/
│   ├── codigo/                scripts 00–09 (adimensionalización, cotas, referencia numérica, acción euclídea, costos)
│   ├── secciones/             explicación de cada bloque, una sección por script
│   ├── figuras/               figuras que generan los scripts
│   ├── bitacora_fase1_entrega.tex / .pdf
│   ├── guion_fase1.md, decisiones_pendientes.md, que_sigue_fase2.md
└── fase2/
    ├── LEEME.md               resumen de resultados y orden de reproducción
    ├── codigo/                módulos (radial, pares, transferencia, pigs), pruebas y scripts 10–18
    ├── secciones/             explicación de cada bloque (10–17)
    ├── figuras/               figuras de cada script
    ├── resultados/            cifras de cada script en JSON (todos los dígitos)
    ├── verificacion/          recálculo independiente (V1), auditoría (V2), respuesta (V3) y salidas impresas
    ├── explicacion_sencilla/  la Fase 2 contada en lenguaje simple
    ├── presentacion/          guion, PDF de las láminas y script que las genera
    ├── fuentes_control/       fuentes de los controles exactos (Hulthén, pozo)
    ├── auditoria_gemini/      script e informe de la auditoría con otra IA
    ├── revision_juan_sebastian/  lista de revisión para el compañero
    ├── bitacora_fase2.md / .pdf
    └── decisiones_fase2.md, que_sigue_fase3.md
```

---

## Cómo correr los scripts

Requisitos: Python 3.11 o más reciente.

```bash
pip install -r requirements.txt
```

Todos los scripts usan rutas relativas a su propio archivo, así que se pueden correr desde cualquier carpeta. Fijan sus semillas, así que dan los mismos números.

### Fase 1

Cada script es independiente y guarda su figura en `fase1/figuras/`:

```bash
cd fase1/codigo
python 01_adimensionalizacion.py
```

| Script | Qué hace | Explicación |
|---|---|---|
| `00_toy_model.py` | Modelos de juguete con umbral exacto (Hulthén, pozo cuadrado) y la cota $1 \le \delta_c \le 2$ | `secciones/00_marco.md` |
| `01_adimensionalizacion.py` | Reduce el problema a un solo parámetro $\delta$ (sympy) | `secciones/01_adimensionalizacion.md` |
| `02_limite_coulomb.py` | Comprueba el límite $\delta \to 0$ (hidrógeno, $E_0 = -1/2$) | `secciones/02_limite_coulomb.md` |
| `03_cota_variacional.py` | Cota variacional: si la energía de prueba es negativa, hay estado ligado | `secciones/03_cota_variacional.md` |
| `04_cota_bargmann.py` | Cota de Bargmann: por encima de cierto $\delta$ no puede haber ligado | `secciones/04_cota_bargmann.md` |
| `05_referencia_numerica.py` | Valor de referencia de $\delta_c$, $E_0$ y $\langle r\rangle$ por métodos independientes | `secciones/05_referencia_numerica.md` |
| `06_fuentes.py` | Comprueba las cifras citadas de la literatura | `secciones/06_fuentes.md` |
| `07_limites_fisicos.py` | Límites físicos que todo algoritmo debe cumplir | `secciones/07_limites_fisicos.md` |
| `08_accion_euclidea.py` | Acción euclídea, peso de la integral de camino y por qué la acción primitiva falla en $r=0$ | `secciones/08_accion_euclidea.md` |
| `09_prueba_costos.py` | Prueba de costo y plan de cómputo para la Fase 2 | `secciones/09_plan_computo.md` |

### Fase 2

Desde `fase2/codigo/`, en este orden (unos 20 minutos en total con 4 núcleos):

```bash
cd fase2/codigo
python test_radial.py
python test_transferencia.py
python test_pigs.py
python 10_radial_controles.py
python 11_transferencia_controles.py
python 12_pigs_produccion.py
python 12b_pigs_replica_tau5.py
python 12c_pigs_coulomb_tau5.py
python 13_controles_hulthen_pozo.py
python 14_criterio_cajas.py
python 15_limites.py
python 16_tabla_controles.py
python 16_primer_grafico.py
python 18_figura_presentacion.py
```

La primera vez que se corre `11_transferencia_controles.py`, el programa calcula y guarda la tabla de la acción de Coulomb en `fase2/resultados/tablas/` (unos 31 MB). Esa carpeta no se sube al repositorio porque se regenera sola; por eso la primera ejecución tarda más que los tiempos de `fase2/LEEME.md`.

---

## Fase 2 script por script

La Fase 2 calcula la energía y el tamaño del estado ligado **con la integral de camino** y los compara contra una referencia independiente. La idea en tres pasos:

1. **Referencia.** Se resuelve la ecuación radial de Schrödinger de la forma clásica, muy precisa. Contra esto se compara todo.
2. **El eslabón de la integral de camino.** El tiempo imaginario se parte en pasos $\epsilon$. En cada paso, la parte de Coulomb ($-1/r$) se trata *exacta* (acción de pares) y el resto, $W(r) = (1 - e^{-\delta r})/r$, que es suave y acotado, se trata aproximado. Así el peso queda positivo y sin la divergencia en $r=0$ que arruina la acción primitiva.
3. **Dos formas de usar ese eslabón.** (a) **Matriz de transferencia:** se convierte en una matriz y se saca su autovalor más grande, sin ruido estadístico. (b) **PIGS** (Monte Carlo de integral de camino del estado fundamental): se muestrean caminos al azar y se promedia, con barras de error.

Si los dos métodos coinciden con la referencia en casos con respuesta exacta (Coulomb, Hulthén, pozo cuadrado), se puede confiar en ellos cerca del umbral.

### Módulos base (lo que usan todos los scripts)

| Archivo | Qué contiene | Cómo leerlo |
|---|---|---|
| [`radial.py`](fase2/codigo/radial.py) | Solucionador radial por diferencias finitas con extrapolación de Richardson. Da $E_0$, $\langle r\rangle$, $\langle r^2\rangle$ y el umbral. | Es la referencia. Empieza por la función que arma la matriz y la que extrapola en la malla. |
| [`pares.py`](fase2/codigo/pares.py) | Tabla de la acción exacta de Coulomb $U_C(r, r'; \epsilon)$. Guarda caché en `resultados/tablas/`. | Es la pieza "exacta" del eslabón. Lo importante: el peso es positivo y finito en $r=0$. |
| [`transferencia.py`](fase2/codigo/transferencia.py) | Matriz de transferencia en banda (método de Nyström): autovalor, autovector, observables. | Toma el eslabón de `pares.py`, le suma $W(r)$ y saca $E_0 = -\ln(\lambda)/\epsilon$. |
| [`pigs.py`](fase2/codigo/pigs.py) | Monte Carlo PIGS: mueve caminos con puentes brownianos, estima la energía y los observables con errores por bloques. | Usa el mismo eslabón que la transferencia; si los dos coinciden, el muestreo está bien. |
| `test_*.py` | Pruebas automáticas con `assert` (7, 7 y 14). | Correrlas primero: si pasan, los módulos funcionan. |

### Scripts de producción

| Script | Pregunta que responde | Sección que lo explica | Figura |
|---|---|---|---|
| [`10_radial_controles.py`](fase2/codigo/10_radial_controles.py) | ¿La referencia reproduce Coulomb, Hulthén, el pozo y el $\delta_c$ de la Fase 1? | [`10_solucionador_radial.md`](fase2/secciones/10_solucionador_radial.md) | `10_radial_convergencia.png` |
| [`11_transferencia_controles.py`](fase2/codigo/11_transferencia_controles.py) | ¿La integral de camino (transferencia) da la misma energía? ¿Con qué orden baja el error al achicar $\epsilon$? | [`11_accion_pares_transferencia.md`](fase2/secciones/11_accion_pares_transferencia.md) | `11_trotter.png`, `11_proyeccion.png` |
| [`12_pigs_produccion.py`](fase2/codigo/12_pigs_produccion.py) | ¿El Monte Carlo concuerda dentro de sus barras de error en $\delta = 0.2$? | [`12_pigs.md`](fase2/secciones/12_pigs.md) | `12_pigs_delta02.png`, `12_pigs_tau.png` |
| [`12b_pigs_replica_tau5.py`](fase2/codigo/12b_pigs_replica_tau5.py), [`12c_pigs_coulomb_tau5.py`](fase2/codigo/12c_pigs_coulomb_tau5.py) | Réplicas para estudiar la anomalía en $\tau = 5$ | [`12_pigs.md`](fase2/secciones/12_pigs.md) | — |
| [`13_controles_hulthen_pozo.py`](fase2/codigo/13_controles_hulthen_pozo.py) | ¿Funciona igual en potenciales con solución exacta? | [`13_controles_hulthen_pozo.md`](fase2/secciones/13_controles_hulthen_pozo.md) | `13_controles.png` |
| [`14_criterio_cajas.py`](fase2/codigo/14_criterio_cajas.py) | Cerca del umbral, ¿el estado está ligado o no? Se decide comparando varias cajas, no por el signo de un autovalor | [`14_criterio_cajas.md`](fase2/secciones/14_criterio_cajas.md) | `14_cajas.png` |
| [`15_limites.py`](fase2/codigo/15_limites.py) | ¿Se cumplen los límites físicos de la Fase 1 con la integral de camino? | [`15_tabla_controles.md`](fase2/secciones/15_tabla_controles.md) | `15_limites.png` |
| [`16_tabla_controles.py`](fase2/codigo/16_tabla_controles.py) | Junta todos los controles en una tabla (88 filas) | [`15_tabla_controles.md`](fase2/secciones/15_tabla_controles.md) | — |
| [`16_primer_grafico.py`](fase2/codigo/16_primer_grafico.py), [`18_figura_presentacion.py`](fase2/codigo/18_figura_presentacion.py) | Primer gráfico del avance (solo lee los JSON) | [`fase2/LEEME.md`](fase2/LEEME.md) | `16_primer_grafico.png`, `18_primer_grafico.png` |

### Resultados principales de la Fase 2

- En $\delta = 0.2$: referencia $E_0 = -0.3268085110$; transferencia extrapolada a $4\times10^{-9}$ de ella; PIGS $E = -0.326725 \pm 0.000068$ (a $1.2\sigma$).
- Controles exactos: Coulomb a $2\times10^{-7}$, Hulthén a $5\times10^{-9}$.
- Cerca del umbral: $\delta = 1.18$ ligado y $\delta = 1.20$ no ligado por los dos métodos, así que $\delta_c \in [1.18, 1.20]$, de acuerdo con la referencia.
- Pendiente: la anomalía de $\tau = 5$ en el PIGS y las 10 decisiones del equipo en [`decisiones_fase2.md`](fase2/decisiones_fase2.md).

---

## Qué no está en el repositorio

- La caché `fase2/resultados/tablas/*.npz` (31 MB) y las series del Monte Carlo `12_pigs_series.npz` (4.5 MB): se regeneran al correr los scripts. Sin ese archivo, `verificacion/codigo_independiente/v1d_pigs_series.py` necesita correr antes `12_pigs_produccion.py`.
- Los PDF de los artículos y libros de referencia y sus transcripciones, por derechos de autor. La lista está en [`enunciado/INDICE_FUENTES.md`](enunciado/INDICE_FUENTES.md).
- Las transcripciones completas de las conversaciones con Gemini (queda el informe de la auditoría).
- Las diapositivas en `.pptx` y el audio; queda el PDF de las láminas.

## Uso de IA

Buena parte del código y de los textos se hizo con ayuda de IA (Claude, de Anthropic), y la auditoría externa con Gemini. Cada fase tiene su registro: [`fase1/secciones/10_registro_ia.md`](fase1/secciones/10_registro_ia.md) y [`fase2/secciones/17_registro_ia.md`](fase2/secciones/17_registro_ia.md). Las decisiones y la firma de los resultados son del equipo.
