"""V1 parte G: compara cada cifra clave de fase2/resultados/*.json con el recalculo propio
(resultados/v1a..v1f) y aplica de nuevo el criterio de cajas 9.6 con numeros propios.
Escribe resultados/v1_comparacion.json y resultados/v1_tabla.md."""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..','..'))  # raiz del repositorio
import json
import numpy as np

P = _RAIZ + "/fase2/resultados/"
p10 = json.load(open(P + "10_radial.json")); p11 = json.load(open(P + "11_transferencia.json"))
p12 = json.load(open(P + "12_pigs.json")); p12b = json.load(open(P + "12b_pigs_replica.json"))
p13 = json.load(open(P + "13_controles.json")); p14 = json.load(open(P + "14_cajas.json"))
A = json.load(open("resultados/v1a_radial.json")); B = json.load(open("resultados/v1b_trotter.json"))
Bf = json.load(open("resultados/v1b_trotter_fino.json"))
C = json.load(open("resultados/v1c_nystrom.json")); Dp = json.load(open("resultados/v1d_pigs.json"))
E = json.load(open("resultados/v1e_proyeccion.json")); Fx = json.load(open("resultados/v1f_extremos.json"))

filas = []
def fila(bloque, cifra, vp, vo, metodo, tol, nota="", rel=False):
    dif = vo - vp if (vp is not None and vo is not None) else None
    if dif is None:
        ok = None
    else:
        ok = bool(abs(dif) <= tol * (abs(vo) if rel else 1.0))
    filas.append(dict(bloque=bloque, cifra=cifra, proyecto=vp, propio=vo, metodo=metodo, dif=dif, tol=tol,
                      tol_rel=rel, coincide=ok, nota=nota))

DIS = "disparo solve_ivp DOP853 (rtol 1e-12)"
SPE = "Trotter espectral FEDVR (h->0 exacto)"
NYS = "Nystrom propio con rho_C espectral FEDVR (Rb=46)"
# ---------------- A: radial ----------------
c = p10["coulomb"]["R60"]
fila("radial", "Coulomb E0", c["E0"], A["coulomb"]["E0"], DIS, 1e-8)
fila("radial", "Coulomb E1", c["E1"], A["coulomb"]["E1"], DIS, 1e-8)
fila("radial", "Coulomb <r>", c["r_med"], A["coulomb"]["r"], DIS, 1e-7)
fila("radial", "Coulomb <r^2>", c["r2_med"], A["coulomb"]["r2"], DIS, 1e-7)
y = p10["yukawa_0.2"]["R40"]
fila("radial", "delta=0.2 E0 (10_radial, h=1/40,1/80)", y["E0"], A["yukawa_0.2"]["E0"], DIS, 5e-9,
     "criterio del proyecto |E0+0.32680851|<5e-9 se cumple frente al valor redondeado, no frente al exacto")
fila("radial", "delta=0.2 E0 (referencia de 11_transferencia)", p11["referencia_radial"]["0.2"]["E0"], A["yukawa_0.2"]["E0"], DIS, 5e-9)
fila("radial", "delta=0.2 <r>", y["r_med"], A["yukawa_0.2"]["r"], DIS, 5e-5)
fila("radial", "delta=0.2 <r^2>^1/2", y["r_rms"], A["yukawa_0.2"]["rrms"], DIS, 5e-5)
fila("radial", "delta=0.2 E1 (R=60)", p10["yukawa_0.2"]["R60"]["E1"], A["yukawa_0.2"]["E1_R60"], DIS + " en caja R=60", 1e-8)
fila("radial", "delta=1.0 E0 (referencia de 11, R=174)", p11["referencia_radial"]["1.0"]["E0"], A["yukawa_1.0"]["E0"], DIS, 1e-8)
fila("radial", "delta_c (1s)", p10["delta_c"]["yukawa_1s"]["R800"], A["umbrales"]["delta_c_1s"], DIS + ", E=0, u'(60/delta)=0", 1e-8)
fila("radial", "delta_c (2s)", p10["delta_c"]["yukawa_2s_R400"], A["umbrales"]["delta_c_2s"], DIS + ", E=0", 1e-8)
for d in ("0.2", "1.0", "1.5"):
    fila("radial", f"Hulthen {d} E0 radial (13)", p13["A_hulthen"][d]["E_radial"], A["hulthen"][d]["E0"], DIS, 1e-8)
    fila("radial", f"Hulthen {d} <r> exacto (sympy)", p13["A_hulthen"][d]["r_exacto"], A["hulthen"][d]["r"], DIS, 2e-7, rel=True)
