"""transferencia.py -- matriz de transferencia simetrica en banda (Nystrom) para l = 0 (Fase 2, proyecto 05).

Integral de camino discretizada calculada SIN muestreo. Con la accion de pares de Coulomb (por defecto):

    T_ij = h K_D(r_i, r_j; eps) e^{-U_C(r_i, r_j; eps)} e^{-eps [W(r_i) + W(r_j)]/2},

con r_i = i h (i = 1..N, N = R/h - 1, Dirichlet en 0 por la imagen de K_D y en R por la malla),
K_D el nucleo libre con imagen normalizado, U_C la accion de pares exacta del Coulomb puro
(tabla de pares.py, en nodos, sin interpolar) y W = V - V_C un resto ACOTADO (para Yukawa
W = (1 - e^{-delta r})/r en [0, delta]). Fuera de r = R_TAB se usa pares.U_extremos (extremos + Wigner-Kirkwood, V3);
fuera de la banda |r - r'| <= banda de la tabla los elementos son CERO (correccion (iii) del
registro de la Fase 1: antes eran NaN y ARPACK fallaba). La regla del trapecio con u(0) = u(R) = 0
da pesos h iguales, de modo que T es simetrica.

Opcion sin U_C (usar con potenciales sin singularidad, p. ej. pozo cuadrado u oscilador):
    T_ij = h K_D(r_i, r_j; eps) e^{-eps [V(r_i) + V(r_j)]/2}.

E0(eps) = -ln(lambda0)/eps con lambda0 el mayor autovalor (eigsh). El autovector v (u_i ~ v_i, por
la simetria de la factorizacion es el estado fundamental de e^{-eps H_ef}, H_ef = H + O(eps^2)) da
<r>, <r^2>, F_1/2 (trapecio, medio peso en r = R/2) y <r>/R.

Contenido
---------
W_yukawa(delta), V_yukawa(delta)
matriz_T(R, h, eps, W=None, tabla=None, V=None, banda=None) -> (T csr, r)
resolver(R, h, eps, W=None, tabla=None, V=None, nev=1, banda=None, aviso_pared=True)
    -> dict(E0, E1?, r_med, r2_med, F12, sesgo_pared_est, ...); avisa (RuntimeWarning) si la densidad
    llega a la pared en R, que no tiene imagen (V3).
sesgo_pared(r, v, h, eps) -> estimacion -BETA sqrt(eps) u'(R)^2/2 del sesgo de la pared (V3).
proyeccion_mixta(T, r, uT, HuT, eps, taus) -> E_mixto(tau) = <uT|T^M H|uT>/<uT|T^M|uT>, M = tau/eps,
    con H u_T calculado con el hamiltoniano CONTINUO (energia local), y su limite tau -> inf.
"""
import warnings

import numpy as np
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh

from pares import logKD, U_extremos


def W_yukawa(delta):
    """W = V_Y - V_C = (1 - e^{-delta r})/r, acotado en [0, delta] (W(0+) = delta)."""
    return lambda r: np.where(r > 1e-12, -np.expm1(-delta * r) / np.maximum(r, 1e-300), delta)


def V_yukawa(delta):
    return lambda r: -np.exp(-delta * r) / r


def matriz_T(R, h, eps, W=None, tabla=None, V=None, banda=None):
    """Matriz en banda. Con tabla (TablaPares): accion de pares de Coulomb + resto W (callable).
    Sin tabla: hace falta V (callable) y se usa K_D e^{-eps(V_i+V_j)/2}."""
    N = int(round(R / h)) - 1
    r = h * np.arange(1, N + 1)
    usa_UC = tabla is not None
    if usa_UC:
        if abs(tabla.eps - eps) > 1e-14:
            raise ValueError("la tabla es de otro eps")
        step = int(round(h / tabla.h))
        if abs(step * tabla.h - h) > 1e-12:
            raise ValueError("h debe ser multiplo entero del paso de la tabla")
        banda = tabla.banda if banda is None else min(banda, tabla.banda)
        Wr = np.zeros(N) if W is None else W(r)
    else:
        if V is None:
            raise ValueError("sin tabla hace falta V")
        banda = 7.0 * np.sqrt(eps) if banda is None else banda
        Wr = V(r)
    nb = int(np.floor(banda / h + 1e-9))
    diags, offs = [], []
    for d in range(0, min(nb, N - 1) + 1):
        a, b = r[:N - d], r[d:]
        lk = logKD(a, b, eps)
        if usa_UC:
            Uv = U_extremos(a, b, eps)
            i = np.arange(N - d)
            k = (i + 1) * step - 1                    # indice de r_i en la tabla
            m = d * step
            dentro = (k + m) < tabla.nt
            if m <= tabla.nb:
                Uv[dentro] = tabla.Ub[k[dentro], m]
            else:
                Uv[:] = np.nan                         # fuera de la banda tabulada
            val = h * np.exp(lk - Uv - 0.5 * eps * (Wr[:N - d] + Wr[d:]))
        else:
            val = h * np.exp(lk - 0.5 * eps * (Wr[:N - d] + Wr[d:]))
        val[~np.isfinite(val)] = 0.0                   # fuera de banda / NaN -> 0
        diags.append(val); offs.append(d)
        if d:
            diags.append(val); offs.append(-d)
    T = sps.diags(diags, offs, shape=(N, N), format="csr")
    return T, r


