"""26_transferencia_grande.py -- Proyecto 05, Fase 3: condicion (c) en delta = 1.19 con R = 6400 y 12800 (hallazgo G7 de la auditoria
con Gemini). En 20b el modo shift-invert de eigsh (LU dispersa de SuperLU) no cupo en memoria con N = 319999. Aqui la
iteracion inversa usa la LU EN BANDA de LAPACK (dgbtrf/dgbtrs): sin relleno fuera de la banda, memoria N (3 nb + 1) dobles.
Desplazamiento sigma = e^{-eps (E_g - 2e-8)} cerca de lambda0 y vector inicial del radial; se itera hasta que el cociente de
Rayleigh no cambie a 1e-15. Misma receta de extrapolacion que comun3.celda (h = 0.02, 0.04; eps = 0.2, 0.1, 0.05; pared en el
error). Salida: fase3/resultados/26_transferencia_grande.json."""
import json, os, sys, time
import numpy as np
from scipy.linalg.lapack import dgbtrf, dgbtrs
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comun3 as c  # noqa: E402


def mayor_autovalor(T, sigma, v0, itmax=60):
    N = T.shape[0]
    Td = T.todia()
    nb = int(max(abs(o) for o in Td.offsets))
    ab = np.zeros((3 * nb + 1, N))
    for off, dat in zip(Td.offsets, Td.data):           # formato DIA: data[k, j] = A[j - off, j]
        ab[2 * nb - off, :] = dat
    ab[2 * nb, :] -= sigma
    lu, piv, info = dgbtrf(ab, nb, nb)
    assert info == 0, info
    v = v0 / np.linalg.norm(v0); lam_old = 0
    for it in range(itmax):
        w, info = dgbtrs(lu, nb, nb, v, piv)
        v = w / np.linalg.norm(w)
        lam = float(v @ (T @ v))
        if abs(lam - lam_old) < 1e-15 * abs(lam):
            break
        lam_old = lam
    res = float(np.linalg.norm(T @ v - lam * v))
    return lam, v * np.sign(v.sum()), it, res


def correr(R):
    T0 = time.perf_counter()
    d = 1.19
    ref = c.radial_ref(d, R, h=1 / 160)
    xr = c.radial.resolver(c.radial.V_yukawa(d), R, h=1 / 160, nev=1)
    crudo = {}
    for h in c.HS:
        for e in c.EPSS:
            t = time.perf_counter()
            T, r = c.tr.matriz_T(R, h, e, W=c.tr.W_yukawa(d), tabla=c.tabla(e))
            v0 = np.interp(r, xr["r"], xr["u"])
            Eg = ref["E0"] - 3e-6 * (e / 0.2)**2         # el sesgo de Trotter baja la energia (~1e-6 con eps = 0.2)
            lam, v, it, res = mayor_autovalor(T, float(np.exp(-e * (Eg - 5e-7))), v0)
            ob = c.tr._observables(r, v, R)
            crudo[f"h{h:g}_eps{e:g}"] = dict(E0=float(-np.log(lam) / e), iteraciones=it, residuo=res,
                                             perron_min=float(v.min() / np.abs(v).max()), **ob)
            print(f"h={h} eps={e}: E0={-np.log(lam)/e:+.8e} it={it} res={res:.1e} perron={v.min()/np.abs(v).max():+.1e} "
                  f"r/R={ob['r_sobre_R']:.5f} F12={ob['F12']:.5f} t={time.perf_counter()-t:.0f}s", flush=True)
    E = {(h, e): crudo[f"h{h:g}_eps{e:g}"]["E0"] for h in c.HS for e in c.EPSS}
    EhR = {e: (16 * E[(0.02, e)] - E[(0.04, e)]) / 15 for e in c.EPSS}
    Eb = c.ext_eps(EhR[0.1], EhR[0.05]); Eg2 = c.ext_eps(EhR[0.2], EhR[0.1]); E002 = c.ext_eps(E[(0.02, 0.1)], E[(0.02, 0.05)])
    pared = {e: c.radial.resolver_rich(c.radial.V_yukawa(d), R + c.BETA * np.sqrt(e), h=1 / 160, nev=1)["E0"] - ref["E0"] for e in c.EPSS}
    pe = c.ext_eps(pared[0.1], pared[0.05])
    err = abs(E002 - Eb) + abs(Eb - Eg2) + abs(pe)
    obs = {}
    for k in ("r_sobre_R", "F12"):
        o = {(h, e): crudo[f"h{h:g}_eps{e:g}"][k] for h in c.HS for e in c.EPSS}
        b = c.ext_eps(o[(0.02, 0.1)], o[(0.02, 0.05)])
        obs[k] = dict(mejor=float(b), err=float(abs(b - c.ext_eps(o[(0.04, 0.1)], o[(0.04, 0.05)])) + abs(b - c.ext_eps(o[(0.02, 0.2)], o[(0.02, 0.1)]))))
    out = dict(script="26_transferencia_grande.py", fecha="2026-11-10", delta=d, R=R, radial_h160=ref, crudo=crudo,
               E_hRich={f"{e:g}": v for e, v in EhR.items()}, E_mejor=Eb, err=err, sesgo_pared_extrapolado=pe,
               compatible=bool(abs(Eb - ref["E0"]) <= 2 * (err + ref["err"])), obs=obs, tiempo_s=time.perf_counter() - T0)
    return out
    print(f"delta=1.19 R={R}: transferencia {Eb:+.4e} +- {err:.1e}; radial (h=1/160) {ref['E0']:+.4e} +- {ref['err']:.1e}; "
          f"compatible {out['compatible']}; r/R {obs['r_sobre_R']['mejor']:.4f}, F12 {obs['F12']['mejor']:.4f}; {out['tiempo_s']:.0f} s")


