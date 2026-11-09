"""12_pigs_produccion.py -- Proyecto 05 (Yukawa), Fase 2, tarea 4 (y parte de la 8): produccion PIGS.

Unidades hbar = m = g = 1, V = -e^{-delta r}/r. Accion de pares (pares.py, Richardson h_tab = 0.01/0.005)
interpolada en r continuo (pigs.py). eps = 0.1 en todo el script.

Partes
  (0) Referencias: solucionador radial (radial.py, R = 40, h = 1/40 y 1/80 con Richardson) y la
      transferencia en banda (transferencia.py, R = 40, h = 0.02 y 0.04, Richardson en h con
      exponente 4) con el MISMO eps y la MISMA tau: E_mixto(tau) y el estimador puro de <r>, <r^2>
      en tau/2, calculados sin muestreo.
  (1) Control Coulomb delta = 0, tau = 10: 1 cadena de 5e4 barridos + 500, semilla 20262008.
  (2) delta = 0.2, tau = 20: 8 cadenas de 5e4 + 500, semillas 20262000..20262007, interpolacion
      bicubica (produccion); en cada configuracion se guarda dS = sum_k [U_bil - U_bic] para repesar.
  (3) E_mixto(tau) y <r>_puro(tau) en delta = 0.2 para tau = 2, 5, 10 (8 cadenas de 3e4 + 500 cada
      una; semillas 20262020+k, 20262030+k, 20262040+k) y tau = 20 (la produccion), frente a la curva
      determinista de la transferencia.
  (4) Interpolacion bilineal frente a bicubica: (a) repesado de la produccion bicubica (correlacionado,
      error pequeno); (b) 8 cadenas directas con interpolacion bilineal de 2.5e4 + 500 barridos,
      semillas 20262010..20262017.
Paralelo: multiprocessing con 4 procesos (fork). Salidas: resultados/12_pigs.json,
resultados/12_pigs_series.npz, figuras/12_pigs_tau.png, figuras/12_pigs_delta02.png.
"""
import os
import sys
import json
import time
import datetime
import multiprocessing as mp
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import radial          # noqa: E402
import pares           # noqa: E402
import transferencia   # noqa: E402
import pigs            # noqa: E402

T0 = time.perf_counter()
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
EPS = 0.1
NB = 20                      # bloques por cadena
NPROC = 4
print(f"Carga al empezar (loadavg 1/5/15): {os.getloadavg()}; nucleos: {os.cpu_count()}; procesos: {NPROC}")

# ------------------------------------------------------------------ tabla e interpoladores (antes del fork)
TAB = pares.tabla_richardson(EPS)
U_BIC = pigs.interpolador(TAB, "bicubica")
U_BIL = pigs.interpolador(TAB, "bilineal")
print(f"Tabla U_C: {TAB.origen}, eps={EPS}, nt={TAB.nt}, banda={TAB.banda}")

# ------------------------------------------------------------------ (0) referencias
print("\n=== (0) Referencias deterministas ===")
ref_rad = {}
for dl in (0.0, 0.2):
    o = radial.resolver_rich(radial.V_yukawa(dl), 40.0, h=1 / 40, nev=1)
    ref_rad[dl] = dict(E0=float(o["E0"]), r=float(o["r_med"]), r2=float(o["r2_med"]))
    print(f"radial delta={dl}: E0={o['E0']:.10f}  <r>={o['r_med']:.10f}  <r^2>={o['r2_med']:.10f}")


