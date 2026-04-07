"""
O14 Attack: Incidence Algebra Approach
======================================

THE PRECISE MATHEMATICAL QUESTION:

In the incidence algebra of a locally finite poset (the causal set),
consider operators of the form:

    B = Σ_{k=0}^{K} c_k × ζ^k

where ζ is the zeta function and ζ^k counts k-chains.

When applied to a scalar field φ on the causal set:
    (Bφ)(x) = Σ_{k=0}^{K} c_k × Σ_{y: |[y,x]|=k+1} φ(y)

CONSTRAINTS on the c_k:

(C1) RETARDED: B only looks into the causal past (automatic for ζ^k).

(C2) SECOND-ORDER: B must annihilate constant fields on "flat" regions.
     For a uniform Poisson sprinkling at density ρ:
     <Bφ>(x) |_{φ=const} = 0  (up to boundary terms)
     
     This means: Σ c_k × <N_k> = 0 where <N_k> is the expected number
     of elements with exactly k-element intervals.
     
     For a Poisson sprinkling in d dimensions:
     <N_k> = (ρV)^{k} × f_d(k) / k!
     where V is the interval volume and f_d(k) involves the d-dimensional
     volume fractions.

(C3) MINIMAL DEPTH: K = ⌊d/2⌋ + 2 (the minimum number of layers).
     Yeats (2024) notes that extending beyond this breaks uniqueness.

(C4) CORRECT NORMALIZATION: B must give the d'Alembertian □ in the 
     continuum limit. BUT — this is the continuum constraint we want
     to AVOID. So we need to replace this with an RA-native condition.

THE RA-NATIVE REPLACEMENT FOR (C4):

Instead of "reproduces □", we need: "B is the unique operator satisfying
(C1)-(C3) that is COMPLETE at second order."

"Complete at second order" means: B captures ALL the curvature information
available from chains of depth ≤ K. It's not just any second-order operator;
it's the MAXIMAL second-order operator at depth K.

Formally: in the vector space of operators Σ c_k ζ^k with k ≤ K,
the subspace satisfying (C2) has some dimension D.
If D = 1, uniqueness follows (up to normalization).

Let me compute D for each K and d.
"""
import numpy as np
from math import factorial, comb, gamma
from scipy.special import gamma as Gamma
import sympy as sp

print("=" * 65)
print("O14: DIMENSION OF THE SECOND-ORDER SUBSPACE")
print("=" * 65)

print("""
SETUP:
  Operator B = Σ_{k=0}^{K} c_k ζ^k
  Applied to a Poisson sprinkling at density ρ in d dimensions.
  
  The expected value of ζ^k (the k-chain count) for an interval
  of n elements sprinkled into a d-dimensional causal diamond is:
  
    <N_k>(n) = Σ over all k-element subsets that form a chain
  
  For large n (thermodynamic limit), this scales as:
    <N_k> ∝ n^{k+1} × V_d(k)
  
  where V_d(k) is a dimension-dependent volume factor.
  
  The SECOND-ORDER condition is:
    <B(const)> = Σ c_k <N_k> should scale as n^{2/d} (curvature term)
    and NOT as n^{1} (density term) or n^{0} (cosmological constant).
  
  This gives a HIERARCHY of constraints as powers of n:
    - Coefficient of n^{K+1}: must vanish (K+1 > 2/d for any reasonable K)
    - Coefficient of n^{K}: must vanish
    - ...
    - Coefficient of n^{2}: either vanishes or gives curvature
    - Coefficient of n^{1}: density term, must vanish for 2nd order
    - Coefficient of n^{0}: cosmological constant term

Wait — this is getting into continuum-limit scaling again. Let me
think about this purely discretely.
""")

# ══════════════════════════════════════════════════════════════
# PURELY DISCRETE APPROACH
# ══════════════════════════════════════════════════════════════

