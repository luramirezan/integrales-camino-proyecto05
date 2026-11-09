"""11_transferencia_controles.py -- Proyecto 05 (Yukawa), Fase 2: controles de la tabla U_C y de la
matriz de transferencia en banda (tareas 2, 3 y 7 de fase1/que_sigue_fase2.md).

Unidades hbar = m = g = 1, V = -e^{-delta r}/r. Metodo: fase1/secciones/09_plan_computo.md (9.3, 9.4, 9.7).
Modulos: pares.py (tabla U_C, Richardson en h_tab), transferencia.py (Nystrom), radial.py (referencia).

Partes
  0. Peso: valores de U_C cerca del origen, positividad de T, comparacion con la primitiva.
  1. Coulomb delta=0, R=40, eps in {0.2,0.1,0.05}: |E+0.5|<1e-6 tras Richardson en h_tab; <r>=1.5 a 1e-4.
  2. delta=0.2, R=40, eps in {0.2,0.1,0.05}, h=0.02 y 0.04: E, <r> frente al radial; orden aparente de
     Trotter y extrapolacion eps->0 (L18). Tambien delta=1.0, R=174 (como la Fase 1).
  3. Estabilidad Nystrom 0.02 -> 0.04 (criterio 1e-6) y orden de la malla Nystrom (h = 0.04, 0.02, 0.01).
  4. Proyeccion determinista E_mixto(tau) desde u_T = r e^{-r} en delta=0.2 (eps=0.1, h=0.02, tabla Richardson).
  5. Interpolacion bilineal y bicubica de U_C (para el PIGS): error en los puntos medios de la malla 0.01.
  6. Informativo: opcion sin U_C con el pozo cuadrado (V0=2, a=1) frente al radial.
Determinista (no usa numeros aleatorios; las semillas 20262000+k no se necesitan aqui).
Salida: fase2/resultados/11_transferencia.json, figuras fase2/figuras/11_*.png.
"""
import json
import os
import sys
import time

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pares                      # noqa: E402
import transferencia as tr        # noqa: E402
import radial                     # noqa: E402  (fase2/codigo/radial.py, ya existe)

T0 = time.perf_counter()
BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")
os.makedirs(RES, exist_ok=True); os.makedirs(FIG, exist_ok=True)
print(f"Carga (loadavg): {os.getloadavg()}")
EPSS = (0.2, 0.1, 0.05)
HS = (0.02, 0.04)
out = dict(script="11_transferencia_controles.py", fecha="2026-10-27", unidades="hbar=m=g=1",
           radial="fase2/codigo/radial.py resolver_rich (DF, Richardson orden 2)")


def orden(E):
    """orden aparente con eps = 0.2, 0.1, 0.05 (razon 2) y extrapolacion eps->0 con ley eps^2."""
    p = float(np.log2(abs(E[0] - E[1]) / abs(E[1] - E[2])))
    ext = float(E[2] + (E[2] - E[1]) / 3)
    return p, ext


# ---------------------------------------------------------------------------- tablas
print("=== Tablas U_C (h_tab = 0.01 y 0.005, R_B = 14, R_TAB = 10, banda 7 sqrt(eps)) ===")
TR, T1, T2 = {}, {}, {}
for e in EPSS:
    t = time.perf_counter()
    TR[e] = pares.tabla_richardson(e)
    T1[e], T2[e] = pares.tabla(e, 0.01), pares.tabla(e, 0.005)
    print(f"eps={e}: banda={TR[e].banda:.4f}  E0 Coulomb red h=0.01: {TR[e].info['E0_red_h1']:.10f}  "
          f"h=0.005: {TR[e].info['E0_red_h2']:.10f}  rho<=0 en banda: {TR[e].info['n_no_positivos']}  "
          f"tiempos {TR[e].info['tiempo']} (0 = cache)  {time.perf_counter()-t:.1f} s")
    nb1 = int(round(1.0 / TR[e].h))
    dif = np.nanmax(np.abs(TR[e].U1[:, :nb1 + 1] - TR[e].U2[:, :nb1 + 1]))
    print(f"    max|U(h_tab=0.01)-U(h_tab=0.005)| en |r-r'|<=1: {dif:.3e}")
    out.setdefault("tablas", {})[str(e)] = dict(banda=TR[e].banda, E0_red_h001=TR[e].info["E0_red_h1"],
                                                E0_red_h0005=TR[e].info["E0_red_h2"],
                                                rho_no_positivos=list(TR[e].info["n_no_positivos"]),
                                                max_dif_htab_banda1=float(dif))

