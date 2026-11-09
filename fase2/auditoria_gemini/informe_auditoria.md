# Informe de la auditoría externa de la Fase 2 (Gemini, por puntos)

5 de noviembre de 2026 · Auditora: Gemini (API de Google AI Studio, capa gratuita) · Respuestas de los autores: Claude · **Las decisiones son del equipo; nada de esto está aplicado todavía a la bitácora.**

## Cómo se hizo

- La Fase 2 se partió en 10 puntos. Cada uno fue una **conversación nueva**: Gemini solo vio el material de ese punto (sección, scripts, salida impresa) y no supo que hubo otras revisiones.
- El encargo fue la plantilla de `fuentes_control/auditor_otra_ia.md`. Gemini tenía Python para recalcular con código propio.
- Por cada hallazgo, Claude lo comprobó contra los archivos (y, cuando hacía falta, calculando) y respondió. Hubo de 2 a 4 rondas por punto y luego una tabla final.
- Los prompts, las respuestas y el código que ejecutó Gemini quedaron literales en `conversaciones/<punto>.md`. Las respuestas de los autores están en `respuestas/`.

**Modelos (anotar en el registro de IA).** Gemini Pro no tiene cuota en la capa gratuita (límite 0), así que se usó Flash, que permite 20 consultas al día por modelo:
- `gemini-3.6-flash` (alias `gemini-3.5-flash`): P10, P13, P14, P15, PT y PF.
- `gemini-3-flash-preview`: P11, P12, P16 y PD.

El segundo modelo es claramente más flojo: en P16 no ejecutó código y en las tablas de cierre tiende a dar todo por "resuelto".

## Resultado en una línea

Gemini **no encontró ningún error de física ni de signo** que cambie un resultado de la Fase 2. Rehízo con código propio, entre otros:
- $\delta_c = 1.1906124210606$;
- $E_0(\delta=0.2)$ por disparo, a $3\times10^{-14}$ de la referencia;
- $U_C$ en 7 cifras;
- el orden $h^4$ del residuo de Richardson;
- el $\chi^2 = 11.26$ ($p = 0.010$) de $\tau=5$;
- el conteo 88/70/9/9 de la tabla.

Sí encontró **errores de documento**, una **discrepancia con una fuente** y una **fragilidad de código**. Lo más útil está en la sección siguiente.

## Lo que hay que corregir (propuestas, para que el equipo decida)

| # | Qué | Dónde | Origen | Verificado por Claude |
|---|---|---|---|---|
| 1 | El resumen dice "21 criterios pasan, 0 fallan", pero B3b falla en $V_0=1.3$ (+2.2e−5). Debe decir 22 pasan, 1 no pasa y 5 medidos. | `secciones/13_controles_hulthen_pozo.md`, línea 9 | P13 H1 | Sí: línea 9 frente a 13.6 y el JSON |
| 2 | **Roy (H9) cita $\delta_c(1s) = 1.19061227 \pm 4\times10^{-8}$, y el nuestro es 1.1906124211.** La diferencia es de $1.5\times10^{-7}$, casi 4 veces la incertidumbre que da Roy. Gemini recalculó 1.190612421061, y Claude lo volvió a calcular con un código aparte (DOP853, `rtol` 1e−13, $R=300$): 1.1906124210606. Conviene una nota en la fila H9: la cifra citada no coincide con la nuestra. | `fuentes_control/fuentes_control.md`, fila H9 | PF H2 | Sí, recalculado |
| 3 | La errata −3.08e−5 (debe ser −3.07e−5, en δ=1.18, R=400) también está copiada en la tabla de cajas de las fuentes, no solo en la 9.6 de la Fase 1. | `fuentes_control.md`, línea 117 | P10 H2 (Claude la encontró al responder) | Sí |
| 4 | En `todos()`, `all([])` da `True`: si un prefijo no encuentra filas, la fila sale "sí" sin nada medido. **Hoy no pasa en ninguna fila**: Claude revisó los 13 prefijos y todos encuentran entre 1 y 9 criterios. Conviene lanzar un error si la lista sale vacía. | `codigo/16_tabla_controles.py`, línea 36 | PT H1 | Sí, se ejecutó el generador sin escribir archivos |
| 5 | En la tabla de la Parte VI, L02 y L15 dicen "Fuente: 15_limites.py", pero sus cifras salen de `11_transferencia_controles.py`. Hay que citar el script 11 en esas filas. | `bitacora_fase2.md`, Parte VI | P15 H1 | Sí |
| 6 | L05: la diferencia de $5.6\times10^{-6}$ es casi toda de la derivada numérica. Con el paso mitad (ya está en el JSON) baja a $1.4\times10^{-6}$, y con Richardson en $\Delta\delta$ queda $<10^{-9}$. Conviene reportar el valor extrapolado. | Parte VI, fila L05 | P15 H3 | Paso mitad sí (JSON); el Richardson es de Gemini, cuadra con el JSON |
| 7 | Pozo en $V_0=1.3$: si el ajuste $\epsilon^{3/2}$ se restringe a $\epsilon\le0.05$, el error baja de $+2.2\times10^{-5}$ a $+7.2\times10^{-7}$ (con exponente libre, $-4.2\times10^{-7}$). Esto sirve para la decisión 4, pero elegir el rango después de ver el dato es justo lo que hay que declarar. | sección 13.3, decisión 4 | P13 H4 | Cálculo de Gemini, no repetido |
| 8 | La sección 10 no remite a ninguna fuente externa. Basta una línea que apunte a `fuentes_control.md` y a la Fase 1. | sección 10 | P10 H1 | Sí |
| 9 | En $\delta=0.2$, la tabla 1 de 13 da un orden de Hulthén de 1.38 que no es un orden. Hay que añadir la nota en la tabla misma. | sección 13.2 | P13 H3 | Ya lo dice el texto |
| 10 | Notas menores. En la sección 2.1 de las fuentes, Hulthén y Yukawa comparten el $-1/r$, pero sus constantes en el origen son distintas ($+\delta/2$ frente a $+\delta$). La fórmula de $A(\delta)$ del 2s solo vale para $\delta<0.5$. | `fuentes_control.md` | PF F1 y F4 | Sí (desarrollo en serie) |

