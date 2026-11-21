# Notas del borrador del artículo final (proyecto 05)

17-11-2026 · borrador escrito por Claude (IA) por delegación de Lucho (decisión D15). Pendiente de revisión del equipo.

## Archivos de esta carpeta

| Archivo | Qué es |
|---|---|
| `articulo_final.md` | El borrador, en Markdown con citas de pandoc (`[@Clave]`) |
| `referencias.bib` | Solo las 59 entradas citadas, copiadas sin cambios de `fase4/extensiones/bibliografia/referencias.bib` |
| `figuras/` | Las 12 PNG usadas, copiadas de las carpetas `figuras/` de la Fase 3 y de cada extensión (prefijo `f3_`, `e1_` a `e5_`) |
| `articulo_final.pdf` | Generado con pandoc 3.1.3 (citeproc, MathML) y Chrome sin interfaz; no hay LaTeX en la máquina |
| `estilo.css` | Hoja de estilo del PDF (la de la Fase 3 más ajustes de tamaño) |

Para regenerar el PDF (desde una copia de esta carpeta con `figuras/` al lado):

```
pandoc articulo_final.md --citeproc --bibliography=referencias.bib --mathml -s --css estilo.css -o articulo_final.html
google-chrome --headless --no-sandbox --no-pdf-header-footer --print-to-pdf=articulo_final.pdf articulo_final.html
```

**Extensión.** El PDF tiene 17 páginas A4: el cuerpo (secciones 1 a 9) ocupa unas 11.5; los apéndices opcionales A (E3) y B (E5), unas 3.5, y las referencias, unas 2.5. Si el equipo deja fuera los dos apéndices, el artículo queda en unas 13.5 páginas con referencias.

## Qué entró de cada extensión

| Origen | Dónde | Qué entró |
|---|---|---|
| Fase 3 (`fase3/articulo/borrador_articulo.md`) | Secciones 2 a 4, 7 y 8 | Modelo, métodos, controles, barrido (tabla 1), cajas, δ = 1.19 y la prueba sin caja, condensados. Se aplicaron las correcciones de citas D1 a D6, D9 y D11 de `discrepancias.md` (ver abajo) |
| E1 contexto físico | Sección 1, figura 1 | Plasma (λ_D crítica, curva n_e(T), N_D), materia oscura (2/δ_c, Tulin et al. y Hulthén) y deuterón de juguete (δ_d, m_π^c, NPLQCD, sensibilidad frente a Berengut et al.), con las etiquetas ilustrativas que declara E1 (1.68 y 4.52 son etiquetas de curvas, el modelo a g fijo no es una predicción) |
| E2 cruce de cajas (aporte principal) | Sección 5, figuras 4 y 5, tablas 2 y 3 | Teoría (punto fijo 1/4 y 1/2 − 2/π², ley 1/R²), método A y B, tablas de cruces y de intervalos, mecanismo de Trotter (R2-03), término de pared en ⟨r⟩/R (R2-01, D14), prueba de artefacto en δ = 1.19 con el cruce corregido (auditoría Gemini E2-G4), controles negativos y originalidad baja a moderada (D13) |
| E4 extensión según ℓ | Sección 6, figuras 6 a 8 | Umbrales 2s, 2p, 3d; exponentes y coeficientes de E; ⟨r⟩ y ⟨r²⟩; logaritmo de la onda p; cajas para ℓ ≥ 1; integral de camino de la onda p |
| E3 otros perfiles (opcional) | Apéndice A, figura A1, tabla A1 | Tabla de umbrales, c y r_e; universalidad frente a r_e; sentido del cruce; integral de camino del ECSC; controles |
| E5 Feynman–Kac (opcional) | Apéndice B, figuras B1 a B3, tabla B1 | Teorema 1, ley de la cola (con ⟨e_k, f⟩ = 0 para l ≥ 1 y w̄₁ = δ_c/(2c)), MC libre con el pico de 3.70, puente, difusión guiada, costo y controles, en la versión posterior a la revisión R5 y a la auditoría con Gemini. Figuras copiadas después de su regeneración (22:59) |
| Todas | Sección 7.2, tabla 5 | Conteos de controles copiados de cada `controles.md` (y de la Fase 3) |

## Qué se dejó fuera y por qué