# ---------------------------------------------------------------------------- 0. peso
print("\n=== 0. Declaracion del peso: U_C cerca del origen (tabla Richardson) ===")
peso = {}
for e in EPSS:
    t = TR[e]
    fila = {}
    for (a, b) in ((0.01, 0.01), (0.02, 0.02), (0.05, 0.05), (0.1, 0.1), (0.5, 0.5), (1.0, 1.0),
                   (0.01, 0.5), (0.01, 1.0), (9.0, 9.0)):
        k = int(round(a / t.h)) - 1; m = int(round((b - a) / t.h))
        fila[f"U({a},{b})"] = float(t.Ub[k, m])
    k, m = np.meshgrid(np.arange(t.nt), np.arange(t.nb + 1), indexing="ij")
    val = t.Ub[k + m < t.nt]
    fila["U_min_tabla"], fila["U_max_tabla"] = float(val.min()), float(val.max())
    fila["eps/r_primitiva_en_r=0.01"] = e / 0.01
    T, r = tr.matriz_T(40.0, 0.02, e, W=tr.W_yukawa(0.2), tabla=t)
    fila["T_min_no_nulo"] = float(T.data[T.data > 0].min())
    fila["T_negativos"] = int((T.data < 0).sum())
    fila["T_no_finitos"] = int((~np.isfinite(T.data)).sum())
    fila["max_suma_fila_T"] = float(np.asarray(T.sum(1)).max())
    peso[str(e)] = fila
    print(f"eps={e}: U(0.01,0.01)={fila['U(0.01,0.01)']:.6f} U(0.02,0.02)={fila['U(0.02,0.02)']:.6f} "
          f"U(0.1,0.1)={fila['U(0.1,0.1)']:.6f} U(0.01,0.5)={fila['U(0.01,0.5)']:.6f}  "
          f"min/max U tabla = {fila['U_min_tabla']:.6f}/{fila['U_max_tabla']:.6f}  "
          f"(primitiva: -eps V(0.01) = {e/0.01:.0f}, e^{{{e/0.01:.0f}}})  T: min>0 {fila['T_min_no_nulo']:.2e}, "
          f"negativos {fila['T_negativos']}, max suma de fila {fila['max_suma_fila_T']:.6f}")
out["peso"] = peso

# ---------------------------------------------------------------------------- referencias radiales
print("\n=== Referencias radiales (radial.resolver_rich) ===")
ref = {}
for dl, R in ((0.2, 40.0), (1.0, 174.0)):
    a = radial.resolver_rich(radial.V_yukawa(dl), R, h=1 / 40)
    b = radial.resolver_rich(radial.V_yukawa(dl), R, h=1 / 80)
    ref[dl] = dict(R=R, E0=b["E0"], r_med=b["r_med"], r2_med=b["r2_med"], F12=b["F12"],
                   E0_h40=a["E0"], dif_h40_h80=abs(a["E0"] - b["E0"]), r_med_h40=a["r_med"])
    print(f"delta={dl}, R={R}: E0={b['E0']:.11f} (h=1/80,1/160)  E0(h=1/40,1/80)={a['E0']:.11f}  "
          f"dif={abs(a['E0']-b['E0']):.1e}  <r>={b['r_med']:.7f}  <r^2>={b['r2_med']:.7f}")
ref[0.0] = dict(R=40.0, E0=-0.5, r_med=1.5, r2_med=3.0)
out["referencia_radial"] = {str(k): v for k, v in ref.items()}