fila("radial", "Hulthen umbral 1s", 2.0, A["umbrales"]["hulthen_1s"], DIS, 1e-8)
fila("radial", "Hulthen umbral 2s", 0.5, A["umbrales"]["hulthen_2s"], DIS, 1e-8)
fila("radial", "Hulthen 0.2 E1", -0.045, A["hulthen"]["0.2"]["E1"], DIS, 1e-8)
for V0 in ("2.0", "1.3"):
    fila("radial", f"pozo V0={V0} E exacta", p13["B_pozo"][V0]["E_exacta"], A["pozo"][V0]["E_exacta"], "raiz propia de k cot k = -kappa", 1e-12)
    fila("radial", f"pozo V0={V0} E radial borde medio", p13["B_pozo"][V0]["E_radial_media"], A["pozo"][V0]["E_disparo"], DIS + " con salto", 2e-8)
    fila("radial", f"pozo V0={V0} <r> exacto", p13["B_pozo"][V0]["r_exacto"], A["pozo"][V0]["r_disparo"], DIS, 1e-8)
fila("radial", "pozo umbral pi^2/8", np.pi**2 / 8, A["pozo"]["umbral_disparo"], DIS + ", E=0", 1e-8)
for d in ("1.15", "1.18", "1.2"):
    fila("radial", f"a_s delta={d}", p14["a_s"][d], A["cajas"][f"a_s_{d}"], DIS + ", E=0", 1e-6, rel=True)
for d in ("1.15", "1.18", "1.2"):
    for R in (50, 100, 200, 400, 800):
        pr = p14["celdas"][d][f"R{R}"]["radial"]; mo = A["cajas"][f"{d}_R{R}"]
        fila("cajas-radial", f"E0 delta={d} R={R}", pr["E0"], mo["E0"], DIS + " u(R)=0", pr["err"], "tol = error declarado del radial")
        fila("cajas-radial", f"<r>/R delta={d} R={R}", pr["r_sobre_R"], mo["r_sobre_R"], DIS, 5e-4, "3 cifras")
        fila("cajas-radial", f"F_1/2 delta={d} R={R}", pr["F12"], mo["F12"], DIS + " (FEDVR si kappa R>10)", 5e-4, "3 cifras")
fila("cajas-radial", "errata 9.6: E0(1.18, R=400) a 3 cifras", -3.08e-5, float(f"{A['cajas']['1.18_R400']['E0']:.2e}"), DIS, 0.0,
     "el valor propio redondea a -3.07e-5: se confirma la errata de la Fase 1")
# ---------------- B: transferencia ----------------
for eps in ("0.2", "0.1", "0.05"):
    for k in ("U(0.01,0.01)", "U(0.02,0.02)", "U(9.0,9.0)"):
        kk = k.replace("9.0", "9")
        fila("pares", f"{k} eps={eps}", p11["peso"][eps][k], C["U_C"][eps][kk], "suma espectral FEDVR / K_D exacto", 1e-6)
