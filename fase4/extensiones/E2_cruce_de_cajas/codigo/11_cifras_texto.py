"""11_cifras_texto.py -- comprueba que cada cifra de los textos de E2 sale de un JSON (regla 3 del CONTEXTO_COMUN).

Toma todos los numeros con al menos 3 cifras significativas de seccion_articulo.md, teoria.md, LEEME.md y verificacion.md
(decimales, notacion a×10⁻ⁿ y aen), y busca en todos los JSON de resultados/ un valor que, redondeado a las mismas cifras,
de el mismo numero. Prueba tambien |v|. Mide la tasa de coincidencias casuales con numeros al azar de 3, 4, 5 y 7 cifras. Lo que no
encuentra lo lista para revisarlo a mano (constantes como pi, cifras de la Fase 3 citadas, fechas, etc.).
Salida: resultados/11_cifras_texto.json y _salida.txt
"""
import json, glob, os, re, sys
import numpy as np
import e2comun as c

sys.stdout = c.Tee("11_cifras_texto")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
vals = []


def recoge(x):
    if isinstance(x, bool):
        return
    if isinstance(x, (int, float)):
        if np.isfinite(x):
            vals.append(float(x))
    elif isinstance(x, dict):
        for v in x.values(): recoge(v)
    elif isinstance(x, (list, tuple)):
        for v in x: recoge(v)


for fn in glob.glob(os.path.join(c.RES, "*.json")):
    if "11_cifras" in fn:
        continue
    recoge(json.load(open(fn)))
V = np.array(vals)
REF = c.DELTA_C_REF
cand = np.concatenate([V, np.abs(V)])       # solo el valor tal cual (un conjunto mayor da demasiadas coincidencias casuales)
cand = cand[np.isfinite(cand)]
PAT = re.compile(r"(?<![\w.])([+−-]?\d+\.\d+|\d+)(?:\s*[×x]\s*10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)|e([+-]?\d+))?")


def coincide(txt, mant, exp):
    m = float(mant.replace("−", "-"))
    e = int(exp.translate(SUP)) if exp else 0
    val = m * 10.0**e
    dec = len(mant.split(".")[1]) if "." in mant else 0
    tol = 0.5 * 10.0**(e - dec) * 1.0000001
    return bool(np.any(np.abs(cand - val) <= tol + 1e-300) or np.any(np.abs(-cand - val) <= tol + 1e-300))


res = {}
for nombre in ("seccion_articulo.md", "teoria.md", "LEEME.md", "verificacion.md"):
    fn = os.path.join(c.BASE, nombre)
    if not os.path.exists(fn):
        continue
    txt = open(fn).read()
    sin = []
    n = 0
    for m in PAT.finditer(txt):
        mant, exp = m.group(1), m.group(2) or (m.group(3) if m.group(3) else None)
        digs = re.sub(r"[^0-9]", "", mant).lstrip("0")
        if len(digs) < 3 or re.fullmatch(r"20\d\d", mant):        # cifras cortas y anos
            continue
        n += 1
        if not coincide(txt, mant, exp if m.group(2) else (m.group(3) if m.group(3) else None)):
            ini = max(0, m.start() - 40)
            sin.append(dict(numero=m.group(0), contexto=txt[ini:m.end() + 25].replace("\n", " ")))
    res[nombre] = dict(n_cifras=n, sin_json=sin)
    print(f"{nombre}: {n} cifras, {len(sin)} sin JSON")
    for s in sin:
        print(f"   {s['numero']!r:>16}  ...{s['contexto']}...")
rng = np.random.default_rng(0)
tasa = {}
for nd in (3, 4, 5, 7):
    tasa[nd] = float(np.mean([coincide("", f"{v:.{nd - 1}f}", None) for v in rng.uniform(0.1, 10, 400)]))
res["tasa_coincidencia_casual"] = tasa
print("tasa de coincidencias casuales (numeros al azar en [0.1, 10]) segun cifras:", tasa)
c.guardar("11_cifras_texto", res)
