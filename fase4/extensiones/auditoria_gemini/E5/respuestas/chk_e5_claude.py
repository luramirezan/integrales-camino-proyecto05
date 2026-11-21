# Comprobacion independiente de E5: a(delta) por energia cero y el estimador a = -(2/delta^2) E[phi(r0)], r0 ~ Gamma(2,1/delta)
import numpy as np
from scipy.integrate import solve_ivp, quad
for d in (1.5,2.0,3.0,4.0,1.195,1.192,1.1907):
    R=60/d+40
    f=lambda r,y:[y[1],-2*np.exp(-d*r)/r*y[0]]
    s=solve_ivp(f,[1e-9,R],[1e-9,1.0],method='DOP853',rtol=1e-13,atol=1e-30,dense_output=True)
    u,up=s.y[0,-1],s.y[1,-1]; al=u-up*R; be=up      # u = al + be r ; normalizar u -> r - a : divide by be
    a=-al/be
    phi=lambda r:(s.sol(r)[0]/be)/r                 # phi -> 1 at infinity
    EW=quad(lambda r:d*d*r*np.exp(-d*r)*phi(r),1e-9,R,limit=500)[0]
    print(f"delta={d}: a={a:.6f}   -(2/d^2)E[phi]={-2/d**2*EW:.6f}  E[phi]={EW:.6f}")
