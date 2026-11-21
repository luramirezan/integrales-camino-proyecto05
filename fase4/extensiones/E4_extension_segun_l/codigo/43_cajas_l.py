"""43_cajas_l.py -- E4, tarea 3: prueba de cajas para l = 1 y l = 2 (con 1s de referencia).

Predicciones (teoria.md, seccion 5), con An2 y S del script 41:
  (a) En el umbral, caja de Dirichlet de radio R:
        l = 0:  E(R) -> pi^2/(8 R^2),  y = 2 R^2 E/pi^2 -> 1/4;
        l >= 1: E(R) = (2l+1) An2 / (2 R^{2l+1}) [1 + O(1/R)],  y -> 0 como 1/R^{2l-1};
                la variable con punto fijo es Y = 2 R^{2l+1} E / ((2l+1) An2) -> 1.
  (b) Radio de caja en el que el nivel cruza E = 0 (por Sturm, ultimo nodo de la solucion de energia cero):
        l = 0: R_c = a_s ~ 1/(c0 Delta);  l >= 1: R_c^{2l+1} = (2l+1) An2/(2 S Delta).
      Con R > R_c el signo de E en la caja es el correcto (ligado); con R < R_c la caja da E > 0 aunque haya ligado.
  (c) Cruce de las curvas y(delta) de las cajas R y 2R (l = 1, 2):
        delta* - delta_c = (2l+1) An2 (1 - 2^{1-2l}) / (6 S R^{2l+1}),   y* = (2l+1) An2 R^{1-2l} [1 + (1-2^{1-2l})/3]/pi^2.
Metodo: disparo con u(R) = 0 (comun4.caja_disparo), con el numero de nodos comprobado; control con diferencias finitas.
Criterios fijados ANTES de correr (17-11-2026):
  (a) l = 1, 2: |Y(R_max) - 1| < 0.01 y |Y - 1| decrece con R; l = 0: |y(R_max) - 1/4| < 0.01.
  (b) R_c medido frente al predicho: error relativo < 1 % para Delta/delta_c <= 1e-4 (l >= 1) y, para l = 0,
      R_c frente a a_s (fase3 comun3.long_dispersion) < 1e-3 relativo.
  (c) delta* y y* frente a la prediccion: error relativo < 10 % en la caja mas grande.
  FD de control (h = 1/160, Richardson): |E_FD - E_disparo| < 1e-9 absoluto en el umbral para R <= 160.
Salida: resultados/43_cajas_l.json y _salida.txt.
"""
import math
import sys
import time

import numpy as np
from scipy.optimize import brentq

import comun4 as c

sys.path.insert(0, c.F3)
T0 = time.time()
c.Tee("43_cajas_l")
C40 = c.leer_json("40_controles_radial_l")["C_umbrales"]
K41 = c.leer_json("41_constantes_umbral")["constantes"]
out = dict(criterios=dict(a=0.01, b=0.01, b_l0=1e-3, c=0.10, fd=1e-9))


def caja(l, nr, delta, R, Eg):
    """Nivel de la caja con nr nodos interiores. Eg: estimacion (positiva o negativa)."""
    def nod(E):
        return c.u_en_R(l, delta, E, R, nodos=True)[1]
    escala = max(abs(Eg), 1e-300)
    lo, hi = Eg - escala, Eg + escala
    for _ in range(200):
        if nod(lo) <= nr:
            break
        lo -= escala; escala *= 2
    escala = max(abs(Eg), 1e-300)
    for _ in range(200):
        if nod(hi) >= nr + 1:
            break
        hi += escala; escala *= 2
    # biseccion en el numero de nodos hasta aislar el cambio de signo de u(R)
    for _ in range(200):
        if c.u_en_R(l, delta, lo, R) * c.u_en_R(l, delta, hi, R) < 0 and nod(lo) == nr and nod(hi) == nr + 1:
            break
        m = 0.5 * (lo + hi)
        if nod(m) <= nr:
            lo = m
        else:
            hi = m
    return c.caja_disparo(l, delta, R, lo, hi)


