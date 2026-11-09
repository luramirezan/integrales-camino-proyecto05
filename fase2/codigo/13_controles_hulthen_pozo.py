"""13_controles_hulthen_pozo.py -- Proyecto 05 (Yukawa), Fase 2, tarea 5 (pedida por el profesor tras la
presentacion de la Fase 1): controles EXACTOS pasados por la MISMA formulacion de tiempo imaginario
(fase2/codigo/transferencia.py) y por el solucionador radial (fase2/codigo/radial.py).

Unidades hbar = m = 1.

A. Hulthen V_H = -delta/(e^{delta r} - 1). Misma singularidad -1/r en el origen que el Yukawa, asi que se usa
   la MISMA accion de pares de Coulomb (tabla U_C de pares.py, Richardson en h_tab) con el resto
       W_H = V_H + 1/r = 1/r - delta/(e^{delta r} - 1),
   que se comprueba acotado en [0, delta/2] (A.0). delta in {0.2, 1.0, 1.5}; caja R = max(60, 25/kappa),
   kappa = 1 - delta/2. eps in {0.2, 0.1, 0.05} (extrapolacion eps -> 0 con ley eps^2) y, como extra,
   eps = 0.025 para ver mejor el orden. Mallas Nystrom h = 0.04, 0.02 (y 0.01): el error de Nystrom de la
   cuspide escala como h^4 (seccion 11.4), asi que E se combina con Richardson en h de exponente 4.
   Exacto: E = -(1/2)(1 - delta/2)^2, <r> = (12 - delta^2)/(2(4 - delta^2)) (radial.hulthen_exacto, sympy).
B. Pozo esferico cuadrado V = -V0 (r < 1), V0 in {2, 1.3} (umbral pi^2/8 = 1.2337). Sin singularidad: opcion
   sin U_C de transferencia.py, T_ij = h K_D e^{-eps(V_i + V_j)/2}. Convencion principal V(1) = -V0/2 con
   r = 1 en un nodo ("media"); control con V(1) = 0 ("estricta"). Se MIDE el orden de Trotter aparente con
   la discontinuidad: eps in {0.2, 0.1, 0.05, 0.025, 0.0125}, h in {0.04, 0.02, 0.01}, extrapolacion h -> 0
   con el orden medido en h, y luego eps -> 0 con el orden medido en eps. Exacto: brentq de k cot k = -kappa
   (radial.pozo_exacto). Caja R = max(60, 25/kappa) redondeada hacia arriba a entero.
   Autovalor por desplazamiento-inversion (eigsh con sigma por encima del espectro); se comprueba frente a
   tr.resolver (Lanczos 'LA') en un caso.
C. PIGS de Hulthen (opcional): NO se hace aqui (pigs.py aun no existe en fase2/codigo/).

Determinista: no usa numeros aleatorios (las semillas 20262000+k no hacen falta).
Salida: fase2/resultados/13_controles.json y fase2/figuras/13_controles.png.
Criterios fijados ANTES de ejecutar (ver lista CRIT_DECL).
"""
import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np                                        # noqa: E402
from scipy.sparse.linalg import eigsh                     # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import pares                       # noqa: E402
import transferencia as tr         # noqa: E402
import radial                      # noqa: E402

BASE = os.path.dirname(AQUI)
RES = os.path.join(BASE, "resultados")
FIG = os.path.join(BASE, "figuras")

CRIT_DECL = {
    "A0": "W_H en [0, delta/2] y decreciente en r in [1e-8, 400] (tolerancia 1e-14)",
    "A1": "radial frente a exacto: |E0-E| < 1e-8 y |<r>-<r>_ex|/<r>_ex < 2e-7",
    "A2": "transferencia (Richardson h^4 con h=0.02,0.04), extrapolada eps->0 con eps^2 desde eps 0.2/0.1/0.05: "
          "|E_ext - E_exacta| < 1e-6",
    "A3": "orden de Trotter aparente (eps 0.2/0.1/0.05, Richardson en h) en [1.8, 2.2] para delta=1.0 y 1.5 "
          "(en delta=0.2 el sesgo de Trotter es del tamano del residuo de Nystrom: informativo)",
    "A4": "<r> de la transferencia, h->0 y eps->0: |<r>_ext - <r>_ex| < 1e-4",
    "B1": "radial (borde medio, r=1 en un nodo) frente a brentq: |E0-E| < 1e-8 (V0=2) y < 2e-8 (V0=1.3)",
    "B2": "orden de Trotter aparente del pozo: MEDIDO y declarado (sin criterio de aceptacion)",
    "B3": "pozo, transferencia h->0 (V3: mallas 0.02/0.01/0.005) y eps->0 con el orden medido: |E_ext - E_brentq| < 1e-5",
    "B4": "desplazamiento-inversion frente a tr.resolver (Lanczos): |dE| < 1e-10",
}

