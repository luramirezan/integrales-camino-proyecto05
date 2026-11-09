"""
09_prueba_costos.py  --  Proyecto 05 (Yukawa), Fase 1, bloque 09: prueba de costos para el plan de computo.

Unidades: hbar = m = g = 1, delta = mu hbar^2/(m g). Ecuacion radial l=0: -u''/2 - e^{-delta r} u/r = E u.

Partes (todas cronometradas con time.perf_counter):
  A. Solucionador radial (DF + Richardson, receta de la seccion 5) en delta = 0.2 y 1.1; observables
     E0, <r>, <r^2>^{1/2}, fraccion de densidad en la mitad interior de la caja F_1/2.
  B. Barrido corto de cajas cerca del umbral (delta = 1.15, 1.18, 1.20, 1.25; R = 50 ... 800):
     prueba de que el signo de E0(R) solo no decide y de que <r>/R y F_1/2 separan ligado de caja.
  C. Tabla de la accion de pares de Coulomb U_C(r,r';eps) = -ln(rho_C/rho_libre) en la red
     (espectral, como el bloque 08 parte G) para h = 0.01 y 0.005; costo y error de tabulacion.
  D. Proyeccion determinista (matriz de transferencia T = e^{-eps W/2} rho_C e^{-eps W/2}) desde
     u_T = r e^{-r}: duracion tau necesaria para sesgo de proyeccion < 1e-5 en delta = 0.2.
  E. PIGS (path integral ground state) radial con Metropolis, r continuo, accion de pares interpolada,
     movimientos de puente browniano (L=10), de extremos y de escala global: control delta = 0
     (funcion de prueba exacta) y punto fuertemente ligado delta = 0.2 (8 cadenas); error por bloques
     frente a dispersion entre semillas, tiempo por barrido y extrapolacion del costo (4 procesos).
  F. Integral de camino determinista: matriz de transferencia en banda (Nystrom) con la misma accion;
     Richardson en el paso de la tabla; ley eps^2 en delta = 1.0.

Semillas fijas: delta=0: 20261012; delta=0.2: 20261013 a 20261020 (numpy default_rng).
"""
import time
import numpy as np
from scipy.linalg import eigh_tridiagonal

T0 = time.perf_counter()
import os
print(f"Carga de la maquina al empezar (loadavg 1, 5, 15 min): {os.getloadavg()}; nucleos: {os.cpu_count()}")
DC = 1.19061242106


def tic():
    return time.perf_counter()


# ----------------------------------------------------------------------------- A. solucionador radial
def radial(dl, R, h, nev=1):
    N = int(round(R / h)) - 1
    hh = R / (N + 1)
    rr = hh * np.arange(1, N + 1)
    w, v = eigh_tridiagonal(1 / hh**2 - np.exp(-dl * rr) / rr, -0.5 / hh**2 * np.ones(N - 1),
                            select="i", select_range=(0, nev - 1))
    u2 = v[:, 0]**2
    u2 /= u2.sum()
    obs = dict(E=w[0], r=(rr * u2).sum(), r2=(rr**2 * u2).sum(), F=u2[rr <= R / 2].sum())
    if nev > 1:
        obs["E1"] = w[1]
    return obs


def radial_rich(dl, R, h, nev=1):
    a, b = radial(dl, R, h, nev), radial(dl, R, h / 2, nev)
    out = {k: (4 * b[k] - a[k]) / 3 for k in a}
    out["dE"] = abs(a["E"] - b["E"])
    return out


print("=== A. Solucionador radial (DF h y h/2 + Richardson) ===")
for dl, R, h in ((0.2, 60.0, 1 / 40), (1.1, 370.0, 1 / 40)):
    t = tic()
    o = radial_rich(dl, R, h, nev=2)
    dt = tic() - t
    print(f"delta={dl}: R={R:.0f} N={int(R/h)}  E0={o['E']:.8f}  E1={o['E1']:.6f}  <r>={o['r']:.4f}  "
          f"<r^2>^1/2={np.sqrt(o['r2']):.4f}  F_1/2={o['F']:.6f}  |E_h-E_h/2|={o['dE']:.1e}  tiempo={dt:.2f} s")
oA = radial_rich(0.2, 60.0, 1 / 40, nev=2)
E0_02, E1_02 = oA["E"], oA["E1"]

