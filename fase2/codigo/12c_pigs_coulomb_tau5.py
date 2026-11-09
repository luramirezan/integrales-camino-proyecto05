"""12c_pigs_coulomb_tau5.py -- respuesta a los hallazgos H5 de V1 y H6, H7 de V2 (V3, 27-10-2026).

(A) Control de Coulomb (delta = 0) con 8 cadenas (antes 1): el criterio E_L = -1/2 es tautologico (W = 0 =>
    E_L = -1/2 para cualquier camino, H7 de V2); el control real es <r> y <r^2> puros, ahora con error entre
    cadenas, y una prueba de la DISTRIBUCION: histograma de r_{M/2} frente a [T^{M/2} u_T]^2 de la transferencia.
    tau = 10, eps = 0.1, 3e4 + 500 barridos por cadena, semillas 20262090..20262097.
(B) Segunda replica de tau = 5 (delta = 0.2, eps = 0.1): 16 cadenas de 3e4 + 500 barridos, semillas
    20262070..20262085 (nuevas, sin solape con los rangos 20262000-65 ni con la auditoria 20269000+).
(C) Combinacion de TODAS las cadenas de tau = 5: produccion (8, resultados/12_pigs.json), replica 1 (16,
    resultados/12b_pigs_replica.json), replica 2 (16, esta), y por separado la auditoria de V2 (24 cadenas,
    verificacion/V2_auditoria/mc_audit.json, hecha con el codigo anterior a V3; para delta = 0.2 el cambio de
    U_C fuera de r = 10 mueve E en 2.4e-11, despreciable). chi^2 de consistencia entre corridas.
Criterios (fijados antes de ejecutar): (A) <r>, <r^2> a menos de 2 sigma de 1.5 y 3; histograma p > 1e-3.
(B) E y <r> a menos de 2 sigma de la transferencia. (C) informativo: se reporta, no se decide aqui.
Salida: resultados/12c_pigs_coulomb_tau5.json
"""
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np
from scipy import stats

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pares, pigs, transferencia  # noqa: E402,E401

T0 = time.perf_counter()
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
EPS = 0.1
TAB = pares.tabla_richardson(EPS)
U = pigs.interpolador(TAB, "bicubica")
SEM_C = [20262090 + k for k in range(8)]
SEM_5 = [20262070 + k for k in range(16)]
print(f"Carga (loadavg): {os.getloadavg()}")


