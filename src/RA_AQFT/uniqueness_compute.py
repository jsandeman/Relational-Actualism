"""
UNIQUENESS COMPUTATION
======================

For each depth K, compute the dimension of the space of self-consistent
second-order growth functionals on a Poisson-CSG DAG.

The key insight: SELF-CONSISTENCY of the Poisson-CSG model provides
additional constraints beyond the second-order condition.

When we filter by S > 0, the filtered distribution of N_k must remain
consistent with the Poisson model. This means:

  E[N_k | S > 0] ≈ E[N_k]  (unfiltered Poisson mean)

If the filter systematically biases the N_k distribution, the model
is inconsistent: the graph produced by the growth rule doesn't have
the statistics assumed by the growth rule.

This gives K additional constraints (one per N_k), which combined with
the second-order condition (1 constraint) on K free parameters,
may uniquely determine the coefficients.
"""
import numpy as np
from math import factorial, comb
from scipy.optimize import minimize
from scipy import stats as sp_stats

np.random.seed(42)

print("=" * 65)
print("SELF-CONSISTENCY CONSTRAINTS ON GROWTH FUNCTIONALS")
print("=" * 65)

def poisson_pmf(k, lam):
    """Poisson probability mass function."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return np.exp(-lam) * lam**k / factorial(k)

def compute_pacc_and_bias(coeffs, mu, n_samples=500000):
    """
    For action S = 1 + Σ c_k N_k with N_k ~ Poisson(μ^(k+1)/(k+1)!):
    
    1. Compute P_acc = P(S > 0)
    2. Compute E[N_k | S > 0] for each k
    3. Compare with E[N_k] (unfiltered) to measure bias
    
    Returns: P_acc, bias ratios E[N_k|S>0] / E[N_k]
    """
    K = len(coeffs)
    
    # Poisson parameters
    lambdas = [mu**(k+1) / factorial(k+1) for k in range(K)]
    
    # Monte Carlo: sample N_k values
    samples = np.array([np.random.poisson(lam, n_samples) for lam in lambdas]).T
    
    # Compute S for each sample
    S = np.ones(n_samples)  # birth term
    for k in range(K):
        S += coeffs[k] * samples[:, k]
    
    # Filter: S > 0
    accepted = S > 0
    P_acc = np.mean(accepted)
    
    if P_acc < 1e-6 or P_acc > 1 - 1e-6:
        return P_acc, None  # degenerate
    
    # Compute bias: E[N_k | accepted] / E[N_k]
    bias_ratios = []
    for k in range(K):
        E_Nk = lambdas[k]
        if E_Nk < 1e-10:
            bias_ratios.append(1.0)
            continue
        E_Nk_given_acc = np.mean(samples[accepted, k])
        bias_ratios.append(E_Nk_given_acc / E_Nk)
    
    return P_acc, np.array(bias_ratios)

def self_consistency_residual(coeffs, mu, n_samples=500000):
    """
    Measure how far the filtered distribution deviates from Poisson.
    Returns sum of squared bias deviations: Σ(bias_k - 1)²
    """
    P_acc, bias = compute_pacc_and_bias(coeffs, mu, n_samples)
    if bias is None:
        return 1e10  # degenerate
    return np.sum((bias - 1.0)**2)


# ══════════════════════════════════════════════════════════════
# K=2: One free parameter (c₁, c₂ = -c₁)
# ══════════════════════════════════════════════════════════════

print("\n" + "=" * 50)
print("K=2: Action S = 1 + c₁N₁ + c₂N₂, with c₂ = -c₁")
print("=" * 50)
print("Free parameter: c₁")
print()

for c1 in [-3, -2, -1, -0.5, 0.5, 1, 2, 3]:
    coeffs = [c1, -c1]
    P_acc, bias = compute_pacc_and_bias(coeffs, mu=1.0, n_samples=200000)
    if bias is not None:
        bias_str = ", ".join(f"{b:.4f}" for b in bias)
        residual = np.sum((bias - 1.0)**2)
        print(f"  c₁={c1:+5.1f}: P_acc={P_acc:.4f}, bias=[{bias_str}], residual={residual:.6f}")
    else:
        print(f"  c₁={c1:+5.1f}: P_acc={P_acc:.4f} (degenerate)")

# Known d=2 BDG: S = 1 - 2N₁, i.e. c₁=-2 (and no N₂ term)
# But that's K=1, not K=2.
# For K=2: d=2 BDG would be c₁=-2, c₂=0 → doesn't satisfy Σc_k=0 unless c₂=2
# Actually d=2 BDG is S = N₀ - 2N₁ = 1 - 2N₁ (only one layer)
# So K=1 for d=2: trivially c₁ with Σc_k=0 → c₁=0 (trivial)
# This means K=1 is too small. d=2 uses K=1 with c₁=-2, NOT satisfying Σ=0.
# Hmm, let me reconsider.

# Actually the second-order condition Σc_k=0 is for k=1..K.
# For d=2: S = 1 - 2N_1. Here c_1 = -2, and Σ = -2 ≠ 0.
# So d=2 is FIRST-ORDER, not second-order?

# Wait — let me re-examine. The Benincasa-Dowker d=2 action is:
# S_BD = N_0 - 2N_1  where N_0 counts "links" (immediate past with no interval)
# In the RASM convention: S = 1 - 2N_1 (birth + links term)
# Σ c_k = c_0 + c_1 = 1 + (-2) = -1 ≠ 0

# So the "second-order" condition as I stated it (Σc_k=0 for k≥1) may be 
# specific to d≥4. Let me reconsider what "second-order" means.

print()
print("NOTE: Reconsidering the second-order condition.")
print("d=2 BDG has c = (1, -2): Σ c_k = -1 ≠ 0 (FIRST order)")
print("d=4 BDG has c = (1, -1, 9, -16, 8): Σ c_k(k≥1) = 0 (SECOND order)")
print()
print("The second-order condition may be a DERIVED PROPERTY of d≥4,")
print("not an axiom. Let's check what self-consistency gives WITHOUT")
print("imposing it a priori.")

# ══════════════════════════════════════════════════════════════
# K=4: Three free parameters (scan for self-consistency)
# ══════════════════════════════════════════════════════════════

print("\n" + "=" * 50)
print("K=4: Full scan WITHOUT assuming second-order condition")
print("=" * 50)

# Parameterize: c = (c₁, c₂, c₃, c₄) with 4 free parameters
# (no constraints yet — let self-consistency determine everything)
#
# Strategy: grid search over parameter ratios, find self-consistent points

# First: fix overall scale by setting c₁ = -1 (normalization)
# Then scan c₂, c₃, c₄

print("\nScanning c₂, c₃, c₄ (with c₁ = -1 fixed as normalization)...")
print("Looking for self-consistent points (bias ≈ 1 for all N_k)")
print()

best_residual = np.inf
best_params = None
results = []

# Coarse grid search
for c2 in np.arange(1, 20, 2):
    for c3 in np.arange(-30, -1, 3):
        for c4 in np.arange(1, 20, 2):
            coeffs = [-1, c2, c3, c4]
            P_acc, bias = compute_pacc_and_bias(coeffs, mu=1.0, n_samples=50000)
            if bias is not None and 0.1 < P_acc < 0.9:
                residual = np.sum((bias - 1.0)**2)
                results.append((residual, P_acc, coeffs, bias))
                if residual < best_residual:
                    best_residual = residual
                    best_params = coeffs

# Sort by residual
results.sort(key=lambda x: x[0])

print(f"Scanned {len(results)} viable parameter sets")
print(f"\nTop 10 most self-consistent (lowest bias residual):")
print(f"  {'c₁':>4} {'c₂':>4} {'c₃':>5} {'c₄':>4}  {'P_acc':>6}  {'residual':>10}  {'bias (N₁,N₂,N₃,N₄)'}")
print("  " + "-" * 70)

for i, (res, pacc, coeffs, bias) in enumerate(results[:10]):
    bias_str = ", ".join(f"{b:.3f}" for b in bias)
    c1, c2, c3, c4 = coeffs
    sum_c = sum(coeffs)
    print(f"  {c1:4.0f} {c2:4.0f} {c3:5.0f} {c4:4.0f}  {pacc:6.3f}  {res:10.6f}  [{bias_str}]  Σ={sum_c:.0f}")

print()

# Now: refine around the best point
if best_params:
    print(f"Refining around best point: c = {best_params}")
    c1_fix = -1
    best_ref = None
    best_res_ref = np.inf
    
    c2_b, c3_b, c4_b = best_params[1], best_params[2], best_params[3]
    
    for c2 in np.arange(c2_b-2, c2_b+2.1, 0.5):
        for c3 in np.arange(c3_b-3, c3_b+3.1, 0.5):
            for c4 in np.arange(c4_b-2, c4_b+2.1, 0.5):
                coeffs = [c1_fix, c2, c3, c4]
                P_acc, bias = compute_pacc_and_bias(coeffs, mu=1.0, n_samples=100000)
                if bias is not None and 0.1 < P_acc < 0.9:
                    residual = np.sum((bias - 1.0)**2)
                    if residual < best_res_ref:
                        best_res_ref = residual
                        best_ref = (coeffs, P_acc, bias, residual)
    
    if best_ref:
        coeffs, pacc, bias, res = best_ref
        print(f"\n  Refined best: c = [{coeffs[0]:.1f}, {coeffs[1]:.1f}, {coeffs[2]:.1f}, {coeffs[3]:.1f}]")
        print(f"  P_acc = {pacc:.4f}")
        print(f"  Bias = [{', '.join(f'{b:.4f}' for b in bias)}]")
        print(f"  Residual = {res:.6f}")
        print(f"  Σ c_k = {sum(coeffs):.1f}")
        
        # Compare with BDG
        bdg = [-1, 9, -16, 8]
        print(f"\n  BDG d=4: c = {bdg}")
        P_acc_bdg, bias_bdg = compute_pacc_and_bias(bdg, mu=1.0, n_samples=200000)
        res_bdg = np.sum((bias_bdg - 1.0)**2) if bias_bdg is not None else None
        print(f"  BDG P_acc = {P_acc_bdg:.4f}")
        if bias_bdg is not None:
            print(f"  BDG Bias = [{', '.join(f'{b:.4f}' for b in bias_bdg)}]")
            print(f"  BDG Residual = {res_bdg:.6f}")
            print(f"  BDG Σ c_k = {sum(bdg):.0f}")

# ══════════════════════════════════════════════════════════════
# KEY TEST: Does the BDG action have minimal bias?
# ══════════════════════════════════════════════════════════════

print("\n" + "=" * 50)
print("KEY TEST: Is BDG the UNIQUE minimum-bias action at K=4?")
print("=" * 50)

# Compare BDG bias with nearby parameter values
print("\nBDG neighborhood scan (c₁=-1 fixed, varying c₂,c₃,c₄ around BDG):")
print(f"  {'c₂':>5} {'c₃':>5} {'c₄':>5}  {'P_acc':>6}  {'residual':>10}  {'Σc_k':>5}")
print("  " + "-" * 48)

neighborhood = []
for dc2 in [-2, -1, 0, 1, 2]:
    for dc3 in [-2, -1, 0, 1, 2]:
        for dc4 in [-2, -1, 0, 1, 2]:
            c2 = 9 + dc2
            c3 = -16 + dc3
            c4 = 8 + dc4
            coeffs = [-1, c2, c3, c4]
            P_acc, bias = compute_pacc_and_bias(coeffs, mu=1.0, n_samples=100000)
            if bias is not None and P_acc > 0.01:
                residual = np.sum((bias - 1.0)**2)
                neighborhood.append((residual, coeffs, P_acc, sum(coeffs)))

neighborhood.sort()
for res, coeffs, pacc, sc in neighborhood[:15]:
    marker = " ← BDG" if coeffs == [-1, 9, -16, 8] else ""
    print(f"  {coeffs[1]:5.0f} {coeffs[2]:5.0f} {coeffs[3]:5.0f}  {pacc:6.3f}  {res:10.6f}  {sc:5.0f}{marker}")

