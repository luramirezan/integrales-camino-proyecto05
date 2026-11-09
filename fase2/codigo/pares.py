"""pares.py -- tabla de la accion de pares EXACTA del Coulomb puro (Fase 2, proyecto 05).

Unidades hbar = m = g = 1. Sector radial l = 0 (u(0) = 0). Para el Coulomb puro V_C = -1/r,

    rho_C(r, r'; eps) = <r| e^{-eps H_C} |r'>,      H_C = -1/2 d^2/dr^2 - 1/r,
    K_D(r, r'; eps)   = (2 pi eps)^{-1/2} [e^{-(r-r')^2/(2eps)} - e^{-(r+r')^2/(2eps)}]   (libre con imagen),
    U_C(r, r'; eps)   = -ln[ rho_C / K_D ].

Como en la parte C de fase1/codigo/09_prueba_costos.py, U_C se calcula en una red de diferencias
finitas de paso h_tab en una caja de Dirichlet R_B (espectral: se diagonaliza el hamiltoniano
tridiagonal y se exponencia), y se divide por el nucleo libre DE LA MISMA RED, para que el error
de red se cancele en lo posible. El error que queda es O(h_tab^2) y se elimina con Richardson
entre h_tab = 0.01 y 0.005 (en los puntos comunes, la malla de 0.01):

    U_R = (4 U_{0.005} - U_{0.01}) / 3.

Se tabula en r, r' <= R_TAB (10 por defecto) y en la banda |r - r'| <= banda (7 sqrt(eps) por
defecto: el peso gaussiano fuera de la banda es menor que e^{-24.5} = 2.3e-11 del diagonal).
Fuera de r = R_TAB se usa la aproximacion de extremos con la correccion de Wigner-Kirkwood
(desarrollo de alta temperatura de U a orden eps^2, puente browniano con varianza eps s(1-s)):
    U_C ~ (eps/2)[V_C(r) + V_C(r')] + (V_C''(m)/12) [eps^2 - eps (r - r')^2],   m = (r + r')/2,
con V_C'' = -2/r^3. Correccion V3 (hallazgo H2 de V2 / H3 de V1, 27-10-2026): la version anterior
(solo extremos) decia "error O(eps^3 V'^2), < 1e-7 en r >= 10", pero su error real es el termino
eps^2 V''/12 = -eps^2/(6 r^3): 2.29e-6 en r = 9 con eps = 0.1 (medido contra la tabla). Con el
termino de Wigner-Kirkwood el error en la diagonal baja a 8.1e-9 (r = 9, eps = 0.1) y a 6.5e-8
(r = 9, eps = 0.2). wk=False reproduce la version anterior (solo para comparar). Fuera de la banda U_C no se tabula (NaN); quien
la use pone a cero esos elementos de matriz (correccion (iii) del registro de la Fase 1).

Contenido
---------
tabla_red(eps, h_tab, RB=14, RTAB=10, banda=None, cache=True)
    Tabla de una sola red, en almacenamiento en banda Ub[k, m] = U_C(r_k, r_{k+m}), m = 0..nb.
    Con cache=True se guarda / lee en fase2/resultados/tablas/UC_*.npz.
TablaPares
    Objeto con la tabla (una red, o la combinacion de Richardson) en la malla r_k = (k+1) h:
      .en_pares(a_idx_r, b_r)   valores exactos de la tabla en nodos (para Nystrom);
      .valor(a, b, metodo)      interpolacion 'bilineal' o 'bicubica' (spline) para r continuo (PIGS);
      .U_extremos(a, b)         aproximacion de extremos.
tabla_richardson(eps, h1=0.01, h2=0.005, ...) -> TablaPares
    Combina las dos redes con Richardson en la malla de h1.
tabla(eps, h_tab, ...) -> TablaPares
    Una sola red (sin Richardson), para controles.
"""
import os
import time
import numpy as np
from scipy.linalg import eigh_tridiagonal

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR_CACHE = os.path.join(os.path.dirname(AQUI), "resultados", "tablas")
RB_DEF, RTAB_DEF = 14.0, 10.0


