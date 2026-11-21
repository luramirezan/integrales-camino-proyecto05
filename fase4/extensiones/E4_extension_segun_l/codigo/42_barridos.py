"""42_barridos.py -- E4, tarea 2: barridos cerca de cada umbral (1s, 2s, 2p, 3d) sin caja (disparo).

Para Delta = delta_c - delta = delta_c x 10^{-k/4}: E, kappa = sqrt(-2E), <r>, <r^2>, <e^{-delta r}> (= dE/d delta,
Hellmann-Feynman). l = 0: k = 4..28 (Delta/delta_c de 1e-1 a 1e-7); l >= 1: k = 4..36 (hasta 1e-9).
Controles internos: dE/d delta por diferencias (Delta +- 1e-3 Delta) frente a Hellmann-Feynman en 3 puntos por estado;
diferencias finitas (h = 1/40 + Richardson, caja R = 30/kappa) en Delta/delta_c = 1e-2 y 1e-3.

Criterios fijados ANTES de correr (17-11-2026), ventana asintotica = las dos ultimas decadas de Delta de cada barrido:
  exponentes de potencia: |p_ajuste - p_predicho| < 0.01 (l = 0: E 2, <r> -1, <r^2> -2 en kappa;
                           l >= 1: E 1; l = 1: <r^2> -1; l = 2: <r> y <r^2> con |p| < 0.01);
  l = 1, <r>: (i) el exponente local d ln<r>/d ln(1/kappa) baja de forma monotona en todo el barrido (no es potencia),
              (ii) la pendiente del ajuste <r> = a ln(1/kappa) + b en la ventana difiere de An2 en menos de 1 %,
              (iii) la formula refinada del script 41 reproduce <r> con error relativo < 1e-3 en la ventana;
  coeficientes (ultimo punto): l = 0: kappa/Delta frente a c0, <r>kappa y <r^2>kappa^2 frente a 1/2, error rel < 1e-3;
              l >= 1: -E/Delta frente a S (< 1e-3); l = 1: <r^2>kappa frente a 5An2/4 (< 1e-3);
              l = 2: <r>, <r^2> frente a los valores de energia cero (< 1e-3).
  Hellmann-Feynman: error relativo < 1e-6; FD frente a disparo: E rel < 1e-5, <r> rel < 1e-4.
Salida: resultados/42_barridos.json y _salida.txt.
"""
import math
import time

import numpy as np

import comun4 as c

T0 = time.time()
c.Tee("42_barridos")
C40 = c.leer_json("40_controles_radial_l")["C_umbrales"]
K41 = c.leer_json("41_constantes_umbral")["constantes"]
U41 = c.leer_json("41_constantes_umbral")["universales"]
CRIT = dict(p=0.01, log_pend=0.01, log_formula=1e-3, coef=1e-3, HF=1e-6, FD_E=1e-5, FD_r=1e-4)
out = dict(criterios=CRIT, estados={})


def barrido(nom):
    e = c.ESTADOS[nom]
    l, nr = e["l"], e["nr"]
    dc = C40[nom]["delta_c"]
    ks = range(4, 29) if l == 0 else range(4, 37)
    pts = []
    kap = None
    for k in ks:
        D = dc * 10**(-k / 4)
        if kap is None:
            kg = K41[nom]["pred"]["c0"] * D if l == 0 else math.sqrt(2 * K41[nom]["S"] * D)
        else:
            kg = kap * (10**(-0.25))**(1.0 if l == 0 else 0.5)
        s = c.ligado(l, dc - D, kg, nr=nr)
        s["Delta"], s["Delta_rel"], s["k"] = D, D / dc, k
        kap = s["kappa"]
        pts.append(s)
    return pts


def ajuste(x, y):
    """Pendiente de y frente a x por minimos cuadrados y su error estandar."""
    A = np.vstack([x, np.ones_like(x)]).T
    p, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    n = len(x)
    s2 = float(np.sum((y - A @ p)**2) / max(n - 2, 1))
    cov = s2 * np.linalg.inv(A.T @ A)
    return float(p[0]), float(p[1]), float(np.sqrt(cov[0, 0]))


