"""02_validacion_mc.py -- E5: validacion del Monte Carlo libre (sin muestreo por importancia) donde la varianza es finita.

(a) Muestra universal X = delta * Lambda con partida r0 ~ Gamma(2, 1/delta), R_in = 36/delta, dt = eta^2 r^2. El esquema es
    covariante de escala, asi que la misma muestra vale para todo delta: W = exp(X/delta) y
    a(delta) = -(2/delta^2) mean(W). Se corre con eta = 0.8, 0.4, 0.2, 0.1 (semillas distintas, independientes).
    Controles: E[X] = 1 exacto (C16); a(delta) frente a la EDO en delta = 2.5, 3, 4; orden del sesgo en eta (C8b) y
    extrapolacion eta -> 0 (C7).
(b) Perfil phi(r) en delta = 3 y 4 en la rejilla r = 0.05 ... 8 (partida fija), eta = 0.2, frente a la EDO.
(c) Documentacion del fallo del trapecio (delta = 3, eta = 0.8, 0.4, 0.2): media del estimador que explota.
Salida: resultados/02_validacion_mc.json, resultados/02_validacion_mc_salida.txt.
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


def media_err(w):
    """media y error estandar; ademas el error por 50 bloques (sensible a colas pesadas)."""
    n = w.size
    m = float(w.mean())
    e = float(w.std(ddof=1) / np.sqrt(n))
    b = w[: (n // 50) * 50].reshape(50, -1).mean(1)
    eb = float(b.std(ddof=1) / np.sqrt(50))
    return m, e, eb


out = dict(semillas={}, universal={}, perfil={}, trapecio={})
ETAS = [0.8, 0.4, 0.2, 0.1]
NS = {0.8: 10_000_000, 0.4: 10_000_000, 0.2: 10_000_000, 0.1: 3_000_000}
SEM = {0.8: 202611, 0.4: 202612, 0.2: 202613, 0.1: 202614}
DVAL = [2.5, 3.0, 4.0]

# ------------------------------------------------------------------ (a) muestra universal
dref = 1.0                                   # se simula en delta = 1 (la ley de X = delta Lambda no depende de delta)
for eta in ETAS:
    N = NS[eta]
    rng = np.random.default_rng(SEM[eta])
    r0 = rng.gamma(2.0, 1.0 / dref, N)
    t = time.perf_counter()
    Lam, pas = fk.simular_libre(r0, dref, eta, 36.0 / dref, SEM[eta] + 1000, devolver_pasos=True)
    X = dref * Lam
    tt = time.perf_counter() - t
    mX, eX, ebX = media_err(X)
    res = dict(N=N, semilla_r0=SEM[eta], semilla_caminos=SEM[eta] + 1000, tiempo_s=tt, pasos_medios=float(pas.mean()),
               pasos_max=int(pas.max()), E_X=mX, err_E_X=eX, dev_E_X_sigmas=(mX - 1.0) / eX, X_max=float(X.max()),
               a={})
    log(f"(a) eta={eta}: N={N}, {tt:.1f} s, pasos medios {pas.mean():.1f} (max {pas.max()}); "
        f"E[X] = {mX:.5f} +- {eX:.5f} ({(mX-1)/eX:+.2f} sigma); X_max = {X.max():.3f}")
    for d in DVAL + [2.0, 1.5]:
        W = np.exp(X / d)
        mW, eW, ebW = media_err(W)
        a_mc = -(2 / d ** 2) * mW
        ea = 2 / d ** 2 * eW
        eab = 2 / d ** 2 * ebW
        a_edo = REF["a_delta"][f"{d:g}"]["a_M1_disparo"]
        res["a"][f"{d:g}"] = dict(a_mc=a_mc, err=ea, err_bloques=eab, a_edo=a_edo, dif_rel=(a_mc - a_edo) / abs(a_edo),
                                  dev_sigmas=(a_mc - a_edo) / ea, W_max=float(W.max()))
        log(f"    delta={d}: a_MC = {a_mc:+.6f} +- {ea:.6f} (bloques {eab:.6f}); EDO {a_edo:+.6f}; "
            f"dif_rel = {(a_mc-a_edo)/abs(a_edo):+.2e} ({(a_mc-a_edo)/ea:+.2f} sigma)")
    out["universal"][f"{eta:g}"] = res
    # curva a(delta) para la figura (solo delta > 2 delta_c tiene barra de error con sentido)
    if eta == 0.2:
        dd = np.linspace(2.45, 4.5, 30)
        cur = []
        for d in dd:
            W = np.exp(X / d)
            cur.append([float(d), float(-(2 / d ** 2) * W.mean()), float(2 / d ** 2 * W.std(ddof=1) / np.sqrt(N)),
                        fk.a_disparo(d)])
        out["curva_a_mc_eta02"] = cur
        dd2 = np.linspace(1.25, 2.4, 24)
        cur2 = []
        for d in dd2:
            W = np.exp(X / d)
            cur2.append([float(d), float(-(2 / d ** 2) * W.mean()), fk.a_disparo(d)])
        out["curva_a_mc_eta02_varianza_infinita"] = cur2
    del Lam, X, r0, pas

# sesgo en eta y extrapolacion: ajuste a(eta) = a0 + c eta^p con p libre (tres finos) y con p = 4 fijo
ext = {}
for d in DVAL:
    a_e = np.array([out["universal"][f"{e:g}"]["a"][f"{d:g}"]["a_mc"] for e in ETAS])
    s_e = np.array([out["universal"][f"{e:g}"]["a"][f"{d:g}"]["err"] for e in ETAS])
    a_edo = REF["a_delta"][f"{d:g}"]["a_M1_disparo"]
    sesgo = a_e - a_edo
    # orden observado con los tres eta mas gruesos (0.8, 0.4, 0.2), donde el sesgo supera al ruido
    p_obs = float(np.log2(abs(sesgo[0]) / abs(sesgo[1]))) if sesgo[1] != 0 else float("nan")
    p_obs2 = float(np.log2(abs(sesgo[1]) / abs(sesgo[2]))) if sesgo[2] != 0 else float("nan")
    # ajuste ponderado con p = 4 sobre eta <= 0.4: a = a0 + c eta^4
    e3 = np.array(ETAS[1:])
    Am = np.vstack([np.ones(3), e3 ** 4]).T
    Wt = np.diag(1 / s_e[1:] ** 2)
    cov = np.linalg.inv(Am.T @ Wt @ Am)
    coef = cov @ Am.T @ Wt @ a_e[1:]
    a0, ea0 = float(coef[0]), float(np.sqrt(cov[0, 0]))
    ext[f"{d:g}"] = dict(eta=ETAS, a_mc=a_e.tolist(), err=s_e.tolist(), sesgo=sesgo.tolist(), sesgo_rel=(sesgo / abs(a_edo)).tolist(),
                         p_obs_08_04=p_obs, p_obs_04_02=p_obs2, a_extrap_p4=a0, err_extrap=ea0, c_eta4=float(coef[1]),
                         dev_extrap_sigmas=(a0 - a_edo) / ea0, a_edo=a_edo)
    log(f"(a) delta={d}: sesgo_rel por eta {np.round(sesgo/abs(a_edo), 5).tolist()}; orden 0.8/0.4 = {p_obs:.2f}, "
        f"0.4/0.2 = {p_obs2:.2f}; extrapolado (p=4) a0 = {a0:+.6f} +- {ea0:.6f} frente a {a_edo:+.6f} "
        f"({(a0-a_edo)/ea0:+.2f} sigma)")
out["extrapolacion"] = ext

# ------------------------------------------------------------------ (b) perfil phi(r) con partida fija
R_GRID = REF["perfil"]["3"]["r"]
for d in [3.0, 4.0]:
    filas = []
    for j, r in enumerate(R_GRID):
        N = 400_000
        sem = 20262100 + int(10 * d) * 10 + j
        Lam = fk.simular_libre(np.full(N, r), d, 0.2, 36.0 / d, sem)
        W = np.exp(Lam)
        m, e, eb = media_err(W)
        pe = REF["perfil"][f"{d:g}"]["phi_M1"][j]
        filas.append(dict(r=r, N=N, semilla=sem, phi_mc=m, err=e, err_bloques=eb, phi_edo=pe, dev_sigmas=(m - pe) / e))
        log(f"(b) delta={d} r={r}: phi_MC = {m:.5f} +- {e:.5f}; EDO {pe:.5f} ({(m-pe)/e:+.2f} sigma)")
    out["perfil"][f"{d:g}"] = filas

# ------------------------------------------------------------------ (c) el trapecio explota
for eta in [0.8, 0.4, 0.2]:
    N = 1_000_000
    rng = np.random.default_rng(202620)
    r0 = rng.gamma(2.0, 1 / 3.0, N)
    Lam = fk.simular_libre(r0, 3.0, eta, 12.0, 202621, metodo="trapecio")
    with np.errstate(over="ignore"):
        W = np.exp(Lam)
        a_tr = float(-(2 / 9) * W.mean())
    srt = np.sort(Lam)[::-1]
    out["trapecio"][f"{eta:g}"] = dict(N=N, a_trapecio=a_tr, Lambda_max=float(srt[0]), Lambda_top5=srt[:5].tolist(),
                                       frac_Lambda_mayor_10=float((Lam > 10).mean()), a_edo=REF["a_delta"]["3"]["a_M1_disparo"])
    log(f"(c) trapecio delta=3 eta={eta}: a = {a_tr:.4e}; Lambda max = {srt[0]:.2f}; top5 = {np.round(srt[:5], 2).tolist()}")

out["tiempo_s"] = time.perf_counter() - T0
log(f"tiempo total {out['tiempo_s']:.1f} s")
json.dump(out, open(os.path.join(RES, "02_validacion_mc.json"), "w"), indent=1)
open(os.path.join(RES, "02_validacion_mc_salida.txt"), "w").write("\n".join(LOG) + "\n")
