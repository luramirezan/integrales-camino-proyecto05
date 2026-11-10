# Material para auditoría (parte 1 de 3)

Responde solo "Recibido" hasta la parte 3, que trae el encargo.

## Contexto

Proyecto de física teórica (curso de investigación, universidad). Estado ligado 1s del potencial de Yukawa V(r) = −g e^{−μr}/r. En unidades ħ = m = g = 1, V = −e^{−δr}/r con δ = μħ²/(mg). Ecuación radial −u''/2 + V u = E u, u(0) = u(R) = 0 (caja esférica de radio R, Dirichlet). Pregunta: ¿en qué δ_c deja de existir el estado ligado? Valor de referencia del grupo (integración a energía cero, código propio): δ_c = 1.1906124211.

Cerca del umbral el estado se extiende (tamaño ~1/κ, κ = √(−2E0)), y una caja finita puede inventar o esconder el estado ligado. Por eso el veredicto ligado / no ligado se toma con un **criterio de cajas** sobre ternas consecutivas de R (R1 < R2 < R3):

- **Ligado:** (a) E(R2) y E(R3) negativas con |E| mayor que su error, y |E(R3) − E(R2)| < 0.1 |E(R3)|; (a') error de malla < 10 % de |E| en las tres; (b) ⟨r⟩/R decreciente, F_1/2 (fracción de densidad en r < R/2) creciente y F_1/2(R3) > 0.95.
- **No ligado:** E > 0 en las tres (con |E| mayor que el error), ⟨r⟩/R creciente, F_1/2 decreciente y la ley de caja de un estado libre con longitud de dispersión a_s: desviación relativa de π²/[2(R − a_s)²] menor que 0.1 en R3 y decreciente en la terna. El umbral 0.1 se fijó antes de calcular estos datos.
- **(c):** dos métodos independientes deben dar el mismo signo y la misma tendencia en las mismas cajas: un solucionador radial (diferencias finitas, h = 1/40 y 1/80 con Richardson p = 2) y una integral de camino en tiempo imaginario evaluada como matriz de transferencia.

**Integral de camino.** Eslabón T(r, r'; ε) = K_D · e^{−U_C} · e^{−ε[W(r)+W(r')]/2}, con K_D el núcleo libre con imagen en r = 0, U_C la acción de pares EXACTA de Coulomb (tabulada) y W = (1 − e^{−δr})/r ∈ [0, δ] el resto acotado. E0(ε) = −ln λ0 / ε, con λ0 el mayor autovalor de la matriz de Nyström h·T(r_i, r_j) en r_i = ih. Extrapolación: Richardson en h con exponente 4 (h = 0.02, 0.04) y ley ε² con ε = 0.1, 0.05. **La pared en R no tiene imagen**: la caja efectiva es R + 0.5826√ε (0.5826 = −ζ(1/2)/√(2π)). Ese efecto NO se corrige en el núcleo: se estima con el radial en R + 0.5826√ε y se suma a la barra de error.

## Código común (comun3.py)