# ---------------------------------------------------------------------------- 1 y 2. barridos
print("\n=== 1-2. Transferencia: delta in {0, 0.2, 1.0}, eps in {0.2, 0.1, 0.05}, h in {0.02, 0.04} ===")
res = {}
for dl, R in ((0.0, 40.0), (0.2, 40.0), (1.0, 174.0)):
    res[dl] = {}
    for h in HS:
        for e in EPSS:
            t = time.perf_counter()
            W = tr.W_yukawa(dl)
            o = tr.resolver(R, h, e, W=W, tabla=TR[e])
            e1 = tr.resolver(R, h, e, W=W, tabla=T1[e])["E0"]
            e2 = tr.resolver(R, h, e, W=W, tabla=T2[e])["E0"]
            d = dict(E_tablaRich=o["E0"], E_htab001=e1, E_htab0005=e2, E_RichE=(4 * e2 - e1) / 3,
                     r_med=o["r_med"], r2_med=o["r2_med"], F12=o["F12"], N=o["N"],
                     dE=o["E0"] - ref[dl]["E0"], dr=o["r_med"] - ref[dl]["r_med"], tiempo=time.perf_counter() - t)
            res[dl][(h, e)] = d
            print(f"delta={dl} R={R:.0f} h={h} eps={e}: E={o['E0']:.10f} (h_tab 0.01: {e1:.10f}, 0.005: {e2:.10f}, "
                  f"Rich en E: {d['E_RichE']:.10f})  E-ref={d['dE']:+.2e}  <r>={o['r_med']:.6f} (dif {d['dr']:+.1e})  "
                  f"F_1/2={o['F12']:.6f}  {d['tiempo']:.1f} s")

crit = []


def C(nombre, valor, pasa, criterio):
    crit.append(dict(control=nombre, criterio=criterio, valor=valor, pasa=bool(pasa)))
    print(f"  [{'PASA' if pasa else 'NO PASA'}] {nombre}: {valor}  (criterio: {criterio})")


print("\n--- Control 1: Coulomb delta=0, R=40, h=0.02 ---")
for e in EPSS:
    d = res[0.0][(0.02, e)]
    C(f"Coulomb eps={e} |E+0.5|", f"{abs(d['E_tablaRich']+0.5):.2e} (Rich en E: {abs(d['E_RichE']+0.5):.2e}; "
      f"sin Rich: {abs(d['E_htab001']+0.5):.2e}, {abs(d['E_htab0005']+0.5):.2e})",
      abs(d["E_tablaRich"] + 0.5) < 1e-6, "<1e-6 tras Richardson en h_tab")
    C(f"Coulomb eps={e} |<r>-1.5|", f"{abs(d['r_med']-1.5):.2e}", abs(d["r_med"] - 1.5) < 1e-4, "<1e-4")

print("\n--- Control 2: delta=0.2, R=40 frente al radial ---")
for h in HS:
    for e in EPSS:
        d = res[0.2][(h, e)]
        C(f"delta=0.2 h={h} eps={e} |E-E_rad|", f"{abs(d['dE']):.2e}", abs(d["dE"]) < 1e-6, "<1e-6")
        C(f"delta=0.2 h={h} eps={e} |<r>-<r>_rad|", f"{abs(d['dr']):.2e}", abs(d["dr"]) < 1e-3, "<1e-3")