for i, eps in enumerate(("0.2", "0.1", "0.05")):
    fila("transferencia", f"Coulomb h=0.02 E+0.5 eps={eps}", p11["orden_nystrom"][f"delta=0.0,eps={eps}"]["E_menos_ref"][1],
         C["nystrom"][f"d0_eps{eps}"]["0.02"][0] + 0.5, NYS, 1e-8, "tabla con Richardson del proyecto deja ~1e-9/eps")
    fila("transferencia", f"Coulomb, E de Trotter h->0, eps={eps}", -0.5, B["coulomb"]["E"][i], SPE, 1e-9)
    fila("transferencia", f"delta=0.2 h=0.02 E eps={eps}", p11["trotter"]["0.2"]["h=0.02"]["E"][i], C["nystrom"][f"d0.2_eps{eps}"]["0.02"][0], NYS, 1e-8)
    fila("transferencia", f"delta=0.2 h=0.04 E eps={eps}", p11["trotter"]["0.2"]["h=0.04"]["E"][i], C["nystrom"][f"d0.2_eps{eps}"]["0.04"][0], NYS, 1e-8)
    fila("transferencia", f"estabilidad Nystrom delta=0 eps={eps}", p11["estabilidad_nystrom"][f"delta=0.0,eps={eps}"],
         C["nystrom"][f"d0_eps{eps}"]["dE_0.02_0.04"], NYS, 2e-8)
    fila("transferencia", f"orden Nystrom delta=0 eps={eps}", p11["orden_nystrom"][f"delta=0.0,eps={eps}"]["orden"], C["nystrom"][f"d0_eps{eps}"]["orden_h"], NYS, 0.01)
    fila("transferencia", f"delta=0.2 E Richardson h^4 eps={eps}", p11["trotter"]["0.2"]["Richardson h^4 (0.02,0.04)"]["E"][i], B["yukawa_0.2"]["E"][i], SPE, 1e-6,
         "tol del plan 1e-6; dif. real ~1e-9/eps (residuo de la tabla)")
    fila("transferencia", f"delta=1.0 E Richardson h^4 eps={eps}", p11["trotter"]["1.0"]["Richardson h^4 (0.02,0.04)"]["E"][i], B["yukawa_1.0"]["E"][i], SPE, 1e-6,
         "dif. sistematica = aprox. de extremos r>10 (parte F)")
E2 = [C["nystrom"][f"d0.2_eps{e}"]["0.02"][0] for e in ("0.2", "0.1", "0.05")]
fila("transferencia", "delta=0.2 orden Trotter h=0.02 sin Richardson", p11["trotter"]["0.2"]["h=0.02"]["orden"], float(np.log2((E2[0] - E2[1]) / (E2[1] - E2[2]))), NYS, 0.05)
fila("transferencia", "delta=0.2 orden Trotter (Richardson h)", p11["trotter"]["0.2"]["Richardson h^4 (0.02,0.04)"]["orden"], B["yukawa_0.2"]["orden"], SPE, 0.05)
fila("transferencia", "delta=0.2 E extrapolado eps->0", p11["trotter"]["0.2"]["Richardson h^4 (0.02,0.04)"]["extrapolado"], B["yukawa_0.2"]["ext_orden"], SPE, 1e-6)
fila("transferencia", "delta=0.2 E extrapolado frente al radial exacto", A["yukawa_0.2"]["E0"], B["yukawa_0.2"]["ext_orden"], SPE + " vs disparo", 1e-9)
fila("transferencia", "delta=1.0 orden Trotter (Richardson h)", p11["trotter"]["1.0"]["Richardson h^4 (0.02,0.04)"]["orden"], B["yukawa_1.0"]["orden"], SPE, 0.05)
fila("transferencia", "delta=1.0 E extrapolado eps->0", p11["trotter"]["1.0"]["Richardson h^4 (0.02,0.04)"]["extrapolado"], B["yukawa_1.0"]["ext_orden"], SPE, 1e-6)
fila("transferencia", "delta=0.2 <r> h=0.02 eps=0.1", None, None, "", 0)
filas.pop()
for i, eps in enumerate(("0.2", "0.1", "0.05")):
    fila("transferencia", f"delta=0.2 <r> h=0.02 eps={eps}", None if False else C["nystrom"][f"d0.2_eps{eps}"]["0.02"][1], C["nystrom"][f"d0.2_eps{eps}"]["0.02"][1], NYS, 0)
    filas.pop()
# proyeccion
taus = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30]
lim_mio = E["n12_l0.5"]["60.0"]["E_mixto"]
for t, ep in zip(taus, p11["proyeccion"]["E_mixto"]):
    if t in (1, 5, 10, 20, 30):
        fila("proyeccion", f"E_mixto(tau={t}) eps=0.1 (11, h=0.02)", ep, E["n12_l0.5"][f"{float(t)}"]["E_mixto"], SPE, 1e-8)
fila("proyeccion", "E_mixto(20)-limite", p11["proyeccion"]["E_mixto_menos_limite"][9], E["n12_l0.5"]["20.0"]["E_mixto"] - lim_mio, SPE, 1e-8)
fila("proyeccion", "variacion E_mixto tau 20->30", p11["proyeccion"]["variacion_tau20_30"],
     E["n12_l0.5"]["20.0"]["E_mixto"] - E["n12_l0.5"]["30.0"]["E_mixto"], SPE, 1e-9)
