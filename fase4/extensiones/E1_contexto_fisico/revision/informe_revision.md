# Revisión adversarial de la extensión E1 (17-11-2026)

Revisor: un agente de Claude distinto del que escribió E1, con el encargo de buscar errores y no de confirmar.
Leí `CONTEXTO_COMUN.md` y todo E1 (LEEME, sección, controles, fuentes, registro, verificación, los ocho scripts y los
seis JSON). Todo lo nuevo está en esta carpeta `revision/`; los cambios a E1 se listan al final.

## 1. Recálculo independiente (código propio, métodos distintos)

`r01_recalculo_independiente.py` no importa nada de E1 ni de las Fases 2 y 3. Usa:

- **umbrales y longitud de dispersión:** ecuación de fase de Prüfer a energía cero,
  $\phi' = \cos^2\phi + 2e^{-\delta r}\sin^2\phi/r$, desde $r = 0$ exacto, con Radau (implícito); umbral n-ésimo en
  $\phi(R) = (n-\tfrac12)\pi$, $a_s = R - \tan\phi(R)$;
- **estado 1s:** colocación espectral de Chebyshev con mapeo $r = L_m(1+x)/(1-x)$, autovalores densos, observables
  por Clenshaw y Curtis, error estimado con dos tamaños de base;
- **sensibilidad:** Hellmann y Feynman, $d\varepsilon/d\delta = \langle e^{-\delta r}\rangle$, sin diferencias finitas;
- **constantes:** `scipy.constants` 1.18 (CODATA 2022) y masas del pion del PDG escritas a mano.

Controles del método nuevo: Coulomb $E+\tfrac12 = 4.5\times10^{-13}$, $\langle r\rangle - \tfrac32 = 2\times10^{-12}$;
Hulthén ($\delta = 1$) $E + \tfrac18 = 1.3\times10^{-13}$.

| cifra | E1 (JSON) | revisión | ¿coincide? |
|---|---|---|---|
| $\delta_c(1s)$ | 1.1906124210606 | 1.1906124210606 (R = 200 y 100) | sí, a 1e-13 |
| $\delta_c(2s)$, $\delta_c(3s)$ | 0.31020928271, 0.13945029406 | 0.31020928271, 0.13945029406 | sí |
| $\lambda_D^c/a_0$ (núcleo infinito; masa reducida) | 0.8399039; 0.8403613 | 0.8399039; 0.8403613 | sí |
| coeficiente de Debye; $n_e/T$ | 743.394 cm; 2.7975e22 cm⁻³/eV | 743.394 cm; 2.7975e22 | sí |
| $N_D/T$ en la curva; $T(N_D=1)$ | 1.0289e-2; 97.2 eV | 1.0289e-2; 97.19 eV | sí |
| $\Gamma_e$, $k_BT/E_F$, $a_{ws}/\lambda_D$ a 13.6 eV | 1.237, 0.710, 1.926 | 1.237, 0.710, 1.926 | sí |
| $E_{1s}$ en $\delta$ = 0.2 … 1.18 | A: −0.3268085114 … −0.0000309859 | −0.326808511372 … −0.000030985911 | sí con A; B (caja) falla en 1.18 (ver C7) |
| $2/\delta_c$; 2s; 3s | 1.679808; 6.4473; 14.3420 | 1.679808; 6.4473; 14.3420 | sí |
| Hulthén κ = 1.6, π²/6 | −4.751 %, −2.076 % | −4.751 %, −2.076 % | sí |
| antirresonancia ($a_s = 0$) | δ = 0.4478572850, b = 4.46571 | δ = 0.4478572850, b = 4.46571 | sí |
| $a_s(1.19)$, $a_s(1.20)$ | 2203.8, −142.93 | 2203.8, −142.93 | sí |
| $B_d$; $\mu$ | 2.22456637; 469.45915515 MeV | iguales | sí |
| $\delta_d$ (π promedio, π⁰, π±) | 0.8304583940, 0.8249221354, 0.8331636441 | iguales a 10 cifras | sí |
| $g/\hbar c$; $\langle r\rangle$; rms; ½ rms; 1/κ | 0.354068; 3.2000; 3.9413; 1.9706; 4.3177 fm | iguales | sí |
| $m_\pi^c$ (g fijo) | 197.904 (194.812 a 199.450) MeV | 197.904 (194.812 a 199.450) | sí; aumento 43.37 % |
| $d\ln B/d\ln m_\pi$ (g y μ fijos) | −4.758790 | −4.75878 (Hellmann y Feynman) | sí, a 2e-6 relativo |
| límite quiral, $\mu\alpha^2/2$ | 29.4 MeV | 29.43 MeV | sí |
| NPLQCD: $\delta_L$; g/ħc; cociente; δ con g físico | 0.921222 (0.8982 a 0.9488); 1.0708; 3.024; 2.7859 | iguales | sí |
| $r_\text{str}$ experimental | 1.9757 ± 0.0007 fm | 1.97573 (mismas entradas); 1.97558 ± 0.00044 con PDG 2024 | ver R1-01, R1-04 |
| Berengut $K_\text{deut}/K_\pi$ | −1.741 (−2.75 a −0.83) | −1.741; con la incertidumbre de $K_\pi$ también: −2.83 a −0.82 | ver R1-06 |

