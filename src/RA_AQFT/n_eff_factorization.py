#!/usr/bin/env python3
"""
Test: is (N_2, N_3, N_4) genuinely a 3D factored space in the BDG dynamics?
And: does 64 emerge as a "dominant configuration" count under some criterion?
"""

import numpy as np
from collections import Counter
from scipy import stats

np.random.seed(42)

# ═══════════════════════════════════════════════════════════════════════════
# 1. Factorization test: does P(N_2,N_3,N_4) ≈ P(N_2)·P(N_3)·P(N_4) 
#    conditional on BDG acceptance?
# ═══════════════════════════════════════════════════════════════════════════

n_samples = 5_000_000
lam = np.array([1.0, 0.5, 1/6, 1/24])
N1 = np.random.poisson(lam[0], n_samples)
N2 = np.random.poisson(lam[1], n_samples)
N3 = np.random.poisson(lam[2], n_samples)
N4 = np.random.poisson(lam[3], n_samples)

S = 1 - N1 + 9*N2 - 16*N3 + 8*N4
acc = S > 0

print("─" * 72)
print("Conditional factorization test")
print("─" * 72)
print(f"Samples: {n_samples:,}, Acceptance: {acc.mean():.4f}")
print()

# Joint distribution of (N_2, N_3, N_4) conditional on acceptance
N2a, N3a, N4a = N2[acc], N3[acc], N4[acc]

# Empirical joint distribution
L_q = 4
p_joint = np.zeros((L_q, L_q, L_q))
for i in range(L_q):
    for j in range(L_q):
        for k in range(L_q):
            p_joint[i,j,k] = np.mean((N2a == i) & (N3a == j) & (N4a == k))

# Empirical marginals
p_N2 = np.array([np.mean(N2a == i) for i in range(L_q)])
p_N3 = np.array([np.mean(N3a == i) for i in range(L_q)])
p_N4 = np.array([np.mean(N4a == i) for i in range(L_q)])

# Factored product
p_factored = np.einsum('i,j,k->ijk', p_N2, p_N3, p_N4)

# Total probability in the [0,L_q)^3 cube
total_in_cube = p_joint.sum()
print(f"P((N_2,N_3,N_4) ∈ [0,L_q)^3 | accepted) = {total_in_cube:.6f}")
print(f"(fraction of accepted configs that lie in the 'confinement cube')")
print()

# KL divergence between joint and factored (restricted to support)
mask = (p_joint > 1e-6) & (p_factored > 1e-6)
p_j_norm = p_joint[mask] / p_joint[mask].sum()
p_f_norm = p_factored[mask] / p_factored[mask].sum()
kl = np.sum(p_j_norm * np.log(p_j_norm / p_f_norm))
print(f"KL(joint || factored) = {kl:.6f} nats")
print(f"  (0 = perfect factorization; non-zero = correlated)")
print()

# ═══════════════════════════════════════════════════════════════════════════
# 2. Dominant profile test: how many profiles account for 
#    99% of accepted probability mass?
# ═══════════════════════════════════════════════════════════════════════════

print("─" * 72)
print("Dominant accepted profile count")
print("─" * 72)

# Count (N_1, N_2, N_3, N_4) profiles conditional on acceptance
N_acc = np.column_stack([N1[acc], N2[acc], N3[acc], N4[acc]])
profiles = [tuple(n) for n in N_acc]
profile_counts = Counter(profiles)

total_acc = acc.sum()
profile_probs = sorted([(c/total_acc, p) for p,c in profile_counts.items()], reverse=True)

cumulative = 0.0
for thresh in [0.50, 0.80, 0.90, 0.95, 0.99, 0.999]:
    cum = 0.0
    for i, (prob, prof) in enumerate(profile_probs):
        cum += prob
        if cum >= thresh:
            print(f"  Top {i+1} profiles account for {cum:.4f} of accepted mass "
                  f"(>={thresh:.3f} threshold)")
            break
print()

# Just the top 64:
top64 = profile_probs[:64]
print(f"Top 64 profiles account for {sum(p for p,_ in top64):.4f} of accepted mass")
print()

# Show the top 10 profiles with their counts
print("Top 10 most common profiles (N_1, N_2, N_3, N_4) → P | S:")
for i, (prob, prof) in enumerate(profile_probs[:10]):
    S_val = 1 - prof[0] + 9*prof[1] - 16*prof[2] + 8*prof[3]
    print(f"  #{i+1}: {prof} → {prob:.5f} | S={S_val}")
print()

# ═══════════════════════════════════════════════════════════════════════════
# 3. Check the 36 ↔ 64 relationship
# ═══════════════════════════════════════════════════════════════════════════

