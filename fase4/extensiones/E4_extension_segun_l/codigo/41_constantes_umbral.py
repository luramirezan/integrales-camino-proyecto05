"""41_constantes_umbral.py -- E4: constantes de la solucion de energia cero en cada umbral y coeficientes predichos.

Para cada estado (1s, 2s, 2p, 3d) en su delta_c (leido de 40_controles_radial_l.json):
  l = 0: Sigma = int e^{-delta_c r} ubar0^2 dr con ubar0 -> 1 lejos;  prediccion kappa ~ c0 (delta_c - delta),
         c0 = 2 Sigma  (identidad del wronskiano: d(1/a_s)/d delta = -2 Sigma);  <r> kappa -> 1/2, <r^2> kappa^2 -> 1/2.
  l >= 1: u0 normalizada, cola u0 -> A r^{-l};  An2 = A^2;  S = <e^{-delta_c r}>_0  (Hellmann-Feynman: E ~ -S Delta).
  l = 1: <r> = [C0 + An2 (ln(1/kappa) + 5/4 - gamma - ln 2)] (1 + (3/2) An2 kappa) + O(kappa),
         <r^2> = 5 An2/(4 kappa) + D0 + (15/8) An2^2 + O(kappa ln kappa),
         |E| = S Delta + (An2/2) (2 S Delta)^{3/2} + O(Delta^2).
  l = 2: <r> -> <r>_0,  <r^2> = <r^2>_0 - (35/36) An2 kappa + O(kappa^2),  |E| = S Delta + O(Delta^2).
Integrales universales de la cola (se comprueban con mpmath a 30 cifras):
  I_N(l=1) = int_0^inf [(1+x)^2 e^{-2x} - 1]/x^2 dx = -3/2,
  I_2(l=2) = int_0^inf [f2^2 - 1]/x^2 dx = -35/36, f2 = e^{-x}(1 + x + x^2/3),
  K_1      = lim [int_eps^inf (1+x)^2 e^{-2x}/x dx + ln eps] = 5/4 - gamma - ln 2,
  M_1      = int_0^inf (1+x)^2 e^{-2x} dx = 5/4.
Ademas: prediccion del radio de caja en el que el nivel cruza E = 0 (prueba de cajas, script 43):
  l = 0: R_c = a_s ~ 1/(c0 Delta);  l >= 1: R_c^{2l+1} = (2l+1) An2/(2 S Delta).
Salida: resultados/41_constantes_umbral.json y _salida.txt.
"""
import math

import mpmath as mp

import comun4 as c

c.Tee("41_constantes_umbral")
mp.mp.dps = 30
C40 = c.leer_json("40_controles_radial_l")["C_umbrales"]

# ---------------------------------------------------------------- integrales universales
f1 = lambda x: (1 + x) * mp.exp(-x)
f2 = lambda x: mp.exp(-x) * (1 + x + x**2 / 3)
# en [1, inf) se integra f^2/x^2 y se resta int_1^inf dx/x^2 = 1 analiticamente (una primera version
# daba -1.50091 por la cancelacion de f^2 - 1 en los nodos de tanh-sinh muy cerca de x = 0)
# y en [0, 1] f^2 - 1 se escribe expm1(2 ln f) para evitar la cancelacion cerca de x = 0
g1 = lambda x: mp.expm1(2 * mp.log1p(x) - 2 * x)
g2 = lambda x: mp.expm1(2 * mp.log1p(x + x**2 / 3) - 2 * x)
IN = mp.quad(lambda x: g1(x) / x**2, [0, 1]) + mp.quad(lambda x: f1(x)**2 / x**2, [1, mp.inf]) - 1
I2 = mp.quad(lambda x: g2(x) / x**2, [0, 1]) + mp.quad(lambda x: f2(x)**2 / x**2, [1, mp.inf]) - 1
M1 = mp.quad(lambda x: f1(x)**2, [0, mp.inf])
e = mp.mpf("1e-12")
K1 = mp.quad(lambda x: f1(x)**2 / x, [e, 1, mp.inf]) + mp.log(e)
univ = dict(I_N=float(IN), I_N_exacto=-1.5, I_2=float(I2), I_2_exacto=-35 / 36, M_1=float(M1), M_1_exacto=1.25,
            K_1=float(K1), K_1_exacto=1.25 - c.GAMMA_E - math.log(2))
print("Integrales universales de la cola (mpmath, 30 cifras):")
for k in ("I_N", "I_2", "M_1", "K_1"):
    print(f"  {k} = {univ[k]:.15f}   forma cerrada {univ[k + '_exacto']:.15f}   dif {univ[k] - univ[k + '_exacto']:+.1e}")
print("  (K_1 con corte 1e-12: el error del corte es O(1e-12 ln 1e-12))")

# ---------------------------------------------------------------- constantes en cada umbral
cons = {}
for nom, est in c.ESTADOS.items():
    l = est["l"]
    dc = C40[nom]["delta_c"]
    u = c.estado_umbral(l, dc)
    if l == 0:
        u["pred"] = dict(c0=u["c0_pred"], r_kappa=0.5, r2_kappa2=0.5, E_exponente=2, r_exponente=-1, r2_exponente=-2,
                         R_c="1/(c0 Delta)")
    else:
        u["pred"] = dict(S=u["S"], E_exponente=1, kappa2_sobre_Delta=2 * u["S"],
                         R_c_coef=(2 * l + 1) * u["An2"] / (2 * u["S"]), R_c_exponente=-1 / (2 * l + 1),
                         caja_coef=(2 * l + 1) * u["An2"] / 2)
        if l == 1:
            u["pred"].update(pendiente_log=u["An2"], cte_log=u["C0"] + u["An2"] * univ["K_1_exacto"],
                             r2_kappa=1.25 * u["An2"], r2_cte=u["D0"] + 15 / 8 * u["An2"]**2,
                             E_correccion_coef=u["An2"] / 2)
        if l == 2:
            u["pred"].update(r_med0=u["r_med0"], r2_med0=u["r2_med0"], r2_pendiente_kappa=-35 / 36 * u["An2"])
    cons[nom] = u
    print(f"\n{nom} (l = {l}), delta_c = {dc:.13f}:")
    for k, v in u.items():
        if k not in ("pred",):
            print(f"  {k} = {v}")
    print("  predicciones:", u["pred"])
c.guardar_json("41_constantes_umbral", dict(universales=univ, constantes=cons))
