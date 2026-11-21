"""46_figuras.py -- E4, tarea 5: figuras a partir de los JSON 41, 42, 43 y 45 (no calcula nada nuevo).
Salidas en figuras/: 46_extension_vs_kappa.png, 46_energia_umbral.png, 46_log_onda_p.png, 46_cajas_l.png,
46_integral_camino_l1.png. Paleta categorica fija (1s azul, 2s naranja, 2p aguamarina, 3d amarillo) con marcador
distinto por estado como segunda codificacion. En los barridos sin caja (disparo) las barras de error son menores que
los marcadores (error relativo < 1e-6, verificacion.md); en la integral de camino se dibujan las barras."""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

import comun4 as c  # noqa: E402

COL = {"1s": "#2a78d6", "2s": "#eb6834", "2p": "#1baf7a", "3d": "#eda100"}
MK = {"1s": "o", "2s": "s", "2p": "^", "3d": "D"}
ETQ = {"1s": "1s (l = 0)", "2s": "2s (l = 0)", "2p": "2p (l = 1)", "3d": "3d (l = 2)"}
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.25, "axes.spines.top": False,
                     "axes.spines.right": False})
B = c.leer_json("42_barridos")["estados"]
K = c.leer_json("41_constantes_umbral")["constantes"]
U = c.leer_json("41_constantes_umbral")["universales"]
CJ = c.leer_json("43_cajas_l")
TR = c.leer_json("45_transferencia_l1")


def arr(nom, k):
    return np.array([p[k] for p in B[nom]["puntos"]])


def guardar(fig, n):
    fig.tight_layout()
    fig.savefig(os.path.join(c.FIG, n), dpi=150)
    plt.close(fig)


# ------------------------------------------------------------------ 1. <r> y <r^2> frente a kappa
fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
for nom in ("1s", "2s", "2p", "3d"):
    kap, r1, r2 = arr(nom, "kappa"), arr(nom, "r_med"), arr(nom, "r2_med")
    for a, y in ((ax[0], r1), (ax[1], r2)):
        a.loglog(kap, y, MK[nom], color=COL[nom], ms=5, mfc="none", label=ETQ[nom] + " (disparo)")
kk = np.logspace(-7.2, -0.8, 50)
ax[0].loglog(kk, 0.5 / kk, "-", color="0.35", lw=1, label="l = 0: 1/(2κ)")
k2p = np.logspace(-5, -0.8, 50)
ax[0].loglog(k2p, K["2p"]["C0"] + K["2p"]["An2"] * (np.log(1 / k2p) + U["K_1_exacto"]), "--", color="0.35", lw=1,
             label="l = 1: A²[ln(1/κ) + 5/4 − γ − ln 2] + C₀")
ax[0].axhline(K["3d"]["r_med0"], ls=":", color="0.35", lw=1, label="l = 2: ⟨r⟩₀ (energía cero)")
ax[1].loglog(kk, 0.5 / kk**2, "-", color="0.35", lw=1, label="l = 0: 1/(2κ²)")
ax[1].loglog(k2p, 1.25 * K["2p"]["An2"] / k2p, "--", color="0.35", lw=1, label="l = 1: 5A²/(4κ)")
ax[1].axhline(K["3d"]["r2_med0"], ls=":", color="0.35", lw=1, label="l = 2: ⟨r²⟩₀")
ax[0].set_xlabel("κ = (−2E)^½  (mg/ħ)"); ax[0].set_ylabel("⟨r⟩  (ħ²/mg)")
ax[1].set_xlabel("κ = (−2E)^½  (mg/ħ)"); ax[1].set_ylabel("⟨r²⟩  ((ħ²/mg)²)")
ax[0].set_title("(a) Radio medio cerca de cada umbral"); ax[1].set_title("(b) Radio cuadrático medio")
ax[0].legend(fontsize=7.5); ax[1].legend(fontsize=7.5)
guardar(fig, "46_extension_vs_kappa.png")

# ------------------------------------------------------------------ 2. energia frente a Delta y exponentes locales
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
for nom in ("1s", "2s", "2p", "3d"):
    D, E = arr(nom, "Delta"), arr(nom, "E")
    ax[0].loglog(D, -E, MK[nom], color=COL[nom], ms=5, mfc="none", label=ETQ[nom])
    if nom in ("1s", "2s"):
        c0 = K[nom]["pred"]["c0"]
        ax[0].loglog(D, 0.5 * (c0 * D)**2, "-", color=COL[nom], lw=0.8)
    else:
        ax[0].loglog(D, K[nom]["S"] * D, "--", color=COL[nom], lw=0.8)
    loc = np.array(B[nom]["exponentes_locales"]["E"])
    Dm = np.sqrt(D[1:] * D[:-1])
    ax[1].semilogx(Dm, loc, MK[nom] + "-", color=COL[nom], ms=4, mfc="none", lw=0.8, label=ETQ[nom])
