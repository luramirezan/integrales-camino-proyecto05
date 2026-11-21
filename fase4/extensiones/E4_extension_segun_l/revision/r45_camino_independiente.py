"""r45_camino_independiente.py -- revision R4: integral de camino de la onda p con OTROS eps y OTRA malla que los de E4.
 (a) metodo de E4 (K_1 exacto + U_1) con eps = 0.15 y 0.075 (tablas nuevas, sin cache) y h = 0.03 (E4 uso 0.04/0.02);
     Coulomb 2p (R = 60) frente a -1/8 y Yukawa delta = 0.2 (R = 100) frente a la caja espectral (espectral.py).
 (b) metodo primitivo con eps = 0.05, 0.025, 0.0125 (tablas l = 0 calculadas con pares_l, sin cache) para medir su
     orden de Trotter mas cerca de eps -> 0 (E4 lo midio solo con 0.2, 0.1, 0.05 y lo llamo 'compatible con 4/3').
Salida: revision/r45_camino_independiente.json y _salida.txt."""
import json, math, os, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "codigo"))
import pares_l as pl
import transferencia as tr
import espectral as s

log = open(os.path.join(AQUI, "r45_camino_independiente_salida.txt"), "w")
def p(*a):
    t = " ".join(str(x) for x in a); print(t, flush=True); log.write(t + "\n"); log.flush()
out = dict(a={}, b={})
T0 = time.time()
# referencias espectrales en caja
ref = {}
w = s.caja_autovalores(0.0, 1, 60.0, N=500, k=1)[0]
ref[0.0] = s.caja(0.0, 1, 60.0, w - 1e-6, w + 1e-6, N=500) if False else w
for delta, R in ((0.2, 100.0),):
    w = s.caja_autovalores(delta, 1, R, N=600, k=1)[0]
    ref[delta] = w
p("referencias espectrales en caja:", ref, "(Coulomb exacto -0.125)")
out["ref"] = {str(k): v for k, v in ref.items()}

# (a)
EPS_A = (0.15, 0.075)
tabs = {e: pl.tabla_richardson_l(1, e, h1=0.01, h2=0.005, cache=False) for e in EPS_A}
for delta, R in ((0.0, 60.0), (0.2, 100.0)):
    W = tr.W_yukawa(delta) if delta > 0 else None
    E = {}
    for h in (0.03, 0.01):
        for e in EPS_A:
            T, r = pl.matriz_T_l(R, h, e, 1, W=W, tabla=tabs[e])
            d = pl.resolver_T(T, r, R, e, ref[delta], h)
            E[(h, e)] = d["E0"]
            p(f"(a) delta={delta} h={h} eps={e}: E = {d['E0']:+.12e}  perron_min {d['perron_min']:+.1e}  min T {d['min_T']:.1e}")
    for h in (0.03, 0.01):
        Ex = E[(h, 0.075)] + (E[(h, 0.075)] - E[(h, 0.15)]) / 3
        exacto = -0.125 if delta == 0 else ref[delta]
        out["a"][f"d{delta}_h{h}"] = dict(E={str(k): v for k, v in E.items()}, E_ext=Ex, dif_ref=Ex - exacto,
                                         sesgo_eps0075=E[(h, 0.075)] - exacto, sesgo_eps015=E[(h, 0.15)] - exacto)
        p(f"(a) delta={delta} h={h}: E(eps->0, ley eps^2) = {Ex:+.12e}  ref {exacto:+.12e}  dif {Ex-exacto:+.1e}; "
          f"cociente de sesgos {(E[(h,0.15)]-exacto)/(E[(h,0.075)]-exacto):.3f} (4 si es eps^2)")
# (b)
EPS_B = (0.1, 0.05, 0.025, 0.0125)
Eb = {}
for e in EPS_B:
    t0 = pl.tabla_richardson_l(0, e, h1=0.01, h2=0.005, cache=False)
    Wp = lambda r: 1.0 / r**2
    T, r = tr.matriz_T(60.0, 0.01, e, W=Wp, tabla=t0)
    d = pl.resolver_T(T, r, 60.0, e, -0.125, 0.01)
    Eb[e] = d["E0"]
    p(f"(b) Coulomb 2p primitivo eps={e}: E = {d['E0']:+.12e}  sesgo {d['E0']+0.125:+.3e}")
ords = []
for e1, e2 in zip(EPS_B[:-1], EPS_B[1:]):
    o = math.log2((Eb[e1] + 0.125) / (Eb[e2] + 0.125))
    ords.append(dict(eps=(e1, e2), orden=o))
    p(f"(b) orden local entre eps={e1} y {e2}: {o:.3f}")
out["b"] = dict(E={str(k): v for k, v in Eb.items()}, ordenes=ords)
out["t"] = time.time() - T0
json.dump(out, open(os.path.join(AQUI, "r45_camino_independiente.json"), "w"), indent=1, default=float)
p(f"tiempo {out['t']:.0f} s")
