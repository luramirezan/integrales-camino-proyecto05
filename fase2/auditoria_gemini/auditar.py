#!/usr/bin/env python3
"""Auditoría de la Fase 2 con Gemini, punto por punto, con contexto limpio en cada punto.

Cada punto (P10, P11, ...) es una conversación NUEVA con Gemini que solo ve el material
de ese punto. El auditor (Gemini) entrega hallazgos; los autores responden; se repiten
rondas; al cerrar, Gemini entrega la tabla final con el estado de cada hallazgo.

La API key se lee de la variable de entorno GEMINI_API_KEY y NUNCA se escribe en disco.

Uso (desde cualquier carpeta):
  python auditar.py modelos                      # lista los modelos disponibles con la key
  python auditar.py puntos                       # lista los puntos y su material
  python auditar.py abrir P10 [--modelo M]       # conversación nueva: material + encargo
  python auditar.py responder P10 resp.md        # manda la respuesta de los autores
  python auditar.py cerrar P10                   # pide la tabla final de ese punto
  python auditar.py informe                      # junta todo en informe_auditoria.md

Todo se guarda literal en conversaciones/<punto>.json (estado de la API) y
conversaciones/<punto>.md (transcripción legible, con el código que ejecutó Gemini).
"""
import json, os, sys, time, datetime, pathlib
import requests

AQUI = pathlib.Path(__file__).resolve().parent
F2 = AQUI.parent
CONV = AQUI / "conversaciones"
CONV.mkdir(exist_ok=True)
URL = "https://generativelanguage.googleapis.com/v1beta"
MODELO_DEF = os.environ.get("GEMINI_MODELO", "gemini-3.5-flash")

# --- Material de cada punto: (título, archivos relativos a fase2/, extracto de bitácora) ---
PUNTOS = {
 "P10": ("Solucionador radial de referencia",
         ["secciones/10_solucionador_radial.md", "codigo/radial.py",
          "codigo/10_radial_controles.py", "verificacion/10_radial_salida.txt"]),
 "P11": ("Acción de pares de Coulomb y matriz de transferencia",
         ["secciones/11_accion_pares_transferencia.md", "codigo/pares.py",
          "codigo/transferencia.py", "codigo/11_transferencia_controles.py",
          "verificacion/11_transferencia_salida.txt"]),
 "P12": ("PIGS radial y anomalía de tau=5",
         ["secciones/12_pigs.md", "codigo/pigs.py", "codigo/12_pigs_produccion.py",
          "codigo/12b_pigs_replica_tau5.py", "codigo/12c_pigs_coulomb_tau5.py",
          "verificacion/12_pigs_salida.txt", "verificacion/12b_pigs_replica_salida.txt",
          "verificacion/12c_pigs_coulomb_tau5_salida.txt"]),
 "P13": ("Controles exactos: Hulthén y pozo cuadrado",
         ["secciones/13_controles_hulthen_pozo.md", "codigo/13_controles_hulthen_pozo.py",
          "verificacion/13_controles_salida.txt"]),
 "P14": ("Criterio de cajas 9.6 con la condición (c)",
         ["secciones/14_criterio_cajas.md", "codigo/14_criterio_cajas.py",
          "verificacion/14_criterio_cajas_salida.txt"]),
 "P15": ("Límites físicos L01-L19 con la integral de camino",
         ["@bitacora:# Parte VI.:# Parte VII.", "codigo/15_limites.py",
          "verificacion/15_limites_salida.txt"]),
 "P16": ("Primer gráfico congelado (figuras 16 y 18)",
         ["@bitacora:## V.5 :## V.6 ", "codigo/16_primer_grafico.py",
          "codigo/18_figura_presentacion.py", "verificacion/16_primer_grafico_salida.txt",
          "resultados/16_primer_grafico.json", "figuras/16_primer_grafico.png"]),
 "PT": ("Tabla de controles consolidada (88 filas)",
        ["secciones/15_tabla_controles.md", "codigo/16_tabla_controles.py"]),
 "PD": ("Las 10 decisiones pendientes del equipo",
        ["decisiones_fase2.md"]),
 "PF": ("Fuentes de los controles (referencias bibliográficas)",
        ["fuentes_control/fuentes_control.md", "fuentes_control/verificacion_hulthen_2s.py"]),
}