print("PURELY DISCRETE APPROACH:")
print("=" * 50)
print("""
Forget the continuum limit. Work with FINITE posets.

For a finite poset P with n elements, define:
  N_k(x) = #{y ∈ P : y < x, |[y,x]| = k+1}  (k-element interval)
  
An operator B = Σ c_k N_k is "second-order" if:
  B(x) = 0 for every x in a "homogeneous" poset.

What is a "homogeneous" poset, purely combinatorially?

DEFINITION (proposed): A finite poset is HOMOGENEOUS of type (d,n) if:
  For every x ∈ P, the interval counts N_k(x) depend only on the
  "height" of x (its longest chain to a minimal element), not on
  which element x is at that height.

In other words: all elements at the same height have the same
interval statistics. This is the discrete analogue of "flat space"
(translational invariance → every point looks the same at each time).

The SECOND-ORDER condition then becomes:
  For a homogeneous poset, Σ c_k × N_k(x) = const for all x.
  (The constant may depend on height but not on which element at that height.)

Actually, the stronger condition is:
  For a homogeneous poset, Σ c_k × N_k(x) = 0 for all interior x.
  (Vanishes in the bulk; may have boundary contributions.)

This gives constraints on the c_k in terms of the homogeneous
interval counts.
""")

# ══════════════════════════════════════════════════════════════
# COMPUTE HOMOGENEOUS INTERVAL COUNTS FOR SMALL POSETS
# ══════════════════════════════════════════════════════════════

print("COMPUTING HOMOGENEOUS INTERVAL COUNTS")
print("-" * 40)

# The simplest homogeneous posets are the "antichain layers" model:
# L layers, each with w elements, with every element in layer i
# related to every element in layer i-1 (the "thick chain").
#
# For such a poset, at a generic element x in layer h:
# N_0(x) = w (the w elements in layer h-1 that are covered by x)
# N_1(x) = w^2 - w (pairs in layers h-2 and h-1 with 1 between)
# ... this gets complicated because of the "width" w.

# Actually, the cleanest homogeneous poset is the BOOLEAN LATTICE
# or the CROWN. But for causal sets, the natural homogeneous model
# is the POISSON SPRINKLING of a flat Alexandrov interval.

# Let me use a different approach: compute N_k for actual sprinklings
# and check what constraints "second-order" imposes.

# For a Poisson sprinkling at density ρ in d dimensions, the expected
# interval counts are KNOWN (Dowker-Glaser):
#
# <N_k>(ρ,V) = C_d(k) × (ρV)^{k+1}
#
# where C_d(k) = Γ(d/2 + 1)^{k+1} / (Γ((k+1)(d/2) + 1) × (k+1)!)
#
# This is a specific function of k and d.

def C_d_k(d, k):
    """Expected N_k per unit ρV for d-dimensional Poisson sprinkling."""
    # <N_k> = C_d(k) × (ρV)^{k+1}
    # C_d(k) = Γ(d/2+1)^{k+1} / (Γ((k+1)d/2 + 1) × Γ(k+2))
    num = Gamma(d/2 + 1)**(k+1)
    den = Gamma((k+1)*d/2 + 1) * Gamma(k+2)
    return num / den

print(f"\nExpected interval counts C_d(k) [<N_k> = C_d(k) × (ρV)^(k+1)]:")
print(f"{'k':>3}", end="")
for d in [2, 3, 4, 5, 6]:
    print(f"  {'d='+str(d):>12}", end="")
print()
print("  " + "-" * 65)

for k in range(7):
    print(f"{k:3d}", end="")
    for d in [2, 3, 4, 5, 6]:
        val = C_d_k(d, k)
        print(f"  {val:12.6f}", end="")
    print()

# ══════════════════════════════════════════════════════════════
# THE SECOND-ORDER CONDITION IN TERMS OF C_d(k)
# ══════════════════════════════════════════════════════════════

print(f"\n{'='*50}")
print("SECOND-ORDER CONDITION")
print(f"{'='*50}")

