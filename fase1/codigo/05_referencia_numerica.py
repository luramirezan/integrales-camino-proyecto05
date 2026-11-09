"""Bloque 05: referencia numerica independiente del umbral delta_c (Yukawa, l=0).
Unidades: hbar=m=g=1. Ecuacion: -u''/2 - e^{-delta r}/r u = E u, u(0)=0.
Metodos: (A) diferencias finitas + Richardson; (B) Numerov con disparo (log-malla);
(C) condicion de umbral a energia cero (solve_ivp, u'(inf)=0); (D) extrapolacion k(delta)->0."""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..'))  # raiz del repositorio
import numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
DC_LIT = 1.19061242106  # Gebremedhin y Weatherford 2023, tomado de arXiv:2510.10420 (tabla II); no verificado en la fuente primaria
OUT = _RAIZ + "/fase1/figuras/05_E0_r_vs_delta.png"

def fd(delta, R, N):
    """Diferencias finitas de 2o orden; devuelve E0, <r>."""
    h = R/(N+1); r = h*np.arange(1, N+1)
    d = 1/h**2 - np.exp(-delta*r)/r
    e = -0.5/h**2*np.ones(N-1)
    w, v = eigh_tridiagonal(d, e, select='i', select_range=(0, 0))
    u = v[:, 0]; return w[0], np.sum(r*u**2)/np.sum(u**2)

def fd_rich(delta, R, N):
    """Richardson h->h/2 (error O(h^2)): E = (4E_{h/2}-E_h)/3."""
    E1, r1 = fd(delta, R, N); E2, r2 = fd(delta, R, 2*N+1)
    return (4*E2-E1)/3, (4*r2-r1)/3, abs(E2-E1)

def numerov_E(delta, R=None, n=40000):
    """Numerov con disparo en malla x=ln r, u=sqrt(r) y. Biseccion sobre E."""
    def miss(E):
        x = np.linspace(np.log(1e-6), np.log(R), n); hx = x[1]-x[0]; r = np.exp(x)
        # y'' = f y,  f = 1/4 + r^2 * 2(V - E)
        f = 0.25 + 2*r**2*(-np.exp(-delta*r)/r - E)
        y = np.zeros(n); y[0] = r[0]**0.5*(1-r[0]); y[1] = r[1]**0.5*(1-r[1])  # u~r(1-r)
        c = 1 - hx**2*f/12
        for i in range(1, n-1):
            y[i+1] = ((12-10*c[i])*y[i] - c[i-1]*y[i-1])/c[i+1]
            if abs(y[i+1]) > 1e200: y[:i+2] *= 1e-200
        return y[-1]
    return miss

def numerov(delta, Eguess, R):
    m = numerov_E(delta, R)
    a, b = Eguess*1.02, Eguess*0.98
    # bracket
    Es = np.linspace(Eguess*1.2, min(Eguess*0.8, -1e-12), 25); vals = [m(E) for E in Es]
    for i in range(len(Es)-1):
        if np.sign(vals[i]) != np.sign(vals[i+1]):
            return brentq(m, Es[i], Es[i+1], xtol=1e-14)
    raise RuntimeError

def slope_inf(delta, R):
    """Energia cero: u''=-2 e^{-dr}/r u. Para r>>1/d, u=A+B r; umbral <=> B=0."""
    s = solve_ivp(lambda r, y: [y[1], -2*np.exp(-delta*r)/r*y[0]], [1e-8, R],
                  [1e-8, 1.0], method='DOP853', rtol=1e-13, atol=1e-16)
    return s.y[1, -1]

