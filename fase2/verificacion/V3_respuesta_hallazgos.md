# V3. Respuesta a los hallazgos de la verificación (V1 y V2) de la Fase 2

**Proyecto 05, umbral de ligadura del 1s en $V=-e^{-\delta r}/r$** · Fase 2 · 27-10-2026
Hecho por Claude (agente del flujo de trabajo pedido por Lucho). Equipo: Juan Sebastián Calixto (verificación) y Luis Felipe Ramírez (implementación). Esta respuesta **no sustituye** la firma de Juan Sebastián.

Método: cada hallazgo se reprodujo primero con un cálculo propio. Si era real, se corrigió el código o el texto, se volvieron a ejecutar los scripts afectados y las pruebas, y se actualizaron los JSON y las secciones. No se cambió ninguna tolerancia para que un criterio pase. Antes de tocar nada se copiaron código, resultados, figuras y secciones a `fase2/resultados/archivo_pre_V3/`; las cifras "antes" salen de esa copia y las "después" de los JSON nuevos.

## Qué se volvió a ejecutar

| Script | Tiempo | Resultado tras V3 |
|---|---|---|
| `test_radial.py` | 3.7 s | 7/7 (la prueba 3 tiene un control más) |
| `test_transferencia.py` | (no medido) | 7/7 (antes 5; nuevas: `test_extremos_wk`, `test_aviso_pared`) |
| `test_pigs.py` | ~35 s (histograma 31 s) | 14/14 (antes 9) |
| `10_radial_controles.py` | 5.4 s | `cajas_9_6` y `yukawa_0.2/R40` idénticos a antes |
| `11_transferencia_controles.py` | 24 s | 28/35, igual que antes (mismos 7 fallos) |
| `12_pigs_produccion.py` | 9.3 min, 4 procesos | Monte Carlo idéntico bit a bit; 10/11 |
| `12b_pigs_replica_tau5.py` | 136 s | idéntico (+0.03σ) |
| `12c_pigs_coulomb_tau5.py` (nuevo) | 219 s, 4 procesos | 6 de 6 criterios pasan; 1 informativo |
| `13_controles_hulthen_pozo.py` | 133 s, 3 procesos | 22 pasan, 1 no pasa (B3b, nuevo), 5 medidos |
| `14_criterio_cajas.py` | 101 s | mismos veredictos; criterio estricto 15/15 con pared |
| `15_limites.py` (nuevo) | 26 s | 19 pasan, 1 no pasa (L16), 1 medido |
| `16_tabla_controles.py` (nuevo) | <1 s | `secciones/15_tabla_controles.md`: 88 filas, 70 pasan, 9 no pasan, 9 medidas |

Salidas en `fase2/verificacion/*_salida.txt`. Ningún proceso pasó de 4 a la vez.

## Tabla de respuesta