EPS_H = (0.2, 0.1, 0.05, 0.025)          # Hulthen (las tres primeras son las del plan)
EPS_P = (0.2, 0.1, 0.05, 0.025, 0.0125)  # pozo
HS = (0.04, 0.02, 0.01)
# V3 (hallazgo H2 de V1): en el pozo el error de Nystrom es de orden h^1 y E_h0 con (0.04, 0.02, 0.01) no estaba
# convergido a la cota de B3. Se anade h = 0.005 y E_h0 se extrapola con (0.02, 0.01, 0.005); el valor con
# (0.04, 0.02, 0.01) se guarda como E_h0_anterior.
HS_P = (0.04, 0.02, 0.01, 0.005)


def W_hulthen(delta):
    """W_H = 1/r - delta/(e^{delta r}-1). Para x = delta r < 1e-3 se usa la serie
    W_H = delta [1/2 - x/12 + x^3/720 - x^5/30240] (evita la cancelacion)."""
    def W(r):
        r = np.asarray(r, dtype=float)
        x = delta * r
        serie = delta * (0.5 - x / 12 + x**3 / 720 - x**5 / 30240)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            directo = 1.0 / r - delta / np.expm1(x)
        return np.where(x < 1e-3, serie, directo)
    return W


def ext_eps2(E):
    """Tres valores con eps en razon 2: orden aparente y extrapolacion con ley eps^2."""
    p = float(np.log2(abs(E[0] - E[1]) / abs(E[1] - E[2])))
    return p, float(E[2] + (E[2] - E[1]) / 3)


def ext_p(x1, x2, p):
    """Richardson con razon 2 y orden p: x2 es el de paso menor."""
    return float(x2 + (x2 - x1) / (2.0**p - 1))


def orden3(x):
    return float(np.log2(abs(x[0] - x[1]) / abs(x[1] - x[2])))


# ----------------------------------------------------------------------------- tarea del pozo (proceso aparte)
def tarea_pozo(args):
    V0, borde, R, h, eps, Eg = args
    t = time.perf_counter()
    Vp = radial.V_pozo(V0, 1.0, borde=borde)
    T, r = tr.matriz_T(R, h, eps, V=Vp)
    sig = float(np.exp(-eps * Eg))
    if h >= 0.01 - 1e-12:
        lam, v = eigsh(T.tocsc(), k=1, sigma=sig, which="LM", tol=0)
    else:
        # V3: con h = 0.005 la LU de SuperLU no cabe en memoria (V0=1.3, N=76999). sigma I - T es definida
        # positiva (sigma > lambda0) y en banda: factorizacion de Cholesky en banda (LAPACK) como OPinv.
        from scipy.linalg import cholesky_banded, cho_solve_banded
        from scipy.sparse.linalg import LinearOperator
        Td = T.todia(); N = T.shape[0]; nbw = int(max(Td.offsets))
        ab = np.zeros((nbw + 1, N))
        for kk, off in enumerate(Td.offsets):
            if off >= 0:
                ab[nbw - off, off:] = -Td.data[kk, off:]
        ab[nbw] += sig
        cb = cholesky_banded(ab, lower=False)
        op = LinearOperator((N, N), matvec=lambda x: -cho_solve_banded((cb, False), x), dtype=float)
        lam, v = eigsh(T, k=1, sigma=sig, which="LM", OPinv=op, tol=0)
        del ab, cb
    v = v[:, 0]
    if v.sum() < 0:
        v = -v
    E = float(-np.log(lam[0]) / eps)
    ob = tr._observables(r, v, R)
    return dict(V0=V0, borde=borde, R=R, h=h, eps=eps, E0=E, r_med=ob["r_med"], r2_med=ob["r2_med"],
                F12=ob["F12"], sobre_sigma=bool(E > Eg), signo_unico=bool(v.min() > -1e-10 * v.max()),
                N=len(r), nnz=int(T.nnz), tiempo=time.perf_counter() - t)


