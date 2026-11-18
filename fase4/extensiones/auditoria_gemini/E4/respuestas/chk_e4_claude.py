import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq
# zero-energy radial eq: u'' = [l(l+1)/r^2 - 2 e^{-d r}/r] u ; start r0 small with u=r^{l+1}(1 - r/(l+1)) (Coulomb Frobenius)
def sol(d,l,R=60.0):
    r0=1e-4; c1=-2/(2*(l+1))  # u=r^{l+1}(1+c1 r): c1 = -2*1/(2(l+1))? from (l+1)(l+2)-l(l+1)=2(l+1): c1*2(l+1) = -2 -> c1=-1/(l+1)
    u0=r0**(l+1)*(1+c1*r0); up=(l+1)*r0**l+(l+2)*c1*r0**(l+1)
    f=lambda r,y:[y[1],(l*(l+1)/r**2-2*np.exp(-d*r)/r)*y[0]]
    s=solve_ivp(f,[r0,R],[u0,up],method='DOP853',rtol=1e-12,atol=1e-30,dense_output=True)
    return s
def B(d,l,R=60.0):
    s=sol(d,l,R); u,up=s.y[0,-1],s.y[1,-1]
    # outside (V~0 for large R, d*R large) u = a r^{-l} + b r^{l+1}; W with r^{-l}: b
    # b = (u*l/R + up) / ((2l+1) R^l) ... solve 2x2
    M=np.array([[R**-l, R**(l+1)],[-l*R**(-l-1),(l+1)*R**l]]); a,b=np.linalg.solve(M,[u,up]); return b,a,s
for l,(lo,hi) in [(0,(0.25,0.4)),(1,(0.15,0.3)),(2,(0.085,0.1))]:
    R={0:120,1:200,2:400}[l]
    dc=brentq(lambda d:B(d,l,R)[0],lo,hi,xtol=1e-15)
    print(l,dc)
    if l==1:
        b,a,s=B(dc,l,R)
        n=quad(lambda r:s.sol(r)[0]**2,1e-4,R,limit=500)[0]+a**2/R  # tail int a^2 r^-2 from R
        A=a/np.sqrt(n); print('A^2',A**2)
        S=(quad(lambda r:np.exp(-dc*r)*s.sol(r)[0]**2,1e-4,R,limit=500)[0])/n; print('S',S)