- **E1:** la comparación del radio del deuterón (1.9706 fm frente a 1.9756 ± 0.0004 fm). Usa r_n² del PDG 2024, que la verificación bibliográfica marca [no verificada]; habría que citar la tabla abierta o volver a Filin et al. También se dejaron fuera la antirresonancia s (C9 se menciona solo en la lista de controles), los detalles de Γ_e y k_BT/E_F y las figuras 02_plasma_*.png, por espacio.
- **E2:** las figuras C (⟨r⟩/R frente a δ) y D (colapso), la tabla de δ = 1.19 completa (solo se citan las cifras de R = 50) y la variante con la pared restada. Están en `E2_cruce_de_cajas/seccion_articulo.md`.
- **E3:** estado virtual (figura E3_05), tabla 2 completa (B, P), comparación con Lam y Varshni 1972 (0.7115) y la cifra de Ikhdair y Sever (1993), que E3 marca [V] pero **no está** en `bibliografia_verificada.md`; por la regla de D9 no se cita. El caso e–H (a = −9.447) se omitió porque no hay valor publicado verificado para comparar.
- **E4:** detalles de las tablas U₁, la corrección (9/5)A²/R de 2p y el método primitivo en detalle; la figura 46_energia_umbral y 46_integral_camino_l1.
- **E5:** figuras e5_01, 02, 03, 07, 08 y 09; guías que no son supersolución y el ansatz 1 + A/(r + b); el estimador de colisiones (sugerencia R5-12, no aplicada en E5).
- **Fase 3:** la figura 16 (primer gráfico, δ = 0.2), la figura de cajas 23_cajas.png, la convergencia 23_convergencia.png y la tabla detallada de la auditoría Gemini de la Fase 3 (queda en `fase3/LEEME.md`).
- **Referencias no citadas:** Debye y Hückel 1923 y PDG 2024 (r_n²) están [no verificada]. Petraki se cita solo para ξ ≳ n² (D7). Varshni 1990 se cita solo para el Hulthén (D9).

## Correcciones de citas aplicadas (D9, `bibliografia/discrepancias.md`)

| # | Corrección |
|---|---|
| D1 | D. Gebremedhin y C. Weatherford; el valor de δ_c está comprobado en el resumen de APS (se quitó "fuente secundaria") |
| D2 | El 1.19061227 ± 0.00000004 es de Gomes, Chacham y Mohallem (1994), no de Roy; "unas 3.8 veces su barra" sale de `bibliografia_verificada.md` |
| D3 | La cota 1.24305 es de Schwinger (1961) |
| D4 | Roy: *Pramana* 65, 1 (2005) |
| D5, D11 | Kole y De Raedt: *PRE* 64, 016704 (2001), cota inferior del propagador, no suavizado; Myrheim: preprint, suavizado gaussiano |
| D6 | Se añadieron Pollock y Ceperley (1984) y Ceperley (1995) para la acción de pares |
| D7 | 1.68 citado a Tulin, Yu y Zurek (2013) |
| D8 | Epelbaum et al. y Beane y Savage con año 2003 (vía `referencias.bib`) |
| D9 | "Los métodos aproximados fallan cerca de δ_c" ya no se atribuye a Varshni 1990; Varshni 1990 queda para el Hulthén |
| D12, D29 | Edwards et al. 2019 citado como *Ann. Phys.* 411, 167966 |
| D13, D26 | Roy "2019" de E3 se cita como Roy 2016 (*IJQC* 116, 953) |
| D20 | CODATA 2022 (Mohr et al. 2025) |
| D25 | ECSC citado a Lam y Varshni 1972 |
| D28, D30 | Cranston 109–112 (no se cita en el texto); Ciesielski y Taylor 103, 434 (vía `referencias.bib`) |
| — | Serra, "spatial finite size scaling": se cita como manuscrito [V-doc]; la revista (*Phys. Lett. A* 303, 20) no está verificada |

## Procedencia de las cifras

Ninguna cifra se escribió a mano: todas están copiadas de los textos generados desde los JSON (secciones, LEEME y controles de cada extensión) o de la bibliografía verificada. La tabla dice de dónde sale cada grupo.

