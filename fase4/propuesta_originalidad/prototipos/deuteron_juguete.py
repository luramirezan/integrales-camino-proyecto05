import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
def Abound(E,d):
    k=np.sqrt(-2*E); R=30/k; r0=1e-8
    f=lambda r,y:[y[1], 2*(-np.exp(-d*r)/r - E)*y[0]]
    s=solve_ivp(f,[r0,R],[r0*(1-r0),1-2*r0],rtol=1e-11,atol=1e-300,method='DOP853')
    u,up=s.y[0,-1],s.y[1,-1]
    return up+k*u   # decaying requires u'=-k u
def eps(d):
    return brentq(lambda E:Abound(E,d),-0.4999,-1e-9,xtol=1e-14)
hc=197.327; mN=938.918; mr=mN/2; mpi=138.04; B=2.22457
target=-B*mr/(hc*mpi/hc)**2/1.0  # E m/(hbar mu)^2  with mu in MeV: (hbar c mu)^2 -> mpi^2
target=-B*mr/mpi**2
print("target eps/delta^2",target)
dd=brentq(lambda d:eps(d)/d**2-target,0.5,1.18)
print("delta deuteron",dd, "eps",eps(dd))
g=mpi*hc/ (mr*dd) /hc  # g in units: delta=mu hbar^2/(m g) -> g/(hbar c)= (mpi)/(mr*delta)
print("g/(hbar c)=",mpi/(mr*dd), " ; m_pi critico (g fijo) =", mpi*1.1906124/dd, "MeV")
