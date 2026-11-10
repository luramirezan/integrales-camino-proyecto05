# Material para auditoría (parte 2 de 3)

Responde solo "Recibido".

## Script del barrido de cajas (20_cajas_fase3.py)

```python
"""20_cajas_fase3.py -- Proyecto 05, Fase 3: barrido de tamano de caja cerca del umbral.
delta in {1.15, 1.18, 1.19, 1.20, 1.25}, R in {50, 100, 200, 400, 800, 1600, 3200}; ternas consecutivas.
Criterio 9.6 (Fase 1) con la condicion (c) (Fase 2): mismo veredicto con el radial y con la integral de camino
(transferencia extrapolada en h y eps, receta de comun3.py). Umbral de la ley de caja 0.1, fijado ANTES de ver
estos datos (decision 3, aprobada el 10-11-2026). Pared en R sin imagen: solo termino en el error (decision 5).
Determinista. Salida: fase3/resultados/20_cajas.json, fase3/figuras/20_cajas.png.
"""
import json, os, sys, time
from multiprocessing import Pool
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402

DELTAS = (1.15, 1.18, 1.19, 1.20, 1.25)
RS = (50, 100, 200, 400, 800, 1600, 3200)
TERNAS = [RS[i:i + 3] for i in range(len(RS) - 2)]


def trabajo(arg):
    d, R = arg
    import warnings; warnings.simplefilter("ignore")
    return (d, R, c.celda(d, R))


if __name__ == "__main__":
    T0 = time.perf_counter()
    tareas = [(d, R) for R in sorted(RS, reverse=True) for d in DELTAS]
    with Pool(int(os.environ.get("NPROC", "3"))) as p:
        res = p.map(trabajo, tareas, chunksize=1)
    cel = {d: {} for d in DELTAS}
    for d, R, x in res:
        cel[d][R] = x
    a_s = {d: c.long_dispersion(d) for d in DELTAS}
    out = dict(script="20_cajas_fase3.py", fecha="2026-11-10", umbral_ley_caja=c.UMBRAL_LEY_CAJA,
               decisiones="1 (Richardson h^4), 3 (umbral 0.1 fijado antes), 5 (pared solo en el error)",
               a_s={f"{d:g}": a_s[d] for d in DELTAS}, celdas={}, veredictos={})
    for d in DELTAS:
        out["celdas"][f"{d:g}"] = {f"R{R}": cel[d][R] for R in RS}
        V, ver, usada = {}, "indeterminado", None
        for t in TERNAS:
            rr, tt, cc = (c.evaluar(cel[d], t, "radial", a_s[d]), c.evaluar(cel[d], t, "transferencia", a_s[d]),
                          c.cond_c(cel[d], t, a_s[d]))
            V[str(tuple(t))] = dict(radial=rr, transferencia=tt, c=cc)
            print(f"d={d} terna={t}: radial lig={rr['ligado']} nolig={rr['no_ligado']} (signo,tend,ley)=({rr['nl_signo']},"
                  f"{rr['nl_tendencias']},{rr['nl_ley']}) dev={[round(x,3) for x in rr['dev_ley']]} | transf lig={tt['ligado']} "
                  f"nolig={tt['no_ligado']} | c={cc['c']}", flush=True)
            if ver == "indeterminado":
                if rr["ligado"] and tt["ligado"] and cc["c"]:
                    ver, usada = "ligado", t
                elif rr["no_ligado"] and tt["no_ligado"] and cc["c"]:
                    ver, usada = "no ligado", t
        out["veredictos"][f"{d:g}"] = dict(veredicto=ver, terna=usada, por_terna=V)
        print(f"  VEREDICTO delta={d}: {ver} (terna {usada})", flush=True)
    out["n_celdas"] = len(tareas)
    out["n_compatibles"] = int(sum(cel[d][R]["compatible"] for d in DELTAS for R in RS))
    out["perron_min_global"] = float(min(cel[d][R]["perron_min"] for d in DELTAS for R in RS))
    out["tiempo_total_s"] = time.perf_counter() - T0
    json.dump(out, open(os.path.join(c.RES3, "20_cajas.json"), "w"), indent=1, default=float)
    print(f"celdas compatibles transferencia-radial: {out['n_compatibles']}/{out['n_celdas']}; "
          f"Perron min {out['perron_min_global']:+.1e}; tiempo {out['tiempo_total_s']:.0f} s")

```

## Salida impresa de 20_cajas_fase3.py

