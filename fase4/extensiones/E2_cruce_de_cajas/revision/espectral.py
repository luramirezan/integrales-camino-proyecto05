"""espectral.py -- solucionador INDEPENDIENTE de la revision R2 (no usa e2comun ni DOP853).

Metodo: elementos espectrales de Chebyshev en [0, r_m] (r_m = 40, donde e^{-delta r}/r < 1e-21) marchando el
problema de valor inicial u(0) = 0, u'(0) = 1 elemento a elemento (colocacion de Chebyshev en cada elemento,
cuadratura de Clenshaw-Curtis para int u^2 y int r u^2), y solucion EXACTA libre fuera: u = A sin(k(R - r)) o
A sinh(q(R - r)), integrales exteriores por Gauss-Legendre. E0 por brentq sobre la condicion de empalme.
Unidades hbar = m = g = 1, V = -e^{-delta r}/r.
"""
import numpy as np
from scipy.optimize import brentq

RM = 40.0


def cheb(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.hstack([2, np.ones(N - 1), 2]) * (-1) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    dX = X - X.T
    D = np.outer(c, 1 / c) / (dX + np.eye(N + 1))
    D -= np.diag(D.sum(axis=1))
    return D, x


def clenshaw_curtis(N):
    # pesos en [-1, 1] para los nodos cos(pi j / N)
    th = np.pi * np.arange(N + 1) / N
    w = np.zeros(N + 1)
    v = np.ones(N - 1)
    if N % 2 == 0:
        w[0] = w[N] = 1 / (N**2 - 1)
        for k in range(1, N // 2):
            v -= 2 * np.cos(2 * k * th[1:-1]) / (4 * k * k - 1)
        v -= np.cos(N * th[1:-1]) / (N**2 - 1)
    else:
        w[0] = w[N] = 1 / N**2
        for k in range(1, (N - 1) // 2 + 1):
            v -= 2 * np.cos(2 * k * th[1:-1]) / (4 * k * k - 1)
    w[1:-1] = 2 * v / N
    return w


class Interior:
    def __init__(self, N=32, bordes=None):
        if bordes is None:
            # elementos finos cerca del origen, mas anchos hacia afuera
            bordes = np.concatenate([[0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.5, 8.0, 10.0],
                                     np.arange(12.0, RM + 1e-9, 2.0)])
        self.b = np.asarray(bordes)
        self.N = N
        D, x = cheb(N)
        self.D0, self.x0, self.w0 = D, x, clenshaw_curtis(N)

    def resolver(self, delta, E, V=None):
        """Devuelve u(rm), u'(rm), int_0^rm u^2, int_0^rm r u^2 con u(0)=0, u'(0)=1."""
        u0, up0 = 0.0, 1.0
        n0 = n1 = 0.0
        N = self.N
        for a, b in zip(self.b[:-1], self.b[1:]):
            L = b - a
            r = a + (1 - self.x0) * L / 2           # x0[0]=1 -> r=a ; x0[N]=-1 -> r=b
            D = -self.D0 * 2 / L
            Vr = np.empty_like(r)
            with np.errstate(divide="ignore", invalid="ignore"):
                Vr = -np.exp(-delta * r) / r if V is None else V(r)
            A = D @ D - np.diag(2 * (Vr - E))
            rhs = np.zeros(N + 1)
            # fila del nodo a (indice 0): u(a)=u0 ; fila del nodo b (indice N): u'(a)=up0
            A[0, :] = 0; A[0, 0] = 1; rhs[0] = u0
            A[N, :] = D[0, :]; rhs[N] = up0
            u = np.linalg.solve(A, rhs)
            w = self.w0 * L / 2
            n0 += w @ (u * u); n1 += w @ (r * u * u)
            u0, up0 = u[N], (D @ u)[N]
        return u0, up0, n0, n1


INT = Interior()
_gx, _gw = np.polynomial.legendre.leggauss(400)


def empalme(delta, E, R, it=INT):
    u, up, _, _ = it.resolver(delta, E)
    L = R - RM
    if E > 0:
        k = np.sqrt(2 * E); return up * np.sin(k * L) / k + u * np.cos(k * L)
    if E < 0:
        q = np.sqrt(-2 * E); return up * np.tanh(q * L) / q + u
    return up * L + u


def exterior(E, R):
    L = R - RM
    s = RM + (_gx + 1) * L / 2; w = _gw * L / 2
    if E > 0:
        k = np.sqrt(2 * E); f = np.sin(k * (R - s)) / np.sin(k * L)
    elif E < 0:
        q = np.sqrt(-2 * E); f = np.sinh(q * (R - s)) / np.sinh(q * L)
    else:
        f = (R - s) / L
    return w @ (f * f), w @ (s * f * f)


def E0(delta, R, it=INT):
    """Estado base en la esfera dura R (R > RM). Busca el primer cambio de signo de la condicion de empalme
    subiendo desde abajo (el estado base es la raiz mas baja)."""
    hi = np.pi**2 / (2 * (R - 0.0)**2) * 1.0000001   # cota: E0 < energia libre (potencial atractivo)
    g = lambda E: empalme(delta, E, R, it)
    # rejilla de busqueda: energias negativas (ligado) y positivas
    Es = np.concatenate([-np.geomspace(1e-2, 1e-14, 60), np.linspace(0, hi, 41)[1:]])
    gs = np.array([g(E) for E in Es])
    idx = np.nonzero(np.sign(gs[1:]) != np.sign(gs[:-1]))[0]
    if len(idx) == 0:
        raise RuntimeError("sin raiz")
    i = idx[0]
    E = brentq(g, Es[i], Es[i + 1], xtol=1e-26, rtol=1e-15, maxiter=300)
    u, up, n0, n1 = it.resolver(delta, E)
    e0, e1 = exterior(E, R)
    n0 += u * u * e0; n1 += u * u * e1
    return dict(E0=E, y=2 * R * R * E / np.pi**2, rho=n1 / n0 / R, n_raices_en_busqueda=len(idx))


def energia_cero(delta, it=INT):
    u, up, n0, n1 = it.resolver(delta, 0.0)
    inva = up / (RM * up - u)         # u = A (r - a) fuera
    return dict(u=u, up=up, inv_a=inva)