```python
"""comun3.py -- utilidades de la Fase 3 (proyecto 05, Yukawa). Reutiliza los modulos probados de la Fase 2
(fase2/codigo: radial.py, pares.py, transferencia.py) sin modificarlos.

Unidades hbar = m = g = 1, V = -e^{-delta r}/r.

Receta de la integral de camino (la misma de 14_criterio_cajas.py de la Fase 2, decision 1 y 5 aprobadas):
  - transferencia en banda con la accion de pares de Coulomb (tablas U_C con Richardson h_tab 0.01/0.005);
  - Richardson en h con exponente 4: E_hR = (16 E_0.02 - E_0.04)/15  (decision 1);
  - extrapolacion eps -> 0 con ley eps^2: E_ext = E(0.05) + [E(0.05) - E(0.1)]/3;
  - error = |E_ext(h=0.02) - E_ext(hR)| + |E_ext(0.1,0.05) - E_ext(0.2,0.1)| + |sesgo de pared extrapolado|,
    con el sesgo de la pared en R sin imagen estimado con el radial en R + 0.5826 sqrt(eps)
    (decision 5: SOLO termino en el error; el nucleo no se cambia).
Autovalor: eigsh shift-invert; se comprueba Perron-Frobenius (autovector de signo constante) y el residuo.
"""
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.sparse.linalg import eigsh

AQUI = os.path.dirname(os.path.abspath(__file__))
F2 = os.path.join(os.path.dirname(os.path.dirname(AQUI)), "fase2", "codigo")
sys.path.insert(0, F2)
import pares            # noqa: E402
import radial           # noqa: E402
import transferencia as tr  # noqa: E402

BASE3 = os.path.dirname(AQUI)
RES3 = os.path.join(BASE3, "resultados")
FIG3 = os.path.join(BASE3, "figuras")
BETA = tr.BETA_PARED
DELTA_C_REF = 1.1906124210606      # Fase 1 / Fase 2 (radial, energia cero), recalculado por Gemini y V1
EPSS = (0.2, 0.1, 0.05)
HS = (0.02, 0.04)
UMBRAL_LEY_CAJA = 0.1               # decision 3: fijado ANTES de ver los datos de la Fase 3 (aprobado 10-11-2026)

_TABLAS = {}


def tabla(eps):
    if eps not in _TABLAS:
        _TABLAS[eps] = pares.tabla_richardson(eps)
    return _TABLAS[eps]


def resolver_tr(delta, R, h, eps, E_guess, k=3):
    """Mayor autovalor de T (shift-invert). Devuelve E0, E1, observables, chequeos y tiempo."""
    t = time.perf_counter()
    T, r = tr.matriz_T(R, h, eps, W=tr.W_yukawa(delta), tabla=tabla(eps))
    sigma = float(np.exp(-eps * (E_guess - 2e-4)))
    lam, v = eigsh(T, k=k, sigma=sigma, which="LM", tol=0)
    o = np.argsort(lam)[::-1]
    lam, v = lam[o], v[:, o]
    v0 = v[:, 0] * np.sign(v[:, 0].sum())
    perron = float(v0.min() / np.abs(v0).max())
    res = float(np.linalg.norm(T @ v0 - lam[0] * v0) / np.linalg.norm(v0))
    ob = tr._observables(r, v0, R)
    return dict(E0=float(-np.log(lam[0]) / eps), E1=float(-np.log(lam[1]) / eps),
                r_sobre_R=ob["r_sobre_R"], F12=ob["F12"], r_med=ob["r_med"], r2_med=ob["r2_med"],
                N=len(r), perron_min=perron, residuo=res, t=time.perf_counter() - t)


def ext_eps(a01, a005):
    return a005 + (a005 - a01) / 3.0


def radial_ref(delta, R, h=1 / 40):
    c = radial.resolver_rich(radial.V_yukawa(delta), R, h=h, nev=2)
    return dict(E0=c["E0"], E1=c["E1"], err=abs(c["E0"] - c["E0_h2"]), dE_rel=c["dE_rel"],
                r_med=c["r_med"], r2_med=c["r2_med"], r_sobre_R=c["r_sobre_R"], F12=c["F12"],
                err_r=abs(c["r_sobre_R"] - c["r_sobre_R_h2"]), err_F=abs(c["F12"] - c["F12_h2"]),
                err_rmed=abs(c["r_med"] - c["r_med_h2"]))


def celda(delta, R, verbose=True):
    """Receta completa de la Fase 2 (14_criterio_cajas.py) en una caja (delta, R)."""
    ref = radial_ref(delta, R)
    crudo, Eg = {}, ref["E0"]
    for h in HS:
        for eps in EPSS:
            d = resolver_tr(delta, R, h, eps, Eg)
            Eg = d["E0"]
            crudo[f"h{h:g}_eps{eps:g}"] = d
    E = {(h, e): crudo[f"h{h:g}_eps{e:g}"]["E0"] for h in HS for e in EPSS}
    EhR = {e: (16 * E[(0.02, e)] - E[(0.04, e)]) / 15 for e in EPSS}
    E_best = ext_eps(EhR[0.1], EhR[0.05])
    E_gruesa = ext_eps(EhR[0.2], EhR[0.1])
    E_h002 = ext_eps(E[(0.02, 0.1)], E[(0.02, 0.05)])
    den = abs(EhR[0.1] - EhR[0.05])
    p_trot = float(np.log2(abs(EhR[0.2] - EhR[0.1]) / den)) if den > 0 else float("nan")
    err_sin_pared = abs(E_h002 - E_best) + abs(E_best - E_gruesa)
    pared_e = {e: radial.resolver_rich(radial.V_yukawa(delta), R + BETA * np.sqrt(e), h=1 / 40, nev=1)["E0"]
               - ref["E0"] for e in EPSS}
    pared_ext = float(ext_eps(pared_e[0.1], pared_e[0.05]))
    err = err_sin_pared + abs(pared_ext)
    obs = {}
    for k in ("r_sobre_R", "F12", "r_med"):
        o = {(h, e): crudo[f"h{h:g}_eps{e:g}"][k] for h in HS for e in EPSS}
        b = ext_eps(o[(0.02, 0.1)], o[(0.02, 0.05)])
        er = (abs(b - ext_eps(o[(0.04, 0.1)], o[(0.04, 0.05)])) + abs(b - ext_eps(o[(0.02, 0.2)], o[(0.02, 0.1)])))
        obs[k] = dict(mejor=float(b), err=float(er))
    absE = abs(ref["E0"])
    c = dict(delta=delta, R=R, radial=ref, crudo=crudo, E_hRich={f"{e:g}": v for e, v in EhR.items()},
             E_mejor=float(E_best), err=float(err), err_sin_pared=float(err_sin_pared),
             sesgo_pared_extrapolado=pared_ext, orden_trotter=p_trot,
             dif_rad=float(E_best - ref["E0"]),
             compatible=bool(abs(E_best - ref["E0"]) <= 2 * (err + ref["err"]) + 1e-12),
             malla_rel={f"{e:g}": abs(E[(0.02, e)] - E[(0.04, e)]) / abs(E[(0.02, e)]) for e in EPSS},
             trotter_eps02_rel=abs(EhR[0.2] - E_best) / absE,
             perron_min=min(d["perron_min"] for d in crudo.values()),
             residuo_max=max(d["residuo"] for d in crudo.values()),
             t=sum(d["t"] for d in crudo.values()), obs=obs)
    if verbose:
        print(f"d={delta:<5} R={R:<5} E_tr={E_best:+.10e}+-{err:.1e} E_rad={ref['E0']:+.10e} dif={c['dif_rad']:+.1e} "
              f"pTrot={p_trot:.3f} r/R={obs['r_sobre_R']['mejor']:.5f} F12={obs['F12']['mejor']:.5f} "
              f"perron={c['perron_min']:+.1e} t={c['t']:.0f}s", flush=True)
    return c


def long_dispersion(delta, Rf=80.0):
    f = lambda r, s: [s[1], -2.0 * np.exp(-delta * r) / r * s[0]]
    s = solve_ivp(f, [1e-10, Rf], [1e-10, 1.0], method="DOP853", rtol=1e-13, atol=1e-18)
    return float(Rf - s.y[0, -1] / s.y[1, -1])


def evaluar(celdas_d, terna, fuente, a_s):
    """Criterio 9.6 de la Fase 1 con la condicion (c) de la Fase 2 (identico a 14_criterio_cajas.py)."""
    C = celdas_d
    if fuente == "radial":
        E = [C[R]["radial"]["E0"] for R in terna]; eE = [C[R]["radial"]["err"] for R in terna]
        rr = [C[R]["radial"]["r_sobre_R"] for R in terna]; F = [C[R]["radial"]["F12"] for R in terna]
        malla = [C[R]["radial"]["dE_rel"] for R in terna]
    else:
        E = [C[R]["E_mejor"] for R in terna]; eE = [C[R]["err"] for R in terna]
        rr = [C[R]["obs"]["r_sobre_R"]["mejor"] for R in terna]; F = [C[R]["obs"]["F12"]["mejor"] for R in terna]
        malla = [max(C[R]["malla_rel"].values()) for R in terna]
    dec = lambda x: all(x[i + 1] < x[i] for i in range(2))
    inc = lambda x: all(x[i + 1] > x[i] for i in range(2))
    neg = [E[i] < 0 and abs(E[i]) > eE[i] for i in range(3)]
    pos = [E[i] > 0 and abs(E[i]) > eE[i] for i in range(3)]
    a = bool(neg[1] and neg[2] and abs(E[2] - E[1]) < 0.1 * abs(E[2]))
    ap = bool(all(m < 0.1 for m in malla))
    b = bool(dec(rr) and inc(F) and F[2] > 0.95)
    ley = [np.pi**2 / (2 * (R - a_s)**2) for R in terna]
    dev = [abs(E[i] - ley[i]) / ley[i] for i in range(3)]
    nl_ley = bool(dev[2] < UMBRAL_LEY_CAJA and dev[2] < dev[1] < dev[0])
    return dict(terna=list(terna), E=E, err_E=eE, r_sobre_R=rr, F12=F, malla_rel=malla, a=a, a_prima=ap, b=b,
                ligado=bool(a and ap and b), nl_signo=bool(all(pos)), nl_tendencias=bool(inc(rr) and dec(F)),
                dev_ley=dev, nl_ley=nl_ley, no_ligado=bool(all(pos) and inc(rr) and dec(F) and nl_ley and ap))


def cond_c(celdas_d, terna, a_s):
    rr, tt = evaluar(celdas_d, terna, "radial", a_s), evaluar(celdas_d, terna, "transferencia", a_s)
    signo = all(np.sign(rr["E"][i]) == np.sign(tt["E"][i]) and abs(tt["E"][i]) > tt["err_E"][i] for i in range(3))
    tend = lambda x: [np.sign(x[i + 1] - x[i]) for i in range(2)]
    misma = tend(rr["r_sobre_R"]) == tend(tt["r_sobre_R"]) and tend(rr["F12"]) == tend(tt["F12"])
    compat = all(celdas_d[R]["compatible"] for R in terna)
    return dict(mismo_signo=bool(signo), misma_tendencia=bool(misma), E_compatibles=bool(compat),
                c=bool(signo and misma and compat))

```
