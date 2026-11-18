"""pares_l.py -- E4: accion de pares EXACTA del Coulomb en la onda parcial l y matriz de transferencia para l >= 1.

Generaliza fase2/codigo/pares.py y transferencia.py (que son solo l = 0) SIN modificarlos.

Onda parcial l, hbar = m = 1:
    H_l   = -1/2 d^2/dr^2 + l(l+1)/(2 r^2) - 1/r          (Coulomb + centrifugo)
    H_l^0 = -1/2 d^2/dr^2 + l(l+1)/(2 r^2)                 (libre en la onda l)
    K_l(r, r'; eps) = <r| e^{-eps H_l^0} |r'> = 4 pi r r' (2 pi eps)^{-3/2} e^{-(r^2+r'^2)/(2 eps)} i_l(r r'/eps)
                    = sqrt(r r')/eps * Ive(l+1/2, r r'/eps) * e^{-(r-r')^2/(2 eps)}   (exacto; l = 0 da K_D de pares.py)
    U_l(r, r'; eps) = -ln[ rho_l(r, r'; eps) / K_l(r, r'; eps) ],   rho_l = <r| e^{-eps H_l} |r'>.
El centrifugo va EXACTO en K_l; U_l solo contiene el efecto del Coulomb (y su cruce con el centrifugo).
U_l se calcula como en pares.py: red de diferencias finitas de paso h_tab en una caja de Dirichlet R_B = 14,
diagonalizacion del hamiltoniano tridiagonal (con l(l+1)/(2 r_j^2) en la diagonal), exponenciacion espectral y
division por el nucleo libre DE LA MISMA RED (con el mismo centrifugo), para cancelar el error de red; Richardson
entre h_tab = 0.01 y 0.005. Fuera de r = R_TAB = 10 se usa pares.U_extremos (extremos de Coulomb + Wigner-Kirkwood):
alli el centrifugo ya esta en K_l y la correccion cruzada es O(eps^2 l(l+1)/r^5).

Peso: rho_l es el nucleo de un semigrupo de Schrodinger en la semirrecta con potencial acotado inferiormente fuera
del origen y repulsivo en el origen; por Feynman-Kac (y, en la red, porque la matriz tridiagonal tiene fuera de la
diagonal elementos negativos) es real y positivo. K_l > 0 y e^{-U_l} > 0: la matriz T es real, simetrica y de
elementos no negativos; su autovector dominante es de signo constante (Perron-Frobenius).

Contenido: logK_l, tabla_red_l, tabla_richardson_l (cache en E4/resultados/tablas), matriz_T_l, resolver_T.
"""
import os
import time

import numpy as np
import scipy.sparse as sps
from scipy.linalg import eigh_tridiagonal
from scipy.sparse.linalg import eigsh
from scipy.special import ive

import comun4 as c4  # noqa: F401  (anade fase2/codigo a sys.path)
import pares          # fase2 (solo se usan U_extremos y banda_def)
import transferencia as tr

DIR_CACHE = os.path.join(c4.RES, "tablas")
RB_DEF, RTAB_DEF = 14.0, 10.0


