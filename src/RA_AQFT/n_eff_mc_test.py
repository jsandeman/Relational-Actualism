#!/usr/bin/env python3
"""
N_eff Monte Carlo test for RA Paper II proton mass cascade.

Conjecture: N_eff = L_q^3 = 64, where L_q = 4 is the Lean-verified quark
confinement depth, and the "3" is the number of effective depth-space
dimensions in d=4.

This script generates Poisson-CSG configurations at μ=1 and measures
several candidate "effective site count" observables to test whether
any of them converge on 64.

Units and conventions:
  μ = 1 (actualization threshold of the BDG filter)
  BDG coefficients (c_0, c_1, c_2, c_3, c_4) = (1, -1, 9, -16, 8)
  Profile (N_1, N_2, N_3, N_4) counts chains of length 1, 2, 3, 4 from a vertex
  Score S = c_0 + c_1·N_1 + c_2·N_2 + c_3·N_3 + c_4·N_4
  Filter: vertex accepted iff S > 0 (same convention as D4U02 setup)
"""

import numpy as np
from collections import Counter
from scipy import stats

np.random.seed(42)  # reproducibility

# ═══════════════════════════════════════════════════════════════════════════
# 1. Direct Poisson sampling at μ=1
# ═══════════════════════════════════════════════════════════════════════════

def sample_bdg_profile(n_samples=10_000_000, mu=1.0):
    """
    Sample (N_1, N_2, N_3, N_4) where N_k ~ Pois(μ^k / k!) independently.
    Returns array of shape (n_samples, 4).
    """
    lam = np.array([mu, mu**2/2, mu**3/6, mu**4/24])  # rates for N_1..N_4
    N = np.column_stack([np.random.poisson(lam[k-1], n_samples) for k in range(1,5)])
    return N

def bdg_score(N):
    """Compute BDG score S = 1 - N_1 + 9·N_2 - 16·N_3 + 8·N_4."""
    return 1 - N[:,0] + 9*N[:,1] - 16*N[:,2] + 8*N[:,3]

def accepted_mask(N):
    """Vertex accepted iff S > 0."""
    return bdg_score(N) > 0

# ═══════════════════════════════════════════════════════════════════════════
# 2. Candidate N_eff interpretations to test
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("N_eff Monte Carlo test — RA Paper II proton mass cascade")
print("=" * 72)
print()
print(f"μ = 1.0, n_samples = 10,000,000")
print()

N = sample_bdg_profile(n_samples=10_000_000)
S = bdg_score(N)
acc = accepted_mask(N)
P_acc = acc.mean()
print(f"Acceptance rate P_acc(1) = {P_acc:.6f}")
print(f"Expected from prior work: P_acc(1) ≈ 0.548 (gives ΔS* ≈ 0.601)")
print(f"Delta S* = {-np.log(P_acc):.6f} nats")
print()

# ═══════════════════════════════════════════════════════════════════════════
# Test 1: Accepted profile diversity
# ═══════════════════════════════════════════════════════════════════════════
# How many distinct (N_1, N_2, N_3, N_4) profiles survive the filter?
# If the confinement region is characterized by L_q^3 = 64 independent
# configurations, we should see ~64 dominant profiles.

N_acc = N[acc]
profiles = [tuple(n) for n in N_acc]
profile_counts = Counter(profiles)

print("─" * 72)
print("Test 1: Effective profile diversity")
print("─" * 72)
print(f"Total accepted: {acc.sum():,}")
print(f"Distinct profiles: {len(profile_counts):,}")
print()

# The "effective" count (1/H where H = Shannon entropy) is the usual measure
# of effective number of configurations
probs = np.array(list(profile_counts.values())) / acc.sum()
H = -(probs * np.log(probs)).sum()
N_eff_entropy = np.exp(H)
print(f"Shannon entropy H = {H:.6f} nats")
print(f"Effective profile count N_eff_H = exp(H) = {N_eff_entropy:.3f}")
print(f"Target (conjecture): 64")
print(f"Ratio N_eff_H / 64 = {N_eff_entropy / 64:.4f}")
print()

# Also report: concentration of top 64 profiles
top_counts = sorted(profile_counts.values(), reverse=True)
mass_in_top_64 = sum(top_counts[:64]) / acc.sum()
print(f"Fraction of mass in top 64 profiles: {mass_in_top_64:.4f}")
print()

# ═══════════════════════════════════════════════════════════════════════════
# Test 2: Profiles with bounded BDG depth
# ═══════════════════════════════════════════════════════════════════════════
# Restrict to profiles with all N_k < L_q = 4 (i.e., "within the confinement lattice")

print("─" * 72)
print("Test 2: Profiles within confinement lattice (all N_k < L_q = 4)")
print("─" * 72)

L_q = 4
within_lattice = np.all(N < L_q, axis=1) & acc
print(f"Accepted profiles with all N_k < 4: {within_lattice.sum():,} " +
      f"({within_lattice.mean():.4f} of total)")

N_within = N[within_lattice]
profiles_within = [tuple(n) for n in N_within]
profile_counts_within = Counter(profiles_within)
print(f"Distinct profiles in this restricted set: {len(profile_counts_within)}")
print(f"Maximum possible (L_q^4 = 256): 256")
print()

# Among profiles with all N_k in [0, 4), how many satisfy the BDG filter?
# This is a direct combinatorial count.
all_profiles = np.array([(n1,n2,n3,n4)
                          for n1 in range(L_q)
                          for n2 in range(L_q)
                          for n3 in range(L_q)
                          for n4 in range(L_q)])
