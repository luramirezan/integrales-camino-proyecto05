# Revisión del artículo de 6 páginas: referencias y claridad

Revisado: `articulo_final_6p.pdf` (6 páginas, 18 referencias) y `main.pdf` (borrador de 5 páginas del compañero). Fecha: 28-11-2026.

## Resumen

- **Las 18 referencias del PDF de 6 páginas existen.** Ninguna es inventada: título, autores, revista, volumen y año coinciden con el registro del editor o de un índice con DOI.
- **17 de 18 respaldan lo que se les atribuye**, con lo comprobado en la fuente (resumen o texto completo). La excepción es [6] Gebremedhin y Weatherford: el artículo existe, pero el valor δc = 1.19061242106… no lo pude leer en la fuente primaria (APS y PubMed bloquean la descarga automática). Las notas del propio proyecto (`fase1/`) ya decían que ese número se tomó de una cita secundaria. Nuestro cálculo y el de Napsuciale [5] (1.1906124207(2)) lo respaldan, pero la cita en sí no está comprobada.
- **`main.pdf` tiene un problema grave:** su lista de referencias es de otro trabajo (PLUTO, discos de acreción, toros magnetohidrodinámicos). Ninguna de esas 6 referencias tiene que ver con el Yukawa, y el texto tiene marcadores «COLOCAR UN PAR DE CITAS», «CITA», «CITE» sin llenar. Si se entrega `main.pdf` así, sí parecerá un artefacto. La lista correcta es la del PDF de 6 páginas.
- Lo que no es de la literatura sino cálculo propio (la cota 1.19055 con 12 exponenciales, la prueba e^{−r/b}, c0, re, A², S) aparece en 2.1 sin decir que es propio. No es una cita falsa, pero un lector puede creer que falta una cita. Abajo va la frase para arreglarlo.

## 1. Referencias del PDF de 6 páginas

