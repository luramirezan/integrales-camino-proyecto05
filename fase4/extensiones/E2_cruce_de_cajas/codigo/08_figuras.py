"""08_figuras.py -- figuras A a D de E2 (PNG, dpi 150, ejes en espanol, barras de error donde existen).
A: y = 2R^2E0/pi^2 frente a delta (transferencia con barras, radial 1/160 en linea), linea 1/4.
B: delta*(R, 2R) frente a 1/R^2: transferencia (A y B), radial, disparo, modelo ERE, ajuste y banda.
C: <r>/R frente a delta, linea 1/2 - 2/pi^2.
D: colapso de datos y frente a z = R/a_s con F(z), y residuo R (y - F) que tiende a r_e/4 en z = 0.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import e2comun as c

X = c.cargar("05_cruces"); D = c.cargar("02_disparo"); RA = c.cargar("03_radial"); T = c.cargar("01_teoria")
Rt = X["R_transferencia"]
TR = {R: c.cargar(f"04_transferencia_R{R}")["celdas"] for R in Rt}
DEL = np.array(c.DELTAS)
RAMPA = ["#86b6ef", "#5598e7", "#3987e5", "#2a78d6", "#1c5cab", "#184f95", "#0d366b"]   # azul ordinal (dataviz)
COL = {"transferencia": "#2a78d6", "B": "#6250d6", "radial_h160": "#eb6834", "disparo": "#1baf7a", "ERE": "#52514e"}
TXT2 = "#52514e"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#e4e3df", "grid.linewidth": 0.6, "axes.edgecolor": "#8a8984",
                     "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "lines.linewidth": 1.6})
REF = c.DELTA_C_REF


def guardar(fig, nombre):
    fig.savefig(os.path.join(c.FIG, nombre), dpi=150, bbox_inches="tight")
    plt.close(fig)


def curvas(ax, clave_tr, clave_rad, err_tr, err_rad, fijo, etiqueta_fijo, zoom=None):
    for k, R in enumerate(c.RS):
        col = RAMPA[k]
        yr = [RA["celdas"]["h160"][f"{d:g}"][f"R{R}"][clave_rad] for d in DEL]
        ax.plot(DEL, yr, "-", color=col, lw=1.0, alpha=0.9)
        if R in TR:
            yt = [clave_tr(TR[R][f"{d:g}"], R) for d in DEL]
            et = [err_tr(TR[R][f"{d:g}"], R) for d in DEL]
            ax.errorbar(DEL, yt, yerr=et, fmt="o", ms=3.2, color=col, mfc=col, mec="#fcfcfb", mew=0.6, elinewidth=1.0,
                        capsize=1.5, label=f"R = {R}")
    ax.axhline(fijo, color=TXT2, lw=1.0, ls="--")
    ax.axvline(REF, color=TXT2, lw=0.8, ls=":")
    ax.text(0.01, fijo, etiqueta_fijo, va="bottom", ha="left", color=TXT2, fontsize=8, transform=ax.get_yaxis_transform())


# ------------------------------------------------------------------ A
fig, (ax, az) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw=dict(width_ratios=[1.4, 1]))
for a_ in (ax, az):
    curvas(a_, lambda x, R: c.y_de(x["E_mejor"], R), "y", lambda x, R: c.y_de(x["err"], R), "err_y", 0.25, "1/4")
ax.set_ylim(-1.6, 1.0); ax.set_xlabel("apantallamiento δ"); ax.set_ylabel("2R²E₀/π²")
ax.set_title("Integral de camino (puntos, con barras) y radial h = 1/160 (líneas)", fontsize=9, loc="left")
ax.legend(fontsize=7.5, ncol=2, frameon=False, loc="lower right")
az.set_xlim(1.1903, 1.1912); az.set_ylim(0.235, 0.275); az.set_xlabel("apantallamiento δ")
az.set_title("Ampliación cerca de δ_c (línea punteada: referencia)", fontsize=9, loc="left")
guardar(fig, "A_y_vs_delta.png")

# ------------------------------------------------------------------ C
fig, (ax, az) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw=dict(width_ratios=[1.4, 1]))
for a_ in (ax, az):
    curvas(a_, lambda x, R: x["obs"]["r_sobre_R"]["mejor"], "r_sobre_R", lambda x, R: x["obs"]["r_sobre_R"]["err"], "err_r",
           c.RHO_FIJO, "1/2 − 2/π² = 0.2974")
ax.set_ylim(0.0, 0.5); ax.set_xlabel("apantallamiento δ"); ax.set_ylabel("⟨r⟩/R")
ax.set_title("Extensión: integral de camino (puntos) y radial h = 1/160 (líneas)", fontsize=9, loc="left")
ax.legend(fontsize=7.5, ncol=2, frameon=False, loc="lower right")
az.set_xlim(1.1903, 1.1950); az.set_ylim(0.28, 0.33); az.set_xlabel("apantallamiento δ")
az.set_title("Ampliación cerca de δ_c", fontsize=9, loc="left")
guardar(fig, "C_rho_vs_delta.png")

# ------------------------------------------------------------------ B
fig, axs = plt.subplots(2, 2, figsize=(10, 7.6))
MARC = (("disparo", "disparo sin malla", "s"), ("radial_h160", "radial h = 1/160", "^"),
        ("transferencia", "integral de camino, método A", "o"), ("B", "integral de camino, método B", "D"))


def serie(fu, obs):
    pr = X["transferencia_metodo_B"][obs]["pares"] if fu == "B" else X["fuentes"][fu][obs]["pares"]
    return (np.array([f["R"] for f in pr]), np.array([f["delta"] for f in pr]), np.array([f["sigma"] for f in pr]))


for fila_, (obs, tit) in enumerate((("y", "cruce de 2R²E₀/π²"), ("rho", "cruce de ⟨r⟩/R"))):
    al, az = axs[fila_]
    ere = T["modelo_ERE"]
    Re = np.array([f["R"] for f in ere]); de = np.array([f["delta_y" if obs == "y" else "delta_rho"] for f in ere])
    al.plot(1e4 / Re**2, de - REF, "-", color=COL["ERE"], lw=1.0, label="teoría: modelo de rango efectivo")
    for k, (fu, lab, mk) in enumerate(MARC):
        R, d, s = serie(fu, obs)
        f = 1 + 0.03 * (k - 1.5)
        al.errorbar(1e4 / R**2 * f, d - REF, yerr=s, fmt=mk, ms=4, color=COL[fu], mec="#fcfcfb", mew=0.6, capsize=2,
                    elinewidth=1.0, label=lab)
        az.errorbar(1e4 / R**2 * f, (d - REF) * 1e6, yerr=s * 1e6, fmt=mk, ms=4, color=COL[fu], mec="#fcfcfb", mew=0.6,
                    capsize=2, elinewidth=1.0)
    al.set_xscale("log"); al.set_yscale("log"); al.set_ylim(1e-9, 1e-2)
    al.set_xlabel("10⁴ / R²  (R = caja menor del par)"); al.set_ylabel("δ*(R, 2R) − δ_c,ref")
    al.set_title(tit + ": ley 1/R² (pendiente 1)", fontsize=9, loc="left")
    # zoom lineal con extrapolaciones
    xx = np.linspace(0, 1e4 / 200**2, 100)
    az.plot(xx, (de[0] * 0 + 0) * xx, alpha=0)
    for fu, src in (("transferencia", X["fuentes"]["transferencia"]), ("B", X["transferencia_metodo_B"]),
                    ("radial_h160", X["fuentes"]["radial_h160"])):
        e = src[obs]["extrapolacion"]; a = e["ajuste_ab"]
        Rx = 1e4 / np.sqrt(np.maximum(xx, 1e-12)) * 0 + np.sqrt(1e4 / np.maximum(xx, 1e-12))
        yfit = a["delta_c"] + a["alpha"] / Rx**2 + a["beta"] / Rx**3
        az.plot(xx, (yfit - REF) * 1e6, "--", color=COL[fu], lw=1.0)
        az.fill_between([-0.004, 0.004], (e["intervalo"][0] - REF) * 1e6, (e["intervalo"][1] - REF) * 1e6,
                        color=COL[fu], alpha=0.25, lw=0)
    az.plot(1e4 / Re**2, (de - REF) * 1e6, "-", color=COL["ERE"], lw=1.0)
    az.axhline(0, color=TXT2, lw=0.8, ls=":")
    az.set_xlim(-0.006, 1e4 / 200**2 * 1.15); az.set_ylim(-70, 90)
    az.set_xlabel("10⁴ / R²"); az.set_ylabel("10⁶ (δ* − δ_c,ref)")
    az.set_title("ampliación: ajustes α/R² + β/R³ y bandas finales en R infinito", fontsize=9, loc="left")
axs[0][0].legend(fontsize=7, frameon=False, loc="upper left")
fig.tight_layout()
guardar(fig, "B_cruces_vs_R.png")

# ------------------------------------------------------------------ D
fig, (ax, ar) = plt.subplots(1, 2, figsize=(10, 4.2))
zz = np.linspace(-8, 4, 600)
Fz = np.array([c.F_escala(z) for z in zz])
ax.plot(zz, Fz, "-", color=COL["ERE"], lw=1.2, label="F(z), alcance cero: x cot x = z")
for k, R in enumerate(c.RS):
    z, y, rres = [], [], []
    for dk, fila in D["celdas"].items():
        x = fila[f"R{R}"]
        if x["nodos"] != 0:
            continue
        a = D["energia_cero"][dk]["a"]
        if not -8 <= R / a <= 4:
            continue
        z.append(R / a); y.append(x["y"]); rres.append(R * (x["y"] - x["y_alcance_cero"]))
    o = np.argsort(z)
    ax.plot(np.array(z)[o], np.array(y)[o], "o", ms=3.2, color=RAMPA[k], mec="#fcfcfb", mew=0.5, label=f"R = {R}")
    ar.plot(np.array(z)[o], np.array(rres)[o], "o-", ms=3, lw=0.8, color=RAMPA[k], mec="#fcfcfb", mew=0.5, label=f"R = {R}")
ax.axhline(0.25, color=TXT2, lw=0.8, ls="--"); ax.axvline(0, color=TXT2, lw=0.8, ls=":")
ax.set_xlabel("z = R / a_s(δ)   (a_s a energía cero)"); ax.set_ylabel("2R²E₀/π²"); ax.set_ylim(-2.0, 1.05)
ax.set_title(f"Colapso de datos: disparo, {len(D['deltas'])} valores de δ y {len(c.RS)} cajas", fontsize=9, loc="left")
ax.legend(fontsize=7, frameon=False, loc="lower left", ncol=2)
ar.axhline(T["constantes"]["r_e"] / 4, color=TXT2, lw=0.8, ls="--")
ar.text(-7.8, T["constantes"]["r_e"] / 4, "r_e/4 (teoría, z = 0)", va="bottom", fontsize=8, color=TXT2)
ar.set_xlabel("z = R / a_s(δ)"); ar.set_ylabel("R · [2R²E₀/π² − F(z)]")
ar.set_title("Residuo del colapso: corrección de rango efectivo ∝ 1/R", fontsize=9, loc="left")
ar.set_ylim(-1.5, 1.0)
guardar(fig, "D_colapso.png")
print("figuras escritas en", c.FIG)