def banda_def(eps):
    return 7.0 * np.sqrt(eps)


def logKD(a, b, eps):
    """ln K_D(a, b; eps) con la normalizacion (2 pi eps)^{-1/2} (nucleo libre con imagen, l = 0)."""
    return (-(a - b)**2 / (2 * eps) + np.log1p(-np.exp(-2 * a * b / eps))
            - 0.5 * np.log(2 * np.pi * eps))


WK_DEF = True      # correccion de Wigner-Kirkwood en la aproximacion de extremos (V3)


def U_extremos(a, b, eps, wk=None):
    """Accion de pares de Coulomb fuera de la tabla: extremos (eps/2)[V_C(a) + V_C(b)] mas, si wk,
    el termino de Wigner-Kirkwood (V_C''(m)/12)[eps^2 - eps (a-b)^2], m = (a+b)/2, V_C'' = -2/m^3."""
    wk = WK_DEF if wk is None else wk
    a = np.asarray(a, float); b = np.asarray(b, float)
    U = -0.5 * eps * (1.0 / a + 1.0 / b)
    if wk:
        m = 0.5 * (a + b)
        U = U - (2.0 / m**3) / 12.0 * (eps**2 - eps * (a - b)**2)
    return U


def _nombre_cache(eps, h, RB, RTAB, banda):
    return os.path.join(DIR_CACHE, f"UC_eps{eps:.6g}_h{h:.6g}_RB{RB:.6g}_RT{RTAB:.6g}_b{banda:.6g}.npz")


def _calcular_tabla_red(eps, h, RB, RTAB, banda):
    """Calculo espectral en la red (como la parte C de 09_prueba_costos.py)."""
    N = int(round(RB / h)) - 1
    rr = h * np.arange(1, N + 1)
    off = -0.5 / h**2 * np.ones(N - 1)
    wC, vC = eigh_tridiagonal(1 / h**2 - 1 / rr, off)
    w0, v0 = eigh_tridiagonal(np.full(N, 1 / h**2), off)
    nt = int(round(RTAB / h))
    nb = int(round(banda / h))
    A, B = vC[:nt], v0[:nt]
    # desplazamientos para evitar desbordes (se cancelan al final): e^{-eps(w - w_min)}
    rhoC = (A * np.exp(-eps * (wC - wC[0]))) @ A.T
    rho0 = (B * np.exp(-eps * (w0 - w0[0]))) @ B.T
    # rho_verdadero = e^{-eps w_min} rho_calculado  =>  U = -(ln c - ln z) + eps (wC0 - w00)
    shift = eps * (wC[0] - w0[0])
    Ub = np.full((nt, nb + 1), np.nan)
    nmalos = 0
    for m in range(nb + 1):
        i = np.arange(nt - m)
        c, z = rhoC[i, i + m], rho0[i, i + m]
        ok = (c > 0) & (z > 0)
        nmalos += int((~ok).sum())
        with np.errstate(divide="ignore", invalid="ignore"):
            u = -(np.log(c) - np.log(z)) + shift
        u[~ok] = np.nan
        Ub[i, m] = u
    return dict(r=rr[:nt], Ub=Ub, eps=eps, h=h, RB=RB, RTAB=RTAB, banda=banda, nb=nb,
                E0_red=float(wC[0]), n_no_positivos=nmalos)


def tabla_red(eps, h_tab, RB=RB_DEF, RTAB=RTAB_DEF, banda=None, cache=True, verbose=False):
    """Tabla de una red; devuelve dict con r, Ub (banda), E0_red, tiempo y si salio de la cache."""
    banda = banda_def(eps) if banda is None else banda
    fn = _nombre_cache(eps, h_tab, RB, RTAB, banda)
    if cache and os.path.exists(fn):
        try:
            z = np.load(fn)
            d = {k: z[k] for k in z.files}
            for k in ("eps", "h", "RB", "RTAB", "banda", "E0_red"):
                d[k] = float(d[k])
            d["nb"] = int(d["nb"]); d["n_no_positivos"] = int(d["n_no_positivos"])
            d["cache"] = True; d["tiempo"] = 0.0
            return d
        except Exception as e:  # cache corrupta: se recalcula
            if verbose:
                print("cache ilegible, se recalcula:", fn, e)
    t = time.perf_counter()
    d = _calcular_tabla_red(eps, h_tab, RB, RTAB, banda)
    d["tiempo"] = time.perf_counter() - t
    d["cache"] = False
    if cache:
        os.makedirs(DIR_CACHE, exist_ok=True)
        np.savez(fn, **{k: v for k, v in d.items() if k not in ("cache", "tiempo")})
    return d