S_all = 1 - all_profiles[:,0] + 9*all_profiles[:,1] - 16*all_profiles[:,2] + 8*all_profiles[:,3]
accepted_profiles_in_lattice = (S_all > 0).sum()
print(f"Combinatorial count: profiles in [0,L_q)^4 with S>0: {accepted_profiles_in_lattice}")
print(f"Total profiles in [0,L_q)^4 = L_q^4: {L_q**4}")
print()

# ═══════════════════════════════════════════════════════════════════════════
# Test 3: 3D projection (ignoring N_1)
# ═══════════════════════════════════════════════════════════════════════════
# The claim is that (N_2, N_3, N_4) form the "3D depth-space". Test by looking
# at the number of distinct (N_2, N_3, N_4) configurations with all < L_q.

print("─" * 72)
print("Test 3: (N_2, N_3, N_4) configurations with all < L_q = 4")
print("─" * 72)

# Combinatorial: how many (N_2, N_3, N_4) triples in [0, L_q)^3 are accepted
# for SOME value of N_1?
accepted_3d_configs = set()
for n1 in range(20):  # try many N_1 values
    for n2 in range(L_q):
        for n3 in range(L_q):
            for n4 in range(L_q):
                S = 1 - n1 + 9*n2 - 16*n3 + 8*n4
                if S > 0:
                    accepted_3d_configs.add((n2, n3, n4))

print(f"Distinct (N_2,N_3,N_4) triples in [0,4)^3 that are accepted for some N_1: " +
      f"{len(accepted_3d_configs)}")
print(f"Maximum possible: L_q^3 = {L_q**3}")
print(f"Ratio: {len(accepted_3d_configs) / L_q**3:.4f}")
print()

# Alternative: constrained to N_1 = 0 or N_1 small (depth contribution minimal)
for n1_fixed in [0, 1, 2]:
    cfgs = set()
    for n2 in range(L_q):
        for n3 in range(L_q):
            for n4 in range(L_q):
                S = 1 - n1_fixed + 9*n2 - 16*n3 + 8*n4
                if S > 0:
                    cfgs.add((n2, n3, n4))
    print(f"  With N_1={n1_fixed}: {len(cfgs)} accepted (N_2,N_3,N_4) triples")
print()

# ═══════════════════════════════════════════════════════════════════════════
# Test 4: Expected profile weight at μ=1
# ═══════════════════════════════════════════════════════════════════════════

print("─" * 72)
print("Test 4: Exponentiated entropy of joint distribution at μ=1")
print("─" * 72)

# The Poisson distribution of (N_1, ..., N_4) with rates (1, 1/2, 1/6, 1/24)
# has joint entropy which we can compute exactly.
rates = [1.0, 1/2, 1/6, 1/24]

# Poisson entropy: H(Pois(λ)) ≈ (1/2)·log(2πe·λ) for large λ, but we need
# exact for small λ.
def poisson_entropy(lam, k_max=100):
    """Exact Shannon entropy of Poisson(λ) in nats, truncated at k_max."""
    k = np.arange(k_max + 1)
    p = stats.poisson.pmf(k, lam)
    mask = p > 0
    return -(p[mask] * np.log(p[mask])).sum()

H_total = sum(poisson_entropy(l) for l in rates)
print(f"Joint entropy of (N_1,N_2,N_3,N_4) at μ=1: H = {H_total:.6f} nats")
print(f"exp(H) = {np.exp(H_total):.3f}")
print(f"Target (conjecture): 64")
print()

# ═══════════════════════════════════════════════════════════════════════════
# Test 5: L_q^3 = 64 as the count of strictly accepting configurations
# ═══════════════════════════════════════════════════════════════════════════

print("─" * 72)
print("Test 5: Direct count — profiles that strictly accept with all depths ≤ L_q")
print("─" * 72)

# Count profiles (n_1, n_2, n_3, n_4) with n_k ∈ {0, 1, ..., L_q-1} that satisfy S > 0
# and are consistent with a depth-bounded causal structure.

total_accepted_bounded = 0
for n1 in range(L_q):
    for n2 in range(L_q):
        for n3 in range(L_q):
            for n4 in range(L_q):
                S = 1 - n1 + 9*n2 - 16*n3 + 8*n4
                if S > 0:
                    total_accepted_bounded += 1
print(f"Profiles (N_1,N_2,N_3,N_4) ∈ [0,L_q)^4 with S > 0: {total_accepted_bounded}")
print(f"Out of L_q^4 = {L_q**4} total")
print()

# ═══════════════════════════════════════════════════════════════════════════
# Summary
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 72)
print("Summary of candidate N_eff interpretations")
print("=" * 72)

results = [
    ("Test 1: exp(Shannon entropy of all accepted profiles)",
     N_eff_entropy, 64),
    ("Test 2: Distinct accepted profiles with N_k < L_q",
     len(profile_counts_within), 64),
    ("Test 2b: Combinatorial accepting profiles in [0,L_q)^4",
     accepted_profiles_in_lattice, 64),
    ("Test 3: Accepted (N_2,N_3,N_4) triples in [0,L_q)^3",
     len(accepted_3d_configs), 64),
    ("Test 4: exp(joint entropy of unconditioned Poisson)",
     np.exp(H_total), 64),
    ("Test 5: Profiles in [0,L_q)^4 with S>0 (direct)",
     total_accepted_bounded, 64),
]
print()
print(f"{'Interpretation':<58} {'Value':>10} {'Target':>8}")
print("-" * 80)
for name, val, tgt in results:
    ratio = val / tgt
    marker = "✓" if 0.9 < ratio < 1.1 else ("~" if 0.5 < ratio < 2 else "✗")
    print(f"{name:<58} {val:>10.2f} {tgt:>8}  {marker}  (ratio {ratio:.3f})")