# ----------------------------------------------------------------------------- B. barrido de cajas
# Revision adversarial (ronda 2): con h=1/20 el sesgo de malla es del orden de |E0| cerca del umbral.
# Se resuelve cada (delta,R) con h=1/20, 1/40 y 1/80 y se da Richardson(1/40,1/80) y el control de convergencia en h.
print("\n=== B. Barrido corto de cajas cerca del umbral (h=1/20, 1/40, 1/80; Richardson con 1/40 y 1/80) ===")
t = tic()
nsolve = 0
HB = (1 / 20, 1 / 40, 1 / 80)
for dl in (1.15, 1.18, 1.20, 1.25):
    row = []
    for R in (50.0, 100.0, 200.0, 400.0, 800.0):
        oo = [radial(dl, R, hb) for hb in HB]
        nsolve += 3
        Er = (4 * oo[2]["E"] - oo[1]["E"]) / 3
        rel = abs(oo[2]["E"] - oo[1]["E"]) / abs(oo[2]["E"])
        row.append(f"R={R:4.0f}: E0(1/20)={oo[0]['E']:+.3e} E0(1/80)={oo[2]['E']:+.3e} Rich={Er:+.3e} "
                   f"|dE_h|/|E0|={rel:.2f} <r>/R={oo[2]['r']/R:.3f} F={oo[2]['F']:.3f}")
    print(f"delta={dl}:\n    " + "\n    ".join(row))
    if dl < DC:
        k = 0.7421 * (DC - dl)
        print(f"    ley kappa=0.7421(delta_c-delta) (seccion 7): E0={-k*k/2:+.3e}")
dtB = tic() - t
print(f"Barrido B: {nsolve} autovalores en {dtB:.2f} s ({dtB/nsolve:.3f} s por punto (delta,R,h))")
# umbral efectivo de la red h=1/20: delta tal que la ley kappa da el E0(h=1/20, R=800) de delta=1.18 (estimacion)
E20 = radial(1.18, 800.0, 1 / 20)["E"]
print(f"Umbral efectivo de la red h=1/20 (estimacion por la ley kappa con E0(1.18,R=800,h=1/20)={E20:.3e}): "
      f"{1.18 + np.sqrt(-2 * E20) / 0.7421:.4f}  (delta_c={DC})")

# ----------------------------------------------------------------------------- C. tabla de pares
print("\n=== C. Tabla de la accion de pares de Coulomb en la red ===")
EPS = 0.1
RB, RTAB, BAND = 14.0, 10.0, 2.0     # caja de la tabla, radio tabulado, banda |r-r'|


def pair_table(eps, h, band=None):
    band = BAND if band is None else band
    N = int(round(RB / h)) - 1
    rr = h * np.arange(1, N + 1)
    off = -0.5 / h**2 * np.ones(N - 1)
    wC, vC = eigh_tridiagonal(1 / h**2 - 1 / rr, off)
    w0, v0 = eigh_tridiagonal(np.full(N, 1 / h**2), off)
    nt = int(RTAB / h)
    A = vC[:nt]
    B = v0[:nt]
    rhoC = (A * np.exp(-eps * wC)) @ A.T
    rho0 = (B * np.exp(-eps * w0)) @ B.T
    with np.errstate(divide="ignore", invalid="ignore"):
        U = -np.log(rhoC / rho0)
    inb = np.abs(rr[:nt, None] - rr[None, :nt]) <= band
    U[~inb] = np.nan
    return rr[:nt], U, wC[0]


tabs = {}
for h in (0.01, 0.005):
    t = tic()
    rt, U, e0lat = pair_table(EPS, h)
    tabs[h] = (rt, U)
    print(f"h={h}: N_caja={int(RB/h)}  tabla {len(rt)}x{len(rt)}  E0 Coulomb red={e0lat:.7f}  "
          f"U(diag) en r=0.02,0.1,0.5: {U[1 if h==0.01 else 3,1 if h==0.01 else 3]:.4f} "
          f"{U[int(0.1/h)-1,int(0.1/h)-1]:.4f} {U[int(0.5/h)-1,int(0.5/h)-1]:.4f}  tiempo={tic()-t:.2f} s")