CONTEXTO = ("Proyecto universitario de física teórica (curso de investigación teórica). "
 "Tema: umbral de ligadura del potencial de Yukawa V(r) = -exp(-delta r)/r en unidades "
 "hbar = m = g = 1, estado s. La Fase 1 dejó delta_c = 1.1906124211 con un solucionador "
 "radial. La Fase 2 compara ese resultado con integrales de camino en tiempo imaginario "
 "(acción de pares exacta de Coulomb, matriz de transferencia y PIGS). Los números de "
 "sección (9.6, 9.7, etc.) se refieren al plan de cómputo de la Fase 1.")

SISTEMA = ("Eres revisor de un proyecto de física teórica (mecánica cuántica, umbral de "
 "ligadura del potencial de Yukawa, integrales de camino en tiempo imaginario). "
 "Haces una auditoría adversarial, no un resumen. Escribe en español. "
 "Tienes una herramienta para ejecutar Python: úsala para rehacer los números importantes "
 "con código PROPIO (no copies el código del material) y di qué número obtuviste. "
 "Si un cálculo no cabe en tu tiempo de ejecución, haz una versión reducida y dilo. "
 "No inventes referencias ni datos: si no puedes confirmar algo, dilo. "
 "En rondas posteriores los autores responden tus hallazgos: no aceptes una respuesta "
 "solo porque suena segura; acéptala si la evidencia la respalda, y si no, sostén el "
 "hallazgo y di qué cálculo lo resolvería.")

ENCARGO = """Te paso el material de UN punto de la auditoría (no el proyecto entero). Punto: {titulo}.

1. Rehaz por tu cuenta cada deducción y cada número importante. Ejecuta código propio y di qué número obtuviste.
2. Busca errores de signo, de factores de 2 o pi, de unidades y de límites (delta -> 0, cerca del umbral).
3. Revisa si las conclusiones se siguen de lo que se calcula, y si hay afirmaciones sin respaldo.
4. Para cada referencia que aparezca, di si puedes confirmar autores, revista, volumen, página y año. Si no puedes, dilo; no inventes datos.
5. Entrega una tabla con columnas: ID (H1, H2, ...), hallazgo, gravedad (alta/media/baja), dónde está, cómo lo comprobaste, propuesta de corrección. Si no encuentras errores, dilo y lista lo que comprobaste.

Contexto mínimo: {contexto}

MATERIAL
{material}"""

CIERRE = ("Cierra este punto. Entrega la tabla final de TODOS tus hallazgos con columnas: "
 "ID, hallazgo, gravedad, estado (resuelto por la respuesta / sigue en pie / pendiente de "
 "cálculo), y una línea de motivo. Después, en una lista aparte, lo que comprobaste y "
 "quedó bien. No agregues hallazgos nuevos salvo que sean de gravedad alta.")


def key():
    k = os.environ.get("GEMINI_API_KEY", "").strip()
    if not k:
        sys.exit("Falta GEMINI_API_KEY en el entorno (no se guarda en archivos).")
    return k


def limpiar(txt):
    k = os.environ.get("GEMINI_API_KEY", "")
    return txt.replace(k, "***") if k else txt


def extracto_bitacora(ini, fin):
    t = (F2 / "bitacora_fase2.md").read_text(encoding="utf-8")
    a = t.index(ini); b = t.index(fin, a + len(ini))
    return t[a:b]


def partes_material(pid):
    titulo, archivos = PUNTOS[pid]
    texto, imagenes = [], []
    for a in archivos:
        if a.startswith("@bitacora:"):
            _, ini, fin = a.split(":", 2)
            texto.append(f"===== bitacora_fase2.md (extracto '{ini.strip()}') =====\n"
                         + extracto_bitacora(ini, fin))
        elif a.endswith(".png"):
            import base64
            imagenes.append((a, base64.b64encode((F2 / a).read_bytes()).decode()))
        else:
            texto.append(f"===== {a} =====\n" + (F2 / a).read_text(encoding="utf-8"))
    if imagenes:
        texto.append("(Se adjuntan como imagen: " + ", ".join(n for n, _ in imagenes) + ")")
    return titulo, "\n\n".join(texto), imagenes


