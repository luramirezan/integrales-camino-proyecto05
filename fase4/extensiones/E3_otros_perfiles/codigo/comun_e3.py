"""comun_e3.py -- rutas, salida doble (pantalla + archivo) y JSON para los scripts de E3."""
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
PROY = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))     # /mnt/project-files
F2 = os.path.join(PROY, "fase2", "codigo")
F3 = os.path.join(PROY, "fase3", "codigo")
os.makedirs(RES, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

DELTA_C_YUK_REF = 1.1906124210606      # Fases 1-3 (energia cero)
A_FASE3 = 0.7411                        # fase3/resultados/21_barrido.json, ajuste kappa = A D + B D^2
ORDEN = ("yukawa", "ecsc", "hulthen", "hatomo")


class Tee:
    def __init__(self, nombre):
        self.f = open(os.path.join(RES, f"{nombre}_salida.txt"), "w")
        self.t0 = time.perf_counter()

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.f.write(s + "\n")
        self.f.flush()

    def cerrar(self):
        self("tiempo total: %.1f s" % (time.perf_counter() - self.t0))
        self.f.close()


def guardar(nombre, d):
    with open(os.path.join(RES, f"{nombre}.json"), "w") as f:
        json.dump(d, f, indent=1, ensure_ascii=False, default=float)


def cargar(nombre):
    with open(os.path.join(RES, f"{nombre}.json")) as f:
        return json.load(f)
