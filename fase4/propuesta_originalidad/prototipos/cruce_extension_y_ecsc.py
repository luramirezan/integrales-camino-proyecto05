import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
Vy=lambda r,d:-np.exp(-d*r)/r
Ve=lambda r,d:-np.exp(-d*r)*np.cos(d*r)/r
def sol(E,d,R,V,dense=False):
    r0=1e-7
    f=lambda r,y:[y[1], 2*(V(r,d) - E)*y[0]]
    return solve_ivp(f,[r0,R],[r0*(1-r0),1-2*r0],rtol=1e-11,atol=1e-30,method='DOP853',dense_output=dense)
def E0(d,R,V): return brentq(lambda E:sol(E,d,R,V).y[0,-1],-0.02,np.pi**2/(2*R**2)*1.05,xtol=1e-16,rtol=1e-13)
def rmean(d,R,V):
    E=E0(d,R,V); s=sol(E,d,R,V,True); r=np.linspace(1e-7,R,200001); u=s.sol(r)[0]
    return np.trapezoid(r*u*u,r)/np.trapezoid(u*u,r)/R
print("universal <r>/R en umbral:",0.5-2/np.pi**2)
for R in [200,400,800]: print("Yukawa dc, R=%d  <r>/R=%.5f"%(R,rmean(1.1906124,R,Vy)))
Rs=[100,200,400,800]
for i in range(3):
    R1,R2=Rs[i],Rs[i+1]
    dc=brentq(lambda d:E0(d,R1,Ve)*R1**2-E0(d,R2,Ve)*R2**2,0.70,0.74,xtol=1e-10)
    print("ECSC cruce %d/%d: %.7f  2R^2E/pi^2=%.5f"%(R1,R2,dc,2*R2**2*E0(dc,R2,Ve)/np.pi**2))