## Lo que sigue abierto (no lo resolvió la auditoría)

- **$\tau=5$ en el PIGS (decisión 2).** Gemini reprodujo $\chi^2 = 11.26$ con 3 g.l. ($p = 0.010$). Primero propuso "errores subestimados" o "termalización". Claude le mostró que, en esa corrida, el error por bloques y el error entre cadenas coinciden (cociente 1.007), con $\tau_{\rm int}\approx5$ y $3\times10^4$ barridos, y Gemini aceptó la lectura del material: dispersión entre corridas con $p\approx1\%$ y causa no identificada. Una de las conversaciones (P16) llegó a proponer descartar la corrida original, y se rechazó porque eso sesga el resultado.
- **Umbral 0.1 de la ley de caja (decisión 3).** Gemini propuso como criterio "a priori" exigir $R_3 > 5|a_s|$. Es razonable, pero lo propuso conociendo ya $a_s=-142.93$, y 800 apenas supera $5|a_s|=715$. La pregunta de por qué 5 quedó para la próxima ronda (ver "Pendiente").
- **Ley $\epsilon^{3/2}$ del pozo.** Gemini dio una explicación heurística: una capa de anchura $\sqrt\epsilon$ en el salto, que da un error $\epsilon\cdot\sqrt\epsilon$ por paso. Es plausible, pero **no es una demostración y no tiene fuente**.
- **Condición (c) de las cajas.** La compatibilidad 15/15 usa una corrección de pared calculada con el radial. Los veredictos (ligado o no ligado) no dependen de ella, y Gemini lo comprobó con $p=2$ y $p=4$.

## Cuidado con las referencias que dio Gemini

Gemini no tenía internet. Aun así, varias veces marcó como "confirmado" o "verificado" algo que salía de su memoria. Cuando se le insistió, lo retiró o lo pasó a "no verificado". **Ninguna de estas citas debe entrar a la bitácora sin revisarla contra la fuente:**