for nom in ("1s", "2s", "2p", "3d"):
    t = time.time()
    e = c.ESTADOS[nom]
    l, nr = e["l"], e["nr"]
    dc = C40[nom]["delta_c"]
    K = K41[nom]
    P = barrido(nom)
    D = np.array([p["Delta"] for p in P]); Dr = D / dc
    kap = np.array([p["kappa"] for p in P]); E = np.array([p["E"] for p in P])
    r1 = np.array([p["r_med"] for p in P]); r2 = np.array([p["r2_med"] for p in P])
    HF = np.array([p["HF"] for p in P])
    print(f"\n=== {nom} (l = {l}), delta_c = {dc:.13f}, {len(P)} puntos, {time.time() - t:.0f} s")
    print("   Delta/dc        kappa            E                <r>              <r^2>           nodos  frac_cola")
    for p in P:
        print(f"   {p['Delta_rel']:.3e}  {p['kappa']:.10e}  {p['E']:+.10e}  {p['r_med']:.10e}  {p['r2_med']:.10e}  "
              f"{p['nodos']}  {p['frac_cola']:.2e}")
    # ventana asintotica: las dos ultimas decadas de Delta
    w = Dr <= Dr[-1] * 100 * (1 + 1e-9)
    w1 = Dr <= Dr[-1] * 10 * (1 + 1e-9)                   # ultima decada
    w2 = w & (Dr >= Dr[-1] * 10 * (1 - 1e-9))              # penultima decada
    res = dict(l=l, nr=nr, delta_c=dc, puntos=P, ventana_Delta_rel=[float(Dr[w].min()), float(Dr[w].max())])
    fits = {}
    for nomb, x, y, pp in (("E", np.log(D), np.log(-E), 2.0 if l == 0 else 1.0),
                           ("r_med", np.log(kap), np.log(r1), -1.0 if l == 0 else (None if l == 1 else 0.0)),
                           ("r2_med", np.log(kap), np.log(r2), -2.0 if l == 0 else (-1.0 if l == 1 else 0.0))):
        p, b, se = ajuste(x[w], y[w])
        p1 = ajuste(x[w1], y[w1])[0]; p2 = ajuste(x[w2], y[w2])[0]
        err = se + abs(p1 - p2)
        f = dict(p=p, err=err, err_estandar=se, p_ultima_decada=p1, p_penultima_decada=p2, p_pred=pp)
        if pp is not None:
            f["pasa"] = bool(abs(p - pp) < CRIT["p"])
        fits[nomb] = f
        print(f"   ajuste {nomb}: p = {p:+.5f} +- {err:.1e} (ultima decada {p1:+.5f}, penultima {p2:+.5f}); "
              f"predicho {pp}" + (f"  pasa = {f['pasa']}" if pp is not None else ""))
    # exponentes locales entre puntos vecinos
    loc = dict(E=list(np.diff(np.log(-E)) / np.diff(np.log(D))),
               r_med=list(np.diff(np.log(r1)) / np.diff(np.log(1 / kap))),
               r2_med=list(np.diff(np.log(r2)) / np.diff(np.log(1 / kap))))
    res["exponentes_locales"] = loc
    res["ajustes"] = fits
    # coeficientes en el ultimo punto
    co = {}
    if l == 0:
        co["kappa_sobre_Delta"] = dict(med=kap[-1] / D[-1], pred=K["pred"]["c0"])
        co["r_kappa"] = dict(med=r1[-1] * kap[-1], pred=0.5)
        co["r2_kappa2"] = dict(med=r2[-1] * kap[-1]**2, pred=0.5)
    else:
        co["menos_E_sobre_Delta"] = dict(med=-E[-1] / D[-1], pred=K["S"])
        if l == 1:
            co["r2_kappa"] = dict(med=r2[-1] * kap[-1], pred=1.25 * K["An2"])
        if l == 2:
            co["r_med"] = dict(med=r1[-1], pred=K["r_med0"])
            co["r2_med"] = dict(med=r2[-1], pred=K["r2_med0"])
            co["r2_pendiente_kappa"] = dict(med=(r2[-1] - K["r2_med0"]) / kap[-1], pred=-35 / 36 * K["An2"])
    for k_, v in co.items():
        v["rel"] = (v["med"] - v["pred"]) / abs(v["pred"])
        v["pasa"] = bool(abs(v["rel"]) < CRIT["coef"]) if k_ != "r2_pendiente_kappa" else None
        print(f"   coeficiente {k_}: medido {v['med']:.8g}  predicho {v['pred']:.8g}  rel {v['rel']:+.2e}")
    res["coeficientes"] = co
    # l = 1: crecimiento logaritmico de <r>
    if l == 1:
        a, b, se = ajuste(np.log(1 / kap[w]), r1[w])
        refin = (K["C0"] + K["An2"] * (np.log(1 / kap) + U41["K_1_exacto"])) * (1 + 1.5 * K["An2"] * kap)
        lider = K["C0"] + K["An2"] * (np.log(1 / kap) + U41["K_1_exacto"])
        Ecorr = -(K["S"] * D + K["An2"] / 2 * (2 * K["S"] * D)**1.5)
        r2pred = 1.25 * K["An2"] / kap + K["D0"] + 15 / 8 * K["An2"]**2
        lg = dict(pendiente=a, ordenada=b, err=se, An2=K["An2"], rel_pendiente=(a - K["An2"]) / K["An2"],
                  r_formula_lider=list(lider), r_formula_refinada=list(refin),
                  rel_refinada=list((r1 - refin) / r1), rel_lider=list((r1 - lider) / r1),
                  max_rel_refinada_ventana=float(np.abs((r1 - refin) / r1)[w].max()),
                  E_refinada=list(Ecorr), rel_E_refinada=list((E - Ecorr) / np.abs(E)),
                  r2_refinada=list(r2pred), rel_r2_refinada=list((r2 - r2pred) / r2),
                  exponente_local_monotono=bool(np.all(np.diff(loc["r_med"]) < 0)),
                  exponente_local_pred=list(K["An2"] / r1))
        # potencia ajustada en la primera y en la ultima mitad del barrido (si fuera potencia, coincidirian)
        hlf = len(P) // 2
        lg["p_potencia_primera_mitad"] = ajuste(np.log(1 / kap[:hlf]), np.log(r1[:hlf]))[0]
        lg["p_potencia_segunda_mitad"] = ajuste(np.log(1 / kap[hlf:]), np.log(r1[hlf:]))[0]
        lg["pasa"] = bool(lg["exponente_local_monotono"] and abs(lg["rel_pendiente"]) < CRIT["log_pend"]
                          and lg["max_rel_refinada_ventana"] < CRIT["log_formula"])
        res["log"] = lg
        print(f"   <r> = a ln(1/kappa) + b en la ventana: a = {a:.6f} +- {se:.1e} (An2 = {K['An2']:.6f}, rel "
              f"{lg['rel_pendiente']:+.2e}), b = {b:.5f}")
        print(f"   formula refinada: error relativo maximo en la ventana {lg['max_rel_refinada_ventana']:.2e}; "
              f"solo termino lider: {np.abs(lg['rel_lider'])[w].max():.2e}")
        print(f"   exponente local d ln<r>/d ln(1/kappa): de {loc['r_med'][0]:.4f} a {loc['r_med'][-1]:.4f}, monotono = "
              f"{lg['exponente_local_monotono']}; potencia ajustada en la 1a mitad {lg['p_potencia_primera_mitad']:.4f}, "
              f"en la 2a {lg['p_potencia_segunda_mitad']:.4f}")
        print(f"   E con correccion Delta^(3/2): error relativo en el ultimo punto {lg['rel_E_refinada'][-1]:+.2e}, en el "
              f"primero {lg['rel_E_refinada'][0]:+.2e};  <r^2> refinada: {lg['rel_r2_refinada'][-1]:+.2e}")
    # Hellmann-Feynman frente a diferencias en tres puntos
    hf = []
    for i in (2, len(P) // 2, len(P) - 1):
        d0 = dc - D[i]; eta = 1e-3 * D[i]
        Ep = c.ligado(l, d0 + eta, kap[i], nr=nr)["E"]; Em = c.ligado(l, d0 - eta, kap[i], nr=nr)["E"]
        num = (Ep - Em) / (2 * eta)
        hf.append(dict(Delta_rel=Dr[i], dEdd_num=num, HF=HF[i], rel=(num - HF[i]) / HF[i]))
        print(f"   Hellmann-Feynman Delta/dc = {Dr[i]:.1e}: dE/dd numerico {num:.10e}  <e^(-d r)> {HF[i]:.10e}  "
              f"rel {(num - HF[i]) / HF[i]:+.1e}")
    res["hellmann_feynman"] = hf
    # diferencias finitas en caja grande
    fdc = []
    for dr_ in (1e-2, 1e-3):
        i = int(np.argmin(np.abs(Dr - dr_)))
        R = min(max(60.0, 30.0 / kap[i]), 40000.0)
        f = c.fd_rich(c.V_yukawa_np(dc - D[i]), l, R, h=1 / 40, nev=nr + 1)
        key = "E0" if nr == 0 else "E1"
        z = dict(Delta_rel=Dr[i], R=R, E_fd=f[key], E_disp=E[i], rel_E=(f[key] - E[i]) / abs(E[i]))
        if nr == 0:
            z.update(r_fd=f["r_med"], r_disp=r1[i], rel_r=(f["r_med"] - r1[i]) / r1[i],
                     r2_fd=f["r2_med"], r2_disp=r2[i], rel_r2=(f["r2_med"] - r2[i]) / r2[i])
        z["pasa"] = bool(abs(z["rel_E"]) < CRIT["FD_E"] and (nr > 0 or abs(z["rel_r"]) < CRIT["FD_r"]))
        fdc.append(z)
        print(f"   FD (R = {R:.0f}) Delta/dc = {Dr[i]:.0e}: E rel {z['rel_E']:+.1e}"
              + (f", <r> rel {z['rel_r']:+.1e}, <r^2> rel {z['rel_r2']:+.1e}" if nr == 0 else "") + f"  pasa = {z['pasa']}")
    res["fd"] = fdc
    res["t"] = time.time() - t
    out["estados"][nom] = res
    c.guardar_json("42_barridos", out)

out["t_total"] = time.time() - T0
c.guardar_json("42_barridos", out)
print(f"\nTiempo total {out['t_total']:.0f} s")
