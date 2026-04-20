#!/usr/bin/env python3
"""
Test the alternative hypothesis: N_eff = 2 · L_q² = 32

Motivation: participation ratio of depth-space covariance is 1.31, not 3.
The dominant profiles have N_3 = 0 almost always; N_2 is the primary direction.
Maybe the effective depth-space is 2D, not 3D.

If N_eff = 32 = 2 · L_q², then:
  - The "2" could be particle-antiparticle or spin degeneracy
  - The L_q² could be 2D confinement area (in Planck units)
  - μ_p = α_EM / N_eff = α_EM / 32 directly (no extra factor of 2)

If this is right, the proton's confinement region is 2D, not 3D — which 
would correspond to a "membrane" or "holographic" structure at the confinement
scale, consistent with string-like confinement pictures in QCD.
"""

import numpy as np
from collections import Counter

np.random.seed(42)
n_samples = 5_000_000

# Sample BDG profile at mu=1
lam = np.array([1.0, 0.5, 1/6, 1/24])
N1 = np.random.poisson(lam[0], n_samples)
N2 = np.random.poisson(lam[1], n_samples)
N3 = np.random.poisson(lam[2], n_samples)
N4 = np.random.poisson(lam[3], n_samples)

S = 1 - N1 + 9*N2 - 16*N3 + 8*N4
acc = S > 0

# ═══════════════════════════════════════════════════════════════════════════
# Test 1: Marginal distribution of each N_k conditional on acceptance
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("Marginal distributions P(N_k | accepted)")
print("=" * 72)
N1a, N2a, N3a, N4a = N1[acc], N2[acc], N3[acc], N4[acc]

print(f"\nN_1 (expected large spread, not confined):")
for v in range(8):
    p = np.mean(N1a == v)
    print(f"  P(N_1 = {v} | acc) = {p:.4f}  {'█' * int(p*50)}")

print(f"\nN_2 (expected confined to [0, L_q)):")
for v in range(6):
    p = np.mean(N2a == v)
    print(f"  P(N_2 = {v} | acc) = {p:.4f}  {'█' * int(p*50)}")

print(f"\nN_3 (expected nearly always 0 — heavily penalized):")
for v in range(4):
    p = np.mean(N3a == v)
    print(f"  P(N_3 = {v} | acc) = {p:.4f}  {'█' * int(p*50)}")

print(f"\nN_4 (expected small, occasionally 1):")
for v in range(4):
    p = np.mean(N4a == v)
    print(f"  P(N_4 = {v} | acc) = {p:.4f}  {'█' * int(p*50)}")

# ═══════════════════════════════════════════════════════════════════════════
# Test 2: If depth-space is EFFECTIVELY 2D, which coordinates define it?
# ═══════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("Effective 2D structure test")
print("=" * 72)

# The dominant "direction" of variation is N_2 (from PCA).
# The secondary direction might be N_4 (the next least penalized)
# or N_1 (the "spatial" negative coefficient direction).

# Count distinct (N_2, N_4) configurations that are accepted
# (marginalizing out N_1 and N_3)
accepted_24_combos = set()
for n1 in range(10):
    for n3 in range(4):
        for n2 in range(6):
            for n4 in range(4):
                if 1 - n1 + 9*n2 - 16*n3 + 8*n4 > 0:
                    accepted_24_combos.add((n2, n4))
print(f"\nDistinct (N_2, N_4) pairs accepted for some (N_1, N_3): {len(accepted_24_combos)}")

# Count distinct (N_1, N_2) configurations  
accepted_12_combos = set()
for n3 in range(4):
    for n4 in range(4):
        for n1 in range(10):
            for n2 in range(6):
                if 1 - n1 + 9*n2 - 16*n3 + 8*n4 > 0:
                    accepted_12_combos.add((n1, n2))
print(f"Distinct (N_1, N_2) pairs accepted for some (N_3, N_4): {len(accepted_12_combos)}")

# Restrict to [0, L_q)² for each pair
L_q = 4
for coords, name in [(('N_2', 'N_4'), 'N_2, N_4'),
                      (('N_1', 'N_2'), 'N_1, N_2'),
                      (('N_2', 'N_3'), 'N_2, N_3'),
                      (('N_1', 'N_4'), 'N_1, N_4')]:
    idx = {'N_1': 0, 'N_2': 1, 'N_3': 2, 'N_4': 3}
    i, j = idx[coords[0]], idx[coords[1]]
    pairs = set()
    for n1 in range(L_q):
        for n2 in range(L_q):
            for n3 in range(L_q):
                for n4 in range(L_q):
                    vals = (n1, n2, n3, n4)
                    if 1 - n1 + 9*n2 - 16*n3 + 8*n4 > 0:
                        pairs.add((vals[i], vals[j]))
    print(f"  Distinct ({name}) pairs in [0,L_q)² accepted (marg. over others in [0,L_q)): {len(pairs)}")

# ═══════════════════════════════════════════════════════════════════════════
# Test 3: Count of BDG score levels
# ═══════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("BDG score level structure")
print("=" * 72)