| id | de | gravedad | ¿reproducido? | decisión | qué cambió | antes → después |
|---|---|---|---|---|---|---|
| H1 | V1 | media | **sí** | corregido | `14_criterio_cajas.py`: el error de la transferencia suma el sesgo de pared estimado con el radial, $|{\rm ext}_{\epsilon^2}[E_{\rm rad}(R+0.5826\sqrt\epsilon)-E_{\rm rad}(R)]|$; nuevas claves `err_sin_pared`, `sesgo_pared_extrapolado`, `dif_rad_corregida_pared`, `V3_criterio_estricto`. Texto de 14.4 corregido | Criterio $|{\rm dif}|\le{\rm err}_{\rm tr}$: antes fallaba en 11/15 (radial del proyecto). Tras Wigner-Kirkwood y sin pared: falla en 9/15 (las mismas 9 de V1). Con el término de pared: **15/15**. Diferencia corregida por la pared: $\le2.1\times10^{-7}$ en $R=50$, $\le8.1\times10^{-9}$ en $R\ge200$. Veredictos iguales |
| H2 | V1 | media | **sí** | corregido en parte | `13_controles_hulthen_pozo.py`: pozo con $h=0.005$ (Cholesky en banda como inverso), $E_{h0}$ con 0.02/0.01/0.005; se guarda el anterior; nuevo criterio B3b (ajuste $\epsilon^{3/2}$ a 5 puntos), fijado antes de ejecutar | $V_0=2$: $E_{h0}$ nuevo − anterior $=-0.86,-1.60,-1.70,-1.34,-0.84\times10^{-5}$ (V1, continuo: $-1.15$ a $-2.42\times10^{-5}$): **no estaba convergido** y aún no lo está del todo. B3: $+6.2\times10^{-6}\to+3.6\times10^{-6}$ ($V_0=2$), $-2.6\times10^{-7}\to-4.2\times10^{-7}$ ($V_0=1.3$): pasa. Ajuste a 5 puntos: $+1.47\times10^{-5}\to+9.7\times10^{-7}$ ($V_0=2$); $+2.1\times10^{-5}\to+2.2\times10^{-5}$ ($V_0=1.3$): **B3b no pasa** en $V_0=1.3$. Borde estricto: $-2.0\times10^{-3}\to-1.2\times10^{-4}$ ($V_0=1.3$) y $-1.1\times10^{-4}\to-2.5\times10^{-5}$ ($V_0=2$): era error de Nyström, como dijo V1. Que los dos bordes tengan el mismo límite **no** queda probado con estas mallas (aún difieren $2$–$3\times10^{-5}$ y $\sim10^{-4}$). Órdenes en ε: 1.497, 1.499, 1.502 (V1: 1.497, 1.498, 1.499) |
| H3 | V1 | baja | **sí** | corregido | `pares.U_extremos`: término de Wigner-Kirkwood (ver H2 de V2) | $\delta=1.0$, $R=174$: $E(\epsilon)$ sube $+1.5\times10^{-7}$, $+5.0\times10^{-8}$, $+1.7\times10^{-8}$ (V1 midió $-1.44$, $-0.49$, $-0.17\times10^{-7}$ con el núcleo exacto: mismo tamaño). Extrapolado $-1.8\times10^{-8}\to-1.2\times10^{-8}$. Hulthén 1.5: $-3.3\times10^{-9}\to-1.8\times10^{-9}$. Residuo de volumen $\delta=1.15$, $R\ge200$: $-1.8\times10^{-8}\to-8.1\times10^{-9}$ |
| H4 | V1 | baja | **sí** | corregido (se reporta el fallo) | `10_radial_controles.py` calcula la referencia fina (Richardson hasta $h=1/320$); `test_radial.py` añade la prueba con $h=1/80$ frente al exacto. **No** se cambió la tolerancia | Fina: $-0.3268085113851$ (a $1.6\times10^{-11}$ de V1). Error con $h=1/40,1/80$: $6.2\times10^{-9}$ → el criterio de 5e-9 **no pasa** frente al exacto (solo frente a la referencia redondeada). Con $h=1/80,1/160$: $4.0\times10^{-10}$, pasa |
| H5 | V1 | baja | **sí** | pendiente (decisión) | Segunda réplica de τ = 5 (16 cadenas, semillas 20262070–85) y combinación en `12c` | Réplica 2: +0.99σ. Producción −3.19σ, réplica 1 +0.03σ; χ² de las 3 corridas 11.13/3 (p = 0.011). 40 cadenas: −0.83σ (ponderada), −0.61σ (iguales); χ² por cadena 50.2/39 (p = 0.11); 20/40 por debajo. Con la auditoría V2: 64 cadenas, −0.97σ. La combinación no muestra sesgo; la producción sigue en la cola. Decide Juan Sebastián |
| H6 | V1 | baja | **sí** | corregido | `11_transferencia_controles.py`: $u'(0)=\lim u/r$ por ajuste cúbico de $u/r$ en 6 nodos | $u'(0)^2$: 3.9502 → 3.99992 (exacto 4); 3.7560 → 3.80321 (V1: 3.8033); 0.91752 → 0.92904 (V1: 0.92913). Cociente: 4.05, 4.04, $3.91\times10^{-8}$ → 4.00, 3.99, $3.86\times10^{-8}$ |
| H7 | V1 | baja | **sí** | corregido (texto + cálculo) | Script 11 calcula $E_0(T)$ y el límite del mixto también con $h=0.04$ y Richardson $h^4$ (`proyeccion/V3_malla`); texto de 11.5 | Límite − $E_0(T)$: $-1.05\times10^{-7}$ ($h=0.02$), $-1.67\times10^{-6}$ ($h=0.04$), **$-1.3\times10^{-9}$** (Richardson). $E_0(T)$ con $h=0.02$ está $+1.01\times10^{-7}$ sobre su extrapolado; el límite del mixto se mueve $2.9\times10^{-9}$ |
| H1 | V2 | media | **sí** | corregido | Igual que H1 de V1 | Ver H1 de V1 |
| H2 | V2 | media | **sí** | corregido | `pares.U_extremos(a, b, eps, wk=True)`: $+\frac{V_C''(m)}{12}[\epsilon^2-\epsilon(a-b)^2]$, $m=(a+b)/2$; `pigs.interpolador` bilineal usa la misma función; docstrings de `pares.py` y `transferencia.py` y sección 11.1 corregidos; prueba `test_extremos_wk` | Tabla − aproximación en $r=r'=9$, $\epsilon=0.1$: $-2.29\times10^{-6}$ (igual a $-\epsilon^2/6r^3$) → $8.1\times10^{-9}$; con $\epsilon=0.2$: $9.2\times10^{-6}\to6.5\times10^{-8}$. Efecto en energías: ver H3 de V1 y H1. PIGS δ = 0.2: series idénticas bit a bit |
| H3 | V2 | media | **sí** | corregido (aviso); la imagen en $R$ queda pendiente | `transferencia.sesgo_pared` y `resolver(..., aviso_pared=True)`: estima $\Delta E\approx-\beta\sqrt\epsilon\,u'(R)^2/2$ con $u'$ a $2\sqrt\epsilon$ de la pared, lo guarda como `sesgo_pared_est` y lanza `RuntimeWarning` si supera $\min(10^{-7},10^{-3}|E_0|)$; prueba `test_aviso_pared`. No se cambió el núcleo | δ = 0.2, ε = 0.1: $R=2$: −0.0376 frente a +0.0589 (radial), aviso; $R=5$: sesgo real $-1.08\times10^{-3}$, estimado $-1.31\times10^{-3}$, aviso; $R=10$: $-5.5\times10^{-7}$ frente a $-7.2\times10^{-7}$, aviso; $R=40$: sin aviso. δ = 1.18, $R=50$: $-3.22\times10^{-6}$ frente a $-3.20\times10^{-6}$ |
| H4 | V2 | media | sí (faltan) | en parte: tabla hecha; firma, presentación y bitácora pendientes | `secciones/15_tabla_controles.md` (generada por `16_tabla_controles.py`) con lista de figuras congeladas (sha256) y las 6 decisiones por firmar | `presentacion/` sigue vacía; no hay bitácora de IA consolidada de la Fase 2 (los registros están en cada sección y aquí). La firma es de Juan Sebastián |
| H5 | V2 | baja | sí (no estaban) | corregido | `15_limites.py` (nuevo): L03, L04, L05, L06, L07, L08, L09, L12, L14, L16, L19 con la transferencia | L04 0 violaciones; L05 dif $+5.6\times10^{-6}$, $+2.7\times10^{-6}$, $+1.3\times10^{-6}$ (δ = 0.2, 0.5, 1.0; con paso mitad $1.4\times10^{-6}$ en 0.2: es error de la derivada numérica); L06 $-1.33\times10^{-4}$ ($h=0.02$) → $-3.8\times10^{-5}$ ($h=0.01$), orden 2.00, extrapolado $-5.9\times10^{-7}$; L09 sin nodos. V2 dio $2.2\times10^{-7}$ en HF con otra derivada |
| H6 | V2 | baja | sí | pendiente (decisión) | Igual que H5 de V1 | Ver H5 de V1 |
| H7 | V2 | baja | **sí** | corregido | Sección 12 dice que el control es tautológico; `12c` (A): Coulomb con 8 cadenas y histograma | ⟨r⟩ 1.49027 ± 0.00720 (−1.35σ), ⟨r²⟩ 2.96787 ± 0.03430 (−0.94σ); histograma χ² 57.7/32, **p = 0.004** (pasa p > 10⁻³ por poco) |
| H8 | V2 | baja | **sí** | corregido | `pigs.cadena` lanza `ValueError` si τ/ε no es entero múltiplo de L; guarda `tau_ef` | τ = 2.5, ε = 0.2: antes M = 10 en silencio; ahora error "tau/eps = 12.5 debe ser un entero multiplo de L = 10" |
| H9 | V2 | baja | **sí** | corregido | `BASE` relativa a `__file__` en `10_radial_controles.py` | Reejecutado: `cajas_9_6` y `yukawa_0.2/R40` idénticos |
| H10 | V2 | baja | **no** | rechazado | nada | `A_hulthen/<δ>/transferencia` es un objeto JSON (dict) en los tres δ, tanto en el archivo anterior (comprobado con `json.load` antes de reejecutar) como en el nuevo. Las únicas cadenas de `A_hulthen` son `A0/lim0`, `liminf` y `serie`, que son expresiones de sympy guardadas como texto a propósito |
| H11 | V2 | baja | **sí** | corregido | Sección 13 | −1.53e-6 (texto) frente a −1.5249e-6 (JSON) → ahora −1.52e-6 (nuevo JSON: −1.521e-6) |
| H12 | V2 | baja | **sí** | corregido | `test_pigs.py`: positividad real, `ValueError`, prueba de histograma de r_{M/2} con su prueba de potencia | 9 → 14 pruebas, todas pasan; histograma χ² 32.9/24 (p = 0.106); la escala r×1.05 se rechaza con p = 1.5e-62 |
| H13 | V2 | baja | **sí** | corregido | `14_criterio_cajas.py`: `err_r`, `err_F` del radial = $|X_{\rm Rich}-X_{1/80}|$ | Antes 0; ahora $3\times10^{-5}$ a $6.8\times10^{-4}$ (⟨r⟩/R) y hasta $5.9\times10^{-4}$ ($F_{1/2}$). No cambia ninguna tendencia ni la condición (c) (9/9) |

