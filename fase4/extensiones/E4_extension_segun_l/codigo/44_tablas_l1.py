"""44_tablas_l1.py -- E4, tarea 4 (preparacion): tablas de la accion de pares de Coulomb en la onda l = 1.

Calcula (y guarda en resultados/tablas/) las tablas U_1 para eps = 0.2, 0.1, 0.05 con h_tab = 0.01 y 0.005
(pares_l.tabla_richardson_l) y hace los controles:
  T1  ln K_l con l = 0 coincide con pares.logKD (nucleo con imagen de la Fase 2): |dif| < 1e-12.
  T2  el nucleo libre de la red con centrifugo reproduce el K_1 exacto: error de red O(h_tab^2) (cociente de los
      errores de h_tab = 0.01 y 0.005 entre 3.5 y 4.5) y, con Richardson, |ln rho0 - ln K_1| < 1e-5 en la banda
      |r - r'| <= 3 sqrt(eps).
  T3  Richardson de U_1: |U_R - U_0.005| < 1e-4 (estimacion del error que queda en U_1) en la banda 3 sqrt(eps).
  T4  continuidad en r = R_TAB = 10 con la aproximacion de extremos + Wigner-Kirkwood: |U_tabla - U_extremos| < 1e-6
      en r en [9, 9.9] (diagonal y |r-r'| <= sqrt(eps)).
  T5  peso positivo: ningun rho_l de la red <= 0 en la tabla (n_no_positivos = 0).
Criterios fijados ANTES de correr (17-11-2026).
Salida: resultados/44_tablas_l1.json y _salida.txt.
"""
import time

import numpy as np

import comun4 as c
import pares_l as pl
import pares

T0 = time.time()
c.Tee("44_tablas_l1")
L = 1
out = dict(criterios=dict(T1=1e-12, T2_cociente=(3.5, 4.5), T2_rich=1e-5, T3=1e-4, T4=1e-6), eps={})

# T1
a = np.linspace(0.01, 12, 400)[:, None]; b = np.linspace(0.01, 12, 400)[None, :]
for eps in (0.2, 0.05):
    d = pl.logK_l(a, b, eps, 0) - pares.logKD(a, b, eps)
    m = np.isfinite(d) & (np.abs(a - b) < 7 * np.sqrt(eps))
    out.setdefault("T1", {})[str(eps)] = float(np.abs(d[m]).max())
print("T1 ln K_0 frente a pares.logKD:", out["T1"], "pasa =", all(v < 1e-12 for v in out["T1"].values()))
out["T1_pasa"] = bool(all(v < 1e-12 for v in out["T1"].values()))

for eps in (0.2, 0.1, 0.05):
    t = time.time()
    tb = pl.tabla_richardson_l(L, eps)
    r = tb.r
    nb3 = int(np.floor(3 * np.sqrt(eps) / tb.h))
    nb1 = int(np.floor(np.sqrt(eps) / tb.h))
    res = dict(info=dict(tb.info), nt=tb.nt, nb=tb.nb, t=time.time() - t)
    # T2: nucleo libre de la red frente al exacto
    D1, D2 = tb.D1[:, :nb3 + 1], tb.D2[:, :nb3 + 1]
    DR = (4 * D2 - D1) / 3
    ok = np.isfinite(D1) & np.isfinite(D2)
    res["T2_max_h01"] = float(np.abs(D1[ok]).max())
    res["T2_max_h005"] = float(np.abs(D2[ok]).max())
    res["T2_cociente"] = res["T2_max_h01"] / res["T2_max_h005"]
    res["T2_max_rich"] = float(np.abs(DR[ok]).max())
    res["T2_pasa"] = bool(3.5 < res["T2_cociente"] < 4.5 and res["T2_max_rich"] < 1e-5)
    # T3
    U2, UR = tb.U2[:, :nb3 + 1], tb.Ub[:, :nb3 + 1]
    ok = np.isfinite(U2) & np.isfinite(UR)
    res["T3_max"] = float(np.abs(UR[ok] - U2[ok]).max())
    res["T3_pasa"] = bool(res["T3_max"] < 1e-4)
    # T4
    k0 = int(round(9.0 / tb.h)) - 1; k1 = int(round(9.9 / tb.h)) - 1
    difs = []
    for m in range(0, nb1 + 1):
        k = np.arange(k0, min(k1, tb.nt - 1 - m) + 1)
        Ut = tb.Ub[k, m]
        Ue = pares.U_extremos(r[k], r[k + m], eps)
        difs.append(float(np.nanmax(np.abs(Ut - Ue))))
    res["T4_max"] = max(difs)
    res["T4_pasa"] = bool(res["T4_max"] < 1e-6)
    res["T5_no_positivos"] = tb.info["n_no_positivos"]
    res["T5_pasa"] = bool(sum(tb.info["n_no_positivos"]) == 0)
    # ilustracion: U_1 frente a U_0 (Fase 2) en la diagonal
    t0 = pares.tabla_richardson(eps)
    res["U_diag_muestra"] = {f"{x:g}": dict(U1=float(tb.Ub[int(round(x / tb.h)) - 1, 0]),
                                             U0=float(t0.Ub[int(round(x / t0.h)) - 1, 0]),
                                             extremos=float(pares.U_extremos(x, x, eps)))
                             for x in (0.01, 0.05, 0.1, 0.5, 1.0, 3.0, 9.0)}
    out["eps"][str(eps)] = res
    print(f"\neps = {eps}: nt = {tb.nt}, nb = {tb.nb}, tiempo {res['t']:.0f} s (cache {tb.info['cache']})")
    print(f"  T2 error de red del nucleo libre l=1: h=0.01 {res['T2_max_h01']:.2e}, h=0.005 {res['T2_max_h005']:.2e}, "
          f"cociente {res['T2_cociente']:.2f}, Richardson {res['T2_max_rich']:.2e}  pasa = {res['T2_pasa']}")
    print(f"  T3 |U_R - U_0.005| max {res['T3_max']:.2e}  pasa = {res['T3_pasa']}")
    print(f"  T4 continuidad en R_TAB: max |U_tabla - U_extremos| (r en [9, 9.9]) = {res['T4_max']:.2e}  pasa = {res['T4_pasa']}")
    print(f"  T5 elementos no positivos: {res['T5_no_positivos']}  pasa = {res['T5_pasa']}")
    for x, v in res["U_diag_muestra"].items():
        print(f"     r = r' = {x:>5}: U_1 = {v['U1']:+.8f}  U_0 = {v['U0']:+.8f}  extremos = {v['extremos']:+.8f}")
out["t_total"] = time.time() - T0
c.guardar_json("44_tablas_l1", out)
print(f"\nTiempo total {out['t_total']:.0f} s")