rt1, U1 = tabs[0.01]
rt2, U2 = tabs[0.005]
U2c = U2[1::2, 1::2]                # puntos comunes
m = np.isfinite(U1) & np.isfinite(U2c) & (np.abs(rt1[:, None] - rt1[None, :]) <= 1.0)
print(f"Error de tabulacion max|U(h=0.01)-U(h=0.005)| en |r-r'|<=1: {np.nanmax(np.abs(U1-U2c)[m]):.2e}; "
      f"en la diagonal r>=0.05: {np.nanmax(np.abs(np.diag(U1-U2c))[rt1>=0.05]):.2e}")
# continuidad con la aproximacion de extremos lejos del origen
i9 = int(9.0 / 0.01) - 1
print(f"U_C(9,9) tabla={U1[i9,i9]:.5f} frente a eps*V_C(9)={-EPS/9:.5f}")

# ----------------------------------------------------------------------------- D. proyeccion determinista
print("\n=== D. Proyeccion determinista desde u_T = r e^{-r} (delta=0.2, eps=0.1) ===")
t = tic()
dl = 0.2
h = 0.02
R = 40.0
N = int(round(R / h)) - 1
rr = h * np.arange(1, N + 1)
off = -0.5 / h**2 * np.ones(N - 1)
wC, vC = eigh_tridiagonal(1 / h**2 - 1 / rr, off)
rhoC = (vC * np.exp(-EPS * (wC - wC[0]))) @ vC.T
Wr = (1 - np.exp(-dl * rr)) / rr
g = np.exp(-EPS * Wr / 2)
Tm = g[:, None] * rhoC * g[None, :]
wT, vT = np.linalg.eigh(Tm)
ET = wC[0] - np.log(np.abs(wT[::-1])) / EPS        # "energias" de la matriz de transferencia
uT = rr * np.exp(-rr)
c = vT[:, ::-1].T @ uT
HuT = (Wr - 0.5) * uT                      # H u_T = E_L u_T con E_L = W - 1/2 (cuspide exacta)
cH = vT[:, ::-1].T @ HuT
lam = wT[::-1] / wT[-1]
print(f"E0(eps=0.1, h={h}) de T = {ET[0]:.8f}; E1 = {ET[1]:.6f}; brecha = {ET[1]-ET[0]:.4f}; "
      f"solucionador radial (sec. 5) = -0.32680851")
Elim = cH[0] / c[0]                       # limite tau->inf del estimador mixto: <phi0|H_cont uT>/<phi0|uT>
print(f"E0 Coulomb de la red h={h}: {wC[0]:.8f} (error {wC[0]+0.5:+.1e}); limite del mixto={Elim:.8f}; "
      f"limite - E0(T) = {Elim-ET[0]:+.3e}")
prev = None
for tau in (1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30):
    Mt = int(round(tau / EPS))
    wts = lam**Mt
    Emix = (c * cH * wts).sum() / (c * c * wts).sum()      # <uT|H T^M|uT>/<uT|T^M|uT>
    print(f"  tau={tau:3d}: E_mixto - limite = {Emix-Elim:+.2e}   E_mixto - E0(T) = {Emix-ET[0]:+.2e}")
    if tau == 20: E20m = Emix
    if tau == 30: print(f"  cambio entre tau=20 y 30: {abs(Emix-E20m):.1e}")


def partD(hh_, ee_, dl_=0.2, R_=40.0):
    N_ = int(round(R_ / hh_)) - 1
    r_ = hh_ * np.arange(1, N_ + 1)
    wC_, vC_ = eigh_tridiagonal(1 / hh_**2 - 1 / r_, -0.5 / hh_**2 * np.ones(N_ - 1))
    rho_ = (vC_ * np.exp(-ee_ * (wC_ - wC_[0]))) @ vC_.T
    W_ = (1 - np.exp(-dl_ * r_)) / r_
    g_ = np.exp(-ee_ * W_ / 2)
    w_, v_ = np.linalg.eigh(g_[:, None] * rho_ * g_[None, :])
    E_T = wC_[0] - np.log(w_[-1]) / ee_
    u_ = r_ * np.exp(-r_)
    El_ = (v_[:, -1] @ ((W_ - 0.5) * u_)) / (v_[:, -1] @ u_)
    return wC_[0], E_T, El_