- "Hulthén 1935" (lo retiró), "pp. 1–12" para Ark. Mat. Astron. Fys. 28A (no verificado).
- Que β = 0.5826 venga de "Spitzer 1957", "Barker 1971" o "Milne/Spitzer" (atribución de memoria; el proyecto lo atribuye a Broadie, Glasserman y Kou). El valor numérico $-\zeta(1/2)/\sqrt{2\pi}$ sí lo calculó.
- Broadie, Glasserman y Kou, *Math. Finance* 7(4), 325–349 (1997). Coincide con lo que se conoce, pero es de memoria.
- "Hansen & Ostermann, SIAM J. Numer. Anal. 37, 2009" y "Descombes & Schatzman, Math. Comp. 71, 2002" para el $\epsilon^{3/2}$. El volumen 37 de esa revista no es de 2009, y Gemini las pasó a NO VERIFICADAS.
- "del Valle & Nader (2019)" como fuente de 1.1906124211. Hay que preguntarlo; probablemente no existe así.
- Revistas para las referencias que solo están en arXiv (H9 *Pramana* 2014, H10 *Int. J. Quantum Chem.* 2018, P1 *Am. J. Phys.* 2013, etc.). Todas son de memoria. **No se pudieron comprobar desde aquí** porque la red bloquea arXiv. Siguen como "revista NO confirmada".
- Sokal 1997 (NATO ASI 361, Plenum, pp. 131–192), Ceperley RMP 67, 279 (1995), Pollock y Ceperley PRB 30, 2555 (1984), Sarsa, Schmidt y Magro JCP 113, 1366 (2000). Coinciden con lo que se conoce, pero son de memoria: hay que verificarlas con el DOI.
- En PD dijo que Cai, Cai e Inomata (1986) es "para el núcleo de Coulomb exacto". Es un error: ese artículo trata la integral de camino de **Hulthén**.

Otra cosa que conviene saber: en P10, Gemini reportó primero un orden $h^4$ para Yukawa usando solo los datos de Hulthén, y su propia corrida de Yukawa no lo respaldaba (las razones salían 17, 70 y 0.19). Al pedírselo, lo rehízo con una referencia mejor y salió $p=4.00$. **Por eso cada hallazgo y cada "confirmado" se comprobó antes de aceptarlo.**

## Estado por punto

| Punto | Material | Modelo | Rondas | Hallazgos (gravedad) | Estado |
|---|---|---|---|---|---|
| P10 | Solucionador radial | 3.6-flash | 3 + cierre | 4 (3 bajas, 1 media) | Cerrado, todos resueltos |
| P11 | Acción de pares y transferencia | 3-flash-preview | 3 + cierre | 5 (sin errores de fondo; $U_C$ en 7 cifras) | Cerrado |
| P12 | PIGS y $\tau=5$ | 3-flash-preview | 3 + cierre | 5; la cita de Sokal queda pendiente | Cerrado |
| P13 | Hulthén y pozo | 3.6-flash | 3 | 4; el H1 es un error real del resumen | Cerrado en la ronda 3 (falta la tabla formal) |
| P14 | Criterio de cajas | 3.6-flash | 2 | 4; está pendiente la ronda sobre BGK y $5\lvert a_s\rvert$ | **Pendiente** de una ronda |
| P15 | Límites L01–L19 | 3.6-flash | 2 | 3; aceptó las exclusiones de L01, L10, L11, L13 y L17 | Respondido (falta la tabla formal) |
| P16 | Primer gráfico | 3-flash-preview | 3 + cierre | 5; retiró 2 (H1 y H3) | Cerrado |
| PT | Tabla de controles | 3.6-flash | 2 | 5; conteo 88/70/9/9 confirmado | Cerrado en la ronda 2 |
| PD | Las 10 decisiones | 3-flash-preview | 2 + cierre | 5; "recomienda firmar" | Cerrado |
| PF | Fuentes de control | 3.6-flash | 2 + cierre | 4; F2 (Roy) es el más importante | Cerrado |

**Pendiente:** cuando se renueve la cuota, mandar `respuestas/P14_r3.md` y pedir las tablas de cierre de P14, P15 y PT. Este informe se actualiza con eso.

## Segunda pasada con Gemini Pro (app web, 5-11-2026, modelo "3.1 Pro")

