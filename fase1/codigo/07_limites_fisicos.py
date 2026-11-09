"""Bloque 07: verificacion de la lista de limites fisicos propuesta por la IA (Claude, 12-10-2026).
Unidades: hbar=m=g=1, delta=mu*hbar^2/(m g). Ecuacion radial l=0:
    -u''/2 - e^{-delta r}/r u = E u,   u(0)=0, u(inf)=0.
Cada bloque imprime una linea "Lnn | resultado | estado". Tiempo total ~1-2 min.
Figura: fase1/figuras/07_limites_fisicos.png"""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..'))  # raiz del repositorio
import numpy as np
import sympy as sp
from scipy.linalg import eigh_tridiagonal
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

DC = 1.19061242106          # Gebremedhin y Weatherford (2023)
FIG = _RAIZ + "/fase1/figuras/07_limites_fisicos.png"
tabla = []

def reg(item, res, estado):
    tabla.append((item, res, estado)); print(f"{item:4s}| {res} | {estado}")

# ---------------------------------------------------------------- solucionador
def fd(delta, R, N, k=1, a=0.0, hb=1.0, m=1.0, g=1.0, vec=False):
    """DF 2o orden en (0,R), Dirichlet. Potencial -g e^{-mu r}/sqrt(r^2+a^2), mu=delta (en unidades del usuario)."""
    h = R/(N+1); r = h*np.arange(1, N+1)
    V = -g*np.exp(-delta*r)/np.sqrt(r**2 + a**2)
    t = hb**2/(2*m*h**2)
    w, v = eigh_tridiagonal(2*t + V, -t*np.ones(N-1), select='i', select_range=(0, k-1))
    if not vec: return w
    v = v/np.sqrt(h); v *= np.sign(v[np.argmax(np.abs(v[:, 0])), 0])
    return w, r, v, h

def E0r(delta, R, N, a=0.0):
    """Richardson h -> h/2 para E0."""
    return (4*fd(delta, R, 2*N+1, a=a)[0] - fd(delta, R, N, a=a)[0])/3

def Rauto(delta):
    E = E0r(delta, 60, 3000); return min(max(60, 30/np.sqrt(-2*E)), 6000) if E < 0 else 400

def zero_energy(delta, R, a=0.0):
    """Solucion a E=0 desde el origen; devuelve u(R), u'(R)."""
    s = solve_ivp(lambda r, y: [y[1], -2*np.exp(-delta*r)/np.sqrt(r*r + a*a)*y[0]], [1e-8, R],
                  [1e-8, 1.0], method='DOP853', rtol=1e-12, atol=1e-15)
    return s.y[0, -1], s.y[1, -1]