print("  Origen de la diferencia limite - E0(T): variacion con eps y con h")
for hh_ in (0.02, 0.01):
    for ee_ in (0.2, 0.1, 0.05):
        eC_, eT_, eL_ = partD(hh_, ee_)
        print(f"    h={hh_} eps={ee_}: E0 Coulomb red={eC_:.8f}  E0(T)={eT_:.8f}  limite mixto={eL_:.8f}  "
              f"limite-E0(T)={eL_-eT_:+.3e}  E0(T)-radial={eT_+0.326808505:+.2e}  limite-radial={eL_+0.326808505:+.1e}")
print(f"Parte D: {tic()-t:.1f} s")

# ----------------------------------------------------------------------------- E. PIGS radial
print("\n=== E. PIGS radial con Metropolis (r continuo, accion de pares interpolada) ===")


def make_U(rt, U, eps):
    h = rt[1] - rt[0]
    r0 = rt[0]
    n = len(rt)

    def Uf(a, b):
        # interpolacion bilineal; fuera de la tabla, aproximacion de extremos eps/2 (V_C(a)+V_C(b))
        out = -0.5 * eps * (1 / a + 1 / b)
        inside = (a < rt[-1]) & (b < rt[-1])
        x = np.clip((a[inside] - r0) / h, 0, n - 1.000001)
        y = np.clip((b[inside] - r0) / h, 0, n - 1.000001)
        i, j = x.astype(int), y.astype(int)
        fx, fy = x - i, y - j
        v = ((1 - fx) * (1 - fy) * U[i, j] + fx * (1 - fy) * U[i + 1, j]
             + (1 - fx) * fy * U[i, j + 1] + fx * fy * U[i + 1, j + 1])
        out[inside] = v
        return out          # NaN fuera de la banda -> se rechaza
    return Uf


def logKD(a, b, eps):
    return -(a - b)**2 / (2 * eps) + np.log1p(-np.exp(-2 * a * b / eps))


def pigs(dl, tau, eps, nsweep, seed, Uf, L=10, ntherm=500, nscale=4):
    """PIGS radial: movimientos de rebrote por puente browniano (Levy) de L eslabones y de extremos."""
    rng = np.random.default_rng(seed)
    M = int(round(tau / eps)); M -= M % L
    Le = L // 2
    r = 1.0 + 0.1 * rng.random(M + 1)
    W = lambda x: np.where(x > 1e-8, -np.expm1(-dl * x) / np.maximum(x, 1e-300), dl)
    k_in = np.arange(1, L)

    def lres(a, b):      # parte no gaussiana de cada eslabon: imagen, accion de pares, resto W
        return np.log1p(-np.exp(-2 * a * b / eps)) - Uf(a, b) - 0.5 * eps * (W(a) + W(b))

    def seg_logw(P):     # P: (nseg, L+1) caminos de segmento
        v = lres(P[:, :-1].ravel(), P[:, 1:].ravel()).reshape(P.shape[0], -1).sum(1)
        return np.where(np.isfinite(v), v, -np.inf)
    lnuT = lambda x: np.log(x) - x

    def full_logw(P):
        v = (-(np.diff(P)**2).sum() / (2 * eps) + seg_logw(P[None])[0] + lnuT(P[0]) + lnuT(P[-1]))
        return v if np.isfinite(v) else -np.inf
    sc = 0.7 / np.sqrt(M); accs = ntrys = 0
    EL, rmid, r2mid = [], [], []
    acc = ntry = 0
    mid = M // 2
    for sweep in range(ntherm + nsweep):
        for off in (0, Le):
            s = np.arange(off, M - L + 1, L)
            if s.size == 0:
                continue
            a, b = r[s], r[s + L]
            dW = np.sqrt(eps) * rng.standard_normal((s.size, L))
            Wc = np.cumsum(dW, 1)
            B = Wc[:, :-1] - (k_in / L) * Wc[:, -1:]
            newin = a[:, None] + (b - a)[:, None] * (k_in / L) + B
            idx = s[:, None] + np.arange(L + 1)
            Pold = r[idx]
            Pnew = Pold.copy(); Pnew[:, 1:-1] = newin
            ok = (newin > 0).all(1)
            Pn = np.where(ok[:, None], Pnew, Pold)
            dS = seg_logw(Pn) - seg_logw(Pold)
            accept = ok & (np.log(rng.random(s.size)) < dS)
            for j in np.nonzero(accept)[0]:
                r[s[j] + 1: s[j] + L] = newin[j]
            acc += accept.sum(); ntry += s.size
        for end in (0, M):        # extremos: caminata libre desde el bead fijo r[Le] o r[M-Le]
            if end == 0:
                anchor = r[Le]; idx = np.arange(Le, -1, -1)
            else:
                anchor = r[M - Le]; idx = np.arange(M - Le, M + 1)
            newp = anchor + np.concatenate(([0.0], np.cumsum(np.sqrt(eps) * rng.standard_normal(Le))))
            if (newp[1:] <= 0).any():
                ntry += 1; continue
            old = r[idx]
            dS = (seg_logw(newp[None])[0] + lnuT(newp[-1])) - (seg_logw(old[None])[0] + lnuT(old[-1]))
            if np.log(rng.random()) < dS:
                r[idx] = newp; acc += 1
            ntry += 1
        # movimiento global de escala r -> lam r (jacobiano lam^(M+1)); varias veces por barrido
        for _ in range(nscale):
            lam = np.exp(sc * rng.standard_normal())
            new = lam * r
            dS = full_logw(new) - full_logw(r) + (M + 1) * np.log(lam)
            if np.log(rng.random()) < dS:
                r = new; accs += 1
            ntrys += 1
        if sweep >= ntherm:
            EL.append(0.5 * (W(r[0]) + W(r[M])) - 0.5)
            rmid.append(r[mid]); r2mid.append(r[mid]**2)
    return np.array(EL), np.array(rmid), np.array(r2mid), (acc / ntry, accs / max(ntrys, 1))


