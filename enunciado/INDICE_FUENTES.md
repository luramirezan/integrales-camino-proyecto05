# Índice de fuentes — Integrales de camino (Path Integrals)

| # | Autor(es) | Año | Título | URL original | Archivo(s) | Estado |
|---|---|---|---|---|---|---|
| 01 | R. MacKenzie | 2000 | Path Integral Methods and Applications | https://arxiv.org/abs/quant-ph/0004090 (fuente: https://arxiv.org/e-print/quant-ph/0004090) | `md/01_MacKenzie_2000_PathIntegralMethods.md` | ok |
| 02 | R. Rosenfelder | 2017 | Path Integrals in Quantum Physics (v4) | https://arxiv.org/abs/1209.1315 (fuente: https://arxiv.org/e-print/1209.1315) | `md/02_Rosenfelder_2017_PathIntegralsQuantumPhysics.md` | ok |
| 03 | C. Grosche | 1993 | An Introduction into the Feynman Path Integral | https://arxiv.org/abs/hep-th/9302097 (PDF: https://arxiv.org/pdf/hep-th/9302097) | `md/03_Grosche_IntroFeynmanPI.md` | transcripción IA (visión) |
| 04 | K. Fujikawa | 1996 | Path integral of the hydrogen atom, Jacobi's principle of least action and one-dimensional quantum gravity | https://arxiv.org/abs/hep-th/9602080 (fuente: https://arxiv.org/e-print/hep-th/9602080) | `md/04_Fujikawa_1996_HydrogenPathIntegral.md` | ok |
| 05 | C. Grosche, F. Steiner | 1994/95 | How to solve path integrals in quantum mechanics (DESY 94-180; J. Math. Phys. 36, 2354) | https://www-library.desy.de/preparch/desy/1994/desy94-180.pdf | `md/05_GroscheSteiner_HowToSolve.md` | transcripción IA (visión), parcial: pp. 28-30 sin transcribir (bloqueo del filtro de la API), ver PDF |
| 06 | M. S. Suzuki | 2021 | Feynman Path Integral: Formulation of Quantum Dynamics | https://bingweb.binghamton.edu/~suzuki/QM_Graduate/Feynman_path_integral.pdf | `md/06_Suzuki_FeynmanPathIntegral.md` | transcripción IA (visión) |
| 07 | R. Köberle | 2021 | Introduction to path-integral Quantum Field Theory – A toolbox | https://www.ifsc.usp.br/~roland/pdf/PIQFT_00.pdf (DOI 10.1590/1806-9126-RBEF-2021-0170) | `md/07_Koberle_PIQFTToolbox.md` | transcripción IA (visión) |
| 08 | H. Kleinert | 2009 | Path Integrals in Quantum Mechanics, Statistics, Polymer Physics, and Financial Markets (5ª ed.) | https://hagenkleinert.de/documents/pi/HagenKleinert_PathIntegrals.pdf | `pdf/08_Kleinert_2009_PathIntegralsBook.pdf` | solo PDF (1641 pp.) |
| 09 | H. Kleinert | — | Path Integrals — Elementary Properties and Simple Solutions (cap. 2 del libro anterior) | https://www.physics.mcgill.ca/~keshav/551II/pathintegral551.pdf | `md/09_Kleinert_Ch2_ElementaryProperties.md` | transcripción IA (visión) |
| 10 | T. Saporiti (sup. J. M. Frost) | 2020 | Path Integral Monte Carlo and Hydrogen bond | http://saporiti.ch/pdfs/ProjectReport_Frost_Saporiti.pdf | `md/10_Saporiti_PIMC_HydrogenBond.md` | transcripción IA (visión); código C++ del apéndice I resumido |
| 11 | T. Saporiti | 2022 | Path integrals in quantum mechanics, Semiclassical approximation | https://saporiti.ch/pdfs/Proseminar_Report_Saporiti.pdf | `md/11_Saporiti_Semiclassical.md` | transcripción IA (visión) |
| 12 | J. Zinn-Justin | ~2015 | Lecture 3: Path integrals in quantum mechanics (curso QFT, CEA/IRFU) | https://irfu.cea.fr/Phocea/file.php?class=page&file=678/QFT-IRFU2.pdf | `md/12_ZinnJustin_QFTIRFU2.md` | transcripción IA (visión) |
| 13 | R. Rattazzi | 2009 | The Path Integral approach to Quantum Mechanics — Lecture Notes for Quantum Mechanics IV (incluye "Functional and Euclidean Methods") | https://courses.physics.ucsd.edu/2016/Spring/physics142/Lectures/Lecture3/RevisedLectureNotesV2.pdf | `md/13_Rattazzi_FunctionalEuclidean.md` | transcripción IA (visión) |
| 14 | F. Steiner | 1984 | Exact path integral treatment of the hydrogen atom, Phys. Lett. A 106, 363 | https://doi.org/10.1016/0375-9601(84)90123-1 | — | no obtenido (de pago; no se encontró copia abierta legítima) |
| 15 | Feynman & Hibbs | — | Quantum Mechanics and Path Integrals (ed. emendada, Dover) | — | — | no obtenido (protegido por derechos de autor; se omitió deliberadamente) |

## Notas

- Ítems 01, 02 y 04: convertidos con `pandoc -f latex -t gfm+tex_math_dollars` directamente desde el código fuente LaTeX de arXiv (alta fidelidad matemática).
- Ítem 03: el fuente de arXiv está en AMS-TeX plano (`\input amstex`), no compatible con el lector LaTeX de pandoc; se usó el PDF (94 pp.) para transcripción por IA (visión), no extracción automática de texto.
- Ítems 05–07, 09–13: no tienen fuente LaTeX disponible; se descargó únicamente el PDF y se renderizaron sus páginas a PNG (110 dpi) en `pages/<NN>_<nombre>/`, para transcripción manual asistida por IA (visión), evitando la extracción automática de texto de PDF (que distorsiona ecuaciones, especialmente en escaneos como el ítem 05).
- Ítem 08: libro completo de Kleinert (1641 páginas); se dejó solo como PDF + páginas renderizadas por su extensión; no se transcribió a Markdown en esta etapa.
