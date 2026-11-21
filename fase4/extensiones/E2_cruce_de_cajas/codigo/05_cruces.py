"""05_cruces.py -- cruces delta*(R, 2R) de y = 2R^2E0/pi^2 y de rho = <r>/R, propagacion de errores y extrapolacion en R.

Fuentes: disparo sin malla (02), radial h = 1/40 y h = 1/160 (03), integral de camino (transferencia, 04).
Interpolacion en delta de D(delta) = X(delta, R) - X(delta, 2R) sobre los 15 nodos de la rejilla:
  - "spline": spline cubico not-a-knot (metodo principal: suave, lineal en los datos, error O(h^4));
  - "pchip": interpolante monotono por tramos (no lineal, sin oscilaciones);
  - "local3": polinomio cubico por los 4 nodos mas cercanos al cambio de signo.
Errores del cruce (fijados en criterios_previos.md): (i) Monte Carlo con semilla fija, N = 20240 replicas
gaussianas independientes por celda; la misma replica de una celda se usa en los dos pares donde aparece, asi que
la correlacion entre cruces vecinos se conserva; (ii) propagacion lineal conservadora
(|sigma(R)| + |sigma(2R)|)/|D'(delta*)|. La barra es la mayor de las dos.
Transferencia, metodo B: la receta de la Fase 3 aplicada al cruce (se cruza con cada (h, eps) crudo y se extrapola).
  Barra de B = malla + Trotter + |pared| para los dos observables; la pared de <r>/R viene de 04b_pared_rho.py (anadida
  tras la revision R2, hallazgo R2-01) y, como en y, solo entra en la barra (decision 5 de la Fase 2).
  Metodo A de <r>/R: la barra de cada celda tambien suma |pared_rho| (mismo criterio que la de E0, que la trae de 04).
Extrapolacion en R (forma fijada por teoria.md): delta*(R) = delta_c + alpha/R^2 + beta/R^3, pares con R >= 100;
se compara con Richardson de los dos pares mayores (solo 1/R^2) y la diferencia se suma a la barra.
Salida: resultados/05_cruces.json
"""
import sys, time
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.optimize import brentq
import e2comun as c

sys.stdout = c.Tee("05_cruces")
T0 = time.perf_counter()
NREP = 20240
SEMILLA = 20261117
DEL = np.array(c.DELTAS)
TEO = c.cargar("01_teoria")


