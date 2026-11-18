"""06_figuras.py -- E3: figuras (PNG, dpi 150) a partir de los JSON de 01-05. No calcula nada nuevo."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np               # noqa: E402

import comun_e3 as C             # noqa: E402

COL = {"yukawa": "#2a78d6", "ecsc": "#eb6834", "hulthen": "#1baf7a", "hatomo": "#c98500"}
MK = {"yukawa": "o", "ecsc": "s", "hulthen": "^", "hatomo": "D"}
NOM = {"yukawa": "Yukawa", "ecsc": "ECSC", "hulthen": "Hulthén", "hatomo": "átomo H estático"}
GRIS = "#52514e"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "lines.linewidth": 2})


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(os.path.join(C.FIG, nombre), dpi=150)
    plt.close(fig)
    print("figura", nombre)


def main():
    D2 = C.cargar("02_dispersion")["perfiles"]
    D3 = C.cargar("03_ligados_virtuales")["perfiles"]
    D3b = C.cargar("03b_curvas_E")["perfiles"]
    D4 = C.cargar("04_cajas_universalidad")["perfiles"]
    D5 = C.cargar("05_transferencia_ecsc")["celdas"]

    # ---- figura 1: energias reescaladas
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    for k in C.ORDEN:
        cu = D3b[k]["curva"]
        x = [f["x"] for f in cu]; E = [f["E0"] for f in cu]
        axs[0].plot(x, E, color=COL[k], marker=MK[k], ms=5, label=f"{NOM[k]} ($\\delta_c$ = {D3b[k]['delta_c']:.6f})")
        c = D2[k]["c_HF"]; dc = D2[k]["delta_c"]
        s = np.array([1 - f["x"] for f in cu]); kap = np.array([f["kappa"] for f in cu])
        axs[1].loglog(s, kap / (c * dc), color=COL[k], marker=MK[k], ms=5, label=NOM[k])
    axs[0].axhline(0, color=GRIS, lw=1)
    axs[0].set_xlabel(r"$\delta/\delta_c$"); axs[0].set_ylabel(r"$E_0$ (unidades $\hbar=m=g=1$)")
    axs[0].set_title("(a) Energía del 1s frente a $\\delta/\\delta_c$")
    axs[0].legend(frameon=False, fontsize=8)
    ss = np.geomspace(1e-3, 0.9, 50)
    axs[1].loglog(ss, ss, color=GRIS, ls="--", lw=1, label=r"$\kappa=c\,(\delta_c-\delta)$")
    axs[1].set_xlabel(r"$1-\delta/\delta_c$"); axs[1].set_ylabel(r"$\kappa/(c\,\delta_c)$")
    axs[1].set_title("(b) Colapso con la pendiente $c$ predicha")
    axs[1].legend(frameon=False, fontsize=8)
    guardar(fig, "E3_01_energias_reescaladas.png")

    # ---- figura 2: kappa frente a D con las pendientes predichas
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    for k in C.ORDEN:
        L = D3[k]["ligados"]
        D = np.array([x["D"] for x in L]); kap = np.array([x["kappa"] for x in L])
        c, B = D3[k]["c"], D3[k]["B_pred"]
        axs[0].loglog(D, kap, ls="none", color=COL[k], marker=MK[k], ms=6, label=f"{NOM[k]}: $c$ = {c:.4f}")
        DD = np.geomspace(D.min(), D.max(), 100)
        axs[0].loglog(DD, c * DD, color=COL[k], lw=1.2)
        axs[1].semilogx(D, (kap - c * D) / (c * D), ls="none", color=COL[k], marker=MK[k], ms=6, label=NOM[k])
        axs[1].semilogx(DD, B * DD / c, color=COL[k], lw=1.2)
    axs[0].set_xlabel(r"$\Delta=\delta_c-\delta$"); axs[0].set_ylabel(r"$\kappa=\sqrt{-2E_0}$")
    axs[0].set_title(r"(a) $\kappa$ (puntos) y $c\,\Delta$ predicho con $c=-d(1/a)/d\delta$ (líneas)")
    axs[0].legend(frameon=False, fontsize=8)
    axs[1].axhline(0, color=GRIS, lw=1)
    axs[1].set_xlabel(r"$\Delta=\delta_c-\delta$"); axs[1].set_ylabel(r"$(\kappa-c\Delta)/(c\Delta)$")
    axs[1].set_title(r"(b) Desvío relativo; líneas: $B_{\rm pred}\Delta/c$ (rango efectivo)")
    axs[1].legend(frameon=False, fontsize=8)
    guardar(fig, "E3_02_kappa_pendientes.png")

    # ---- figura 3: 1/a frente a delta, cruzando cero
    fig, axs = plt.subplots(1, 2, figsize=(10, 4))
    for k in C.ORDEN:
        rj = D2[k]["rejilla"]; dc = D2[k]["delta_c"]; c = D2[k]["c_HF"]
        x = np.array([1 + r["rel"] for r in rj]); ia = np.array([r["inv_a"] for r in rj])
        axs[0].plot(x, ia, color=COL[k], marker=MK[k], ms=4, label=NOM[k])
        axs[1].plot(x, ia / (c * dc), color=COL[k], marker=MK[k], ms=4, label=NOM[k])
        re = np.array([r["r_e"] for r in rj])
    xx = np.linspace(0.9, 1.1, 3)
    axs[1].plot(xx, 1 - xx, color=GRIS, ls="--", lw=1, label=r"$1-\delta/\delta_c$")
    for ax in axs:
        ax.axhline(0, color=GRIS, lw=1); ax.axvline(1, color=GRIS, lw=1, ls=":")
        ax.set_xlabel(r"$\delta/\delta_c$"); ax.legend(frameon=False, fontsize=8)
    axs[0].set_ylabel(r"$1/a$"); axs[0].set_title("(a) Inversa de la longitud de dispersión ($a>0$: ligado)")
    axs[1].set_ylabel(r"$(1/a)/(c\,\delta_c)$"); axs[1].set_title("(b) Reescalada con la pendiente $c$")
    guardar(fig, "E3_03_inversa_a.png")

    # ---- figura 4: universalidad y su correccion por r_e
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.2))
    for k in C.ORDEN:
        L = D3[k]["ligados"]; re = D3[k]["r_e_c"]
        kap = np.array([x["kappa"] for x in L if x["s"] <= 0.03]); rk = np.array([x["rk"] for x in L if x["s"] <= 0.03])
        axs[0].plot(kap, rk, ls="none", color=COL[k], marker=MK[k], ms=6, label=f"{NOM[k]} ($r_e$ = {re:+.3f})")
        kk = np.linspace(0, kap.max(), 50)
        axs[0].plot(kk, 0.5 * (1 + re * kk), color=COL[k], lw=1.2)
        F = D4[k]["punto_fijo"]
        R = np.array([f["R"] for f in F]); v = np.array([f["valor"] for f in F])
        axs[1].plot(1 / R, v, color=COL[k], marker=MK[k], ms=6, ls="none", label=NOM[k])
        xx = np.linspace(0, 1 / R.min(), 50)
        axs[1].plot(xx, 0.25 * (1 + re * xx), color=COL[k], lw=1.2)
        cr = D4[k]["cruces"]
        x = np.array([1 / (c_["R1"] * c_["R2"]) for c_ in cr]); y = np.array([c_["dif"] for c_ in cr])
        axs[2].plot(x / x.max(), y / D4[k]["delta_c"], color=COL[k], marker=MK[k], ms=6, ls="none", label=NOM[k])
        axs[2].plot(x / x.max(), re * np.pi**2 / (8 * D4[k]["c"]) * x / D4[k]["delta_c"], color=COL[k], lw=1.2)
    axs[0].axhline(0.5, color=GRIS, lw=1, ls=":")
    axs[0].set_xlabel(r"$\kappa$"); axs[0].set_ylabel(r"$\langle r\rangle\kappa$")
    axs[0].set_title(r"(a) $\langle r\rangle\kappa\to1/2$; líneas: $\frac{1}{2}(1+r_e\kappa)$")
    axs[0].legend(frameon=False, fontsize=8)
    axs[1].axhline(0.25, color=GRIS, lw=1, ls=":")
    axs[1].set_xlabel(r"$1/R$"); axs[1].set_ylabel(r"$2R^2E_0/\pi^2$ en $\delta=\delta_c$")
    axs[1].set_title(r"(b) Punto fijo 1/4; líneas: $\frac{1}{4}(1+r_e/R)$")
    axs[1].legend(frameon=False, fontsize=8)
    axs[2].axhline(0, color=GRIS, lw=1)
    axs[2].set_xlabel(r"$(R_1R_2)^{-1}/(50\cdot100)^{-1}$, pares $R_2=2R_1$")
    axs[2].set_ylabel(r"$(\delta^\ast-\delta_c)/\delta_c$")
    axs[2].set_title(r"(c) Cruces de cajas; líneas: $r_e\pi^2/(8cR_1R_2)$")
    axs[2].legend(frameon=False, fontsize=8)
    guardar(fig, "E3_04_universalidad.png")

    # ---- figura 5: polo virtual
    fig, ax = plt.subplots(figsize=(6, 4))
    for k in C.ORDEN:
        V = D3[k]["virtuales"]
        s = np.array([x["s"] for x in V]); kd = np.array([x["kappa_v_dir"] for x in V]); ke = np.array([x["kappa_v_ERE"] for x in V])
        ax.loglog(s, kd, ls="none", color=COL[k], marker=MK[k], ms=6, label=f"{NOM[k]} (directo)")
        ax.loglog(s, ke, color=COL[k], lw=1.2)
        vc = D4[k]["virtual_caja"]
        ax.loglog([x["s"] for x in vc], [x["kappa_v_caja"] for x in vc], ls="none", marker="x", ms=9, color=GRIS)
    ax.plot([], [], color=GRIS, lw=1.2, label="rango efectivo (líneas)")
    ax.plot([], [], ls="none", marker="x", color=GRIS, label="desde las cajas $R$ = 50..1600")
    ax.set_xlabel(r"$\delta/\delta_c-1$"); ax.set_ylabel(r"$\kappa_v$ (polo $k=-i\kappa_v$)")
    ax.set_title("Estado virtual al otro lado del umbral")
    ax.legend(frameon=False, fontsize=8)
    guardar(fig, "E3_05_virtual.png")

    # ---- figura 6: integral de camino frente al disparo (desvio en unidades de la barra y error relativo)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4))
    for i, c_ in enumerate(D5):
        k = c_["perfil"]
        axs[0].plot(i, c_["dif_disparo"] / c_["err_tr"], color=COL[k], marker=MK[k], ms=8, ls="none")
        axs[1].semilogy(i, abs(c_["dif_disparo"]) / abs(c_["E_disparo"]), color=COL[k], marker=MK[k], ms=8, ls="none")
        axs[1].semilogy(i, c_["err_tr"] / abs(c_["E_disparo"]), color=COL[k], marker="_", ms=16, mew=2, ls="none")
    axs[0].axhspan(-2, 2, color="#cccccc", alpha=0.4, lw=0)
    axs[0].axhline(0, color=GRIS, lw=1)
    axs[0].set_ylabel(r"$(E_{\rm tr}-E_{\rm disparo})/\sigma_{\rm tr}$")
    axs[0].set_title("(a) Desvío en unidades de la barra (banda: criterio $\\pm2$)")
    axs[1].set_ylabel("relativo a $|E_{\\rm disparo}|$")
    axs[1].set_title("(b) $|E_{\\rm tr}-E_{\\rm disparo}|$ (puntos) y barra $\\sigma_{\\rm tr}$ (rayas)")
    for ax in axs:
        ax.set_xticks(range(len(D5)))
        ax.set_xticklabels([f"{NOM[c_['perfil']].split()[0]}\n$\\delta$={c_['delta']}\nR={c_['R']:.0f}" for c_ in D5], fontsize=7)
    guardar(fig, "E3_06_transferencia.png")


if __name__ == "__main__":
    main()
