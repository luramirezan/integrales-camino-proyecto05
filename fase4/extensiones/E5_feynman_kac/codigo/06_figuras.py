"""06_figuras.py -- E5: figuras (PNG, dpi 150) a partir de los JSON de 01 a 05. No calcula nada nuevo salvo curvas de la EDO.
Paleta categorica fija (azul, naranja, aguamarina, amarillo) en ese orden; ejes y leyendas en espanol."""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import fk_comun as fk  # noqa: E402

RES = os.path.join(AQUI, "../resultados")
FIG = os.path.join(AQUI, "../figuras")
J = {k: json.load(open(os.path.join(RES, f"{k}.json"))) for k in
     ["01_referencia_edo", "02_validacion_mc", "03_colas", "04_importancia", "04b_extrapolacion", "05_cerca_umbral"]}
X4 = J["04b_extrapolacion"]["delta"]          # extrapolacion eta -> 0 con p = 2 (revisada, ver 04b)
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
TXT = "#3b3b3b"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": "#8a8a8a", "axes.labelcolor": TXT, "xtick.color": TXT,
                     "ytick.color": TXT, "axes.grid": True, "grid.color": "#e4e4e4", "grid.linewidth": 0.6,
                     "lines.linewidth": 2, "legend.frameon": False})
DC = fk.DELTA_C


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, nombre), dpi=150)
    plt.close(fig)
    print("figura", nombre)


# ------------------------------------------------------------------ F1: phi(r) MC frente a EDO (delta = 3, 4)
R1, R2 = J["01_referencia_edo"], J["02_validacion_mc"]
fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.8))
for i, d in enumerate(["3", "4"]):
    p = R1["perfil"][d]
    ax[0].plot(p["denso_r"], p["denso_phi"], color=C[i], label=f"EDO, δ = {d}")
    f = R2["perfil"][d]
    ax[0].errorbar([x["r"] for x in f], [x["phi_mc"] for x in f], yerr=[x["err"] for x in f], fmt="o", ms=5,
                   color=C[i], mfc="white", capsize=2, label=f"Monte Carlo, δ = {d} (η = 0.2)")
    ax[1].errorbar(np.array([x["r"] for x in f]) * (1.04 if i else 0.96), [x["dev_sigmas"] for x in f], yerr=1,
                   fmt="o", ms=5, color=C[i], capsize=2, label=f"δ = {d}")
ax[0].set_xscale("log"); ax[0].set_xlabel("r (unidades ħ²/mg)"); ax[0].set_ylabel("φ(r) = E_r[e^Λ]")
ax[0].legend(fontsize=8)
ax[1].axhspan(-2, 2, color="#f0f0f0", zorder=0); ax[1].axhline(0, color="#8a8a8a", lw=1)
ax[1].set_xscale("log"); ax[1].set_xlabel("r"); ax[1].set_ylabel("(MC − EDO)/σ"); ax[1].legend(fontsize=8)
ax[0].set_title("Solución de energía cero: caminos brownianos frente a la EDO", fontsize=10)
ax[1].set_title("Residuos normalizados (barra = 1σ)", fontsize=10)
guardar(fig, "e5_01_phi_r.png")

# ------------------------------------------------------------------ F2: |a(delta)|: EDO, MC libre, MC con importancia
fig, ax = plt.subplots(figsize=(7.5, 4.6))
cur = R1["curva_a"]
ax.plot(cur["delta"], -np.array(cur["a"]), color="#3b3b3b", lw=1.5, label="EDO (disparo y fase variable)")
ax.axvspan(DC, 2 * DC, color="#fbe3d6", zorder=0, label="δ_c < δ ≤ 2δ_c: varianza infinita del MC libre")
ax.axvline(DC, color="#8a8a8a", lw=1, ls="--")
c2 = np.array(J["02_validacion_mc"]["curva_a_mc_eta02"])
sel = c2[:, 0] > 2 * DC
ax.errorbar(c2[sel, 0], -c2[sel, 1], yerr=c2[sel, 2], fmt="o", ms=4, color=C[0], label="MC libre (η = 0.2, N = 10⁷)")
c3 = np.array(J["02_validacion_mc"]["curva_a_mc_eta02_varianza_infinita"])
ax.plot(c3[:, 0], -c3[:, 1], "o", ms=4, mfc="white", color=C[0], label="MC libre, sin barra (varianza infinita)")
P4 = J["04_importancia"]["produccion"]
xs = [float(k) for k in P4]
ax.errorbar(xs, [-X4[k]["p2"]["a_extrap"] for k in P4], yerr=[X4[k]["p2"]["err"] for k in P4], fmt="s", ms=5,
            color=C[1], label="Importancia, extrapolado η → 0 (p = 2)")