# --------------------------------------------------------------------------- carga de datos
def cargar_fuentes():
    F = {}
    dis = c.cargar("02_disparo")
    Rs = [R for R in c.RS]
    F["disparo"] = dict(Rs=Rs,
                        y=np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["y"] for R in Rs] for d in DEL]),
                        rho=np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["r_sobre_R"] for R in Rs] for d in DEL]))
    F["disparo"]["sy"] = np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["err_y"] for R in Rs] for d in DEL])
    F["disparo"]["srho"] = np.array([[dis["celdas"][f"{d:g}"][f"R{R}"]["err_r"] for R in Rs] for d in DEL])
    rad = c.cargar("03_radial")
    for nm in ("h40", "h160"):
        C = rad["celdas"][nm]
        F["radial_" + nm] = dict(
            Rs=Rs,
            y=np.array([[C[f"{d:g}"][f"R{R}"]["y"] for R in Rs] for d in DEL]),
            sy=np.array([[C[f"{d:g}"][f"R{R}"]["err_y"] for R in Rs] for d in DEL]),
            rho=np.array([[C[f"{d:g}"][f"R{R}"]["r_sobre_R"] for R in Rs] for d in DEL]),
            srho=np.array([[C[f"{d:g}"][f"R{R}"]["err_r"] for R in Rs] for d in DEL]))
    Rt = []
    T = {}
    for R in c.RS:
        try:
            x = c.cargar(f"04_transferencia_R{R}")["celdas"]
        except FileNotFoundError:
            continue
        if all(f"{d:g}" in x for d in DEL) and (not Rt or R == 2 * Rt[-1]):
            T[R] = x; Rt.append(R)
    g = lambda fn: np.array([[fn(T[R][f"{d:g}"], R) for R in Rt] for d in DEL])
    tr = dict(Rs=Rt,
              y=g(lambda x, R: c.y_de(x["E_mejor"], R)), sy=g(lambda x, R: c.y_de(x["err"], R)),
              rho=g(lambda x, R: x["obs"]["r_sobre_R"]["mejor"]), srho=g(lambda x, R: x["obs"]["r_sobre_R"]["err"]),
              pared_y=g(lambda x, R: c.y_de(x["sesgo_pared_extrapolado"], R)),
              E=g(lambda x, R: x["E_mejor"]), sE=g(lambda x, R: x["err"]))
    # sesgo de pared de <r>/R por celda (04b_pared_rho.py, revision R2-01): misma receta que el de E0; solo va a la barra
    PR = c.cargar("04b_pared_rho")["celdas"]
    tr["pared_rho"] = np.array([[PR[f"{d:g}"][f"R{R}"]["pared_rho"] for R in Rt] for d in DEL])
    # metodo A de <r>/R: como en E0 (cuya barra de celda ya trae |sesgo de pared|), la barra de celda de <r>/R pasa a ser
    # malla + Trotter + |pared_rho|; el valor central no cambia (decision 5 de la Fase 2)
    tr["srho_sin_pared"] = tr["srho"]
    tr["srho"] = tr["srho"] + np.abs(tr["pared_rho"])
    tr["crudo_y"] = {k: g(lambda x, R, k=k: c.y_de(x["crudo"][k]["E0"], R)) for k in T[Rt[0]]["1.19"]["crudo"]}
    tr["crudo_rho"] = {k: g(lambda x, R, k=k: x["crudo"][k]["r_sobre_R"]) for k in T[Rt[0]]["1.19"]["crudo"]}
    F["transferencia"] = tr
    # variante de sensibilidad: pared restada del valor central (NO es la receta; decision 5 deja la pared en el error)
    F["transferencia_pared_restada"] = dict(Rs=Rt, y=tr["y"] - tr["pared_y"], sy=tr["sy"] - np.abs(tr["pared_y"]),
                                            rho=tr["rho"], srho=tr["srho_sin_pared"])
    return F


# --------------------------------------------------------------------------- interpolacion y raiz
def raiz(D, metodo, guia=None):
    """Cruce: raiz de D(delta) interpolado. Si hay varias, la mas cercana a 'guia' (o al primer cambio de signo
    de los nodos contando desde el lado ligado)."""
    s = np.sign(D)
    idx = np.nonzero(s[1:] != s[:-1])[0]
    if len(idx) == 0:
        return np.nan, 0
    if guia is None:
        i = idx[0]
    else:
        i = idx[np.argmin(np.abs(DEL[idx] - guia))]
    if metodo == "spline":
        f = CubicSpline(DEL, D)
    elif metodo == "pchip":
        f = PchipInterpolator(DEL, D)
    elif metodo == "local3":
        j0 = int(np.clip(i - 1, 0, len(DEL) - 4))
        p = np.polyfit(DEL[j0:j0 + 4] - DEL[i], D[j0:j0 + 4], 3)
        f = lambda x: np.polyval(p, x - DEL[i])
    elif metodo == "lineal":
        return float(DEL[i] - D[i] * (DEL[i + 1] - DEL[i]) / (D[i + 1] - D[i])), len(idx)
    r = brentq(lambda x: float(f(x)), DEL[i], DEL[i + 1], xtol=1e-14)
    return float(r), len(idx)


def deriv_spline(D, x):
    return float(CubicSpline(DEL, D)(x, 1))


def interp_spline(v, x):
    return float(CubicSpline(DEL, v)(x))