def llamar(estado):
    cuerpo = {"system_instruction": {"parts": [{"text": SISTEMA}]},
              "contents": estado["contents"],
              "tools": [{"code_execution": {}}],
              "generationConfig": {"temperature": 0.4}}
    url = f"{URL}/models/{estado['modelo']}:generateContent"
    for intento in range(6):
        try:
            r = requests.post(url, json=cuerpo, timeout=900,
                              headers={"x-goog-api-key": key(), "Content-Type": "application/json"})
        except requests.RequestException as ex:
            print(f"[red] reintento en 30s: {limpiar(str(ex))[:300]}", file=sys.stderr)
            time.sleep(30); continue
        if r.status_code == 429 and "PerDay" in r.text:
            sys.exit("Cuota diaria agotada para este modelo: " + limpiar(r.text)[:600])
        if r.status_code in (429, 500, 503):
            espera = 20 * 2 ** intento
            print(f"[{r.status_code}] reintento en {espera}s: {limpiar(r.text)[:300]}", file=sys.stderr)
            time.sleep(espera); continue
        if r.status_code != 200:
            sys.exit(f"Error {r.status_code}: {limpiar(r.text)[:2000]}")
        d = r.json()
        cand = d.get("candidates", [{}])[0]
        cont = cand.get("content")
        if not cont:
            sys.exit("Respuesta vacía: " + json.dumps(d)[:2000])
        cont.setdefault("role", "model")
        estado["contents"].append(cont)
        estado.setdefault("uso", []).append(d.get("usageMetadata", {}))
        estado["version_modelo"] = d.get("modelVersion", estado["modelo"])
        return cont
    sys.exit("Se agotaron los reintentos (límite de la capa gratuita?).")


def render(cont):
    out = []
    for p in cont.get("parts", []):
        if p.get("thought"):
            continue
        if "text" in p:
            out.append(p["text"])
        elif "executableCode" in p:
            out.append("```python\n" + p["executableCode"].get("code", "") + "\n```")
        elif "codeExecutionResult" in p:
            r = p["codeExecutionResult"]
            out.append(f"Salida ({r.get('outcome','')}):\n```\n" + r.get("output", "") + "\n```")
    return "\n\n".join(out)


def guardar(pid, estado):
    (CONV / f"{pid}.json").write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")
    md = [f"# Auditoría externa {pid}: {estado['titulo']}\n",
          f"Modelo: `{estado.get('version_modelo', estado['modelo'])}` (API de Gemini, Google AI Studio). "
          f"Abierta: {estado['abierta']}. Conversación nueva, sin contexto de otros puntos.\n",
          "## Instrucción de sistema (literal)\n", SISTEMA, ""]
    for i, c in enumerate(estado["contents"]):
        if c["role"] == "user":
            if i == 0:
                md += ["## Prompt inicial (literal; el material va resumido por nombre de archivo)\n",
                       estado["prompt_sin_material"],
                       "\nArchivos incluidos completos: " + ", ".join(f"`{a}`" for a in PUNTOS[pid][1]), ""]
            else:
                md += [f"## {estado['etiquetas'][i]}\n", c["parts"][0]["text"], ""]
        else:
            md += [f"## Gemini ({estado['etiquetas'][i]})\n", render(c), ""]
    (CONV / f"{pid}.md").write_text("\n".join(md), encoding="utf-8")


def cargar(pid):
    p = CONV / f"{pid}.json"
    if not p.exists():
        sys.exit(f"{pid} no está abierto. Usa: abrir {pid}")
    return json.loads(p.read_text(encoding="utf-8"))


