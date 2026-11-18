"""espectral.py -- revision adversarial de E4 (R4): solucionador INDEPENDIENTE del de E4.

Metodo: colocacion espectral de Chebyshev (Gauss-Lobatto) en [0, Rx] con el cambio de variable
r = c sinh(s), s = b (1 + t)/2, b = asinh(Rx/c), que agrupa puntos cerca del origen y da paso relativo
constante (dr/r ~ cte) lejos. No usa diferencias finitas ni integradores de EDO ni nada de comun4.py.

Ecuacion: -u''/2 + [V(r) + l(l+1)/(2 r^2)] u = E u, V = -exp(-delta r)/r, u(0) = 0.

* Problema de contorno "con normalizacion": filas interiores (H - E) u = 0, u(0) = 0 y en r = Rx una fila de
  normalizacion (u(Rx) = 1, o u'(Rx) = 1). Asi se obtiene la solucion regular evaluada en Rx sin integrar EDO.
* Estado ligado sin caja: fuera de Rx se usa w = r k_l(kappa r) (scipy.special.spherical_kn, no el polinomio
  de E4) y se busca kappa con u'(Rx)/u(Rx) = w'(Rx)/w(Rx).  Momentos: Clenshaw-Curtis + cola por cuadratura.
* Umbral: E = 0 y derivada logaritmica -l/Rx (cola pura r^{-l}; para l = 0, u' = 0).
* Caja de Dirichlet en R: raiz en E de u(R) con u'(R) = 1.
"""
import math
import numpy as np
from scipy.special import spherical_kn
from scipy.integrate import quad
from scipy.optimize import brentq


def cheb(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.hstack([2, np.ones(N - 1), 2]) * (-1) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1 / c) / (dX + np.eye(N + 1))
    D = D - np.diag(D.sum(axis=1))
    return D, x