def cruces_fuente(Fu, obs, rng_rep=None, con_mc=True):
    """Para cada par (R, 2R) de la fuente: cruce con tres interpolaciones, valor en el cruce, barras MC y lineal."""
    Rs = Fu["Rs"]
    X, S = Fu[obs], Fu["s" + obs]
    pares = [(i, i + 1) for i in range(len(Rs) - 1) if Rs[i + 1] == 2 * Rs[i]]
    res = []
    # replicas MC: una por celda, compartida entre pares
    if con_mc and np.any(S > 0):
        rng = np.random.default_rng(SEMILLA)
        ruido = rng.standard_normal((NREP,) + X.shape)
        Xr = X[None, :, :] + S[None, :, :] * ruido
    else:
        Xr = None
    for (i, j) in pares:
        D = X[:, i] - X[:, j]
        d = {m: raiz(D, m) for m in ("spline", "pchip", "local3", "lineal")}
        ds = d["spline"][0]
        fila = dict(R=Rs[i], R2=Rs[j], delta=ds, n_cambios_signo=d["spline"][1],
                    delta_pchip=d["pchip"][0], delta_local3=d["local3"][0], delta_lineal=d["lineal"][0],
                    dif_interp=float(max(abs(d["pchip"][0] - ds), abs(d["local3"][0] - ds))),
                    valor=interp_spline(X[:, j], ds), valor_R=interp_spline(X[:, i], ds),
                    pendiente=deriv_spline(D, ds))
        if Xr is not None:
            sR, s2R = interp_spline(S[:, i], ds), interp_spline(S[:, j], ds)
            fila["sigma_lineal"] = float((abs(sR) + abs(s2R)) / abs(fila["pendiente"]))
            Dr = Xr[:, :, i] - Xr[:, :, j]                      # (NREP, ndelta)
            w = max(8.0 * fila["sigma_lineal"], 5e-5)
            xf = np.linspace(max(DEL[0], ds - w), min(DEL[-1], ds + w), 1601)
            reps = np.full(NREP, np.nan)
            for k0 in range(0, NREP, 2530):                      # por bloques, para no llenar la memoria
                vf = CubicSpline(DEL, Dr[k0:k0 + 2530].T, axis=0)(xf)   # (nfino, bloque)
                cambio = np.sign(vf[1:]) != np.sign(vf[:-1])
                for kk in range(vf.shape[1]):
                    ii = np.nonzero(cambio[:, kk])[0]
                    if len(ii) == 0:
                        continue
                    m = ii[np.argmin(np.abs(xf[ii] - ds))]
                    reps[k0 + kk] = xf[m] - vf[m, kk] * (xf[m + 1] - xf[m]) / (vf[m + 1, kk] - vf[m, kk])
            ok = np.isfinite(reps)
            fila["mc_validas"] = int(ok.sum())
            fila["sigma_mc"] = float(np.std(reps[ok]))
            fila["mc_p16_p84"] = [float(np.percentile(reps[ok], 16)), float(np.percentile(reps[ok], 84))]
            fila["sigma"] = float(max(fila["sigma_mc"], fila["sigma_lineal"]))
            fila["_reps"] = reps
        else:
            fila["sigma_lineal"] = fila["sigma_mc"] = fila["sigma"] = 0.0
        res.append(fila)
    return res


# --------------------------------------------------------------------------- extrapolacion en R
def ajuste(Rs, ds, w=None, beta=True):
    Rs = np.asarray(Rs, float); ds = np.asarray(ds, float)
    A = np.column_stack([np.ones_like(Rs), Rs**-2] + ([Rs**-3] if beta else []))
    W = np.ones_like(Rs) if w is None else np.asarray(w, float)
    coef, *_ = np.linalg.lstsq(A * W[:, None], ds * W, rcond=None)
    # pesos lineales del valor extrapolado: delta_c = sum_i L_i ds_i
    L = np.linalg.pinv(A * W[:, None])[0] * W
    return coef, L


