# Material para auditoría (parte 3 de 3)

## δ = 1.19 con cajas más grandes (20b, radial h = 1/40; 20c, radial h = 1/160)

```python
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

```

Salida de 20b:
```
radial R=1600: E0=+1.544358e-07 +- 3.6e-08  r/R=0.26404 F12=0.85921
radial R=3200: E0=-6.987871e-08 +- 2.2e-08  r/R=0.22750 F12=0.89998
radial R=6400: E0=-9.817510e-08 +- 1.7e-08  r/R=0.15849 F12=0.96391
radial R=12800: E0=-9.886962e-08 +- 1.6e-08  r/R=0.08092 F12=1.00152
radial R=25600: E0=-9.883403e-08 +- 1.6e-08  r/R=0.03981 F12=1.00028
radial R=51200: E0=-9.883491e-08 +- 1.6e-08  r/R=0.01990 F12=1.00000
terna (1600, 3200, 6400): (a,a',b)=(False,False,True) ligado=False no_ligado=False
terna (3200, 6400, 12800): (a,a',b)=(True,False,True) ligado=False no_ligado=False
terna (6400, 12800, 25600): (a,a',b)=(True,False,False) ligado=False no_ligado=False
terna (12800, 25600, 51200): (a,a',b)=(True,False,False) ligado=False no_ligado=False
transferencia R=1600: +1.5300e-07 +- 1.3e-08 (radial +1.5444e-07), compatible True
transferencia R=3200: -7.1475e-08 +- 1.8e-08 (radial -6.9879e-08), compatible True
```
Salida de 20c:
```
radial h=1/160 R=3200: E0=-7.25815945e-08 +- 1.6e-09 (dE_rel 0.067) r/R=0.22745 F12=0.89966 <r>=727.8
radial h=1/160 R=6400: E0=-1.01746016e-07 +- 1.3e-09 (dE_rel 0.039) r/R=0.16003 F12=0.96096 <r>=1024.2
radial h=1/160 R=12800: E0=-1.03024183e-07 +- 1.3e-09 (dE_rel 0.038) r/R=0.08602 F12=0.99711 <r>=1101.1
radial h=1/160 R=25600: E0=-1.02986070e-07 +- 1.3e-09 (dE_rel 0.037) r/R=0.04305 F12=0.99999 <r>=1102.2
terna (3200, 6400, 12800): (a,a',b)=(True,True,True) ligado=True F12=[0.89966, 0.96096, 0.99711]
terna (6400, 12800, 25600): (a,a',b)=(True,True,True) ligado=True F12=[0.96096, 0.99711, 0.99999]
```

## Diagnóstico de la pared (20d): orden de Trotter antes y después de comparar con el radial en R + 0.5826√ε

```
delta=1.18 R=50: orden 1.647 -> 1.984 con la pared en R + beta sqrt(eps)
delta=1.19 R=50: orden 1.570 -> 1.984 con la pared en R + beta sqrt(eps)
delta=1.2 R=50: orden 1.491 -> 1.984 con la pared en R + beta sqrt(eps)
delta=1.2 R=100: orden 1.787 -> 1.991 con la pared en R + beta sqrt(eps)
delta=1.25 R=50: orden 1.144 -> 1.983 con la pared en R + beta sqrt(eps)
delta=1.25 R=100: orden 1.317 -> 1.988 con la pared en R + beta sqrt(eps)
delta=1.25 R=200: orden 1.394 -> 1.992 con la pared en R + beta sqrt(eps)
delta=1.25 R=400: orden 1.420 -> 1.993 con la pared en R + beta sqrt(eps)
delta=1.25 R=800: orden 1.422 -> 1.975 con la pared en R + beta sqrt(eps)
```

## Convergencia (22_convergencia.py, salida)