def determinista(dl, h, taus, R=40.0):
    """Transferencia con la misma accion (en nodos): E_mixto(tau) y estimador puro en tau/2."""
    T, r = transferencia.matriz_T(R, h, EPS, W=transferencia.W_yukawa(dl), tabla=TAB)
    uT = r * np.exp(-r)
    HuT = (pigs.W_yukawa(dl)(r) - 0.5) * uT
    out = {}
    x = uT.copy(); M = 0
    Ms = sorted({int(round(t / EPS)) for t in taus} | {int(round(t / EPS)) // 2 for t in taus})
    snap = {}
    for Mt in Ms:
        while M < Mt:
            x = T @ x; x /= np.abs(x).max(); M += 1
        snap[Mt] = x.copy()
    for t in taus:
        Mf = int(round(t / EPS)); Mh = Mf // 2
        xf, xh = snap[Mf], snap[Mh]
        out[t] = dict(E_mixto=float((HuT @ xf) / (uT @ xf)),
                      r_puro=float((r * xh**2).sum() / (xh**2).sum()),
                      r2_puro=float((r**2 * xh**2).sum() / (xh**2).sum()))
    lam, v = transferencia.autoestado(T)
    v0 = v[:, 0]
    lim = dict(E0_T=float(-np.log(lam[0]) / EPS), E_mixto=float((v0 @ HuT) / (v0 @ uT)),
               r_puro=float((r * v0**2).sum() / (v0**2).sum()), r2_puro=float((r**2 * v0**2).sum() / (v0**2).sum()))
    return out, lim


TAUS_DET = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30]
det = {}
for dl in (0.0, 0.2):
    det[dl] = {}
    for h in (0.02, 0.04):
        det[dl][h] = determinista(dl, h, TAUS_DET)
    # Richardson en h con exponente 4 (seccion 11.4): X = (16 X_0.02 - X_0.04)/15
    a, la = det[dl][0.02]; b, lb = det[dl][0.04]
    rich = {t: {k: (16 * a[t][k] - b[t][k]) / 15 for k in a[t]} for t in TAUS_DET}
    lrich = {k: (16 * la[k] - lb[k]) / 15 for k in la}
    det[dl]["rich"] = (rich, lrich)
    print(f"transferencia delta={dl} (h=0.02 | Richardson h^4): E0(T)={la['E0_T']:.10f} | {lrich['E0_T']:.10f}")
    for t in (2, 5, 10, 20):
        print(f"   tau={t:>2}: E_mixto={a[t]['E_mixto']:.9f} | {rich[t]['E_mixto']:.9f}   "
              f"<r>_puro={a[t]['r_puro']:.7f} | {rich[t]['r_puro']:.7f}   <r^2>_puro={a[t]['r2_puro']:.7f}")
print(f"[referencias: {time.perf_counter()-T0:.1f} s]")

# ------------------------------------------------------------------ trabajos Monte Carlo
SEM = 20262000
FAC = float(os.environ.get("PIGS_FACTOR", "1"))   # solo para pruebas rapidas; produccion: 1
trabajos = []
trabajos += [("prod02", 0.2, 20.0, int(50000 * FAC), SEM + k, "bic") for k in range(8)]
trabajos += [("coul", 0.0, 10.0, int(50000 * FAC), SEM + 8, "bic")]
trabajos += [("bil02", 0.2, 20.0, int(25000 * FAC), SEM + 10 + k, "bil") for k in range(8)]
for j, tau in enumerate((10.0, 5.0, 2.0)):
    trabajos += [(f"tau{tau:g}", 0.2, tau, int(30000 * FAC), SEM + 40 - 10 * j + k, "bic") for k in range(8)]


def correr(tr):
    nombre, dl, tau, nsw, seed, met = tr
    Uf, Ua = (U_BIC, U_BIL) if met == "bic" else (U_BIL, U_BIC)
    o = pigs.cadena(dl, tau, EPS, nsw, seed, Uf, L=10, ntherm=500, nscale=4, Ualt=Ua)
    o.pop("r_final", None)
    return tr, o


t = time.perf_counter()
with mp.get_context("fork").Pool(NPROC) as pool:
    salidas = pool.map(correr, trabajos, chunksize=1)
t_mc = time.perf_counter() - t
print(f"\n[{len(trabajos)} cadenas en {NPROC} procesos: {t_mc:.1f} s de reloj, "
      f"{sum(o['tiempo'] for _, o in salidas):.1f} s de CPU]")

grupos = {}
for tr, o in salidas:
    grupos.setdefault(tr[0], []).append(o)


def resumen(lista):
    out = {}
    for k in ("EL", "rmid", "r2mid"):
        c = pigs.combinar([o[k] for o in lista], NB)
        taus_s = [pigs.tau_int_sokal(o[k])[0] for o in lista]
        taus_b = [pigs.tau_bloques(o[k], pigs.bloques(o[k], NB)[1]) for o in lista]
        c["tau_int_sokal"] = float(np.mean(taus_s)); c["tau_int_bloques"] = float(np.mean(taus_b))
        out[k] = c
    out["M"] = lista[0]["M"]; out["tau"] = lista[0]["tau"]; out["n_cadenas"] = len(lista)
    out["barridos"] = lista[0]["nsweep"]; out["semillas"] = [o["seed"] for o in lista]
    out["acept"] = dict(puentes=float(np.mean([o["acept_puentes"] for o in lista])),
                        extremos=float(np.mean([o["acept_extremos"] for o in lista])),
                        escala=float(np.mean([o["acept_escala"] for o in lista])))
    out["ms_por_barrido"] = float(np.mean([1e3 * o["tiempo"] / (o["nsweep"] + o["ntherm"]) for o in lista]))
    return out


def jack_repesado(o, clave, nb=NB):
    """Diferencia (repesado a la otra interpolacion) - (directo) en una cadena, con jackknife de bloques."""
    x = o[clave]; d = o["dS_alt"]
    n = len(x) // nb * nb; x = x[:n]; d = d[:n]
    w = np.exp(-(d - d.mean()))
    xb = x.reshape(nb, -1); wb = w.reshape(nb, -1)
    Sx, Sw, Sxw = xb.sum(1), wb.sum(1), (xb * wb).sum(1)

    def dif(mask):
        return (Sxw[mask].sum() / Sw[mask].sum()) - (Sx[mask].sum() / (n / nb * mask.sum()))
    full = dif(np.ones(nb, bool))
    jk = np.array([dif(np.arange(nb) != i) for i in range(nb)])
    err = np.sqrt((nb - 1) / nb * ((jk - jk.mean())**2).sum())
    return float(full), float(err)


def comb_dif(lista, clave):
    v = [jack_repesado(o, clave) for o in lista]
    m = np.array([a for a, _ in v]); e = np.array([b for _, b in v]); n = len(v)
    eb = float(np.sqrt((e**2).sum()) / n); es = float(m.std(ddof=1) / np.sqrt(n))
    return dict(media=float(m.mean()), err_jackknife=eb, err_cadenas=es, err=max(eb, es))


R = {k: resumen(v) for k, v in grupos.items()}


def sig(x, ref, e):
    return float((x - ref) / e) if e > 0 else (0.0 if x == ref else float("inf"))


def imprime(nombre, s):
    print(f"{nombre}: tau={s['tau']} M={s['M']} cadenas={s['n_cadenas']} x {s['barridos']}+500 barridos, "
          f"{s['ms_por_barrido']:.2f} ms/barrido; aceptacion puentes/extremos/escala = "
          f"{s['acept']['puentes']:.3f}/{s['acept']['extremos']:.3f}/{s['acept']['escala']:.3f}")
    for k, nm in (("EL", "E"), ("rmid", "<r>"), ("r2mid", "<r^2>")):
        c = s[k]
        print(f"    {nm:6s} = {c['media']:.6f} +- {c['err']:.6f}  (bloques {c['err_bloques']:.2e}, entre cadenas "
              f"{c['err_cadenas']:.2e}, cociente {c['cociente']:.2f}; tau_int Sokal {c['tau_int_sokal']:.1f}, "
              f"por bloques {c['tau_int_bloques']:.1f} barridos)")


crit = []


def criterio(control, texto, valor, pasa):
    crit.append(dict(control=control, criterio=texto, valor=valor, pasa=bool(pasa)))
    print(f"  [{'PASA' if pasa else 'FALLA'}] {control}: {valor}")


# ------------------------------------------------------------------ (1) Coulomb
print("\n=== (1) Control Coulomb delta=0, tau=10 ===")
sC = R["coul"]; imprime("delta=0", sC)
oC = grupos["coul"][0]
varEL = float(np.var(oC["EL"])); maxdev = float(np.abs(oC["EL"] + 0.5).max())
detC = det[0.0]["rich"][0][10]
print(f"    E_L: varianza {varEL:.3e}, max|E_L+0.5| = {maxdev:.3e}; determinista tau=10: "
      f"<r>_puro={detC['r_puro']:.8f}, <r^2>_puro={detC['r2_puro']:.8f}")
dr = sig(sC["rmid"]["media"], 1.5, sC["rmid"]["err"]); dr2 = sig(sC["r2mid"]["media"], 3.0, sC["r2mid"]["err"])
criterio("Coulomb PIGS E_L", "E_L = -0.5 con varianza nula", f"var={varEL:.1e}, max|E_L+0.5|={maxdev:.1e}",
         varEL < 1e-24 and maxdev < 1e-12)
criterio("Coulomb PIGS <r> puro", "a menos de 2 sigma de 1.5",
         f"{sC['rmid']['media']:.5f} +- {sC['rmid']['err']:.5f} ({dr:+.2f} sigma)", abs(dr) < 2)
criterio("Coulomb PIGS <r^2> puro", "a menos de 2 sigma de 3",
         f"{sC['r2mid']['media']:.5f} +- {sC['r2mid']['err']:.5f} ({dr2:+.2f} sigma)", abs(dr2) < 2)

# ------------------------------------------------------------------ (2) delta = 0.2
print("\n=== (2) delta=0.2, tau=20, 8 cadenas (produccion, bicubica) ===")
sP = R["prod02"]; imprime("delta=0.2", sP)
rr = ref_rad[0.2]; dd = det[0.2]["rich"][0][20]; dd02 = det[0.2][0.02][0][20]
dE = sig(sP["EL"]["media"], rr["E0"], sP["EL"]["err"])
drr = sig(sP["rmid"]["media"], rr["r"], sP["rmid"]["err"])
dr22 = sig(sP["r2mid"]["media"], rr["r2"], sP["r2mid"]["err"])
print(f"    radial: E0={rr['E0']:.8f}, <r>={rr['r']:.6f}, <r^2>={rr['r2']:.6f}")
print(f"    transferencia (mismo eps, tau=20, Richardson h^4): E_mixto={dd['E_mixto']:.8f}, <r>_puro={dd['r_puro']:.6f}, "
      f"<r^2>_puro={dd['r2_puro']:.6f}")
criterio("delta=0.2 PIGS E (mixto)", "a menos de 2 sigma del radial (sigma = mayor entre bloques y cadenas)",
         f"{sP['EL']['media']:.6f} +- {sP['EL']['err']:.6f} frente a {rr['E0']:.8f} ({dE:+.2f} sigma)", abs(dE) < 2)
criterio("delta=0.2 PIGS <r> (puro)", "a menos de 2 sigma del radial",
         f"{sP['rmid']['media']:.5f} +- {sP['rmid']['err']:.5f} frente a {rr['r']:.5f} ({drr:+.2f} sigma)", abs(drr) < 2)
criterio("delta=0.2 PIGS <r^2> (puro)", "a menos de 2 sigma del radial",
         f"{sP['r2mid']['media']:.5f} +- {sP['r2mid']['err']:.5f} frente a {rr['r2']:.5f} ({dr22:+.2f} sigma)", abs(dr22) < 2)
cocs = [sP[k]["cociente"] for k in ("EL", "rmid", "r2mid")]
print(f"    (entre cadenas / bloques)^2: E {cocs[0]:.2f}, <r> {cocs[1]:.2f}, <r^2> {cocs[2]:.2f} "
      f"(regla 9.7: si >2 manda el error entre cadenas; aqui se reporta siempre el mayor)")

# ------------------------------------------------------------------ (3) tau
print("\n=== (3) E_mixto(tau) y <r>_puro(tau), delta=0.2: PIGS frente a transferencia ===")
tabla_tau = []
for tau, g in ((2.0, "tau2"), (5.0, "tau5"), (10.0, "tau10"), (20.0, "prod02")):
    s = R[g]; d = det[0.2]["rich"][0][int(tau)]
    sE = sig(s["EL"]["media"], d["E_mixto"], s["EL"]["err"]); sr = sig(s["rmid"]["media"], d["r_puro"], s["rmid"]["err"])
    sr2 = sig(s["r2mid"]["media"], d["r2_puro"], s["r2mid"]["err"])
    tabla_tau.append(dict(tau=tau, M=s["M"], cadenas=s["n_cadenas"], barridos=s["barridos"],
                          E_pigs=s["EL"]["media"], eE=s["EL"]["err"], E_det=d["E_mixto"], sigma_E=sE,
                          r_pigs=s["rmid"]["media"], er=s["rmid"]["err"], r_det=d["r_puro"], sigma_r=sr,
                          r2_pigs=s["r2mid"]["media"], er2=s["r2mid"]["err"], r2_det=d["r2_puro"], sigma_r2=sr2,
                          tau_int_E=s["EL"]["tau_int_sokal"], tau_int_r=s["rmid"]["tau_int_sokal"],
                          ms_por_barrido=s["ms_por_barrido"]))
    print(f"  tau={tau:>4}: E_PIGS={s['EL']['media']:.6f}+-{s['EL']['err']:.6f}  E_det={d['E_mixto']:.6f} ({sE:+.2f} s) | "
          f"<r>_PIGS={s['rmid']['media']:.4f}+-{s['rmid']['err']:.4f}  det={d['r_puro']:.4f} ({sr:+.2f} s) | "
          f"<r^2> ({sr2:+.2f} s) | tau_int(E)={s['EL']['tau_int_sokal']:.1f}")
nmal = sum(abs(x["sigma_E"]) >= 2 or abs(x["sigma_r"]) >= 2 or abs(x["sigma_r2"]) >= 2 for x in tabla_tau)
criterio("E_mixto(tau) y <r>,<r^2> puros (tau = 2, 5, 10, 20)", "PIGS a menos de 2 sigma de la transferencia en cada tau",
         "; ".join(f"tau={x['tau']:g}: {x['sigma_E']:+.1f}/{x['sigma_r']:+.1f}/{x['sigma_r2']:+.1f} sigma" for x in tabla_tau),
         nmal == 0)
pend = (tabla_tau[0]["E_pigs"] - tabla_tau[-1]["E_pigs"]) / np.hypot(tabla_tau[0]["eE"], tabla_tau[-1]["eE"])
pend_r = (tabla_tau[0]["r_pigs"] - tabla_tau[-1]["r_pigs"]) / np.hypot(tabla_tau[0]["er"], tabla_tau[-1]["er"])
proy_info = dict(dE_pigs=tabla_tau[0]["E_pigs"] - tabla_tau[-1]["E_pigs"], sigma_dE=float(pend),
                 dE_det=tabla_tau[0]["E_det"] - tabla_tau[-1]["E_det"],
                 dr_pigs=tabla_tau[0]["r_pigs"] - tabla_tau[-1]["r_pigs"], sigma_dr=float(pend_r),
                 dr_det=tabla_tau[0]["r_det"] - tabla_tau[-1]["r_det"])
print(f"  (informativo) E_mixto(2)-E_mixto(20): PIGS {proy_info['dE_pigs']:+.2e} ({pend:+.1f} sigma), determinista "
      f"{proy_info['dE_det']:+.2e};  <r>(2)-<r>(20): PIGS {proy_info['dr_pigs']:+.4f} ({pend_r:+.1f} sigma), "
      f"determinista {proy_info['dr_det']:+.4f}")

# ------------------------------------------------------------------ (4) interpolacion
print("\n=== (4) PIGS frente a transferencia en el mismo eps; bilineal frente a bicubica ===")
lim_r = det[0.2]["rich"][1]
for k, nm in (("EL", "E_mixto"), ("rmid", "r_puro"), ("r2mid", "r2_puro")):
    c = sP[k]
    print(f"  {k}: PIGS bicubica - transferencia(tau=20) = {c['media']-dd[nm]:+.3e} +- {c['err']:.1e} "
          f"({sig(c['media'], dd[nm], c['err']):+.2f} sigma); transferencia h=0.02 sin Richardson: {dd02[nm]:.9f}")
rw = {k: comb_dif(grupos["prod02"], k) for k in ("EL", "rmid", "r2mid")}
rw_inv = {k: comb_dif(grupos["bil02"], k) for k in ("EL", "rmid", "r2mid")}
sB = R["bil02"]; imprime("delta=0.2 bilineal directa", sB)
dSm = float(np.mean([o["dS_alt"].mean() for o in grupos["prod02"]]))
dSs = float(np.mean([o["dS_alt"].std() for o in grupos["prod02"]]))
print(f"  dS = sum_k [U_bil - U_bic] en la produccion: media {dSm:+.3e}, desviacion {dSs:.3e}")
for k, nm in (("EL", "E"), ("rmid", "<r>"), ("r2mid", "<r^2>")):
    a = rw[k]; b = rw_inv[k]
    dir_ = sB[k]["media"] - sP[k]["media"]; edir = np.hypot(sB[k]["err"], sP[k]["err"])
    print(f"  {nm}: bilineal - bicubica, repesado de la produccion = {a['media']:+.3e} +- {a['err']:.1e}; "
          f"repesado inverso (bicubica - bilineal) = {b['media']:+.3e} +- {b['err']:.1e}; "
          f"directo = {dir_:+.3e} +- {edir:.1e}")
sesgoE = rw["EL"]
criterio("Sesgo de la interpolacion bilineal en E (repesado)", "medido y menor que el error estadistico de la produccion",
         f"{sesgoE['media']:+.2e} +- {sesgoE['err']:.1e} (error de produccion {sP['EL']['err']:.1e})",
         abs(sesgoE["media"]) + 2 * sesgoE["err"] < sP["EL"]["err"])
cons = abs(rw["EL"]["media"] - (sB["EL"]["media"] - sP["EL"]["media"])) / np.hypot(rw["EL"]["err"], np.hypot(sB["EL"]["err"], sP["EL"]["err"]))
criterio("Repesado frente a corrida bilineal directa", "diferencias de E compatibles a 2 sigma", f"{cons:.2f} sigma", cons < 2)
dTE = sig(sP["EL"]["media"], dd["E_mixto"], sP["EL"]["err"])
criterio("PIGS (bicubica) frente a transferencia, mismo eps y tau", "E, <r>, <r^2> a menos de 2 sigma",
         "; ".join(f"{nm} {sig(sP[k]['media'], dd[q], sP[k]['err']):+.2f} sigma" for k, q, nm in
                   (("EL", "E_mixto", "E"), ("rmid", "r_puro", "<r>"), ("r2mid", "r2_puro", "<r^2>"))),
         all(abs(sig(sP[k]["media"], dd[q], sP[k]["err"])) < 2 for k, q in (("EL", "E_mixto"), ("rmid", "r_puro"), ("r2mid", "r2_puro"))))
ttot = time.perf_counter() - T0
criterio("Tiempo de reloj", "< 25 min", f"{ttot/60:.1f} min (Monte Carlo {t_mc/60:.1f} min)", ttot < 25 * 60)

# ------------------------------------------------------------------ figuras
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

dr_, lr_ = det[0.2]["rich"]
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
tt = np.array(TAUS_DET, float)
ax[0].plot(tt, [dr_[t]["E_mixto"] for t in TAUS_DET], "-", color="0.3", label="transferencia (sin muestreo)")
ax[0].errorbar([x["tau"] for x in tabla_tau], [x["E_pigs"] for x in tabla_tau], yerr=[x["eE"] for x in tabla_tau],
               fmt="o", color="C0", capsize=3, label="PIGS (8 cadenas)")
ax[0].axhline(rr["E0"], ls=":", color="C3", label="radial $E_0$")
ax[0].set_xlabel(r"duración de proyección $\tau$"); ax[0].set_ylabel(r"$E_{\rm mixto}(\tau)$")
ax[0].set_title(r"$\delta=0.2$, $\epsilon=0.1$: estimador mixto")
ax[0].legend(fontsize=8)
ax[1].plot(tt, [dr_[t]["r_puro"] for t in TAUS_DET], "-", color="0.3", label="transferencia (sin muestreo)")
ax[1].errorbar([x["tau"] for x in tabla_tau], [x["r_pigs"] for x in tabla_tau], yerr=[x["er"] for x in tabla_tau],
               fmt="o", color="C0", capsize=3, label="PIGS (8 cadenas)")
ax[1].axhline(rr["r"], ls=":", color="C3", label=r"radial $\langle r\rangle$")
ax[1].set_xlabel(r"duración de proyección $\tau$"); ax[1].set_ylabel(r"$\langle r\rangle$ puro en $\tau/2$")
ax[1].set_title(r"$\delta=0.2$: estimador puro en el eslabón central"); ax[1].legend(fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "12_pigs_tau.png"), dpi=150); plt.close(fig)

fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
for i, (k, q, nm, rk) in enumerate((("EL", "E_mixto", r"$E$", "E0"), ("rmid", "r_puro", r"$\langle r\rangle$", "r"),
                                    ("r2mid", "r2_puro", r"$\langle r^2\rangle$", "r2"))):
    vals = [rr[rk], lr_["E0_T"] if k == "EL" else lr_[q], dd[q], sP[k]["media"], sB[k]["media"]]
    errs = [0, 0, 0, sP[k]["err"], sB[k]["err"]]
    labs = ["radial", "transf.\n" + r"$\tau\to\infty$", "transf.\n" + r"$\tau=20$", "PIGS\nbicúbica", "PIGS\nbilineal"]
    ax[i].errorbar(range(5), vals, yerr=errs, fmt="o", capsize=4, color="C0")
    ax[i].axhline(rr[rk], ls=":", color="C3")
    ax[i].set_xticks(range(5)); ax[i].set_xticklabels(labs, fontsize=8)
    ax[i].set_ylabel(nm); ax[i].set_title(nm + r" en $\delta=0.2$ ($\epsilon=0.1$)")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "12_pigs_delta02.png"), dpi=150); plt.close(fig)

# ------------------------------------------------------------------ guardar
np.savez_compressed(os.path.join(RES, "12_pigs_series.npz"),
                    **{f"{g}_{o['seed']}_{k}": o[k].astype(np.float32) for g in ("prod02", "coul") for o in grupos[g]
                       for k in ("EL", "rmid", "r2mid")})


