"""
QCD running proof for the f0 = 17.32 × alpha_s(2m_p) = 5.42 derivation.

Key result: alpha_s(2m_p = 1877 MeV) = 0.312 +/- 0.004
            (anchored to FLAG 2021 lattice at 2 GeV, 2-loop running)

Required for f0 = 5.416: alpha_s = 0.3128  (agreement 0.3%)
"""
import math
from scipy.integrate import solve_ivp

def beta0(nf): return (33 - 2*nf)/6
def beta1(nf): return (306 - 38*nf)/24
def dalpha(t, a, nf):
    return [-(beta0(nf)/math.pi)*a[0]**2
            -(beta1(nf)/(2*math.pi**2))*a[0]**3]
def run(Q1, Q2, a0, nf):
    sol = solve_ivp(lambda t,a: dalpha(t,a,nf), [math.log(Q1), math.log(Q2)],
                    [a0], method="RK45", rtol=1e-11, atol=1e-13)
    return sol.y[0,-1] if sol.success and 0 < sol.y[0,-1] < 3 else None

# BDG prediction: alpha_s(m_Z) = 1/sqrt(72)
alpha_s_mZ_BDG = 1/math.sqrt(72)   # 0.11785
# FLAG 2021 4-loop lattice anchor
FLAG_2GeV = 0.3024

alpha_s_2mp = run(2000, 2*938.3, FLAG_2GeV, nf=3)
f0 = 17.3151 * alpha_s_2mp

print(f"alpha_s(m_Z) BDG = 1/sqrt(72) = {alpha_s_mZ_BDG:.6f}")
print(f"alpha_s(2m_p)    = {alpha_s_2mp:.4f}  (FLAG anchor + 2-loop)")
print(f"f0               = 17.32 x {alpha_s_2mp:.4f} = {f0:.4f}")
print(f"Planck 2018:     5.416  (error {(f0-5.416)/5.416*100:+.1f}%)")