def extrapolar(filas, Rmin=100, con_mc=True, ponderado=True, Rmax=10**9):
    usa = [f for f in filas if Rmin <= f["R"] <= Rmax and np.isfinite(f["delta"])]
    Rs = [f["R"] for f in usa]; ds = [f["delta"] for f in usa]; sg = [f["sigma"] for f in usa]
    out = dict(R_usados=Rs)
    w = 1.0 / np.asarray(sg) if (ponderado and all(x > 0 for x in sg)) else None
    out["ponderado"] = w is not None
    coef, L = ajuste(Rs, ds, w=w, beta=True)
    out["ajuste_ab"] = dict(delta_c=float(coef[0]), alpha=float(coef[1]), beta=float(coef[2]),
                            sigma_lineal=float(np.sum(np.abs(L) * np.asarray(sg))))
    # Richardson con los dos pares mayores (solo 1/R^2)
    f1, f2 = usa[-2], usa[-1]
    rich = (4 * f2["delta"] - f1["delta"]) / 3
    out["richardson_2_mayores"] = dict(delta_c=float(rich), sigma_lineal=float((4 * f2["sigma"] + f1["sigma"]) / 3))
    # ajuste a + alpha/R^2 con los tres pares mayores (otra variante de modelo)
    if len(usa) >= 3:
        coef3, L3 = ajuste(Rs[-3:], ds[-3:], beta=False)
        out["ajuste_a_3_mayores"] = dict(delta_c=float(coef3[0]), alpha=float(coef3[1]))
    out["sistematico_modelo"] = float(abs(out["ajuste_ab"]["delta_c"] - rich))
    if con_mc and all("_reps" in f for f in usa):
        R = np.array([f["_reps"] for f in usa])           # (npares, NREP)
        ok = np.all(np.isfinite(R), axis=0)
        dcr = L @ R[:, ok]
        out["ajuste_ab"]["sigma_mc"] = float(np.std(dcr))
    s_est = max(out["ajuste_ab"].get("sigma_mc", 0.0), out["ajuste_ab"]["sigma_lineal"])
    out["sigma_estadistica"] = float(s_est)
    out["barra_total"] = float(s_est + out["sistematico_modelo"])
    dc = out["ajuste_ab"]["delta_c"]
    out["intervalo"] = [float(dc - out["barra_total"]), float(dc + out["barra_total"])]
    out["contiene_referencia"] = bool(out["intervalo"][0] <= c.DELTA_C_REF <= out["intervalo"][1])
    out["dif_referencia"] = float(dc - c.DELTA_C_REF)
    out["razones_dif_sucesivas"] = [float((filas[k]["delta"] - filas[k + 1]["delta"]) /
                                          (filas[k + 1]["delta"] - filas[k + 2]["delta"]))
                                    for k in range(len(filas) - 2)]
    return out


