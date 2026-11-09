"""Verificacion independiente (V1): operador de Trotter simetrico e^{-eps W/2} e^{-eps H_C} e^{-eps W/2}
construido ESPECTRALMENTE en la base FEDVR (diagonalizacion de H_C en esa base), sin tabla de U_C
ni Nystrom. Su autovalor mayor da E(eps) = -ln(lambda)/eps, que es el limite h->0 de la matriz
de transferencia del proyecto (T_ij = h rho_C(r_i,r_j) e^{-eps(W_i+W_j)/2}).
Se usa la forma similar M' = B^{1/2} e^{-eps W} B^{1/2} (mismo espectro; autovector suave).
"""
import numpy as np
from scipy.linalg import eigh
import v_fedvr as F

class Espectral:
    def __init__(self, fed, Vc):
        self.f = fed
        Vd = fed.diag_funcion(Vc) if Vc is not None else np.zeros(len(fed.x))
        self.H0 = fed.T + np.diag(Vd)
        self.lam, self.U = eigh(self.H0)

    def B(self, eps, frac=1.0):
        return (self.U * np.exp(-frac * eps * self.lam)) @ self.U.T

    def trotter(self, W, eps, vectores=False):
        f = self.f
        Bh = self.B(eps, 0.5)
        A2 = f.diag_funcion(lambda r: np.exp(-eps * W(r)))
        Mp = (Bh * A2) @ Bh
        Mp = 0.5 * (Mp + Mp.T)
        N = Mp.shape[0]
        l, v = eigh(Mp, subset_by_index=[N - 2, N - 1])
        lam0, phi = l[1], v[:, 1]
        E = -np.log(lam0) / eps
        E1 = -np.log(l[0]) / eps if l[0] > 0 else np.nan
        A = f.diag_funcion(lambda r: np.exp(-0.5 * eps * W(r)))
        psi = A * (Bh @ phi)          # autovector de la forma M = A B A
        psi /= np.sqrt(np.sum(psi**2))
        if psi.sum() < 0:
            psi = -psi
        x = f.x
        out = dict(E=E, E1=E1, r=float(np.sum(psi**2 * x)), r2=float(np.sum(psi**2 * x**2)),
                   perron_min=float(psi.min() / psi.max()))
        # F_1/2 con cuadratura del elemento (R/2 debe ser borde de elemento)
        out["F12"] = float(np.sum(psi[x < f.R / 2 - 1e-9]**2) + self._medio(psi))
        if vectores:
            out["psi"] = psi
        return out

    def _medio(self, psi):
        f = self.f
        j = np.where(np.abs(f.x - f.R / 2) < 1e-9)[0]
        if len(j) == 0:
            return 0.0
        j = j[0]
        # peso izquierdo del nodo puente / peso total
        wl = [we[-1] for a, c, xe, we, idx in f.elems if abs(c - f.R / 2) < 1e-9][0]
        return psi[j]**2 * wl / f.w[j]

    def pigs_det(self, W, EL, uT, eps, taus):
        """Estimador mixto <uT|E_L M^n|uT>/<uT|M^n|uT> y puro <r>, <r^2> en el eslabon central."""
        f = self.f
        B = self.B(eps)
        A = f.diag_funcion(lambda r: np.exp(-0.5 * eps * W(r)))
        M = (A[:, None] * B) * A[None, :]
        a = np.sqrt(f.w) * uT(f.x)
        ELd = EL(f.x)
        res = {}
        for tau in taus:
            n = int(round(tau / eps))
            assert n % 2 == 0
            v = a.copy()
            for _ in range(n // 2):
                v = M @ v
                v /= np.linalg.norm(v)
            vv = v.copy()
            for _ in range(n // 2):
                vv = M @ vv
                vv /= np.linalg.norm(vv)
            Emix = float(np.sum(a * ELd * vv) / np.sum(a * vv))
            res[tau] = dict(E_mixto=Emix, r_puro=float(np.sum(v**2 * f.x) / np.sum(v**2)),
                            r2_puro=float(np.sum(v**2 * f.x**2) / np.sum(v**2)))
        return res

def orden_y_ext(E3):
    """Tres valores en eps, eps/2, eps/4: orden aparente y extrapolado con ese orden."""
    a, b, c = E3
    p = np.log2((a - b) / (b - c))
    return float(p), float(c - (b - c) / (2**p - 1))

def ext_eps2(E3):
    """Richardson eps^2 de dos pasos sobre (eps, eps/2, eps/4)."""
    a, b, c = E3
    r1 = (4 * b - a) / 3; r2 = (4 * c - b) / 3
    return float((16 * r2 - r1) / 15), float(r2)
