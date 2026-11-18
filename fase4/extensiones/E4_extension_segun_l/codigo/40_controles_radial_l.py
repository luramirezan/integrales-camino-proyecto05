"""40_controles_radial_l.py -- E4, tarea 1: solucionador radial para l > 0 y sus controles.

A. Diferencias finitas (radial.py de la Fase 2 con V_ef = V + l(l+1)/2r^2) en Coulomb: 1s, 2s, 2p, 3d frente a
   E_n = -1/(2n^2), <r> = [3n^2 - l(l+1)]/2, <r^2> = n^2[5n^2 + 1 - 3l(l+1)]/2; orden aparente de la malla.
B. Disparo de alta precision (comun4.Disparo, exterior de Whittaker) en los mismos estados de Coulomb.
C. Umbrales delta_c de 1s, 2s, 2p, 3d con la solucion de energia cero (B = 0), su convergencia numerica
   (rtol, r0, r_ext) y una estimacion independiente con diferencias finitas (ajuste de E(delta) cerca del umbral).
D. Diferencias finitas frente a disparo para Yukawa lejos y cerca del umbral.
Criterios fijados ANTES de correr (17-11-2026):
  A: |E_FD - E_exacto| < 1e-8 con h = 1/40 y Richardson; orden aparente de la malla entre 1.8 y 2.2.
  B: |E_disparo - E_exacto| < 1e-12 y |<r> - exacto| < 1e-9.
  C: |delta_c - valor del encargo| < 1e-8 (el encargo da 8 decimales); convergencia numerica < 1e-11;
     diferencias finitas compatibles a 1e-6.
  D: |E_FD - E_disparo|/|E| < 1e-6 y |<r>_FD - <r>_disparo|/<r> < 1e-5 (malla h = 1/40 con Richardson, caja 30/kappa).
Salida: resultados/40_controles_radial_l.json y _salida.txt.
"""
import math
import time

import numpy as np

import comun4 as c

T0 = time.time()
c.Tee("40_controles_radial_l")
out = dict(criterios=dict(A_E=1e-8, A_orden=(1.8, 2.2), B_E=1e-12, B_r=1e-9, C_pred=1e-8, C_num=1e-11, C_fd=1e-6,
                          D_E=1e-6, D_r=1e-5))
VC = lambda r: -1.0 / r
COUL = [("1s", 1, 0, 0, 60.0), ("2s", 2, 0, 1, 80.0), ("2p", 2, 1, 0, 80.0), ("3d", 3, 2, 0, 120.0)]


def exacto(n, l):
    return dict(E=-0.5 / n**2, r_med=(3 * n * n - l * (l + 1)) / 2, r2_med=n * n * (5 * n * n + 1 - 3 * l * (l + 1)) / 2)


# ------------------------------------------------------------------ A. diferencias finitas en Coulomb
print("A. Diferencias finitas (radial.py con V_ef), Coulomb, h = 1/40 + Richardson")
A = {}
for nom, n, l, nr, R in COUL:
    ex = exacto(n, l)
    d = c.fd_rich(VC, l, R, h=1 / 40, nev=nr + 1)
    key = "E0" if nr == 0 else "E1"
    fila = dict(n=n, l=l, R=R, E=d[key], E_exacto=ex["E"], dif_E=d[key] - ex["E"], dif_E_h=d[key + "_h2"] - ex["E"])
    if nr == 0:
        fila.update(r_med=d["r_med"], dif_r=d["r_med"] - ex["r_med"], r2_med=d["r2_med"], dif_r2=d["r2_med"] - ex["r2_med"])
    X, p = c.radial.orden_aparente(c.V_ef(VC, l), R, [1 / 20, 1 / 40, 1 / 80, 1 / 160], clave=key, exacto=ex["E"],
                                   nev=nr + 1)
    fila["orden_aparente"] = p
    fila["pasa"] = bool(abs(fila["dif_E"]) < out["criterios"]["A_E"] and 1.8 < p[-1] < 2.2)
    A[nom] = fila
    print(f"  {nom}: E = {fila['E']:.12f} (exacto {ex['E']:.12f}), dif = {fila['dif_E']:+.2e} "
          f"[sin Richardson h/2: {fila['dif_E_h']:+.2e}]  orden = {', '.join(f'{x:.3f}' for x in p)}"
          + (f"  <r> dif = {fila['dif_r']:+.1e}  <r^2> dif = {fila['dif_r2']:+.1e}" if nr == 0 else "")
          + f"  pasa = {fila['pasa']}", flush=True)
