"""r02_diagnostico_numerov.py -- el error del Numerov de E1 (umbral, metodo B) crece al bajar h. Hipotesis del
revisor: no es redondeo acumulado (es independiente de R), sino la serie de arranque u(h) truncada; se prueba
reescribiendo el Numerov (codigo propio) con arranque de orden h^3 (como E1) y de orden h^4, en float64 y longdouble.
u = r - r^2 + b3 r^3 + b4 r^4, con u'' = -2 e^{-d r} u/r: b3 = (1+d)/3, b4 = -(1/6)(2 b3 - 2 + d^2... ) (ver abajo)."""
import numpy as np
from scipy.optimize import brentq
REF = 1.1906124210606


def coefs(d):
    # u'' = -2 e^{-d r} u / r ; e^{-dr} = 1 - d r + d^2 r^2/2 ; u/r = 1 - r + b3 r^2
    # producto: 1 + (-1 - d) r + (b3 + d + d^2/2) r^2 ;  u'' = 2 a2 + 6 b3 r + 12 b4 r^2, a2 = -1
    b3 = (1 + d) / 3
    b4 = -2 * (b3 + d + d * d / 2) / 12
    return b3, b4


def pend(d, h, R, orden, dt):
    N = int(round(R / h))
    hh = dt(1) / dt(int(round(1 / h)))
    r = hh * np.arange(N + 1, dtype=dt)
    k2 = np.zeros(N + 1, dtype=dt)
    k2[1:] = dt(2) * np.exp(-dt(d) * r[1:]) / r[1:]
    u = np.zeros(N + 1, dtype=dt)
    b3, b4 = coefs(dt(d))
    u[1] = hh - hh * hh + b3 * hh ** 3 + (b4 * hh ** 4 if orden == 4 else 0)
    f = -k2 * u
    f[0] = dt(-2)
    c = hh * hh / 12
    for n in range(1, N):
        u[n + 1] = (2 * u[n] - u[n - 1] + c * (f[n - 1] + 10 * f[n])) / (1 + c * k2[n + 1])
        f[n + 1] = -k2[n + 1] * u[n + 1]
    return float((u[N - 4] - 8 * u[N - 3] + 8 * u[N - 1] - u[N]) / (12 * hh))


for dt in (np.float64, np.longdouble):
    for orden in (3, 4):
        s = []
        for h in (1 / 100, 1 / 200, 1 / 400, 1 / 800):
            dd = brentq(lambda x: pend(x, h, 20.0, orden, dt), 1.17, 1.21, xtol=1e-15)
            s.append(f"{dd - REF:+.2e}")
        print(dt.__name__, "arranque O(h^%d)" % orden, "dc - ref para h = 1/100..1/800:", s, flush=True)