def logK_l(a, b, eps, l):
    """ln K_l(a, b; eps) (nucleo libre exacto de la onda parcial l, medida dr)."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    z = a * b / eps
    with np.errstate(divide="ignore"):
        return 0.5 * np.log(a * b) - np.log(eps) + np.log(ive(l + 0.5, z)) - (a - b)**2 / (2 * eps)


def _nombre(l, eps, h, RB, RTAB, banda):
    return os.path.join(DIR_CACHE, f"UCl{l}_eps{eps:.6g}_h{h:.6g}_RB{RB:.6g}_RT{RTAB:.6g}_b{banda:.6g}.npz")


def _calcular(l, eps, h, RB, RTAB, banda):
    N = int(round(RB / h)) - 1
    rr = h * np.arange(1, N + 1)
    off = -0.5 / h**2 * np.ones(N - 1)
    cent = 0.5 * l * (l + 1) / rr**2
    wC, vC = eigh_tridiagonal(1 / h**2 + cent - 1 / rr, off)
    w0, v0 = eigh_tridiagonal(1 / h**2 + cent, off)
    nt = int(round(RTAB / h))
    nb = int(round(banda / h))
    A, B = vC[:nt], v0[:nt]
    rhoC = (A * np.exp(-eps * (wC - wC[0]))) @ A.T
    rho0 = (B * np.exp(-eps * (w0 - w0[0]))) @ B.T
    shift = eps * (wC[0] - w0[0])
    Ub = np.full((nt, nb + 1), np.nan)
    Dlib = np.full((nt, nb + 1), np.nan)     # ln[rho0_red / K_l exacto]: error de red del nucleo libre
    nmalos = 0
    for m in range(nb + 1):
        i = np.arange(nt - m)
        cc, z = rhoC[i, i + m], rho0[i, i + m]
        ok = (cc > 0) & (z > 0)
        nmalos += int((~ok).sum())
        with np.errstate(divide="ignore", invalid="ignore"):
            u = -(np.log(cc) - np.log(z)) + shift
            dl = np.log(z) - eps * w0[0] - np.log(h) - logK_l(rr[i], rr[i + m], eps, l)
        u[~ok] = np.nan
        Ub[i, m] = u
        Dlib[i, m] = dl
    return dict(r=rr[:nt], Ub=Ub, Dlib=Dlib, eps=eps, h=h, RB=RB, RTAB=RTAB, banda=banda, nb=nb, l=l,
                E0_red=float(wC[0]), n_no_positivos=nmalos)


def tabla_red_l(l, eps, h, RB=RB_DEF, RTAB=RTAB_DEF, banda=None, cache=True):
    banda = pares.banda_def(eps) if banda is None else banda
    fn = _nombre(l, eps, h, RB, RTAB, banda)
    if cache and os.path.exists(fn):
        z = np.load(fn)
        d = {k: z[k] for k in z.files}
        for k in ("eps", "h", "RB", "RTAB", "banda", "E0_red"):
            d[k] = float(d[k])
        d["nb"] = int(d["nb"]); d["l"] = int(d["l"]); d["n_no_positivos"] = int(d["n_no_positivos"])
        d["tiempo"] = 0.0; d["cache"] = True
        return d
    t = time.perf_counter()
    d = _calcular(l, eps, h, RB, RTAB, banda)
    d["tiempo"] = time.perf_counter() - t; d["cache"] = False
    if cache:
        os.makedirs(DIR_CACHE, exist_ok=True)
        np.savez(fn, **{k: v for k, v in d.items() if k not in ("cache", "tiempo")})
    return d


def tabla_richardson_l(l, eps, h1=0.01, h2=0.005, RB=RB_DEF, RTAB=RTAB_DEF, banda=None, cache=True):
    """Igual que pares.tabla_richardson, en la onda parcial l."""
    banda = pares.banda_def(eps) if banda is None else banda
    d1 = tabla_red_l(l, eps, h1, RB, RTAB, banda, cache)
    d2 = tabla_red_l(l, eps, h2, RB, RTAB, banda, cache)
    nt = d1["Ub"].shape[0]
    nb = min(d1["Ub"].shape[1] - 1, (d2["Ub"].shape[1] - 1) // 2)
    banda = min(banda, nb * h1)
    k = np.arange(nt)[:, None]; m = np.arange(nb + 1)[None, :]
    k2, m2 = 2 * k + 1, 2 * m
    ok = (k2 + m2 < d2["Ub"].shape[0]) & (m2 < d2["Ub"].shape[1])
    U2 = np.full((nt, nb + 1), np.nan)
    D2 = np.full((nt, nb + 1), np.nan)
    kk, mm = np.broadcast_to(k2, ok.shape)[ok], np.broadcast_to(m2, ok.shape)[ok]
    U2[ok] = d2["Ub"][kk, mm]
    D2[ok] = d2["Dlib"][kk, mm]
    UR = (4 * U2 - d1["Ub"][:, :nb + 1]) / 3
    t = pares.TablaPares(d1["r"], UR, eps, h1, banda, origen=f"l={l} Richardson h_tab={h1},{h2}")
    t.U1, t.U2 = d1["Ub"][:, :nb + 1], U2
    t.D1, t.D2 = d1["Dlib"][:, :nb + 1], D2
    t.l = l
    t.info = dict(E0_red_h1=d1["E0_red"], E0_red_h2=d2["E0_red"],
                  n_no_positivos=(d1["n_no_positivos"], d2["n_no_positivos"]),
                  tiempo=(d1["tiempo"], d2["tiempo"]), cache=(d1["cache"], d2["cache"]))
    return t


def matriz_T_l(R, h, eps, l, W=None, tabla=None):
    """T_ij = h K_l(r_i, r_j) e^{-U_l(r_i, r_j)} e^{-eps [W(r_i) + W(r_j)]/2} (misma estructura que
    transferencia.matriz_T, con K_l y la tabla de la onda l). Sin tabla: U_l = 0 (solo el libre de la onda l)."""
    N = int(round(R / h)) - 1
    r = h * np.arange(1, N + 1)
    if tabla is not None:
        if abs(tabla.eps - eps) > 1e-14 or getattr(tabla, "l", l) != l:
            raise ValueError("la tabla es de otro eps o de otra l")
        step = int(round(h / tabla.h))
        if abs(step * tabla.h - h) > 1e-12:
            raise ValueError("h debe ser multiplo entero del paso de la tabla")
        banda = tabla.banda
    else:
        banda = pares.banda_def(eps)
    Wr = np.zeros(N) if W is None else W(r)
    nb = int(np.floor(banda / h + 1e-9))
    diags, offs = [], []
    for d in range(0, min(nb, N - 1) + 1):
        a, b = r[:N - d], r[d:]
        lk = logK_l(a, b, eps, l)
        if tabla is not None:
            Uv = pares.U_extremos(a, b, eps)
            i = np.arange(N - d)
            k = (i + 1) * step - 1
            m = d * step
            dentro = (k + m) < tabla.nt
            if m <= tabla.nb:
                Uv[dentro] = tabla.Ub[k[dentro], m]
            else:
                Uv[:] = np.nan
        else:
            Uv = np.zeros(N - d)
        val = h * np.exp(lk - Uv - 0.5 * eps * (Wr[:N - d] + Wr[d:]))
        val[~np.isfinite(val)] = 0.0
        diags.append(val); offs.append(d)
        if d:
            diags.append(val); offs.append(-d)
    return sps.diags(diags, offs, shape=(N, N), format="csr"), r


def resolver_T(T, r, R, eps, E_guess, h, k=2):
    """Mayor autovalor por shift-invert (como comun3.resolver_tr) y comprobaciones de Perron y residuo."""
    t = time.perf_counter()
    sigma = float(np.exp(-eps * (E_guess - 2e-4)))
    lam, v = eigsh(T, k=k, sigma=sigma, which="LM", tol=0)
    o = np.argsort(lam)[::-1]
    lam, v = lam[o], v[:, o]
    v0 = v[:, 0] * np.sign(v[:, 0].sum())
    perron = float(v0.min() / np.abs(v0).max())
    res = float(np.linalg.norm(T @ v0 - lam[0] * v0) / np.linalg.norm(v0))
    ob = tr._observables(r, v0, R)
    return dict(E0=float(-np.log(lam[0]) / eps), E1=float(-np.log(lam[1]) / eps), r_med=ob["r_med"],
                r2_med=ob["r2_med"], F12=ob["F12"], perron_min=perron, residuo=res, N=len(r),
                min_T=float(T.data.min()), sesgo_pared_est=tr.sesgo_pared(r, v0, h, eps),
                t=time.perf_counter() - t)