Conclusión numérica: **no encontré ningún error de cálculo**. Todas las cifras centrales salen igual con métodos
distintos, y las del texto salen de los JSON (salvo las excepciones de R1-12).

## 2. Hallazgos

| ID | gravedad | descripción | evidencia | corrección |
|---|---|---|---|---|
| R1-01 | media | $r_n^2 = -0.1161(22)$ fm² se presentaba como "del PDG", pero es el promedio antiguo que Filin et al. citan solo para comparar. El PDG 2024 (y pdgLive hoy) da −0.1155(17) fm². | Tabla de bariones N del PDG 2024 (espejo de KEK) y `pdglive.lbl.gov/view/S017MCR`. $r_\text{str}$ pasa de 1.97573 a 1.97558 fm. | **Corregido** en `comun_e1.py`; 04 a 07 vueltos a correr. |
| R1-02 | media | Se llamaba "radio de estructura del modelo" a $\tfrac12\langle r^2\rangle^{1/2}$ y `verificacion.md` decía que "es lo que corresponde al radio de estructura". El $r_\text{str}$ de Filin et al. (Ec. 2) sale del factor de forma de carga e incluye operadores de dos cuerpos y correcciones relativistas; el del modelo es solo el radio de nucleones puntuales de la función de onda (su parte principal). | Lectura de arXiv:1911.04877 (secciones sobre el operador de carga). | **Corregido** el nombre y añadida la advertencia en sección, LEEME y verificación. |
| R1-03 | media | Tulin, Yu y Zurek: "b = 1.68" y "b = 4.52" son las **etiquetas de curvas ilustrativas** de su figura 3 ($\alpha_X = 10^{-2}$), no un umbral ni un cero calculados con precisión. La sección decía que $2/\delta_c$ "es la que la literatura obtiene numéricamente" (exagerado) y C9 comparaba un cero exacto con un valor ilustrativo con tolerancia 0.005 (criterio mal planteado). | PDF de arXiv:1302.3898, Sec. IV B y VI. Medido (`r03_…py`): Hulthén de su Sec. VI, $b = 1.6\,r^2$ con $r = 1.69093$, da 4.575; el cero de la fase s del Yukawa a momento finito $kL = v/\alpha$ = 0.02, 0.05, 0.06, 0.1 sale en b = 4.4715, 4.5019, 4.5179, 4.6120. | **Corregido** el texto (1.68 "compatible", no "obtenido"); causa de C9 reescrita con estas cifras. C9 sigue "no pasa" (no se cambia un criterio después). La antirresonancia de Hulthén se calcula ahora en `03_materia_oscura.py`. |
| R1-04 | baja | La incertidumbre de $r_\text{str}$ sumaba las de $r_d$ y $r_p$ de CODATA como independientes, pero están casi totalmente correlacionadas (ambas salen de espectroscopía de H y D). | Con $r_d^2 - r_p^2$ = 3.82070(31) fm² (desplazamiento isotópico citado por Filin et al., Ec. 1): ±0.00044 fm en vez de ±0.00068 (con el $r_n^2$ nuevo, ±0.00059 sin correlación). | **Corregido** en `04_deuteron.py` (se guarda también la versión sin correlación). |
| R1-05 | media | La comparación de sensibilidad con Berengut et al. no decía que su $K^q_\text{deut}$ incluye la variación de la masa del nucleón ("emerges from both the nucleon mass … and the potential"). | Con $K^q_N = 0.048$ (su Ec. 2.4) y $\partial\ln B/\partial\ln\mu = 1 - s = 5.759$: $K^q_\text{deut}$(modelo) = −2.074 frente a −0.86, cociente 2.41 (sin $m_N$: −2.351, cociente 2.73). | **Añadido** al texto y al JSON de 04. La conclusión cualitativa no cambia. |
| R1-06 | baja | El rango −2.75 a −0.83 de Berengut solo propaga la incertidumbre de $K_\text{deut}$. | Con la de $K_\pi$: −2.83 a −0.82. | **Aclarado** en el texto ("solo con la incertidumbre de $K^q_\text{deut}$"). |
| R1-07 | baja | "Con el g físico, ese punto tendría δ = 2.786" usa ya la masa reducida de la red ($M_B/2$ = 817 MeV), sin decirlo. | Con g y μ físicos sería δ = 4.848. | **Aclarado** en el texto. |
| R1-08 | baja | "El radio lo fija sobre todo la cola $e^{-\kappa r}$" no se sostiene con la propia cifra: el límite de alcance cero da 1.527 fm, 23 % menos que el modelo. | 1.5265 frente a 1.9706 fm. | **Reescrito**: la cola la fija $B_d$, pero el resto lo pone el alcance del pion. |
| R1-09 | baja | `verificacion.md` atribuía la dispersión del Numerov en $h$ a "redondeo acumulado". Es redondeo, pero no acumulado: no depende de $R$ (igual con R = 30 y 60) y desaparece en aritmética extendida. Además $h = 1/400$ está más cerca de la referencia que el $h = 1/800$ que se reporta. | `r02_diagnostico_numerov.py`: float64 da −2.8e-11 y −1.35e-10 con h = 1/400 y 1/800; longdouble da −6.0e-13 y −4.7e-12. Arranque de orden $h^4$ no cambia nada. | **Reescrito** el párrafo. C1 pasa igual. |
| R1-10 | baja | C6 (Rogers et al. 0.83991): confirmado como precisión de la fuente. Además, la tabla 1 de Janev et al. da 0.839907, también 3 ppm por encima del nuestro, y una fuente secundaria (arXiv:1904.11166) cita a Gomes et al. con δ_c = 1.19061227(4), 1.5e-7 por debajo del nuestro. | Resumen de Rogers releído en Scilit; Janev releído en arXiv. Tres métodos independientes (E1 A, E1 B y Prüfer de la revisión) dan 1.1906124210606 a 1e-10. | **Documentado** en C6 y `fuentes.md`. No es error nuestro. |
| R1-11 | baja | Referencias incompletas que se podían cerrar. | Berengut et al.: DOI 10.1103/PhysRevD.87.085018 (arXiv). Crowley: *HEDP* **13**, 84–102 (2014) (referencia de revista en arXiv). | **Corregido** en la sección, LEEME y `fuentes.md`. |
| R1-12 | baja | No corregido, solo señalado: (a) en la tabla de "Método", μ es a la vez el inverso del alcance (en δ = μħ²/mg) y la masa reducida del deuterón; (b) `verificacion.md` escribe a mano 0.830460 y 197.91 MeV del prototipo (salen de su salida impresa, no de un JSON); (c) la incertidumbre de $m_\pi$ de NPLQCD (8.9 MeV) no se propaga a $\delta_L$ (no lo medí). | Lectura de `07_documentos.py`. | Propuesta: renombrar la masa reducida $m_r$ y guardar las cifras del prototipo en un JSON. |
| R1-13 | baja | Física del plasma, no un error: en la curva, a 1 a 13.6 eV los electrones están parcialmente degenerados ($k_BT/E_F$ = 0.30 a 0.71), así que ni siquiera la longitud de Debye clásica es la longitud de apantallamiento electrónica correcta (habría que usar la de Thomas y Fermi o una interpolación). El texto ya dice que el modelo no vale allí; esto lo refuerza. | Cifras de `02_plasma.json`, confirmadas. | Sugerencia de una frase; no lo cambié. |