# --------------------------------------------------------------------------- metodo B (transferencia)
def metodo_B(tr, obs):
    Rs = tr["Rs"]
    cr = tr["crudo_" + obs]
    pares = [(i, i + 1) for i in range(len(Rs) - 1) if Rs[i + 1] == 2 * Rs[i]]
    filas = []
    for (i, j) in pares:
        dd = {}
        for k, X in cr.items():
            dd[k] = raiz(X[:, i] - X[:, j], "spline")[0]
        g = lambda h, e: dd[f"h{h:g}_eps{e:g}"]
        if obs == "y":
            hR = {e: (16 * g(0.02, e) - g(0.04, e)) / 15 for e in (0.2, 0.1, 0.05)}
            best = c.comun3.ext_eps(hR[0.1], hR[0.05]); grues = c.comun3.ext_eps(hR[0.2], hR[0.1])
            h002 = c.comun3.ext_eps(g(0.02, 0.1), g(0.02, 0.05))
            Xc = tr["y"]; P = tr["pared_y"]
            d_sin = raiz((Xc - P)[:, i] - (Xc - P)[:, j], "spline")[0]
            d_con = raiz(Xc[:, i] - Xc[:, j], "spline")[0]
            pared = abs(d_con - d_sin)
            err = abs(h002 - best) + abs(best - grues) + pared
            filas.append(dict(R=Rs[i], R2=Rs[j], delta=float(best), sigma=float(err), err_malla=float(abs(h002 - best)),
                              err_trotter=float(abs(best - grues)), err_pared=float(pared), crudos=dd,
                              delta_pared_restada=float(best - (d_con - d_sin))))
        else:
            best = c.comun3.ext_eps(g(0.02, 0.1), g(0.02, 0.05))
            e_h = abs(best - c.comun3.ext_eps(g(0.04, 0.1), g(0.04, 0.05)))
            e_t = abs(best - c.comun3.ext_eps(g(0.02, 0.2), g(0.02, 0.1)))
            # termino de pared (revision R2-01), igual que en y: corrimiento del cruce de los valores de la receta al
            # restarles el sesgo de pared de cada celda; por la decision 5 de la Fase 2 solo entra en la barra
            Xc = tr["rho"]; P = tr["pared_rho"]
            d_sin = raiz((Xc - P)[:, i] - (Xc - P)[:, j], "spline")[0]
            d_con = raiz(Xc[:, i] - Xc[:, j], "spline")[0]
            pared = abs(d_con - d_sin)
            filas.append(dict(R=Rs[i], R2=Rs[j], delta=float(best), sigma=float(e_h + e_t + pared), err_malla=float(e_h),
                              err_trotter=float(e_t), err_pared=float(pared), sigma_sin_pared=float(e_h + e_t),
                              crudos=dd, delta_pared_restada=float(best - (d_con - d_sin))))
    return filas


# --------------------------------------------------------------------------- principal
F = cargar_fuentes()
out = dict(script="05_cruces.py", fecha=c.ahora(), NREP=NREP, semilla=SEMILLA, deltas=list(c.DELTAS),
           referencia=c.DELTA_C_REF, R_transferencia=F["transferencia"]["Rs"], fuentes={})
pred = {f["R"]: f for f in TEO["modelo_ERE"]}
for nombre in ("disparo", "radial_h40", "radial_h160", "transferencia", "transferencia_pared_restada"):
    Fu = F[nombre]
    out["fuentes"][nombre] = {}
    for obs in ("y", "rho"):
        if nombre == "transferencia_pared_restada" and obs == "rho":
            continue
        filas = cruces_fuente(Fu, obs)
        ex = extrapolar(filas, ponderado=(nombre != "disparo"))
        # variante: solo cajas R <= 800 (pares hasta 400/800), para comparar con lo que da la caja pequena
        ex800 = extrapolar(filas, con_mc=(nombre != "disparo"), ponderado=(nombre != "disparo"), Rmax=400)
        for f in filas:
            f.pop("_reps", None)
            p = pred.get(f["R"])
            if p is not None:
                f["prediccion_ERE"] = p["delta_y" if obs == "y" else "delta_rho"]
        out["fuentes"][nombre][obs] = dict(pares=filas, extrapolacion=ex, extrapolacion_R_hasta_800=ex800)
        print(f"== {nombre} / {obs}")
        for f in filas:
            print(f"   {f['R']:>5}/{f['R2']:<5} delta*={f['delta']:.9f} +- {f['sigma']:.2e} (MC {f['sigma_mc']:.1e}, "
                  f"lin {f['sigma_lineal']:.1e})  valor={f['valor']:.6f}  dif_interp={f['dif_interp']:.1e}  "
                  f"ERE={f.get('prediccion_ERE', float('nan')):.9f}  ncambios={f['n_cambios_signo']}")
        e = ex
        print(f"   ajuste a+b/R^2+c/R^3: delta_c={e['ajuste_ab']['delta_c']:.10f} alpha={e['ajuste_ab']['alpha']:.4f} "
              f"beta={e['ajuste_ab']['beta']:.3f} | Richardson={e['richardson_2_mayores']['delta_c']:.10f} | "
              f"barra={e['barra_total']:.2e} -> [{e['intervalo'][0]:.9f}, {e['intervalo'][1]:.9f}] contiene ref: "
              f"{e['contiene_referencia']}  razones={['%.2f' % r for r in e['razones_dif_sucesivas']]}", flush=True)

