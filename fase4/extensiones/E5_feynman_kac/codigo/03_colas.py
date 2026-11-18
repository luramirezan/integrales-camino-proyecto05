"""03_colas.py -- E5: colas pesadas del peso W = exp(Lambda) del Monte Carlo libre y exponente theta = delta/delta_c.

(1) Muestra universal X = delta * Lambda (partida Gamma(2, 1/delta), eta = 0.2, N = 1e7, semilla propia). W = exp(X/delta).
    Tasa de la cola exponencial de X por maxima verosimilitud en el 1 % superior: kappa_hat; theta_hat(delta) = delta kappa_hat;
    delta_c(MC) = 1/kappa_hat. Prediccion: P(X > x) = sum_k wbar_k e^{-x/delta_c(ks)} (01_referencia_edo.json).
(2) Kolmogorov-Smirnov de X frente a la mezcla para x >= x_min (truncamiento de la serie < 1e-4).
(3) Histogramas log-log de W (delta = 1.5, 2, 3, 4) frente a la densidad predicha sum wbar_k p_k w^{-p_k-1}.
(4) Media acumulada y varianza muestral frente a n: 20 replicas de 5e5; pendiente log-log de la mediana de la varianza
    (prediccion 2/theta - 1 si theta < 2) y de la dispersion de la media (prediccion 1/theta - 1 si theta < 2, -1/2 si no).
(5) Control independiente de la partida (C9b): r0 = 1 fijo, delta = 1.5, N = 2e6, cola de Lambda con tasa theta.
(6) Referencia de tamano finito para (4): el mismo estadistico (pendiente de la mediana de la varianza, 20 replicas de 5e5)
    calculado sobre 10 muestras de 1e7 tomadas de la ley EXACTA (mezcla de exponenciales). Da el valor esperado a n finito
    y su dispersion, para separar el efecto preasintotico del ruido del estadistico. Informativo: no cambia C11.
Salida: resultados/03_colas.json, resultados/03_colas_salida.txt.
"""
import json
import os
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fk_comun as fk  # noqa: E402

RES = os.path.join(AQUI, "../resultados")
REF = json.load(open(os.path.join(RES, "01_referencia_edo.json")))
T0 = time.perf_counter()
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.append(s)


def mle_cola(Y, frac=0.01):
    """Tasa de una cola exponencial: 1/mean(Y - u | Y > u), u = cuantil 1 - frac. Error asintotico tasa/sqrt(k)."""
    u = np.quantile(Y, 1 - frac)
    exc = Y[Y > u] - u
    k = exc.size
    tasa = 1.0 / exc.mean()
    return float(tasa), float(tasa / np.sqrt(k)), float(u), int(k)


out = {}
mez = REF["mezcla"]["3"]                      # wbar_k y delta_c(ks) no dependen de delta (escala exacta)
wbar = np.array(mez["w_k_gamma"])
dck = np.array(mez["delta_c_ks"])
out["mezcla_usada"] = dict(wbar=wbar.tolist(), delta_c_ks=dck.tolist(), suma=float(wbar.sum()))
DC = fk.DELTA_C

# ------------------------------------------------------------------ (1) muestra universal
N = 10_000_000
SEM = 202630
rng = np.random.default_rng(SEM)
r0 = rng.gamma(2.0, 1.0, N)
t = time.perf_counter()
X = fk.simular_libre(r0, 1.0, 0.2, 36.0, SEM + 1000)
out["muestra"] = dict(N=N, eta=0.2, semilla_r0=SEM, semilla_caminos=SEM + 1000, tiempo_s=time.perf_counter() - t,
                      E_X=float(X.mean()), err_E_X=float(X.std(ddof=1) / np.sqrt(N)))
log(f"(1) N={N}, eta=0.2, {out['muestra']['tiempo_s']:.1f} s; E[X] = {X.mean():.5f} +- {X.std()/np.sqrt(N):.5f} (exacto 1)")

kap, ekap, u, k = mle_cola(X, 0.01)
out["cola"] = dict(kappa=kap, err_kappa=ekap, umbral_x=u, k=k, delta_c_MC=1 / kap, err_delta_c_MC=ekap / kap ** 2,
                   kappa_pred=1 / DC, dev_sigmas=(kap - 1 / DC) / ekap)
log(f"(1) tasa de la cola de X (1 % superior, u = {u:.3f}, k = {k}): kappa = {kap:.5f} +- {ekap:.5f}; "
    f"1/delta_c = {1/DC:.5f} ({(kap-1/DC)/ekap:+.2f} sigma); delta_c(MC) = {1/kap:.5f} +- {ekap/kap**2:.5f}")
# sensibilidad al umbral (informativa)
sens = []
for fr in [0.05, 0.02, 0.01, 0.005, 0.002, 0.001]:
    kk, ee, uu, nk = mle_cola(X, fr)
    sens.append(dict(frac=fr, kappa=kk, err=ee, u=uu, k=nk))
