"""Verificacion independiente (V1): base FEDVR (elementos finitos con cuadratura de Gauss-Lobatto).
Base distinta de las diferencias finitas del proyecto. Dirichlet en r=0 y r=R.
H = -1/2 d^2/dr^2 + V, con V diagonal (promedio de cuadratura en los nodos puente, de modo
que un salto del potencial situado en un borde de elemento se integra sin error de salto).
"""
import numpy as np
from numpy.polynomial import legendre as L

def gll(n):
    """Nodos y pesos de Gauss-Lobatto-Legendre en [-1,1] (n puntos) y matriz de derivadas."""
    c = np.zeros(n); c[-1] = 1.0                  # P_{n-1}
    dc = L.legder(c)
    x = np.concatenate(([-1.0], np.sort(np.real(L.legroots(dc))), [1.0]))
    P = L.legval(x, c)
    w = 2.0 / (n * (n - 1) * P**2)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                D[i, j] = P[i] / (P[j] * (x[i] - x[j]))
    D[0, 0] = -n * (n - 1) / 4.0
    D[-1, -1] = n * (n - 1) / 4.0
    return x, w, D

class FEDVR:
    def __init__(self, bordes, n):
        self.b = np.asarray(bordes, float)
        self.n = n
        t, wt, Dt = gll(n)
        self.t, self.wt = t, wt
        ne = len(self.b) - 1
        Ng = ne * (n - 1) + 1
        xg = np.zeros(Ng); wg = np.zeros(Ng)
        K = np.zeros((Ng, Ng))
        self.elems = []
        for e in range(ne):
            a, c = self.b[e], self.b[e + 1]
            Le = c - a
            xe = a + (t + 1) * Le / 2
            we = wt * Le / 2
            De = Dt * 2 / Le
            idx = np.arange(e * (n - 1), e * (n - 1) + n)
            xg[idx] = xe
            wg[idx] += we
            K[np.ix_(idx, idx)] += 0.5 * (De.T * we) @ De
            self.elems.append((a, c, xe, we, idx))
        self.xg, self.wg, self.Kg = xg, wg, K
        keep = np.arange(1, Ng - 1)                  # Dirichlet en ambos extremos
        self.keep = keep
        self.x = xg[keep]; self.w = wg[keep]
        s = 1 / np.sqrt(self.w)
        self.T = K[np.ix_(keep, keep)] * np.outer(s, s)
        self.R = self.b[-1]

    def diag_funcion(self, f):
        """Valor DVR de la multiplicacion por f: promedio de cuadratura de f en cada nodo,
        evaluando f desde el interior de cada elemento (lado correcto de un salto)."""
        acc = np.zeros_like(self.xg)
        for a, c, xe, we, idx in self.elems:
            xs = xe.copy()
            tiny = 1e-13 * max(1.0, abs(c))
            xs[0] = xe[0] + tiny; xs[-1] = xe[-1] - tiny
            acc[idx] += we * f(xs)
        return (acc / self.wg)[self.keep]

    def evalua(self, coef, r):
        """u(r) = sum_i coef_i chi_i(r) para coef en la base DVR normalizada (columnas si 2D)."""
        r = np.atleast_1d(r)
        full = np.zeros((len(self.xg),) + coef.shape[1:])
        full[self.keep] = (coef.T / np.sqrt(self.w)).T
        out = np.zeros((len(r),) + coef.shape[1:])
        for a, c, xe, we, idx in self.elems:
            m = (r >= a) & (r <= c)
            if not m.any():
                continue
            rr = r[m]
            # Lagrange en los nodos del elemento
            Lm = np.ones((len(rr), self.n))
            for j in range(self.n):
                for k in range(self.n):
                    if k != j:
                        Lm[:, j] *= (rr - xe[k]) / (xe[j] - xe[k])
            out[m] = Lm @ full[idx]
        return out

def bordes_graduados(R, finos=((0.0, 0.05), (0.05, 0.15), (0.15, 0.3), (0.3, 0.5)), l1=0.5, r1=10.0,
                     l2=1.0, r2=40.0, l3=4.0, extra=()):
    """Bordes de elemento: finos cerca del origen, luego longitud l1 hasta r1, l2 hasta r2, l3 hasta R.
    'extra' fuerza bordes (p. ej. el salto del pozo en r=1 o R/2)."""
    b = [0.0]
    for a, c in finos:
        if c < R:
            b.append(c)
    def avanza(hasta, l):
        while b[-1] + 1e-12 < min(hasta, R):
            nxt = min(b[-1] + l, hasta, R)
            b.append(nxt)
    avanza(r1, l1); avanza(r2, l2); avanza(R, l3)
    b = sorted(set(np.round(np.concatenate((b, [e for e in extra if 0 < e < R])), 12)))
    # elimina elementos degenerados
    bb = [b[0]]
    for v in b[1:]:
        if v - bb[-1] > 1e-9:
            bb.append(v)
    return np.array(bb)
