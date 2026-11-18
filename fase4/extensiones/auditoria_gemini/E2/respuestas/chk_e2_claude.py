# Cruce de cajas independiente: E0(R) por disparo con u(R)=0 (sin malla), cruce de y=2R^2E0/pi^2 para R y 2R.
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
dc=1.1906124210606; re=1.780632; c=0.74119177
def uR(E,d,R):
    f=lambda r,y:[y[1],2*(-np.exp(-d*r)/r-E)*y[0]]
    r0=1e-7; s=solve_ivp(f,[r0,R],[r0*(1-r0),1-2*r0],method='DOP853',rtol=1e-12,atol=1e-30)
    return s.y[0,-1]
def E0(d,R):
    # E0 near threshold: between -0.01 and (pi/R)^2/2
    lo,hi=-2e-3,(np.pi/R)**2/2*0.999
    Es=np.linspace(lo,hi,60); v=[uR(E,d,R) for E in Es]
    for i in range(len(Es)-1):
        if np.sign(v[i])!=np.sign(v[i+1]): return brentq(uR,Es[i],Es[i+1],args=(d,R),xtol=1e-16,rtol=1e-14)
y=lambda d,R:2*R*R*E0(d,R)/np.pi**2
for R in (200,):
    ds=brentq(lambda d:y(d,R)-y(d,2*R),1.1906,1.1912,xtol=1e-12)
    pred=np.pi**2*re/(16*c*R*R)+3*np.pi**2*re**2/(32*c*R**3)
    print(R,ds,ds-dc,pred)