```
delta=0.2 R=40: radial -3.2680850515e-01; ext -3.2680850158e-01 (dif +3.6e-09, 1.1e-08 de |E0|); orden malla [4.0, 4.0, 4.0, 4.0]; orden Trotter [1.959, 1.767]
   presupuesto/|E0|: trotter_eps01=3.7e-07, trotter_eps005=1.0e-07, malla_h002_eps005=6.2e-07, pared_eps01=1.4e-11, pared_extrapolada=3.3e-11, extrapolacion_eps=1.6e-08, final_menos_radial=1.1e-08, radial_malla=1.8e-08
delta=0.8 R=100: radial -4.4704297970e-02; ext -4.4704300857e-02 (dif -2.9e-09, 6.5e-08 de |E0|); orden malla [4.0, 4.0, 4.0, 4.0]; orden Trotter [1.983, 1.991]
   presupuesto/|E0|: trotter_eps01=1.7e-04, trotter_eps005=4.4e-05, malla_h002_eps005=2.2e-06, pared_eps01=3.5e-11, pared_extrapolada=7.2e-11, extrapolacion_eps=2.8e-07, final_menos_radial=6.5e-08, radial_malla=1.4e-07
delta=1.0 R=174: radial -1.0285784215e-02; ext -1.0285788887e-02 (dif -4.7e-09, 4.5e-07 de |E0|); orden malla [4.0, 4.0, 4.0, 4.0]; orden Trotter [1.983, 1.991]
   presupuesto/|E0|: trotter_eps01=8.3e-04, trotter_eps005=2.1e-04, malla_h002_eps005=4.7e-06, pared_eps01=8.8e-11, pared_extrapolada=3.6e-11, extrapolacion_eps=1.2e-06, final_menos_radial=4.5e-07, radial_malla=5.3e-07
delta=1.15 R=600: radial -4.5588440793e-04; ext -4.5588883325e-04 (dif -4.4e-09, 9.7e-06 de |E0|); orden malla [4.02, 4.0, 4.0, 4.0]; orden Trotter [1.989, 1.993]
   presupuesto/|E0|: trotter_eps01=6.6e-03, trotter_eps005=1.7e-03, malla_h002_eps005=2.3e-05, pared_eps01=2.4e-09, pared_extrapolada=3.9e-09, extrapolacion_eps=8.1e-06, final_menos_radial=9.7e-06, radial_malla=9.5e-06
```

## Conclusión que presenta el grupo

1. δ = 1.15 y 1.18 ligados, δ = 1.20 y 1.25 no ligados, con los dos métodos y la condición (c): **δ_c ∈ [1.18, 1.20]**.
2. δ = 1.19: con R ≤ 3200 el criterio queda indeterminado (E0 cambia de signo entre R = 1600 y 3200). Con el radial solo en R = 3200 … 25600 (h = 1/160) sale ligado, con E0 = −1.03×10⁻⁷ y ⟨r⟩ = 1102: **δ_c ∈ [1.19, 1.20]** con un solo método.
3. El cambio de signo de E0(R) en δ = 1.19 es un efecto de caja (estado ligado más grande que la caja), no un artefacto del método.

## Encargo (auditoría adversarial de autovalores cercanos a cero)

Eres revisor. No me des un resumen: intenta **refutar** estas conclusiones. Antes de empezar, di si puedes ejecutar código. Si no puedes, marca cada número tuyo como "calculado a mano".

1. Para los autovalores cercanos a cero (δ = 1.19 en todas las cajas, δ = 1.18 en R = 50 a 200, δ = 1.20 en R ≥ 800), propón explicaciones alternativas **verificables** de que el signo o la tendencia sean un artefacto: pared sin imagen, sesgo de Trotter, malla, extrapolación, tabla U_C, error de malla del radial, el propio criterio. Para cada una, di qué cálculo concreto la confirmaría o la descartaría con los datos que hay.
2. ¿El veredicto "no ligado" de δ = 1.20 podría esconder un estado ligado muy débil que aparecería con R mucho mayor? Usa a_s = −142.93 y la ley de caja.
3. ¿El criterio (umbrales 0.1, 0.95, ternas) puede dar un falso "ligado" o un falso "no ligado"? Da un caso concreto.
4. ¿Las barras de error son creíbles? Fíjate en la suma de errores y en el término de pared.
5. ¿Es correcto pasar de los veredictos a los intervalos 1. y 2.?

**Primero entrega solo la lista de hallazgos: máximo 8, una línea cada uno, con gravedad (alta / media / baja).** El detalle lo pediré después, 2 o 3 hallazgos por mensaje.