out["A_fd_coulomb"] = A

# ------------------------------------------------------------------ B. disparo en Coulomb
print("\nB. Disparo (Frobenius + Whittaker), Coulomb")
B = {}
for nom, n, l, nr, R in COUL:
    ex = exacto(n, l)
    t = time.time()
    s = c.ligado(l, 0.0, (1.0 / n) * 1.03, nr=nr)
    fila = dict(E=s["E"], dif_E=s["E"] - ex["E"], r_med=s["r_med"], dif_r=s["r_med"] - ex["r_med"],
                r2_med=s["r2_med"], dif_r2=s["r2_med"] - ex["r2_med"], nodos=s["nodos"], salto=s["salto_dlog"],
                t=time.time() - t)
    fila["pasa"] = bool(abs(fila["dif_E"]) < 1e-12 and abs(fila["dif_r"]) < 1e-9 and s["nodos"] == nr)
    B[nom] = fila
    print(f"  {nom}: E dif = {fila['dif_E']:+.2e}  <r> dif = {fila['dif_r']:+.2e}  <r^2> dif = {fila['dif_r2']:+.2e}  "
          f"nodos = {s['nodos']}  pasa = {fila['pasa']}  ({fila['t']:.1f} s)", flush=True)
out["B_disparo_coulomb"] = B

# ------------------------------------------------------------------ C. umbrales
print("\nC. Umbrales por la solucion de energia cero")
C = {}
for nom, e in c.ESTADOS.items():
    l = e["l"]
    dc = c.umbral(l, *e["br"])
    fila = dict(l=l, delta_c=dc, encargo=c.PRED.get(nom, c.DELTA_C_1S_REF))
    fila["dif_encargo"] = dc - fila["encargo"]
    # convergencia numerica: rtol, r0, r_ext
    var = {}
    rt0 = c.RTOL
    c.RTOL = 1e-11
    var["rtol_1e-11"] = c.umbral(l, *e["br"]) - dc
    c.RTOL = rt0
    rext0 = c.r_externo
    c.r_externo = lambda d: 55.0 / d
    var["r_ext_55/delta"] = c.umbral(l, *e["br"]) - dc
    c.r_externo = rext0
    var["r0_1e-4"] = c.umbral(l, *e["br"], r0=1e-4) - dc        # arranque de Frobenius en 1e-4 en vez de 1e-3
    fila["variaciones"] = var
    fila["conv_num_max"] = max(abs(v) for v in var.values())
    C[nom] = fila
    print(f"  {nom} (l={l}): delta_c = {dc:.13f}  encargo {fila['encargo']}  dif = {fila['dif_encargo']:+.1e}  "
          f"variaciones num.: " + ", ".join(f"{k} {v:+.1e}" for k, v in var.items()), flush=True)