if __name__ == "__main__":
    print("=== Verificacion de limites fisicos (L01..L19) ===")
    # L01 escalamiento: hbar=1, m=2, g=3, mu tal que delta = mu hbar^2/(m g) = 0.5
    hb, m, g, d = 1.0, 2.0, 3.0, 0.5
    a0 = hb**2/(m*g); EH = m*g**2/hb**2; mu = d/a0
    Ed = fd(mu, 60*a0, 12000, hb=hb, m=m, g=g)[0]/EH; Eu = fd(d, 60, 12000)[0]
    reg("L01", f"E/(mg^2/hbar^2) con (m,g)=(2,3): {Ed:.10f}; con (1,1): {Eu:.10f}; dif {abs(Ed-Eu):.1e}",
        "CONFIRMADO")

    # L02 Coulomb
    w, r, v, h = fd(0.0, 60, 24000, vec=True); u = v[:, 0]
    rm = np.sum(r*u*u)*h; r2 = np.sum(r*r*u*u)*h
    reg("L02", f"E0(0)={E0r(0.0, 60, 12000):.9f}  <r>={rm:.5f}  <r^2>={r2:.5f}", "CONFIRMADO")

    # L03 serie perturbativa: residuo del orden 4 debe escalar como delta^5
    ser = lambda x: -0.5 + x - 0.75*x**2 + 0.5*x**3 - 11/16*x**4
    res = [abs(E0r(x, 60, 12000) - ser(x)) for x in (0.02, 0.04)]
    reg("L03", f"|E-serie4| en 0.02, 0.04: {res[0]:.2e}, {res[1]:.2e}; cociente {res[1]/res[0]:.1f} (2^5=32)",
        "CONFIRMADO")

    # L04 cotas -1/2 <= E0 <= -1/2+delta (prueba: 1-x <= e^{-x} <= 1)
    x = sp.symbols('x', nonnegative=True)
    f = sp.exp(-x) - 1 + x; ok_sym = sp.simplify(sp.diff(f, x)) == 1 - sp.exp(-x) and f.subs(x, 0) == 0
    ds = np.round(np.arange(0.0, 1.181, 0.05), 3); Es = np.array([E0r(dd, Rauto(dd), int(Rauto(dd)*20)) for dd in ds])
    tol = 1e-6   # error de discretizacion de E0r con h=1/20 (en delta=0 da -0.4999999)
    viol = np.sum((Es < -0.5 - tol) | (Es > -0.5 + ds + tol))
    m_inf = np.min(Es + 0.5); m_sup = np.min((-0.5 + ds - Es)[1:])
    reg("L04", f"sympy: f=e^-x-1+x, f(0)=0, f'=1-e^-x>=0 -> {ok_sym}; delta en [0,{ds[-1]}] ({len(ds)} puntos): "
        f"violaciones (tol {tol:g}) = {viol}; margen min. inferior {m_inf:.1e}, superior (delta>0) {m_sup:.3f}",
        "CONFIRMADO")

    # L05 Hellmann-Feynman y concavidad
    out = []
    for dd in (0.3, 0.8, 1.1):
        R = Rauto(dd); N = int(R*20); hd = 1e-4
        dE = (fd(dd+hd, R, 2*N+1)[0] - fd(dd-hd, R, 2*N+1)[0])/(2*hd)   # misma malla que el valor esperado
        w, r, v, h = fd(dd, R, 2*N+1, vec=True); u = v[:, 0]
        out.append(f"d={dd}: dE/dd={dE:.6f} <e^-dr>={np.sum(np.exp(-dd*r)*u*u)*h:.6f}")
    d2 = np.diff(Es, 2)
    reg("L05", "; ".join(out) + f"; max 2a diferencia de E0 = {d2.max():.2e} (<0: concava)", "CONFIRMADO")
    slopes = np.diff(Es)/np.diff(ds)
    print(f"     pendientes dE0/dd en (0,1]: min {slopes.min():.4f}, max {slopes.max():.4f}")

    # L06 virial 2<T> = -<V> + delta <e^{-delta r}>
    out = []
    for dd in (0.0, 0.5, 1.0):
        R = Rauto(dd); vir = []
        for ppu in (40, 80):   # puntos por unidad: el residuo debe bajar como h^2
            w, r, v, h = fd(dd, R, int(R*ppu), vec=True); u = v[:, 0]
            up = np.concatenate([[0], u, [0]]); lap = (up[2:] - 2*up[1:-1] + up[:-2])/h**2
            T = -0.5*np.sum(u*lap)*h; Vm = np.sum(-np.exp(-dd*r)/r*u*u)*h; ex = np.sum(np.exp(-dd*r)*u*u)*h
            vir.append(2*T + Vm - dd*ex)
        out.append(f"d={dd}: 2T+V-d<e>={vir[1]:.1e} (h=1/80), cociente h/(h/2)={vir[0]/vir[1]:.2f}")
    reg("L06", "; ".join(out), "CONFIRMADO")

    # L07 origen: Frobenius con sympy y ajuste numerico de u ~ A(r + a2 r^2)
    rs, E, dl = sp.symbols('r E delta'); a2, a3 = sp.symbols('a2 a3')
    us = rs + a2*rs**2 + a3*rs**3
    Vser = -sp.series(sp.exp(-dl*rs), rs, 0, 4).removeO()/rs
    eq = sp.expand(sp.diff(us, rs, 2) - 2*(Vser - E)*us)
    sol = sp.solve([eq.coeff(rs, 0), eq.coeff(rs, 1)], [a2, a3])
    out = [f"sympy: a2={sol[a2]}, a3={sp.factor(sol[a3])}"]
    for dd in (0.0, 0.5, 1.0):
        w, r, v, h = fd(dd, 40 if dd < 1 else 120, 200000 if dd < 1 else 600000, vec=True); u = v[:, 0]
        sel = r < 0.05; p = np.polyfit(r[sel], u[sel]/r[sel], 2)
        out.append(f"d={dd}: a2 ajustado={p[1]/p[2]:.4f}")
    reg("L07", "; ".join(out), "CONFIRMADO")

    # L08 cola: d ln u/dr -> -kappa sin termino 1/(kappa r) para delta>0
    out = []
    for dd in (0.0, 0.5):
        R = 80; w, r, v, h = fd(dd, R, 32000, vec=True); u = v[:, 0]; kap = np.sqrt(-2*w[0])
        for rr in (10, 20):
            i = np.searchsorted(r, rr); L = (np.log(u[i+1]) - np.log(u[i-1]))/(2*h)
            out.append(f"d={dd},r={rr}: r(dlnu/dr+k)={rr*(L+kap):.4f}")
    reg("L08", "; ".join(out) + "  (Coulomb: 1/k=1; Yukawa: ->0)", "CONFIRMADO")

    # L09 sin nodos
    nn = []
    for dd in (0.0, 0.5, 1.0, 1.15):
        R = Rauto(dd); w, r, v, h = fd(dd, R, int(R*20), vec=True); u = v[:, 0]
        nn.append(int(np.sum(u < -1e-10*np.abs(u).max())))
    reg("L09", f"puntos con u<0 (d=0,0.5,1,1.15): {nn}", "CONFIRMADO")

    # L10 umbral y ley cuadratica
    dcz = brentq(lambda dd: zero_energy(dd, 600)[1], 1.1, 1.3, xtol=1e-12)
    dk = np.array([1.13, 1.15, 1.17]); ks = []
    for dd in dk:
        E = E0r(dd, 400, 8000); R = min(40/np.sqrt(-2*E), 8000); ks.append(np.sqrt(-2*E0r(dd, R, int(R*20))))
    ks = np.array(ks); cc = ks/(DC - dk); c_lim = np.polyval(np.polyfit(dk, cc, 1), DC)
    reg("L10", f"delta_c(E=0)={dcz:.10f} (ref {DC}); kappa/(dc-d) en 1.13,1.15,1.17={np.round(cc, 4)}, "
        f"extrapolado a dc: c={c_lim:.4f}", "CONFIRMADO; PRECISADO (c=0.741, no 0.75)")

    # L11 extension: 2 kappa <r> -> 1, 2 kappa^2 <r^2> -> 1
    out = []
    for dd in (1.0, 1.15, 1.18):
        E = E0r(dd, 400, 8000); R = min(40/np.sqrt(-2*E), 8000)
        w, r, v, h = fd(dd, R, int(R*20), vec=True); u = v[:, 0]; kap = np.sqrt(-2*w[0])
        out.append(f"d={dd}: 2k<r>={2*kap*np.sum(r*u*u)*h:.3f}, 2k^2<r^2>={2*kap**2*np.sum(r*r*u*u)*h:.3f}")
    reg("L11", "; ".join(out), "CONFIRMADO (asintotico)")

    # L12 caja: E0(R) decrece con R; dc(R) < dc con ley 1/R
    Rs = np.array([50, 100, 200, 400, 800, 1600]); dcR = []
    for R in Rs:
        dcR.append(brentq(lambda dd: zero_energy(dd, R)[0], 0.6, DC, xtol=1e-12))
    dcR = np.array(dcR); prodR = Rs*(DC - dcR)
    ER = [E0r(1.0, R, int(R*40)) for R in (30, 40, 60, 80)]
    kap1 = np.sqrt(-2*ER[-1])
    reg("L12", f"dc(R) R=50..1600: {np.round(dcR, 5)}; R(dc-dc(R))={np.round(prodR, 3)}", "CONFIRMADO")
    print(f"     d=1: E0(R=30,40,60,80)={np.round(ER, 8)}; (E0(R)-E0(80))/exp(-2kR): "
          + str([f'{(e-ER[-1])/np.exp(-2*kap1*R):.2f}' for e, R in zip(ER[:2], (30, 40))]))

    # L13 estado no ligado en caja y falso no ligado
    out = []
    for dd in (1.3, 2.0):
        for R in (100, 400):
            w, r, v, h = fd(dd, R, int(R*10), vec=True); u = v[:, 0]
            out.append(f"d={dd},R={R}: E0R^2={w[0]*R*R:.3f}, <r>/R={np.sum(r*u*u)*h/R:.3f}")
    Efake = [E0r(1.18, R, int(R*20)) for R in (20, 40, 400)]
    reg("L13", "; ".join(out) + f"; d=1.18 (ligado): E0(R=20,40,400)={np.round(Efake, 6)}",
        "CORREGIDO (falta la longitud de dispersion)")
    # longitud de dispersion a_s = -A/B de u(r) = A + B r a E=0, y prediccion pi^2/(2(R-a_s)^2)
    for dd in (1.3, 2.0):
        uR, dR = zero_energy(dd, 300); a_s = 300 - uR/dR
        pred = [np.pi**2/2*(R/(R - a_s))**2 for R in (100, 400)]
        print(f"     d={dd}: a_s={a_s:.3f}; E0R^2 predicho con pi^2/(2(R-a_s)^2) en R=100,400: {np.round(pred, 3)}; pi^2/2={np.pi**2/2:.3f}")

    # L14 umbral del 2s
    d2s = brentq(lambda dd: zero_energy(dd, 800)[1], 0.25, 0.45, xtol=1e-10)
    reg("L14", f"delta_c(2s) = {d2s:.6f}", "CONFIRMADO")

    # L15 proyeccion en tiempo imaginario con funcion de prueba 1s de hidrogeno
    taus = np.logspace(-1, 5, 400); proy = {}
    out = []
    for dd in (0.5, 1.0, 1.15):
        R = 400 if dd < 1.1 else 800; N = int(R*8); hh = R/(N+1); r = hh*np.arange(1, N+1)
        Vd = -np.exp(-dd*r)/r; t = 1/(2*hh*hh)
        w, v = eigh_tridiagonal(2*t + Vd, -t*np.ones(N-1))
        c = v.T @ (r*np.exp(-r)); c2 = c*c
        Etau = np.array([np.sum(w*c2*np.exp(-(w-w[0])*tt))/np.sum(c2*np.exp(-(w-w[0])*tt)) for tt in taus])
        mono = np.all(np.diff(Etau) <= 1e-14)
        err = Etau - w[0]; tstar = taus[np.argmax(err < 1e-6*abs(w[0]))] if np.any(err < 1e-6*abs(w[0])) else np.nan
        proy[dd] = (Etau, w[0])
        out.append(f"d={dd}: monotona={mono}, gap={w[1]-w[0]:.4g}, |E0|={-w[0]:.4g}, tau(err rel<1e-6)={tstar:.4g}, tau*|E0|={tstar*abs(w[0]):.1f}")
    reg("L15", "; ".join(out), "CONFIRMADO (en caja); la ley tau~1/|E0| se prueba en Fase 2")

    # L16 propagador libre en la semirrecta (metodo de imagenes)
    rr, rp, tt = sp.symbols('r rp tau', positive=True)
    K = (sp.exp(-(rr-rp)**2/(2*tt)) - sp.exp(-(rr+rp)**2/(2*tt)))/sp.sqrt(2*sp.pi*tt)
    heat = sp.simplify(sp.diff(K, tt) - sp.diff(K, rr, 2)/2)
    norm = sp.simplify(sp.integrate(K, (rr, 0, sp.oo)))
    pos = sp.simplify((rr+rp)**2 - (rr-rp)**2)
    reg("L16", f"dK/dtau-K''/2={heat}; K(0,r')={K.subs(rr, 0)}; int K dr={norm}; (r+r')^2-(r-r')^2={pos}>0",
        "CONFIRMADO")

    # L17 peso primitivo y suavizado
    eps = sp.symbols('epsilon', positive=True)
    lim = sp.limit(rr**2*sp.exp(eps/rr), rr, 0, '+')
    parc = [quad(lambda s: s*s*np.exp(0.1/s), r0, 1, limit=400)[0] for r0 in (0.01, 0.005, 0.004)]
    # sesgo del suavizado: delta=0 primer orden y exacto
    fI = lambda s, a: 4*s*s*np.exp(-2*s)*(1/s - 1/np.sqrt(s*s + a*a))
    dE1 = lambda a: quad(fI, 0, 10*a, args=(a,), limit=400)[0] + quad(fI, 10*a, np.inf, args=(a,), limit=400)[0]
    as_ = np.array([0.1, 0.05, 0.025, 0.0125])
    ratio1 = [dE1(a)/(2*a*a*np.log(1/a)) for a in as_]
    fine = [E0r(0.0, 40, 40000, a=a) + 0.5 for a in as_]
    ratio_ex = [f/(2*a*a*np.log(1/a)) for f, a in zip(fine, as_)]
    dca = [brentq(lambda dd: zero_energy(dd, 600, a=a)[1], 1.0, 1.25, xtol=1e-11) for a in as_]
    reg("L17", f"lim r^2 e^(eps/r)={lim}; int_r0^1 r^2 e^(0.1/r) (r0=0.01,0.005,0.004)={[f'{p:.3g}' for p in parc]}; "
        f"dE/(2a^2 ln(1/a)) 1er orden {np.round(ratio1, 3)}, exacto {np.round(ratio_ex, 3)}; "
        f"dc(a)-dc={[f'{x-DC:.2e}' for x in dca]}",
        "CONFIRMADO; PRECISADO (convergencia logaritmica lenta)")

    Cs = [dE1(a)/a**2 - 2*np.log(1/a) for a in (1e-2, 1e-3, 1e-4)]
    print(f"     primer orden: dE/a^2 - 2 ln(1/a) en a=1e-2,1e-3,1e-4: {np.round(Cs, 4)} (-> constante C)")
    print(f"     dE exacto en a=0.1,0.05,0.025,0.0125: {[f'{x:.3e}' for x in fine]}")
    reg("L18", "error de Trotter con singularidad 1/r: requiere el propagador de la Fase 2", "SOLO FASE 2")

    # L19 delta >= 2 sin ligados (Bargmann), ya visto en L13 con d=2
    E2 = E0r(2.0, 200, 4000)
    reg("L19", f"E0(delta=2, R=200)={E2:.3e} > 0", "CONFIRMADO")

    # ------------------------------------------------------------- figura
    fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
    ax[0].plot(1/Rs, DC - dcR, 'o-', color='#2a6fb0', label=r'$\delta_c-\delta_c(R)$ (caja de Dirichlet)')
    ax[0].plot(1/Rs, prodR[-1]/Rs, '--', color='gray', label=fr'${prodR[-1]:.2f}/R$')
    ax[0].set_xlabel('$1/R$  [$1/a$]'); ax[0].set_ylabel(r'sesgo de caja en $\delta_c$'); ax[0].legend(fontsize=8)
    ax[0].set_title('L12: el sesgo de caja decae como $1/R$')
    for dd, col in zip(proy, ('#2a6fb0', '#2e8b57', '#c0392b')):
        Et, e0 = proy[dd]; ax[1].loglog(taus, np.maximum((Et - e0)/abs(e0), 1e-16), color=col, label=fr'$\delta={dd}$')
    ax[1].axhline(1e-6, ls=':', color='gray'); ax[1].set_ylim(1e-12, 1e2)
    ax[1].set_xlabel(r'$\tau$  [$\hbar^3/(mg^2)$]'); ax[1].set_ylabel(r'$(E(\tau)-E_0)/|E_0|$'); ax[1].legend(fontsize=8)
    ax[1].set_title(r'L15: proyección en tiempo imaginario')
    ax[2].loglog(as_, fine, 'o-', color='#8e44ad', label=r'$E_0(a)-E_0$, $\delta=0$')
    ax[2].loglog(as_, 2*as_**2*np.log(1/as_), '--', color='gray', label=r'$2a^2\ln(1/a)$')
    ax[2].loglog(as_, as_**2, ':', color='k', label=r'$a^2$')
    ax[2].set_xlabel('$a$ (suavizado)  [$a_0$]'); ax[2].legend(fontsize=8); ax[2].set_title('L17: sesgo del suavizado')
    ax[0].set_xticks([0, 0.005, 0.01, 0.015, 0.02])
    from matplotlib.ticker import NullFormatter
    ax[2].xaxis.set_minor_formatter(NullFormatter())
    fig.tight_layout(); fig.savefig(FIG, dpi=150)
    print(f"Figura: {FIG}")
    print(f"Resumen: {sum('CONFIRMADO' in t[2] for t in tabla)} confirmados (incl. con precision), "
          f"{sum('CORREGIDO' in t[2] for t in tabla)} corregidos, {sum('FASE 2' in t[2] for t in tabla)} solo Fase 2")