Se hizo en la app gemini.google.com desde el Chrome de Lucho. Cada punto se envió como archivo adjunto en un chat nuevo. Las transcripciones literales están en la PC, en `InvTeorica\auditoria_gemini_pro\conversaciones\`, y el resumen en `resumen_pro.md`, en la misma carpeta.

**Ojo: en la app, Gemini Pro no ejecuta código.** En P11 mostró una "salida de ejecución" escrita a mano y lo admitió cuando se le señaló. Todos sus números son cálculos a mano.

**Estado.** Los 10 puntos están auditados con Pro: P11, P12 y P16 el 5-11, y el resto el 9-11, enviando el material en trozos de hasta 15 KB y pidiendo los hallazgos por etapas.

**Hallazgos nuevos (comprobados contra el material):**
- **P12, gravedad media.** La frase "no hay indicio de sesgo del muestreador" (12.4) y la opción propuesta en la decisión 2 son más fuertes de lo que permiten p = 0.011 y p = 0.004.
- **P12, desajustes del documento:** 9 pruebas frente a 14; 161 s frente a 135.8 s; "10/11 criterios" frente a una tabla de 13 filas; y el ⟨r²⟩ con Richardson del texto, que no aparece en la salida impresa (solo se imprime h = 0.02).
- **P16, gravedad baja:**
  - los PIGS se dibujan en ε = 0.112 y las réplicas en τ = 5.5 y 6.0 sin decirlo;
  - las huellas sha256 dependen de `os.listdir`, así que incluyen la figura 18;
  - la etiqueta de la transferencia cambia entre paneles.
- **P11, gravedad baja:**
  - cifras desincronizadas (27 s frente a 23.7 s; E₁ −0.012107 frente a −0.012106; dos redondeos);
  - el residuo de 8.1e−9 de Wigner-Kirkwood se explica con el término ε³ (da 8.04e−9), pero los coeficientes son de memoria.

**Lo que retiró al discutírselo:** una "raíz exacta" falsa del pozo; que U_C diverge en el origen; el "principio variacional" del PIGS; y "acción primitiva".

**Referencias dudosas (todas de memoria):**
- −ζ(1/2)/√(2π) atribuido a "Chernoff";
- los coeficientes de Wigner-Kirkwood;
- Madras y Sokal, J. Stat. Phys. 50, 109–186 (1988);
- Sokal 1997 (dijo primero Springer y después "probablemente Plenum").

**Hallazgos nuevos del 9-11:**
- **PT, el más importante para la firma.** Seis filas están repetidas, con el mismo valor, entre los bloques A y D: A22–A27 son D2–D6 y D21 (Hellmann-Feynman, virial, cotas y L19). Lo comprobé en la tabla. Son 82 controles distintos, no 88: 64 pasan, 9 no pasan y 9 son medidos. Hay que corregir el resumen o quitar el duplicado.
- **P13.** B3b no está en `CRIT_DECL`; su criterio está escrito a mano en el código. Además, la cabecera dice 110 s y la salida, 132.5 s.
- **P14.** La cabecera dice 95 s y la salida, 101 s.
- **P15.** L18 tampoco sale de `15_limites.py`, igual que L02 y L15.
- **P10, fragilidades latentes.** $F_{1/2}$ pierde el orden si $R/2$ no cae en un nodo, y `caja_recomendada` devuelve inf si $E\ge0$. Además, lo que el texto llama "exacto" en $\delta=0.2$ es la referencia de V1, no un resultado analítico.
- **PF.** El año de H8 no cuadra: el arXiv es de 2001 y la revista, de 2000. Hay que verificarlo.
- **PD.** El umbral 0.1 de la decisión 3 se fijó conociendo ya los datos de la Fase 2. Para la decisión 2, Gemini propone una redacción neutral: hay heterogeneidad con $p=0.011$ y la causa sigue abierta.

**Más referencias dudosas del 9-11:**
- "Broadbridge/Bouchaud" como origen de $\zeta(1/2)$: probablemente falsa.
- Siegmund 1985 y Chernoff 1965.
- "Makri / J. Math. Phys." y "Jiao, Ho, Roy": demasiado vagas para citar.
- "J. Math. Phys." para Cai, Cai e Inomata: falsa. La revista es Phys. Rev. A 34, 4621, y Gemini la retiró.

El resumen completo, con 10 propuestas para el equipo, está en la PC en `InvTeorica\auditoria_gemini_pro\resumen_pro.md`.

## Para el registro de IA (ficha sugerida)

| Campo | Valor |
|---|---|
| ID | A-02 a A-11 (un punto por ficha, o una ficha con la tabla de arriba) |
| Fecha | 05-11-2026 |
| IA auditora | Gemini `gemini-3.6-flash` y `gemini-3-flash-preview`, API de Google AI Studio (capa gratuita), con ejecución de código |
| Material auditado | Ver "Estado por punto"; la lista exacta de archivos de cada punto está en `PUNTOS` de `auditar.py` |
| Consulta | Literal en `conversaciones/<punto>.md` (instrucción de sistema, prompt y cada ronda) |
| Respuesta utilizada | Tabla "Lo que hay que corregir", filas 1 a 10 |
| Comprobación | Columna "Verificado por Claude"; δ_c recalculado con código aparte |
| Decisión humana | **Pendiente** (Lucho y Juan Sebastián) |
| Corrección posterior | Ninguna aplicada todavía |