| Cifras | Texto del que se copiaron | JSON de origen |
|---|---|---|
| Fase 3: convergencia, barrido (tabla 1), A = 0.7411, B = 0.059, ⟨r⟩κ | `fase3/articulo/borrador_articulo.md` | `fase3/resultados/21_barrido.json`, `22_convergencia.json` |
| Fase 3: cajas, δ = 1.19, R = 6400 y 12800, cruces R_c(h), a_s sin caja | ídem | `20_cajas.json`, `20c_umbral_119_fino.json`, `26_transferencia_grande.json`, `25_respuesta_gemini.json` |
| Fase 3: 34 controles (23/3/8) | ídem | `24_tabla_controles.json` |
| E1: λ_D^c, n_e(T), N_D, 2/δ_c, Hulthén, δ_d, g/ħc, m_π^c, NPLQCD, sensibilidades | `E1/seccion_articulo.md`, `LEEME.md` | `E1/resultados/02_plasma.json`, `03_materia_oscura.json`, `04_deuteron.json`; controles en `06_verificacion.json` y `controles.md` |
| E2: r_e, c, α, β, α_ρ, c_w, corrimiento de pared | `E2/seccion_articulo.md` | `E2/resultados/01_teoria.json` |
| E2: tabla 2 (cruces), cocientes 4.125… , diferencias B menos disparo | ídem | `05_cruces.json` |
| E2: tabla 3 (intervalos A, B, radial, disparo; R ≤ 800) | ídem; comprobado contra `05_cruces.json` (`fuentes/*/extrapolacion/ajuste_ab/delta_c`, `barra_total`, `transferencia_metodo_B/*`) | `05_cruces.json` (versión de las 22:45 con el término de pared de `04b_pared_rho.json`) |
| E2: barras de ⟨r⟩/R antes y después del término de pared (1.47e-5 a 1.57e-5; 6.04e-5 a 6.93e-5) | ídem | `05_cruces.json` (`extrapolacion_sin_pared_R2_01`, `sin_pared_A`) |
| E2: s_ε = 6.1e-4, 1.53e-4, 3.8e-5 | ídem | `revision/resultados/r04_mecanismo_trotter.json` |
| E2: δ = 1.19 (E₀ en R = 50, y = 0.2544 frente a 0.2589, cruces corregidos 1.1906131 y 1.1905372) | ídem | `06_artefacto.json`, `13_cruce_corregido.json` |
| E2: 27 de 31 controles | `E2/controles.md` | `07_controles.json` |
| E4: umbrales, exponentes, c₀, S, ⟨r⟩κ, A², 5A²/4, ⟨r⟩ y ⟨r²⟩ de 3d, pendiente 6.597, error 2.3e-7 | `E4/seccion_articulo.md` | `E4/resultados/40_controles_radial_l.json`, `40b_umbral_fd.json`, `41_constantes_umbral.json`, `42_barridos.json` |
| E4: cajas (0.25017, Y = 1.0047 y 1.00007, radios con R = 100) | ídem | `43_cajas_l.json` |
| E4: integral de camino ℓ = 1 (−1/8 + 5e-11, órdenes 2.00, 1.61, 1.34 a 1.37) | ídem | `45_transferencia_l1.json`, `44_tablas_l1.json` |
| E4: 129 controles (105/16/8) | `E4/controles.md` | `47_tabla_controles.json` |
| E3: término de segundo orden ¼(1 + r_e/R + ¾ r_e²/R²) y acuerdo a 2e-10 | `E3/seccion_articulo.md` regenerado tras la auditoría (E3-G4) | `04_cajas_universalidad.json` |
| E3: tabla A1, pendientes de ⟨r⟩κ, valores de caja en R = 1600, ECSC por integral de camino | `E3/seccion_articulo.md`, `LEEME.md` | `E3/resultados/01_umbrales.json`, `02_dispersion.json`, `03_ligados_virtuales.json`, `04_cajas_universalidad.json`, `05_transferencia_ecsc.json` |
| E3: 32 controles (29/2/1) | `E3/controles.md` | `08_tabla.json` |
| E5: κ̂, θ, a(3), a(4), tabla B1, costo, varianzas | `E5/seccion_articulo.md` y `LEEME.md` (versión posterior a R5) | `E5/resultados/01_referencia_edo.json`, `02_validacion_mc.json`, `03_colas.json`, `04_importancia.json`, `04b_extrapolacion.json`, `05_cerca_umbral.json` |
| E5: w̄₁ medido 0.8031743448462 (ley exacta) y predicho δ_c/(2c) = 0.8031743448459 con c = 0.7411917653 | apéndice B (diferencia 3e-13) | `E5/resultados/03_colas.json` (`amplitud/wbar1`); `E3/resultados/02_dispersion.json` (`perfiles/yukawa/c_HF`) |
| E5: pico 3.70 en n ≈ 9.4e5, 1.25 al final, pendiente +0.78 | `E5/LEEME.md` | `03_colas.json` |
| E5: 43 controles (34/4/1 n. a./4 inf.) | `E5/controles.md` | `07_controles.json` |
| Diferencia con Edwards et al. 2017 (2.106e-7, 421 barras) | calculada en este borrador | (aritmética sobre 1.1906124210606 y 1.1906122105(5)) |
| Literatura: 1.19061227(4), 1.1906122105(5), 1.1906124207(2), 1.1906124210606177…, 0.83991, 1.68, 86 referencias (75/5/4/2) | `bibliografia/bibliografia_verificada.md` | (fuentes externas verificadas) |