print("\n--- Ley eps^2 (L18) ---")
trot = {}
for dl in (0.2, 1.0):
    trot[str(dl)] = {}
    for clave, Es in (("h=0.02", [res[dl][(0.02, e)]["E_tablaRich"] for e in EPSS]),
                      ("h=0.04", [res[dl][(0.04, e)]["E_tablaRich"] for e in EPSS]),
                      ("Richardson h^4 (0.02,0.04)",
                       [(16 * res[dl][(0.02, e)]["E_tablaRich"] - res[dl][(0.04, e)]["E_tablaRich"]) / 15
                        for e in EPSS])):
        p, ext = orden(Es)
        trot[str(dl)][clave] = dict(E=Es, E_menos_ref=[x - ref[dl]["E0"] for x in Es], orden=p, extrapolado=ext,
                                   extrap_menos_ref=ext - ref[dl]["E0"])
        print(f"delta={dl} {clave}: E-ref = " + ", ".join(f"{x-ref[dl]['E0']:+.3e}" for x in Es)
              + f"  orden aparente={p:.3f}  extrapolado eps->0={ext:.10f} (dif {ext-ref[dl]['E0']:+.2e})")
    pr = trot[str(dl)]["h=0.02"]
    C(f"Trotter delta={dl} orden aparente (h=0.02, sin Richardson en h)", f"{pr['orden']:.3f}",
      1.8 <= pr["orden"] <= 2.2, "[1.8, 2.2]")
    pr = trot[str(dl)]["Richardson h^4 (0.02,0.04)"]
    C(f"Trotter delta={dl} orden aparente (Richardson en h)", f"{pr['orden']:.3f}",
      1.8 <= pr["orden"] <= 2.2, "[1.8, 2.2]")
    C(f"Trotter delta={dl} |extrapolado-radial| (Richardson en h)", f"{abs(pr['extrap_menos_ref']):.2e}",
      abs(pr["extrap_menos_ref"]) < 1e-6, "<1e-6")
out["trotter"] = trot

print("\n--- Control 3: estabilidad Nystrom 0.02 -> 0.04 ---")
estab = {}
for dl in (0.0, 0.2, 1.0):
    for e in EPSS:
        dd = res[dl][(0.04, e)]["E_tablaRich"] - res[dl][(0.02, e)]["E_tablaRich"]
        estab[f"delta={dl},eps={e}"] = dd
        C(f"Nystrom delta={dl} eps={e} |E(0.04)-E(0.02)|", f"{abs(dd):.2e}  (eps*dif={e*dd:.2e})",
          abs(dd) < 1e-6, "<1e-6")
# orden de la malla Nystrom con h = 0.04, 0.02, 0.01 (tabla Richardson en la malla 0.01)
nys = {}
for dl in (0.0, 0.2):
    for e in EPSS:
        Es = [tr.resolver(40.0, h, e, W=tr.W_yukawa(dl), tabla=TR[e])["E0"] for h in (0.04, 0.02, 0.01)]
        p = float(np.log2(abs(Es[0] - Es[1]) / abs(Es[1] - Es[2])))
        nys[f"delta={dl},eps={e}"] = dict(E=Es, E_menos_ref=[x - ref[dl]["E0"] for x in Es], orden=p)
        print(f"  delta={dl} eps={e}: E(h)-ref para h=0.04,0.02,0.01: "
              + ", ".join(f"{x-ref[dl]['E0']:+.3e}" for x in Es) + f"; orden aparente en h = {p:.2f}")
# diagnostico del origen del error de Nystrom: error por paso eps*dE frente a u'(0)^2 (radial)
diag = {}
for dl, R in ((0.0, 40.0), (0.2, 40.0), (1.0, 174.0)):
    Vr = radial.V_coulomb() if dl == 0 else radial.V_yukawa(dl)
    o = radial.resolver_rich(Vr, R, h=1 / 80)
    # V3 (hallazgo H6 de V1): antes u'(0)^2 ~ (u_1/r_1)^2 con r_1 = 1/160, sesgado por (1 - r_1)^2 = 0.9875.
    # Ahora u'(0) = lim u/r: ajuste cubico de u/r en los 6 primeros nodos, evaluado en r = 0.
    xr = o["rgrid"][:6]; yr = o["u"][:6] / xr
    up0 = float(np.polyval(np.polyfit(xr, yr, 3), 0.0)**2)
    up0_viejo = float((o["u"][0] / o["rgrid"][0])**2)
    porpaso = float(0.1 * (res[dl][(0.04, 0.1)]["E_tablaRich"] - res[dl][(0.02, 0.1)]["E_tablaRich"]))
    diag[str(dl)] = dict(up0_cuadrado=up0, up0_cuadrado_version_anterior=up0_viejo, eps_por_dE=porpaso,
                         cociente=porpaso / up0)
    print(f"  delta={dl}: u'(0)^2 = {up0:.6f} (lim u/r, ajuste cubico; antes u_1/r_1: {up0_viejo:.4f}); "
          f"eps*[E(0.04)-E(0.02)] = {porpaso:.3e}; cociente = {porpaso/up0:.4e}")
