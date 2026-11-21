import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.linalg import eigh_tridiagonal
dc=1.1906124210606
e=1.602176634e-19; eps0=8.8541878188e-12; a0=5.29177210544e-11; hbar=1.054571817e-34; me=9.1093837139e-31
lam=a0/dc; print('lam_c/a0',1/dc,'pm',lam*1e12)
n1=eps0*1*e/(e*e*lam**2); print('n_e(1eV) cm^-3',n1*1e-6)
ND=4*np.pi/3*n1*lam**3; print('N_D(1eV)',ND, 'T for N_D=1', 1/ND)
T=13.6; n=n1*T; aws=(3/(4*np.pi*n))**(1/3); G=e*e/(4*np.pi*eps0*aws*T*e); EF=hbar**2*(3*np.pi**2*n)**(2/3)/(2*me)/e
print('Gamma',G,'T/EF',T/EF,'aws/lam',aws/lam)
print('2/dc',2/dc)
# deuteron
mp,mn=938.27208943,939.56542194; mu=mp*mn/(mp+mn); mpi=(2*139.57039+134.9768)/3
B=2.22456640
# ground energy of -e^{-d r}/r, l=0, dimensionless via FD with Richardson
def E0(d,R=None,h=None):
    k=1.0
    def ev(h,R):
        N=int(R/h)-1; r=h*np.arange(1,N+1)
        w=eigh_tridiagonal(1/h**2-np.exp(-d*r)/r,-0.5/h**2*np.ones(N-1),select='i',select_range=(0,0))[0][0]; return w
    R=R or 80/np.sqrt(max(1e-6,-2*ev(0.05,60)))+40
    a,b,c=ev(0.02,R),ev(0.01,R),ev(0.005,R)
    r1=(4*b-a)/3; r2=(4*c-b)/3; return (16*r2-r1)/15
# B = -E m_pi^2/(mu d^2)  (E dimless)
f=lambda d: -E0(d)*mpi**2/(mu*d*d)-B
dd=brentq(f,0.7,0.95,xtol=1e-9); print('delta_d',dd,'g/hbarc',mpi/(mu*dd),'mpi_c',mpi*dc/dd)
mL,ML,BL=805.9,1634.0,19.5; muL=ML/2
fL=lambda d:-E0(d)*mL**2/(muL*d*d)-BL
dL=brentq(fL,0.7,1.1,xtol=1e-9); gL=mL/(muL*dL); print('delta_L',dL,'gL',gL,'ratio',gL/(mpi/(mu*dd)))
print('chiral limit B',mu*(mpi/(mu*dd))**2/2)
h=1e-4
s=(np.log(-E0(dd*(1+h)))-np.log(-E0(dd*(1-h))))/(2*h); print('dlnB/dlnmpi fixed g',s)
print('K_deut model (mu varies with K_N=0.048, K_pi=0.494):', s*0.494 + (1-s)*0.048*1)