## Cambios tras la auditoría con Gemini (17-11-2026)

- Apéndice A: la corrección del punto fijo se escribe como 2R²E₀/π² = ¼(1 + r_e/R + ¾ r_e²/R²), con la forma del `seccion_articulo.md` regenerado de E3.
- Apéndice B: ⟨e_k, f⟩ = 0 explica por qué no cuentan los estados con l ≥ 1; se añade w̄₁ = δ_c/(2c) = 0.803174 frente a 0.80317 de la ley exacta; nueva figura B2 (e5_05 regenerada, pico de 3.70); e5_04 y e5_06 se volvieron a copiar de su versión regenerada.
- E2: el cruce corregido (1.1906131 con el disparo y 1.1905372 con la integral de camino, par 50/100) se comprobó contra `13_cruce_corregido.json` y no cambia.
- Sección 9: el párrafo de la auditoría con Gemini resume los cinco chats (2 o 3 rondas, sin ejecutar código), lo aceptado y lo refutado; la fila F4-ART-01 de la bitácora lo registra.

## Pendientes

1. ~~Auditoría externa con Gemini de E5.~~ **Resuelto:** terminó (`auditoria_gemini/LEEME.md`, 2 rondas, 3 hallazgos y 1 retirado). Se incorporaron al apéndice B: la causa de que los estados con l ≥ 1 no cuenten (⟨e_k, f⟩ = 0 porque f = q^{1/2} es radial; no depende del punto de partida, ver `E5/teoria.md` sec. 5), la forma cerrada w̄₁ = δ_c/(2c) = 0.803174 (mejora que el coordinador decidió aplicar) y la figura e5_05 regenerada, con la anotación del pico de 3.70. La revisión R5 también terminó y está incorporada.
2. **Decisión del equipo** sobre los apéndices A (E3) y B (E5), y revisión de las decisiones D1 a D15.
3. **Atribución de β = −ζ(1/2)/√(2π)** para la pared sin imagen: sigue pendiente desde la Fase 3.
4. **Lectura de originales** que solo se conocen por resumen o por terceros: Klaus y Simon (1980), Lam y Varshni (1971), Bethe (1949), Zhao (1992), Singh y Varshni (1983, cifra citada por Roy), Nasser et al. (2011).
5. ~~Valor de Edwards et al. (2017).~~ **Resuelto (decisión del coordinador):** la sección 7.1 lo discute junto a la tabla 4. Queda $2.106\times10^{-7}$ por debajo de 1.1906124210606, unas 421 veces su barra declarada ($5\times10^{-10}$). Calculé la diferencia con aritmética decimal exacta: 2.105606e-7, que es 421.1 barras. Se reporta como discrepante, sin afirmar la causa.
6. **Revista del trabajo de Serra** (*Phys. Lett. A* 303, 20 (2002)): sin verificar en el editor; se cita como manuscrito.
7. ~~Bitácora de IA.~~ **Resuelto:** la entrada F4-ART-01 está al final de la sección 9, en el formato del curso. No había bitácora propia en `articulo_final/`, así que no hubo otro archivo que actualizar.