# solo para documentar el cambio: metodo A de <r>/R con la barra de celda de antes (sin pared); no es la receta
_Fsp = dict(F["transferencia"], srho=F["transferencia"]["srho_sin_pared"])
_fsp = cruces_fuente(_Fsp, "rho")
out["fuentes"]["transferencia"]["rho"]["sin_pared_A"] = dict(
    sigmas=[f["sigma"] for f in _fsp],
    extrapolacion={k: v for k, v in extrapolar(_fsp, ponderado=True).items() if k in ("barra_total", "intervalo", "ajuste_ab")},
    extrapolacion_R_hasta_800={k: v for k, v in extrapolar(_fsp, ponderado=True, Rmax=400).items()
                               if k in ("barra_total", "intervalo", "ajuste_ab")})

# metodo B
out["transferencia_metodo_B"] = {}
for obs in ("y", "rho"):
    filas = metodo_B(F["transferencia"], obs)
    ex = extrapolar(filas, con_mc=False)
    ex800 = extrapolar(filas, con_mc=False, Rmax=400)
    out["transferencia_metodo_B"][obs] = dict(pares=filas, extrapolacion=ex, extrapolacion_R_hasta_800=ex800)
    if obs == "rho":   # solo para documentar R2-01: la barra de antes, sin el termino de pared (no es la receta)
        ex_sp = extrapolar([dict(f, sigma=f["sigma_sin_pared"]) for f in filas], con_mc=False)
        out["transferencia_metodo_B"][obs]["extrapolacion_sin_pared_R2_01"] = dict(
            barra_total=ex_sp["barra_total"], intervalo=ex_sp["intervalo"], delta_c=ex_sp["ajuste_ab"]["delta_c"])
    print(f"== transferencia metodo B / {obs}")
    for f in filas:
        print(f"   {f['R']:>5}/{f['R2']:<5} delta*={f['delta']:.9f} +- {f['sigma']:.2e} (malla {f['err_malla']:.1e}, "
              f"Trotter {f['err_trotter']:.1e}, pared {f.get('err_pared', 0):.1e})")
    print(f"   delta_c={ex['ajuste_ab']['delta_c']:.10f}  barra={ex['barra_total']:.2e} -> [{ex['intervalo'][0]:.9f}, "
          f"{ex['intervalo'][1]:.9f}] contiene ref: {ex['contiene_referencia']}", flush=True)

# sensibilidad a h de la transferencia: cruce y extrapolacion usando solo h = 0.02 (eps extrapolado), sin Richardson h^4
tr = F["transferencia"]
sens = {}
for hh in (0.02, 0.04):
    Xh = c.comun3.ext_eps(tr["crudo_y"][f"h{hh:g}_eps0.1"], tr["crudo_y"][f"h{hh:g}_eps0.05"])
    Fu = dict(Rs=tr["Rs"], y=Xh, sy=tr["sy"])
    fil = cruces_fuente(Fu, "y", con_mc=False)
    ex = extrapolar(fil, con_mc=False)
    sens[f"h{hh:g}"] = dict(cruces=[f["delta"] for f in fil], delta_c=ex["ajuste_ab"]["delta_c"])
    print(f"sensibilidad h={hh}: cruces {['%.9f' % f['delta'] for f in fil]} delta_c={ex['ajuste_ab']['delta_c']:.10f}")
out["sensibilidad_h_transferencia"] = sens
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("05_cruces", out)
print(f"tiempo {out['tiempo_s']:.0f} s")
