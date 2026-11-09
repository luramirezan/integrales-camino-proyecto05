"""10_radial_controles.py -- cifras de referencia del solucionador radial (Fase 2, proyecto 05).

Corre radial.py en todos los puntos de control y guarda:
  fase2/resultados/10_radial.json          (todas las cifras, con todas sus cifras)
  fase2/resultados/10_radial_u_delta02.npz (u(r) normalizado de delta=0.2 en R=40 y R=60, malla h=1/80)
  fase2/figuras/10_radial_convergencia.png (error frente a h: orden aparente)
Unidades hbar=m=g=1, V = -e^{-delta r}/r. Malla h=1/40 y 1/80 con Richardson (p=2) salvo que se diga.
Es determinista: no usa numeros aleatorios (la semilla 20262000 se fija solo por convencion del proyecto).
Tiempo: ~15 s en un nucleo.
"""
import sys, os, json, time, platform
import numpy as np
import scipy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import radial as rd

np.random.seed(20262000)
# V3 (hallazgo H9 de V2): ruta relativa a este archivo, no fija (antes BASE = "/mnt/project-files/fase2/")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
OUT_JSON = BASE + "resultados/10_radial.json"
OUT_NPZ = BASE + "resultados/10_radial_u_delta02.npz"
OUT_FIG = BASE + "figuras/10_radial_convergencia.png"
H = 1 / 40
t0 = time.perf_counter()


def limpio(o):
    """Quita los arreglos del dict de resolver_rich para guardarlo en JSON."""
    return {k: (float(v) if isinstance(v, (float, np.floating)) else v) for k, v in o.items()
            if not isinstance(v, np.ndarray)}


res = dict(meta=dict(script="fase2/codigo/10_radial_controles.py", modulo="fase2/codigo/radial.py",
                     fecha="2026-10-27", unidades="hbar=m=g=1; V=-exp(-delta r)/r; energias en m g^2/hbar^2",
                     malla="diferencias finitas 2o orden, h=1/40 y h/2=1/80 (N y 2N+1 puntos), Richardson p=2",
                     caja="Dirichlet u(R)=0; R=max(60,25/kappa) salvo que se indique",
                     F12="trapecio con medio peso en r=R/2", python=platform.python_version(),
                     numpy=np.__version__, scipy=scipy.__version__))

# ----------------------------------------------------------------------------- Coulomb
print("=== Coulomb (delta=0), R=60 ===")
o = rd.resolver_rich(rd.V_coulomb(), 60.0, H)
_, pC = rd.orden_aparente(rd.V_coulomb(), 60.0, [1 / 20, 1 / 40, 1 / 80, 1 / 160], exacto=-0.5)
print(f"E0={o['E0']:.12f} (exacto -0.5, dif {o['E0']+0.5:+.2e})  E1={o['E1']:.12f} (exacto -0.125)  "
      f"<r>={o['r_med']:.10f}  <r^2>={o['r2_med']:.10f}  F_1/2={o['F12']:.12f}  |E_h-E_h/2|={o['dE']:.2e}")
print(f"orden aparente de E0 (h=1/20..1/160): {pC}")
res["coulomb"] = dict(R60=limpio(o), exacto=dict(E0=-0.5, E1=-0.125, r_med=1.5, r2_med=3.0),
                      orden_aparente_E0=pC)
o40 = rd.resolver_rich(rd.V_coulomb(), 40.0, H)
res["coulomb"]["R40"] = limpio(o40)
print(f"R=40: E0={o40['E0']:.12f}  <r>={o40['r_med']:.10f}")

# ----------------------------------------------------------------------------- delta = 0.2
print("\n=== Yukawa delta=0.2 (punto fuertemente ligado) ===")
res["yukawa_0.2"] = {}
Vy = rd.V_yukawa(0.2)
for R in (40.0, 60.0):
    o = rd.resolver_rich(Vy, R, H)
    print(f"R={R:.0f}: E0={o['E0']:.12f}  E1={o['E1']:.10f}  <r>={o['r_med']:.10f}  <r^2>={o['r2_med']:.10f}  "
          f"<r^2>^1/2={o['r_rms']:.10f}  F_1/2={o['F12']:.12f}  brecha={o['E1']-o['E0']:.10f}  |E_h-E_h/2|={o['dE']:.2e}")
    res["yukawa_0.2"][f"R{R:.0f}"] = limpio(o)
