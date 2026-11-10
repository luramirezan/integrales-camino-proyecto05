"""20b_umbral_119.py -- Proyecto 05, Fase 3: el caso delta = 1.19 (a 6e-4 del umbral de referencia 1.19061).
Con R <= 3200 el criterio de cajas queda INDETERMINADO (20_cajas.json): E0 cambia de signo entre R = 1600 (+1.5e-7)
y R = 3200 (-7.1e-8). La longitud de dispersion es a_s = +2204, del orden de la extension del estado, asi que hacen
falta cajas R >> 2200. Aqui:
  (1) radial (DF h = 1/40, 1/80, Richardson) en R = 1600 ... 51200: criterio 9.6 con el radial solo;
  (2) la transferencia se queda en R <= 3200 (20_cajas.json): en R = 6400 la factorizacion LU del modo shift-invert
      (N = 319999, banda de 156 diagonales a cada lado) no cabe en la memoria de la maquina (MemoryError, 10-11-2026).
      La condicion (c) se evalua solo con R = 1600 y 3200.
Mismo umbral 0.1 de la ley de caja (decision 3). Salida: fase3/resultados/20b_umbral_119.json.
"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402
import warnings; warnings.simplefilter("ignore")

T0 = time.perf_counter()
d = 1.19
RS = (1600, 3200, 6400, 12800, 25600, 51200)
rad = {}
for R in RS:
    rad[R] = c.radial_ref(d, R)
    print(f"radial R={R}: E0={rad[R]['E0']:+.6e} +- {rad[R]['err']:.1e}  r/R={rad[R]['r_sobre_R']:.5f} F12={rad[R]['F12']:.5f}",
          flush=True)
a_s = c.long_dispersion(d)
cel = {R: dict(radial=rad[R]) for R in RS}
ternas = [RS[i:i + 3] for i in range(len(RS) - 2)]
ev = {str(t): c.evaluar(cel, t, "radial", a_s) for t in ternas}
for t in ternas:
    e = ev[str(t)]
    print(f"terna {t}: (a,a',b)=({e['a']},{e['a_prima']},{e['b']}) ligado={e['ligado']} no_ligado={e['no_ligado']}", flush=True)
prev = json.load(open(os.path.join(c.RES3, "20_cajas.json")))["celdas"]["1.19"]
trans = {1600: prev["R1600"], 3200: prev["R3200"]}
out = dict(script="20b_umbral_119.py", fecha="2026-11-10", delta=d, a_s=a_s,
           radial={f"R{R}": rad[R] for R in RS}, criterio_radial=ev,
           transferencia={f"R{R}": dict(E=trans[R]["E_mejor"], err=trans[R]["err"], E_rad=trans[R]["radial"]["E0"],
                                         compatible=trans[R]["compatible"], r_sobre_R=trans[R]["obs"]["r_sobre_R"]["mejor"],
                                         F12=trans[R]["obs"]["F12"]["mejor"]) for R in trans},
           nota_6400="MemoryError en la LU de shift-invert con N = 319999", tiempo_total_s=time.perf_counter() - T0)
json.dump(out, open(os.path.join(c.RES3, "20b_umbral_119.json"), "w"), indent=1, default=float)
for R in trans:
    t = out["transferencia"][f"R{R}"]
    print(f"transferencia R={R}: {t['E']:+.4e} +- {t['err']:.1e} (radial {t['E_rad']:+.4e}), compatible {t['compatible']}")