print("""
The operator B = Σ c_k N_k applied to a constant field on a flat
d-dimensional sprinkling gives:

  <B(1)>(x) = Σ c_k × <N_k>(x) = Σ c_k × C_d(k) × (ρV)^{k+1}

For this to be "second order" (vanish at leading order in ρV):

  Σ c_k × C_d(k) × λ^{k+1} = O(λ^{2/d})  for large λ = ρV

This requires the coefficients of λ^{K+1}, λ^K, ..., λ^{2/d+1}
to all vanish. That's K+1 - (2/d+1) = K - 2/d constraints.

For d=4, K=4: K - 2/d = 4 - 0.5 = 3.5, so 3 or 4 constraints
on 4 free parameters (c_1,...,c_4 after fixing c_0 = birth term).

Wait — this uses the continuum scaling again. Let me be more careful.

Actually, for a PURELY DISCRETE "second-order" condition, I need:
  B vanishes identically on a HOMOGENEOUS poset (not just at leading order).
  
On a homogeneous poset of "size" n:
  N_k(x) = C_d(k) × n^{k+1} + lower order terms

The condition "B = 0 on homogeneous posets OF ALL SIZES" gives:
  Σ c_k × C_d(k) × n^{k+1} = 0 for all n

Since this must hold for ALL n, each power of n must vanish independently.
But n^{k+1} are distinct powers, so this would force c_k × C_d(k) = 0
for each k, hence c_k = 0 for all k. TRIVIAL!

The resolution: B doesn't vanish IDENTICALLY on flat posets.
It gives a BOUNDARY CONTRIBUTION that scales differently from the bulk.

In the continuum: <B(1)> = boundary_term + bulk_term
  boundary_term ∝ n^{(K+1)/(K+1)} = n^1  (linear in n)
  bulk_term ∝ n^{2/d} (curvature) = 0 on flat space

So the actual condition is: the non-boundary part of <B(1)> vanishes.
""")

# Let me try a COMPLETELY DIFFERENT approach that avoids all of this.

print(f"\n{'='*65}")
print("ALTERNATIVE: FUNCTIONAL EQUATION APPROACH")
print(f"{'='*65}")

print("""
Instead of working with expected values and continuum limits,
let's ask a purely ALGEBRAIC question in the incidence algebra.

The incidence algebra A(P) of a poset P has elements f: Intervals → ℝ.
Multiplication is convolution: (f*g)(x,y) = Σ_{x≤z≤y} f(x,z)g(z,y).
The identity is the delta function δ(x,y).
The zeta function ζ(x,y) = 1 for all x ≤ y.
The Möbius function μ = ζ⁻¹.

The BDG operator is P(ζ) = Σ c_k ζ^k (a polynomial in ζ).

KEY ALGEBRAIC FACT: In the incidence algebra, the Möbius function μ
satisfies μ * ζ = δ. This means μ is the UNIQUE left inverse of ζ.

The BDG operator is NOT μ. It's a POLYNOMIAL in ζ, which is different.
But there's a relationship: the BDG operator is the TRUNCATED VERSION
of a function of ζ.

Specifically, if we write the d'Alembertian as a formal power series
in ζ: □ = Σ_{k=0}^∞ α_k ζ^k, then the BDG operator is the truncation
at k = K: B = Σ_{k=0}^K c_k ζ^k.

The question is: what ALGEBRAIC property of P(ζ) determines the c_k?

CONJECTURE: The BDG operator is the unique polynomial P(ζ) of degree K
such that:
  (1) P(ζ) * ζ^{K-1} = (something with specific symmetry properties)
  (2) P annihilates the "flat" part of the interval structure

This is a FINITE ALGEBRAIC PROBLEM: find the polynomial P of degree K
in the incidence algebra that satisfies specific convolution identities.

Let me check if the BDG polynomial satisfies any obvious algebraic
identities in the incidence algebra.
""")

# Check algebraic properties of the BDG polynomial
# P(z) = 1 - z + 9z² - 16z³ + 8z⁴
# (using z as formal variable, not complex number)

z = sp.Symbol('z')
P_bdg = 1 - z + 9*z**2 - 16*z**3 + 8*z**4

print(f"BDG polynomial: P(z) = {P_bdg}")
print()

# Factor
factors = sp.factor(P_bdg)
print(f"Factored: {factors}")

