import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def uR(E,d,R):
    r0=1e-7
    f=lambda r,y:[y[1], 2*(-np.exp(-d*r)/r - E)*y[0]]
    s=solve_ivp(f,[r0,R],[r0*(1-r0),1-2*r0],rtol=1e-11,atol=1e-30,method='DOP853')
    return s.y[0,-1]
def E0(d,R):
    hi=np.pi**2/(2*R**2)*1.05
    lo=-0.02
    return brentq(lambda E:uR(E,d,R),lo,hi,xtol=1e-16,rtol=1e-13)
Rs=[50,100,200,400,800]
ds=[1.17,1.18,1.185,1.19,1.1906,1.195,1.20,1.21]
tab={}
for d in ds:
    row=[2*R*R*E0(d,R)/np.pi**2 for R in Rs]; tab[d]=row
    print(d, " ".join("%.5f"%x for x in row))
print("valor universal en el umbral 2R^2E/pi^2 = 1/4")
# crossing between consecutive R
for i in range(len(Rs)-1):
    R1,R2=Rs[i],Rs[i+1]
    g=lambda d:E0(d,R1)*R1**2-E0(d,R2)*R2**2
    dc=brentq(g,1.17,1.21,xtol=1e-10)
    print("cruce R=%d/%d: delta*=%.7f  2R^2E/pi^2=%.5f"%(R1,R2,dc,2*R2**2*E0(dc,R2)/np.pi**2))
