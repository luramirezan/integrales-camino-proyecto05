# Apantallamiento lineal de un gas ideal de Fermi a T finita: lambda^2 = eps0/(e^2 dn/dmu).
# Cociente con Debye clasico: (lambda/lambda_De)^2 = (n/kT)/(dn/dmu) = F_{1/2}(eta)/F_{-1/2}(eta) (F_j normalizadas con 1/Gamma(j+1)).
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma
from scipy.optimize import brentq
def F(j,eta): return quad(lambda x:x**j/(np.exp(x-eta)+1),0,np.inf)[0]/gamma(j+1)
# kT/E_F = t: E_F/kT = (3 sqrt(pi)/4 * F_{1/2}^{Gamma-norm}... use n ∝ Gamma(3/2) F_{1/2} T^{3/2}; E_F^{3/2} ∝ (2/3) n
def tEF(eta): return 1/((1.5*gamma(1.5)*F(0.5,eta))**(2/3))   # kT/E_F
for t in (0.71, 2.0, 10.0):
    eta=brentq(lambda e:tEF(e)-t,-20,50)
    r=np.sqrt(F(0.5,eta)/F(-0.5,eta))
    print(f"kT/E_F={t}: eta={eta:.4f}, lambda/lambda_De={r:.4f}, TF limite sqrt(2E_F/3kT)={np.sqrt(2/(3*t)):.4f}")