## 3. Controles C6, C7 y C9: ¿error nuestro, de la fuente o de definición?

- **C6: de la fuente.** Rogers et al. (1970) dan 0.83991; el valor correcto es 0.8399039 (tres métodos). La cifra de 1970
  tiene una precisión menor que la que sugiere su número de decimales.
- **C7: nuestro, pero del método de control (B), no del resultado.** La colocación de Chebyshev confirma el método A en
  los ocho puntos (por ejemplo, δ = 1.18: −0.000030985911 frente a A −0.0000309859 y B −0.0000309816). El error de B
  es de discretización con $h = 1/40$ (cociente 16 al pasar a 1/80). Las cifras publicadas usan A, así que no hay
  que corregir nada.
- **C9: de definición.** 4.52 es una curva ilustrativa a velocidad finita; el cero exacto de $a_s$ a $v = 0$ es 4.4657.
  A $kL = v/\alpha \approx 0.06$ el cero de la fase s pasa por 4.52, y la fórmula de Hulthén del mismo artículo da 4.575.
  El control quedó mal planteado; no se cambia su criterio después de ver los datos.

## 4. Lo que comprobé y está bien

- La correspondencia δ en los tres sistemas: $a_0/\lambda_D$ (con $m_e$, como Rogers et al.); $2m_\phi/(\alpha m_\chi)$ con
  masa reducida $m_\chi/2$ (igual que Tulin et al., Sec. III); $m_\pi/(\mu\,g/\hbar c)$ con $\mu = m_pm_n/(m_p+m_n)$.