P5 = J["05_cerca_umbral"]["cerca"]
ax.errorbar([float(k) for k in P5], [-P5[k]["a_mc"] for k in P5], yerr=[P5[k]["sigma_total"] for k in P5], fmt="D",
            ms=5, color=C[2], label="Importancia cerca del umbral (η = 0.2, error + sesgo)")
ax.plot([float(k) for k in P5], [-P5[k]["a_edo"] for k in P5], "_", color="#3b3b3b", ms=12, mew=2,
        label="EDO en los δ cercanos al umbral")
ax.set_yscale("log"); ax.set_xscale("log")
ax.set_xlabel("δ = μħ²/(mg)"); ax.set_ylabel("−a (longitud de dispersión, sin ligado)")
ax.set_xticks([1.2, 1.5, 2, 3, 4]); ax.set_xticklabels(["1.2", "1.5", "2", "3", "4"])
ax.legend(fontsize=7.5, loc="upper right")
ax.set_title("Longitud de dispersión a energía cero, sin caja", fontsize=10)
guardar(fig, "e5_02_a_delta.png")

# ------------------------------------------------------------------ F3: histogramas de W
R3 = J["03_colas"]
fig, ax = plt.subplots(figsize=(7.2, 4.6))
for i, d in enumerate(["1.5", "2", "3", "4"]):
    h = R3["histogramas"][d]
    w = np.array(h["w"]); dens = np.array(h["dens"]); cnt = np.array(h["cuentas"])
    ok = cnt >= 5
    ax.errorbar(w[ok], dens[ok], yerr=dens[ok] / np.sqrt(cnt[ok]), fmt="o", ms=3.5, color=C[i], mfc="white",
                label=f"δ = {d}: MC (θ = {float(d)/DC:.2f})")
    ax.plot(w, h["pred"], color=C[i], lw=1.4)
ax.plot([], [], color="#3b3b3b", lw=1.4, label="ley exacta Σ w̄_k p_k w^(−p_k−1)")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("peso W = exp(∫ q(B_t) dt)"); ax.set_ylabel("densidad de probabilidad")
ax.legend(fontsize=8); ax.set_title("Colas de potencias del peso: densidad ∝ w^(−θ−1), θ = δ/δ_c", fontsize=10)
guardar(fig, "e5_03_histogramas_W.png")

# ------------------------------------------------------------------ F4: theta medido frente a delta/delta_c
fig, ax = plt.subplots(figsize=(6.4, 4.2))
dd = np.linspace(1.15, 4.2, 50)
ax.plot(dd, dd / DC, color="#3b3b3b", lw=1.5, label="θ = δ/δ_c (Teorema 1)")
T = R3["theta"]
ax.errorbar([float(k) for k in T], [T[k]["theta_MC"] for k in T], yerr=[T[k]["err"] for k in T], fmt="o", color=C[0],
            ms=5, label="MC, partida Γ (una muestra para todos los δ)")
pf = R3["partida_fija"]
ax.errorbar([pf["delta"] + 0.04], [pf["theta_MC"]], yerr=[pf["err"]], fmt="s", color=C[1], ms=5,
            label="MC, partida fija r₀ = 1 (independiente)")
ax.axhline(2, color=C[3], lw=1, ls="--"); ax.text(3.2, 2.06, "θ = 2: varianza finita encima", fontsize=8, color=TXT)
ax.axhline(1, color="#8a8a8a", lw=1, ls=":"); ax.text(3.2, 1.06, "θ = 1: media finita encima", fontsize=8, color=TXT)
ax.set_xlabel("δ"); ax.set_ylabel("exponente de la cola θ")
ax.legend(fontsize=8, loc="upper left"); ax.set_title("Exponente de la cola: medido frente a predicho", fontsize=10)
guardar(fig, "e5_04_theta.png")

# ------------------------------------------------------------------ F5: varianza muestral y media acumulada frente a n
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
S = R3["series"]
for i, d in enumerate(["1.5", "2", "3", "4"]):
    s = S[d]
    n = np.array(s["n"]); v = np.array(s["var_mediana"])
    ax[0].plot(n, v / v[0], color=C[i], label=f"δ = {d}: pendiente {s['pend_var']:+.2f} (asint. {s['pred_pend_var']:+.2f})")
    ax[0].fill_between(n, np.array(s["var_p10"]) / v[0], np.array(s["var_p90"]) / v[0], color=C[i], alpha=0.12, lw=0)
    na = np.array(s["n_acum"]); ma = np.array(s["media_acum"])
    ax[1].plot(na, ma / s["phi_media_exacta"], color=C[i], lw=1.5, label=f"δ = {d}")
