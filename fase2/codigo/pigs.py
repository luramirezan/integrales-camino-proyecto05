"""pigs.py -- PIGS radial (path integral ground state) para l = 0 (Fase 2, proyecto 05).

Unidades hbar = m = g = 1. V(r) = -e^{-delta r}/r = V_C(r) + W(r), V_C = -1/r, W = (1 - e^{-delta r})/r
acotado en [0, delta].

Caminos ABIERTOS r_0, ..., r_M (M = tau/eps eslabones, r continuo, r > 0) con peso

    P[r] ~ u_T(r_0) * prod_k T(r_k, r_{k+1}) * u_T(r_M),          u_T(r) = r e^{-r},
    T(a, b) = K_D(a, b; eps) e^{-U_C(a, b; eps)} e^{-eps [W(a) + W(b)]/2},

con K_D el nucleo libre con imagen (garantiza u(0) = 0), U_C la accion de pares EXACTA del Coulomb
puro (tabla de pares.py, con Richardson en h_tab, interpolada en r continuo) y W el resto acotado.
Es la misma accion que la de transferencia.py (alli en nodos, aqui interpolada). El peso es real,
positivo y normalizable; no aparece nunca 1/r desnudo en el exponente (no hay accion primitiva).

Movimientos de Metropolis (todos cumplen balance detallado):
  1. Rebrote de segmentos de L eslabones por puente browniano (Levy): los L-1 puntos interiores se
     proponen con la parte gaussiana libre; se acepta con el resto (imagen, U_C, W). Dos rejillas
     de segmentos desplazadas L/2 para que ningun punto quede siempre en un borde.
  2. Rebrote de extremos: los L/2 primeros (o ultimos) puntos se proponen como caminata libre que
     parte del punto r_{L/2} (o r_{M-L/2}); se acepta con el resto y la razon de u_T en el extremo.
  3. Escala global r -> lam r con ln lam ~ N(0, s^2) (propuesta simetrica en ln lam); el jacobiano
     de la medida prod dr_k es lam^{M+1}.
  Propuestas con algun r <= 0 se rechazan (el peso es cero alli).

Estimadores:
  - Energia: estimador MIXTO en los extremos, E_L(r) = (H u_T)(r)/u_T(r) = W(r) - 1/2 (exacto para
    u_T = r e^{-r}: -u''/(2u) = 1/r - 1/2 y V = -1/r + W). Se promedia en r_0 y r_M. Converge a E0
    del hamiltoniano efectivo de la accion cuando tau -> inf (para delta = 0 vale -1/2 sin varianza).
  - <r>, <r^2>: estimador PURO en el eslabon central r_{M/2} (la densidad alli es psi_{tau/2}^2,
    que tiende a |u_0|^2 para tau -> inf; no es el mixto <u_T|r|u_0>/<u_T|u_0>).

Errores: por bloques (nb bloques por cadena) y dispersion entre cadenas independientes; se
reporta el MAYOR (regla de 9.7 de la Fase 1). Tiempo de autocorrelacion integrado con ventana
automatica de Sokal (c = 6) y, como control, el que implica el error por bloques.

Contenido
---------
interpolador(tabla, metodo)            -> U(a, b) vectorial ('bilineal' propio, rapido; 'bicubica' spline)
cadena(delta, tau, eps, nsweep, seed, Ufun, L=10, ntherm=500, nscale=4, Ualt=None)  -> dict de series
bloques(x, nb=20)                      -> (media, error por bloques)
tau_int_sokal(x, c=6)                  -> (tau_int, ventana)
combinar(lista_de_series, nb=20)       -> media, error por bloques combinado, error entre cadenas, mayor
"""
import time
import numpy as np

from pares import U_extremos


