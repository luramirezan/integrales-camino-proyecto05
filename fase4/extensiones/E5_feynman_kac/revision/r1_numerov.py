"""r1_numerov.py -- Revision independiente de E5: a(delta) por Numerov (rejilla uniforme, Richardson h^4).
No importa nada de E5. u'' = -2 q u, q = e^{-d r}/r, u(0)=0, u'(0)=1. Se usa g = f u con g(0) = -2 (limite).
Tambien: alpha(p) (pendiente de la solucion regular de p q) y su primer cero p1 -> delta/p1 = delta_c;
peso wbar_1 de la mezcla para la partida Gamma (escala delta = 1)."""
import json, os, time
import numpy as np
from scipy.optimize import brentq

AQ = os.path.dirname(os.path.abspath(__file__))

def numerov(d, p, h, R):
    n = int(round(R / h))
    r = np.arange(n + 1) * h
    f = np.empty(n + 1)
    f[1:] = -2 * p * np.exp(-d * r[1:]) / r[1:]
    u = np.zeros(n + 1)
    c = h * h / 12.0
    # serie de Frobenius para u(h): u = r - p r^2 + c3 r^3 ...; c3 = p(p + d)/3 (u''=-2p(1-dr)(r - p r^2)/r)
    u[1] = h - p * h**2 + p * (p + d) / 3 * h**3 + 0.0
    g0 = -2 * p          # f u en r = 0
    # paso n=1 usa g0
    u[2] = (2 * u[1] + 10 * c * f[1] * u[1] - (0 - c * g0)) / (1 - c * f[2])
    for k in range(2, n):
        u[k + 1] = (2 * u[k] * (1 + 5 * c * f[k]) - u[k - 1] * (1 - c * f[k - 1])) / (1 - c * f[k + 1])
    # fuera del potencial u es lineal: pendiente por diferencia de 4o orden hacia atras
    up = (25 * u[n] - 48 * u[n - 1] + 36 * u[n - 2] - 16 * u[n - 3] + 3 * u[n - 4]) / (12 * h)
    return r, u, up

def a_num(d, h, R=None):
    R = R if R is not None else 60.0 / d
    r, u, up = numerov(d, 1.0, h, R)
    return R - u[-1] / up

def a_rich(d, h=4e-3):
    a1, a2 = a_num(d, h), a_num(d, h / 2)
    return a2 + (a2 - a1) / 15, abs(a2 - a1) / 15

out = {}
t0 = time.time()
ref = {1.2: -142.9349, 1.5: None, 2.0: None, 3.0: None, 4.0: None}
for d in [1.2, 1.5, 2.0, 3.0, 4.0, 1.195, 1.192, 1.1907]:
    h = 4e-3 if d > 1.19 else 2e-3
    a, e = a_rich(d, h)
    out[f"{d:g}"] = dict(a_numerov=a, err_richardson=e)
    print(f"delta={d}: a_Numerov = {a:+.10f} (Richardson {e:.1e})", flush=True)
# delta_c: primer cero de alpha(p) con d = 1  => delta_c = 1/p1
def alpha(p, h=4e-3):
    r, u, up = numerov(1.0, p, h, 60.0)
    return up
p1 = brentq(alpha, 0.7, 0.95, xtol=1e-13)
p1b = brentq(lambda p: alpha(p, 2e-3), 0.7, 0.95, xtol=1e-13)
dc = 1 / (p1b + (p1b - p1) / 15)
out["delta_c_numerov"] = dc
print(f"delta_c (Numerov, cero de alpha) = {dc:.12f}")
# wbar_1 = -E_Gamma[u_{p1}(r)/r] / (alpha'(p1) p1), escala d = 1, partida Gamma(2,1)
p1r = 1 / dc
r, u, up = numerov(1.0, p1r, 2e-3, 60.0)
ep = 1e-5
dal = (alpha(p1r + ep, 2e-3) - alpha(p1r - ep, 2e-3)) / (2 * ep)
m = r > 0
Eu = np.trapezoid(r[m] * np.exp(-r[m]) * u[m] / r[m], r[m])
w1 = -Eu / (dal * p1r)
out["wbar1_numerov"] = float(w1)
print(f"wbar_1 (Numerov) = {w1:.5f}")
out["tiempo_s"] = time.time() - t0
json.dump(out, open(os.path.join(AQ, "r1_numerov.json"), "w"), indent=1)