ax[0].set_xscale("log"); ax[0].set_yscale("log"); ax[0].set_xlabel("n (caminos)")
ax[0].set_ylabel("varianza muestral / valor en n = 100")
ax[0].set_title("Varianza muestral (mediana y p10–p90 de 20 réplicas)", fontsize=10); ax[0].legend(fontsize=7.5)
ax[1].axhline(1, color="#8a8a8a", lw=1); ax[1].set_xscale("log"); ax[1].set_xlabel("n (caminos)")
ax[1].set_ylabel("media acumulada / E[W] exacto"); ax[1].set_ylim(0.6, 1.5)
# el pico de delta = 1.5 queda fuera del eje: se anota con su valor (auditoria Gemini E5, hallazgo E5-C1)
_s = S["1.5"]; _m = np.array(_s["media_acum"]) / _s["phi_media_exacta"]; _i = int(np.argmax(_m))
ax[1].annotate(f"δ = 1.5: pico {_m[_i]:.2f} en n = {_s['n_acum'][_i]:.2g} (fuera de escala)", xy=(_s["n_acum"][_i], 1.5),
               xytext=(12, 1.42), fontsize=7.5, color=TXT, arrowprops=dict(arrowstyle="->", color="#8a8a8a", lw=0.8))
ax[1].set_title("Media acumulada de W (una muestra de 10⁷)", fontsize=10); ax[1].legend(fontsize=8)
guardar(fig, "e5_05_varianza_n.png")

# ------------------------------------------------------------------ F6: muestreo por importancia
fig, ax = plt.subplots(1, 3, figsize=(13, 4))
dd4 = [float(k) for k in P4]
vr = [P4[k]["eta"]["0.1"]["var_rel"] for k in P4]
cota = [P4[k]["eta"]["0.1"]["cota_var_rel"] for k in P4]
dd5 = [float(k) for k in P5]
ax[0].plot(dd4, cota, "-", color="#8a8a8a", lw=1.2, label="cota φ_T/φ − 1 (Proposición 4)")
ax[0].plot(dd4, vr, "s", color=C[1], label="medida, η = 0.1 (04)")
ax[0].plot(dd5, [P5[k]["var_rel"] for k in P5], "D", color=C[2], label="medida, η = 0.2 (05)")
ax[0].plot(dd5, [P5[k]["cota_var_rel"] for k in P5], "-", color="#bdbdbd", lw=1.2)
ax[0].set_xlabel("δ"); ax[0].set_ylabel("varianza relativa del estimador de a")
ax[0].set_title("Varianza finita y acotada hasta el umbral", fontsize=10); ax[0].legend(fontsize=8)
dev = [X4[k]["p2"]["dev_sigmas"] for k in P4]
ax[1].axhspan(-3, 3, color="#f0f0f0", zorder=0); ax[1].axhline(0, color="#8a8a8a", lw=1)
ax[1].plot(dd4, dev, "s", color=C[1], label="extrapolado η → 0, p = 2 (04b)")
ax[1].plot(dd5, [P5[k]["dev_sigma_total"] for k in P5], "D", color=C[2], label="η = 0.2, σ con sesgo (05)")
ax[1].set_xlabel("δ"); ax[1].set_ylabel("(a_MI − a_EDO)/σ")
ax[1].set_title("Acuerdo con la EDO", fontsize=10); ax[1].legend(fontsize=8)
co = J["05_cerca_umbral"]["costo"]; c4 = P4
aT4 = [abs(P4[k]["eta"]["0.2"]["a_T"]) for k in P4]; pp4 = [P4[k]["eta"]["0.2"]["pasos_medios"] for k in P4]
ax[2].loglog(aT4, pp4, "s", color=C[1], label="04 (η = 0.2)")
ax[2].loglog(co["a_T"], co["pasos_medios"], "D", color=C[2], label=f"05: pendiente {co['pendiente_loglog']:.2f}")
xx = np.geomspace(min(aT4), max(co["a_T"]), 10)
ax[2].loglog(xx, co["pasos_medios"][-1] * xx / co["a_T"][-1], color="#8a8a8a", lw=1, ls="--", label="∝ |a_T|")
ax[2].set_xlabel("|a_T| (longitud de dispersión de la guía)"); ax[2].set_ylabel("pasos por camino")
ax[2].set_title("Costo por camino ∝ |a_T| ∝ 1/(δ − δ_c)", fontsize=10); ax[2].legend(fontsize=8)
guardar(fig, "e5_06_importancia.png")