# 2s convergido en caja (kappa_1 ~ 0.156)
E1 = res["yukawa_0.2"]["R60"]["E1"]
R1 = rd.caja_recomendada(E1, entera=True)
o = rd.resolver_rich(Vy, R1, H)
print(f"R={R1:.0f} (caja para el 2s): E0={o['E0']:.12f}  E1={o['E1']:.12f}  brecha={o['E1']-o['E0']:.10f}")
res["yukawa_0.2"][f"R{R1:.0f}_caja_2s"] = limpio(o)
# V3 (hallazgo H4 de V1): el criterio |E0+0.32680851|<5e-9 se aplicaba contra la referencia redondeada a 8
# cifras. Referencia fina: Richardson con mallas mas finas (R=40); el error de h=1/40,1/80 se mide contra ella.
fina = {}
for hh in (1 / 40, 1 / 80, 1 / 160, 1 / 320):
    o = rd.resolver_rich(Vy, 40.0, hh, nev=1)
    fina[f"h=1/{round(1/hh)}"] = dict(E0=float(o["E0"]), r_med=float(o["r_med"]))
E_fina = fina["h=1/320"]["E0"]
for k_, v_ in fina.items():
    v_["E0_menos_fina"] = v_["E0"] - E_fina
    print(f"  delta=0.2, R=40, Richardson {k_} y h/2: E0={v_['E0']:.13f}  E0-E(1/320)={v_['E0_menos_fina']:+.2e}")
res["yukawa_0.2"]["V3_referencia_fina"] = dict(
    mallas=fina, E0_fina=E_fina, referencia_V1_disparo_FEDVR=-0.3268085113692,
    error_h40_frente_fina=fina["h=1/40"]["E0_menos_fina"], error_h80_frente_fina=fina["h=1/80"]["E0_menos_fina"],
    criterio_5e9_h40_frente_exacto=bool(abs(fina["h=1/40"]["E0_menos_fina"]) < 5e-9),
    criterio_5e9_h80_frente_exacto=bool(abs(fina["h=1/80"]["E0_menos_fina"]) < 5e-9))
print(f"  criterio 5e-9 frente al exacto: h=1/40 -> {abs(fina['h=1/40']['E0_menos_fina']) < 5e-9}; "
      f"h=1/80 -> {abs(fina['h=1/80']['E0_menos_fina']) < 5e-9}")
_, p02 = rd.orden_aparente(Vy, 60.0, [1 / 20, 1 / 40, 1 / 80, 1 / 160])
print(f"orden aparente de E0 (tres mallas, sin exacto): {p02}")
res["yukawa_0.2"]["orden_aparente_E0"] = p02
# autovector para los demas modulos
oa, ob = rd.resolver(Vy, 40.0, N=2 * (int(round(40 / H)) - 1) + 1), rd.resolver(Vy, 60.0, N=2 * (int(round(60 / H)) - 1) + 1)
np.savez(OUT_NPZ, r_R40=oa["r"], u_R40=oa["u"], E0_R40=oa["E0"], r_R60=ob["r"], u_R60=ob["u"], E0_R60=ob["E0"],
         nota="u normalizado con int u^2 dr = 1, malla h=1/80 sin Richardson (E0 de esa malla)")

# ----------------------------------------------------------------------------- umbral delta_c
print("\n=== Umbral por energia cero ===")
dcs = {}
for R in (200.0, 400.0, 800.0):
    dcs[f"R{R:.0f}"] = rd.umbral(rd.V_yukawa, 1.1, 1.3, R=R)
    print(f"R={R:.0f}: delta_c={dcs[f'R{R:.0f}']:.13f}  dif ref Fase 1 = {dcs[f'R{R:.0f}']-rd.DELTA_C_REF:+.1e}")
dc2 = rd.umbral(rd.V_yukawa, 0.30, 0.32, R=400.0)
print(f"delta_c(2s) (R=400) = {dc2:.10f}")
res["delta_c"] = dict(yukawa_1s=dcs, referencia_fase1=rd.DELTA_C_REF, yukawa_2s_R400=dc2)

