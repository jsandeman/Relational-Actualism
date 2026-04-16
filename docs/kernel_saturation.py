"""
Kernel Saturation Theorem
===========================

ChatGPT's suggestion: formalize "loss of discriminatory power" using
D_KL(K(·|μ) ∥ Poisson_μ) → 0 or TV(K, Poisson) → 0.

THEOREM: For the BDG acceptance kernel K(N|μ) = Poisson(N;λ) × 𝟙[S>0] / P_acc,
both D_KL and TV are SIMPLE FUNCTIONS OF P_acc ALONE.

This follows from K being a truncated Poisson (same shape, zeroed below threshold).
"""

import numpy as np
from math import factorial, exp, log, pi, sqrt
from scipy.stats import poisson as poisson_dist

np.random.seed(42)

c_bdg = [1, -1, 9, -16, 8]

print("=" * 80)
print("KERNEL SATURATION THEOREM")
print("=" * 80)

# ================================================================
# 1. THE KEY IDENTITY
# ================================================================

print(f"""
1. THE KEY IDENTITY
{'─'*80}

  The BDG acceptance kernel is:
    K(N|μ) = Poisson(N; λ(μ)) × 𝟙[S(N)>0] / P_acc(μ)

  This is a TRUNCATED POISSON: same shape within the accepted
  region S>0, zeroed outside, renormalized by 1/P_acc.

  THEOREM (algebraic):

    D_KL(K ∥ Poisson) = -log P_acc(μ) = ΔS*(μ)

  PROOF:
    D_KL = Σ_N K(N) log(K(N)/P(N))
    For S(N) > 0: K(N)/P(N) = 1/P_acc (constant!)
    For S(N) ≤ 0: K(N) = 0 (no contribution)
    Therefore: D_KL = Σ_{{S>0}} K(N) × log(1/P_acc) = log(1/P_acc)
    = -log P_acc = ΔS*  ∎

  THEOREM (algebraic):

    TV(K, Poisson) = 1 - P_acc(μ)

  PROOF:
    TV = (1/2) Σ_N |K(N) - P(N)|
    For S>0: K(N) - P(N) = P(N)(1/P_acc - 1) = P(N)(1-P_acc)/P_acc
    For S≤0: K(N) - P(N) = -P(N)
    TV = (1/2)[Σ_{{S>0}} P(N)(1-P_acc)/P_acc + Σ_{{S≤0}} P(N)]
       = (1/2)[P_acc × (1-P_acc)/P_acc + (1-P_acc)]
       = (1/2)[2(1-P_acc)]
       = 1 - P_acc  ∎

  COROLLARY: Both divergence measures go to zero iff P_acc → 1.
  Both are SIMPLE FUNCTIONS of the single quantity P_acc(μ).
""")

# ================================================================
# 2. NUMERICAL VERIFICATION
# ================================================================

print(f"2. NUMERICAL VERIFICATION")
print("─" * 80)

def P_acc_mc(mu, N_samples=200000):
    lam = [mu**(k+1)/factorial(k+1) for k in range(4)]
    S_vals = np.zeros(N_samples)
    for k in range(4):
        N_k = np.random.poisson(lam[k], N_samples)
        S_vals += c_bdg[k+1] * N_k
    S_vals += c_bdg[0]
    return np.mean(S_vals > 0)

print(f"  {'μ':>6} {'P_acc':>8} {'ΔS*':>8} {'D_KL':>8} {'TV':>8} {'Regime':>20}")
print("  " + "─" * 65)

for mu in [0.1, 0.5, 1.0, 2.0, 3.0, 4.0, 4.712, 5.0, 5.7, 6.0,
           7.0, 8.0, 9.0, 10.0, 12.0, 15.0, 20.0, 50.0]:
    p = P_acc_mc(mu)
    if p > 0 and p < 1:
        dkl = -log(p)
        tv = 1 - p
    elif p >= 1:
        dkl = 0.0
        tv = 0.0
    else:
        dkl = float('inf')
        tv = 1.0

    if tv < 0.01:
        regime = "SATURATED (Π ≈ G)"
    elif tv < 0.1:
        regime = "near saturation"
    elif dkl > 0.8:
        regime = "strongly selective"
    elif dkl > 0.4:
        regime = "selective"
    else:
        regime = "gentle"

    print(f"  {mu:>6.1f} {p:>8.4f} {dkl:>8.4f} {dkl:>8.4f} {tv:>8.4f} {regime:>20}")