out["cola_sensibilidad"] = sens
log("(1) sensibilidad al umbral:", [(s["frac"], round(s["kappa"], 4), round(s["err"], 4)) for s in sens])
# amplitud: P(X > x) e^{x/delta_c} en la cola frente a wbar_1
xs = np.linspace(3.0, 9.0, 13)
Fe = np.array([(X > x).mean() for x in xs])
amp = Fe * np.exp(xs / DC)
out["amplitud"] = dict(x=xs.tolist(), P_emp=Fe.tolist(), amp_emp=amp.tolist(), wbar1=float(wbar[0]),
                       P_pred=[float(np.sum(wbar * np.exp(-x / dck))) for x in xs])
log("(1) amplitud P(X>x) e^{x/delta_c} =", np.round(amp, 4).tolist(), f"frente a wbar_1 = {wbar[0]:.5f}")

tabla_theta = {}
for d in [1.2, 1.3, 1.5, 2.0, 2.5, 3.0, 4.0]:
    th = d * kap
    tabla_theta[f"{d:g}"] = dict(theta_pred=d / DC, theta_MC=th, err=d * ekap, dev_sigmas=(th - d / DC) / (d * ekap),
                                 var_finita=bool(d / DC > 2), media_finita=bool(d / DC > 1))
    log(f"(1) delta={d}: theta_MC = {th:.4f} +- {d*ekap:.4f}; delta/delta_c = {d/DC:.4f}")
out["theta"] = tabla_theta

# ------------------------------------------------------------------ (2) Kolmogorov-Smirnov contra la mezcla
resto = 1 - wbar.sum()
x_min = float(dck[-1] * np.log(max(resto, 1e-12) / 1e-4)) if resto > 1e-4 else 0.0
Xs = np.sort(X)
xg = Xs[Xs >= x_min]
Femp = 1 - (np.searchsorted(Xs, xg, side="right") / N)
Fpred = np.array([0.0])
Fpred = np.sum(wbar[None, :] * np.exp(-xg[:, None] / dck[None, :]), axis=1) if xg.size < 3_000_000 else None
if Fpred is None:
    # en bloques para no gastar memoria
    Fpred = np.concatenate([np.sum(wbar[None, :] * np.exp(-c[:, None] / dck[None, :]), axis=1)
                            for c in np.array_split(xg, 50)])
D = np.abs(Femp - Fpred)
ks = float(np.sqrt(N) * D.max())
out["ks"] = dict(x_min=x_min, resto_serie=float(resto), D=float(D.max()), sqrtN_D=ks, x_en_D=float(xg[np.argmax(D)]),
                 fraccion_muestra_usada=float(xg.size / N))
log(f"(2) KS para x >= {x_min:.4f} ({xg.size/N:.3f} de la muestra): D = {D.max():.2e}, sqrt(N) D = {ks:.2f} "
    f"(en x = {xg[np.argmax(D)]:.4f})")
# curva de supervivencia para la figura (submuestreada)
qx = np.concatenate([np.linspace(0, 2, 60), np.linspace(2, Xs[-1], 140)])
out["supervivencia"] = dict(x=qx.tolist(), P_emp=[float(1 - np.searchsorted(Xs, x, side='right') / N) for x in qx],
                            P_pred=[float(np.sum(wbar * np.exp(-x / dck))) for x in qx])
del Xs, xg, Femp, Fpred, D

# ------------------------------------------------------------------ (3) histogramas de W
hist = {}
for d in [1.5, 2.0, 3.0, 4.0]:
    W = np.exp(X / d)
    bins = np.geomspace(1.0, W.max() * 1.0001, 60)
    h, e = np.histogram(W, bins=bins)
    dens = h / (N * np.diff(e))
    wc = np.sqrt(e[1:] * e[:-1])
    pk = d / dck
    pred = np.sum(wbar[None, :] * pk[None, :] * wc[:, None] ** (-pk[None, :] - 1), axis=1)
    hist[f"{d:g}"] = dict(w=wc.tolist(), dens=dens.tolist(), cuentas=h.tolist(), pred=pred.tolist(), W_max=float(W.max()))
out["histogramas"] = hist