# ------------------------------------------------------------------ interpolacion de U_C
def interpolador(tabla, metodo="bicubica"):
    """Devuelve U(a, b) vectorial. 'bicubica': spline de pares.TablaPares (error ~1e-8).
    'bilineal': interpolacion bilineal propia en la matriz completa (como la Fase 1, pero con
    extrapolacion LINEAL por debajo del primer nodo en vez de constante). Fuera de r = rmax: accion
    de extremos. |a - b| > banda: NaN (el movimiento se rechaza)."""
    if metodo == "bicubica":
        tabla._spline("bicubica")          # se construye antes del fork
        return lambda a, b: tabla.valor(a, b, "bicubica")
    if metodo != "bilineal":
        raise ValueError(metodo)
    F = tabla.completa()
    rt = tabla.r; h = tabla.h; r0 = float(rt[0]); n = len(rt); rmax = float(rt[-1])
    eps, banda = tabla.eps, tabla.banda

    def U(a, b):
        a = np.asarray(a, float); b = np.asarray(b, float)
        out = U_extremos(a, b, eps)            # fuera de la tabla (con Wigner-Kirkwood, V3)
        ins = (a <= rmax) & (b <= rmax)
        x = (a[ins] - r0) / h; y = (b[ins] - r0) / h
        i = np.clip(np.floor(x).astype(int), 0, n - 2); j = np.clip(np.floor(y).astype(int), 0, n - 2)
        fx, fy = x - i, y - j                  # fx < 0 bajo el primer nodo: extrapolacion lineal
        out[ins] = ((1 - fx) * (1 - fy) * F[i, j] + fx * (1 - fy) * F[i + 1, j]
                    + (1 - fx) * fy * F[i, j + 1] + fx * fy * F[i + 1, j + 1])
        return np.where(np.abs(a - b) > banda, np.nan, out)
    return U


def W_yukawa(delta):
    return lambda x: np.where(x > 1e-12, -np.expm1(-delta * x) / np.maximum(x, 1e-300), delta)


# ------------------------------------------------------------------ cadena de Markov
def cadena(delta, tau, eps, nsweep, seed, Ufun, L=10, ntherm=500, nscale=4, Ualt=None, r_ini=None):
    """Una cadena PIGS. Devuelve dict con series por barrido (tras termalizar):
    EL (media de los dos extremos), EL0, ELM, rmid, r2mid; si Ualt: dS_alt = sum_k [Ualt - U] por
    configuracion (para repesar a la otra interpolacion); aceptaciones y tiempo."""
    t0 = time.perf_counter()
    rng = np.random.default_rng(seed)
    M = int(round(tau / eps))
    # V3 (hallazgo H8 de V2): antes M se truncaba en silencio a un multiplo de L y se guardaba el tau
    # pedido. Ahora se exige que tau/eps sea entero y multiplo de L, y se guarda tau_ef = M eps.
    if abs(M * eps - tau) > 1e-9 * max(1.0, tau) or M % L != 0:
        raise ValueError(f"tau/eps = {tau/eps:.6g} debe ser un entero multiplo de L = {L}")
    if M < L:
        raise ValueError("tau/eps debe ser al menos L")
    Le = L // 2
    mid = M // 2
    W = W_yukawa(delta)
    k_in = np.arange(1, L)
    r = (1.0 + 0.1 * rng.random(M + 1)) if r_ini is None else np.array(r_ini, float)

    def lres(a, b):          # parte no gaussiana de cada eslabon
        return np.log1p(-np.exp(-2 * a * b / eps)) - Ufun(a, b) - 0.5 * eps * (W(a) + W(b))

    def seg_logw(P):         # P: (nseg, n+1)
        v = lres(P[:, :-1].ravel(), P[:, 1:].ravel()).reshape(P.shape[0], -1).sum(1)
        return np.where(np.isfinite(v), v, -np.inf)

    lnuT = lambda x: np.log(x) - x

    def full_logw(P):
        if (P <= 0).any():
            return -np.inf
        v = -(np.diff(P)**2).sum() / (2 * eps) + seg_logw(P[None])[0] + lnuT(P[0]) + lnuT(P[-1])
        return v if np.isfinite(v) else -np.inf

    s_esc = 0.7 / np.sqrt(M)
    acc_seg = n_seg = acc_ext = n_ext = acc_esc = n_esc = 0
    nmed = nsweep
    EL0 = np.empty(nmed); ELM = np.empty(nmed); rm = np.empty(nmed); r2m = np.empty(nmed)
    dS = np.empty(nmed) if Ualt is not None else None
    sq = np.sqrt(eps)
    for sweep in range(ntherm + nsweep):
        # 1. puentes brownianos
        for off in (0, Le):
            s = np.arange(off, M - L + 1, L)
            if s.size == 0:
                continue
            a, b = r[s], r[s + L]
            Wc = np.cumsum(sq * rng.standard_normal((s.size, L)), 1)
            B = Wc[:, :-1] - (k_in / L) * Wc[:, -1:]
            newin = a[:, None] + (b - a)[:, None] * (k_in / L) + B
            idx = s[:, None] + np.arange(L + 1)
            Pold = r[idx]
            ok = (newin > 0).all(1)
            Pnew = Pold.copy(); Pnew[ok, 1:-1] = newin[ok]
            d = seg_logw(Pnew) - seg_logw(Pold)
            accept = ok & (np.log(rng.random(s.size)) < d)
            for j in np.nonzero(accept)[0]:
                r[s[j] + 1: s[j] + L] = newin[j]
            acc_seg += int(accept.sum()); n_seg += s.size
        # 2. extremos
        for end in (0, M):
            if end == 0:
                anchor = r[Le]; idx = np.arange(Le, -1, -1)
            else:
                anchor = r[M - Le]; idx = np.arange(M - Le, M + 1)
            newp = anchor + np.concatenate(([0.0], np.cumsum(sq * rng.standard_normal(Le))))
            n_ext += 1
            if (newp[1:] <= 0).any():
                continue
            old = r[idx]
            d = (seg_logw(newp[None])[0] + lnuT(newp[-1])) - (seg_logw(old[None])[0] + lnuT(old[-1]))
            if np.log(rng.random()) < d:
                r[idx] = newp; acc_ext += 1
        # 3. escala global (jacobiano lam^(M+1))
        lw = full_logw(r)
        for _ in range(nscale):
            lam = np.exp(s_esc * rng.standard_normal())
            new = lam * r
            lwn = full_logw(new)
            if np.log(rng.random()) < lwn - lw + (M + 1) * np.log(lam):
                r = new; lw = lwn; acc_esc += 1
            n_esc += 1
        if sweep >= ntherm:
            k = sweep - ntherm
            EL0[k] = W(r[0]) - 0.5; ELM[k] = W(r[M]) - 0.5
            rm[k] = r[mid]; r2m[k] = r[mid]**2
            if Ualt is not None:
                a_, b_ = r[:-1], r[1:]
                dS[k] = np.nansum(Ualt(a_, b_) - Ufun(a_, b_))
    out = dict(delta=delta, tau=tau, tau_ef=M * eps, eps=eps, M=M, L=L, seed=seed, nsweep=nsweep, ntherm=ntherm,
               EL=0.5 * (EL0 + ELM), EL0=EL0, ELM=ELM, rmid=rm, r2mid=r2m,
               acept_puentes=acc_seg / max(n_seg, 1), acept_extremos=acc_ext / max(n_ext, 1),
               acept_escala=acc_esc / max(n_esc, 1), tiempo=time.perf_counter() - t0, r_final=r.copy())
    if dS is not None:
        out["dS_alt"] = dS
    return out