if __name__ == "__main__":
    print("== (A) Validacion Coulomb y tabla FD+Richardson ==")
    tabla = []
    for d in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.1]:
        E0 = fd_rich(d, 60, 8000)[0]
        R = min(max(60, 25/np.sqrt(-2*E0)), 6000)
        E, rm, err = fd_rich(d, R, int(R*40))
        tabla.append((d, R, int(R*40), E, rm, err)); print(f"d={d:.2f} R={R:.0f} N={int(R*40)} E0={E:.9f} <r>={rm:.5f} |E_h-E_h/2|={err:.1e}")
    print("== (B) Numerov disparo ==")
    for d in [0.0, 0.5, 1.0]:
        Ef = [t[3] for t in tabla if abs(t[0]-d) < 1e-9] or [fd_rich(d, 80, 4000)[0]]
        R = max(40, 30/np.sqrt(-2*Ef[0])); En = numerov(d, Ef[0], R)
        print(f"d={d} E_numerov={En:.10f}  E_FD={Ef[0]:.10f}  diff={abs(En-Ef[0]):.1e}")
    print("== (C) Umbral a energia cero ==")
    for R in [200, 400, 800]:
        dc = brentq(lambda d: slope_inf(d, R), 1.1, 1.3, xtol=1e-13)
        print(f"R={R}: delta_c={dc:.10f}  diff lit={dc-DC_LIT:.1e}")
    print("== (D) Extrapolacion k=sqrt(-2E0) -> 0 ==")
    ds = np.linspace(1.05, 1.15, 11); ks = []
    for d in ds:
        E0 = fd_rich(d, 400, 16000)[0]; R = min(40/np.sqrt(-2*E0), 8000)
        E = fd_rich(d, R, int(R*20))[0]; ks.append(np.sqrt(-2*E))
    ks = np.array(ks)
    for deg in [2, 3]:
        p = np.polyfit(ds, ks, deg); roots = [x.real for x in np.roots(p) if abs(x.imag) < 1e-12 and 1.15 < x.real < 1.3]
        print(f"grado {deg}: delta_c={roots[0]:.7f} diff={roots[0]-DC_LIT:.1e}")
    for d, k in zip(ds, ks): print(f"  d={d:.3f} k={k:.7f} E0={-k*k/2:.9f}")
    # Figura
    dd = np.concatenate([np.linspace(0, 1.0, 21), np.linspace(1.02, 1.17, 9)]); Es, rs = [], []
    for d in dd:
        E0 = fd_rich(d, 300, 12000)[0]; R = min(max(60, 30/np.sqrt(-2*E0)), 8000)
        E, rm, _ = fd_rich(d, R, int(R*15)); Es.append(E); rs.append(rm)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].plot(dd, Es, 'o-', ms=3, color='#2a6fb0', label='$E_0(\\delta)$ (DF+Richardson)')
    for x, lab, c in [(1, 'cota inferior $\\delta=1$', '#2e8b57'), (2, 'cota superior $\\delta=2$', '#c0392b'), (DC_LIT, '$\\delta_c=1.1906$', 'k')]:
        ax[0].axvline(x, ls='--', color=c, lw=1, label=lab); ax[1].axvline(x, ls='--', color=c, lw=1)
    ax[0].axhline(0, color='gray', lw=.6); ax[0].set_xlabel('$\\delta=\\mu a$'); ax[0].set_ylabel('$E_0$  [$mg^2/\\hbar^2$]'); ax[0].legend(fontsize=8); ax[0].set_xlim(0, 2.1)
    ax[1].semilogy(dd, rs, 'o-', ms=3, color='#8e44ad'); ax[1].set_xlabel('$\\delta$'); ax[1].set_ylabel('$\\langle r\\rangle$  [$a$]'); ax[1].set_xlim(0, 2.1)
    ax[0].set_title('Energía del estado base'); ax[1].set_title('Tamaño medio $\\langle r\\rangle$ (diverge en $\\delta_c$)')
    fig.tight_layout(); fig.savefig(OUT, dpi=150)
    for d, E, r in zip(dd[-6:], Es[-6:], rs[-6:]): print(f"fig d={d:.3f} E0={E:.8f} <r>={r:.3f}")