RS = [10, 20, 40, 80, 160, 320, 640, 1280, 2560]
# ------------------------------------------------------------------ (a) en el umbral
print("(a) Cajas en el umbral")
A = {}
for nom in ("1s", "2p", "3d"):
    e = c.ESTADOS[nom]; l, nr = e["l"], e["nr"]
    dc = C40[nom]["delta_c"]; K = K41[nom]
    filas = []
    for R in RS:
        Eg = math.pi**2 / (8 * R**2) if l == 0 else (2 * l + 1) * K["An2"] / (2 * R**(2 * l + 1))
        t = time.time()
        E = caja(l, nr, dc, R, Eg)
        f = dict(R=R, E=E, y=2 * R**2 * E / math.pi**2, t=time.time() - t)
        if l >= 1:
            f["Y"] = 2 * R**(2 * l + 1) * E / ((2 * l + 1) * K["An2"])
            f["E_pred"] = Eg
        filas.append(f)
        print(f"  {nom} R = {R:5d}: E = {E:+.10e}  y = 2R^2E/pi^2 = {f['y']:.6e}"
              + (f"  Y = {f['Y']:.6f}" if l >= 1 else "") + f"  ({f['t']:.1f} s)", flush=True)
    res = dict(filas=filas)
    if l == 0:
        res["pasa"] = bool(abs(filas[-1]["y"] - 0.25) < 0.01)
    else:
        dev = [abs(f["Y"] - 1) for f in filas]
        res["dev"] = dev
        Rs_ = np.array(RS[3:], float); dv = np.array([f["Y"] - 1 for f in filas[3:]])
        res["exponente_correccion"] = float(np.polyfit(np.log(Rs_), np.log(np.abs(dv)), 1)[0]) if np.all(dv != 0) else None
        res["pasa"] = bool(dev[-1] < 0.01 and all(dev[i + 1] < dev[i] for i in range(2, len(dev) - 1)))
        print(f"  {nom}: |Y-1| en R_max = {dev[-1]:.2e}; Y - 1 ~ R^p con p = {res['exponente_correccion']}; pasa = {res['pasa']}")
    A[nom] = res
out["a_umbral"] = A

# control FD en el umbral
print("\n  Control con diferencias finitas (h = 1/160 + Richardson) en el umbral")
fdc = []
for nom in ("2p", "3d", "1s"):
    e = c.ESTADOS[nom]; l, nr = e["l"], e["nr"]; dc = C40[nom]["delta_c"]
    for f in A[nom]["filas"]:
        if f["R"] > 640:
            continue
        r = c.fd_rich(c.V_yukawa_np(dc), l, f["R"], h=1 / 160, nev=1)
        r40 = c.fd_rich(c.V_yukawa_np(dc), l, f["R"], h=1 / 40, nev=1)
        z = dict(estado=nom, R=f["R"], E_disp=f["E"], E_fd160=r["E0"], E_fd40=r40["E0"], dif160=r["E0"] - f["E"],
                 dif40=r40["E0"] - f["E"])
        z["pasa"] = bool(abs(z["dif160"]) < 1e-9) if f["R"] <= 160 else None
        fdc.append(z)
        print(f"  {nom} R = {f['R']:4d}: E_disp = {f['E']:+.6e}  FD h=1/40 dif {z['dif40']:+.1e}  FD h=1/160 dif "
              f"{z['dif160']:+.1e}  (dif/E h=1/160: {z['dif160'] / f['E']:+.1e})", flush=True)
out["a_fd"] = fdc

# ------------------------------------------------------------------ (b) radio de cruce R_c
print("\n(b) Radio de caja en el que el nivel cruza E = 0 (ultimo nodo de la solucion de energia cero)")
import comun3  # noqa: E402  (solo long_dispersion, l = 0)
B = {}
for nom in ("1s", "2p", "3d"):
    e = c.ESTADOS[nom]; l, nr = e["l"], e["nr"]; dc = C40[nom]["delta_c"]; K = K41[nom]
    filas = []
    for k in range(4, 25 if l == 0 else 37, 4):
        Dr = 10**(-k / 4); D = dc * Dr
        if l == 0:
            pred = 1 / (K["pred"]["c0"] * D)
            a_s = comun3.long_dispersion(dc - D, Rf=max(80.0, 40.0 / dc)) if D / dc > 1e-6 else None
        else:
            pred = ((2 * l + 1) * K["An2"] / (2 * K["S"] * D))**(1 / (2 * l + 1))
            a_s = None
        Rc = c.nodo_energia_cero(l, dc - D, nr + 1, rmax=20 * pred + 200)
        f = dict(Delta_rel=Dr, R_c=Rc, R_c_pred=pred, rel=(Rc - pred) / pred if Rc else None)
        if a_s is not None:
            f["a_s"] = a_s; f["rel_a_s"] = (Rc - a_s) / a_s
        filas.append(f)
        print(f"  {nom} Delta/dc = {Dr:.0e}: R_c = {Rc:.6g}  predicho {pred:.6g}  rel {f['rel']:+.2e}"
              + (f"  a_s = {a_s:.6g} (rel {f['rel_a_s']:+.1e})" if a_s is not None else ""), flush=True)
    if l == 0:
        ok = [abs(f["rel_a_s"]) < 1e-3 for f in filas if "rel_a_s" in f]
    else:
        ok = [abs(f["rel"]) < 0.01 for f in filas if f["Delta_rel"] <= 1e-4 * (1 + 1e-9)]
    B[nom] = dict(filas=filas, pasa=bool(all(ok)))
    print(f"  {nom}: pasa = {B[nom]['pasa']}")
out["b_radio_cruce"] = B

