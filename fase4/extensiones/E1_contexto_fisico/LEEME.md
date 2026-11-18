# E1 · Contexto físico del umbral

**Pregunta.** ¿Qué significa físicamente $\delta_c = 1.1906124211$ en sistemas reales, sin presentarlo como una
"cifra universal"? Se traduce a tres sistemas (hidrógeno en un plasma de Debye, materia oscura con mediador ligero
y un deuterón de juguete) declarando en cada uno qué parámetro se mantiene fijo.

## Cómo reproducir

```
cd fase4/extensiones/E1_contexto_fisico/codigo
export OMP_NUM_THREADS=1
python3 01_umbral_y_controles.py    # 9 s   umbrales 1s, 2s, 3s con dos métodos; Coulomb y Hulthén
python3 02_plasma.py                # 13 s   longitud crítica, diagrama (n_e, T), E_1s(lambda_D)
python3 03_materia_oscura.py        # 2 s    alpha m_chi/m_phi crítico, Hulthén, antirresonancia
python3 04_deuteron.py              # 136 s  deuterón de juguete, radio, m_pi crítico, punto de NPLQCD
python3 05_mapa.py                  # figura común (delta frente al parámetro físico)
python3 06_verificacion.py          # diagnósticos (V1 a V5)
python3 07_documentos.py            # controles.md, verificacion.md, seccion_articulo.md, LEEME.md
```
`comun_e1.py` contiene las constantes (con su fuente) y los dos métodos; importa `fase2/codigo/radial.py` y
`fase3/codigo/comun3.py` sin modificarlos.

## Resultados principales

- **Plasma:** $\lambda_D^c = a_0/\delta_c = 0.8399039\,a_0$ (44.45 pm); curva
  $n_e = 2.798\times10^{22}$ cm$^{-3}$ $\times\,(k_BT/\text{eV})$. Sobre esa curva
  $N_D = 0.0103\,(k_BT/\text{eV})$, así que allí $N_D < 1$ por debajo de unos 97 eV y $N_D \le 10$ hasta
  unos 972 eV: el modelo estático de Debye, que pide $N_D \gg 1$, no es válido en esa región.
- **Materia oscura:** hay 1s si $\alpha m_\chi/m_\phi > 1.679808$ (2s: 6.4473;
  3s: 14.3420). Compatible con la "primera resonancia s en b = 1.68" de Tulin, Yu y Zurek (2013),
  que es la etiqueta de una curva ilustrativa, no un umbral calculado con precisión.
  Hulthén con $\kappa$ = 1.6 o $\pi^2/6$ se equivoca en -4.8% y
  -2.1%.
- **Deuterón de juguete** ($m_\pi$ promedio): $\delta_d = 0.83046$ (0.698 $\delta_c$),
  $g/\hbar c = 0.3541$, radio de nucleones puntuales del modelo 1.9706 fm frente a
  un radio de estructura experimental de 1.9756 ± 0.0004 fm; $m_\pi^c$ a $g$ fijo = 197.9 MeV,
  contradicho por NPLQCD (ligado a 805.9 MeV); para reproducir la red, $g$ debe ser 3.02 veces el
  físico. Sensibilidad a $g$ fijo -4.76 frente a -1.74 de Berengut et al.
  (2.4 veces en $K^q_\text{deut}$ si se deja variar también la masa del nucleón).
- Controles: ver `controles.md` (tres no pasan, con su causa medida: C6, C7 y C9).

## Archivos

`seccion_articulo.md` (sección lista para el artículo), `controles.md`, `verificacion.md`, `fuentes.md`,
`registro_ia.md`, `resultados/*.json` y `*_salida.txt`, `figuras/02_plasma_diagrama.png`,
`figuras/02_plasma_energia.png`, `figuras/05_mapa_delta.png`.

## Qué quedó sin hacer

- No pudimos leer el apéndice A.2 de Petraki, Postma y de Vries (el texto que devuelve arXiv se corta antes); solo
  verificamos lo que dice su texto principal.
- No verificamos en el editor el volumen y la página de Murillo y Weisheit (*Phys. Rep.* 302, 1, 1998), que
  conocemos por la cita de Janev et al.; por eso no está en las referencias de la sección. (El número de artículo de
  Berengut et al., 085018, lo cerró la revisión adversarial con el DOI que da arXiv.)
- La revisión de Tulin y Yu (2018) se leyó solo en parte (el HTML se corta); no encontramos la cifra 1.68 en la
  parte leída.
- No hicimos un escenario con $g$ que dependa de $m_\pi$ según una fórmula de la teoría quiral: solo el punto de
  la red y la sensibilidad local de Berengut et al.
- La auditoría con Gemini (D4) queda para el paso de revisión.
- Revisión adversarial independiente (17-11-2026): `revision/informe_revision.md`, con código propio que recalcula
  todas las cifras centrales por métodos distintos.