- El promedio de isospín $(2m_{\pi^\pm} + m_{\pi^0})/3$ es el natural para el intercambio de un pion en el canal
  I = 0 ($\tau_1\cdot\tau_2$ tiene dos partes cargadas y una neutra), y se dan además los dos extremos.
- La longitud de Debye: el texto usa la electrónica (la del NRL y la de Janev et al., con $T_e$ y $n_e$) y da la
  variante con protones (λ/√2, densidad a la mitad), que es correcta para electrones y protones a la misma T.
- El umbral de Hulthén $b = \kappa n^2$ (de $E_n = -\tfrac12(1/n - n\delta_H/2)^2$), la serie de arranque del Numerov
  ($b_3 = (1+\delta)/3$), el término de Darwin y Foldy $3/4m_p^2$ = 0.03317 fm², $1/(\sqrt8\kappa)$ para alcance cero.
- Fuentes releídas por mí: Tulin, Yu y Zurek (cifras, variables, κ = 1.6, Sec. VI); Rogers et al. (resumen); NPLQCD
  (805.9(0.6)(0.4)(8.9) MeV, 1.634 GeV, 19.5(3.6)(3.1)(0.2) MeV); Berengut et al. (Ec. 3.14, 4.1, Tabla I, Ec. 2.4,
  DOI); Filin et al. (Ec. 1, 2, 9); Feng, Kaplinghat y Yu (Ec. 7, $b = \pi^2n^2/6$); Epelbaum et al. (9.6 ± 1.9 MeV,
  DOI); Beane y Savage (frase del resumen, DOI); Crowley (revista); Janev et al. (0.839907, cita de Murillo y
  Weisheit, *Phys. Rep.* 302, 1 (1998), que sigue sin verificar en el editor); PDG 2024 ($r_n^2$).

## 5. Cambios hechos en E1

| archivo | cambio |
|---|---|
| `codigo/comun_e1.py` | $r_n^2$ = −0.1155(17) (PDG 2024); constantes nuevas `rd2_rp2_iso_u_fm2`, `K_N_q`, `rn2_filin_pdg_antiguo`; nota sobre 1.68 y 4.52 |
| `codigo/03_materia_oscura.py` | antirresonancia de Hulthén (digamma) en el JSON |
| `codigo/04_deuteron.py` | incertidumbre de $r_\text{str}$ con la diferencia isotópica; $K^q_\text{deut}$ del modelo con $m_N$ variable |
| `codigo/07_documentos.py` | textos de R1-02, R1-03, R1-05 a R1-09, R1-11; causas de C6 y C9; lee `revision/r03_extras.json` |
| `fuentes.md`, `registro_ia.md` | estados y notas de la revisión; fila E1-07 |
| regenerados | `resultados/03_*.json`, `04_*.json`, `05_*`, `06_*`, figura `05_mapa_delta.png`, `controles.md`, `verificacion.md`, `seccion_articulo.md`, `LEEME.md` |

Copias de los scripts antes del cambio: `revision/orig_*.py.txt`. Las cifras principales no cambian, salvo
$r_\text{str}$ = 1.9756 ± 0.0004 fm (antes 1.9757 ± 0.0007) y el acuerdo del radio, ahora 0.25 % (el texto lo
redondea a 0.2 %).

Archivos de esta carpeta: `r01_recalculo_independiente.py` (90 s) con `r01_recalculo.json` y su salida;
`r02_diagnostico_numerov.py` con su salida; `r03_antirresonancia_y_extras.py` con `r03_extras.json` y su salida.
La auditoría con Gemini no se hizo en esta revisión.