| # | Referencia | Estado | Qué se comprobó | Evidencia |
|---|---|---|---|---|
| 1 | Yukawa 1935, Proc. Phys.-Math. Soc. Japan 17, 48; reimpr. PTPS 1, 1 (1955) | Verificada | Existe en J-STAGE (vol. 17, p. 48) e INSPIRE. Es el artículo original del potencial. | [J-STAGE](https://www.jstage.jst.go.jp/article/ppmsj1919/17/0/17_0_48/_article), [INSPIRE](https://inspirehep.net/literature/32148) |
| 2 | Rogers, Graboske, Harwood 1970, PRA 1, 1577 | Verificada | Resumen: D0 = 0.83991 a0/Z, es decir δc = 1/0.83991 ≈ 1.1906. Calcularon el umbral, como dice el texto. | [Scilit](https://scilit.com/publications/0a9e895709c5f15dea4a14783ff346e9) |
| 3 | Gomes, Chacham, Mohallem 1994, PRA 50, 228 | Verificada | Resumen: qc = 1.19061227 ± 4×10⁻⁸ (variacional, LCAO). Es un refinamiento variacional. | [Scilit](https://scilit.com/publications/b1826ad4b884b2b864d95c2b506b4398) |
| 4 | Edwards et al. 2017, PTEP 2017, 083A01 | Verificada | arXiv:1706.09979, ec. (1.3): μc/αm = 1.1906122105(5). La diferencia con 1.1906124210606 es 2.1×10⁻⁷, como dice el texto. Autores: Edwards, Gerber, Schubert, Trejo, Weber. | [arXiv](https://arxiv.org/pdf/1706.09979), [OUP](https://academic.oup.com/ptep/article/2017/8/083A01/4092946) |
| 5 | Napsuciale y Rodríguez 2021, PLB 816, 136218 | Verificada | arXiv:2012.12969, ec. (38): δ10 = 1.1906124207(2). Es un refinamiento, compatible con el valor de [6]. | [arXiv](https://arxiv.org/pdf/2012.12969) |
| 6 | Gebremedhin y Weatherford 2023, PRE 108, 045301 | **Existe; valor sin comprobar en la fuente** | El artículo está en APS y PubMed con esos datos. No pude abrir el texto para ver 1.19061242106… Las notas del proyecto dicen que el número vino de una cita secundaria (arXiv:2510.10420). | [APS](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.108.045301), [PubMed](https://pubmed.ncbi.nlm.nih.gov/37978652/) |
| 7 | Klaus y Simon 1980, Ann. Phys. 130, 251 | Verificada | Registro de Caltech: el artículo estudia el orden α de e(λ) ~ (λ−λ0)^α. El resumen no da α = 2 (ℓ = 0) y α = 1 (ℓ ≥ 1), pero Serra et al. [8] lo citan exactamente para eso. | [Caltech](https://resolver.caltech.edu/CaltechAUTHORS:20180521-150501792) |
| 8 | Serra, Neirotti, Kais 1998, PRA 57, R1481 | Verificada | Dice «a = 2 para momento angular cero y a = 1 para no nulo [Klaus y Simon]». Trata el Yukawa: λc(ℓ=0) = 0.8399039 (δc = 1.19061) y λc(ℓ=1) = 4.540980 (δc(2p) = 0.220217, igual al nuestro). | [PDF del autor](https://www.chem.purdue.edu/kais/docs/papers/Physical-Review-1998.pdf) |
| 9 | Serra, manuscrito «A spatial finite size scaling method…» | Verificada (manuscrito) | El PDF existe; ejemplo de pozo cuadrado con ℓ = 1, radio de corte R, cruces de curvas R y R+1, μ = 3. No dice revista ni año, como ya advierte la referencia. Es el antecedente cercano para ℓ = 1, como dice el texto. | [PDF](https://www.famaf.unc.edu.ar/~serra/serra28.pdf) |
| 10 | Bargmann 1952, PNAS 38, 961 | Verificada | La cota n_ℓ < ∫r\|U\|dr/(2ℓ+1) da n0 < 2/δ para el Yukawa (comprobado a mano). | [MaRDI](https://portal.mardi4nfdi.de/wiki/Item:Q5814640), [Wikipedia](https://en.wikipedia.org/wiki/Bargmann%27s_limit) |
| 11 | Schwinger 1961, PNAS 47, 122 | Verificada | Recalculé la cota: Tr K² = 4(2 ln 2 − 1)/δ² = 1 da δc ≤ 2√(2 ln 2 − 1) = 1.24305. El número es correcto. | DOI 10.1073/pnas.47.1.122 |
| 12 | Feynman y Hibbs 1965, McGraw-Hill | Verificada | Libro clásico; la proyección al fundamental en tiempo imaginario está ahí. | — |
| 13 | Pollock y Ceperley 1984, PRB 30, 2555 | Verificada | Introduce la acción de pares para integrales de camino. | [APS](https://link.aps.org/doi/10.1103/PhysRevB.30.2555) |
| 14 | Ceperley 1995, RMP 67, 279 | Verificada | Revisión de integrales de camino con acción de pares. | [APS](https://link.aps.org/doi/10.1103/RevModPhys.67.279) |
| 15 | Bethe 1949, Phys. Rev. 76, 38 | Verificada | Teoría del rango efectivo, k cot η = −1/a + re k²/2. | [APS](https://link.aps.org/doi/10.1103/PhysRev.76.38) |
| 16 | Borasoy et al. 2007, EPJA 34, 185 | Verificada | Usa el «spherical wall method»: pared dura en R; condición cos δ_L j_L(kR) = sin δ_L y_L(kR) (para ℓ = 0 equivale a sin(kR+η0) = 0). | [Springer](https://link.springer.com/article/10.1140/epja/i2007-10500-9), [arXiv](https://arxiv.org/abs/0708.1780) |
| 17 | Nightingale 1976, Physica A 83, 561 | Verificada (detalle de año) | Es el artículo fundacional de la renormalización fenomenológica de sistemas finitos. IDEAS/Elsevier lo fechan en 1975 (el DOI dice «75»); la forma usual es «Physica A 83, 561 (1976)». Cualquiera de las dos es aceptable. | [IDEAS](https://ideas.repec.org/a/eee/phsmap/v83y1975i3p561-572.html) |
| 18 | Varshni 1990, PRA 41, 4682 | Verificada | Energías del potencial de Hulthén, usado como caso exacto. | [OUCI](https://ouci.dntb.gov.ua/works/4YYxxy64) |

**Qué hacer con [6].** Dos opciones, ambas caben en 6 páginas:
1. Abrir el PDF de Gebremedhin y Weatherford con el acceso de la UNAL y confirmar el número (y la fe de erratas de 2024, ec. 22, que menciona `referencias.bib`).
2. Si no se puede, cambiar en la Introducción «hasta δc = 1.19061242106… [6]» por «hasta δc = 1.1906124207(2) [5] y 1.19061242106… [6]», para que el valor no dependa solo de una cita no leída.

## 2. Problemas en `main.pdf` (borrador del compañero)

Errores que hay que corregir si se sigue con esta versión:

1. **Bibliografía equivocada:** las referencias [1]–[6] (PLUTO, Papaloizou y Pringle, Goldreich y Goodman, Hawley, Hawley y Balbus, Kuwabara et al.) son de otro artículo. Hay que reemplazarlas por la lista de 18 del PDF de 6 páginas.
2. **Citas sin llenar:** «COLOCAR UN PAR DE CITAS» (Resumen), «CITA» (Intro, 2.1, 2.2 ×2, 3.1), «CITE» (2.3). La correspondencia es: Resumen → [2, 6]; Yukawa → [1]; Bargmann → [10]; tiempo imaginario → [12]; acción de pares → [13, 14]; pared esférica → [16]; renormalización → [17]; Hulthén → [18].
3. **Error de física:** «cuenta con un infinito número de estados ligados». Es al revés: el Yukawa tiene un número **finito** de estados ligados (el infinito es el de Coulomb).
4. **Ecuación sin el 1/2:** «dE/dR = −u′(R)² < 0» debe ser −u′(R)²/2.
5. **sin(kr + η0) = 0** debe ser sin(kR + η0) = 0 (la pared está en R).
6. **Tabla 1:** la fila 400/800 copia exactamente los valores de 100/200 (1.1907465…, 1.190764616). Es un error de copia; los valores verdaderos de 400/800 están en los resultados del proyecto.
7. **Historia:** «sistemas atómicos» debe ser «núcleo atómico» (Yukawa explicaba la fuerza nuclear). «Heisenberg … Fermi» es una afirmación histórica sin cita; mejor quitarla o citar [1].
8. **Atribución equivocada:** «Ĩν(z) = Iν(z)e^{−z} el núcleo libre exacto»: el núcleo libre es Kℓ, no Ĩν.
9. «normalización fenomenológica» → «renormalización fenomenológica». «⟨r⟩ ≈ 1/2k» → 1/(2κ). Erratas: «e^{−mur}», «lso», «propocional», «correción».
10. El texto termina en «3.2 … La fig. 5». Falta el resto. También menciona PIGS por Monte Carlo y una figura de siete cajas que no están en la versión de 6 páginas.

## 3. Pasajes poco claros en el PDF de 6 páginas, con reescritura

Cada propuesta ocupa lo mismo o menos que el original.

**3.1 Cifras propias que parecen citas (§2.1).** Hoy: «Tres resultados analíticos encierran el umbral del 1s: una prueba e^{−r/b} …; la cota variacional con 12 exponenciales da δc ≥ 1.19055 …». Son cuatro resultados, y dos son cálculos propios sin cita.
→ «Cuatro cotas encierran el umbral del 1s: dos propias (una prueba e^{−r/b} da ligado si δ < 1, y una de Ritz con 12 exponenciales da δc ≥ 1.19055) y dos de la literatura: Bargmann [10], n0 < 2/δ, excluye el estado si δ ≥ 2, y Schwinger [11] da δc ≤ 2√(2 ln 2 − 1) ≈ 1.24305.»
Comprobar en el PDF que la raíz cubre todo «2 ln 2 − 1» (si cubre solo el 2, el valor sería 0.96).

**3.2 «un µc aislado carece de sentido» (§2.1).** Así se lee como un error.
→ «Solo δ tiene significado físico: a g y m fijos, el umbral en µ es µc = δc mg/ħ².» Quitar también «y d = δ − δc», que no se usa en las 6 páginas.

**3.3 Dos nombres para la misma constante.** c0 = 0.741192 (§2.1) y c = 0.741192 (§2.3) son el mismo número. Usar solo c y decir una vez «c = −d(1/a)/dδ, calculada a energía cero».

**3.4 «Como Kℓ no tiene imagen en R» (§2.2).** Es jerga.
→ «Kℓ es el núcleo del espacio libre: no incluye el término imagen que anularía el propagador en r = R. Por eso la pared solo actúa en los tiempos discretos y queda efectivamente en R + βw√ε, con βw = −ζ(1/2)/√(2π) = 0.5826, valor que comprobamos numéricamente.»

**3.5 El término re/(4R) (§2.3).** Aparece sin haberse definido; en y* el término es 3re/(8R).
→ «La convergencia es 1/R² aunque y* tenga una corrección 1/R: en el cruce de dos cajas los términos de orden 1/R se cancelan y el primer resto es de orden 1/R².»

**3.6 Métodos A y B, y la «receta».** Solo se definen en la leyenda de la Tabla 1, pero el Resumen y §3.2–3.3 los usan. Añadir al final de §2.2: «Llamamos A a aplicar la receta a E0 y propagarla al cruce, y B a aplicarla directamente al cruce.» En el Resumen cambiar «si la receta de extrapolación se aplica al cruce» por «si la extrapolación se aplica al cruce».

**3.7 βy sin definir (§3.3).** «δ* − αy/R² − βy/R³» usa βy, que no aparece en las 6 páginas. En §2.3, tras «αy = 1.4819», añadir «y βy = 3π²re²/(32c) = 3.958».

**3.8 La Tabla 1 recortada no sostiene el texto (§3.2).** Se citan cocientes 4.125, 4.062, 4.031, 4.016 y cuatro diferencias «pares 50 a 400», que necesitan las filas 100/200 y 400/800, pero la tabla solo tiene 4 filas. Dos opciones: volver a poner las dos filas (dos renglones de tabla) o escribir «(pares 50/100 a 400/800; tabla completa en el repositorio)».

**3.9 Fórmula de tres cajas (§3.3).** «δc ≃ δ2* − (δ1* − δ2*)/3» aparece sin explicación.
→ «Con los cruces δ1* (50/100) y δ2* (100/200) y la ley 1/R², la extrapolación de Richardson da δc ≃ δ2* − (δ1* − δ2*)/3.»

**3.10 rℓ «conocida» sin cita (§2.4).** «rℓ = −2[(2ℓ−1)!!]²/A² (conocida para estados débilmente ligados, aquí derivada y comprobada)». Sin una cita, un revisor puede pedirla. O se cita (por ejemplo König, Lee y Hammer 2011, PRL 107, 112001, que ya está en `referencias.bib`, tras comprobar que contiene la relación), o se escribe «(la derivamos y la comprobamos numéricamente)».

**3.11 q, s, γY sin significado (§2.4).** Añadir «q y s son factores que salen de comparar las cajas R y 2R; γY es el coeficiente de la corrección de orden R⁻² del cruce de Y».

**3.12 Leyenda de la Fig. 1(b).** La imagen dice «ec. (5), sin ajuste», pero en las 6 páginas la ecuación es la (4). Hay que regenerar la figura o cambiar la etiqueta. Este es el tipo de detalle que hace pensar en un «artefacto».

**3.13 Conclusión 5 sin respaldo en el texto.** «en la onda p, 10⁻⁵ en δ con dos cajas … o unos 1.5×10⁻⁶ con tres cajas» no aparece en §3.5. Añadir una frase en §3.5 con esos dos números o quitarlos de la conclusión.

**3.14 «con la barra que incluye el resto de la ley» (§3.5).**
→ «con una barra que incluye el término siguiente de la ley (6)».

**3.15 Controles (§3.6).** «471 controles: 395 pasan, 49 no pasan…» sin decir dónde están. Añadir «(lista en el repositorio)».

**3.16 Apantallamiento de Debye (Intro).** «El mismo perfil aparece como apantallamiento de Debye y Hückel en plasmas» va sin cita. Es conocimiento común, pero si sobra espacio se puede citar el NRL Plasma Formulary (Huba 2004, ya en `referencias.bib`).
