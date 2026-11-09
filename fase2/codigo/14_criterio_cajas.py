"""14_criterio_cajas.py -- Proyecto 05 (Yukawa), Fase 2: condicion (c) del criterio de cajas (seccion 9.6).

Unidades hbar = m = g = 1, V = -e^{-delta r}/r. delta in {1.15, 1.18, 1.20}, R in {50,100,200,400,800}.
Transferencia en banda (transferencia.py) con la accion de pares de Coulomb (tablas U_C con Richardson
en h_tab = 0.01/0.005, pares.py), eps in {0.2, 0.1, 0.05} y Nystrom h in {0.02, 0.04} en TODAS las cajas.
  - Richardson en h con exponente 4 (seccion 11.4): E_hR = (16 E_0.02 - E_0.04)/15.
  - Extrapolacion eps -> 0 con ley eps^2: E_ext = E(0.05) + [E(0.05) - E(0.1)]/3.
  - Observables <r>/R y F_1/2: extrapolacion eps^2 de los valores con h = 0.02.
  - Control extra: orden de la malla Nystrom cerca del umbral (delta = 1.18, R = 50 y 100, eps = 0.1,
    h = 0.04, 0.02, 0.01).
Referencia: fase2/resultados/10_radial.json, clave cajas_9_6 (DF h = 1/40 y 1/80 con Richardson).
Autovalor: eigsh en modo shift-invert (sigma cerca del extremo superior); se comprueba que el autovector
es de signo constante (Perron-Frobenius: T >= 0 => es el del MAYOR autovalor) y el residuo.
Determinista (sin numeros aleatorios; las semillas 20262000+k no se usan).
Salida: fase2/resultados/14_cajas.json, fase2/figuras/14_cajas.png.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse.linalg import eigsh

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pares                      # noqa: E402
import transferencia as tr        # noqa: E402
import radial                     # noqa: E402

T0 = time.perf_counter()
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
DELTAS = (1.15, 1.18, 1.20)
RS = (50, 100, 200, 400, 800)
EPSS = (0.2, 0.1, 0.05)
HS = (0.02, 0.04)
TERNAS = ((50, 100, 200), (100, 200, 400), (200, 400, 800))
print(f"Carga (loadavg) al empezar: {os.getloadavg()}")

rad_all = json.load(open(os.path.join(RES, "10_radial.json")))["cajas_9_6"]


def rad(delta, R):
    c = rad_all[f"{delta:g}"][f"R{R}"]
    # V3 (hallazgo H13 de V2): error de malla del radial tambien para <r>/R y F_1/2 (|Richardson - h/2|)
    return dict(E0=c["E0"], err=abs(c["E0"] - c["E0_h2"]), dE_rel=c["dE_rel"],
                r_sobre_R=c["r_sobre_R"], F12=c["F12"],
                err_r=abs(c["r_sobre_R"] - c["r_sobre_R_h2"]), err_F=abs(c["F12"] - c["F12_h2"]))


TABLAS = {e: pares.tabla_richardson(e) for e in EPSS}
BETA = tr.BETA_PARED          # -zeta(1/2)/sqrt(2 pi) = 0.5826 (ver el diagnostico de la pared mas abajo)


def resolver(delta, R, h, eps, E_guess):
    """Mayor autovalor de T por shift-invert; devuelve E0, observables, chequeos y tiempo."""
    t = time.perf_counter()
    T, r = tr.matriz_T(R, h, eps, W=tr.W_yukawa(delta), tabla=TABLAS[eps])
    tb = time.perf_counter() - t
    sigma = float(np.exp(-eps * (E_guess - 2e-4)))     # algo por encima de lambda0
    lam, v = eigsh(T, k=3, sigma=sigma, which="LM", tol=0)
    o = np.argsort(lam)[::-1]
    lam, v = lam[o], v[:, o]
    v0 = v[:, 0] * np.sign(v[:, 0].sum())
    perron = float(v0.min() / np.abs(v0).max())        # >= -1e-8 si es el vector de Perron
    res = float(np.linalg.norm(T @ v0 - lam[0] * v0) / np.linalg.norm(v0))
    ob = tr._observables(r, v0, R)
    return dict(E0=float(-np.log(lam[0]) / eps), E1=float(-np.log(lam[1]) / eps),
                r_sobre_R=ob["r_sobre_R"], F12=ob["F12"], r_med=ob["r_med"], N=len(r), nnz=int(T.nnz),
                perron_min=perron, residuo=res, t_matriz=tb, t_total=time.perf_counter() - t)


def ext_eps(a01, a005):
    return a005 + (a005 - a01) / 3.0


# ---------------------------------------------------------------- longitud de dispersion (no ligado)
def long_dispersion(delta, Rf=80.0):
    f = lambda r, s: [s[1], -2.0 * np.exp(-delta * r) / r * s[0]]
    s = solve_ivp(f, [1e-10, Rf], [1e-10, 1.0], method="DOP853", rtol=1e-13, atol=1e-18)
    u, up = s.y[0, -1], s.y[1, -1]
    return float(Rf - u / up)


out = dict(script="14_criterio_cajas.py", fecha="2026-10-27", unidades="hbar=m=g=1",
           metodo="transferencia en banda, accion de pares de Coulomb (tablas Richardson h_tab 0.01/0.005), "
                  "eps 0.2/0.1/0.05, h 0.02/0.04, Richardson en h exponente 4, extrapolacion eps^2",
           referencia="fase2/resultados/10_radial.json cajas_9_6 (DF h=1/40,1/80, Richardson p=2)",
           celdas={}, orden_nystrom={}, veredictos={})

# ---------------------------------------------------------------- barrido
for delta in DELTAS:
    out["celdas"][f"{delta:g}"] = {}
    for R in RS:
        ref = rad(delta, R)
        crudo = {}
        Eg = ref["E0"]
        for h in HS:
            for eps in EPSS:
                d = resolver(delta, R, h, eps, Eg)
                Eg = d["E0"]
                crudo[f"h{h:g}_eps{eps:g}"] = d
                print(f"d={delta:<5} R={R:<4} h={h:<5} eps={eps:<5} N={d['N']:<6} E0={d['E0']:+.10e} "
                      f"r/R={d['r_sobre_R']:.6f} F12={d['F12']:.6f} perron={d['perron_min']:+.1e} "
                      f"res={d['residuo']:.1e} t={d['t_total']:.1f}s", flush=True)
        E = {(h, e): crudo[f"h{h:g}_eps{e:g}"]["E0"] for h in HS for e in EPSS}
        EhR = {e: (16 * E[(0.02, e)] - E[(0.04, e)]) / 15 for e in EPSS}
        E_best = ext_eps(EhR[0.1], EhR[0.05])
        E_best_gruesa = ext_eps(EhR[0.2], EhR[0.1])
        E_ext_h002 = ext_eps(E[(0.02, 0.1)], E[(0.02, 0.05)])
        p_trot = float(np.log2(abs(EhR[0.2] - EhR[0.1]) / abs(EhR[0.1] - EhR[0.05])))
        err_tr_sin_pared = abs(E_ext_h002 - E_best) + abs(E_best - E_best_gruesa)
        # V3 (hallazgo H1 de V1 y V2): err_tr no recogia el sesgo de la pared en R sin imagen (la pared efectiva
        # esta en R + BETA sqrt(eps)). Se estima con el radial: dP(eps) = E_rad(R + BETA sqrt(eps)) - E_rad(R), y lo
        # que queda tras la extrapolacion eps^2 (eps = 0.1, 0.05) se suma al error.
        pared_e = {e: radial.resolver_rich(radial.V_yukawa(delta), R + BETA * np.sqrt(e), h=1 / 40, nev=1)["E0"]
                      - ref["E0"] for e in EPSS}
        pared_ext = float(ext_eps(pared_e[0.1], pared_e[0.05]))
        err_tr = err_tr_sin_pared + abs(pared_ext)
        obs = {}
        for k in ("r_sobre_R", "F12"):
            o = {(h, e): crudo[f"h{h:g}_eps{e:g}"][k] for h in HS for e in EPSS}
            b = ext_eps(o[(0.02, 0.1)], o[(0.02, 0.05)])
            err = (abs(b - ext_eps(o[(0.04, 0.1)], o[(0.04, 0.05)]))
                   + abs(b - ext_eps(o[(0.02, 0.2)], o[(0.02, 0.1)])))
            obs[k] = dict(mejor=float(b), err=float(err), eps01_h002=o[(0.02, 0.1)],
                          dif_rad=float(b - ref[k]))
        absE = abs(ref["E0"])
        celda = dict(
            radial=ref, crudo=crudo, E_hRich=EhR, E_mejor=float(E_best), err=float(err_tr),
            err_sin_pared=float(err_tr_sin_pared), sesgo_pared_por_eps={f"{e:g}": v for e, v in pared_e.items()},
            sesgo_pared_extrapolado=pared_ext, dif_rad_corregida_pared=float(E_best - pared_ext - ref["E0"]),
            estricto_dif_menor_err_tr=bool(abs(E_best - ref["E0"]) <= err_tr),
            estricto_sin_pared=bool(abs(E_best - ref["E0"]) <= err_tr_sin_pared),
            orden_trotter=p_trot, E_ext_eps_h002=float(E_ext_h002),
            dif_rad=float(E_best - ref["E0"]), dif_rad_sobre_absE=float(abs(E_best - ref["E0"]) / absE),
            compatible=bool(abs(E_best - ref["E0"]) <= 2 * (err_tr + ref["err"]) + 1e-12),
            # errores parciales comparados con |E0|
            malla_rel={f"{e:g}": abs(E[(0.02, e)] - E[(0.04, e)]) / abs(E[(0.02, e)]) for e in EPSS},
            trotter_rel_eps01=abs(EhR[0.1] - E_best) / absE,
            eps01_h002_menos_rad_rel=abs(E[(0.02, 0.1)] - ref["E0"]) / absE,
            obs=obs)
        out["celdas"][f"{delta:g}"][f"R{R}"] = celda
        print(f"  -> E_mejor={E_best:+.10e} +- {err_tr:.1e}  radial={ref['E0']:+.10e}  dif={E_best-ref['E0']:+.2e} "
              f"(|dif|/|E0|={celda['dif_rad_sobre_absE']:.1e})  orden Trotter={p_trot:.3f}  "
              f"malla(eps=.1)/|E|={celda['malla_rel']['0.1']:.2e}  Trotter(eps=.1)/|E|={celda['trotter_rel_eps01']:.2e}  "
              f"[eps=0.1,h=0.02 frente al radial: {celda['eps01_h002_menos_rad_rel']:.2e} de |E0|]", flush=True)
        print(f"     r/R: tr {obs['r_sobre_R']['mejor']:.6f}+-{obs['r_sobre_R']['err']:.1e} rad {ref['r_sobre_R']:.6f}; "
              f"F12: tr {obs['F12']['mejor']:.6f}+-{obs['F12']['err']:.1e} rad {ref['F12']:.6f}", flush=True)
        print(f"     V3 pared: sesgo extrapolado {pared_ext:+.2e}; err sin pared {err_tr_sin_pared:.2e} -> con pared "
              f"{err_tr:.2e}; |dif|<=err_tr: {celda['estricto_dif_menor_err_tr']} (sin pared: {celda['estricto_sin_pared']})",
              flush=True)
        json.dump(out, open(os.path.join(RES, "14_cajas.json"), "w"), indent=1, default=float)

n_est = sum(out["celdas"][f"{d:g}"][f"R{R}"]["estricto_dif_menor_err_tr"] for d in DELTAS for R in RS)
n_est0 = sum(out["celdas"][f"{d:g}"][f"R{R}"]["estricto_sin_pared"] for d in DELTAS for R in RS)
out["V3_criterio_estricto"] = dict(n_celdas=len(DELTAS) * len(RS), pasan_con_pared=int(n_est), pasan_sin_pared=int(n_est0),
                                   fallan_con_pared=[f"{d:g}_R{R}" for d in DELTAS for R in RS
                                                     if not out["celdas"][f"{d:g}"][f"R{R}"]["estricto_dif_menor_err_tr"]],
                                   fallan_sin_pared=[f"{d:g}_R{R}" for d in DELTAS for R in RS
                                                     if not out["celdas"][f"{d:g}"][f"R{R}"]["estricto_sin_pared"]])
print(f"\nV3: criterio estricto |dif| <= err_tr: pasan {n_est}/15 con el sesgo de pared en err_tr; "
      f"{n_est0}/15 sin el. Fallan (con pared): {out['V3_criterio_estricto']['fallan_con_pared']}")

# ---------------------------------------------------------------- orden de la malla Nystrom cerca del umbral
print("\n=== Orden de la malla Nystrom, delta=1.18, eps=0.1, h = 0.04, 0.02, 0.01 ===")
for R in (50, 100):
    Es = []
    for h in (0.04, 0.02, 0.01):
        d = resolver(1.18, R, h, 0.1, rad(1.18, R)["E0"])
        Es.append(d["E0"])
    p = float(np.log2(abs(Es[0] - Es[1]) / abs(Es[1] - Es[2])))
    E4 = (16 * Es[2] - Es[1]) / 15
    E4g = (16 * Es[1] - Es[0]) / 15
    out["orden_nystrom"][f"R{R}"] = dict(E_h004=Es[0], E_h002=Es[1], E_h001=Es[2], orden=p,
                                          rich_002_001=E4, rich_004_002=E4g)
    print(f"R={R}: E = {Es[0]:+.10e}, {Es[1]:+.10e}, {Es[2]:+.10e}; orden aparente {p:.3f}; "
          f"Richardson h^4 (0.04,0.02) = {E4g:+.10e}, (0.02,0.01) = {E4:+.10e}", flush=True)

# ---------------------------------------------------------------- diagnostico: pared en R sin imagen
# K_D solo tiene imagen en r = 0; en r = R la condicion de Dirichlet se impone solo en los nodos de tiempo
# (el camino puede salir y volver entre dos eslabones). Para un movimiento browniano vigilado en tiempos
# discretos, la pared efectiva se corre hacia afuera beta sqrt(eps), beta = -zeta(1/2)/sqrt(2 pi) = 0.5826
# (Broadie-Glasserman-Kou). Prueba: comparar E_hR(eps) con el radial en la caja R + beta sqrt(eps).
BETA = 0.5825971579390106
print("\n=== Diagnostico de la pared en R: transferencia frente al radial en R + 0.5826 sqrt(eps) ===")
out["pared"] = dict(beta=BETA, nota="E_hRich(eps) - E_radial(R + beta sqrt(eps)); radial h=1/40,1/80 Richardson")
for delta in DELTAS:
    for R in (50, 100, 200):
        C = out["celdas"][f"{delta:g}"][f"R{R}"]
        dif = []
        for e in EPSS:
            Er = radial.resolver_rich(radial.V_yukawa(delta), R + BETA * np.sqrt(e), h=1 / 40)["E0"]
            dif.append(C["E_hRich"][e] - Er)
        p = float(np.log2(abs(dif[0] - dif[1]) / abs(dif[1] - dif[2])))
        ext = float(ext_eps(dif[1], dif[2]))
        absE = abs(C["radial"]["E0"])
        out["pared"][f"{delta:g}_R{R}"] = dict(dif=dif, orden=p, extrapolado=ext,
                                               sin_correccion=C["dif_rad"], extrapolado_sobre_absE=abs(ext) / absE)
        print(f"delta={delta} R={R}: dif(eps) = {[f'{x:+.3e}' for x in dif]}  orden {p:.3f}  extrapolado {ext:+.2e} "
              f"({abs(ext)/absE:.1e} de |E0|); sin corregir la pared: {C['dif_rad']:+.2e} (orden {C['orden_trotter']:.3f})",
              flush=True)

# ---------------------------------------------------------------- criterio 9.6
a_s ={f"{d:g}": long_dispersion(d) for d in DELTAS}
print("\nlongitud de dispersion a energia cero (solo tiene sentido como ley de caja si no hay ligado):", a_s)
out["a_s"] = a_s


def evaluar(delta, terna, fuente):
    """fuente = 'radial' o 'transferencia'. Devuelve dict de pruebas."""
    C = out["celdas"][f"{delta:g}"]
    if fuente == "radial":
        E = [C[f"R{R}"]["radial"]["E0"] for R in terna]
        eE = [C[f"R{R}"]["radial"]["err"] for R in terna]
        rr = [C[f"R{R}"]["radial"]["r_sobre_R"] for R in terna]
        F = [C[f"R{R}"]["radial"]["F12"] for R in terna]
        malla = [C[f"R{R}"]["radial"]["dE_rel"] for R in terna]
        er = [C[f"R{R}"]["radial"]["err_r"] for R in terna]
        ef = [C[f"R{R}"]["radial"]["err_F"] for R in terna]
    else:
        E = [C[f"R{R}"]["E_mejor"] for R in terna]
        eE = [C[f"R{R}"]["err"] for R in terna]
        rr = [C[f"R{R}"]["obs"]["r_sobre_R"]["mejor"] for R in terna]
        er = [C[f"R{R}"]["obs"]["r_sobre_R"]["err"] for R in terna]
        F = [C[f"R{R}"]["obs"]["F12"]["mejor"] for R in terna]
        ef = [C[f"R{R}"]["obs"]["F12"]["err"] for R in terna]
        malla = [max(C[f"R{R}"]["malla_rel"].values()) for R in terna]
    dec = lambda x: all(x[i + 1] < x[i] for i in range(2))
    inc = lambda x: all(x[i + 1] > x[i] for i in range(2))
    # signo "seguro": |E| mayor que su error
    neg_seg = [E[i] < 0 and abs(E[i]) > eE[i] for i in range(3)]
    pos_seg = [E[i] > 0 and abs(E[i]) > eE[i] for i in range(3)]
    a = bool(neg_seg[1] and neg_seg[2] and abs(E[2] - E[1]) < 0.1 * abs(E[2]))
    ap = bool(all(m < 0.1 for m in malla))
    b = bool(dec(rr) and inc(F) and F[2] > 0.95)
    # no ligado
    nl_signo = bool(all(pos_seg))
    nl_tend = bool(inc(rr) and dec(F))
    asd = a_s[f"{delta:g}"]
    ley = [np.pi**2 / (2 * (R - asd)**2) for R in terna]
    dev = [abs(E[i] - ley[i]) / ley[i] for i in range(3)]
    nl_ley = bool(dev[2] < 0.1 and dev[2] < dev[1] < dev[0])
    return dict(terna=list(terna), E=E, err_E=eE, r_sobre_R=rr, err_r=er, F12=F, err_F=ef, malla_rel=malla,
                a=a, a_prima=ap, b=b, ligado=bool(a and ap and b),
                nl_signo=nl_signo, nl_tendencias=nl_tend, ley_caja=ley, dev_ley=dev, nl_ley=nl_ley,
                no_ligado=bool(nl_signo and nl_tend and nl_ley and ap))


def cond_c(delta, terna):
    """(c): la transferencia da el mismo signo y la misma tendencia en las mismas cajas, dentro de errores."""
    C = out["celdas"][f"{delta:g}"]
    rr, tt = evaluar(delta, terna, "radial"), evaluar(delta, terna, "transferencia")
    mismo_signo = all(np.sign(rr["E"][i]) == np.sign(tt["E"][i]) and abs(tt["E"][i]) > tt["err_E"][i]
                      for i in range(3))
    tend = lambda x: [np.sign(x[i + 1] - x[i]) for i in range(2)]
    misma_tend = tend(rr["r_sobre_R"]) == tend(tt["r_sobre_R"]) and tend(rr["F12"]) == tend(tt["F12"])
    compat = all(C[f"R{R}"]["compatible"] for R in terna)
    return dict(mismo_signo=bool(mismo_signo), misma_tendencia=bool(misma_tend), E_compatibles=bool(compat),
                c=bool(mismo_signo and misma_tend and compat))


print("\n=== Criterio 9.6 por delta y terna ===")
for delta in DELTAS:
    V = {}
    for terna in TERNAS:
        rr, tt, cc = evaluar(delta, terna, "radial"), evaluar(delta, terna, "transferencia"), cond_c(delta, terna)
        V[str(terna)] = dict(radial=rr, transferencia=tt, c=cc)
        print(f"delta={delta} terna={terna}: radial (a,a',b)=({rr['a']},{rr['a_prima']},{rr['b']}) "
              f"no ligado (signo,tend,ley)=({rr['nl_signo']},{rr['nl_tendencias']},{rr['nl_ley']}) | "
              f"transf (a,a',b)=({tt['a']},{tt['a_prima']},{tt['b']}) no ligado=({tt['nl_signo']},"
              f"{tt['nl_tendencias']},{tt['nl_ley']}) | (c)={cc}  dev ley (rad)={[f'{x:.3f}' for x in rr['dev_ley']]}")
    # veredicto: primera terna (de menor a mayor) que decide con las cuatro condiciones
    ver, usada = "indeterminado", None
    for terna in TERNAS:
        X = V[str(terna)]
        if X["radial"]["ligado"] and X["transferencia"]["ligado"] and X["c"]["c"]:
            ver, usada = "ligado", terna; break
        if X["radial"]["no_ligado"] and X["transferencia"]["no_ligado"] and X["c"]["c"]:
            ver, usada = "no ligado", terna; break
    out["veredictos"][f"{delta:g}"] = dict(veredicto=ver, terna=usada, por_terna=V)
    print(f"  VEREDICTO delta={delta}: {ver} (terna {usada})")

out["tiempo_total_s"] = time.perf_counter() - T0
out["carga_final"] = os.getloadavg()
json.dump(out, open(os.path.join(RES, "14_cajas.json"), "w"), indent=1, default=float)

# ---------------------------------------------------------------- figura
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402

fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
col = {1.15: "tab:blue", 1.18: "tab:green", 1.20: "tab:red"}
for delta in DELTAS:
    C = out["celdas"][f"{delta:g}"]
    E_r = [C[f"R{R}"]["radial"]["E0"] for R in RS]
    E_t = [C[f"R{R}"]["E_mejor"] for R in RS]
    ax[0].plot(RS, E_r, "-", color=col[delta], label=f"δ={delta} radial")
    ax[0].plot(RS, E_t, "o", mfc="none", color=col[delta], label=f"δ={delta} transferencia")
    for j, k in ((1, "r_sobre_R"), (2, "F12")):
        ax[j].plot(RS, [C[f"R{R}"]["radial"][k] for R in RS], "-", color=col[delta], label=f"δ={delta} radial")
        ax[j].errorbar(RS, [C[f"R{R}"]["obs"][k]["mejor"] for R in RS],
                       yerr=[C[f"R{R}"]["obs"][k]["err"] for R in RS], fmt="o", mfc="none",
                       color=col[delta], label=f"δ={delta} transferencia")
ax[0].set_yscale("symlog", linthresh=1e-6); ax[0].axhline(0, color="k", lw=0.6)
ax[0].set_ylabel("$E_0$ (unidades $mg^2/\\hbar^2$)"); ax[0].set_title("Energía del estado más bajo")
ax[1].axhline(0.5, color="k", ls=":", lw=0.8); ax[1].set_ylabel("$\\langle r\\rangle/R$")
ax[1].set_title("Radio medio relativo a la caja")
ax[2].axhline(0.5, color="k", ls=":", lw=0.8); ax[2].axhline(1.0, color="k", ls=":", lw=0.8)
ax[2].set_ylabel("$F_{1/2}$"); ax[2].set_title("Fracción de densidad en la mitad interior")
for a in ax:
    a.set_xscale("log"); a.set_xticks(RS); a.set_xticklabels([str(R) for R in RS])
    a.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    a.set_xlabel("radio de la caja $R$")
ax[2].legend(fontsize=7, loc="lower left")
fig.suptitle("Criterio de cajas 9.6: solucionador radial (líneas) y transferencia extrapolada (círculos)")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "14_cajas.png"), dpi=150)
print(f"\nTiempo total: {time.perf_counter()-T0:.1f} s; carga final {os.getloadavg()}")