fila("proyeccion", "limite del mixto - E0(T)", p11["proyeccion"]["limite_menos_E0T"], lim_mio - B["yukawa_0.2"]["E"][1], SPE, 1e-6,
     "proyecto: 1.05e-7 es error Nystrom de E0(T) con h=0.02; en el continuo es <1e-9")
for row in p12["tau_scan"]:
    t = row["tau"]
    fila("pigs-det", f"E_det tau={t:g} (Richardson h)", row["E_det"], E["n12_l0.5"][f"{t}"]["E_mixto"], SPE, 1e-8)
    fila("pigs-det", f"<r>_det tau={t:g}", row["r_det"], E["n12_l0.5"][f"{t}"]["r_puro"], SPE, 1e-6)
    fila("pigs-det", f"<r^2>_det tau={t:g}", row["r2_det"], E["n12_l0.5"][f"{t}"]["r2_puro"], SPE, 1e-6)
    sig = (row["E_pigs"] - E["n12_l0.5"][f"{t}"]["E_mixto"]) / row["eE"]
    fila("pigs-det", f"sigma E PIGS tau={t:g}", row["sigma_E"], sig, "PIGS del proyecto frente a E_det propio", 0.05)
r5 = p12b["replica"]["las_16"]
fila("pigs-det", "replica tau=5 sigma E (16 semillas)", r5["sigma_E"], (r5["E"]["media"] - E["n12_l0.5"]["5.0"]["E_mixto"]) / r5["E"]["err"], "replica frente a E_det propio", 0.05)
# PIGS series
pp = p12["pigs"]
for o, lab in (("EL", "E"), ("rmid", "<r>"), ("r2mid", "<r^2>")):
    fila("pigs-series", f"delta=0.2 PIGS {lab} media", pp["prod02"][o]["media"], Dp[f"prod02_{o}"]["media"], "media propia de las series .npz", 1e-6, rel=True)
    fila("pigs-series", f"delta=0.2 PIGS {lab} error", pp["prod02"][o]["err"], Dp[f"prod02_{o}"]["err"], "max(binning FP, entre cadenas) propio", 0.1, rel=True)
    fila("pigs-series", f"Coulomb PIGS {lab} media", pp["coul"][o]["media"], Dp[f"coul_{o}"]["media"], "media propia", 1e-6, rel=False)
    if o != "EL":
        fila("pigs-series", f"Coulomb PIGS {lab} error", pp["coul"][o]["err"], Dp[f"coul_{o}"]["err"], "binning FP propio", 0.1, rel=True)
    fila("pigs-series", f"delta=0.2 tau_int {lab}", pp["prod02"][o]["tau_int_sokal"], Dp[f"prod02_{o}"]["tau_int_medio"], "ventana automatica propia (c=6)", 0.05, rel=True)
fila("pigs-series", "Coulomb var(E_L)", 0.0, Dp["coul_EL_var"], "series", 0.0)
refE = A["yukawa_0.2"]
for o, lab, ref in (("EL", "E", refE["E0"]), ("rmid", "<r>", refE["r"]), ("r2mid", "<r^2>", refE["r2"])):
    s_p = (pp["prod02"][o]["media"] - p12["referencia_radial"]["0.2"][{"EL": "E0", "rmid": "r", "r2mid": "r2"}[o]]) / pp["prod02"][o]["err"]
    s_m = (Dp[f"prod02_{o}"]["media"] - ref) / Dp[f"prod02_{o}"]["err"]
    fila("pigs-series", f"delta=0.2 sigma {lab} frente al radial", s_p, s_m, "series + disparo", 0.05)
# Hulthen transferencia
for d in ("0.2", "1.0", "1.5"):
    Eex = -0.5 * (1 - float(d) / 2)**2
    for i, eps in enumerate(("0.2", "0.1", "0.05", "0.025")):
        fila("hulthen", f"Hulthen {d} E(eps={eps})-E_ex", p13["A_hulthen"][d]["E_menos_exacta_rich_h4"][i], B["hulthen"][d]["E"][i] - Eex, SPE, 1e-6,
             "tol. del plan; en 1.5 queda una dif. sistematica ~eps^1.5 (aprox. de extremos, parte F)" if d == "1.5" else "residuo de la tabla ~1e-9/eps")
    fila("hulthen", f"Hulthen {d} orden Trotter", p13["A_hulthen"][d]["orden_trotter"], B["hulthen"][d]["orden"], SPE, 0.05,
             "el proyecto lo declara informativo; el orden verdadero es 2" if d == "0.2" else "")
    fila("hulthen", f"Hulthen {d} E extrapolado - E_ex", p13["A_hulthen"][d]["dE_ext"], B["hulthen"][d]["ext_eps2"] - Eex, SPE, 1e-6)
    rex = (12 - float(d)**2) / (2 * (4 - float(d)**2))
    fila("hulthen", f"Hulthen {d} <r> extrapolado - exacto", p13["A_hulthen"][d]["dr_ext"], B["hulthen"][d]["r_ext_eps2"] - rex, SPE, 1e-4)
