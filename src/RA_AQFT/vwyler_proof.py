"""V_eff(mu=1)=1: proof that the BDG Wyler volume factor is unity at mu=1."""
import math
c0,c1,c2,c3,c4 = 1,-1,9,-16,8
assert c1+c2+c3+c4 == 0          # d'Alembertian: Σc_k=0
V_eff_at_1 = c0 + c1+c2+c3+c4   # = 1+0 = 1
assert V_eff_at_1 == 1
T = c2 * V_eff_at_1 * c4         # path weight = 72
alpha_s_mZ = 1/math.sqrt(T)
print(f"V_eff(1)   = {V_eff_at_1}")
print(f"T(ph->q)   = {T}")
print(f"alpha_s    = 1/sqrt({T}) = {alpha_s_mZ:.6f}")
print(f"PDG alpha_s = 0.118000  (error {abs(alpha_s_mZ-0.118)/0.118*100:.2f}%)")