ax[0].set_xlabel("Δ = δ_c − δ"); ax[0].set_ylabel("|E|  (mg²/ħ²)")
ax[0].set_title("(a) |E| frente a Δ: líneas = predicción sin ajuste\n(l = 0: (c₀Δ)²/2; l ≥ 1: SΔ, Hellmann–Feynman)",
                fontsize=9.5)
ax[1].axhline(2, color="0.35", lw=0.8, ls=":"); ax[1].axhline(1, color="0.35", lw=0.8, ls=":")
ax[1].set_xlabel("Δ = δ_c − δ"); ax[1].set_ylabel("d ln|E| / d ln Δ")
ax[1].set_title("(b) Exponente local de la energía (predicho: 2 para l = 0, 1 para l ≥ 1)", fontsize=9.5)
ax[0].legend(fontsize=8); ax[1].legend(fontsize=8)
guardar(fig, "46_energia_umbral.png")

# ------------------------------------------------------------------ 3. el logaritmo de la onda p
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
kap, r1 = arr("2p", "kappa"), arr("2p", "r_med")
lg = B["2p"]["log"]
x = np.log(1 / kap)
ax[0].plot(x, r1, "^", color=COL["2p"], ms=6, mfc="none", label="2p, disparo sin caja")
ax[0].plot(x, lg["r_formula_lider"], "-", color="0.35", lw=1, label="término líder A²ln(1/κ) + cte (sin ajuste)")
ax[0].plot(x, lg["r_formula_refinada"], ":", color="k", lw=1.2, label="con la corrección de norma (1 + 3A²κ/2)")
ax[0].set_xlabel("ln(1/κ)"); ax[0].set_ylabel("⟨r⟩  (ħ²/mg)")
ax[0].set_title(f"(a) 2p: ⟨r⟩ es lineal en ln(1/κ); pendiente medida {lg['pendiente']:.4f}, A² = {lg['An2']:.4f}",
                fontsize=9.5)
ax[0].legend(fontsize=8)
for nom in ("1s", "2p", "3d"):
    kp = arr(nom, "kappa")
    loc = np.array(B[nom]["exponentes_locales"]["r_med"])
    ax[1].semilogx(np.sqrt(kp[1:] * kp[:-1]), loc, MK[nom] + "-", color=COL[nom], ms=4, mfc="none", lw=0.8,
                   label=ETQ[nom])
km = np.sqrt(kap[1:] * kap[:-1])
ax[1].semilogx(kap, np.array(lg["exponente_local_pred"]), "--", color="0.35", lw=1, label="l = 1: A²/⟨r⟩ (predicción)")
ax[1].axhline(1, color="0.35", lw=0.8, ls=":"); ax[1].axhline(0, color="0.35", lw=0.8, ls=":")
ax[1].invert_xaxis()
ax[1].set_xlabel("κ (hacia el umbral, a la derecha)"); ax[1].set_ylabel("d ln⟨r⟩ / d ln(1/κ)")
ax[1].set_title("(b) Exponente local de ⟨r⟩: constante 1 (l = 0), cae a 0 como 1/ln(1/κ) (l = 1),\n0 (l = 2)",
                fontsize=9.5)
ax[1].legend(fontsize=8)
guardar(fig, "46_log_onda_p.png")

# ------------------------------------------------------------------ 4. cajas
fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
A = CJ["a_umbral"]
R1 = [f["R"] for f in A["1s"]["filas"]]
ax[0].semilogx(R1, [f["y"] for f in A["1s"]["filas"]], "o-", color=COL["1s"], mfc="none", lw=0.8,
               label="1s: y = 2R²E/π² (tiende a 1/4)")
for nom in ("2p", "3d"):
    ax[0].semilogx([f["R"] for f in A[nom]["filas"]], [f["Y"] for f in A[nom]["filas"]], MK[nom] + "-", color=COL[nom],
                   mfc="none", lw=0.8, label=f"{nom}: Y = 2R^(2l+1)E/((2l+1)A²) (tiende a 1)")
    ax[0].semilogx([f["R"] for f in A[nom]["filas"]], [f["y"] for f in A[nom]["filas"]], MK[nom] + ":", color=COL[nom],
                   ms=3, lw=0.6, label=f"{nom}: y = 2R²E/π² (tiende a 0)")