## Criterios que dejaron de pasar o que no pasan (tal cual)

- **Radial δ = 0.2 frente al exacto con $h=1/40,1/80$** (H4 de V1): $6.2\times10^{-9}>5\times10^{-9}$. No pasa; se usa $h=1/80,1/160$ cuando se necesite esa precisión.
- **B3b** (nuevo, $V_0=1.3$): $+2.2\times10^{-5}>10^{-5}$.
- **L16** (nuevo): la suma $h\sum_jK_D$ difiere de erf en $8\times10^{-5}$ a $3\times10^{-4}$ (orden $h^2$ medido, error de extremo del trapecio). El criterio de $10^{-10}$ lo fijé mal (suponía convergencia espectral); se deja como "no pasa" y se explica.
- Siguen sin pasar los mismos de antes: estabilidad de Nyström 0.02 → 0.04 (4 de 9 casos), δ = 0.2 con $h=0.04$ (2), ley ε² en δ = 0.2 sin Richardson en $h$, PIGS τ = 5 de producción (−3.19σ), orden de Trotter en $R=50$ y $100$, orden de Nyström cerca del umbral (1.36 y 2.29).

## Lo que queda pendiente

1. Firma de la tabla 15 y de las 6 decisiones listadas allí (Juan Sebastián).
2. Primera presentación (9 + 5 min) en `fase2/presentacion/` y bitácora de IA consolidada: fuera de esta tarea.
3. Imagen en $R$ o $R_{\rm ef}$ para las Fases 3 y 4 (H3 de V2): no se cambió el núcleo aprobado.
4. Pozo: la extrapolación en $h$ (orden ~1) sigue sin converger del todo; para un control cuantitativo hace falta una cuadratura que respete el salto.
5. Anomalía de τ = 5: abierta (p ≈ 1 % para la dispersión entre corridas).

