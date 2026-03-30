"""
D3 EXTENDED: Wyler formula for α_EM and BDG formula for α_s(m_Z).
"""
import math

c2, c4, d = 9, 8, 4
D = d + 1

# Wyler formula (α_EM)
alpha_EM_Wyler = (c2/(2**(d-1)*math.pi**d)) * (math.pi**D/(2**d*math.factorial(D)))**(1/d)

# BDG geometric mean formula (α_s at m_Z) — NEW
alpha_s_BDG = 1/math.sqrt(c2 * c4)

print(f"α_EM (Wyler): 1/{1/alpha_EM_Wyler:.3f}  PDG: 1/137.036  (0.0001%)")
print(f"α_s (BDG):    {alpha_s_BDG:.6f}  PDG: 0.11800    (0.13%)")
print()
print(f"f₀ = W_other/W_baryon × α_s(m_p)")
print(f"   = 17.32 × 0.31 ≈ 5.37  (target: 5.416)")