# Count distinct S values in accepted profiles in [0, L_q)^4
accepted_profiles = []
for n1 in range(L_q):
    for n2 in range(L_q):
        for n3 in range(L_q):
            for n4 in range(L_q):
                S_val = 1 - n1 + 9*n2 - 16*n3 + 8*n4
                if S_val > 0:
                    accepted_profiles.append((n1, n2, n3, n4, S_val))

distinct_S = set(p[4] for p in accepted_profiles)
print(f"Distinct S values in [0,L_q)^4 acceptance: {len(distinct_S)}")
print(f"S value range: [{min(distinct_S)}, {max(distinct_S)}]")

# Possibly 64 arises as 2^6 where 6 is the number of distinct "BDG levels"?
# Check how many distinct S values up to some threshold
score_counts_bounded = Counter(p[4] for p in accepted_profiles)
running_sum = 0
print(f"\nCumulative count of profiles by S level (first reaches 64 at S ≤ ?):")
for s in sorted(score_counts_bounded.keys()):
    running_sum += score_counts_bounded[s]
    if running_sum <= 70:
        print(f"  S ≤ {s}: {running_sum} profiles")

# ═══════════════════════════════════════════════════════════════════════════
# Test 4: Count at specific S values
# ═══════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("Profile count restricted to N_3 = 0 only (the dominant subspace)")
print("=" * 72)

# If N_3 = 0 is strongly preferred, how many accepting (N_1, N_2, N_4) are there 
# with all in [0, L_q)?
n3_zero_count = 0
for n1 in range(L_q):
    for n2 in range(L_q):
        for n4 in range(L_q):
            if 1 - n1 + 9*n2 + 8*n4 > 0:
                n3_zero_count += 1
print(f"Accepted profiles with N_3 = 0, others in [0,L_q): {n3_zero_count}")
print(f"  = L_q³? {n3_zero_count == L_q**3}")

# What about N_3 = 0 AND N_4 = 0 (even more restrictive)?
restrict_count = 0
for n1 in range(L_q):
    for n2 in range(L_q):
        if 1 - n1 + 9*n2 > 0:
            restrict_count += 1
print(f"Accepted profiles with N_3 = N_4 = 0, others in [0,L_q): {restrict_count}")

# Or N_1 fixed and (N_2, N_3, N_4) free?
for n1_fix in range(4):
    cnt = 0
    for n2 in range(L_q):
        for n3 in range(L_q):
            for n4 in range(L_q):
                if 1 - n1_fix + 9*n2 - 16*n3 + 8*n4 > 0:
                    cnt += 1
    print(f"Accepted profiles with N_1 = {n1_fix}, (N_2,N_3,N_4) ∈ [0,L_q)³: {cnt}")

# ═══════════════════════════════════════════════════════════════════════════
# THE KEY TEST: what's the count if we EXCLUDE N_3 = 0 trivial cases?
# ═══════════════════════════════════════════════════════════════════════════

print()
print("=" * 72)
print("MAIN TEST: accepted profiles with N_3 = 0 in [0,L_q)^4")
print("=" * 72)

# If N_3 contributes ZERO probability (since c_3 = -16 suppresses it), then 
# effectively the accepted subspace is ≅ {(N_1, N_2, N_4) : S > 0}
# 
# With N_3 = 0 fixed and (N_1, N_2, N_4) in [0, L_q)^3:
#   total = L_q^3 = 64 POSSIBLE
#   accepted = ?
n3_zero_in_cube = sum(1 for n1 in range(L_q) for n2 in range(L_q) for n4 in range(L_q)
                     if 1 - n1 + 9*n2 + 8*n4 > 0)
print(f"If N_3 = 0 and (N_1, N_2, N_4) ∈ [0, L_q)³:")
print(f"  Total profiles: {L_q**3} = L_q³ = 64")
print(f"  BDG-accepted:   {n3_zero_in_cube}")
print(f"  Accepted fraction: {n3_zero_in_cube/L_q**3:.4f}")

# This is the most compelling: if we interpret the "confinement cube" as
# (N_1, N_2, N_4) in [0, L_q)³ with N_3 = 0, then the total VOLUME is 64
# (the conjecture!) and the BDG-accepted subset is what the filter selects.
print()
print("INTERPRETATION: The 'depth-space' 3-cube is (N_1, N_2, N_4), with N_3 = 0.")
print("  - N_3 = 0 is forced because c_3 = -16 heavily penalizes it")
print("  - (N_1, N_2, N_4) each range over [0, L_q) = [0, 4)")
print("  - Volume = L_q^3 = 64 by construction")
print(f"  - BDG-accepted fraction = {n3_zero_in_cube/L_q**3:.2%}")
print()
print("UNDER THIS INTERPRETATION: N_eff = 64 is the LATTICE VOLUME in (N_1, N_2, N_4) depth-space.")
print("The 3D dimensionality arises because:")
print("  - N_3 is kinematically suppressed (not a depth dimension)")
print("  - N_1, N_2, N_4 are the three effective depth coordinates")
print("  - Each has extent L_q = 4 in the confinement lattice")