## Registro de IA (esta respuesta)

- La primera estimación del sesgo de pared usaba la diferencia hacia atrás suponiendo $u(R)=0$ y daba 250 veces de más ($-0.275$ frente a $-1.08\times10^{-3}$ en $R=5$). Luego, con los tres últimos nodos, salía la mitad. La pendiente tomada a $2\sqrt\epsilon$ de la pared coincide a ~20 % o mejor. Comprobado frente al radial antes de dejarlo en el código.
- En `test_transferencia.py` la primera versión de `test_extremos_wk` exigía error viejo $>10^{-6}$ también fuera de la diagonal, y con $|r-r'|=0.3$ el error viejo es $2.3\times10^{-7}$. Cambié la condición a "el nuevo es 10 veces menor" (sin tocar la tolerancia del nuevo, $2\times10^{-8}$).
- En `test_pigs.py` la prueba de potencia del histograma usaba primero $u_T^2$ como densidad equivocada y **no** la rechazaba (p = 0.22: con τ = 1 la densidad del eslabón central se parece a $u_T^2$). La cambié, **después de ver el resultado**, por la densidad correcta con la escala alterada un 5 %. Queda declarado.
- En `15_limites.py`, primera ejecución: L14 tomaba mal $E_1$ (el desplazamiento cerca de $E_1$ devolvía $E_1$ y $E_2$, y se cogía $E_2$). Era un error del script, no del criterio; se corrigió el desplazamiento y se volvió a ejecutar (la salida de la primera ejecución está en `15_limites_salida_ejecucion1.txt`). El criterio de L16 se dejó como estaba y no pasa.
- En `16_tabla_controles.py` dos errores de programación corregidos (lectura de una clave de texto del JSON del radial y la letra de numeración de las filas).
- No hice esperas fijas de 10 s tras escribir en el montaje (la espera en primer plano está bloqueada); confirmé cada archivo releyéndolo o leyendo su JSON después.
