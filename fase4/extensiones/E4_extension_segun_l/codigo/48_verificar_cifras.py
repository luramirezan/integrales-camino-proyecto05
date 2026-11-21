"""48_verificar_cifras.py -- E4: coteja cada cifra de los textos con los JSON.

Extrae de LEEME.md, seccion_articulo.md, teoria.md y verificacion.md los numeros con al menos 2 cifras significativas
o con potencia de diez (p. ej. 3.9x10^-11, 0.741192, 6.597) y busca, entre todos los valores numericos de
resultados/*.json (y sus transformaciones simples: valor absoluto, 1/x, 100x, cocientes conocidos), uno que redondeado
a las mismas cifras significativas coincida (tolerancia de media unidad en la ultima cifra, ampliada a una unidad por
redondeos encadenados). Lista los que no encuentra para revisarlos a mano: son constantes de formulas (42, 0.5826,
5/4, ...) o cifras derivadas que se comprueban en la salida.
Salida: resultados/48_verificar_cifras.json y _salida.txt.
"""
import glob
import json
import math
import os
import re

import comun4 as c

c.Tee("48_verificar_cifras")
vals = []


def recoger(x):
    if isinstance(x, dict):
        for v in x.values():
            recoger(v)
    elif isinstance(x, list):
        for v in x:
            recoger(v)
    elif isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x != 0:
        vals.append(float(x))


for fn in glob.glob(os.path.join(c.RES, "*.json")) + glob.glob(os.path.join(c.BASE, "revision", "*.json")):  # R4: tambien la revision
    if "48_" in fn:
        continue
    recoger(json.load(open(fn)))
base = list(set(abs(v) for v in vals))
pool = set()
for v in base:
    for w in (v, 1 / v, 100 * v):
        pool.add(w)
pool = sorted(pool)
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
pat = re.compile(r"(?<![\w.^/])[−-]?\d+(?:\.\d+)?(?:\s*×\s*10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)?")


def parse(tok):
    t = tok.replace("−", "-")
    m = re.match(r"(-?\d+(?:\.\d+)?)(?:\s*×\s*10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+))?", t)
    mant, ex = m.group(1), m.group(2)
    x = float(mant) * (10.0**int(ex.translate(SUP)) if ex else 1.0)
    digs = mant.lstrip("-").replace(".", "").lstrip("0")
    sig = max(len(digs), 1)
    return abs(x), sig, ex is not None


import bisect  # noqa: E402


def hay(x, sig):
    tol = 1.0 * 10**(math.floor(math.log10(x)) - sig + 1)
    i = bisect.bisect_left(pool, x - tol)
    return i < len(pool) and pool[i] <= x + tol


res = {}
for nom in ("LEEME.md", "seccion_articulo.md", "teoria.md", "verificacion.md"):
    txt = open(os.path.join(c.BASE, nom)).read()
    ok, falta = 0, []
    for m in pat.finditer(txt):
        tok = m.group(0)
        x, sig, pot = parse(tok)
        if x == 0 or (sig < 2 and not pot):
            continue
        if hay(x, sig):
            ok += 1
        else:
            ctx = txt[max(0, m.start() - 40):m.end() + 20].replace("\n", " ")
            falta.append(dict(cifra=tok, contexto=ctx))
    res[nom] = dict(encontradas=ok, sin_par=falta)
    print(f"\n{nom}: {ok} cifras con par en los JSON; {len(falta)} sin par (revisar a mano):")
    for f in falta:
        print(f"   {f['cifra']:>14}  ...{f['contexto']}...")
c.guardar_json("48_verificar_cifras", res)
