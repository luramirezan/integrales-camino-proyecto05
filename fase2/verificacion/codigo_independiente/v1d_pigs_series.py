"""V1 parte D: reanalisis propio de las series PIGS guardadas (12_pigs_series.npz).
Medias, error por binning de Flyvbjerg-Petersen (meseta), jackknife entre cadenas,
tiempo de autocorrelacion integrado con ventana automatica propia (c=6).
Las series se leen como DATOS; no se importa codigo del proyecto."""
import os as _os
_RAIZ = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..','..','..'))  # raiz del repositorio
import json
import numpy as np

z = np.load(_RAIZ + "/fase2/resultados/12_pigs_series.npz")

def binning(x):
    """Error de la media por binning sucesivo; devuelve la lista y el valor de meseta (max de los
    niveles con al menos 64 bins)."""
    x = np.asarray(x, float)
    errs = []
    while len(x) >= 64:
        errs.append(np.std(x, ddof=1) / np.sqrt(len(x)))
        x = 0.5 * (x[: len(x) // 2 * 2: 2] + x[1: len(x) // 2 * 2: 2])
    return errs, max(errs)

def tau_int(x, c=6.0):
    x = np.asarray(x, float) - np.mean(x)
    n = len(x)
    f = np.fft.rfft(x, 2 * n)
    acf = np.fft.irfft(f * np.conj(f))[:n] / (np.arange(n, 0, -1))
    acf /= acf[0]
    t = 0.5
    for W in range(1, n):
        t += acf[W]
        if W >= c * t:
            break
    return float(t)

def analiza(pref, semillas, obs, descarte=0):
    medias, eb, taus = [], [], []
    for s in semillas:
        x = z[f"{pref}_{s}_{obs}"].astype(float)[descarte:]
        medias.append(x.mean())
        eb.append(binning(x)[1])
        taus.append(tau_int(x))
    medias = np.array(medias); eb = np.array(eb)
    m = medias.mean()
    k = len(medias)
    err_bin = float(np.sqrt(np.sum(eb**2)) / k)
    err_cad = float(np.std(medias, ddof=1) / np.sqrt(k)) if k > 1 else float("nan")
    # jackknife sobre cadenas (igual a err_cad para la media, se deja como control)
    jk = np.array([(m * k - medias[i]) / (k - 1) for i in range(k)]) if k > 1 else np.array([m])
    err_jk = float(np.sqrt((k - 1) / k * np.sum((jk - jk.mean())**2))) if k > 1 else float("nan")
    return dict(media=float(m), err_binning=err_bin, err_cadenas=err_cad, err_jackknife=err_jk,
                err=float(np.nanmax([err_bin, err_cad])), tau_int_medio=float(np.mean(taus)),
                medias_cadena=medias.tolist())

out = {}
sem = list(range(20262000, 20262008))
for obs in ("EL", "rmid", "r2mid"):
    out[f"prod02_{obs}"] = analiza("prod02", sem, obs)
    out[f"coul_{obs}"] = analiza("coul", [20262008], obs)
# descarte adicional del 10 % inicial (control de termalizacion)
for obs in ("EL", "rmid", "r2mid"):
    out[f"prod02_{obs}_descarte10"] = analiza("prod02", sem, obs, descarte=5000)
x = z["coul_20262008_EL"].astype(float)
out["coul_EL_var"] = float(np.var(x)); out["coul_EL_maxdesv"] = float(np.max(np.abs(x + 0.5)))
for k, v in out.items():
    print(k, v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "medias_cadena"})
json.dump(out, open("resultados/v1d_pigs.json", "w"), indent=1)
