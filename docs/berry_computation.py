"""
Berry Phase v3: Boundary-Coupled BDG Action
============================================

THEOREM (v1+v2): Berry phase is identically zero if continuation
phases are constants (independent of boundary condition).

RESOLUTION: The BDG action of a continuation must ITSELF depend on
the boundary configuration. Physically: a continuation that connects
to the boundary at depth k "sees" the boundary's state, which
modifies the causal structure and hence the BDG score.

The modified action:
  S_BDG(N, β) = S_BDG(N) + coupling(N, β)

where coupling(N, β) represents the interaction between the
continuation's causal structure and the boundary state.

This is physically correct: in the causal graph, a continuation's
ancestors include boundary vertices, and those vertices have states.
The BDG score counts causal intervals, which INCLUDE intervals
through the boundary. Different boundary states → different interval
counts → different S_BDG.
"""

import numpy as np
from math import factorial, exp
import cmath

c_bdg = np.array([1, -1, 9, -16, 8])

def S_bdg(N):
    return c_bdg[0] + sum(c_bdg[k+1]*N[k] for k in range(4))

print("=" * 80)
print("BERRY PHASE v3: BOUNDARY-COUPLED BDG ACTION")
print("=" * 80)

print("""
WHY v1 AND v2 GAVE ZERO:
  Ψ(θ) = Σ_k w_k(θ) × exp(i × S_k)
  with S_k independent of θ → Berry phase = 0 (theorem).

THE FIX:
  The BDG score of a continuation MUST depend on boundary state.
  Physically: causal intervals include intervals THROUGH boundary
  vertices. Different boundary states → different interval structure
  → different BDG scores → parameter-dependent phases.

  S_BDG(continuation, boundary) = S_BDG(N) + δS(N, β)

  where δS is the boundary coupling: how much the boundary state
  modifies the causal interval count at each depth.
""")

def compute_coupled_amplitude(N0, mu, theta, coupling_strength=0.3):
    """
    Compute Ψ(θ) with boundary-coupled BDG action.

    The boundary condition θ modifies the BDG score of continuations
    via a depth-dependent coupling:

    S(N, θ) = S_BDG(N) + η × Σ_k N_k × cos(θ + 2πk/4)

    The cos(θ + 2πk/4) term represents the angular coupling between
    the boundary "direction" and the depth-k channel. Different depths
    couple at different angular phases, creating the ROTATION that
    Berry phase requires.

    This is the RA analogue of spin-field coupling: different
    spin components (depths) couple differently to the external
    field (boundary direction), creating anisotropic phase shifts.
    """
    eta = coupling_strength

    lam = [mu**(k+1)/factorial(k+1) for k in range(4)]

    amp = complex(0, 0)

    # Single-step continuations
    for k in range(4):
        N_new = list(N0); N_new[k] += 1
        s_base = S_bdg(N_new)

        # Boundary coupling: depth k couples at angle 2πk/4
        # The k-th depth's contribution to the score is shifted
        # by the projection of the boundary direction onto that depth
        delta_s = eta * np.cos(theta + 2*np.pi*k/4)

        s_coupled = s_base + delta_s

        if s_base > 0:  # use base score for admissibility
            w = np.sqrt(abs(lam[k]) * exp(-abs(lam[k])))
            phase = cmath.exp(1j * s_coupled)  # COUPLED phase
            amp += w * phase

    # Two-step continuations
    for k1 in range(4):
        N1 = list(N0); N1[k1] += 1
        if S_bdg(N1) <= 0: continue
        for k2 in range(4):
            N2 = list(N1); N2[k2] += 1
            s2_base = S_bdg(N2)
            if s2_base > 0:
                delta_s = eta * (np.cos(theta + 2*np.pi*k1/4) +
                                 np.cos(theta + 2*np.pi*k2/4))
                w1 = np.sqrt(abs(lam[k1]) * exp(-abs(lam[k1])))
                w2 = np.sqrt(abs(lam[k2]) * exp(-abs(lam[k2])))
                amp += 0.3 * w1 * w2 * cmath.exp(1j * (s2_base + delta_s))

    return amp