def clencurt(N):
    theta = np.pi * np.arange(N + 1) / N
    x = np.cos(theta)
    w = np.zeros(N + 1)
    ii = np.arange(1, N)
    v = np.ones(N - 1)
    if N % 2 == 0:
        w[0] = w[N] = 1 / (N**2 - 1)
        for k in range(1, N // 2):
            v -= 2 * np.cos(2 * k * theta[ii]) / (4 * k**2 - 1)
        v -= np.cos(N * theta[ii]) / (N**2 - 1)
    else:
        w[0] = w[N] = 1 / N**2
        for k in range(1, (N - 1) // 2 + 1):
            v -= 2 * np.cos(2 * k * theta[ii]) / (4 * k**2 - 1)
    w[ii] = 2 * v / N
    return x, w


class Malla:
    def __init__(self, Rx, N=400, c=1.0):
        self.Rx, self.N, self.c = Rx, N, c
        D, t = cheb(N)
        b = math.asinh(Rx / c)
        s = b * (1 + t) / 2
        r = c * np.sinh(s)
        r[0] = Rx
        r_t = c * np.cosh(s) * b / 2
        r_tt = c * np.sinh(s) * (b / 2) ** 2
        self.t, self.r = t, r
        self.D1 = D / r_t[:, None]
        self.D2 = (D @ D - (r_tt / r_t)[:, None] * D) / (r_t ** 2)[:, None]
        _, w = clencurt(N)
        self.w = w * r_t            # pesos de cuadratura en r


def V_ef(r, delta, l):
    with np.errstate(divide="ignore", invalid="ignore"):
        return -np.exp(-delta * r) / r + 0.5 * l * (l + 1) / r**2


def resolver_contorno(m, delta, l, E, fila0="u"):
    """Solucion regular con u(0) = 0 y, en Rx, u = 1 (fila0='u') o u' = 1 (fila0='du')."""
    N = m.N
    A = -0.5 * m.D2.copy()
    v = V_ef(m.r, delta, l) - E
    A[np.arange(1, N), np.arange(1, N)] += v[1:N]
    rhs = np.zeros(N + 1)
    A[N, :] = 0.0; A[N, N] = 1.0                       # u(0) = 0
    if fila0 == "u":
        A[0, :] = 0.0; A[0, 0] = 1.0
    else:
        A[0, :] = m.D1[0, :]
    rhs[0] = 1.0
    u = np.linalg.solve(A, rhs)
    return u


def dlog_ext(l, kappa, Rx):
    """w'/w en Rx para w = r k_l(kappa r) (kappa = 0: -l/Rx)."""
    if kappa == 0:
        return -l / Rx
    x = kappa * Rx
    k = spherical_kn(l, x)
    kp = spherical_kn(l, x, derivative=True)
    return 1.0 / Rx + kappa * kp / k


def desajuste(m, delta, l, kappa):
    E = -0.5 * kappa**2
    u = resolver_contorno(m, delta, l, E, "u")
    N = m.N
    # wronskiano con la solucion exterior, para la solucion regular normalizada cerca del origen (sin polos)
    j = int(np.argmin(np.abs(m.r - 0.3)))
    return (m.D1[0, :] @ u - dlog_ext(l, kappa, m.Rx) * u[0]) / (u[j] / m.r[j] ** (l + 1))


def cola(l, kappa, Rx, n):
    """int_Rx^inf r^n [w(r)/w(Rx)]^2 dr, w = r k_l(kappa r); cuadratura en y = ln x."""
    x0 = kappa * Rx
    F0 = x0 * spherical_kn(l, x0)

    def f(y):
        x = math.exp(y)
        F = x * spherical_kn(l, x) / F0
        return x ** (n + 1) * F * F
    y0 = math.log(x0)
    pts = [y0, min(0.0, y0 + 30), math.log(80.0)]
    pts = sorted(set([p for p in pts if p >= y0]))
    tot = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        if b > a:
            tot += quad(f, a, b, epsabs=0, epsrel=1e-13, limit=400)[0]
    return tot / kappa ** (n + 1)


def ligado(delta, l, kappa_lo, kappa_hi, Rx=None, N=400, c=1.0):
    Rx = 50.0 / delta if Rx is None else Rx
    m = Malla(Rx, N, c)
    kap = brentq(lambda k: desajuste(m, delta, l, k), kappa_lo, kappa_hi, xtol=1e-16, rtol=8.9e-16, maxiter=300)
    E = -0.5 * kap**2
    u = resolver_contorno(m, delta, l, E, "u")
    u2 = u**2
    I = [m.w @ (m.r**n * u2) + cola(l, kap, Rx, n) for n in (0, 1, 2)]
    HF = m.w @ (np.exp(-delta * m.r) * u2)
    nodos = int(np.sum(np.sign(u[1:-1])[1:] * np.sign(u[1:-1])[:-1] < 0))
    return dict(delta=delta, l=l, kappa=kap, E=E, r_med=I[1] / I[0], r2_med=I[2] / I[0], HF=HF / I[0],
                nodos=nodos, N=N, Rx=Rx)


def umbral(l, a, b, Rx=None, N=400, c=1.0):
    Rx = 50.0 / a if Rx is None else Rx
    m = Malla(Rx, N, c)
    def f(d):
        # B de la solucion REGULAR normalizada cerca del origen (u ~ r^{l+1}): signo continuo en delta
        u = resolver_contorno(m, d, l, 0.0, "u")
        B = (l * u[0] + Rx * (m.D1[0, :] @ u))
        j = int(np.argmin(np.abs(m.r - 0.3)))
        return B / (u[j] / m.r[j] ** (l + 1))
    return brentq(f, a, b, xtol=1e-16, rtol=8.9e-16, maxiter=300), m


def constantes_umbral(l, dc, Rx=None, N=400, c=1.0):
    Rx = 50.0 / dc if Rx is None else Rx
    m = Malla(Rx, N, c)
    u = resolver_contorno(m, dc, l, 0.0, "u")         # u(Rx) = 1
    u2 = u**2
    ex = np.exp(-dc * m.r)
    if l == 0:
        return dict(Sigma=float(m.w @ (ex * u2)), c0=2 * float(m.w @ (ex * u2)))
    A2crudo = Rx ** (2 * l)                          # u = A r^{-l} fuera, con u(Rx) = 1
    Nn = m.w @ u2 + A2crudo * Rx ** (1 - 2 * l) / (2 * l - 1)
    out = dict(An2=A2crudo / Nn, S=float(m.w @ (ex * u2)) / Nn)
    if l == 1:
        out["C0"] = float(m.w @ (m.r * u2)) / Nn - out["An2"] * math.log(Rx)
        out["D0"] = float(m.w @ (m.r**2 * u2)) / Nn - out["An2"] * Rx
    if l == 2:
        out["r_med0"] = (float(m.w @ (m.r * u2)) + A2crudo * Rx ** (2 - 2 * l) / (2 * l - 2)) / Nn
        out["r2_med0"] = (float(m.w @ (m.r**2 * u2)) + A2crudo * Rx ** (3 - 2 * l) / (2 * l - 3)) / Nn
    return out


def caja(delta, l, R, E_lo, E_hi, N=600, c=1.0):
    m = Malla(R, N, c)
    j = int(np.argmin(np.abs(m.r - 0.3)))

    def f(E):
        # u(R) de la solucion regular normalizada cerca del origen: el cociente no tiene polos en E
        u = resolver_contorno(m, delta, l, E, "du")
        return u[0] / (u[j] / m.r[j] ** (l + 1))
    return brentq(f, E_lo, E_hi, xtol=1e-300, rtol=8.9e-16, maxiter=400)


def caja_autovalores(delta, l, R, N=600, c=1.0, k=3):
    """Autovalores de la caja de Dirichlet por diagonalizacion (para acotar la raiz)."""
    m = Malla(R, N, c)
    H = -0.5 * m.D2 + np.diag(V_ef(m.r, delta, l))
    Hi = H[1:N, 1:N]
    w = np.linalg.eigvals(Hi)
    w = np.sort(w[np.abs(w.imag) < 1e-8].real)
    return w[:k]