def main():
    T0 = time.perf_counter()
    print(f"Carga (loadavg): {os.getloadavg()}")
    out = dict(script="13_controles_hulthen_pozo.py", fecha="2026-10-27", unidades="hbar=m=1",
               criterios_declarados=CRIT_DECL)
    crit = []

    def C(nombre, valor, pasa, criterio):
        crit.append(dict(control=nombre, criterio=criterio, valor=valor, pasa=None if pasa is None else bool(pasa)))
        et = "MEDIDO" if pasa is None else ("PASA" if pasa else "NO PASA")
        print(f"  [{et}] {nombre}: {valor}  (criterio: {criterio})")

    # ========================================================================= A. Hulthen
    print("=== A.0 Resto W_H = V_H + 1/r acotado ===")
    import sympy as sp
    rs, ds = sp.symbols("r delta", positive=True)
    Ws = 1 / rs - ds / (sp.exp(ds * rs) - 1)
    lim0 = sp.limit(Ws, rs, 0)
    liminf = sp.limit(Ws, rs, sp.oo)
    serie = sp.series(Ws, rs, 0, 4).removeO()
    print(f"sympy: lim r->0 W_H = {lim0};  lim r->inf W_H = {liminf};  serie: {sp.simplify(serie)}")
    a0 = dict(lim0=str(lim0), liminf=str(liminf), serie=str(serie))
    rr = np.concatenate([np.logspace(-8, -2, 2000), np.linspace(0.01, 400, 400000)])
    for dl in (0.2, 1.0, 1.5, 2.0):
        w = W_hulthen(dl)(rr)
        dw = np.diff(w)
        a0[str(dl)] = dict(W_min=float(w.min()), W_max=float(w.max()), cota=dl / 2,
                           max_incremento=float(dw.max()), W_en_1e8=float(w[0]))
        ok = (w.min() >= -1e-14) and (w.max() <= dl / 2 + 1e-14) and (dw.max() <= 1e-14)
        C(f"A0 W_H delta={dl}", f"min {w.min():.3e}, max {w.max():.15f} (delta/2={dl/2}), max incremento {dw.max():.1e}",
          ok, CRIT_DECL["A0"])
    out["A0_resto"] = a0

    print("\n=== A.1 Radial frente a exacto ===")
    hul = {}
    for dl in (0.2, 1.0, 1.5):
        ex = radial.hulthen_exacto(dl)
        R = radial.caja_recomendada(ex["E"], entera=True)
        rad = radial.resolver_rich(radial.V_hulthen(dl), R, h=1 / 80)
        d = dict(R=R, kappa=ex["kappa"], E_exacta=ex["E"], r_exacto=ex["r_med"], r2_exacto=ex["r2_med"],
                 r_formula=ex["r_med_formula"], residuo_simbolico=ex["residuo_simbolico"],
                 E_radial=rad["E0"], r_radial=rad["r_med"], dE_radial=rad["E0"] - ex["E"],
                 dr_rel_radial=(rad["r_med"] - ex["r_med"]) / ex["r_med"])
        hul[dl] = d
        print(f"delta={dl}: R={R}  E exacta={ex['E']:.12f}  radial={rad['E0']:.12f} ({d['dE_radial']:+.1e})  "
              f"<r> exacto={ex['r_med']:.10f} radial={rad['r_med']:.10f}")
        C(f"A1 radial Hulthen delta={dl}", f"dE={d['dE_radial']:+.2e}, d<r>/<r>={d['dr_rel_radial']:+.2e}",
          abs(d["dE_radial"]) < 1e-8 and abs(d["dr_rel_radial"]) < 2e-7, CRIT_DECL["A1"])

    print("\n=== A.2 Transferencia con la accion de pares de Coulomb + W_H ===")
    tablas = {}
    for e in EPS_H:
        t = time.perf_counter()
        tablas[e] = pares.tabla_richardson(e)
        print(f"tabla eps={e}: {time.perf_counter()-t:.1f} s (cache {tablas[e].info['cache']})")
    for dl in (0.2, 1.0, 1.5):
        d = hul[dl]; R = d["R"]; Wf = W_hulthen(dl)
        filas = {}
        for e in EPS_H:
            f = {}
            for h in HS:
                t = time.perf_counter()
                o = tr.resolver(R, h, e, W=Wf, tabla=tablas[e])
                f[h] = dict(E0=o["E0"], r_med=o["r_med"], r2_med=o["r2_med"], F12=o["F12"], N=o["N"],
                            min_T=o["min_T"], tiempo=time.perf_counter() - t)
            E4, E2, E1 = f[0.04]["E0"], f[0.02]["E0"], f[0.01]["E0"]
            fila = dict(por_h={str(h): v for h, v in f.items()},
                        orden_h_E=orden3([E4, E2, E1]), E_rich_h4=(16 * E2 - E4) / 15, E_rich_h4_fina=(16 * E1 - E2) / 15)
            r4, r2_, r1 = f[0.04]["r_med"], f[0.02]["r_med"], f[0.01]["r_med"]
            ph = orden3([r4, r2_, r1])
            fila["orden_h_r"] = ph
            fila["r_rich_h"] = ext_p(r2_, r1, ph)
            filas[e] = fila
            print(f"delta={dl} R={R:.0f} eps={e}: E(h=.04,.02,.01)-ex = {E4-d['E_exacta']:+.3e}, {E2-d['E_exacta']:+.3e}, "
                  f"{E1-d['E_exacta']:+.3e}  orden h={fila['orden_h_E']:.2f}  Rich h^4 (0.02,0.04): "
                  f"{fila['E_rich_h4']-d['E_exacta']:+.3e}  (0.01,0.02): {fila['E_rich_h4_fina']-d['E_exacta']:+.3e}  "
                  f"<r>(h)-ex = {r4-d['r_exacto']:+.2e}, {r2_-d['r_exacto']:+.2e}, {r1-d['r_exacto']:+.2e} "
                  f"(orden h {ph:.2f}, ext {fila['r_rich_h']-d['r_exacto']:+.2e})  min T {f[0.02]['min_T']:.1e}")
        d["transferencia"] = {str(e): v for e, v in filas.items()}
        E3 = [filas[e]["E_rich_h4"] for e in EPS_H[:3]]
        p, ext = ext_eps2(E3)
        E3f = [filas[e]["E_rich_h4_fina"] for e in EPS_H[:3]]
        pf, extf = ext_eps2(E3f)
        E3raw = [filas[e]["por_h"]["0.02"]["E0"] for e in EPS_H[:3]]
        praw, extraw = ext_eps2(E3raw)
        Eb = [filas[e]["E_rich_h4"] for e in EPS_H[1:]]
        pb, extb = ext_eps2(Eb)
        rr3 = [filas[e]["r_rich_h"] for e in EPS_H[:3]]
        pr, extr = ext_eps2(rr3)
        d.update(orden_trotter=p, E_ext=ext, dE_ext=ext - d["E_exacta"],
                 orden_trotter_fina=pf, dE_ext_fina=extf - d["E_exacta"],
                 orden_trotter_h002_sin_rich=praw, dE_ext_h002_sin_rich=extraw - d["E_exacta"],
                 orden_trotter_eps_01_005_0025=pb, dE_ext_eps_01_005_0025=extb - d["E_exacta"],
                 E_menos_exacta_rich_h4=[filas[e]["E_rich_h4"] - d["E_exacta"] for e in EPS_H],
                 orden_trotter_r=pr, r_ext=extr, dr_ext=extr - d["r_exacto"])
        print(f"  delta={dl}: Trotter (Rich h^4 0.02/0.04, eps .2/.1/.05) orden {p:.3f}, ext {ext:.12f} "
              f"(dif {ext-d['E_exacta']:+.2e});  Rich 0.01/0.02: orden {pf:.3f}, dif {extf-d['E_exacta']:+.2e};  "
              f"h=0.02 sin Rich: orden {praw:.3f}, dif {extraw-d['E_exacta']:+.2e};  eps .1/.05/.025: orden {pb:.3f}, "
              f"dif {extb-d['E_exacta']:+.2e};  <r> ext {extr:.8f} (dif {extr-d['r_exacto']:+.2e}, orden eps {pr:.2f})")
        C(f"A2 Hulthen delta={dl} E extrapolada", f"{ext-d['E_exacta']:+.2e} (Rich h 0.01/0.02: {extf-d['E_exacta']:+.2e})",
          abs(ext - d["E_exacta"]) < 1e-6, CRIT_DECL["A2"])
        C(f"A3 Hulthen delta={dl} orden de Trotter", f"{p:.3f} (eps .1/.05/.025: {pb:.3f})",
          (1.8 <= p <= 2.2) if dl != 0.2 else None, CRIT_DECL["A3"])
        C(f"A4 Hulthen delta={dl} <r> extrapolado", f"{extr-d['r_exacto']:+.2e} (exacto {d['r_exacto']:.8f})",
          abs(extr - d["r_exacto"]) < 1e-4, CRIT_DECL["A4"])
    out["A_hulthen"] = {str(k): v for k, v in hul.items()}

    # ========================================================================= B. Pozo cuadrado
    print("\n=== B. Pozo cuadrado, transferencia sin U_C ===")
    pozo = {}
    tareas = []
    for V0 in (2.0, 1.3):
        ex = radial.pozo_exacto(V0)
        R = radial.caja_recomendada(ex["E"], entera=True)
        radm = radial.resolver_rich(radial.V_pozo(V0, 1.0, borde="media"), R, h=1 / 80)
        rade = radial.resolver_rich(radial.V_pozo(V0, 1.0, borde="estricta"), R, h=1 / 80)
        Eg = ex["E"] - (0.1 if V0 == 2.0 else 0.01)
        pozo[V0] = dict(R=R, E_exacta=ex["E"], k=ex["k"], kappa=ex["kappa"], r_exacto=ex["r_med"],
                        umbral_V0=ex["umbral_V0"], E_guess_sigma=Eg,
                        E_radial_media=radm["E0"], dE_radial_media=radm["E0"] - ex["E"],
                        r_radial_media=radm["r_med"],
                        E_radial_estricta=rade["E0"], dE_radial_estricta=rade["E0"] - ex["E"])
        print(f"V0={V0}: R={R}  E brentq={ex['E']:.12f}  kappa={ex['kappa']:.6f}  <r>={ex['r_med']:.8f}  "
              f"radial media={radm['E0']:.12f} ({radm['E0']-ex['E']:+.1e}); estricta {rade['E0']-ex['E']:+.1e}")
        tol = 1e-8 if V0 == 2.0 else 2e-8
        C(f"B1 radial pozo V0={V0}", f"{radm['E0']-ex['E']:+.2e} (convencion estricta: {rade['E0']-ex['E']:+.2e})",
          abs(radm["E0"] - ex["E"]) < tol, CRIT_DECL["B1"])
        for borde in ("media", "estricta"):
            for h in HS_P:
                for e in EPS_P:
                    tareas.append((V0, borde, R, h, e, Eg))
    tareas.sort(key=lambda a: (a[3], a[2], -a[4]))     # las de h = 0.005 y R grande, al final y repartidas
    t = time.perf_counter()
    with ProcessPoolExecutor(max_workers=3) as ex_:
        resul = list(ex_.map(tarea_pozo, tareas))
    print(f"{len(tareas)} autovalores del pozo en {time.perf_counter()-t:.1f} s (3 procesos)")
    tab = {(o["V0"], o["borde"], o["h"], o["eps"]): o for o in resul}
    malos = [k for k, o in tab.items() if not (o["sobre_sigma"] and o["signo_unico"])]
    print(f"  comprobacion: sigma por encima de lambda0 y autovector sin cambio de signo en todos: {not malos} {malos}")
    out["B_comprobacion_sigma"] = dict(fallos=[list(k) for k in malos])
    # B4: comparacion con tr.resolver
    chk = []
    for (V0, h, e) in ((2.0, 0.02, 0.1), (1.3, 0.04, 0.05)):
        o = tr.resolver(pozo[V0]["R"], h, e, V=radial.V_pozo(V0, 1.0, borde="media"))
        chk.append(dict(V0=V0, h=h, eps=e, E_lanczos=o["E0"], E_si=tab[(V0, "media", h, e)]["E0"],
                        dif=o["E0"] - tab[(V0, "media", h, e)]["E0"]))
        C(f"B4 desplazamiento-inversion V0={V0} h={h} eps={e}", f"{chk[-1]['dif']:+.1e}", abs(chk[-1]["dif"]) < 1e-10,
          CRIT_DECL["B4"])
    out["B4_comprobacion_lanczos"] = chk

    for V0 in (2.0, 1.3):
        P = pozo[V0]; Eex = P["E_exacta"]
        for borde in ("media", "estricta"):
            filas = {}
            for e in EPS_P:
                Es = [tab[(V0, borde, h, e)]["E0"] for h in HS_P]
                rs_ = [tab[(V0, borde, h, e)]["r_med"] for h in HS_P]
                ph_ant = orden3(Es[:3])
                Eh0_ant = ext_p(Es[1], Es[2], ph_ant)
                ph = orden3(Es[1:])
                Eh0 = ext_p(Es[2], Es[3], ph)
                filas[e] = dict(E_por_h={str(h): x for h, x in zip(HS_P, Es)}, r_por_h={str(h): x for h, x in zip(HS_P, rs_)},
                                orden_h=ph, E_h0=Eh0, E_h0_menos_exacta=Eh0 - Eex,
                                orden_h_anterior=ph_ant, E_h0_anterior=Eh0_ant, E_h0_anterior_menos_exacta=Eh0_ant - Eex,
                                E_h001_menos_exacta=Es[2] - Eex, E_h0005_menos_exacta=Es[3] - Eex, r_h001=rs_[2],
                                r_h0005=rs_[3])
                print(f"V0={V0} {borde:8s} eps={e:<7}: E(h=.04,.02,.01,.005)-ex = " + ", ".join(f"{x-Eex:+.4e}" for x in Es)
                      + f"  orden h (.02,.01,.005)={ph:.3f}  E(h->0)-ex={Eh0-Eex:+.4e}  "
                      f"[antes, con .04/.02/.01: orden {ph_ant:.3f}, {Eh0_ant-Eex:+.4e}]")
            Eh = [filas[e]["E_h0"] for e in EPS_P]
            p_loc = [orden3(Eh[i:i + 3]) for i in range(len(Eh) - 2)]
            E01 = [filas[e]["E_por_h"]["0.01"] for e in EPS_P]
            p_loc01 = [orden3(E01[i:i + 3]) for i in range(len(E01) - 2)]
            p_ult = p_loc[-1]
            Eext_p = ext_p(Eh[-2], Eh[-1], p_ult)
            Eext_2 = ext_p(Eh[-2], Eh[-1], 2.0)
            Eext_15 = ext_p(Eh[-2], Eh[-1], 1.5)
            # ajuste E = E* + a eps^p a los tres ultimos puntos (equivale a usar p_ult) y ajuste lineal en
            # eps^1.5 a los cinco: residuo
            x15 = np.array(EPS_P)**1.5
            A = np.vstack([np.ones_like(x15), x15]).T
            coef, res_, *_ = np.linalg.lstsq(A, np.array(Eh), rcond=None)
            Eplan = ext_eps2([Eh[0], Eh[1], Eh[2]])
            d = dict(filas={str(e): v for e, v in filas.items()}, E_h0=Eh, E_h0_menos_exacta=[x - Eex for x in Eh],
                     ordenes_locales_eps=p_loc, ordenes_locales_eps_h001=p_loc01,
                     E_ext_orden_medido=Eext_p, dE_ext_orden_medido=Eext_p - Eex,
                     dE_ext_eps2=Eext_2 - Eex, dE_ext_eps15=Eext_15 - Eex,
                     ajuste_eps15_5puntos=dict(E0=float(coef[0]), a=float(coef[1]), dE0=float(coef[0] - Eex)),
                     plan_eps_02_01_005=dict(orden=Eplan[0], dE_ext_eps2=Eplan[1] - Eex))
            P[borde] = d
            print(f"  V0={V0} {borde}: ordenes locales de Trotter (h->0): " + ", ".join(f"{x:.3f}" for x in p_loc)
                  + "  (con h=0.01 fijo: " + ", ".join(f"{x:.3f}" for x in p_loc01) + ")")
            print(f"     E_ext (orden medido {p_ult:.3f}) - ex = {Eext_p-Eex:+.2e};  con eps^2: {Eext_2-Eex:+.2e};  "
                  f"con eps^1.5: {Eext_15-Eex:+.2e};  ajuste eps^1.5 a 5 puntos: {coef[0]-Eex:+.2e};  "
                  f"plan (eps .2/.1/.05, ley eps^2): orden {Eplan[0]:.3f}, dif {Eplan[1]-Eex:+.2e}")
            C(f"B2 pozo V0={V0} {borde} orden de Trotter aparente", ", ".join(f"{x:.3f}" for x in p_loc),
              None, CRIT_DECL["B2"])
            # V3: lo mismo con el E_h0 anterior (mallas 0.04/0.02/0.01), para comparar
            Eh_ant = [filas[e]["E_h0_anterior"] for e in EPS_P]
            p_ant = orden3(Eh_ant[-3:])
            Eext_ant = ext_p(Eh_ant[-2], Eh_ant[-1], p_ant)
            coef_ant, *_ = np.linalg.lstsq(A, np.array(Eh_ant), rcond=None)
            d["V3_anterior_h004_002_001"] = dict(E_h0=Eh_ant, orden_eps=p_ant, dE_ext_orden_medido=Eext_ant - Eex,
                                                 ajuste_eps15_5puntos_dE0=float(coef_ant[0] - Eex))
            print(f"     [antes, E_h0 con .04/.02/.01: E_ext - ex = {Eext_ant-Eex:+.2e}; ajuste eps^1.5 a 5 puntos "
                  f"{coef_ant[0]-Eex:+.2e}]")
            if borde == "media":
                C(f"B3 pozo V0={V0} E extrapolada (orden medido)", f"{Eext_p-Eex:+.2e} (con ley eps^2: {Eext_2-Eex:+.2e}; "
                  f"ajuste eps^1.5 a 5 puntos: {coef[0]-Eex:+.2e}; antes, mallas .04/.02/.01: {Eext_ant-Eex:+.2e})",
                  abs(Eext_p - Eex) < 1e-5, CRIT_DECL["B3"])
                C(f"B3b pozo V0={V0} ajuste eps^1.5 a 5 puntos (V3)", f"{coef[0]-Eex:+.2e}",
                  abs(coef[0] - Eex) < 1e-5, "|E0_ajuste - E_brentq| < 1e-5 (control de robustez de B3, V3)")
        # <r> del pozo (informativo): h=0.01, eps menor
        # V3: limite h->0 con los dos bordes (en el continuo el valor en un nodo no cuenta: deben coincidir)
        P["V3_media_menos_estricta_E_h0"] = [P["media"]["E_h0"][i] - P["estricta"]["E_h0"][i] for i in range(len(EPS_P))]
        print(f"  V0={V0}: E_h0(media) - E_h0(estricta) por eps: " + ", ".join(f"{x:+.2e}" for x in P["V3_media_menos_estricta_E_h0"]))
        P["r_transferencia_h001_eps00125"] = tab[(V0, "media", 0.01, 0.0125)]["r_med"]
        P["dr_transferencia_h001_eps00125"] = P["r_transferencia_h001_eps00125"] - P["r_exacto"]
        print(f"  V0={V0}: <r> transferencia (media, h=0.01, eps=0.0125) = {P['r_transferencia_h001_eps00125']:.6f}, "
              f"exacto {P['r_exacto']:.6f} (dif {P['dr_transferencia_h001_eps00125']:+.2e})")
        # <r> del pozo (informativo, sin criterio): h -> 0 y eps -> 0 con los ordenes medidos de <r>
        rh0, ph_r = [], []
        for e in EPS_P:
            x = [tab[(V0, "media", h, e)]["r_med"] for h in HS_P[1:]]
            ph_r.append(orden3(x)); rh0.append(ext_p(x[1], x[2], ph_r[-1]))
        pe_r = [orden3(rh0[i:i + 3]) for i in range(len(rh0) - 2)]
        rext = ext_p(rh0[-2], rh0[-1], pe_r[-1])
        P["r_media"] = dict(r_h0=rh0, orden_h=ph_r, ordenes_eps=pe_r, r_ext=rext, dr_ext=rext - P["r_exacto"],
                            dr_h0=[x - P["r_exacto"] for x in rh0])
        print(f"  V0={V0}: <r> media: ordenes en h " + ", ".join(f"{x:.2f}" for x in ph_r) + "; <r>(h->0)-ex = "
              + ", ".join(f"{x-P['r_exacto']:+.2e}" for x in rh0) + "; ordenes en eps " + ", ".join(f"{x:.2f}" for x in pe_r)
              + f"; extrapolado - exacto = {rext-P['r_exacto']:+.2e}")
    out["B_pozo"] = {str(k): v for k, v in pozo.items()}
    out["B_tabla_cruda"] = [o for o in resul]
    out["C_pigs"] = "no hecho (tarea opcional, no bloqueante); pigs.py ya existe, queda para la Fase 3"
    out["criterios"] = crit
    out["n_pasa"] = sum(1 for c in crit if c["pasa"] is True)
    out["n_no_pasa"] = sum(1 for c in crit if c["pasa"] is False)
    out["n_medidos"] = sum(1 for c in crit if c["pasa"] is None)
    out["tiempo_total_s"] = time.perf_counter() - T0
    print(f"\nCriterios: {out['n_pasa']} pasan, {out['n_no_pasa']} no pasan, {out['n_medidos']} solo medidos.")
    for c in crit:
        if c["pasa"] is False:
            print("  NO PASA:", c["control"], c["valor"])
    fn = os.path.join(RES, "13_controles.json")
    with open(fn, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False, default=float)
    print("guardado", fn)

    # ========================================================================= figura
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    col = {0.2: "#2a78d6", 1.0: "#eb6834", 1.5: "#1baf7a", 2.0: "#8e44ad", 1.3: "#c0392b"}
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
    ax = axs[0]
    x = np.array(EPS_H)**2
    for dl, mk in ((0.2, "o"), (1.0, "s"), (1.5, "^")):
        y = np.abs(np.array(hul[dl]["E_menos_exacta_rich_h4"]))
        ax.loglog(x, y, marker=mk, color=col[dl], lw=2, ms=7,
                  label=fr"Hulthén $\delta={dl}$ (orden {hul[dl]['orden_trotter']:.2f})")
    xx = np.array([x.min(), x.max()])
    ax.loglog(xx, 6e-4 * xx, color="#52514e", ls="--", lw=1, label=r"pendiente 1 ($\propto\epsilon^2$)")
    ax.set_xlabel(r"$\epsilon^2$"); ax.set_ylabel(r"$|E_0(\epsilon)-E_{\rm exacta}|$")
    ax.set_title("Hulthén: acción de pares de Coulomb + $W_H$\n(Richardson en $h_{tab}$ y en $h$)")
    ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25, which="both")
    ax = axs[1]
    x = np.array(EPS_P)**2
    for V0, mk in ((2.0, "o"), (1.3, "s")):
        y = np.abs(np.array(pozo[V0]["media"]["E_h0_menos_exacta"]))
        ax.loglog(x, y, marker=mk, color=col[V0], lw=2, ms=7,
                  label=fr"pozo $V_0={V0}$ (órdenes " + ", ".join(f"{p:.2f}" for p in pozo[V0]["media"]["ordenes_locales_eps"]) + ")")
    xx = np.array([x.min(), x.max()])
    ax.loglog(xx, 0.25 * xx**0.75, color="#52514e", ls="--", lw=1, label=r"pendiente 3/4 ($\propto\epsilon^{3/2}$)")
    ax.loglog(xx, 0.5 * xx, color="#52514e", ls=":", lw=1, label=r"pendiente 1 ($\propto\epsilon^{2}$)")
    ax.set_xlabel(r"$\epsilon^2$"); ax.set_ylabel(r"$|E_0(\epsilon)-E_{\rm brentq}|$")
    ax.set_title("Pozo cuadrado: transferencia sin $U_C$\n(borde medio, extrapolado a $h\\to0$)")
    ax.legend(frameon=False, fontsize=8); ax.grid(alpha=0.25, which="both")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "13_controles.png"), dpi=150); plt.close(fig)
    print(f"figura guardada; tiempo total {time.perf_counter()-T0:.1f} s; carga {os.getloadavg()}")


if __name__ == "__main__":
    main()