def compute_berry(N0, mu, n_points=500, coupling=0.3):
    thetas = np.linspace(0, 2*np.pi, n_points + 1)
    psis = [compute_coupled_amplitude(N0, mu, t, coupling) for t in thetas]

    prod = complex(1, 0)
    for i in range(n_points):
        pi = psis[i]; pj = psis[i+1]
        if abs(pi) > 1e-15 and abs(pj) > 1e-15:
            prod *= np.conj(pi) * pj / (abs(pi) * abs(pj))
    return cmath.phase(prod)

# ================================================================
# COMPUTE ACROSS PROFILES, COUPLINGS, DENSITIES
# ================================================================

mu = 1.5

print(f"\n1. BERRY PHASE BY PROFILE (η=0.3, μ={mu})")
print("─" * 70)

profiles = {
    '(1,0,0,0)': [1,0,0,0],
    '(0,1,0,0)': [0,1,0,0],
    '(1,1,0,0)': [1,1,0,0],
    '(2,1,0,0)': [2,1,0,0],
    '(2,2,0,0)': [2,2,0,0],
    '(3,1,0,0)': [3,1,0,0],
}

print(f"{'Profile':<14} {'S':>4} {'γ (rad)':>14} {'γ/π':>10} {'γ (deg)':>10}")
print("─" * 55)
for name, N in profiles.items():
    s = S_bdg(N)
    g = compute_berry(N, mu, 500, 0.3)
    print(f"{name:<14} {s:>4} {g:>14.6f} {g/np.pi:>10.4f} {np.degrees(g):>10.2f}")

print(f"\n\n2. COUPLING STRENGTH DEPENDENCE (profile (1,1,0,0), μ={mu})")
print("─" * 70)
print(f"{'η':>8} {'γ (rad)':>14} {'γ/π':>10}")
print("─" * 35)
for eta in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]:
    g = compute_berry([1,1,0,0], mu, 500, eta)
    print(f"{eta:>8.2f} {g:>14.6f} {g/np.pi:>10.4f}")

print(f"\n\n3. DENSITY DEPENDENCE (profile (1,1,0,0), η=0.3)")
print("─" * 70)
print(f"{'μ':>8} {'γ (rad)':>14} {'γ/π':>10}")
print("─" * 35)
for mu_test in [0.5, 1.0, 1.5, 2.0, 3.0, 4.71, 5.0]:
    g = compute_berry([1,1,0,0], mu_test, 500, 0.3)
    print(f"{mu_test:>8.2f} {g:>14.6f} {g/np.pi:>10.4f}")

print(f"\n\n4. GEOMETRIC TESTS (profile (1,1,0,0), μ=1.5, η=0.3)")
print("─" * 70)

g_fwd = compute_berry([1,1,0,0], 1.5, 500, 0.3)

# Reverse: go θ from 2π to 0
thetas_rev = np.linspace(2*np.pi, 0, 501)
psis_rev = [compute_coupled_amplitude([1,1,0,0], 1.5, t, 0.3) for t in thetas_rev]
prod_rev = complex(1,0)
for i in range(500):
    pi=psis_rev[i]; pj=psis_rev[i+1]
    if abs(pi)>1e-15 and abs(pj)>1e-15:
        prod_rev *= np.conj(pi)*pj/(abs(pi)*abs(pj))
g_rev = cmath.phase(prod_rev)

# Double loop
thetas_dbl = np.linspace(0, 4*np.pi, 1001)
psis_dbl = [compute_coupled_amplitude([1,1,0,0], 1.5, t, 0.3) for t in thetas_dbl]
prod_dbl = complex(1,0)
for i in range(1000):
    pi=psis_dbl[i]; pj=psis_dbl[i+1]
    if abs(pi)>1e-15 and abs(pj)>1e-15:
        prod_dbl *= np.conj(pi)*pj/(abs(pi)*abs(pj))
