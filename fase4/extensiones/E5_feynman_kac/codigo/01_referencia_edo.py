"""01_referencia_edo.py -- E5: referencia determinista a energia cero y ley exacta del funcional de Feynman-Kac.

Partes
  (1) a(delta) con tres metodos independientes: M1 disparo lineal DOP853 desde Frobenius, M2 fase variable de
      Calogero (Riccati, da/dr = 2V (r-a)^2), M3 Nystrom de la ecuacion integral phi = 1 + G0 q phi (con sustraccion
      del quiebre del nucleo). Y el modulo de la Fase 3 (comun3.long_dispersion) como cuarto testigo.
  (2) Perfil phi(r) por M1 y M3 en la rejilla del Monte Carlo.
  (3) Identidad del estimador de a: a = -(2/delta^2) E_{r ~ Gamma(2, 1/delta)}[phi(r)].
  (4) Polos p_k de E[e^{p Lambda}] (ceros de la pendiente alpha(p)): p_k = delta/delta_c(ks); pesos w_k de la mezcla
      de exponenciales, en r fijo y promediados sobre la partida Gamma. Tail theta = p_1 = delta/delta_c.
  (5) Control exacto: pozo cuadrado q = 1_{r<1} (tiempo de estancia en la bola unidad de Ciesielski-Taylor):
      E_0[e^{pT}] = 1/cos(sqrt(2p)), p_k = (k-1/2)^2 pi^2/2, w_k = (-1)^{k+1} 4/((2k-1) pi).
  (6) Momentos del estimador libre: E[W^2] = E_Gamma[phi_2] (gauge de 2q, finita solo si delta > 2 delta_c);
      E[Lambda] exacto (S(r) en forma cerrada) para medir el sesgo de discretizacion sin colas.
  (7) Muestreo por importancia: delta_T con la regla fijada antes (a_T = 1.25 a); cota de la varianza relativa
      E[phi_T phi]/E[phi]^2 - 1; mapa de finitud de la varianza en (delta, delta_T): el segundo momento es la gauge de
      2 q_delta - q_deltaT, se busca el delta_T maximo; y el ansatz 1 + A/(r+b) con cuspide.
Salida: resultados/01_referencia_edo.json y resultados/01_referencia_edo_salida.txt.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import roots_genlaguerre

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "../../../../fase3/codigo"))
sys.path.insert(0, os.path.join(AQUI, "../../../../fase2/codigo"))
import fk_comun as fk  # noqa: E402
import comun3  # noqa: E402

RES = os.path.join(AQUI, "../resultados")
T0 = time.perf_counter()
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


out = {}
DELTAS = [1.2, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0]
R_GRID = [0.05, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

# ---------------------------------------------------------------- (1) a(delta), tres metodos + Fase 3
tab = {}
for d in DELTAS:
    a1 = fk.a_disparo(d)
    a2 = fk.a_fase_variable(d)
    _, a3 = fk.phi_nystrom(d, [1.0])
    a4 = comun3.long_dispersion(d, Rf=max(80.0, 60.0 / d))
    tab[f"{d:g}"] = dict(a_M1_disparo=a1, a_M2_fase_variable=a2, a_M3_nystrom=a3, a_fase3_comun3=a4,
                         dif_rel_M2=(a2 - a1) / abs(a1), dif_rel_M3=(a3 - a1) / abs(a1), dif_rel_F3=(a4 - a1) / abs(a1),
                         theta=d / fk.DELTA_C)
    log(f"(1) delta={d:4.2f}  a_M1={a1:+.10f}  a_M2={a2:+.10f}  a_M3={a3:+.10f}  a_F3={a4:+.10f}  "
        f"dif_rel M2={tab[f'{d:g}']['dif_rel_M2']:.1e} M3={tab[f'{d:g}']['dif_rel_M3']:.1e}  theta={d/fk.DELTA_C:.4f}")
out["a_delta"] = tab
out["a_120_fase3_texto"] = -142.9
log(f"(1) a(1.20) = {tab['1.2']['a_M1_disparo']:.4f} frente a -142.9 de la Fase 3 (LEEME)")

# curva densa para la figura y pendiente c = -d(1/a)/d delta en delta_c (compara con kappa ~ 0.741 (delta_c - delta))
dd = np.concatenate([np.linspace(1.192, 1.3, 40), np.linspace(1.3, 4.5, 80)[1:]])
out["curva_a"] = dict(delta=dd.tolist(), a=[fk.a_disparo(x) for x in dd])
h = 1e-4
c_pend = -(1 / fk.a_disparo(fk.DELTA_C + 2 * h) - 1 / fk.a_disparo(fk.DELTA_C + h)) / h
out["pendiente_inv_a"] = dict(c=c_pend, nota="1/a ~ -c (delta - delta_c); Fase 3: kappa ~ 0.741 (delta_c - delta)")
log(f"(1) pendiente c = -d(1/a)/d delta cerca de delta_c (diferencia hacia delante, h = 1e-4): {c_pend:.4f}")

# ---------------------------------------------------------------- (2) perfil phi(r): M1 frente a M3
perf = {}
for d in DELTAS:
    p1, alpha = fk.phi_edo(d, R_GRID)
    p3, _ = fk.phi_nystrom(d, R_GRID)
    perf[f"{d:g}"] = dict(r=R_GRID, phi_M1=p1.tolist(), phi_M3=p3.tolist(),
                          dif_max_abs=float(np.max(np.abs(p1 - p3))), phi0=float(fk.phi_edo(d, [1e-7])[0][0]))
    log(f"(2) delta={d:4.2f}  phi(r)={np.round(p1, 6).tolist()}  max|M1-M3|={perf[f'{d:g}']['dif_max_abs']:.1e}")
    rr = np.linspace(0.01, 12, 300)
    perf[f"{d:g}"]["denso_r"] = rr.tolist()
    perf[f"{d:g}"]["denso_phi"] = fk.phi_edo(d, rr)[0].tolist()
out["perfil"] = perf

# ---------------------------------------------------------------- (3) identidad del estimador de a
xl, wl = roots_genlaguerre(120, 1)            # int_0^inf x e^{-x} f(x) dx
ident = {}
for d in DELTAS:
    ph = fk.phi_edo(d, xl / d)[0]
    Ephi = float(np.sum(wl * ph))               # E_{r ~ Gamma(2, 1/d)}[phi(r)]  (int x e^{-x} = 1)
    a_id = -(2 / d ** 2) * Ephi
    ident[f"{d:g}"] = dict(E_phi=Ephi, a_identidad=a_id, dif_rel=(a_id - tab[f"{d:g}"]["a_M1_disparo"]) / abs(a_id))
    log(f"(3) delta={d:4.2f}  -(2/d^2) E_Gamma[phi] = {a_id:+.10f}  dif_rel = {ident[f'{d:g}']['dif_rel']:.1e}")
out["identidad_estimador"] = ident

# ---------------------------------------------------------------- (4) polos y pesos de la mezcla
mez = {}
for d in DELTAS:
    qf = lambda r, d=d: fk.q_yuk(r, d)
    Rf = 60.0 / d
    pk = fk.polos(qf, Rf, p_max=d * 160.0, n_scan=1600)
    wr = []
    wg = []
    for p in pk:
        w, _, _ = fk.pesos_mezcla(qf, Rf, p, np.array(R_GRID))
        wl_, _, _ = fk.pesos_mezcla(qf, Rf, p, xl / d)
        wr.append(w.tolist())
        wg.append(float(np.sum(wl * wl_)))
    dck = [d / p for p in pk]
    mez[f"{d:g}"] = dict(p_k=pk, delta_c_ks=dck, w_k_en_r=wr, r=R_GRID, w_k_gamma=wg,
                         suma_w_gamma=float(np.sum(wg)), theta=pk[0])
    log(f"(4) delta={d:4.2f}  {len(pk)} polos; p_1={pk[0]:.8f} (delta/delta_c={d/fk.DELTA_C:.8f}), p_2={pk[1]:.6f}; "
        f"delta_c(1s,2s,3s)={dck[0]:.10f},{dck[1]:.8f},{dck[2]:.8f}; w_gamma[:4]={np.round(wg[:4], 5).tolist()} "
        f"suma={np.sum(wg):.6f}")
out["mezcla"] = mez
dc1 = np.mean([mez[k]["delta_c_ks"][0] for k in mez])
dc2 = np.mean([mez[k]["delta_c_ks"][1] for k in mez])
out["delta_c_desde_polos"] = dict(dc1_medio=dc1, dc2_medio=dc2,
                                  dc1_disp=float(np.ptp([mez[k]["delta_c_ks"][0] for k in mez])),
                                  dc2_disp=float(np.ptp([mez[k]["delta_c_ks"][1] for k in mez])),
                                  err_rel_dc1=(dc1 - fk.DELTA_C) / fk.DELTA_C, err_rel_dc2=(dc2 - 0.3102093) / 0.3102093)
log(f"(4) delta_c(1s) desde los polos = {dc1:.12f} (ref {fk.DELTA_C}), delta_c(2s) = {dc2:.10f} (ref 0.3102093)")

# ---------------------------------------------------------------- (5) control exacto de Ciesielski-Taylor
qsq = lambda r: (np.asarray(r) < 1.0) * 1.0
pk = fk.polos(qsq, 2.0, 130.0, n_scan=600, cortes=[1.0])
ct = []
for k, p in enumerate(pk[:5], 1):
    w, _, _ = fk.pesos_mezcla(qsq, 2.0, p, [1e-7], cortes=[1.0])
    pe = (k - 0.5) ** 2 * np.pi ** 2 / 2
    we = (-1) ** (k + 1) * 4 / ((2 * k - 1) * np.pi)
    ct.append(dict(k=k, p=p, p_exacto=pe, w=float(w[0]), w_exacto=we, err_p=(p - pe) / pe, err_w=(w[0] - we) / we))
    log(f"(5) Ciesielski-Taylor k={k}: p={p:.12f} exacto={pe:.12f}; w={w[0]:+.12f} exacto={we:+.12f}")
out["ciesielski_taylor"] = ct

# ---------------------------------------------------------------- (6) momentos del estimador libre
mom = {}
S = lambda r, d: 2 * (1 - np.exp(-d * r) * (1 + d * r)) / (d * d * r) + 2 * np.exp(-d * r) / d   # E_r[Lambda]
for d in DELTAS:
    ELam = float(np.sum(wl * S(xl / d, d)))
    m = dict(E_Lambda_gamma=ELam, E_Lambda_r={f"{r:g}": float(S(r, d)) for r in R_GRID})
    if d / 2 > fk.DELTA_C:
        # phi_2 = gauge de 2q: solucion regular con p = 2
        Rf = 60.0 / d
        s = fk.regular(lambda r: fk.q_yuk(r, d), p=2.0, Rf=Rf, r_eval=xl / d)
        phi2 = s["u"] / (s["upR"] * (xl / d))
        EW2 = float(np.sum(wl * phi2))
        EW = ident[f"{d:g}"]["E_phi"]
        s2 = fk.regular(lambda r: fk.q_yuk(r, d), p=2.0, Rf=Rf, r_eval=np.array(R_GRID))
        phi2r = s2["u"] / (s2["upR"] * np.array(R_GRID))
        phir = np.array(perf[f"{d:g}"]["phi_M1"])
        m.update(E_W2_gamma=EW2, var_rel_gamma=EW2 / EW ** 2 - 1, sigma_a_por_raizN=2 / d ** 2 * np.sqrt(EW2 - EW ** 2),
                 var_W_r=(phi2r - phir ** 2).tolist())
        log(f"(6) delta={d:4.2f}  E[Lambda]_Gamma={ELam:.6f}  E[W^2]={EW2:.6f}  var_rel={EW2/EW**2-1:.4f}  "
            f"sigma(a)*sqrt(N)={m['sigma_a_por_raizN']:.4f}")
    else:
        m.update(E_W2_gamma=float("inf"))
        log(f"(6) delta={d:4.2f}  E[Lambda]_Gamma={ELam:.6f}  E[W^2] = infinito (delta/2 = {d/2:.3f} <= delta_c)")
    mom[f"{d:g}"] = m
out["momentos_libre"] = mom

# ---------------------------------------------------------------- (7) muestreo por importancia: teoria
mi = {}
for d in [3.0, 2.0, 1.5, 1.3, 1.25, 1.2, 1.195, 1.192]:
    dT = fk.dT_para_razon(d, 1.25)
    aT = fk.a_disparo(dT)
    phT = fk.phi_edo(dT, xl / d)[0]
    ph = fk.phi_edo(d, xl / d)[0]
    cota = float(np.sum(wl * phT * ph) / np.sum(wl * ph) ** 2 - 1)
    mi[f"{d:g}"] = dict(delta_T=dT, a=fk.a_disparo(d), a_T=aT, cota_var_rel_gamma=cota,
                        cota_var_rel_r0=float(fk.phi_edo(dT, [1e-6])[0][0] / fk.phi_edo(d, [1e-6])[0][0] - 1))
    log(f"(7) delta={d:6.3f}  delta_T={dT:.8f}  a={mi[f'{d:g}']['a']:+.4f}  a_T={aT:+.4f}  "
        f"cota var_rel (Gamma) = {cota:.4f}")
out["mi_regla"] = mi


def alpha_qeff(qeff, Rf):
    s = fk.regular(qeff, p=1.0, Rf=Rf)
    return s["upR"]


def nodos_qeff(qeff, Rf):
    rr = np.linspace(1e-6, Rf, 20001)
    s = fk.regular(qeff, p=1.0, Rf=Rf, r_eval=rr)
    return int(np.sum(np.sign(s["u"][1:]) != np.sign(s["u"][:-1])))


# mapa: delta_T maximo con varianza finita (2 q_delta - q_deltaT subcritico)
mapa = []
for d in np.linspace(1.2, 2.36, 30):
    Rf = 60.0 / min(d, 2.0)
    F = lambda dT, d=d: alpha_qeff(lambda r: 2 * fk.q_yuk(r, d) - fk.q_yuk(r, dT), Rf)
    hi = 1e4
    if F(hi) > 0:
        dmax = float("inf")
    else:
        dmax = brentq(F, d, hi, xtol=1e-10)
    mapa.append(dict(delta=float(d), delta_T_max=dmax, delta_T_regla=fk.dT_para_razon(float(d), 1.25)))
log("(7) mapa delta_T_max (varianza finita si delta_c < delta_T < delta_T_max):",
    [(round(m["delta"], 3), round(m["delta_T_max"], 4)) for m in mapa[::5]])
out["mapa_varianza_MI"] = mapa

# ansatz 1 + A/(r+b) con cuspide (b^2 + A b - A = 0)
ans = []
for d in [3.0, 1.5, 1.3]:
    a = fk.a_disparo(d)
    for c in [0.8, 1.0, 1.25, 2.0]:
        A = -c * a
        b = (-A + np.sqrt(A * A + 4 * A)) / 2
        corr = lambda r, A=A, b=b: A * b / (r * (r + b) ** 2 * (r + b + A))
        qeff = lambda r, d=d, corr=corr: 2 * fk.q_yuk(r, d) - corr(r)
        Rf = 60.0 / d
        al = alpha_qeff(qeff, Rf)
        nn = nodos_qeff(qeff, Rf)
        rr = np.geomspace(1e-4, 40, 4000)
        EL = corr(rr) - fk.q_yuk(rr, d)
        ans.append(dict(delta=d, c=c, A=A, b=b, alpha_qeff=al, nodos=nn, var_finita=bool(al > 0 and nn == 0),
                        EL_min=float(EL.min()), EL_max=float(EL.max()), supersolucion=bool(EL.min() >= 0)))
        log(f"(7) ansatz delta={d} A={A:.4f} (c={c}) b={b:.4f}: alpha={al:+.4e} nodos={nn} -> varianza "
            f"{'finita' if al > 0 and nn == 0 else 'INFINITA'}; E_L en [{EL.min():+.3f}, {EL.max():+.3f}]")
out["ansatz"] = ans
out["umbral_supersolucion_ansatz"] = dict(delta=4 / np.e, nota="1 + A/(r+b) puede ser supersolucion (E_L >= 0 en todo r) "
                                          "solo si delta >= 4/e (con A -> infinito y b = 1/delta)")

out["tiempo_s"] = time.perf_counter() - T0
log(f"tiempo total {out['tiempo_s']:.1f} s")
json.dump(out, open(os.path.join(RES, "01_referencia_edo.json"), "w"), indent=1)
open(os.path.join(RES, "01_referencia_edo_salida.txt"), "w").write("\n".join(LOG) + "\n")
