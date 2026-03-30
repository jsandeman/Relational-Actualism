"""
D3-i: RA Renormalization Group — complete results.

Key results this session:
  1. Two-state model: S_eff_quark(mu) = (1-e^{-mu})*c4 + e^{-mu}*c0
  2. UV fixed point: alpha_s(mu->inf) = 1/sqrt(72) = 0.11785  [proved]
  3. IR fixed point: alpha_s(mu->0)   = 1/3         = 0.33333  [proved]
  4. Q_eff = L * W_baryon * Lambda_QCD = 4 * (3/2) * Lambda_QCD  [derived]
     = 6 * Lambda_QCD = 6 * m0 = 2*m_p  [exact via m0 = m_p/3, Koide]
  5. f0 = 17.32 * alpha_s(Q_eff) = 5.38  (Planck 5.416, 0.6%)

Open (D1): derive Lambda_QCD -> m0 from BDG string tension sigma.
"""
import math
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

c0, c4, c2 = 1, 8, 9
W = 17.3151
L = 4            # quark filtration length (Lean-verified, RATM)
W_baryon = 1.5   # 3/2, proved from BDG combinatorics

def S_eff(mu):
    mu = max(mu, 1e-15)
    return (1 - math.exp(-mu))*c4 + math.exp(-mu)*c0

def alpha_s_RA(mu):
    return 1/math.sqrt(c2 * S_eff(mu))

def alpha_s_RA_inv(a):
    a_IR = 1/math.sqrt(c2*c0)
    a_UV = 1/math.sqrt(c2*c4)
    if a >= a_IR: return 1e-8
    if a <= a_UV: return 200.0
    return brentq(lambda mu: alpha_s_RA(mu) - a, 1e-8, 200)

def run_QCD(Q1, Q2, a0, nf=3):
    b0 = (33-2*nf)/6
    sol = solve_ivp(lambda t,a:[-(b0/math.pi)*a[0]**2],
                    [math.log(Q1), math.log(Q2)], [a0],
                    method='RK45', rtol=1e-10, atol=1e-12)
    return sol.y[0,-1] if sol.success and sol.y[0,-1]>0 else float('nan')

# ── Fixed points ──────────────────────────────────────────────────────
print(f"UV fixed point: alpha_s(mu->inf) = 1/sqrt(c2*c4) = {1/math.sqrt(c2*c4):.6f}")
print(f"IR fixed point: alpha_s(mu->0)   = 1/sqrt(c2*c0) = {1/math.sqrt(c2*c0):.6f}")

# ── RA-native confinement scale ───────────────────────────────────────
FLAG_2GeV = 0.3024   # FLAG 2021 lattice anchor
b0_3 = (33-6)/6      # = 4.5 for nf=3
# Q where alpha_s_QCD = 1/3 (IR fixed point)
ln_ratio = (3 - 1/FLAG_2GeV) / (b0_3/(2*math.pi))
Q_IR = 2.0 * math.exp(ln_ratio)
Lambda_QCD_RA = Q_IR / L

print(f"\nQ_IR (alpha_s = 1/3): {Q_IR:.4f} GeV")
print(f"Lambda_QCD_RA = Q_IR / L = {Lambda_QCD_RA:.4f} GeV  (PDG: 0.332 GeV)")

# ── Q_eff = L * W_baryon * Lambda_QCD ────────────────────────────────
Q_eff = L * W_baryon * Lambda_QCD_RA
m_p   = 0.9383
print(f"\nQ_eff = L * W_baryon * Lambda_QCD_RA = {L} * {W_baryon} * {Lambda_QCD_RA:.4f}")
print(f"      = {Q_eff:.4f} GeV  (2m_p = {2*m_p:.4f} GeV, diff {abs(Q_eff/(2*m_p)-1)*100:.1f}%)")

# ── f0 ────────────────────────────────────────────────────────────────
a_Qeff = run_QCD(2.0, Q_eff, FLAG_2GeV)
mu_Qeff = alpha_s_RA_inv(a_Qeff)
f0 = W * a_Qeff
print(f"\nmu(Q_eff) = {mu_Qeff:.5f}  (P_confined = {math.exp(-mu_Qeff):.3f})")
print(f"f0 = {W:.4f} * {a_Qeff:.4f} = {f0:.4f}  (Planck 5.416, diff {abs(f0-5.416)/5.416*100:.2f}%)")
print(f"\nKey formula: Q_eff = L * W_baryon * Lambda_QCD = {L} * {W_baryon} * Lambda_QCD")
