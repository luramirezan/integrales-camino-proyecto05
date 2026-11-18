import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def V_yuk(r,d): return -np.exp(-d*r)/r
def V_ecsc(r,d): return -np.exp(-d*r)*np.cos(d*r)/r
def V_hul(r,d): return -d*np.exp(-d*r)/(1-np.exp(-d*r))
def Acoef(d,V,l=0):
    rmax=50/d; r0=1e-7
    y0=[r0**(l+1)*(1-r0/(l+1)), (l+1)*r0**l*(1-(l+2)/(l+1)*r0)]
    f=lambda r,y:[y[1], (2*V(r,d)+l*(l+1)/r**2)*y[0]]
    s=solve_ivp(f,[r0,rmax],y0,rtol=1e-12,atol=1e-30,method='DOP853')
    u,up=s.y[0,-1],s.y[1,-1]
    return (rmax*up+l*u)/rmax**(l+1)   # coefficient of r^{l+1}
for name,V,l,a,b in [("Yuk 1s",V_yuk,0,1.1,1.3),("Yuk 2s",V_yuk,0,0.25,0.4),("Yuk 2p",V_yuk,1,0.18,0.26),("Yuk 3d",V_yuk,2,0.07,0.12),("ECSC 1s",V_ecsc,0,0.6,0.9),("Hulthen 1s",V_hul,0,1.8,2.2)]:
    print(name, "%.8f"%brentq(lambda d:Acoef(d,V,l),a,b,xtol=1e-12))