# ------------------------------------------------------------------ (4) media acumulada y varianza frente a n
nrep, nb = 20, 500_000
ns = np.unique(np.geomspace(100, nb, 40).astype(int))
serie = {}
for d in [1.5, 2.0, 2.5, 3.0, 4.0]:
    th = d / DC
    W = np.exp(X / d)
    acum = np.cumsum(W) / np.arange(1, N + 1)
    nn_acum = np.unique(np.geomspace(10, N, 200).astype(int))
    var_rep = np.empty((nrep, ns.size))
    med_rep = np.empty((nrep, ns.size))
    for i in range(nrep):
        b = W[i * nb:(i + 1) * nb]
        c1 = np.cumsum(b)
        c2 = np.cumsum(b * b)
        n_ = ns.astype(float)
        m = c1[ns - 1] / n_
        var_rep[i] = (c2[ns - 1] - n_ * m * m) / (n_ - 1)
        med_rep[i] = m
    vmed = np.median(var_rep, axis=0)
    sel = ns >= 1000
    pend_var = float(np.polyfit(np.log(ns[sel]), np.log(vmed[sel]), 1)[0])
    iqr = np.subtract(*np.percentile(med_rep, [75, 25], axis=0))
    pend_med = float(np.polyfit(np.log(ns[sel]), np.log(iqr[sel]), 1)[0])
    pred_var = 2 / th - 1 if th < 2 else 0.0
    pred_med = 1 / th - 1 if th < 2 else -0.5
    serie[f"{d:g}"] = dict(theta=th, pend_var=pend_var, pred_pend_var=pred_var, pend_dispersion_media=pend_med,
                           pred_pend_media=pred_med, n=ns.tolist(), var_mediana=vmed.tolist(),
                           var_p10=np.percentile(var_rep, 10, axis=0).tolist(),
                           var_p90=np.percentile(var_rep, 90, axis=0).tolist(), iqr_media=iqr.tolist(),
                           n_acum=nn_acum.tolist(), media_acum=acum[nn_acum - 1].tolist(),
                           phi_media_exacta=REF["identidad_estimador"][f"{d:g}"]["E_phi"])
    log(f"(4) delta={d} (theta={th:.3f}): pendiente var = {pend_var:+.3f} (pred {pred_var:+.3f}); "
        f"pendiente dispersion media = {pend_med:+.3f} (pred {pred_med:+.3f}); media acumulada final "
        f"{acum[-1]:.4f} frente a {REF['identidad_estimador'][f'{d:g}']['E_phi']:.4f}")
out["series"] = serie
del W, X

# ------------------------------------------------------------------ (5) partida fija r0 = 1, delta = 1.5
d = 1.5
N5 = 2_000_000
Lam = fk.simular_libre(np.ones(N5), d, 0.2, 36.0 / d, 202640)
th5, e5, u5, k5 = mle_cola(Lam, 0.01)
phi1 = REF["perfil"]["1.5"]["phi_M1"][3]
W = np.exp(Lam)
out["partida_fija"] = dict(delta=d, r0=1.0, N=N5, semilla=202640, theta_MC=th5, err=e5, umbral=u5, k=k5,
                           theta_pred=d / DC, dev_sigmas=(th5 - d / DC) / e5, media_W=float(W.mean()), phi_edo=phi1)
log(f"(5) partida r0=1, delta=1.5: theta_MC = {th5:.4f} +- {e5:.4f} frente a {d/DC:.4f} ({(th5-d/DC)/e5:+.2f} sigma); "
    f"media de W = {W.mean():.4f} (phi(1) = {phi1:.4f}, varianza infinita)")

# ------------------------------------------------------------------ (6) referencia a n finito con la ley exacta
def pendiente_estadistico(W, nrep=20, nb=500_000):
    ns_ = np.unique(np.geomspace(100, nb, 40).astype(int))
    V = np.empty((nrep, ns_.size))
    for i in range(nrep):
        b = W[i * nb:(i + 1) * nb]
        c1, c2 = np.cumsum(b), np.cumsum(b * b)
        n_ = ns_.astype(float)
        m = c1[ns_ - 1] / n_
        V[i] = (c2[ns_ - 1] - n_ * m * m) / (n_ - 1)
    vm = np.median(V, axis=0)
    sel_ = ns_ >= 1000
    return float(np.polyfit(np.log(ns_[sel_]), np.log(vm[sel_]), 1)[0])


wn = wbar / wbar.sum()
ref6 = {f"{d:g}": [] for d in [1.5, 2.0, 2.5, 3.0, 4.0]}
for sm in range(10):
    rg = np.random.default_rng(202660 + sm)
    kk = rg.choice(wn.size, N, p=wn)
    Xm = rg.exponential(dck[kk])
    for d in ref6:
        ref6[d].append(pendiente_estadistico(np.exp(Xm / float(d))))
    del kk, Xm
out["referencia_tamano_finito"] = {}
for d, v in ref6.items():
    v = np.array(v)
    mc = out["series"][d]["pend_var"]
    out["referencia_tamano_finito"][d] = dict(pendientes=v.tolist(), media=float(v.mean()), desv=float(v.std(ddof=1)),
                                              pend_MC=mc, z=float((mc - v.mean()) / v.std(ddof=1)))
    log(f"(6) delta={d}: pendiente con la ley exacta a n finito = {v.mean():+.3f} +- {v.std(ddof=1):.3f} "
        f"(min {v.min():+.3f}, max {v.max():+.3f}); MC {mc:+.3f} (z = {(mc - v.mean())/v.std(ddof=1):+.2f})")

out["tiempo_s"] = time.perf_counter() - T0
log(f"tiempo total {out['tiempo_s']:.1f} s")
json.dump(out, open(os.path.join(RES, "03_colas.json"), "w"), indent=1)
open(os.path.join(RES, "03_colas_salida.txt"), "w").write("\n".join(LOG) + "\n")
