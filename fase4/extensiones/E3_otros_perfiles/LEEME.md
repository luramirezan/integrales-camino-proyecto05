# E3: otros perfiles de apantallamiento y universalidad cerca del umbral

Extensión de la Fase 4 (proyecto 05). Responde a la ampliación que sugiere la guía, "cambiar el perfil de apantallamiento":
¿qué del umbral del Yukawa es universal y qué depende del perfil? Perfiles: Yukawa (referencia), ECSC, Hulthén (exacto) y el
potencial estático de un átomo H 1s, $-(1/r+\delta/2)e^{-\delta r}$ (en $\delta=2$ es el potencial e–H estático en u. a.).

## Resultados principales

| Perfil | $\delta_c$ | $c$ predicha | $A$ medida | $r_e(\delta_c)$ | cruce de cajas |
|---|---|---|---|---|---|
| Yukawa | 1.1906124211 | 0.7411918 | 0.7411918 | +1.78063 | desde arriba |
| ECSC | 0.7205240859 | 2.4710277 | 2.4710162 | -0.40996 | desde abajo |
| Hulthén | 2.0000000000 | 0.5000000 | 0.5000000 | +1.50000 | desde arriba |
| átomo H estático | 1.8210587560 | 0.5508545 | 0.5508545 | +1.50853 | desde arriba |

- **Umbrales** con tres métodos (energía cero, energías de ligado y fase variable) que coinciden a $\le$ $7\times10^{-12}$.
  ECSC: 0.7205240859, compatible con 0.72052408 (Singh y Varshni, citado por Roy), 0.7205240 (Roy 2019) y 0.72052408588 (Ikhdair y Sever 1993).
- **Pendiente sin ajuste:** $c=-d(1/a)/d\delta=2\int\partial_\delta V\varphi_0^2$ predice la pendiente medida a
  $5\times10^{-6}$ o mejor; para el Yukawa $c=0.74119$ frente a 0.7411 de la Fase 3.
- **Universal:** $\kappa a\to1$, $\langle r\rangle\kappa\to\tfrac12$, punto fijo $2R^2E_0/\pi^2=\tfrac14$, $\langle r\rangle/R\to\tfrac12-2/\pi^2$.
- **No universal, pero fijado por $r_e$:** $\langle r\rangle\kappa=\tfrac12(1+r_e\kappa)$, $2R^2E_0/\pi^2=\tfrac14(1+r_e/R)$ en $\delta_c$ y
  $\delta^\ast-\delta_c\simeq r_e\pi^2/(8cR_1R_2)$ para los cruces. El ECSC es el único con $r_e<0$ (-0.4100) y por eso
  sus cruces llegan desde abajo.
- **Estado virtual** del otro lado: rango efectivo, cálculo directo y reconstrucción desde cajas coinciden (controles L5, K4).
- **Integral de camino** (acción de pares + $W$) para el ECSC en 5 valores de $\delta$ y 3 controles: todo dentro de la barra
  (máximo 0.61 barras), Trotter 1.98 a 2.01.
- **Controles:** 32 filas en `controles.md`; 29 pasan, 2 no pasan (U2 y S1, ambos por el diseño
  del ajuste del segundo método, con causa medida y variante posterior que pasa), 1 medido.

## Cómo reproducir (desde `codigo/`, un proceso)

```
export OMP_NUM_THREADS=1
python 01_umbrales.py            # delta_c por energia cero y por energias de ligado
python 02_dispersion.py          # a(delta), r_e(delta), c, B; desfasajes; Hulthen exacto
python 03_ligados_virtuales.py   # kappa, <r>, kappa a, polo virtual
python 03b_curvas_E.py           # curvas E0(delta) completas (figura 1)
python 04_cajas_universalidad.py # punto fijo 1/4, cruces, polo virtual desde cajas
python 05_transferencia_ecsc.py  # integral de camino (usa fase2/ y fase3/codigo sin modificarlos)
python 07_verificacion.py        # fase variable, radial de la Fase 3, Hulthen <r>
python 06_figuras.py; python 08_tabla_controles.py; python 09_textos.py
```
Tiempos medidos: ver `verificacion.md` (total 18 minutos). Módulos propios: `perfiles.py` (potenciales y solucionadores sin
malla) y `comun_e3.py` (rutas y salida). Salidas en `resultados/*.json` y `*_salida.txt`; figuras en `figuras/`.

## Archivos

`seccion_articulo.md` (sección para el artículo), `controles.md`, `fuentes.md`, `registro_ia.md`, `verificacion.md`,
`resultados/08_tabla_comparativa.md`.

## Qué quedó sin hacer

- Cruces de cajas con la integral de camino (aquí solo con el disparo); el análisis completo de cajas con transferencia es E2.
- Estados excitados (2s) y $\ell>0$ para los otros perfiles (E4 trata $\ell$ para Yukawa).
- Abrir los originales de Singh y Varshni (1983) y Nasser et al. (2011). Ya no hace falta una referencia para $r_e=3/\delta_c$ ni para $\kappa_v=\delta/2-1$ del Hulthén: se demuestran en `revision/informe_revision.md`.
- Auditoría externa con Gemini (la coordina la sesión principal, decisión D4).