# tabla practica: menor Delta/dc con signo fiable (E < 0) en cajas moderadas, y comprobacion directa
print("\n  Signo de E en cajas moderadas para Delta/dc = 1e-3 (ligado verdadero en los tres casos)")
sig = []
for nom in ("1s", "2p", "3d"):
    e = c.ESTADOS[nom]; l, nr = e["l"], e["nr"]; dc = C40[nom]["delta_c"]; K = K41[nom]
    D = dc * 1e-3
    for R in (25, 50, 100, 200, 400):
        Eg = (math.pi**2 / (8 * R**2) if l == 0 else (2 * l + 1) * K["An2"] / (2 * R**(2 * l + 1))) - (
            0.5 * (K["pred"]["c0"] * D)**2 if l == 0 else K["S"] * D)
        E = caja(l, nr, dc - D, R, Eg)
        Rc = [f for f in B[nom]["filas"] if abs(f["Delta_rel"] - 1e-3) < 1e-9][0]["R_c"]
        z = dict(estado=nom, R=R, E=E, signo_correcto=bool(E < 0), R_c=Rc, coherente_con_R_c=bool((E < 0) == (R > Rc)))
        sig.append(z)
        print(f"  {nom} R = {R:4d}: E = {E:+.4e}  signo correcto = {z['signo_correcto']}  (R_c = {Rc:.4g}; coherente = "
              f"{z['coherente_con_R_c']})", flush=True)
    # menor Delta/dc con E(R) < 0 para R = 50, 100, 200 (desde la ley de R_c)
for R in (50, 100, 200):
    fila = {}
    for nom in ("1s", "2p", "3d"):
        l = c.ESTADOS[nom]["l"]; dc = C40[nom]["delta_c"]; K = K41[nom]
        D = 1 / (K["pred"]["c0"] * R) if l == 0 else (2 * l + 1) * K["An2"] / (2 * K["S"] * R**(2 * l + 1))
        fila[nom] = D / dc
    out.setdefault("Delta_rel_minimo_signo_fiable", {})[str(R)] = fila
    print(f"  R = {R}: menor Delta/dc con signo fiable (ley de R_c): " + ", ".join(f"{k} {v:.2e}" for k, v in fila.items()))
out["signo_cajas_moderadas"] = sig

# ------------------------------------------------------------------ (c) cruce de y(R) y y(2R) para l = 1, 2
print("\n(c) Cruce de y = 2R^2E/pi^2 entre las cajas R y 2R")
Cc = {}
for nom in ("2p", "3d"):
    e = c.ESTADOS[nom]; l, nr = e["l"], e["nr"]; dc = C40[nom]["delta_c"]; K = K41[nom]
    filas = []
    for R in (10, 20, 40, 80, 160):
        q = 1 - 2.0**(1 - 2 * l)
        dpred = (2 * l + 1) * K["An2"] * q / (6 * K["S"] * R**(2 * l + 1))
        ypred = (2 * l + 1) * K["An2"] * R**(1 - 2 * l) * (1 + q / 3) / math.pi**2
        Eg1 = (2 * l + 1) * K["An2"] / (2 * R**(2 * l + 1))

        def g(d):
            E1 = caja(l, nr, d, R, Eg1 - K["S"] * (dc - d))
            E2 = caja(l, nr, d, 2 * R, Eg1 / 2**(2 * l + 1) - K["S"] * (dc - d))
            return R**2 * E1 - 4 * R**2 * E2
        t = time.time()
        a, b = dc, dc + 4 * dpred
        while g(b) * g(a) > 0:
            b = dc + 2 * (b - dc)
        ds = brentq(g, a, b, xtol=1e-14 * dc, rtol=8.9e-16)
        ys = 2 * R**2 * caja(l, nr, ds, R, Eg1) / math.pi**2
        f = dict(R=R, delta_estrella=ds, dif=ds - dc, dif_pred=dpred, rel_dif=(ds - dc - dpred) / dpred, y_estrella=ys,
                 y_pred=ypred, rel_y=(ys - ypred) / ypred, t=time.time() - t)
        filas.append(f)
        print(f"  {nom} R = {R:4d}/{2 * R}: delta* - delta_c = {ds - dc:+.4e} (pred {dpred:+.4e}, rel {f['rel_dif']:+.2e}); "
              f"y* = {ys:.5e} (pred {ypred:.5e}, rel {f['rel_y']:+.2e})  ({f['t']:.0f} s)", flush=True)
    Cc[nom] = dict(filas=filas, pasa=bool(abs(filas[-1]["rel_dif"]) < 0.10 and abs(filas[-1]["rel_y"]) < 0.10))
    print(f"  {nom}: pasa = {Cc[nom]['pasa']}")
out["c_cruces"] = Cc
out["t_total"] = time.time() - T0
c.guardar_json("43_cajas_l", out)
print(f"\nTiempo total {out['t_total']:.0f} s")