def det(delta, tau, h):
    """Transferencia con el mismo eps y la misma accion: E_mixto(tau), <r> y <r^2> puros, y x_{M/2}."""
    T, r = transferencia.matriz_T(40.0, h, EPS, W=transferencia.W_yukawa(delta), tabla=TAB)
    uT = r * np.exp(-r); HuT = (pigs.W_yukawa(delta)(r) - 0.5) * uT
    M = int(round(tau / EPS)); x = uT.copy()
    for _ in range(M // 2):
        x = T @ x; x /= np.abs(x).max()
    xm = x.copy()
    rp = float((r * x**2).sum() / (x**2).sum()); r2p = float((r**2 * x**2).sum() / (x**2).sum())
    for _ in range(M // 2):
        x = T @ x; x /= np.abs(x).max()
    return float((HuT @ x) / (uT @ x)), rp, r2p, r, xm


def ref(delta, tau):
    a, b = det(delta, tau, 0.02), det(delta, tau, 0.04)
    return dict(E=(16 * a[0] - b[0]) / 15, r=(16 * a[1] - b[1]) / 15, r2=(16 * a[2] - b[2]) / 15), a[3], a[4]


def correr(args):
    delta, tau, n, s = args
    o = pigs.cadena(delta, tau, EPS, n, s, U, L=10, ntherm=500, nscale=4)
    return dict(seed=s, EL=o["EL"], rmid=o["rmid"], r2mid=o["r2mid"], M=o["M"], tau_ef=o["tau_ef"],
                acept=(o["acept_puentes"], o["acept_extremos"], o["acept_escala"]), tiempo=o["tiempo"])


trabajos = [(0.0, 10.0, 30000, s) for s in SEM_C] + [(0.2, 5.0, 30000, s) for s in SEM_5]
with mp.get_context("fork").Pool(4) as pool:
    res = pool.map(correr, trabajos, chunksize=1)
coul, t5 = res[:8], res[8:]
print(f"{len(res)} cadenas en {time.perf_counter()-T0:.0f} s")
out = dict(script="fase2/codigo/12c_pigs_coulomb_tau5.py", fecha="2026-10-27", eps=EPS, criterios=[])


def C(nombre, valor, pasa, criterio):
    out["criterios"].append(dict(control=nombre, criterio=criterio, valor=valor, pasa=None if pasa is None else bool(pasa)))
    print(f"  [{'MEDIDO' if pasa is None else ('PASA' if pasa else 'NO PASA')}] {nombre}: {valor}  ({criterio})")


# ------------------------------------------------------------------ (A) Coulomb
print("\n=== (A) Coulomb, tau = 10, 8 cadenas ===")
A = dict(semillas=SEM_C)
EL_all = np.concatenate([o["EL"] for o in coul])
A["E_L"] = dict(varianza=float(EL_all.var()), max_desv=float(np.abs(EL_all + 0.5).max()),
                nota="tautologico: con W = 0, E_L = -1/2 para cualquier camino (H7 de V2)")
refC, rgC, xmC = ref(0.0, 10.0)
A["transferencia"] = refC
for q, exacto in (("rmid", 1.5), ("r2mid", 3.0)):
    c = pigs.combinar([o[q] for o in coul])
    s_ex = (c["media"] - exacto) / c["err"]
    A[q] = dict(c, sigma_exacto=s_ex, sigma_transferencia=(c["media"] - refC["r" if q == "rmid" else "r2"]) / c["err"])
    C(f"(A) Coulomb {q} puro (8 cadenas)", f"{c['media']:.5f} +- {c['err']:.5f} ({s_ex:+.2f} sigma de {exacto}); "
      f"cociente (cadenas/bloques)^2 = {c['cociente']:.2f}", abs(s_ex) < 2, "< 2 sigma del exacto")
# histograma de r_{M/2} frente a x_{M/2}^2 (error por intervalo: dispersion entre las 8 cadenas)
bins = np.linspace(0.0, 8.0, 33)
rr = np.concatenate(([0.0], rgC)); dens = np.concatenate(([0.0], xmC**2))
cdf = np.concatenate(([0.0], np.cumsum(0.5 * (dens[1:] + dens[:-1]) * np.diff(rr))))
P = np.diff(np.interp(bins, rr, cdf / cdf[-1]))
H = np.array([np.histogram(o["rmid"], bins)[0] / len(o["rmid"]) for o in coul])
m_, se = H.mean(0), H.std(0, ddof=1) / np.sqrt(len(H))
ok = se > 0
z = (m_ - P)[ok] / se[ok]
c2 = float((z**2).sum()); dof = int(ok.sum()); pv = float(stats.chi2.sf(c2, dof))
A["histograma_rmid"] = dict(chi2=c2, dof=dof, p=pv, max_z=float(np.abs(z).max()))
C("(A) Coulomb histograma de r_{M/2}", f"chi2 = {c2:.1f} con {dof} intervalos, p = {pv:.3f}", pv > 1e-3, "p > 1e-3")
out["A_coulomb"] = A

# ------------------------------------------------------------------ (B) segunda replica tau = 5
print("\n=== (B) Segunda replica tau = 5, delta = 0.2, 16 cadenas ===")
ref5, _, _ = ref(0.2, 5.0)
B = dict(semillas=SEM_5, transferencia=ref5)
for q, k in (("EL", "E"), ("rmid", "r"), ("r2mid", "r2")):
    c = pigs.combinar([o[q] for o in t5])
    B[q] = dict(c, sigma=(c["media"] - ref5[k]) / c["err"])
    C(f"(B) replica 2 tau=5 {q}", f"{c['media']:.6f} +- {c['err']:.6f} ({B[q]['sigma']:+.2f} sigma; transferencia "
      f"{ref5[k]:.9f})", abs(B[q]["sigma"]) < 2, "< 2 sigma de la transferencia")
out["B_replica2_tau5"] = B

# ------------------------------------------------------------------ (C) combinacion de tau = 5
print("\n=== (C) Todas las cadenas de tau = 5 ===")
p12 = json.load(open(os.path.join(RES, "12_pigs.json")))["pigs"]["tau5"]["EL"]
p12b = json.load(open(os.path.join(RES, "12b_pigs_replica.json")))["replica"]["las_16"]["E"]
corr = dict(produccion=(np.array(p12["medias_cadena"]), np.array(p12["err_bloques_cadena"])),
            replica1=(np.array(p12b["medias_cadena"]), np.array(p12b["err_bloques_cadena"])),
            replica2=(np.array(B["EL"]["medias_cadena"]), np.array(B["EL"]["err_bloques_cadena"])))
Cc = dict(E_det=ref5["E"], por_corrida={})
for k, (m, e) in corr.items():
    err = max(np.sqrt((e**2).sum()) / len(m), m.std(ddof=1) / np.sqrt(len(m)))
    Cc["por_corrida"][k] = dict(n=len(m), media=float(m.mean()), err=float(err), sigma=float((m.mean() - ref5["E"]) / err))
    print(f"  {k}: {len(m)} cadenas, E = {m.mean():.6f} +- {err:.6f} ({(m.mean()-ref5['E'])/err:+.2f} sigma)")
# chi2 de consistencia de las tres corridas frente a E_det
x2 = sum(v["sigma"]**2 for v in Cc["por_corrida"].values())
Cc["chi2_corridas_vs_Edet"] = dict(chi2=float(x2), dof=3, p=float(stats.chi2.sf(x2, 3)))
# combinacion de las 40 cadenas
mm = np.concatenate([v[0] for v in corr.values()]); ee = np.concatenate([v[1] for v in corr.values()])
w = 1 / ee**2
Ew = float((w * mm).sum() / w.sum()); sw = float(np.sqrt(1 / w.sum()))
Eu = float(mm.mean()); su = float(max(np.sqrt((ee**2).sum()) / len(mm), mm.std(ddof=1) / np.sqrt(len(mm))))
chi_c = float((((mm - Ew) / ee)**2).sum())
Cc["las_40"] = dict(media_ponderada=Ew, err_ponderada=sw, sigma_ponderada=(Ew - ref5["E"]) / sw,
                    media_pesos_iguales=Eu, err_pesos_iguales=su, sigma_pesos_iguales=(Eu - ref5["E"]) / su,
                    chi2_por_cadena=chi_c, dof=len(mm) - 1, p_por_cadena=float(stats.chi2.sf(chi_c, len(mm) - 1)),
                    n_bajo_Edet=int((mm < ref5["E"]).sum()))
print(f"  40 cadenas: ponderada {Ew:.6f} +- {sw:.6f} ({(Ew-ref5['E'])/sw:+.2f} sigma); pesos iguales {Eu:.6f} +- {su:.6f} "
      f"({(Eu-ref5['E'])/su:+.2f} sigma); chi2 por cadena {chi_c:.1f}/{len(mm)-1} (p = {Cc['las_40']['p_por_cadena']:.3f}); "
      f"{int((mm < ref5['E']).sum())} de 40 por debajo de E_det")
fa = os.path.join(BASE, "verificacion", "V2_auditoria", "mc_audit.json")
if os.path.exists(fa):
    au = json.load(open(fa))["EL"]
    s_au = max(au["err_bloques"], au["err_cadenas"])
    Cc["auditoria_V2_24_cadenas"] = dict(media=au["media"], err=s_au, sigma=(au["media"] - ref5["E"]) / s_au,
                                         nota="codigo anterior a V3; semillas 20269000-23")
    ws = 1 / sw**2 + 1 / s_au**2
    E64 = (Ew / sw**2 + au["media"] / s_au**2) / ws
    Cc["las_64_con_auditoria"] = dict(media=float(E64), err=float(np.sqrt(1 / ws)),
                                      sigma=float((E64 - ref5["E"]) * np.sqrt(ws)))
    print(f"  auditoria V2 (24): {au['media']:.6f} +- {s_au:.6f} ({(au['media']-ref5['E'])/s_au:+.2f} sigma); "
          f"64 cadenas: {E64:.6f} +- {np.sqrt(1/ws):.6f} ({(E64-ref5['E'])*np.sqrt(ws):+.2f} sigma)")
C("(C) tau=5, 40 cadenas de produccion y replicas", f"{Ew:.6f} +- {sw:.6f} ({(Ew-ref5['E'])/sw:+.2f} sigma, ponderada); "
  f"chi2 de las 3 corridas {x2:.2f}/3 (p = {Cc['chi2_corridas_vs_Edet']['p']:.3f})", None, "informativo")
out["C_tau5_combinado"] = Cc
out["tiempo_s"] = time.perf_counter() - T0
with open(os.path.join(RES, "12c_pigs_coulomb_tau5.json"), "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False, default=float)
print(f"guardado; {out['tiempo_s']:.0f} s")