def blocking(x, nb=40):
    b = x[: len(x) // nb * nb].reshape(nb, -1).mean(1)
    return x.mean(), b.std(ddof=1) / np.sqrt(nb)


def tau_int(x, err):
    v = x.var()
    return 0.5 * err**2 * len(x) / v if v > 0 else 0.0


Uf = make_U(rt1, U1, EPS)
runs = [(0.0, 10.0, 10000, 20261012)] + [(0.2, 20.0, 8000, 20261013 + i) for i in range(8)]


def _run(arg):
    dl, tau, nsw, seed = arg
    t = tic()
    out = pigs(dl, tau, EPS, nsw, seed, Uf)
    return arg, out, tic() - t


import multiprocessing as mp
t = tic()
with mp.get_context("fork").Pool(4) as pool:
    outs = pool.map(_run, runs)
print(f"[{len(runs)} cadenas independientes en 4 procesos: {tic()-t:.1f} s de reloj]")
res02 = []
for (dl, tau, nsw, seed), (EL, rm, r2m, (acc, accs)), dt in outs:
    E, eE = blocking(EL, 20)
    rmean, er = blocking(rm, 20)
    r2, er2 = blocking(r2m, 20)
    M = int(round(tau / EPS))
    print(f"delta={dl} semilla={seed}: tau={tau} M={M} L=10 barridos={nsw}+500 acept. puentes/extremos={acc:.2f} "
          f"escala={accs:.2f} tiempo={dt:.1f} s ({1e3*dt/(nsw+500):.2f} ms/barrido)")
    print(f"    E = {E:.5f} +- {eE:.5f}   <r>_medio = {rmean:.4f} +- {er:.4f}   <r^2>_medio = {r2:.4f} +- {er2:.4f}"
          f"   tau_int(E)~{tau_int(EL, eE):.0f}  tau_int(r)~{tau_int(rm, er):.0f} barridos")
    if dl == 0.0:
        print(f"    exactos: E=-0.5 (prueba exacta, varianza nula), <r>=1.5, <r^2>=3; "
              f"desviaciones {(rmean-1.5)/er:+.1f} y {(r2-3)/er2:+.1f} sigma")
    else:
        res02.append((E, eE, rmean, er, r2, er2, dt, nsw, M))
A = np.array(res02)
n = len(A)
Em, rmm, r2mm = A[:, 0].mean(), A[:, 2].mean(), A[:, 4].mean()
sE, sr, sr2 = A[:, 0].std(ddof=1) / np.sqrt(n), A[:, 2].std(ddof=1) / np.sqrt(n), A[:, 4].std(ddof=1) / np.sqrt(n)
bE, br, br2 = np.sqrt((A[:, 1]**2).sum()) / n, np.sqrt((A[:, 3]**2).sum()) / n, np.sqrt((A[:, 5]**2).sum()) / n
print(f"delta=0.2, {n} semillas combinadas: E={Em:.5f} (err. entre semillas {sE:.5f}, por bloques {bE:.5f}); "
      f"<r>={rmm:.4f} ({sr:.4f}, {br:.4f}); <r^2>={r2mm:.4f} ({sr2:.4f}, {br2:.4f})")
eEc, erc = max(sE, bE), max(sr, br)
print(f"    referencia radial: E0={E0_02:.8f}  <r>={oA['r']:.5f}  <r^2>={oA['r2']:.5f}; desviaciones: "
      f"E {(Em-E0_02)/eEc:+.1f} sigma, <r> {(rmm-oA['r'])/erc:+.1f} sigma, <r^2> {(r2mm-oA['r2'])/max(sr2,br2):+.1f} sigma")
dt1, nsw1, M = A[0, 6], A[0, 7], int(A[0, 8])
eE1, er1 = A[:, 1].mean(), A[:, 3].mean()
ms = dt1 / (nsw1 + 500)
print(f"    error de Trotter+tabla+proyeccion esperado (partes D y F): ~1e-5, menor que el estadistico")
for tgt, e1, nm in ((1e-4, eE1, "E"), (1e-2, er1, "<r>"), (3e-3, er1, "<r>")):
    nb = nsw1 * (e1 / tgt)**2
    print(f"    barridos para error {tgt:.0e} en {nm}: {nb:.2e} (~{nb*ms/60:.1f} min en 1 nucleo)")
fac = (sE / bE)**2
print(f"    factor de subestimacion del error por bloques (entre semillas/bloques)^2 = {fac:.2f}; "
      f"costo corregido para 1e-4 en E: ~{nsw1*(eE1/1e-4)**2*fac*ms/60:.1f} min, para 1e-2 en <r>: "
      f"~{nsw1*(er1/1e-2)**2*(sr/br)**2*ms/60:.1f} min")
cost_sweep_per_bead = ms / (M + 1)
# costo por barrido cerca del umbral (escala lineal en M, autocorrelacion local ~M^2 no incluida)
for dl, E0 in ((1.0, -0.010285784), (1.1, -0.002287239)):
    for nt in (5, 9):            # 9/|E0| es lo que exige 9.4 (seccion 7, L15); 5/|E0| solo como comparacion
        M = nt / abs(E0) / EPS
        print(f"delta={dl}: M={nt}/|E0|/eps={M:.0f}  tiempo por barrido estimado = {M*cost_sweep_per_bead*1e3:.0f} ms")

# ----------------------------------------------------------------------------- F. matriz de transferencia en banda
print("\n=== F. Integral de camino determinista: matriz de transferencia en banda (Nystrom, r continuo) ===")
import scipy.sparse as sps
from scipy.sparse.linalg import eigsh


def band_T(dl, R, h, eps, rt, U, band):
    """T_ij = h K_D(r_i,r_j) e^{-U_C} e^{-eps(W_i+W_j)/2}; U_C de la tabla (r<10) o eps(V_C+V_C)/2 fuera."""
    N = int(round(R / h)) - 1
    rr = h * np.arange(1, N + 1)
    nb = int(round(band / h))
    ht = rt[1] - rt[0]
    step = int(round(h / ht))
    Us = U[step - 1::step, step - 1::step]
    nt = Us.shape[0]
    Wr = -np.expm1(-dl * rr) / rr
    diags, offs = [], []
    for d in range(0, nb + 1):
        a, b = rr[:N - d], rr[d:]
        lk = -(a - b)**2 / (2 * eps) + np.log1p(-np.exp(-2 * a * b / eps)) - 0.5 * np.log(2 * np.pi * eps)
        Uv = -0.5 * eps * (1 / a + 1 / b)
        i = np.arange(N - d)
        m = (i + d) < nt
        Uv[m] = Us[i[m], i[m] + d]
        val = h * np.exp(lk - Uv - 0.5 * eps * (Wr[:N - d] + Wr[d:]))
        val[~np.isfinite(val)] = 0.0
        diags.append(val); offs.append(d)
        if d:
            diags.append(val); offs.append(-d)
    T = sps.diags(diags, offs, shape=(N, N), format="csr")
    lam, v = eigsh(T, k=1, which="LA")
    u2 = v[:, 0]**2
    u2 /= u2.sum()
    return -np.log(lam[0]) / eps, (rr * u2).sum(), u2[rr <= R / 2].sum()


ref = {0.0: (-0.5, 1.5), 0.2: (-0.326808505, 1.54972), 1.0: (-0.010285784, 4.36670), 1.1: (-0.002287239, 8.27764)}
Rd = {0.0: 40.0, 0.2: 40.0, 1.0: 174.0, 1.1: 370.0}
for dl in (0.0, 0.2, 1.0, 1.1):
    t = tic()
    Ea, ra, Fa = band_T(dl, Rd[dl], 0.02, EPS, rt1, U1, BAND)
    Eb, rb, Fb = band_T(dl, Rd[dl], 0.02, EPS, rt2, U2, BAND)
    Er, rR = (4 * Eb - Ea) / 3, (4 * rb - ra) / 3
    print(f"delta={dl}: R={Rd[dl]:.0f} N={int(Rd[dl]/0.02)}  E(tabla h=0.01)={Ea:.8f}  E(tabla h=0.005)={Eb:.8f}  "
          f"Richardson={Er:.8f}  ref={ref[dl][0]:.8f}  dif={Er-ref[dl][0]:+.1e}  <r>={rR:.5f} (ref {ref[dl][1]})  "
          f"F_1/2={Fb:.4f}  tiempo={tic()-t:.1f} s")
# ley eps^2 en delta=1.0 (tablas h=0.01 y 0.005 con Richardson para cada eps)
t = tic()
dl = 1.0
res = []
for ee in (0.2, 0.1, 0.05):
    bd = max(BAND, 7 * np.sqrt(ee))
    ra_, Ua_, _ = pair_table(ee, 0.01, bd)
    rb_, Ub_, _ = pair_table(ee, 0.005, bd)
    Ea = band_T(dl, 174.0, 0.02, ee, ra_, Ua_, bd)[0]
    Eb = band_T(dl, 174.0, 0.02, ee, rb_, Ub_, bd)[0]
    res.append((4 * Eb - Ea) / 3)
res = np.array(res)
sl = np.log(abs(res[0] - res[1]) / abs(res[1] - res[2])) / np.log(2)
Eext = res[2] + (res[2] - res[1]) / 3
print(f"delta=1.0, eps=0.2,0.1,0.05: E={res[0]:.8f} {res[1]:.8f} {res[2]:.8f}; orden aparente={sl:.2f}; "
      f"extrapolado eps->0={Eext:.8f} (ref -0.01028578, dif {Eext+0.010285784:+.1e}); tiempo={tic()-t:.1f} s")

# ----------------------------------------------------------------------------- G. puntos junto al umbral
print("\n=== G. Escalas junto al umbral (ley kappa de la seccion 7 y longitud de dispersion) ===")
from scipy.integrate import solve_ivp
for dl in (1.185, 1.19):
    k = 0.741 * (DC - dl)
    print(f"delta={dl}: kappa~0.741(delta_c-delta)={k:.5f}  <r>~1/(2 kappa)={1/(2*k):.0f}")


def a_sc(dl, rmax=200.0):
    f = lambda r, y: [y[1], -2 * np.exp(-dl * r) / r * y[0]]
    r0 = 1e-8
    sol = solve_ivp(f, (r0, rmax), [r0, 1.0 - r0], rtol=1e-11, atol=1e-14)
    u, up = sol.y[0, -1], sol.y[1, -1]
    return rmax - u / up


for dl in (1.195, 1.20, 1.25):
    print(f"delta={dl}: longitud de dispersion a_sc (E=0, r_max=200) = {a_sc(dl):.1f}")
print(f"\nCarga al terminar (loadavg): {os.getloadavg()}")
print(f"\nTiempo total: {tic()-T0:.1f} s")