# pozo
for V0 in ("2.0", "1.3"):
    pm = p13["B_pozo"][V0]["media"]; mo = B["pozo"][V0]
    for i, eps in enumerate(mo["eps"]):
        fila("pozo", f"pozo {V0} E h->0 eps={eps:g} (borde medio)", pm["E_h0"][i], mo["E"][i], SPE + " (salto en borde de elemento)", 1e-5)
    for i in range(3):
        fila("pozo", f"pozo {V0} orden Trotter local {i+1}", pm["ordenes_locales_eps"][i], mo["ordenes"][i], SPE, 0.05)
    Eex = A["pozo"][V0]["E_exacta"]
    fila("pozo", f"pozo {V0} E extrapolado (orden medido) - exacta", pm["dE_ext_orden_medido"], mo["ext_orden_medido"] - Eex, SPE, 1e-5)
    # ajuste a 5 puntos con eps^1.5
    eps = np.array(mo["eps"]); Ev = np.array(mo["E"])
    M = np.vstack([np.ones_like(eps), eps**1.5]).T
    c5 = np.linalg.lstsq(M, Ev, rcond=None)[0]
    fila("pozo", f"pozo {V0} ajuste 5 puntos eps^1.5 - exacta", pm["ajuste_eps15_5puntos"]["dE0"], c5[0] - Eex, SPE, 1e-5)
    fila("pozo", f"pozo {V0} E h->0 eps=0.2 borde estricto (el proyecto lo declara no convergido)", p13["B_pozo"][V0]["estricta"]["E_h0"][0], mo["E"][0], SPE + " (el limite h->0 no depende del borde)", 1e-5)
    r = np.array(mo["r"]); pr_ = float(np.log2((r[-3] - r[-2]) / (r[-2] - r[-1])))
    rext = r[-1] - (r[-2] - r[-1]) / (2**pr_ - 1)
    fila("pozo", f"pozo {V0} <r> extrapolado - exacto", p13["B_pozo"][V0]["r_media"]["dr_ext"], rext - A["pozo"][V0]["r_disparo"], SPE, 1e-3 if V0 == "2.0" else 5e-3)
# cajas transferencia
for d in ("1.15", "1.18", "1.2"):
    for R in (50, 100, 200, 400, 800):
        pc = p14["celdas"][d][f"R{R}"]; mo = B["cajas"][f"{d}_R{R}"]
        rad = A["cajas"][f"{d}_R{R}"]["E0"]
        fila("cajas-transf", f"E0 transf. delta={d} R={R}", pc["E_mejor"], mo["ext_eps2"], SPE + ", pared Dirichlet verdadera", pc["err"],
             f"E_proy - radial exacto = {pc['E_mejor'] - rad:+.2e}; mio - radial = {mo['ext_eps2'] - rad:+.2e}")
        fila("cajas-transf", f"orden Trotter delta={d} R={R}", pc["orden_trotter"], mo["orden"], SPE, 0.1)
# pared corrida
for d in ("1.15", "1.18", "1.2"):
    for R in (50, 100):
        for i, eps in enumerate(("0.2", "0.1", "0.05")):
            fila("pared", f"E_hRich({eps}) delta={d} R={R}", p14["celdas"][d][f"R{R}"]["E_hRich"][eps], B["pared"][f"{d}_R{R}"][i],
                 SPE + " en R+0.5826 sqrt(eps)", 2e-7)
json.dump(filas, open("resultados/v1_comparacion.json", "w"), indent=1, default=float)