```
d=1.18  R=3200  E_tr=-3.0985743309e-05+-1.4e-08 E_rad=-3.0981603455e-05 dif=-4.1e-09 pTrot=2.017 r/R=0.02013 F12=1.00000 perron=+1.6e-14 t=111s
d=1.19  R=3200  E_tr=-7.1475293998e-08+-1.8e-08 E_rad=-6.9878705172e-08 dif=-1.6e-09 pTrot=2.332 r/R=0.22745 F12=0.89982 perron=+3.3e-05 t=117s
d=1.15  R=3200  E_tr=-4.5589250747e-04+-3.5e-08 E_rad=-4.5588440843e-04 dif=-8.1e-09 pTrot=1.989 r/R=0.00545 F12=1.00000 perron=-1.2e-16 t=147s
d=1.15  R=1600  E_tr=-4.5589250747e-04+-3.5e-08 E_rad=-4.5588440691e-04 dif=-8.1e-09 pTrot=1.989 r/R=0.01090 F12=1.00000 perron=-2.8e-16 t=49s
d=1.2   R=3200  E_tr=+4.4183741488e-07+-3.3e-11 E_rad=+4.4181971855e-07 dif=+1.8e-11 pTrot=2.002 r/R=0.47807 F12=0.54218 perron=+1.6e-04 t=112s
d=1.25  R=3200  E_tr=+4.7539103142e-07+-6.5e-11 E_rad=+4.7537210728e-07 dif=+1.9e-11 pTrot=1.070 r/R=0.49659 F12=0.50678 perron=+1.6e-04 t=107s
d=1.18  R=1600  E_tr=-3.0985743303e-05+-1.4e-08 E_rad=-3.0981604634e-05 dif=-4.1e-09 pTrot=2.017 r/R=0.04025 F12=1.00000 perron=+8.8e-09 t=42s
d=1.19  R=1600  E_tr=+1.5299654041e-07+-1.3e-08 E_rad=+1.5443583213e-07 dif=-1.4e-09 pTrot=2.176 r/R=0.26403 F12=0.85918 perron=+1.2e-04 t=43s
d=1.2   R=1600  E_tr=+1.6301277194e-06+-3.0e-10 E_rad=+1.6303005972e-06 dif=-1.7e-10 pTrot=2.023 r/R=0.45799 F12=0.57843 perron=+3.0e-04 t=42s
d=1.25  R=1600  E_tr=+1.8756841337e-06+-3.8e-10 E_rad=+1.8758731246e-06 dif=-1.9e-10 pTrot=1.373 r/R=0.49319 F12=0.51345 perron=+3.2e-04 t=42s
d=1.18  R=800   E_tr=-3.0985319405e-05+-1.4e-08 E_rad=-3.0981183252e-05 dif=-4.1e-09 pTrot=2.017 r/R=0.08047 F12=0.99818 perron=+4.9e-06 t=18s
d=1.15  R=800   E_tr=-4.5589250747e-04+-3.5e-08 E_rad=-4.5588440881e-04 dif=-8.1e-09 pTrot=1.989 r/R=0.02181 F12=1.00000 perron=+3.5e-13 t=19s
d=1.19  R=800   E_tr=+1.3200291473e-06+-1.0e-08 E_rad=+1.3218614330e-06 dif=-1.8e-09 pTrot=2.078 r/R=0.28180 F12=0.83813 perron=+2.8e-04 t=18s
d=1.25  R=800   E_tr=+7.3035688061e-06+-2.9e-09 E_rad=+7.3053546863e-06 dif=-1.8e-09 pTrot=1.422 r/R=0.48645 F12=0.52643 perron=+6.3e-04 t=18s
d=1.2   R=800   E_tr=+5.6671918539e-06+-1.6e-09 E_rad=+5.6685609197e-06 dif=-1.4e-09 pTrot=2.007 r/R=0.42563 F12=0.63326 perron=+5.6e-04 t=19s
d=1.15  R=400   E_tr=-4.5589250741e-04+-3.5e-08 E_rad=-4.5588440708e-04 dif=-8.1e-09 pTrot=1.989 r/R=0.04362 F12=0.99999 perron=+6.2e-08 t=9s
d=1.18  R=400   E_tr=-3.0750210745e-05+-1.2e-08 E_rad=-3.0745843438e-05 dif=-4.4e-09 pTrot=2.014 r/R=0.15268 F12=0.96725 perron=+1.2e-04 t=9s
d=1.19  R=400   E_tr=+6.5613727523e-06+-9.9e-09 E_rad=+6.5666936937e-06 dif=-5.3e-09 pTrot=2.022 r/R=0.29095 F12=0.82723 perron=+6.0e-04 t=9s
d=1.2   R=400   E_tr=+1.8430807467e-05+-1.1e-08 E_rad=+1.8439147583e-05 dif=-8.3e-09 pTrot=1.973 r/R=0.38604 F12=0.69570 perron=+1.0e-03 t=9s
d=1.15  R=200   E_tr=-4.5588163460e-04+-3.5e-08 E_rad=-4.5587346951e-04 dif=-8.2e-09 pTrot=1.989 r/R=0.08717 F12=0.99755 perron=+2.6e-05 t=4s
d=1.18  R=200   E_tr=-2.4076630903e-05+-2.3e-08 E_rad=-2.4059500542e-05 dif=-1.7e-08 pTrot=1.994 r/R=0.22498 F12=0.90429 perron=+6.3e-04 t=4s
d=1.19  R=200   E_tr=+2.8765535835e-05+-4.8e-08 E_rad=+2.8798700160e-05 dif=-3.3e-08 pTrot=1.971 r/R=0.29665 F12=0.82089 perron=+1.3e-03 t=4s
d=1.25  R=400   E_tr=+2.7732142461e-05+-2.1e-08 E_rad=+2.7745691414e-05 dif=-1.4e-08 pTrot=1.420 r/R=0.47345 F12=0.55071 perron=+1.2e-03 t=8s
d=1.15  R=100   E_tr=-4.5121222494e-04+-8.3e-08 E_rad=-4.5117431507e-04 dif=-3.8e-08 pTrot=1.982 r/R=0.16398 F12=0.96214 perron=+5.4e-04 t=2s
d=1.25  R=200   E_tr=+1.0076398274e-04+-1.5e-07 E_rad=+1.0085864776e-04 dif=-9.5e-08 pTrot=1.394 r/R=0.45029 F12=0.59200 perron=+2.4e-03 t=4s
d=1.2   R=200   E_tr=+5.7929967996e-05+-7.7e-08 E_rad=+5.7980605611e-05 dif=-5.1e-08 pTrot=1.915 r/R=0.35214 F12=0.74600 perron=+1.8e-03 t=4s
d=1.18  R=100   E_tr=+3.1948613489e-05+-2.9e-07 E_rad=+3.2132957847e-05 dif=-1.8e-07 pTrot=1.919 r/R=0.26767 F12=0.85850 perron=+1.9e-03 t=2s
d=1.19  R=100   E_tr=+1.2071684712e-04+-4.1e-07 E_rad=+1.2097633042e-04 dif=-2.6e-07 pTrot=1.863 r/R=0.30190 F12=0.81582 perron=+2.6e-03 t=2s
d=1.2   R=100   E_tr=+1.8652996866e-04+-5.2e-07 E_rad=+1.8686539043e-04 dif=-3.4e-07 pTrot=1.787 r/R=0.33164 F12=0.77602 perron=+3.2e-03 t=2s
d=1.25  R=100   E_tr=+3.4386300647e-04+-9.5e-07 E_rad=+3.4447571531e-04 dif=-6.1e-07 pTrot=1.317 r/R=0.41648 F12=0.64896 perron=+4.3e-03 t=2s
d=1.15  R=50    E_tr=-3.3177692275e-04+-1.5e-06 E_rad=-3.3081910841e-04 dif=-9.6e-07 pTrot=1.837 r/R=0.23962 F12=0.89500 perron=+2.8e-03 t=1s
d=1.18  R=50    E_tr=+3.3619892673e-04+-2.8e-06 E_rad=+3.3801327623e-04 dif=-1.8e-06 pTrot=1.647 r/R=0.29299 F12=0.83077 perron=+4.6e-03 t=1s
d=1.19  R=50    E_tr=+5.0011503863e-04+-3.3e-06 E_rad=+5.0224327364e-04 dif=-2.1e-06 pTrot=1.570 r/R=0.30929 F12=0.80936 perron=+5.3e-03 t=1s
d=1.2   R=50    E_tr=+6.4126079820e-04+-3.8e-06 E_rad=+6.4370300423e-04 dif=-2.4e-06 pTrot=1.491 r/R=0.32446 F12=0.78877 perron=+5.9e-03 t=1s
d=1.25  R=50    E_tr=+1.1102077215e-03+-5.9e-06 E_rad=+1.1140494688e-03 dif=-3.8e-06 pTrot=1.144 r/R=0.38214 F12=0.70458 perron=+7.8e-03 t=1s
d=1.15 terna=(50, 100, 200): radial lig=True nolig=False (signo,tend,ley)=(False,False,False) dev=[1.017, 1.398, 3.545] | transf lig=True nolig=False | c=True
d=1.15 terna=(100, 200, 400): radial lig=True nolig=False (signo,tend,ley)=(False,False,False) dev=[1.398, 3.545, 13.374] | transf lig=True nolig=False | c=True
d=1.15 terna=(200, 400, 800): radial lig=True nolig=False (signo,tend,ley)=(False,False,False) dev=[3.545, 13.374, 55.203] | transf lig=True nolig=False | c=True
d=1.15 terna=(400, 800, 1600): radial lig=True nolig=False (signo,tend,ley)=(False,False,False) dev=[13.374, 55.203, 227.547] | transf lig=True nolig=False | c=True
d=1.15 terna=(800, 1600, 3200): radial lig=False nolig=False (signo,tend,ley)=(False,False,False) dev=[55.203, 227.547, 926.979] | transf lig=True nolig=False | c=False
  VEREDICTO delta=1.15: ligado (terna (50, 100, 200))
d=1.18 terna=(50, 100, 200): radial lig=False nolig=False (signo,tend,ley)=(False,False,False) dev=[0.584, 0.995, 1.025] | transf lig=False nolig=False | c=True
d=1.18 terna=(100, 200, 400): radial lig=False nolig=False (signo,tend,ley)=(False,False,False) dev=[0.995, 1.025, 1.461] | transf lig=False nolig=False | c=True
d=1.18 terna=(200, 400, 800): radial lig=True nolig=False (signo,tend,ley)=(False,False,False) dev=[1.025, 1.461, 3.836] | transf lig=True nolig=False | c=True
d=1.18 terna=(400, 800, 1600): radial lig=True nolig=False (signo,tend,ley)=(False,False,False) dev=[1.461, 3.836, 14.605] | transf lig=True nolig=False | c=True
d=1.18 terna=(800, 1600, 3200): radial lig=True nolig=False (signo,tend,ley)=(False,False,False) dev=[3.836, 14.605, 60.251] | transf lig=True nolig=False | c=True
  VEREDICTO delta=1.18: ligado (terna (200, 400, 800))
d=1.19 terna=(50, 100, 200): radial lig=False nolig=False (signo,tend,ley)=(True,False,False) dev=[471.128, 107.504, 22.432] | transf lig=False nolig=False | c=True
d=1.19 terna=(100, 200, 400): radial lig=False nolig=False (signo,tend,ley)=(True,False,False) dev=[107.504, 22.432, 3.33] | transf lig=False nolig=False | c=True
d=1.19 terna=(200, 400, 800): radial lig=False nolig=False (signo,tend,ley)=(True,False,False) dev=[22.432, 3.33, 0.472] | transf lig=False nolig=False | c=True
d=1.19 terna=(400, 800, 1600): radial lig=False nolig=False (signo,tend,ley)=(True,False,False) dev=[3.33, 0.472, 0.989] | transf lig=False nolig=False | c=True
d=1.19 terna=(800, 1600, 3200): radial lig=False nolig=False (signo,tend,ley)=(False,False,False) dev=[0.472, 0.989, 1.014] | transf lig=False nolig=False | c=True
  VEREDICTO delta=1.19: indeterminado (terna None)
d=1.2 terna=(50, 100, 200): radial lig=False nolig=False (signo,tend,ley)=(True,True,False) dev=[3.856, 1.235, 0.382] | transf lig=False nolig=False | c=True
d=1.2 terna=(100, 200, 400): radial lig=False nolig=False (signo,tend,ley)=(True,True,False) dev=[1.235, 0.382, 0.101] | transf lig=False nolig=False | c=True
d=1.2 terna=(200, 400, 800): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.382, 0.101, 0.021] | transf lig=False nolig=True | c=True
d=1.2 terna=(400, 800, 1600): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.101, 0.021, 0.004] | transf lig=False nolig=True | c=True
d=1.2 terna=(800, 1600, 3200): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.021, 0.004, 0.001] | transf lig=False nolig=True | c=True
  VEREDICTO delta=1.2: no ligado (terna (200, 400, 800))
d=1.25 terna=(50, 100, 200): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.169, 0.038, 0.007] | transf lig=False nolig=True | c=True
d=1.25 terna=(100, 200, 400): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.038, 0.007, 0.001] | transf lig=False nolig=True | c=True
d=1.25 terna=(200, 400, 800): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.007, 0.001, 0.0] | transf lig=False nolig=True | c=True
d=1.25 terna=(400, 800, 1600): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.001, 0.0, 0.0] | transf lig=False nolig=True | c=True
d=1.25 terna=(800, 1600, 3200): radial lig=False nolig=True (signo,tend,ley)=(True,True,True) dev=[0.0, 0.0, 0.0] | transf lig=False nolig=True | c=True
  VEREDICTO delta=1.25: no ligado (terna (50, 100, 200))
celdas compatibles transferencia-radial: 35/35; Perron min -2.8e-16; tiempo 331 s
```