class TablaPares:
    """Tabla U_C en la malla r_k = (k+1) h, k = 0..nt-1, almacenada en banda Ub[k, m] = U(r_k, r_{k+m})."""

    def __init__(self, r, Ub, eps, h, banda, origen=""):
        self.r = np.asarray(r); self.Ub = np.asarray(Ub)
        self.eps, self.h, self.banda = float(eps), float(h), float(banda)
        self.nt, self.nb = self.Ub.shape[0], self.Ub.shape[1] - 1
        self.rmax = float(self.r[-1])
        self.origen = origen
        self._spl = {}

    # --- valores en nodos -------------------------------------------------------------
    def en_nodos(self, k, m):
        """U(r_k, r_{k+m}) para indices de tabla k (>=0) y m (>=0); NaN si fuera de tabla/banda."""
        k = np.asarray(k); m = np.asarray(m)
        out = np.full(np.broadcast(k, m).shape, np.nan)
        ok = (k >= 0) & (m >= 0) & (m <= self.nb) & (k + m < self.nt)
        kk, mm = np.broadcast_arrays(k, m)
        out[ok] = self.Ub[kk[ok], mm[ok]]
        return out

    def U_extremos(self, a, b):
        return U_extremos(a, b, self.eps)

    def completa(self):
        """Matriz nt x nt simetrica con NaN fuera de la banda."""
        F = np.full((self.nt, self.nt), np.nan)
        for m in range(self.nb + 1):
            i = np.arange(self.nt - m)
            F[i, i + m] = self.Ub[i, m]
            F[i + m, i] = self.Ub[i, m]
        return F

    # --- interpolacion para r continuo (PIGS) -----------------------------------------
    def _spline(self, metodo):
        if metodo not in self._spl:
            from scipy.interpolate import RectBivariateSpline
            F = self.completa()
            # relleno fuera de la banda: se prolonga en |r-r'| el valor del borde de la banda
            # (solo para que el spline este definido; esos puntos se devuelven como NaN)
            for m in range(self.nb + 1, self.nt):
                i = np.arange(self.nt - m)
                F[i, i + m] = self.Ub[i, self.nb]          # i + nb < i + m < nt: siempre existe
                F[i + m, i] = self.Ub[i, self.nb]
            # cualquier NaN restante (bordes de la tabla): copia del vecino en la misma fila
            if np.isnan(F).any():
                for k in range(self.nt):
                    row = F[k]
                    bad = np.isnan(row)
                    if bad.any():
                        good = np.nonzero(~bad)[0]
                        row[bad] = np.interp(np.nonzero(bad)[0], good, row[good])
            kx = 1 if metodo == "bilineal" else 3
            self._spl[metodo] = RectBivariateSpline(self.r, self.r, F, kx=kx, ky=kx, s=0)
        return self._spl[metodo]

    def valor(self, a, b, metodo="bicubica"):
        """U_C(a, b) para a, b > 0 continuos. Dentro de la tabla: interpolacion ('bilineal' o
        'bicubica'; por debajo del primer nodo se extrapola con el polinomio del borde);
        con a o b > rmax: aproximacion de extremos; |a-b| > banda: NaN."""
        a = np.atleast_1d(np.asarray(a, float)); b = np.atleast_1d(np.asarray(b, float))
        a, b = np.broadcast_arrays(a, b)
        out = U_extremos(a, b, self.eps)
        dentro = (a <= self.rmax) & (b <= self.rmax)
        if dentro.any():
            out = out.copy()
            spl = self._spline(metodo)
            aa, bb = a[dentro], b[dentro]
            r0 = float(self.r[0])
            ac, bc = np.maximum(aa, r0), np.maximum(bb, r0)
            v = spl.ev(ac, bc)
            # por debajo del primer nodo el spline de FITPACK se queda constante: se extrapola
            # linealmente con la pendiente del primer intervalo de la tabla (diferencia finita h)
            hh = self.h
            ba, bb_ = aa < r0, bb < r0
            if ba.any():
                v[ba] += (aa[ba] - r0) * (spl.ev(ac[ba] + hh, bc[ba]) - spl.ev(ac[ba], bc[ba])) / hh
            if bb_.any():
                v[bb_] += (bb[bb_] - r0) * (spl.ev(ac[bb_], bc[bb_] + hh) - spl.ev(ac[bb_], bc[bb_])) / hh
            out[dentro] = v
        out = np.where(np.abs(a - b) > self.banda, np.nan, out)
        return out


