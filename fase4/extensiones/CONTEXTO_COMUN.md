# Contexto común para las cinco extensiones (Fase 4 y entrega final, proyecto 05)

Lucho (Luis Felipe Ramírez) pidió el 17-11-2026 hacer TODAS las extensiones propuestas en
`fase4/propuesta_originalidad/ideas_fase4_y_final.md`, cada una aislada en su carpeta, de la más sencilla a la más difícil,
con verificación repetida de fuentes, datos y código, y una auditoría externa con Gemini. Las decisiones las toma Claude
y se registran en `DECISIONES.md`; el equipo las revisa al final.

## El proyecto
- Pregunta (guía del curso, proyecto 05): ¿en qué intervalo de apantallamiento deja de existir el estado ligado de
  V(r) = −g e^{−μr}/r? Unidades ħ = m = g = 1; todo depende de δ = μħ²/(mg). Referencia δ_c = 1.1906124210606 (1s).
- Lo hecho en Fases 1–3 (leer `fase3/LEEME.md` y `fase3/articulo/borrador_articulo.md`): solucionador radial
  (`fase2/codigo/radial.py`), integral de camino en tiempo imaginario con acción de pares de Coulomb evaluada como
  matriz de transferencia en banda (`fase2/codigo/transferencia.py`, `pares.py`), utilidades de la Fase 3
  (`fase3/codigo/comun3.py`: `resolver_tr(delta, R, h, eps, E_guess)` devuelve E0, E1, r_med, r2_med, r_sobre_R, F12,
  perron, residuo; `radial_ref(delta, R, h)`; receta de extrapolación ε→0 (ley ε²) y h→0 (Richardson exponente 4);
  error = suma lineal de los tres términos, incluido el sesgo de pared). Un caso típico (δ = 1.19, R = 200, h = 0.04,
  ε = 0.1) tarda ~1.3 s.
- Sign convention: la longitud de dispersión a_s es POSITIVA cuando hay ligado (u ≈ r − a fuera del potencial);
  a_s(1.19) = +2204, a_s(1.20) = −142.9.
- Guía del curso: `enunciado/guia_texto.txt` (proyecto 05 en líneas ~112–122). Formato de la bitácora de IA: fecha,
  consulta, respuesta utilizada, decisión humana, comprobación, corrección posterior. Para singularidades: decir si el
  peso muestreado es real, positivo y normalizable.

## Reglas para todo el trabajo
1. **No modificar** nada fuera de tu carpeta de extensión. Importa los módulos de `fase2/codigo` y `fase3/codigo`
   añadiendo su ruta a `sys.path`; no los copies ni los edites.
2. Python 3 con numpy, scipy, matplotlib (si falta algo: `pip install -q <paquete>`). `export OMP_NUM_THREADS=1`.
   Hay 4 núcleos compartidos con otros cuatro trabajos simultáneos: **usa como máximo 1 proceso** salvo pasos cortos.
   Ningún script debería pasar de ~20 minutos; si algo es más caro, reduce la rejilla y dilo.
3. Todo determinista (semilla fija si hay Monte Carlo). Cada script escribe `resultados/<nombre>.json` y su salida
   impresa en `resultados/<nombre>_salida.txt`. Ninguna cifra del texto se escribe a mano: sale de un JSON.
4. Figuras PNG (dpi 150) en `figuras/`, con barras de error cuando existan, ejes etiquetados en español.
5. `/mnt/project-files` es un montaje de red: escribe ahí, pero vuelve a leer un archivo ~10 s después de escribirlo
   si dependes de él; nunca busques recursivamente en todo `/mnt/project-files/`.
6. Español, frases completas, sin flechas ni guiones largos en la prosa.
7. **Honestidad:** si un control falla, se reporta como "no pasa" con su causa medida (como en la tabla de la Fase 3).
   No ajustes criterios después de ver los datos; si fijas un umbral, escríbelo antes de correr y di que lo hiciste.
8. **Fuentes:** solo cita lo que verifiques tú mismo (WebSearch/WebFetch a arXiv, DOI, página del editor).
   Marca cada fuente como [V] (verificada en editor/DOI), [V-arXiv] (solo arXiv) o [no verificada]. No inventes
   volúmenes ni páginas.

## Entregables de cada carpeta `E*/`
- `codigo/` scripts numerados y comentados; `resultados/` JSON + salidas; `figuras/`.
- `LEEME.md`: qué pregunta responde, cómo reproducir (orden de los scripts y tiempos), resultados principales con
  cifras, qué quedó sin hacer.
- `seccion_articulo.md`: la sección lista para insertar en el artículo final (10–12 págs en total, así que esta sección
  ocupa ~1.5–3 páginas): motivación, método, resultados con figuras y barras de error, discusión, referencias.
- `controles.md`: tabla de controles (# | control | criterio fijado antes | valor | ¿pasa? | script), generada por
  script desde los JSON.
- `fuentes.md`: referencias con su estado de verificación y qué se comprobó de cada una.
- `registro_ia.md`: entradas en el formato del curso (fecha 17-11-2026 en adelante).
- `verificacion.md`: comprobaciones independientes que hiciste de tus propios resultados (segundo método, caso
  exacto, convergencia), y lo que encontraste al releer el código.
