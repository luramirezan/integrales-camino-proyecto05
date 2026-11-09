# Usar otra IA (no Claude) como auditora

**Respuesta corta: sí es viable y es buena idea.** Hasta ahora el "auditor" de la bitácora fue el mismo Claude (lo dice la sección 10.1 y el supuesto S1 del registro de IA). Un modelo de otra empresa no comparte los mismos sesgos de entrenamiento, así que tiene más chance de ver un error que Claude repite. No es una garantía: la otra IA también se equivoca y también inventa referencias. Por eso la regla es que **un desacuerdo se resuelve calculando, no votando**.

## 1. Qué IA

Cualquiera de las grandes sirve: Gemini (Google AI Studio o la app) o ChatGPT. Lo importante es que pueda **ejecutar código** (Python), porque una auditoría de números sin re-cálculo vale poco. Anoten el nombre exacto del modelo que muestra la app y la fecha.

## 2. Qué darle

Por cada auditoría, un bloque pequeño y cerrado, no la bitácora entera:
- La sección en Markdown (por ejemplo `fase1/secciones/00_marco.md`, apartado 0.6).
- El script que la respalda (por ejemplo `fase1/codigo/00_toy_model.py`).
- Si hay fuentes, la tabla de referencias de esa sección.

No le digan qué resultado esperan ni que "ya lo revisó otra IA": eso la empuja a estar de acuerdo.

## 3. Qué pedirle (plantilla para copiar)

> Eres revisor de un proyecto de física teórica (mecánica cuántica, umbral de ligadura del potencial de Yukawa, integrales de camino en tiempo imaginario). Te paso una sección y su código. Quiero una auditoría adversarial, no un resumen.
> 1. Rehaz por tu cuenta cada deducción y cada número importante. Ejecuta código propio, sin reutilizar el mío, y di qué número obtuviste.
> 2. Busca errores de signo, de factores de 2 o $\pi$, de unidades y de límites ($\delta\to0$, cerca del umbral).
> 3. Revisa si las conclusiones se siguen de lo que se calcula, y si hay afirmaciones sin respaldo.
> 4. Para cada referencia, di si puedes confirmar autores, revista, volumen, página y año. Si no puedes, dilo; no inventes datos.
> 5. Entrega una tabla: hallazgo, gravedad (alta/media/baja), dónde está, cómo lo comprobaste, propuesta de corrección. Si no encuentras errores, dilo y lista lo que comprobaste.

## 4. Qué hacer con la respuesta

1. Guardar el prompt y la respuesta **literales** (copiar y pegar a un .md, o exportar el chat). En la Fase 1 lo que más faltó fue conservar los prompts literales.
2. Cada hallazgo se verifica antes de aceptarlo: re-ejecutar el cálculo, mirar la fuente. Si Claude y la otra IA no coinciden, decide el cálculo independiente (o ustedes), no la IA que suene más segura.
3. Ustedes deciden: aceptar, rechazar (con motivo) o dejar pendiente.

## 5. Cómo registrarlo en el registro de IA

En la tabla 10.1 cambiar "IA auditora" a algo como: *Claude (revisiones internas) y Gemini/ChatGPT [modelo exacto] (auditoría externa desde la Fase 2)*. Y por cada auditoría, una ficha con el formato del profesor:

| Campo | Ejemplo |
|---|---|
| ID | A-01 |
| Fecha | 28-10-2026 |
| IA auditora | Gemini [modelo exacto], app / AI Studio |
| Material auditado | Sección 0.6 y `00_toy_model.py` |
| Consulta | Prompt literal (archivo `auditorias/A-01_prompt.md`) |
| Respuesta utilizada | Hallazgos 1 y 3 (archivo `auditorias/A-01_respuesta.md`) |
| Comprobación | Cómo se verificó cada hallazgo (re-ejecución, fuente) |
| Decisión humana | Quién decidió qué, y por qué se rechazó lo rechazado |
| Corrección posterior | Qué cambió en la bitácora o el código |

## 6. Por dónde empezar

Lo más rentable para auditar con otra IA:
1. El resultado principal ($\delta_c=1.1906124211$, sección 5 y su código).
2. La sección 8 (acción euclídea y la divergencia del peso con $-1/r$), que es la base de la Fase 2.
3. La nueva tabla de fuentes de control (`fase2/fuentes_control/fuentes_control.md`): pedirle que confirme las referencias que aquí quedaron con revista "no confirmada".
