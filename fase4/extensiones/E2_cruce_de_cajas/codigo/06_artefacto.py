"""06_artefacto.py -- prueba "artefacto frente a estado debil" y controles negativos (E2). Determinista, ~3 min.

(a) delta = 1.19: el signo de E0 dice "no ligado" en todas las cajas R <= 1600 (radial, disparo y transferencia), aunque
    a_s = +2204 (ligado). El cruce no se equivoca: y(1.19, R) > y(1.19, 2R) en todos los pares (la curva baja con R, lado
    ligado) y delta*(R, 2R) > 1.19 en todos los pares (05_cruces.json).
(b) Controles negativos, con el disparo y el radial h = 1/160 (R = 50 ... 1600):
    - Yukawa repulsivo V = +e^{-delta r}/r, delta en [0.5, 2.0]: nunca liga; a > 0 pequeno (tipo esfera dura), asi que
      y = R^2/(R - a)^2 > 1 baja hacia 1 con R: y(R) > y(2R) siempre, sin cruce y lejos de 1/4;
    - Yukawa atractivo con delta en [1.4, 2.0] (no ligado): sin cruce;
    - ligado profundo, delta en [0.8, 1.0]: y(R) > y(2R) siempre (sin cruce). Aqui solo el radial para R >= 400, porque el
      disparo hacia afuera pierde precision cuando kappa R es grande.
    Criterio K12 (fijado antes): ningun cambio de signo de y(R) - y(2R) en cada barrido.
Salida: resultados/06_artefacto.json
"""
import sys, time
import numpy as np
import e2comun as c

sys.stdout = c.Tee("06_artefacto")
T0 = time.perf_counter()
out = dict(script="06_artefacto.py", fecha=c.ahora())

# ------------------------------------------------------------------ (a) delta = 1.19
dis, rad = c.cargar("02_disparo"), c.cargar("03_radial")
cr = c.cargar("05_cruces")
a = {}
for R in c.RS:
    fila = dict(R=R, E_disparo=dis["celdas"]["1.19"][f"R{R}"]["E0"], E_radial160=rad["celdas"]["h160"]["1.19"][f"R{R}"]["E0"],
                err_radial160=rad["celdas"]["h160"]["1.19"][f"R{R}"]["err"])
    try:
        t = c.cargar(f"04_transferencia_R{R}")["celdas"]["1.19"]
        fila.update(E_transferencia=t["E_mejor"], err_transferencia=t["err"])
    except (FileNotFoundError, KeyError):
        pass
    fila["y_disparo"] = c.y_de(fila["E_disparo"], R)
    a[R] = fila
    print(f"delta=1.19 R={R:<5} E_disp={fila['E_disparo']:+.6e} E_rad={fila['E_radial160']:+.6e} "
          f"E_tr={fila.get('E_transferencia', float('nan')):+.6e} y={fila['y_disparo']:.5f}")
Rmax_pos = [R for R in c.RS if R <= 1600]
signo_engana = all(a[R]["E_disparo"] > 0 and a[R]["E_radial160"] > a[R]["err_radial160"] and
                   (("E_transferencia" not in a[R]) or a[R]["E_transferencia"] > a[R]["err_transferencia"])
                   for R in Rmax_pos)
baja = [a[c.RS[i]]["y_disparo"] > a[c.RS[i + 1]]["y_disparo"] for i in range(len(c.RS) - 1)]
cruces = {}
for fu in ("disparo", "radial_h160", "transferencia"):
    cruces[fu] = [f["delta"] for f in cr["fuentes"][fu]["y"]["pares"]]
todos_mayores = all(d > 1.19 for v in cruces.values() for d in v)
out["delta_119"] = dict(filas=list(a.values()), a_s=dis["energia_cero"]["1.19"]["a"],
                        signo_dice_no_ligado_hasta_1600=bool(signo_engana), y_baja_con_R_en_cada_par=baja,
                        cruces=cruces, todos_los_cruces_mayores_que_119=bool(todos_mayores),
                        R_primer_E_negativo_disparo=min([R for R in c.RS if a[R]["E_disparo"] < 0], default=None))
print(f"signo engana hasta R=1600: {signo_engana}; y baja con R en cada par: {baja}; todos los cruces > 1.19: {todos_mayores}")


# ------------------------------------------------------------------ (b) controles negativos
def V(delta, signo):
    return lambda r: signo * np.exp(-delta * r) / r


def barrido(nombre, deltas, signo, Rs, R_disp_max):
    res = dict(deltas=list(deltas), Rs=list(Rs), y_radial={}, y_disparo={})
    for d in deltas:
        yr, yd = [], []
        for R in Rs:
            x = c.radial.resolver_rich(V(d, signo), R, h=1 / 160, nev=1)
            yr.append(c.y_de(x["E0"], R))
            if R <= R_disp_max:
                yd.append(c.y_de(c.disparo_E0(d, R, x["E0"], signo=signo, ancho=abs(x["E0"]) * 1e-3 + 1e-14)["E0"], R))
        res["y_radial"][f"{d:g}"] = yr; res["y_disparo"][f"{d:g}"] = yd
    Y = np.array([res["y_radial"][f"{d:g}"] for d in deltas])
    D = Y[:, :-1] - Y[:, 1:]                       # y(R) - y(2R), filas = delta, columnas = par
    cambios = [int(np.sum(np.sign(D[1:, j]) != np.sign(D[:-1, j]))) for j in range(D.shape[1])]
    res["D_min_abs_por_par"] = [float(np.min(np.abs(D[:, j]))) for j in range(D.shape[1])]
    res["signo_D_por_par"] = [int(np.sign(D[0, j])) for j in range(D.shape[1])]
    res["cambios_de_signo_por_par"] = cambios
    Yd = [res["y_disparo"][f"{d:g}"] for d in deltas]
    res["max_dif_radial_disparo"] = float(max(abs(Y[i, k] - Yd[i][k]) for i in range(len(deltas)) for k in range(len(Yd[i]))))
    res["sin_cruce"] = bool(all(k == 0 for k in cambios))
    res["y_min"] = float(Y.min()); res["y_max"] = float(Y.max())
    print(f"{nombre}: cambios de signo por par {cambios}; signo {res['signo_D_por_par']}; min|D| "
          f"{['%.2e' % x for x in res['D_min_abs_por_par']]}; max|radial-disparo| {res['max_dif_radial_disparo']:.1e}; y en [{res['y_min']:.4g}, {res['y_max']:.4g}]",
          flush=True)
    return res


RSn = (50, 100, 200, 400, 800, 1600)
out["repulsivo"] = barrido("repulsivo", np.linspace(0.5, 2.0, 7), +1.0, RSn, 1600)
out["no_ligado"] = barrido("atractivo no ligado", np.linspace(1.4, 2.0, 7), -1.0, RSn, 1600)
out["ligado_profundo"] = barrido("ligado profundo", np.linspace(0.8, 1.0, 5), -1.0, RSn, 200)
out["K12_pasa"] = bool(out["repulsivo"]["sin_cruce"] and out["no_ligado"]["sin_cruce"] and out["ligado_profundo"]["sin_cruce"])
out["K13_pasa"] = bool(signo_engana and todos_mayores)
out["tiempo_s"] = time.perf_counter() - T0
c.guardar("06_artefacto", out)
print(f"K12 {out['K12_pasa']}  K13 {out['K13_pasa']}  tiempo {out['tiempo_s']:.0f} s")
