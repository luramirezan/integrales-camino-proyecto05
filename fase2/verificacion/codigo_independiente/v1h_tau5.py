"""V1 parte H: combinacion de las 8 cadenas de produccion tau=5 y las 16 de la replica frente a E_det propio."""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..','..'))  # raiz del repositorio
import json
import numpy as np
from scipy.stats import norm
p12 = json.load(open(_RAIZ + "/fase2/resultados/12_pigs.json"))
p12b = json.load(open(_RAIZ + "/fase2/resultados/12b_pigs_replica.json"))
Edet = json.load(open("resultados/v1e_proyeccion.json"))["n12_l0.5"]["5.0"]["E_mixto"]
a = p12["pigs"]["tau5"]["EL"]; b = p12b["replica"]["las_16"]["E"]
m = np.array(a["medias_cadena"] + b["medias_cadena"])
out = dict(E_det_propio=Edet)
out["prod_menos_replica_sigma"] = (a["media"] - b["media"]) / np.hypot(a["err"], b["err"])
w = np.array([1 / a["err"]**2, 1 / b["err"]**2])
mc = (w[0] * a["media"] + w[1] * b["media"]) / w.sum(); ec = 1 / np.sqrt(w.sum())
out.update(combinada_ponderada=mc, err_combinada=ec, sigma_combinada=(mc - Edet) / ec)
out.update(media_24_cadenas=m.mean(), err_24_cadenas=m.std(ddof=1) / np.sqrt(len(m)),
           sigma_24=(m.mean() - Edet) / (m.std(ddof=1) / np.sqrt(len(m))))
out["p_dos_colas_prod_vs_replica"] = 2 * norm.sf(abs(out["prod_menos_replica_sigma"]))
out["cadenas_prod_bajo_Edet"] = int(np.sum(np.array(a["medias_cadena"]) < Edet))
print(json.dumps(out, indent=1))
json.dump(out, open("resultados/v1h_tau5.json", "w"), indent=1)
