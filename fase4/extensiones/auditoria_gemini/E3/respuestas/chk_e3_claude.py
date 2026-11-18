# Comprobacion independiente de E3 (no usa su codigo): 1/a, delta_c, c y r_e por energia cero.
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
P={'yukawa':(lambda r,d:-np.exp(-d*r)/r, lambda r,d:np.exp(-d*r)),
   'ecsc':(lambda r,d:-np.exp(-d*r)*np.cos(d*r)/r, lambda r,d:np.exp(-d*r)*(np.cos(d*r)+np.sin(d*r))),
   'hulthen':(lambda r,d:-d*np.exp(-d*r)/(-np.expm1(-d*r)), None),
   'Hatomo':(lambda r,d:-(1/r+d/2)*np.exp(-d*r), lambda r,d:(1/r+d/2)*np.exp(-d*r)*r/r - 0.5*np.exp(-d*r)) }
# dV/dd: ecsc: V=-e^{-dr}cos(dr)/r -> dV/dd = e^{-dr}cos(dr) + e^{-dr} sin(dr) = e^{-dr}(cos+sin). OK
# Hatomo: V=-(1/r+d/2)e^{-dr} -> dV/dd = -1/2 e^{-dr} + (1/r+d/2) r e^{-dr} = e^{-dr}(1 + d r/2 - 1/2)
P['Hatomo']=(P['Hatomo'][0], lambda r,d:np.exp(-d*r)*(0.5+d*r/2))
def sol(name,d):
    V=P[name][0]; R=70/d
    f=lambda r,y:[y[1],2*V(r,d)*y[0]]
    r0=1e-6
    if name=='hulthen': y0=[r0*(1-r0),1-2*r0]
    else: y0=[r0*(1-r0),1-2*r0]   # V ~ -1/r cerca de 0 en todos
    s=solve_ivp(f,[r0,R],y0,method='DOP853',rtol=1e-13,atol=1e-30,dense_output=True)
    u,up=s.y[0,-1],s.y[1,-1]; alpha=u-up*R; beta=up   # u = alpha + beta r
    return s,alpha,beta,R
def inva(name,d):
    s,al,be,R=sol(name,d); return -be/al
for name,(lo,hi) in [('yukawa',(1.1,1.3)),('ecsc',(0.65,0.8)),('hulthen',(1.9,2.1)),('Hatomo',(1.7,1.9))]:
    dc=brentq(lambda d:inva(name,d),lo,hi,xtol=1e-14)
    s,al,be,R=sol(name,dc)        # en dc: beta=0, u -> alpha; phi0 = u/alpha -> 1
    phi=lambda r:s.sol(r)[0]/al
    re=2*quad(lambda r:1-phi(r)**2,1e-6,R,limit=1000)[0]
    if P[name][1] is not None:
        c=2*quad(lambda r:P[name][1](r,dc)*phi(r)**2,1e-6,R,limit=1000)[0]
    else: c=float('nan')
    h=1e-6; cnum=-(inva(name,dc+h)-inva(name,dc-h))/(2*h)
    print(f"{name}: delta_c={dc:.12f} r_e={re:.6f} c(HF)={c:.8f} c(num)={cnum:.8f}")
print('a e-H estatico (delta=2):', 1/inva('Hatomo',2.0))