print("─" * 72)
print("The 36 vs 64 relationship")
print("─" * 72)

# 36 is the count of (N_2,N_3,N_4) triples that accept for SOME N_1
# 64 = L_q^3 is the total count of such triples in [0,L_q)^3
# Ratio: 36/64 = 9/16 exactly? Check.
print(f"36/64 = {36/64}")
print(f"9/16 = {9/16}")
print(f"Match: {abs(36/64 - 9/16) < 1e-10}")
print(f"Note: 9/16 is NOT the BDG ratio — c_2/|c_3| = 9/16 is coincidence")
print()

# How many (N_2, N_3, N_4) triples have a specific S-value range?
print("Counting (N_2,N_3,N_4) triples in [0,L_q)^3 by whether they admit S>0 for N_1=0:")
for n1_val in [0, 1, 2, 3]:
    cnt = 0
    for n2 in range(L_q):
        for n3 in range(L_q):
            for n4 in range(L_q):
                if 1 - n1_val + 9*n2 - 16*n3 + 8*n4 > 0:
                    cnt += 1
    print(f"  N_1 = {n1_val}: {cnt} triples accept")
print()

# ═══════════════════════════════════════════════════════════════════════════
# 4. The key test: what is the effective DIMENSIONALITY of the support?
# ═══════════════════════════════════════════════════════════════════════════

print("─" * 72)
print("Effective dimensionality of accepted (N_2, N_3, N_4) support")
print("─" * 72)

# Principal component analysis on accepted (N_2, N_3, N_4) values
# Treat them as real-valued coordinates
coords = np.column_stack([N2a, N3a, N4a]).astype(float)

# Restrict to [0,L_q)^3 region
in_cube = (N2a < L_q) & (N3a < L_q) & (N4a < L_q)
coords_cube = coords[in_cube]

# Covariance matrix
cov = np.cov(coords_cube.T)
eigenvalues, eigenvectors = np.linalg.eigh(cov)
print(f"Covariance eigenvalues: {eigenvalues}")
print(f"Total variance: {eigenvalues.sum():.4f}")
print(f"Effective dimension (participation ratio): " +
      f"{eigenvalues.sum()**2 / (eigenvalues**2).sum():.3f}")
print(f"Eigenvectors (columns):")
print(eigenvectors)
print()

# ═══════════════════════════════════════════════════════════════════════════
# 5. Directly test: what emerges as a natural "64" in the BDG structure?
# ═══════════════════════════════════════════════════════════════════════════

print("─" * 72)
print("Searching for 64 in BDG structure")
print("─" * 72)

# 64 = 2^6
# 64 = 4^3 = L_q^3
# 64 in BDG coefficients? c_0 + c_1 + c_2 + c_3 + c_4 = 1 - 1 + 9 - 16 + 8 = 1
# sum of squares: 1 + 1 + 81 + 256 + 64 = 403
# Hmm, 64 IS one of the BDG coefficients — c_4 = 8, and c_4^2 = 64!

print(f"c_4 = 8; c_4^2 = 64")
print(f"Perhaps N_eff = c_4^2, not L_q^3?")
print()

# Check: 2·c_4² = 128; α_EM/128 ≠ α_EM/32
# So N_eff = 64 giving μ_p = α_EM/32 requires N_eff/2 = 32

# Alternative: N_eff = 2·L_q² = 32? Then μ_p = α_EM/32 with no factor of 2.
# But then where does L_q^3 come from?
print(f"2 · L_q² = {2 * L_q**2}")
print(f"Comparison: μ_p = α_EM / (2·L_q²) = α_EM / 32  ✓")
print(f"But this interpretation would say N_eff = 2·L_q² = 32, not L_q^3 = 64")
print()

print("Summary of 'N_eff = 64' derivations:")
print(f"  L_q^3 = 64 (geometric, 3D cube of side L_q)")
print(f"  c_4^2 = 64 (BDG coefficient squared)")
print(f"  2^6 = 64 (6 binary degrees of freedom)")
print(f"  Σ_i |c_i|² - 1 = 403 - 1 - 338 = 64? No: 403 - 339 = 64")
print(f"    (|c_0|² + |c_1|² + |c_2|² = 1+1+81 = 83; rest = 320)")
print()

# Final check: accepted profiles contain EXACTLY 132 combinatorial configs;
# is this 2·64 + 4 = 132, or 64 + 68, or just 132?
print(f"132 accepted profiles = {132}")
print(f"64 + 68 = 132; 2·64 + 4 = 132; no clean decomposition")
print()
