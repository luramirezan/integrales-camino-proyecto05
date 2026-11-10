"""20c_umbral_119_fino.py -- Proyecto 05, Fase 3: delta = 1.19 con el radial en malla mas fina.
En 20b la malla h = 1/40, 1/80 deja un error |E(h) - E(h/2)| ~ 1.6e-8 (cusp en el origen, independiente de R), que es
el 16 % de |E0| ~ 1e-7: la condicion (a') del criterio (malla < 10 % de |E0|) falla por la malla, no por la caja.
Aqui se repite con h = 1/160, 1/320 (Richardson p = 2) en R = 3200 ... 25600 (con 1/80 el error de malla aun era el 15 % de |E0|), con el MISMO criterio y umbral 0.1.
Salida: fase3/resultados/20c_umbral_119_fino.json.
"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

T0 = time.perf_counter()
d = 1.19
RS = (3200, 6400, 12800, 25600)
cel = {}
for R in RS:
    cel[R] = dict(radial=c.radial_ref(d, R, h=1 / 160))
    x = cel[R]["radial"]
    print(f"radial h=1/160 R={R}: E0={x['E0']:+.8e} +- {x['err']:.1e} (dE_rel {x['dE_rel']:.3f}) r/R={x['r_sobre_R']:.5f} "
          f"F12={x['F12']:.5f} <r>={x['r_med']:.1f}", flush=True)
a_s = c.long_dispersion(d)
ternas = [RS[i:i + 3] for i in range(len(RS) - 2)]
ev = {str(t): c.evaluar(cel, t, "radial", a_s) for t in ternas}
for t in ternas:
    e = ev[str(t)]
    print(f"terna {t}: (a,a',b)=({e['a']},{e['a_prima']},{e['b']}) ligado={e['ligado']} F12={[round(f,5) for f in e['F12']]}",
          flush=True)
json.dump(dict(script="20c_umbral_119_fino.py", fecha="2026-11-10", delta=d, a_s=a_s, h="1/160, 1/320",
               radial={f"R{R}": cel[R]["radial"] for R in RS}, criterio_radial=ev, tiempo_total_s=time.perf_counter() - T0),
          open(os.path.join(c.RES3, "20c_umbral_119_fino.json"), "w"), indent=1, default=float)