def tabla(eps, h_tab, RB=RB_DEF, RTAB=RTAB_DEF, banda=None, cache=True):
    d = tabla_red(eps, h_tab, RB, RTAB, banda, cache)
    t = TablaPares(d["r"], d["Ub"], eps, h_tab, d["banda"], origen=f"red h_tab={h_tab}")
    t.info = {k: d[k] for k in ("E0_red", "n_no_positivos", "tiempo", "cache")}
    return t


def tabla_richardson(eps, h1=0.01, h2=0.005, RB=RB_DEF, RTAB=RTAB_DEF, banda=None, cache=True):
    """Richardson U_R = (4 U_{h2} - U_{h1})/3 en los nodos de h1 (h1 = 2 h2)."""
    assert abs(h1 - 2 * h2) < 1e-15
    banda = banda_def(eps) if banda is None else banda
    d1 = tabla_red(eps, h1, RB, RTAB, banda, cache)
    d2 = tabla_red(eps, h2, RB, RTAB, banda, cache)
    nt = d1["Ub"].shape[0]
    # banda comun: m de h1 <-> 2m de h2 (con el redondeo puede faltar la ultima columna de h2)
    nb = min(d1["Ub"].shape[1] - 1, (d2["Ub"].shape[1] - 1) // 2)
    banda = min(banda, nb * h1)
    # nodo k de h1 (r=(k+1)h1) es el nodo 2k+1 de h2; m de h1 es 2m de h2
    k = np.arange(nt)[:, None]; m = np.arange(nb + 1)[None, :]
    k2, m2 = 2 * k + 1, 2 * m
    ok = (k2 + m2 < d2["Ub"].shape[0]) & (m2 < d2["Ub"].shape[1])
    U2 = np.full((nt, nb + 1), np.nan)
    U2[ok] = d2["Ub"][np.broadcast_to(k2, ok.shape)[ok], np.broadcast_to(m2, ok.shape)[ok]]
    UR = (4 * U2 - d1["Ub"][:, :nb + 1]) / 3
    t = TablaPares(d1["r"], UR, eps, h1, banda, origen=f"Richardson h_tab={h1},{h2}")
    t.U1, t.U2 = d1["Ub"][:, :nb + 1], U2           # para diagnostico (mismos nodos)
    t.info = dict(E0_red_h1=d1["E0_red"], E0_red_h2=d2["E0_red"],
                  n_no_positivos=(d1["n_no_positivos"], d2["n_no_positivos"]),
                  tiempo=(d1["tiempo"], d2["tiempo"]), cache=(d1["cache"], d2["cache"]))
    return t


if __name__ == "__main__":
    for eps in (0.1,):
        t = tabla_richardson(eps)
        print(t.origen, "eps=", eps, "nt=", t.nt, "nb=", t.nb, "info=", t.info)
        for r in (0.01, 0.02, 0.05, 0.1, 0.5, 1.0, 9.0):
            k = int(round(r / t.h)) - 1
            print(f"  U_R({r},{r}) = {t.Ub[k, 0]:.8f}   U_h1 = {t.U1[k, 0]:.8f}   U_h2 = {t.U2[k, 0]:.8f}")