if __name__ == "__main__":
    import warnings; warnings.simplefilter("ignore")
    res = {f"R{R}": correr(R) for R in (6400, 12800)}
    # condicion (c) en la terna 3200 / 6400 / 12800 con los dos metodos (transferencia de 20 en R = 3200; radial h = 1/160)
    CJ = json.load(open(os.path.join(c.RES3, "20_cajas.json")))["celdas"]["1.19"]["R3200"]
    F = json.load(open(os.path.join(c.RES3, "20c_umbral_119_fino.json")))["radial"]
    cel = {3200: dict(radial=F["R3200"], E_mejor=CJ["E_mejor"], err=CJ["err"], obs=CJ["obs"], malla_rel=CJ["malla_rel"],
                      compatible=bool(abs(CJ["E_mejor"] - F["R3200"]["E0"]) <= 2 * (CJ["err"] + F["R3200"]["err"])))}
    for R in (6400, 12800):
        x = res[f"R{R}"]
        mr = {f"{e:g}": abs(x["crudo"][f"h0.02_eps{e:g}"]["E0"] - x["crudo"][f"h0.04_eps{e:g}"]["E0"]) / abs(x["crudo"][f"h0.02_eps{e:g}"]["E0"]) for e in c.EPSS}
        cel[R] = dict(radial=F[f"R{R}"], E_mejor=x["E_mejor"], err=x["err"], obs=x["obs"], malla_rel=mr,
                      compatible=bool(abs(x["E_mejor"] - F[f"R{R}"]["E0"]) <= 2 * (x["err"] + F[f"R{R}"]["err"])))
    a_s = c.long_dispersion(1.19)
    t = (3200, 6400, 12800)
    ev = dict(radial=c.evaluar(cel, t, "radial", a_s), transferencia=c.evaluar(cel, t, "transferencia", a_s), c=c.cond_c(cel, t, a_s))
    ver = "ligado" if ev["radial"]["ligado"] and ev["transferencia"]["ligado"] and ev["c"]["c"] else "indeterminado"
    print(f"terna {t}: radial ligado={ev['radial']['ligado']} transferencia ligado={ev['transferencia']['ligado']} (c)={ev['c']} -> {ver}")
    json.dump(dict(script="26_transferencia_grande.py", fecha="2026-11-10", celdas=res, terna=list(t), evaluacion=ev, veredicto=ver),
              open(os.path.join(c.RES3, "26_transferencia_grande.json"), "w"), indent=1, default=float)