# estimacion independiente con diferencias finitas: E(delta) en caja grande y ajuste con la forma del umbral
print("\n  Estimacion independiente de delta_c con diferencias finitas (h = 1/40 + Richardson, R = 30/kappa)")
for nom, e in c.ESTADOS.items():
    l, nr, dc = e["l"], e["nr"], C[nom]["delta_c"]
    fr = np.array([3.2e-2, 1.6e-2, 8e-3, 4e-3]) if l == 0 else np.array([8e-3, 4e-3, 2e-3, 1e-3])
    ds = dc * (1 - fr)
    Es = []
    for d in ds:
        # caja: kappa del disparo como guia del tamano (solo fija R)
        Eg = -0.5 * (0.7 * dc * fr[list(ds).index(d)])**2 if l == 0 else -0.15 * dc * fr[list(ds).index(d)]
        R = min(max(60.0, 30.0 / math.sqrt(-2 * Eg)), 40000.0)
        h = 1 / 40 if R <= 4000 else 1 / 20
        r = c.fd_rich(c.V_yukawa_np(d), l, R, h=h, nev=nr + 1)
        Es.append(r["E0" if nr == 0 else "E1"])
    Es = np.array(Es)
    from scipy.optimize import least_squares
    if l == 0:
        y = np.sqrt(-2 * Es)          # kappa = a (dc - d) + b (dc - d)^2
        f = lambda p: p[1] * (p[0] - ds) + p[2] * (p[0] - ds)**2 - y
    elif l == 1:                       # |E| = S D + b D^{3/2}
        y = -Es
        f = lambda p: p[1] * (p[0] - ds) + p[2] * np.abs(p[0] - ds)**1.5 - y
    else:                              # |E| = S D + b D^2
        y = -Es
        f = lambda p: p[1] * (p[0] - ds) + p[2] * (p[0] - ds)**2 - y
    sol = least_squares(f, [dc * 1.00001, 1.0, 0.0], x_scale=[1e-6, 1, 1], xtol=1e-15, ftol=1e-15)
    C[nom]["fd"] = dict(deltas=ds, E=Es, delta_c_fd=sol.x[0], dif=sol.x[0] - dc, params=sol.x[1:],
                        residuo_max=float(np.abs(sol.fun).max()))
    C[nom]["pasa"] = bool(abs(C[nom]["dif_encargo"]) < 1e-8 and C[nom]["conv_num_max"] < 1e-11
                          and abs(C[nom]["fd"]["dif"]) < 1e-6)
    print(f"  {nom}: delta_c(FD) = {sol.x[0]:.10f}  dif con disparo = {sol.x[0] - dc:+.1e}  pasa C = {C[nom]['pasa']}",
          flush=True)
out["C_umbrales"] = C

# ------------------------------------------------------------------ D. FD frente a disparo en Yukawa
print("\nD. Diferencias finitas frente a disparo (Yukawa)")
D = []
casos = [("2p", 0.10), ("2p", 0.20), ("2p", None), ("3d", 0.05), ("3d", 0.085), ("3d", None), ("2s", 0.20), ("2s", None),
         ("1s", 0.80), ("1s", None)]
for nom, d in casos:
    e = c.ESTADOS[nom]
    l, nr, dc = e["l"], e["nr"], C[nom]["delta_c"]
    if d is None:
        d = dc * (1 - 1e-3)
    kg = 0.5 if l == 0 else 0.2
    # guia de kappa: barrido corto desde un valor seguro
    s = None
    for kk in (0.9, 0.6, 0.4, 0.25, 0.15, 0.08, 0.04, 0.02, 0.01, 0.005, 0.002, 0.001, 5e-4):
        try:
            s = c.ligado(l, d, kk, nr=nr)
            break
        except Exception:
            continue
    R = min(max(60.0, 30.0 / s["kappa"]), 20000.0)
    f = c.fd_rich(c.V_yukawa_np(d), l, R, h=1 / 40, nev=nr + 1)
    key = "E0" if nr == 0 else "E1"
    fila = dict(estado=nom, delta=d, R=R, E_disparo=s["E"], E_fd=f[key], dif_rel_E=(f[key] - s["E"]) / abs(s["E"]))
    if nr == 0:
        fila.update(r_disparo=s["r_med"], r_fd=f["r_med"], dif_rel_r=(f["r_med"] - s["r_med"]) / s["r_med"],
                    r2_disparo=s["r2_med"], r2_fd=f["r2_med"], dif_rel_r2=(f["r2_med"] - s["r2_med"]) / s["r2_med"])
    fila["pasa"] = bool(abs(fila["dif_rel_E"]) < 1e-6 and (nr > 0 or abs(fila["dif_rel_r"]) < 1e-5))
    D.append(fila)
    print(f"  {nom} delta = {d:.8f} R = {R:.0f}: E_disp = {s['E']:+.10e} E_FD = {f[key]:+.10e} rel = {fila['dif_rel_E']:+.1e}"
          + (f"  <r> {s['r_med']:.6f} / {f['r_med']:.6f} rel = {fila['dif_rel_r']:+.1e}" if nr == 0 else "")
          + f"  pasa = {fila['pasa']}", flush=True)
out["D_fd_vs_disparo"] = D
out["t_total"] = time.time() - T0
c.guardar_json("40_controles_radial_l", out)
print(f"\nTiempo total {out['t_total']:.0f} s")