Vho = lambda r: 0.5 * r**2
Eho = [tr.resolver(8.0, hh, 0.1, V=Vho)["E0"] for hh in (0.08, 0.04, 0.02)]
diag["oscilador_sin_UC_h=0.08,0.04,0.02"] = Eho
print(f"  oscilador (sin U_C, sin cuspide en el origen), eps=0.1: E(h=0.08,0.04,0.02) = "
      + ", ".join(f"{x:.13f}" for x in Eho) + f"  (variacion {max(Eho)-min(Eho):.1e})")
out["diagnostico_nystrom"] = diag
out["estabilidad_nystrom"] = estab
out["orden_nystrom"] = nys

# ---------------------------------------------------------------------------- 4. proyeccion
print("\n=== 4. Proyeccion determinista desde u_T = r e^{-r} (delta=0.2, eps=0.1, h=0.02, R=40) ===")
dl, e, h, R = 0.2, 0.1, 0.02, 40.0
T, r = tr.matriz_T(R, h, e, W=tr.W_yukawa(dl), tabla=TR[e])
lam, v = tr.autoestado(T, 2)
E0T, E1T = -np.log(lam[0]) / e, -np.log(lam[1]) / e
uT = r * np.exp(-r)
HuT = (tr.W_yukawa(dl)(r) - 0.5) * uT          # H u_T = (W - 1/2) u_T: energia local del H continuo
taus = (1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30)
Em, lim = tr.proyeccion_mixta(T, r, uT, HuT, e, taus, v0=v[:, 0])
proy = dict(E0_T=E0T, E1_T=E1T, brecha=E1T - E0T, limite_mixto=lim, limite_menos_E0T=lim - E0T,
            limite_menos_radial=lim - ref[0.2]["E0"], tau=list(taus), E_mixto=Em,
            E_mixto_menos_limite=[x - lim for x in Em], E_mixto_menos_radial=[x - ref[0.2]["E0"] for x in Em])
print(f"E0(T)={E0T:.10f}  E1(T)={E1T:.6f}  brecha={E1T-E0T:.5f}  limite del mixto={lim:.10f}  "
      f"limite-E0(T)={lim-E0T:+.2e}  limite-radial={lim-ref[0.2]['E0']:+.2e}")
for t_, x in zip(taus, Em):
    print(f"  tau={t_:3d}: E_mixto={x:.10f}  E_mixto-limite={x-lim:+.2e}  E_mixto-radial={x-ref[0.2]['E0']:+.2e}")
var2030 = abs(Em[taus.index(30)] - Em[taus.index(20)])
proy["variacion_tau20_30"] = var2030
mono = bool(np.all(np.diff(Em) < 0))
proy["monotono_decreciente"] = mono
print(f"variacion de tau=20 a 30: {var2030:.2e}; monotono decreciente: {mono}")
C("Proyeccion delta=0.2 |E_mixto(30)-E_mixto(20)|", f"{var2030:.2e}", var2030 < 1e-6, "<1e-6 (de tau a 1.5 tau)")
# V3 (hallazgo H7 de V1): la diferencia limite del mixto - E0(T) con h=0.02 es error de malla de E0(T)?
# Se repite con h=0.04 y se combinan con Richardson h^4 (el limite del mixto usa H continuo en u_T).
T4, r4 = tr.matriz_T(R, 0.04, e, W=tr.W_yukawa(dl), tabla=TR[e])
lam4, v4 = tr.autoestado(T4, 1)
E0T4 = float(-np.log(lam4[0]) / e)
uT4 = r4 * np.exp(-r4); HuT4 = (tr.W_yukawa(dl)(r4) - 0.5) * uT4
lim4 = float((v4[:, 0] @ HuT4) / (v4[:, 0] @ uT4))
limR, E0TR = (16 * lim - lim4) / 15, (16 * E0T - E0T4) / 15
proy["V3_malla"] = dict(E0_T_h004=E0T4, limite_mixto_h004=lim4, limite_menos_E0T_h004=lim4 - E0T4,
                        limite_rich_h4=limR, E0_T_rich_h4=E0TR, limite_menos_E0T_rich_h4=limR - E0TR,
                        E0_T_h002_menos_rich=E0T - E0TR, limite_h002_menos_rich=lim - limR)
