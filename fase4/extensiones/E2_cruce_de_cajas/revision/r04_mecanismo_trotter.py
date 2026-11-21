"""r04_mecanismo_trotter.py -- revision R2: el error de Trotter de la transferencia actua como un corrimiento del
umbral, delta_c(eps) = delta*_crudo(1600/3200; h=0.02, eps). Si es asi, E_crudo(delta, R; eps) ~ E_exacto(delta - s_eps, R)
con s_eps = delta*_crudo - delta*_exacto. Se comprueba en delta = 1.1906 y 1.1912 para R = 800 y 3200 (espectral).
Explica por que la receta aplicada a E0 (metodo A) es muy pesimista en R grande y por que el cruce (metodo B) no lo es.
Salida: resultados/r04_mecanismo_trotter.json"""
import json
import espectral as s
cru = json.load(open("../resultados/05_cruces.json"))
B = cru["transferencia_metodo_B"]["y"]["pares"][-1]["crudos"]
ex = json.load(open("resultados/r01_recalculo.json"))["cruces"]["y"][-1]["delta"]
out = []
for R in (800, 3200):
    for d in (1.1906, 1.1912):
        C = json.load(open(f"../resultados/04_transferencia_R{R}.json"))["celdas"][f"{d:g}"]["crudo"]
        for e in (0.2, 0.1, 0.05):
            sh = B[f"h0.02_eps{e:g}"] - ex
            Ep = s.E0(d - sh, R)["E0"]; Eex = s.E0(d, R)["E0"]
            Et = C[f"h0.02_eps{e:g}"]["E0"]
            f = dict(R=R, delta=d, eps=e, corrimiento=sh, z_corr=R * 0.741192 * sh, E_crudo=Et, E_exacto=Eex,
                     E_exacto_corrido=Ep, error_crudo_rel=(Et - Eex) / abs(Eex), resto_rel=(Et - Ep) / abs(Eex))
            out.append(f)
            print(f"R={R} d={d} eps={e}: corr {sh:.3e} (c R corr = {f['z_corr']:.3f}) E_tr={Et:+.4e} E_ex={Eex:+.4e} "
                  f"E_ex(d-corr)={Ep:+.4e}  error {f['error_crudo_rel']:+.3f}  resto {f['resto_rel']:+.4f}", flush=True)
json.dump(out, open("resultados/r04_mecanismo_trotter.json", "w"), indent=1, default=float)
