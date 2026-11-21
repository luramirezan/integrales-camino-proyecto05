"""r43_cajas.py -- revision R4: punto fijo de caja en el umbral (2p, 3d; 1s como referencia) y radio de cruce,
recalculados con el metodo espectral (espectral.py). Compara con resultados/43_cajas_l.json.
Incluye la prediccion de la correccion O(1/R) para l = 1 derivada en la revision: Y = 1 + (9/5) A^2 / R + ...
Salida: revision/r43_cajas.json y _salida.txt."""
import json, math, os, time
import numpy as np
import espectral as s

AQUI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(AQUI), "resultados")
log = open(os.path.join(AQUI, "r43_cajas_salida.txt"), "w")
def p(*a):
    t = " ".join(str(x) for x in a); print(t, flush=True); log.write(t + "\n"); log.flush()
C = json.load(open(os.path.join(RES, "41_constantes_umbral.json")))["constantes"]
J = json.load(open(os.path.join(RES, "43_cajas_l.json")))
out = dict(Y={}, radio_cruce={})
T0 = time.time()
for k, l, Rs in (("1s", 0, (160, 640, 2560)), ("2p", 1, (160, 640, 2560)), ("3d", 2, (160, 320, 640))):
    dc = C[k]["delta_c"]
    filasE4 = {f["R"]: f for f in J["a_umbral"][k]["filas"]}
    out["Y"][k] = []
    for R in Rs:
        if l == 0:
            Ep = math.pi**2 / (8 * R**2)
        else:
            Ep = (2 * l + 1) * C[k]["An2"] / (2 * R**(2 * l + 1))
        res = {}
        for N in (600, 800):
            res[N] = s.caja(dc, l, float(R), 0.5 * Ep, 3.0 * Ep, N=N)
        E = res[800]
        f = dict(R=R, E=E, conv_N=(res[800] - res[600]) / E, E_E4=filasE4[R]["E"], rel=(E - filasE4[R]["E"]) / E)
        if l == 0:
            f["y"] = 2 * R**2 * E / math.pi**2
        else:
            f["Y"] = E / Ep
            f["Y_E4"] = filasE4[R]["Y"]
            # sensibilidad a delta_c: dE/ddelta = S  => dY = S * 1e-15 / Ep para un error de 1e-15 en delta_c
            f["dY_por_1e-15_en_delta_c"] = C[k]["S"] * 1e-15 / Ep
            if l == 1:
                f["Y_pred_1_mas_9A2_5R"] = 1 + 1.8 * C[k]["An2"] / R
        out["Y"][k].append(f)
        p(k, {kk: (f"{v:.7g}" if isinstance(v, float) else v) for kk, v in f.items()})
# radio de cruce: E de la caja en R = R_c(E4) debe ser 0 (frente a la escala S Delta)
for k, l in (("2p", 1), ("3d", 2), ("1s", 0)):
    dc = C[k]["delta_c"]
    out["radio_cruce"][k] = []
    for f in J["b_radio_cruce"][k]["filas"]:
        if f["Delta_rel"] not in (1e-2, 1e-3, 1e-4):
            continue
        Rc = f["R_c"]; delta = dc * (1 - f["Delta_rel"])
        esc = (C[k]["S"] if l else 0.5 * C[k]["c0_pred"]**2 * dc * f["Delta_rel"]) * dc * f["Delta_rel"]
        lo, hi = -3 * esc, 3 * esc
        try:
            E = s.caja(delta, l, Rc, lo, hi, N=700)
        except ValueError:
            E = float("nan")
        g = dict(Delta_rel=f["Delta_rel"], R_c_E4=Rc, E_en_Rc=E, E_sobre_escala=E / esc)
        out["radio_cruce"][k].append(g)
        p(k, "radio de cruce", g)
# sensibilidad de Y(2560) del 3d a delta_c (con la E de E4, que la revision no recalcula a ese R)
f3 = [f for f in J["a_umbral"]["3d"]["filas"] if f["R"] == 2560][0]
out["sens_3d_2560"] = dict(E_E4=f3["E"], Y_E4=f3["Y"], dY_por_1e15=C["3d"]["S"] * 1e-15 / f3["E"])
p("3d R=2560:", out["sens_3d_2560"])
out["t"] = time.time() - T0
json.dump(out, open(os.path.join(AQUI, "r43_cajas.json"), "w"), indent=1, default=float)
p(f"tiempo {out['t']:.0f} s")