ax[0].axhline(0.25, color="0.35", ls=":", lw=0.8); ax[0].axhline(1, color="0.35", ls=":", lw=0.8)
ax[0].set_ylim(-0.05, 2.4)
ax[0].set_xlabel("R  (ħ²/mg)"); ax[0].set_ylabel("energía de la caja escalada")
ax[0].set_title("(a) Caja de Dirichlet justo en δ_c", fontsize=9.5); ax[0].legend(fontsize=7)
for nom in ("1s", "2p", "3d"):
    F = CJ["b_radio_cruce"][nom]["filas"]
    Dr = [f["Delta_rel"] for f in F]
    ax[1].loglog(Dr, [f["R_c"] for f in F], MK[nom], color=COL[nom], mfc="none", ms=6, label=ETQ[nom] + " (medido)")
    ax[1].loglog(Dr, [f["R_c_pred"] for f in F], "-", color=COL[nom], lw=0.8)
ax[1].set_xlabel("Δ/δ_c"); ax[1].set_ylabel("R_c  (caja mínima con E < 0)")
ax[1].set_title("(b) Radio de caja en que el nivel cruza E = 0\n(líneas: R_c ∝ Δ^(−1), Δ^(−1/3), Δ^(−1/5))", fontsize=9.5)
ax[1].legend(fontsize=8)
for nom in ("2p", "3d"):
    F = CJ["c_cruces"][nom]["filas"]
    Rr = [f["R"] for f in F]
    ax[2].loglog(Rr, [f["y_estrella"] for f in F], MK[nom], color=COL[nom], mfc="none", ms=6, label=f"{nom}: y* medido")
    ax[2].loglog(Rr, [f["y_pred"] for f in F], "-", color=COL[nom], lw=0.8, label=f"{nom}: predicción asintótica")
ax[2].set_xlabel("R (cruce de las cajas R y 2R)"); ax[2].set_ylabel("y* = 2R²E/π² en el cruce")
ax[2].set_title("(c) El cruce de y no tiende a 1/4 sino a 0 (l ≥ 1)", fontsize=9.5); ax[2].legend(fontsize=8)
guardar(fig, "46_cajas_l.png")

# ------------------------------------------------------------------ 5. integral de camino l = 1
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
cols = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#6250d6"]
mks = ["o", "s", "^", "D", "v", "P"]
for i, cs in enumerate(TR["casos"]):
    ref = cs["radial"]["E0"]
    eps = np.array([0.2, 0.1, 0.05])
    for j, (met, ls) in enumerate((("a", "-"), ("b", "--"))):
        m = cs["metodos"][met]
        if met == "a":
            sp = np.array([m["sesgo_sin_pared"][f"{e:g}"] for e in eps])
            y = np.abs(sp) / abs(ref)
        else:
            y = np.abs(np.array([m["E_hRich"][f"{e:g}"] for e in eps]) - ref) / abs(ref)
        ax[0].loglog(eps, y, mks[i] + ls, color=cols[i], mfc="none", lw=0.8,
                     label=(f"δ = {cs['delta']:g}" if met == "a" else None))
ax[0].loglog([0.05, 0.2], [2e-9, 2e-9 * 16], "k-", lw=0.6); ax[0].text(0.09, 2.2e-9, "ε²", fontsize=9)
ax[0].loglog([0.05, 0.2], [3e-3, 3e-3 * 4**(4 / 3)], "k--", lw=0.6); ax[0].text(0.09, 4e-3, "ε^(4/3)", fontsize=9)
ax[0].set_xlabel("ε  (paso de tiempo imaginario)"); ax[0].set_ylabel("|E(ε) − E_radial| / |E|")
ax[0].set_title("(a) Sesgo de Trotter: (a) pares exactos en l = 1 (continua)\nfrente a (b) centrífugo primitivo (discontinua)",
                fontsize=9.5)
ax[0].legend(fontsize=7.5)
d = np.array([cs["delta"] for cs in TR["casos"]])
Ea = np.array([cs["metodos"]["a"]["E_mejor"] for cs in TR["casos"]])
ea = np.array([cs["metodos"]["a"]["err"] for cs in TR["casos"]])
Er = np.array([cs["radial"]["E0"] for cs in TR["casos"]])
Eb = np.array([cs["metodos"]["b"]["E_mejor"] for cs in TR["casos"]])
ax[1].errorbar(d, (Ea - Er) / np.abs(Er), yerr=ea / np.abs(Er), fmt="o", color=cols[0], mfc="none", capsize=3,
               label="(a) extrapolada, con barra de error")
ax[1].plot(d, (Eb - Er) / np.abs(Er), "s", color=cols[1], mfc="none", label="(b) extrapolada con su orden medido")
ax[1].axhline(0, color="0.35", lw=0.8)
ax[1].set_yscale("symlog", linthresh=1e-9)
ax[1].set_xlabel("δ  (δ = 0: Coulomb 2p, R = 60; resto R = 100)"); ax[1].set_ylabel("(E_camino − E_radial)/|E_radial|")
ax[1].set_title("(b) Integral de camino frente al radial en la misma caja", fontsize=9.5)
ax[1].legend(fontsize=8)
guardar(fig, "46_integral_camino_l1.png")
print("figuras escritas en", c.FIG)