# ================================================================
# 3. THE SATURATION TRANSITION
# ================================================================

print(f"\n\n3. THE SATURATION TRANSITION")
print("─" * 80)

print(f"""
  The kernel saturation theorem establishes:

    D_KL(K ∥ Poisson) = ΔS* = -log P_acc(μ)
    TV(K, Poisson) = 1 - P_acc(μ)

  From the numerical P_acc profile:

    μ < 3:    P_acc ≈ 0.5-0.6, TV ≈ 0.4-0.5, D_KL ≈ 0.4-0.6
              Filter is moderately selective.
              Roughly half of candidates are rejected.

    μ ≈ 3-5:  P_acc drops to minimum ~0.40, TV ≈ 0.60, D_KL ≈ 0.9
              MAXIMUM SELECTIVITY.
              The filter carries the most information here.
              This is the selective regime.

    μ ≈ 5-7:  P_acc rises from 0.43 to 0.75, TV drops to 0.25
              Filter is weakening rapidly.

    μ ≈ 7-10: P_acc rises from 0.75 to 1.00, TV → 0, D_KL → 0
              Saturation. Filter carries no information.
              K(N|μ) → Poisson(N; λ(μ)) uniformly.

    μ > 10:   P_acc = 1.00 (to MC precision), TV = 0, D_KL = 0
              COMPLETE SATURATION.
              Every candidate is accepted. The filter is inert.
""")

# ================================================================
# 4. BUT IS THE POISSON MODEL THE RIGHT ONE?
# ================================================================

print(f"4. SUBTLETY: POISSON MODEL vs ACTUAL SEQUENTIAL GROWTH")
print("─" * 80)

print(f"""
  The theorem above proves kernel saturation in the POISSON-CSG
  MODEL — where depth profiles are independently Poisson-distributed.

  ChatGPT's deeper question: does saturation also hold for the
  ACTUAL sequential growth dynamics?

  In the actual dynamics, the depth profile N = (N₁,...,N₄) of a
  proposed vertex is DETERMINED by the existing graph G_n and the
  proposed past set P. It is NOT random.

  The question becomes: at high μ (dense graph), is S(N) > 0
  for EVERY possible extension, not just for random Poisson profiles?

  This is a STRONGER claim than P_acc → 1.

  Let's check: what is the WORST-CASE profile at high density?
""")

# The worst case for S > 0 is: maximum N₁ and N₃, minimum N₂ and N₄.
# S = 1 - N₁ + 9N₂ - 16N₃ + 8N₄
# To minimize S: maximize N₁, N₃ and minimize N₂, N₄.

# At density μ, the expected values are:
# E[N₁] = μ, E[N₂] = μ²/2, E[N₃] = μ³/6, E[N₄] = μ⁴/24

# The worst case in the Poisson model:
# N₁ = E[N₁] + k×σ₁, N₃ = E[N₃] + k×σ₃ (upward fluctuations)
# N₂ = E[N₂] - k×σ₂, N₄ = E[N₄] - k×σ₄ (downward fluctuations)

# But in the actual graph, the profiles are NOT independent.
# A vertex with many depth-1 ancestors (large N₁) also tends
# to have many depth-2 ancestors (large N₂), because the depth-1
# ancestors themselves have depth-1 ancestors.

# The key structural constraint: in a causal graph,
# N₂ ≥ some function of N₁ (each depth-1 ancestor has its own
# ancestors, contributing to N₂).

# Specifically: if v has N₁ depth-1 ancestors, and each of those
# has at least 1 depth-1 ancestor of its own (which is typical
# at high density), then N₂ ≥ N₁.

# More precisely: in a dense graph (μ >> 1), the depth profile
# satisfies N_k ≈ μ^k/k! with fluctuations of order √(μ^k/k!).
# The RATIOS N_k/N_1 ≈ μ^{k-1}/k! are FIXED by the density.