# ----------- criterio 9.6 con numeros propios -----------
def criterio(Es, eEs, rr, Fs, malla, a_s, terna):
    dec = lambda x: all(x[i + 1] < x[i] for i in range(2)); inc = lambda x: all(x[i + 1] > x[i] for i in range(2))
    neg = [Es[i] < 0 and abs(Es[i]) > eEs[i] for i in range(3)]; pos = [Es[i] > 0 and abs(Es[i]) > eEs[i] for i in range(3)]
    a = neg[1] and neg[2] and abs(Es[2] - Es[1]) < 0.1 * abs(Es[2]); ap = all(m < 0.1 for m in malla)
    b = dec(rr) and inc(Fs) and Fs[2] > 0.95
    ley = [np.pi**2 / (2 * (R - a_s)**2) for R in terna]; dev = [abs(Es[i] - ley[i]) / ley[i] for i in range(3)]
    nl = all(pos) and inc(rr) and dec(Fs) and dev[2] < 0.1 and dev[2] < dev[1] < dev[0] and ap
    return dict(a=bool(a), ap=bool(ap), b=bool(b), ligado=bool(a and ap and b), no_ligado=bool(nl), dev=dev,
                sat=abs(Es[2] - Es[1]) / abs(Es[2]))
ver = {}
for d in ("1.15", "1.18", "1.2"):
    ver[d] = {}
    for terna in ((50, 100, 200), (100, 200, 400), (200, 400, 800)):
        cr = [A["cajas"][f"{d}_R{R}"] for R in terna]
        rad = criterio([x["E0"] for x in cr], [1e-10] * 3, [x["r_sobre_R"] for x in cr], [x["F12"] for x in cr],
                       [abs(x["fedvr"]["E0"] - x["E0"]) / abs(x["E0"]) for x in cr], A["cajas"][f"a_s_{d}"], terna)
        ct = [B["cajas"][f"{d}_R{R}"] for R in terna]
        tr = criterio([x["ext_eps2"] for x in ct], [abs(x["ext_eps2"] - x["ext_eps2_2pts"]) for x in ct],
                      [x["r_ext_eps2"] / R for x, R in zip(ct, terna)], [x["F12"][-1] for x in ct],
                      [abs(x["ext_eps2"] - x["ext_eps2_2pts"]) / abs(x["ext_eps2"]) for x in ct], A["cajas"][f"a_s_{d}"], terna)
        cc = all(np.sign(x["E0"]) == np.sign(y["ext_eps2"]) for x, y in zip(cr, ct))
        ver[d][str(terna)] = dict(radial=rad, transferencia=tr, c_mismo_signo=bool(cc))
    print(d, {k: (v["radial"]["ligado"], v["radial"]["no_ligado"], v["transferencia"]["ligado"], v["transferencia"]["no_ligado"],
                 round(v["radial"]["sat"], 3), [round(x, 3) for x in v["radial"]["dev"]]) for k, v in ver[d].items()})
json.dump(ver, open("resultados/v1_veredictos.json", "w"), indent=1, default=float)

# ----------- tabla markdown -----------
def f(x):
    if x is None: return "-"
    if isinstance(x, (bool, np.bool_)): return str(x)
    if abs(x) != 0 and (abs(x) < 1e-3 or abs(x) >= 1e4): return f"{x:.10e}"
    return f"{x:.12g}"
lin = ["| bloque | cifra | valor del proyecto | valor propio | método propio | diferencia | tolerancia | coincide |", "|---|---|---|---|---|---|---|---|"]
for r in filas:
    tol = f"{r['tol']:.1e}" + (" rel." if r["tol_rel"] else "")
    co = "sí" if r["coincide"] else ("no" if r["coincide"] is not None else "-")
    d = "-" if r["dif"] is None else f"{r['dif']:+.2e}"
    nota = f" ({r['nota']})" if r["nota"] else ""
    lin.append(f"| {r['bloque']} | {r['cifra']}{nota} | {f(r['proyecto'])} | {f(r['propio'])} | {r['metodo']} | {d} | {tol} | {co} |")
open("resultados/v1_tabla.md", "w").write("\n".join(lin) + "\n")
n = len(filas); ns = sum(1 for r in filas if r["coincide"]); nn = [r for r in filas if r["coincide"] is False]
print("filas", n, "coinciden", ns, "no coinciden", len(nn))
for r in nn:
    print("  NO:", r["bloque"], r["cifra"], r["proyecto"], r["propio"], r["dif"], r["tol"], r["nota"])