# ----------------------------------------------------------------------------- Hulthen
print("\n=== Hulthen V=-delta/(e^{delta r}-1) ===")
res["hulthen"] = {}
for d in (0.2, 1.0, 1.5):
    ex = rd.hulthen_exacto(d)
    R = rd.caja_recomendada(ex["E"])
    o = rd.resolver_rich(rd.V_hulthen(d), R, H)
    o40 = rd.resolver_rich(rd.V_hulthen(d), 40.0, H)
    print(f"delta={d}: exacto E0={ex['E']:.12f} <r>={ex['r_med']:.12f} <r^2>={ex['r2_med']:.12f} | "
          f"R={R:.0f}: E0={o['E0']:.12f} ({o['E0']-ex['E']:+.1e}) <r>={o['r_med']:.10f} ({o['r_med']-ex['r_med']:+.1e}) "
          f"<r^2>={o['r2_med']:.10f} ({o['r2_med']-ex['r2_med']:+.1e}) | R=40: E0={o40['E0']:.12f} ({o40['E0']-ex['E']:+.1e})")
    ent = dict(exacto={k: ex[k] for k in ("E", "kappa", "r_med", "r2_med", "r_rms", "r_med_formula", "residuo_simbolico")},
               numerico=limpio(o), numerico_R40=limpio(o40))
    if d < 0.5:
        ex2 = rd.hulthen_exacto(d, n=2)
        R2 = rd.caja_recomendada(ex2["E"], entera=True)
        o2 = rd.resolver_rich(rd.V_hulthen(d), R2, H)
        print(f"   2s: exacto E1={ex2['E']:.12f}  R={R2:.0f}: E1={o2['E1']:.12f} ({o2['E1']-ex2['E']:+.1e})")
        ent["exacto_2s"] = dict(E=ex2["E"], kappa=ex2["kappa"])
        ent["numerico_caja_2s"] = limpio(o2)
    res["hulthen"][f"{d}"] = ent
u1 = rd.umbral(rd.V_hulthen, 1.8, 2.2, R=200.0)
u2 = rd.umbral(rd.V_hulthen, 0.4, 0.7, R=200.0)
print(f"umbrales por energia cero (R=200): 1s {u1:.13f} (exacto 2), 2s {u2:.13f} (exacto 0.5)")
res["hulthen"]["umbrales"] = dict(n1=u1, n1_exacto=2.0, n2=u2, n2_exacto=0.5)

# ----------------------------------------------------------------------------- pozo cuadrado
print("\n=== Pozo esferico cuadrado, a=1 ===")
upz = rd.umbral(lambda v: rd.V_pozo(v), 1.0, 1.5, R=50.0, quiebres=(1.0,))
print(f"umbral por energia cero: V0 = {upz:.13f}  (pi^2/8 = {np.pi**2/8:.13f})")
res["pozo"] = dict(umbral=dict(numerico=upz, exacto=np.pi**2 / 8))
HS = [1 / 20, 1 / 40, 1 / 80, 1 / 160, 1 / 320]
conv = {}
for V0 in (2.0, 1.3):
    ex = rd.pozo_exacto(V0)
    R = rd.caja_recomendada(ex["E"], entera=True)
    ent = dict(exacto={k: ex[k] for k in ("E", "k", "kappa", "r_med", "r2_med", "r_rms")}, R=R)
    print(f"V0={V0}: exacto E0={ex['E']:.13f} <r>={ex['r_med']:.10f} <r^2>={ex['r2_med']:.10f}  (R={R:.0f})")
    for b in ("media", "estricta"):
        X, p = rd.orden_aparente(rd.V_pozo(V0, borde=b), R, HS, exacto=ex["E"])
        conv[(V0, b)] = np.abs(np.array(X) - ex["E"])
        pp = 2 if b == "media" else 1
        o = rd.resolver_rich(rd.V_pozo(V0, borde=b), R, H, p=pp)
        o2 = rd.resolver_rich(rd.V_pozo(V0, borde=b), R, H, p=2) if b == "estricta" else o
        print(f"   borde {b:8s}: orden aparente {['%.3f' % x for x in p]};  Richardson p={pp}: E0={o['E0']:.12f} "
              f"({o['E0']-ex['E']:+.1e})  <r>={o['r_med']:.8f} ({o['r_med']-ex['r_med']:+.1e})"
              + (f";  Richardson p=2 (indebido): {o2['E0']-ex['E']:+.1e}" if b == "estricta" else ""))
        ent[b] = dict(E_por_malla=[float(x) for x in X], h=HS, orden_aparente=p, richardson_p=pp, numerico=limpio(o))
        if b == "estricta":
            ent[b]["richardson_p2_indebido"] = limpio(o2)
    res["pozo"][f"V0_{V0}"] = ent

