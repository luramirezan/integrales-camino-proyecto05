"""Comprobacion de E5-G2 (Gemini): forma de S(x) en fk_comun.phi_nystrom.
S(x) = int_0^inf 2 r'^2 q(r') / max(x, r') dr' con q = delta e^{-delta r}/r ... se integra aqui con mpmath sin usar fk_comun
para la forma, y se compara la forma del codigo, la simplificada de Gemini y la estable con expm1."""
import sys, os, numpy as np, mpmath as mp
mp.mp.dps = 40
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../E5_feynman_kac/codigo"))
import fk_comun as fk
for d in [1.5, 3.0]:
    # q del codigo, evaluada en mp por cociente con e^{-dr}/r para conocer la normalizacion
    c = float(fk.q_yuk(np.array([0.7]), d)[0] / (np.exp(-d * 0.7) / 0.7))
    S_cod = lambda x: 2 * (1 - np.exp(-d * x) * (1 + d * x)) / (d * d * x) + 2 * np.exp(-d * x) / d
    S_gem = lambda x: 2 * (1 - np.exp(-d * x)) / (d * d * x)
    S_est = lambda x: -2 * np.expm1(-d * x) / (d * d * x)
    worst = [0, 0, 0]
    for x in [1e-12, 1e-9, 1e-6, 1e-4, 1e-2, 0.3, 1, 5, 30]:
        ex = 2 * mp.quad(lambda r: r * mp.e ** (-d * r) / max(mp.mpf(x), r), [0, x, mp.inf])  # 2 r'^2 (e^{-dr'}/r') / max
        for k, f in enumerate([S_cod, S_gem, S_est]):
            worst[k] = max(worst[k], abs(f(x) / float(ex) - 1))
    print(f"d={d}: factor q/(e^-dr/r) = {c:.6g}; error relativo max de S en x in [1e-12, 30]: "
          f"codigo {worst[0]:.2e}, Gemini {worst[1]:.2e}, expm1 {worst[2]:.2e}")
    # efecto en a: nodos del Nystrom por defecto
    r0 = (np.sqrt(60 / d) / 600 / 2 * (1 - np.polynomial.legendre.leggauss(8)[0].max())) ** 2
    print(f"   nodo mas pequeno r = {r0:.3e}; S codigo/Gemini - 1 alli = {S_cod(r0)/S_gem(r0)-1:.2e}")

# Efecto en a: phi_nystrom con la S del codigo frente a la S estable (expm1); misma funcion, solo cambia la linea de S
import inspect, textwrap
src = inspect.getsource(fk.phi_nystrom)
src_est = src.replace("S = lambda x: 2 * (1 - np.exp(-d * x) * (1 + d * x)) / (d * d * x) + 2 * np.exp(-d * x) / d",
                      "S = lambda x: -2 * np.expm1(-d * x) / (d * d * x)")
assert src_est != src
ns = dict(fk.__dict__); exec(src_est, ns)
for d in [1.5, 3.0, 4.0]:
    _, a1 = fk.phi_nystrom(d, [1.0]); _, a2 = ns["phi_nystrom"](d, [1.0])
    print(f"d={d}: a(codigo) = {a1:.12f}, a(S estable) = {a2:.12f}, diferencia {a1-a2:.1e}")