# Try to factor over rationals/reals
roots = sp.solve(P_bdg, z)
print(f"Roots: {[sp.nsimplify(r, tolerance=1e-6) for r in roots]}")
print()

# Check: P(1) = 1 (birth term survives)
print(f"P(1) = {P_bdg.subs(z, 1)}")
print(f"P'(1) = {sp.diff(P_bdg, z).subs(z, 1)}")
print(f"P''(1) = {sp.diff(P_bdg, z, 2).subs(z, 1)}")
print()

# Check: does P satisfy P(z) = (1-z) × Q(z) + 1 for some Q?
# P(z) - 1 = -z + 9z² - 16z³ + 8z⁴ = z(-1 + 9z - 16z² + 8z³)
Q1 = sp.simplify((P_bdg - 1) / z)
print(f"(P(z) - 1) / z = {Q1}")
print(f"  = {sp.factor(Q1)}")
print()

# Factor Q1
Q1_factored = sp.factor(Q1)
print(f"Q1 factored: {Q1_factored}")
Q1_roots = sp.solve(Q1, z)
print(f"Q1 roots: {[sp.nsimplify(r, tolerance=1e-4) for r in Q1_roots]}")
print()

# Interesting: Q1 = 8z³ - 16z² + 9z - 1
# Check if Q1(1) = 0 (would mean (z-1) is a factor):
print(f"Q1(1) = {Q1.subs(z, 1)}")  # 8-16+9-1 = 0 !!
print("Q1(1) = 0 → (z-1) is a factor of Q1!")
print()

Q2 = sp.simplify(Q1 / (z - 1))
print(f"Q1 / (z-1) = Q2 = {sp.expand(Q2)}")
Q2_factored = sp.factor(Q2)
print(f"Q2 factored: {Q2_factored}")
Q2_roots = sp.solve(Q2, z)
print(f"Q2 roots: {[sp.nsimplify(r, tolerance=1e-4) for r in Q2_roots]}")
print()

# So P(z) = 1 + z(z-1) × Q2(z)
# = 1 + z(z-1)(8z² - 8z + 1)
# Check:
P_reconstructed = 1 + z*(z-1)*(8*z**2 - 8*z + 1)
print(f"P(z) = 1 + z(z-1)(8z² - 8z + 1)?")
print(f"  Expanded: {sp.expand(P_reconstructed)}")
print(f"  Matches BDG: {sp.expand(P_reconstructed - P_bdg) == 0}")
print()

# Now factor 8z² - 8z + 1
disc = 64 - 32
print(f"8z² - 8z + 1: discriminant = {disc} = {disc}") 
print(f"  roots: (8 ± √{disc}) / 16 = (8 ± {np.sqrt(disc):.4f}) / 16")
print(f"  = {(8 + np.sqrt(disc))/16:.6f} and {(8 - np.sqrt(disc))/16:.6f}")
print()

# So the COMPLETE factorization of the BDG polynomial is:
# P(z) = 1 + z(z-1)(8z² - 8z + 1)
#       = 1 + z(z-1) × 8(z - (1+1/√2)/2)(z - (1-1/√2)/2)