def _observables(r, v, R):
    u2 = v**2
    u2 = u2 / u2.sum()
    peso = np.where(r < R / 2 - 1e-9 * R, 1.0, 0.0)
    peso[np.abs(r - R / 2) <= 1e-9 * R] = 0.5
    rm = float((r * u2).sum())
    return dict(r_med=rm, r2_med=float((r**2 * u2).sum()), F12=float((peso * u2).sum()), r_sobre_R=rm / R)


def autoestado(T, nev=1, v0=None):
    lam, v = eigsh(T, k=max(nev, 1), which="LA", v0=v0, tol=0)
    o = np.argsort(lam)[::-1]
    lam, v = lam[o], v[:, o]
    if v[:, 0].sum() < 0:
        v[:, 0] = -v[:, 0]
    return lam, v


BETA_PARED = 0.5825971579390106   # -zeta(1/2)/sqrt(2 pi): corrimiento de una pared vigilada en tiempos discretos


def sesgo_pared(r, v, h, eps):
    """Estimacion del sesgo de la pared en R sin imagen (hallazgo H3 de V2, V3 27-10-2026).
    K_D solo tiene imagen en r = 0; en R la condicion de Dirichlet se impone solo en los nodos de tiempo,
    lo que corre la pared ~BETA sqrt(eps) hacia afuera. Con dE/dR = -u'(R)^2/2 (u normalizada), el sesgo
    es dE ~ -BETA sqrt(eps) u'(R)^2 / 2 (siempre hacia abajo). u'(R) se toma por diferencia centrada a una
    distancia 2 sqrt(eps) de la pared, fuera de la capa limite de anchura ~sqrt(eps) que deja la pared sin
    imagen (con los ultimos nodos la pendiente sale ~sqrt(2) menor). Comprobado frente al radial en R + BETA
    sqrt(eps) (V3): -5.4e-7 frente a -5.5e-7 (delta=0.2, R=10, eps=0.1); -3.2e-6 frente a -3.2e-6 (1.18, 50)."""
    u = v / np.sqrt(h * (v**2).sum())
    j = max(1, len(u) - 1 - int(round(2.0 * np.sqrt(eps) / h)))
    upR = (u[j + 1] - u[j - 1]) / (2.0 * h)
    return float(-0.5 * BETA_PARED * np.sqrt(eps) * upR**2)


def resolver(R, h, eps, W=None, tabla=None, V=None, nev=1, banda=None, aviso_pared=True):
    T, r = matriz_T(R, h, eps, W=W, tabla=tabla, V=V, banda=banda)
    lam, v = autoestado(T, nev)
    out = dict(R=float(R), h=float(h), eps=float(eps), N=len(r), lam0=float(lam[0]),
               E0=float(-np.log(lam[0]) / eps), min_T=float(T.data.min()), nnz=int(T.nnz))
    sp_ = sesgo_pared(r, v[:, 0], h, eps)
    out["sesgo_pared_est"] = sp_
    if aviso_pared and abs(sp_) > max(1e-12, min(1e-7, 1e-3 * abs(out["E0"]))):
        warnings.warn(f"transferencia.resolver: la densidad llega a la pared R={R} (sin imagen); sesgo estimado "
                      f"{sp_:+.2e} (E0={out['E0']:+.3e}). Usar R mayor o corregir la pared.", RuntimeWarning)
    if nev > 1:
        out["E1"] = float(-np.log(lam[1]) / eps)
    out.update(_observables(r, v[:, 0], R))
    out["v"], out["r"] = v[:, 0], r
    return out


def proyeccion_mixta(T, r, uT, HuT, eps, taus, v0=None):
    """E_mixto(tau) = <HuT| T^M |uT> / <uT| T^M |uT>, M = round(tau/eps) (T simetrica).
    Devuelve (lista de E_mixto, limite tau->inf = <v0|H uT>/<v0|uT>)."""
    Ms = [int(round(t / eps)) for t in taus]
    out = {}
    x = uT.copy()
    M = 0
    for Mt in sorted(set(Ms)):
        while M < Mt:
            x = T @ x
            nrm = np.abs(x).max()
            x /= nrm
            M += 1
        out[Mt] = float((HuT @ x) / (uT @ x))
    if v0 is None:
        v0 = autoestado(T)[1][:, 0]
    lim = float((v0 @ HuT) / (v0 @ uT))
    return [out[m] for m in Ms], lim