g_dbl = cmath.phase(prod_dbl)

print(f"  Forward loop:  γ = {g_fwd:+.6f} rad ({g_fwd/np.pi:+.4f}π)")
print(f"  Reversed loop: γ = {g_rev:+.6f} rad ({g_rev/np.pi:+.4f}π)")
print(f"  Sum (should≈0): {g_fwd+g_rev:.6f}")
print(f"  Forward+Reverse = 0? {'YES' if abs(g_fwd+g_rev)<0.01 else 'NO (off by '+f'{abs(g_fwd+g_rev):.4f})'}")
print(f"  Double loop:   γ = {g_dbl:+.6f} rad ({g_dbl/np.pi:+.4f}π)")
print(f"  2×Forward = {2*g_fwd:+.6f}")
print(f"  Double = 2×Single? {'YES' if abs(g_dbl-2*g_fwd)<0.01 else 'CLOSE' if abs(g_dbl-2*g_fwd)<0.1 else 'NO'}")

# ================================================================
# INTERPRETATION
# ================================================================

print(f"""

5. INTERPRETATION
{'='*80}

THE THEOREM (from v1 + v2):
  Berry phase = 0 if continuation phases are parameter-independent.
  This is exact: Ψ = Σ w_k(θ) exp(iφ_k) with constant φ_k gives
  zero holonomy for any closed loop.

THE RESOLUTION (v3):
  The BDG action must include a COUPLING TERM between the
  continuation and the boundary state:

    S(continuation, boundary) = S_BDG(N) + δS(N, β)

  This coupling creates PARAMETER-DEPENDENT PHASES, which is
  what Berry phase requires.

THE PHYSICAL MEANING OF THE COUPLING:
  In the causal graph, a continuation connects to boundary vertices.
  Those vertices have states. The causal intervals counted by the
  BDG action INCLUDE intervals through the boundary. When the
  boundary state changes, the interval count changes, modifying
  the BDG score.

  The coupling δS = η Σ_k N_k cos(θ + 2πk/4) models this:
  each depth channel "sees" the boundary direction at a different
  angle, creating anisotropic phase shifts.

  This is EXACTLY analogous to the standard spin-field coupling:
    H = -μ B⃗ · σ⃗
  where different spin components couple differently to the
  external field direction. In BDG:
    S = S₀ + η Σ_k N_k cos(θ + 2πk/K)
  where different depth channels couple differently to the
  boundary direction.

THE STATUS OF THE COUPLING:
  The coupling δS is NOT imported from standard QM. It is a
  consequence of the BDG action's dependence on the full causal
  structure, WHICH INCLUDES THE BOUNDARY.

  However, the SPECIFIC FORM of the coupling (cosine, angular,
  depth-dependent) is an ANSATZ in this computation. The exact
  coupling should be DERIVABLE from the BDG interval-counting
  formula applied to a graph with specified boundary states.

  That derivation is the concrete OPEN TARGET.

THREE LAYERS (per ChatGPT's recommendation):

  Layer A (Constructed in this note):
    - The zero-holonomy theorem for constant-phase sums
    - The boundary-coupling mechanism as the resolution
    - The discrete connection with coupled amplitudes
    - Nonzero Berry phase demonstrated (if γ ≠ 0 above)

  Layer B (Consistency, partially checked):
    - Geometric properties (reversal, double loop)
    - Coupling-strength dependence (should grow with η)
    - Profile dependence (different particles, different γ)

  Layer C (Open):
    - Derive the coupling δS from BDG interval counting
    - Recover γ = -Ω/2 for spin-1/2 from native coupling
    - Non-Abelian Berry phase from degenerate continuations
    - Connection to GS02 gauge structure
""")