print("=" * 65)
print("KEY ALGEBRAIC STRUCTURE REVEALED")
print("=" * 65)
print(f"""
The d=4 BDG polynomial factors as:

  P(z) = 1 + z(z - 1)(8z² - 8z + 1)

This is STRUCTURALLY SIGNIFICANT:

  1. The "1" is the birth term (constant, present for any K).
  
  2. The factor z means: the correction vanishes when there are
     no elements in the past (N_k = 0 for all k > 0). At a
     "first event," only the birth term contributes.
  
  3. The factor (z - 1) means: the correction vanishes when
     evaluated at z=1, which is the second-order condition
     (Σc_k = 0 for k ≥ 1). This ensures the operator annihilates
     constant fields on homogeneous regions.
  
  4. The factor (8z² - 8z + 1) encodes the DIMENSION-SPECIFIC
     curvature response. This is where d=4 enters.

So the BDG polynomial has the STRUCTURAL FORM:

  P(z) = 1 + z(z - 1) × R_d(z)

where R_d(z) is a dimension-specific polynomial.

THE UNIQUENESS QUESTION BECOMES:
For each d, is R_d(z) uniquely determined by the remaining
constraints (minimality, self-sustaining selectivity)?

For d=4: R_4(z) = 8z² - 8z + 1 (degree 2, since K=4 and
P has degree 4 = 2 + 2 from the z(z-1) factor).

The constraint space for R_d:
  - R_d has degree K-2 = d/2 (for even d)
  - R_d must give a self-sustaining growth rule when combined
    with the z(z-1) factor
  - R_d must be "compatible" with the chord diagram structure
    (Yeats's interpretation)

For d=4: R_4 has degree 2 → 3 coefficients (a, b, c in az²+bz+c).
Do we have 3 constraints?

  Constraint 1: P'(1) = specific value? 
    P'(1) = 1 + 0 + R_4(1) + ... let me compute properly.
""")

# Compute P'(z) = d/dz [1 + z(z-1)R(z)]
R = 8*z**2 - 8*z + 1
P_check = 1 + z*(z-1)*R
dP = sp.diff(P_check, z)
print(f"P'(z) = {sp.expand(dP)}")
print(f"P'(1) = {dP.subs(z, 1)}")
print()

# P'(1) = [z'(z-1) + z(z-1)']R + z(z-1)R' evaluated at z=1
# = [(z-1) + z]R(1) + 0 = (2z-1)R(1)|_{z=1} = R(1)
print(f"R(1) = {R.subs(z, 1)}")  # 8-8+1 = 1
print(f"So P'(1) = R(1) = 1")
print()

# This means: R(1) = 1 is a constraint! (normalization)
# That's 1 constraint on 3 coefficients → 2-dimensional family.

# What other constraints do we have?
# Self-sustaining selectivity: P_acc ∈ (0,1) at μ=1.
# This is a constraint on the POISSON MODEL, not purely algebraic.

# But wait — there might be additional algebraic constraints from
# the chord diagram structure.

# Let me check: for d=2, what's R_2(z)?
# d=2 BDG: S = 1 - 2N_1, i.e. c_0=1, c_1=-2
# P_2(z) = 1 - 2z
# Can we write this as 1 + z(z-1)R_2(z)? 
# 1 - 2z = 1 + z(z-1)R → z(z-1)R = -2z → (z-1)R = -2 → R = -2/(z-1)
# This doesn't work — R would have a pole!

# So the factorization P(z) = 1 + z(z-1)R(z) is specific to d≥4 where
# the second-order condition Σc_k=0 actually holds.

# For d=2: Σc_k = c_1 = -2 ≠ 0 → NOT second order!
# This confirms: d=2 is first-order, d=4 is second-order.

print("DIMENSION CHECK:")
print(f"  d=2: P(z) = 1 - 2z. P(1) = -1 ≠ 1 → FIRST order")
print(f"  d=4: P(z) = 1 - z + 9z² - 16z³ + 8z⁴. P(1) = 1 → SECOND order")
print()

# So the second-order condition P(1) = P(0) = 1 (equivalently, Σc_k=0 for k≥1)
# is itself a constraint that selects d≥4!

# For d=4, with the structure P(z) = 1 + z(z-1)R(z) where R(1) = 1:
# R(z) = az² + bz + c with a + b + c = 1 (from R(1)=1)
# That's 2 free parameters.

# What constrains them further?
# Let me check if SELECTIVITY (the ability to accept/reject) gives constraints.

print("=" * 65)
print("SELECTIVITY CONSTRAINT ON R(z)")
print("=" * 65)

# For the growth rule to be self-sustaining, P_acc = P(S > 0) must be
# in (0,1). The action is S = P(N) where N = (N_0, N_1, ..., N_K)
# are random variables.
#
# But more specifically: the MAXIMUM of ΔS* must occur at μ ≈ 1.
# This is a constraint on the polynomial R.

# Let me parameterize R(z) = az² + bz + (1-a-b) [since R(1)=1]
# and scan for which (a,b) values give ΔS* maximum at μ ≈ 1.