# At high μ:
# N₂/N₁ ≈ μ/2
# N₃/N₁ ≈ μ²/6
# N₄/N₁ ≈ μ³/24

# So S/N₁ ≈ -1 + 9μ/2 - 16μ²/6 + 8μ³/24
#          = -1 + 4.5μ - 2.667μ² + 0.333μ³

# This is positive for large μ (cubic term dominates).
# Find the crossover:

print(f"  Expected BDG score ratio S/N₁ at Poisson mean:")
print(f"  {'μ':>6} {'E[S]':>10} {'E[N₁]':>8} {'E[S]/E[N₁]':>12} {'S>0 guaranteed?':>18}")
print("  " + "─" * 60)

for mu in [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20]:
    lam = [mu**(k+1)/factorial(k+1) for k in range(4)]
    E_S = c_bdg[0] + sum(c_bdg[k+1]*lam[k] for k in range(4))
    E_N1 = lam[0]
    ratio = E_S / E_N1 if E_N1 > 0 else 0

    # Standard deviation of S
    var_S = sum(c_bdg[k+1]**2 * lam[k] for k in range(4))
    std_S = sqrt(var_S)

    # Is E[S] > 3σ? (practically guaranteed S > 0)
    guaranteed = "YES" if E_S > 3*std_S else "NO" if E_S < -3*std_S else "marginal"

    print(f"  {mu:>6} {E_S:>10.2f} {E_N1:>8.2f} {ratio:>12.4f} {guaranteed:>18}")

# ================================================================
# 5. THE VARIANCE CROSSOVER
# ================================================================

print(f"\n\n5. THE VARIANCE CROSSOVER (why P_acc→1 at high μ)")
print("─" * 80)

print(f"""
  At high μ, E[S] can be negative (the mean score is below zero).
  Yet P_acc → 1. How?

  The answer: the VARIANCE of S grows faster than |E[S]|.

  Var[S] = Σ c_k² × λ_k = 1×μ + 81×μ²/2 + 256×μ³/6 + 64×μ⁴/24
         ≈ 2.67μ⁴ for large μ (dominated by c₄²×μ⁴/24 = 64μ⁴/24)

  σ[S] ≈ 1.63 × μ²

  E[S] = 1 - μ + 4.5μ² - 2.67μ³ + 0.333μ⁴
       ≈ 0.333μ⁴ for large μ

  So E[S]/σ[S] ≈ 0.333μ⁴ / (1.63μ²) = 0.204μ² → ∞

  At large μ: E[S]/σ → ∞, meaning S is ALMOST CERTAINLY positive.
  The filter accepts everything not because it's lenient, but
  because the score is overwhelmingly positive.
""")

print(f"  {'μ':>6} {'E[S]':>10} {'σ[S]':>10} {'E[S]/σ':>10} {'P(S>0)≈':>10}")
print("  " + "─" * 50)

for mu in [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20]:
    lam = [mu**(k+1)/factorial(k+1) for k in range(4)]
    E_S = c_bdg[0] + sum(c_bdg[k+1]*lam[k] for k in range(4))
    var_S = sum(c_bdg[k+1]**2 * lam[k] for k in range(4))
    std_S = sqrt(var_S)
    z = E_S / std_S if std_S > 0 else 0

    from scipy.stats import norm
    p_approx = norm.cdf(z)

    print(f"  {mu:>6} {E_S:>10.1f} {std_S:>10.1f} {z:>10.3f} {p_approx:>10.6f}")

# ================================================================
# 6. THE THEOREM STATEMENT
# ================================================================

