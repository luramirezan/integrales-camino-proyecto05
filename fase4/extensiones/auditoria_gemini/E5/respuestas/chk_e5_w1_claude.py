"""Forma cerrada propuesta por Claude: w1bar = delta_c/(2c), con c = -d(1/a)/d delta en delta_c (convencion de E5:
u ~ r - a, a < 0 sin ligado). Independiente del codigo de E5 (EDO propia, DOP853)."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def inv_a(d):
    R = 60 / d + 40
    s = solve_ivp(lambda r, y: [y[1], -2 * np.exp(-d * r) / r * y[0]], [1e-10, R], [1e-10, 1.0],
                  method="DOP853", rtol=1e-13, atol=1e-30)
    u, up = s.y[0, -1], s.y[1, -1]
    return -up / (u - up * R)            # 1/a, con a = -(u - up R)/up
dc = brentq(inv_a, 1.15, 1.25, xtol=1e-14)
h = 1e-4
c = -(inv_a(dc + h) - inv_a(dc - h)) / (2 * h)
print(f"delta_c = {dc:.12f}; c = -d(1/a)/d delta = {c:.6f}; delta_c/(2c) = {dc/(2*c):.6f}  (E5: w1bar = 0.80317)")