# ------------------------------------------------------------------ estadistica
def bloques(x, nb=20):
    x = np.asarray(x, float)
    n = len(x) // nb * nb
    b = x[:n].reshape(nb, -1).mean(1)
    return float(x[:n].mean()), float(b.std(ddof=1) / np.sqrt(nb))


def tau_int_sokal(x, c=6.0):
    """Tiempo de autocorrelacion integrado tau = 1/2 + sum_{t>=1} rho(t), ventana automatica W >= c tau.
    Devuelve (tau, W). Varianza nula -> (0, 0). Unidades: barridos (error = sqrt(2 tau var / N))."""
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    v = x.var()
    if v <= 0:
        return 0.0, 0
    f = np.fft.rfft(x, 2 * n)
    acf = np.fft.irfft(f * np.conj(f))[:n] / (n * v)
    s = 0.5
    for t in range(1, n):
        s += acf[t]
        if t >= c * s:
            return float(s), t
    return float(s), n


def tau_bloques(x, err):
    v = np.var(x)
    return float(0.5 * err**2 * len(x) / v) if v > 0 else 0.0


def combinar(series, nb=20):
    """series: lista de arrays (una por cadena). Devuelve dict con media, error por bloques combinado
    sqrt(sum e_i^2)/n, error entre cadenas std/sqrt(n), el mayor y el cociente (entre/bloques)^2."""
    mb = [bloques(x, nb) for x in series]
    m = np.array([a for a, _ in mb]); e = np.array([b for _, b in mb])
    n = len(series)
    eb = float(np.sqrt((e**2).sum()) / n)
    es = float(m.std(ddof=1) / np.sqrt(n)) if n > 1 else float("nan")
    err = max(eb, es) if n > 1 else eb
    return dict(media=float(m.mean()), err_bloques=eb, err_cadenas=es, err=err,
                cociente=(es / eb)**2 if eb > 0 else float("nan"),
                medias_cadena=m.tolist(), err_bloques_cadena=e.tolist())