def abrir(pid, modelo):
    titulo, material, imagenes = partes_material(pid)
    prompt = ENCARGO.format(titulo=titulo, contexto=CONTEXTO, material=material)
    partes = [{"text": prompt}] + [{"inline_data": {"mime_type": "image/png", "data": b}} for _, b in imagenes]
    estado = {"punto": pid, "titulo": titulo, "modelo": modelo,
              "abierta": datetime.datetime.now().isoformat(timespec="seconds"),
              "prompt_sin_material": ENCARGO.format(titulo=titulo, contexto=CONTEXTO, material="[material]"),
              "contents": [{"role": "user", "parts": partes}], "etiquetas": ["prompt"]}
    cont = llamar(estado); estado["etiquetas"].append("ronda 1: hallazgos")
    # no guardar las imágenes en base64 en el json (pesan); se reconstruyen si hace falta
    guardar(pid, estado); print(render(cont))


def seguir(pid, texto, etiqueta):
    estado = cargar(pid)
    if imgs := partes_material(pid)[2]:  # volver a poner las imágenes del primer turno
        estado["contents"][0]["parts"] = [estado["contents"][0]["parts"][0]] + \
            [{"inline_data": {"mime_type": "image/png", "data": b}} for _, b in imgs]
    estado["contents"].append({"role": "user", "parts": [{"text": texto}]})
    estado["etiquetas"].append(etiqueta)
    cont = llamar(estado)
    estado["etiquetas"].append(etiqueta.replace("Respuesta de los autores", "réplica") )
    estado["contents"][0]["parts"] = estado["contents"][0]["parts"][:1]
    guardar(pid, estado); print(render(cont))


def informe():
    md = ["# Anexo: última respuesta de Gemini en cada punto (literal)\n",
          f"Generado: {datetime.date.today().isoformat()}. Cada punto fue una conversación nueva con "
          "Gemini que solo vio el material de ese punto. Transcripciones literales en `conversaciones/`.\n"]
    for pid in PUNTOS:
        p = CONV / f"{pid}.json"
        if not p.exists():
            md.append(f"## {pid}: {PUNTOS[pid][0]}\n\n_No auditado._\n"); continue
        e = json.loads(p.read_text(encoding="utf-8"))
        md.append(f"## {pid}: {e['titulo']}\n\nModelo `{e.get('version_modelo')}`; "
                  f"{sum(1 for c in e['contents'] if c['role']=='user')-1} respuestas de los autores. "
                  f"Transcripción: `conversaciones/{pid}.md`.\n")
        md.append("### Tabla final de Gemini\n\n" + render(e["contents"][-1]) + "\n")
    (AQUI / "anexo_tablas_finales_gemini.md").write_text("\n".join(md), encoding="utf-8")
    print("Escrito", AQUI / "anexo_tablas_finales_gemini.md")


if __name__ == "__main__":
    a = sys.argv[1:]
    modelo = MODELO_DEF
    if "--modelo" in a:
        i = a.index("--modelo"); modelo = a[i + 1]; del a[i:i + 2]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); sys.exit()
    cmd = a[0]
    if cmd == "modelos":
        r = requests.get(f"{URL}/models?pageSize=200", headers={"x-goog-api-key": key()}, timeout=60)
        for m in r.json().get("models", []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                print(m["name"].split("/")[-1], "|", m.get("displayName"), "| in", m.get("inputTokenLimit"))
    elif cmd == "puntos":
        for k, (t, f) in PUNTOS.items():
            print(k, t, "->", ", ".join(f))
    elif cmd == "abrir":
        abrir(a[1], modelo)
    elif cmd == "responder":
        n = sum(1 for c in cargar(a[1])["contents"] if c["role"] == "user")
        texto = ("Respuesta de los autores a tus hallazgos (la preparó el asistente de IA que produjo "
                 "el material; puede estar equivocada):\n\n" + pathlib.Path(a[2]).read_text(encoding="utf-8"))
        seguir(a[1], texto, f"Respuesta de los autores (ronda {n + 1})")
    elif cmd == "cerrar":
        seguir(a[1], CIERRE, "cierre")
    elif cmd == "informe":
        informe()
    else:
        sys.exit(__doc__)