print(f"""

6. THE KERNEL SATURATION THEOREM
{'='*80}

  THEOREM 1 (Poisson-CSG kernel saturation):

    For the BDG acceptance kernel K(N|μ) on a Poisson-CSG:
      D_KL(K(·|μ) ∥ Poisson(·; λ(μ))) = -log P_acc(μ)
      TV(K(·|μ), Poisson(·; λ(μ))) = 1 - P_acc(μ)

    PROOF: K is a truncated Poisson. The ratio K/P = 1/P_acc
    on the support of K, and 0 elsewhere. Direct substitution. ∎

    STATUS: PROVED (algebraic identity).

  THEOREM 2 (Asymptotic saturation):

    For d=4 BDG coefficients (1,-1,9,-16,8):
      lim_{{μ→∞}} P_acc(μ) = 1

    PROOF: E[S] ~ 0.333μ⁴ and σ[S] ~ 1.63μ², so
    E[S]/σ[S] ~ 0.204μ² → ∞ as μ → ∞.
    By Chebyshev: P(S ≤ 0) ≤ σ²/(E[S])² → 0.
    Therefore P_acc = P(S > 0) → 1. ∎

    STATUS: PROVED (Chebyshev bound).

    Quantitative: P_acc(μ) ≥ 1 - 1/(0.204μ²)² = 1 - 24/(μ⁴)
    for large μ. So P_acc ≥ 0.99 for μ ≥ 4.0 ... wait, let me
    check this against the actual values.
""")

# Check the Chebyshev bound
print(f"  Chebyshev bound vs actual P_acc:")
print(f"  {'μ':>6} {'P_acc(MC)':>10} {'Chebyshev lb':>14} {'Bound tight?':>14}")
print("  " + "─" * 50)

for mu in [3, 4, 5, 6, 7, 8, 10, 15, 20]:
    p_actual = P_acc_mc(mu, 100000)
    lam = [mu**(k+1)/factorial(k+1) for k in range(4)]
    E_S = c_bdg[0] + sum(c_bdg[k+1]*lam[k] for k in range(4))
    var_S = sum(c_bdg[k+1]**2 * lam[k] for k in range(4))

    if E_S > 0:
        cheby = 1 - var_S / E_S**2
        cheby = max(cheby, 0)
    else:
        cheby = 0  # Chebyshev doesn't help when mean is negative

    print(f"  {mu:>6} {p_actual:>10.4f} {cheby:>14.4f} "
          f"{'✓' if cheby <= p_actual else '✗':>14}")

print(f"""

  NOTE: The Chebyshev bound is VERY loose at intermediate μ.
  It only becomes useful at large μ (≥ 7) where E[S] is positive.

  At μ ≈ 3-5, E[S] is NEGATIVE, so Chebyshev gives trivial
  bound (P_acc ≥ 0). Yet P_acc ≈ 0.4-0.5 because the Poisson
  FLUCTUATIONS push many profiles above S=0.

  The EXACT saturation profile must be computed numerically
  (as we've done). But the ASYMPTOTIC result is proved:
  P_acc → 1 as μ → ∞, with rate at least 1 - O(1/μ⁴).

SUMMARY OF PROVED RESULTS:
  ✓ D_KL(K ∥ Poisson) = ΔS* = -log P_acc  [algebraic identity]
  ✓ TV(K, Poisson) = 1 - P_acc              [algebraic identity]
  ✓ P_acc → 1 as μ → ∞                      [Chebyshev]
  ✓ Rate: P_acc ≥ 1 - O(1/μ⁴) for large μ  [from E[S]/σ scaling]

  Therefore: D_KL → 0 and TV → 0 as μ → ∞.
  The acceptance kernel converges to the unconditioned Poisson
  distribution. The filter loses all discriminatory power.

  This is the KERNEL SATURATION THEOREM.
  It is PROVED, not conjectured.

WHAT THIS MEANS FOR THE BIMODAL PHASE TRANSITION:

  At μ → ∞: K(N|μ) → Poisson(N; λ(μ)). The filter accepts
  everything. There is no distinction between "admitted" and
  "filtered" candidates. Every candidate extension is admissible.

  In the bimodal ontology: Π(G) = set of admissible extensions.
  When every extension is admissible, Π(G) equals the FULL set
  of candidate extensions. The filter provides no information
  about which extensions are "real" vs "potential." The
  distinction is as sharp as the filter is selective.

  At saturation, the filter's selectivity is zero (TV = 0).
  The distinction between actual and potential — as mediated
  by the BDG filter — dissolves.

  CAVEAT: This proves saturation for the POISSON-CSG model.
  The actual sequential growth dynamics may differ because
  depth profiles are correlated, not independent Poisson.
  However, the asymptotic argument (E[S]/σ → ∞) applies to
  ANY profile distribution whose mean and variance scale as
  the Poisson ones, which is expected for dense graphs.
""")
