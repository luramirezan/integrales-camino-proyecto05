"""r45b_sesgo_tabla.py -- revision R4: el desfase comun de +5e-11 del metodo (a), ¿viene de la tabla U_1?
Coulomb 2p, R = 60, h = 0.02, eps = 0.1 con tablas U_1 de Richardson (h_tab = 0.01, 0.005) [la de E4] y
(0.005, 0.0025) [mas fina]. Salida: revision/r45b_sesgo_tabla.json y _salida.txt."""
import json, os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "codigo"))
import pares_l as pl
log = open(os.path.join(AQUI, "r45b_sesgo_tabla_salida.txt"), "w")
def p(*a):
    t = " ".join(str(x) for x in a); print(t, flush=True); log.write(t + "\n"); log.flush()
out = {}
for (h1, h2) in ((0.01, 0.005), (0.005, 0.0025)):
    t = time.time()
    tb = pl.tabla_richardson_l(1, 0.1, h1=h1, h2=h2, cache=(h1 == 0.01))
    T, r = pl.matriz_T_l(60.0, 0.02, 0.1, 1, tabla=tb)
    d = pl.resolver_T(T, r, 60.0, 0.1, -0.125, 0.02)
    out[f"{h1}_{h2}"] = d["E0"]
    p(f"tabla h_tab=({h1},{h2}): E(eps=0.1, h=0.02) = {d['E0']:+.14e}  E + 1/8 = {d['E0']+0.125:+.3e}  ({time.time()-t:.0f} s)")
out["dif"] = out["0.005_0.0025"] - out["0.01_0.005"]
p(f"cambio al afinar la tabla: {out['dif']:+.2e}")
json.dump(out, open(os.path.join(AQUI, "r45b_sesgo_tabla.json"), "w"), indent=1)