# ----------------------------------------------------------------------------- tabla 9.6
print("\n=== Cajas cerca del umbral (tabla 9.6): E0 Richardson, <r>/R y F_1/2 ===")
res["cajas_9_6"] = {}
for d in (1.15, 1.18, 1.20, 1.25):
    fila = {}
    for R in (50.0, 100.0, 200.0, 400.0, 800.0):
        o = rd.resolver_rich(rd.V_yukawa(d), R, H, nev=1)
        fila[f"R{R:.0f}"] = limpio(o)
        print(f"delta={d:.2f} R={R:4.0f}: E0={o['E0']:+.6e} (h=1/40 {o['E0_h']:+.4e}, 1/80 {o['E0_h2']:+.4e}, "
              f"|dE|/|E0|={o['dE_rel']:.3f})  <r>/R={o['r_sobre_R']:.5f} (1/80: {o['r_sobre_R_h2']:.5f})  "
              f"F_1/2={o['F12']:.5f} (1/80: {o['F12_h2']:.5f})")
    if d < rd.DELTA_C_REF:
        k = 0.7421 * (rd.DELTA_C_REF - d)
        fila["ley_kappa_E0"] = -k * k / 2
        print(f"   ley kappa=0.7421(delta_c-delta): E0={-k*k/2:+.4e}")
    res["cajas_9_6"][f"{d}"] = fila
res["cajas_9_6"]["errata_fase1"] = ("La tabla 9.6 de la Fase 1 da E0(1.18, R=400) = -3.08e-5; el codigo de la Fase 1 y "
                                    "este modulo dan -3.0746e-5, que redondea a -3.07e-5.")

# ----------------------------------------------------------------------------- figura de convergencia
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
hs4 = np.array([1 / 20, 1 / 40, 1 / 80, 1 / 160])
eC = np.abs(np.array(rd.orden_aparente(rd.V_coulomb(), 60.0, list(hs4), exacto=-0.5)[0]) + 0.5)
exH = rd.hulthen_exacto(1.0)
eH = np.abs(np.array(rd.orden_aparente(rd.V_hulthen(1.0), 60.0, list(hs4), exacto=exH["E"])[0]) - exH["E"])
fig, ax = plt.subplots(figsize=(8.6, 4.6))
ax.loglog(hs4, eC, "o-", label="Coulomb $\\delta=0$")
ax.loglog(hs4, eH, "s-", label="Hulthén $\\delta=1$")
ax.loglog(HS, conv[(2.0, "media")], "^-", label="pozo $V_0=2$, $V(a)=-V_0/2$")
ax.loglog(HS, conv[(2.0, "estricta")], "v-", label="pozo $V_0=2$, $V(a)=0$")
ax.loglog(HS, conv[(1.3, "estricta")], "d--", label="pozo $V_0=1.3$, $V(a)=0$")
hh = np.array(HS)
ax.loglog(hh, 0.1 * hh**2, "k:", lw=1, label="pendiente $h^2$")
ax.loglog(hh, 0.7 * hh, "k--", lw=1, label="pendiente $h$")
ax.set_xlabel("paso de malla $h$")
ax.set_ylabel("$|E_0(h)-E_0^{\\rm exacta}|$ (sin Richardson)")
ax.set_title("Convergencia del solucionador radial")
ax.legend(fontsize=8, loc="center left", bbox_to_anchor=(1.02, 0.5))
ax.grid(True, which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT_FIG, dpi=150)

res["meta"]["tiempo_s"] = time.perf_counter() - t0
with open(OUT_JSON, "w") as f:
    json.dump(res, f, indent=1, ensure_ascii=False)
print(f"\nGuardado {OUT_JSON}, {OUT_NPZ}, {OUT_FIG}  ({res['meta']['tiempo_s']:.1f} s)")