def limpia(x):
    if isinstance(x, dict):
        return {str(k): limpia(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [limpia(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


out = dict(script="fase2/codigo/12_pigs_produccion.py", fecha=datetime.date.today().isoformat(),
           unidades="hbar=m=g=1; V=-exp(-delta r)/r; eps=0.1; u_T=r e^{-r}; L=10; nscale=4; 20 bloques por cadena",
           tabla=dict(origen=TAB.origen, nt=TAB.nt, banda=TAB.banda, h=TAB.h),
           carga_inicial=list(os.getloadavg()), procesos=NPROC,
           referencia_radial={str(k): v for k, v in ref_rad.items()},
           transferencia={str(dl): {("h=" + str(h) if h != "rich" else "Richardson h^4"):
                                   dict(tau=det[dl][h][0], limite=det[dl][h][1]) for h in (0.02, 0.04, "rich")}
                          for dl in (0.0, 0.2)},
           pigs={k: v for k, v in R.items()},
           coulomb_EL=dict(varianza=varEL, max_desv=maxdev),
           tau_scan=tabla_tau, proyeccion_informativo=proy_info,
           interpolacion=dict(repesado_bil_menos_bic=rw, repesado_inverso_bic_menos_bil=rw_inv,
                              dS_media=dSm, dS_desv=dSs),
           criterios=crit, n_pasa=sum(c["pasa"] for c in crit), n_criterios=len(crit),
           tiempo_mc_s=t_mc, tiempo_total_s=time.perf_counter() - T0)
with open(os.path.join(RES, "12_pigs.json"), "w") as f:
    json.dump(limpia(out), f, indent=1, ensure_ascii=False)
print(f"\nCriterios: {out['n_pasa']}/{out['n_criterios']} pasan. Tiempo total {out['tiempo_total_s']:.1f} s.")