print(f"V3: limite-E0(T): h=0.02 {lim-E0T:+.2e}; h=0.04 {lim4-E0T4:+.2e}; Richardson h^4 {limR-E0TR:+.2e}; "
      f"E0(T,h=0.02)-E0(T,Rich) = {E0T-E0TR:+.2e}; limite(h=0.02)-limite(Rich) = {lim-limR:+.2e}")
C("Proyeccion delta=0.2 |limite mixto - E0(T)|", f"{abs(lim-E0T):.2e}", abs(lim - E0T) < 1e-6,
  "<1e-6 (tras Richardson en h_tab; Fase 1 sin tabla Richardson: 4.9e-5)")
out["proyeccion"] = proy

# ---------------------------------------------------------------------------- 5. interpolacion
print("\n=== 5. Interpolacion de U_C (para PIGS): error en los puntos medios de la malla 0.01 ===")
e = 0.1
d2 = pares.tabla_red(e, 0.005)
U2 = d2["Ub"]
# tabla de la red h_tab=0.005 submuestreada en la malla 0.01 (nodos impares de 0.005)
nt1 = TR[e].nt; nb1 = TR[e].nb
Usub = TR[e].U2.copy()
tsub = pares.TablaPares(TR[e].r, Usub, e, 0.01, TR[e].banda, origen="red 0.005 submuestreada a 0.01")
interp = {}
for zona, (lo, hi), bmax in (("r en [0.05,9], |r-r'|<=1", (0.05, 9.0), 1.0), ("r en [0.01,0.1], |r-r'|<=0.1", (0.01, 0.1), 0.1)):
    # puntos medios: nodos pares de la red 0.005 (r = 0.01 k + 0.005)
    k = np.arange(len(d2["r"]))
    rk = d2["r"]
    sel = (k % 2 == 0) & (rk >= lo) & (rk <= hi)
    ka = k[sel]
    pts_a, pts_b, exact = [], [], []
    for mm in range(0, int(round(bmax / 0.005)) + 1, 3):
        kk = ka[ka + mm < U2.shape[0]]
        pts_a.append(rk[kk]); pts_b.append(rk[kk + mm]); exact.append(U2[kk, mm])
    a = np.concatenate(pts_a); b = np.concatenate(pts_b); ex = np.concatenate(exact)
    fila = {}
    for met in ("bilineal", "bicubica"):
        err = np.abs(tsub.valor(a, b, met) - ex)
        fila[met] = dict(max=float(np.nanmax(err)), rms=float(np.sqrt(np.nanmean(err**2))))
    interp[zona] = fila
    print(f"  {zona}: bilineal max {fila['bilineal']['max']:.2e} (rms {fila['bilineal']['rms']:.1e});  "
          f"bicubica max {fila['bicubica']['max']:.2e} (rms {fila['bicubica']['rms']:.1e})")
# por debajo del primer nodo (extrapolacion)
for met in ("bilineal", "bicubica"):
    x = tsub.valor(0.005, 0.005, met)[0]
    interp.setdefault("r=r'=0.005 (extrapolado, bajo el primer nodo 0.01)", {})[met] = float(x - U2[0, 0])
    print(f"  r=r'=0.005 (bajo el primer nodo): {met} - red0.005 = {x-U2[0,0]:+.2e}")
