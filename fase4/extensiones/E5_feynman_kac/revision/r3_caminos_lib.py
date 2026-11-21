"""r3_caminos.py -- Revision independiente de E5: simulador de caminos propio (numpy vectorizado, posicion 3D completa).
Paso dt = eta^2 |x|^2, x' = x + sqrt(dt) Z (exacto); int q en el paso = media sobre el puente browniano 3D, calculada
con la media gaussiana del Yukawa (implementacion propia) y Gauss-Legendre de n_gl nodos en el tiempo del puente.
Cierre: |x| > R_in -> vuelve con probabilidad R_in/|x| (a un punto uniforme de la esfera R_in) o termina.
(A) C16: E[delta Lambda] = 1 con eta = 0.8 y 0.4, n_gl = 3 y 12 (prueba de la causa atribuida por E5).
(B) Hill de la cola de W en delta = 2 y 3 (muestras independientes, eta = 0.25), theta frente a delta/delta_c;
    delta_c desde la cola. Semillas propias 8800x."""
import json, os, time
import numpy as np
from scipy.special import erfc, erfcx
AQ = os.path.dirname(os.path.abspath(__file__))
DC = 1.1906124210606

def yuk_gauss(R, s, d):
    """E[e^{-d|X|}/|X|], X ~ N(m, s^2 I), |m| = R. Formula de la convolucion, escrita con erfcx."""
    A = (d * s * s - R) / (s * np.sqrt(2)); B = (d * s * s + R) / (s * np.sqrt(2))
    G = np.exp(-R * R / (2 * s * s))
    T1 = np.where(A > 0, G * erfcx(np.maximum(A, 0)), np.exp(np.minimum(d * d * s * s / 2 - d * R, 700)) * erfc(np.minimum(A, 0)))
    T2 = G * erfcx(B)
    Rs = np.maximum(R, 1e-300)
    f = (T1 - T2) / (2 * Rs)
    x = d * s / np.sqrt(2)
    f0 = np.sqrt(2 / np.pi) / s * (1 - np.sqrt(np.pi) * x * erfcx(x))
    return np.where(R < 1e-6 * s, f0, f)

def simula(r0, d, eta, n_gl, rng):
    tg, wg = np.polynomial.legendre.leggauss(n_gl); tg = (tg + 1) / 2; wg = wg / 2
    N = r0.size
    v = rng.normal(size=(N, 3)); v /= np.linalg.norm(v, axis=1)[:, None]
    x = v * r0[:, None]
    L = np.zeros(N); vivo = np.arange(N); Rin = 36.0 / d
    while vivo.size:
        xx = x[vivo]
        r = np.linalg.norm(xx, axis=1)
        dt = (eta * r) ** 2
        y = xx + np.sqrt(dt)[:, None] * rng.normal(size=xx.shape)
        I = np.zeros(vivo.size)
        for t, w in zip(tg, wg):
            m = np.linalg.norm(xx + t * (y - xx), axis=1)
            I += w * yuk_gauss(m, np.sqrt(t * (1 - t) * dt), d)
        L[vivo] += I * dt
        ry = np.linalg.norm(y, axis=1)
        fuera = ry > 36.0 / d
        vuelve = rng.random(vivo.size) < Rin / ry
        u = rng.normal(size=y.shape); u /= np.linalg.norm(u, axis=1)[:, None]
        y = np.where((fuera & vuelve)[:, None], u * Rin, y)
        x[vivo] = y
        vivo = vivo[~(fuera & ~vuelve)]
    return L