# ------------------------------------------------------------------ F7: mapa de varianza finita (delta, delta_T)
fig, ax = plt.subplots(figsize=(6.4, 4.4))
mp = R1["mapa_varianza_MI"]
d7 = np.array([m["delta"] for m in mp]); t7 = np.array([m["delta_T_max"] for m in mp])
ax.fill_between(d7, DC, d7, color="#d7ecdf", label="δ_c < δ_T < δ: supersolución, pesos ≤ 1")
ax.fill_between(d7, d7, np.minimum(t7, 6), color="#e9f2fb", label="δ < δ_T < δ_T^max: pesos > 1, varianza finita")
ax.plot(d7, np.minimum(t7, 6), color=C[0], lw=1.5, label="δ_T^max(δ): 2q_δ − q_δT crítico")
ax.plot(d7, [m["delta_T_regla"] for m in mp], color=C[1], lw=1.5, ls="--", label="regla usada: a_T = 1.25 a")
sub = J["05_cerca_umbral"]["subsolucion"]
for k, v in sub.items():
    ax.plot([v["delta"]], [v["delta_T"]], "x" if not v["varianza_finita_pred"] else "o", color=C[2], ms=7)
    ax.annotate(f"δ_T = {k}: θ_MC = {v['theta_MC']:.2f} (pred. {v['theta_pred']:.2f}, η = 0.2)", (v["delta"], v["delta_T"]), fontsize=7.5,
                xytext=(5, 3), textcoords="offset points", color=TXT)
ax.axhline(DC, color="#8a8a8a", lw=1, ls=":")
ax.set_ylim(1.1, 6); ax.set_xlabel("δ (objetivo)"); ax.set_ylabel("δ_T (guía)")
ax.set_title("¿Qué guías dan varianza finita?", fontsize=10); ax.legend(fontsize=7.5, loc="upper left")
guardar(fig, "e5_07_mapa_guias.png")

# ------------------------------------------------------------------ F8: supervivencia de X frente a la mezcla
fig, ax = plt.subplots(figsize=(6.4, 4.2))
sv = R3["supervivencia"]
x = np.array(sv["x"]); pe = np.array(sv["P_emp"]); pp_ = np.array(sv["P_pred"])
ok = pe > 0
ax.semilogy(x[ok], pe[ok], "o", ms=3, mfc="white", color=C[0], label="MC (N = 10⁷, η = 0.2)")
ax.semilogy(x, pp_, color="#3b3b3b", lw=1.4, label="Σ_k w̄_k exp(−x/δ_c(ks)), 14 términos")
ax.semilogy(x, R3["mezcla_usada"]["wbar"][0] * np.exp(-x / DC), color=C[1], lw=1, ls="--", label="solo k = 1")
ax.set_xlabel("x = δΛ (universal)"); ax.set_ylabel("P(X > x)")
ax.set_title("Ley exacta del funcional: tasas = 1/δ_c(ns)", fontsize=10); ax.legend(fontsize=8)
guardar(fig, "e5_08_supervivencia.png")

# ------------------------------------------------------------------ F9: sesgo de discretizacion
fig, ax = plt.subplots(figsize=(6.4, 4.2))
ex = R2["extrapolacion"]
for i, d in enumerate(["2.5", "3", "4"]):
    e = ex[d]
    eta = np.array(e["eta"]); b = np.abs(np.array(e["sesgo_rel"])); er = np.array(e["err"]) / abs(e["a_edo"])
    ax.errorbar(eta, b, yerr=er, fmt="o-", color=C[i], ms=4, lw=1.2, label=f"libre (puente), δ = {d}")
S4 = J["04_importancia"]["sesgo_eta"]
for i, d in enumerate(["3", "1.5"]):
    f = S4[d]["filas"]
    ax.errorbar([x["eta"] for x in f], [abs(x["dif_rel"]) for x in f], yerr=[x["err"] / abs(x["a_edo"]) for x in f],
                fmt="s--", color=C[3 + i], ms=4, lw=1.2, label=f"importancia, δ = {d}")
et = np.array([0.05, 0.8])
ax.loglog(et, 0.0042 * (et / 0.4) ** 4, color="#8a8a8a", lw=1, label="∝ η⁴")
ax.loglog(et, 0.02 * (et / 0.4) ** 2, color="#8a8a8a", lw=1, ls=":", label="∝ η²")
ax.set_xlabel("η (dt = η² r²)"); ax.set_ylabel("|sesgo relativo de a|")
ax.set_title("Sesgo de discretización", fontsize=10); ax.legend(fontsize=7.5)
guardar(fig, "e5_09_sesgo_eta.png")