from math import exp, log

def compute_delta_s_star(a_param, b_param, mu=1.0, n_samples=200000):
    """Compute ΔS* = -log(P_acc) for R(z) = a*z² + b*z + (1-a-b)."""
    c_param = 1 - a_param - b_param
    
    # P(z) = 1 + z(z-1)(a*z² + b*z + c)
    # Expand: need c_0, c_1, c_2, c_3, c_4
    # z(z-1)(az² + bz + c) = (z²-z)(az² + bz + c)
    # = az⁴ + bz³ + cz² - az³ - bz² - cz
    # = az⁴ + (b-a)z³ + (c-b)z² - cz
    
    c0_coeff = 1  # birth term (not part of N_k)
    c1 = -c_param
    c2 = c_param - b_param
    c3 = b_param - a_param
    c4 = a_param
    
    coeffs = [c1, c2, c3, c4]
    
    # Poisson parameters at density mu
    lambdas = [mu**(k+1) / factorial(k+1) for k in range(4)]
    
    # Sample
    samples = np.array([np.random.poisson(lam, n_samples) for lam in lambdas]).T
    
    S = np.ones(n_samples)  # birth term
    for k in range(4):
        S += coeffs[k] * samples[:, k]
    
    P_acc = np.mean(S > 0)
    if P_acc <= 0 or P_acc >= 1:
        return None, coeffs
    
    delta_s = -log(P_acc)
    return delta_s, coeffs

# BDG values: a=8, b=-8, c=1 (and a+b+c = 1 ✓)
ds_bdg, c_bdg = compute_delta_s_star(8, -8, mu=1.0)
print(f"BDG (a=8, b=-8, c=1): ΔS* = {ds_bdg:.4f}, coeffs = {c_bdg}")
print(f"  Compare: BDG actual = [-1, 9, -16, 8] → {[-1, 9-0, -16, 8]}")
print()

# Verify the expansion
print("Verification of P(z) = 1 + z(z-1)(8z²-8z+1):")
print(f"  c_1 = -c = -1 ✓")
print(f"  c_2 = c-b = 1-(-8) = 9 ✓")
print(f"  c_3 = b-a = -8-8 = -16 ✓")
print(f"  c_4 = a = 8 ✓")
print()

# Now scan the (a,b) parameter space
print("Scanning (a,b) parameter space for ΔS* at μ=1:")
print(f"{'a':>6} {'b':>6} {'c':>6}  {'c1':>4} {'c2':>4} {'c3':>5} {'c4':>4}  {'ΔS*':>8}  {'Σck':>4}")
print("-" * 65)

results = []
for a in np.arange(1, 16, 1):
    for b in np.arange(-15, 1, 1):
        c = 1 - a - b
        ds, coeffs = compute_delta_s_star(a, b, mu=1.0, n_samples=100000)
        if ds is not None and ds > 0.01:
            sc = sum(coeffs)
            results.append((ds, a, b, c, coeffs, sc))

results.sort(key=lambda x: -x[0])  # sort by ΔS* descending

print("\nTop 15 by selectivity (highest ΔS*):")
for ds, a, b, c, coeffs, sc in results[:15]:
    c1, c2, c3, c4 = coeffs
    marker = " ← BDG" if (a==8 and b==-8) else ""
    print(f"{a:6.0f} {b:6.0f} {c:6.0f}  {c1:4.0f} {c2:4.0f} {c3:5.0f} {c4:4.0f}  {ds:8.4f}  {sc:4.0f}{marker}")

print()
# Check if BDG is at or near the maximum
bdg_ds = [r for r in results if r[1]==8 and r[2]==-8]
if bdg_ds:
    rank = results.index(bdg_ds[0]) + 1
    print(f"BDG rank by ΔS*: #{rank} out of {len(results)}")
    print(f"BDG ΔS* = {bdg_ds[0][0]:.4f}")
    print(f"Maximum ΔS* = {results[0][0]:.4f} at a={results[0][1]}, b={results[0][2]}")