out["interpolacion_eps0.1"] = interp

# ---------------------------------------------------------------------------- 6. pozo cuadrado (informativo)
print("\n=== 6. Opcion sin U_C: pozo cuadrado V0=2, a=1, R=20 (informativo) ===")
Vp = radial.V_pozo(2.0, 1.0, borde="media")
rp = radial.resolver_rich(Vp, 20.0, h=1 / 80)
pozo = dict(E_radial=rp["E0"], r_radial=rp["r_med"])
for h in (0.02, 0.01):
    Es = [tr.resolver(20.0, h, ee, V=Vp)["E0"] for ee in EPSS]
    p, ext = orden(Es)
    pozo[f"h={h}"] = dict(E=Es, orden=p, extrapolado=ext, extrap_menos_radial=ext - rp["E0"])
    print(f"  h={h}: E(eps)=" + ", ".join(f"{x:.8f}" for x in Es) + f"  orden={p:.2f}  extrapolado={ext:.8f} "
          f"(radial {rp['E0']:.8f}, dif {ext-rp['E0']:+.1e})")
out["pozo_informativo"] = pozo

# ---------------------------------------------------------------------------- resumen, json y figuras
out["resultados"] = {str(dl): {f"h={k[0]},eps={k[1]}": v for k, v in dd.items()} for dl, dd in res.items()}
out["criterios"] = crit
out["n_pasa"] = sum(c["pasa"] for c in crit); out["n_criterios"] = len(crit)
out["tiempo_total_s"] = time.perf_counter() - T0
print(f"\nCriterios: {out['n_pasa']} de {out['n_criterios']} pasan.")
for c in crit:
    if not c["pasa"]:
        print("  NO PASA:", c["control"], c["valor"])
fn = os.path.join(RES, "11_transferencia.json")
with open(fn, "w") as f:
    json.dump(out, f, indent=1, ensure_ascii=False, default=float)
print("guardado", fn)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
AZ, NA, AQ = "#2a78d6", "#eb6834", "#1baf7a"
fig, ax = plt.subplots(figsize=(6.4, 4.2))
x = np.array(EPSS)**2
for dl, col, mk in ((0.2, AZ, "o"), (1.0, NA, "s")):
    y = np.array(trot[str(dl)]["Richardson h^4 (0.02,0.04)"]["E_menos_ref"])
    ax.plot(x, y, marker=mk, color=col, lw=2, ms=8,
            label=fr"$\delta={dl}$ (orden {trot[str(dl)]['Richardson h^4 (0.02,0.04)']['orden']:.2f})")
ax.axhline(0, color="#52514e", lw=0.8)
ax.set_xlabel(r"$\epsilon^2$")
ax.set_ylabel(r"$E_0(\epsilon)-E_{\rm radial}$")
ax.set_title("Sesgo de Trotter de la transferencia (Richardson en $h_{tab}$ y en $h$)")
ax.legend(frameon=False); ax.grid(alpha=0.25)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "11_trotter.png"), dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.semilogy(taus[:-1], np.array(Em[:-1]) - lim, marker="o", color=AZ, lw=2, ms=8, label=r"$E_{\rm mixto}(\tau)-$ límite")
ax.axhline(1e-6, color="#52514e", lw=0.8, ls="--")
ax.text(1, 1.3e-6, "1e-6", color="#52514e")
ax.set_xlabel(r"duración de la proyección $\tau$")
ax.set_ylabel(r"$E_{\rm mixto}(\tau)-E_{\rm mixto}(\infty)$")
ax.set_title(r"Proyección desde $u_T=r\,e^{-r}$, $\delta=0.2$, $\epsilon=0.1$")
ax.legend(frameon=False); ax.grid(alpha=0.25, which="both")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "11_proyeccion.png"), dpi=150); plt.close(fig)
print(f"figuras guardadas en {FIG}; tiempo total {time.perf_counter()-T0:.1f} s; carga {os.getloadavg()}")
