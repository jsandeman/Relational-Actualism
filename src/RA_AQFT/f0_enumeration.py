"""
f0_enumeration.py — Canonical computation of the BDG path-weight ratio
=======================================================================

Computes the exact RA-native path-weight ratio W_other / W_baryon = 17.32
that enters the baryon-to-dark-matter ratio f_0 in Paper II §4.9.

At density μ = 1 (the Planck density, operating point of the BDG filter),
the Poisson-CSG weight of a vertex with profile N = (n1, n2, n3, n4) is:

    W(N | μ=1) = 1 / (n1! n2! n3! n4!)

because each λ_k = μ^k/k! evaluated at μ=1 gives Pois(1), and the joint
weight of N under independent Poisson marginals is

    P(N) = e^{-4} · ∏_k 1/n_k!

The factor e^{-4} is shared across all configurations and cancels in ratios.

The BDG filter admits a vertex iff S_BDG(N) > 0, with
    S_BDG(N) = c_0 + c_1 n_1 + c_2 n_2 + c_3 n_3 + c_4 n_4
             = 1 - n_1 + 9 n_2 - 16 n_3 + 8 n_4.

Baryon configurations (the three-quark bound state topology in RA):
  N_quark   = (2, 1, 0, 0)   → W_quark   = 1/(2! 1! 0! 0!) = 1/2
  N_fermion = (1, 1, 1, 1)   → W_fermion = 1/(1! 1! 1! 1!) = 1
  W_baryon  = 1/2 + 1 = 3/2 EXACTLY.

W_other is the sum of weights over all non-elementary, non-baryon
N-vectors with S_BDG(N) > 0.

The elementary N-vectors (hard-coded, not baryons):
  (0,0,0,0): S=1   (vacuum successor, type 5 lepton-like)
  (1,1,0,0): S=9   (EM-charged singlet)
  (1,2,0,0): S=18  (gluon-like)

Running: python3 f0_enumeration.py

Expected output: W_other / W_baryon = 17.32 (to two decimal places,
stable from max_n=10 upward).

This is a CV (computation-verified) claim. No free parameters; all
inputs are the BDG integers (1, -1, 9, -16, 8).

--
Joshua F. Sandeman, April 2026.
Reconstructed from RA Main Chat 2 (April 8, 2026) canonical enumeration.
"""

from math import factorial
from itertools import product

# ===========================================================================
# BDG coefficients (1, -1, 9, -16, 8) for d=4
# ===========================================================================
C0, C1, C2, C3, C4 = 1, -1, 9, -16, 8


def s_bdg(n1: int, n2: int, n3: int, n4: int) -> int:
    """BDG score S(N) = 1 - n1 + 9 n2 - 16 n3 + 8 n4."""
    return C0 + C1 * n1 + C2 * n2 + C3 * n3 + C4 * n4


def weight(n1: int, n2: int, n3: int, n4: int) -> float:
    """Poisson weight at μ=1: 1 / (n1! n2! n3! n4!). The common e^{-4}
    factor is omitted (it cancels in ratios)."""
    return 1.0 / (factorial(n1) * factorial(n2) * factorial(n3) * factorial(n4))


# ===========================================================================
# Classification: which N-vectors count as baryons vs elementary vs "other"
# ===========================================================================

BARYON_VECS = {(2, 1, 0, 0),   # quark
               (1, 1, 1, 1)}   # fermion (three-quark renewal)

ELEMENTARY_VECS = {(0, 0, 0, 0),   # lepton-like singlet (S=1)
                   (1, 1, 0, 0),   # EM-charged singlet (S=9)
                   (1, 2, 0, 0),   # gluon-like (S=18)
                   (2, 1, 0, 0),   # quark (in baryons)
                   (1, 1, 1, 1)}   # fermion (in baryons)


def classify(N: tuple) -> str:
    if N in BARYON_VECS:
        return "baryon"
    if N in ELEMENTARY_VECS:
        return "elementary_other"  # elementary but not a baryon component
    return "other"


# ===========================================================================
# Exact enumeration
# ===========================================================================

def enumerate_weights(max_n: int) -> dict:
    """Enumerate all N-vectors with 0 <= n_k <= max_n for each k.
    Returns totals for baryon, elementary_other, other, and all S>0."""
    W_baryon = 0.0
    W_elem_other = 0.0
    W_other = 0.0
    W_total_pos = 0.0

    for n1, n2, n3, n4 in product(range(max_n + 1), repeat=4):
        if s_bdg(n1, n2, n3, n4) <= 0:
            continue
        w = weight(n1, n2, n3, n4)
        W_total_pos += w
        klass = classify((n1, n2, n3, n4))
        if klass == "baryon":
            W_baryon += w
        elif klass == "elementary_other":
            W_elem_other += w
        else:
            W_other += w

    return {
        "W_baryon": W_baryon,
        "W_elem_other": W_elem_other,
        "W_other": W_other,
        "W_total_pos": W_total_pos,
        "max_n": max_n,
    }


# ===========================================================================
# Stability check: confirm the ratio converges as max_n increases
# ===========================================================================

def stability_table() -> None:
    """Print W_other / W_baryon for max_n = 4, 6, 8, 10, 12."""
    print()
    print(f"  {'max_n':>6} {'W_baryon':>12} {'W_other':>12} "
          f"{'ratio':>10} {'Δ from prev':>14}")
    print("  " + "-" * 60)

    prev_ratio = None
    for max_n in [4, 6, 8, 10, 12]:
        res = enumerate_weights(max_n)
        ratio = res["W_other"] / res["W_baryon"]
        if prev_ratio is None:
            delta_str = ""
        else:
            delta = ratio - prev_ratio
            delta_str = f"{delta:+.2e}"
        print(f"  {max_n:>6d} {res['W_baryon']:>12.6f} "
              f"{res['W_other']:>12.6f} {ratio:>10.4f} {delta_str:>14}")
        prev_ratio = ratio


# ===========================================================================
# Main
# ===========================================================================

def main():
    print("=" * 72)
    print("f0_enumeration.py — BDG path-weight ratio W_other / W_baryon")
    print("=" * 72)
    print()
    print("BDG coefficients: (c0, c1, c2, c3, c4) = (1, -1, 9, -16, 8)")
    print("Density: μ = 1 (Planck density, BDG operating point)")
    print("Weight at μ=1: W(N) = 1 / (n1! n2! n3! n4!)")
    print("Filter: admit N iff S_BDG(N) = 1 - n1 + 9 n2 - 16 n3 + 8 n4 > 0")
    print()

    # Baryon sanity check
    w_quark = weight(2, 1, 0, 0)
    w_fermion = weight(1, 1, 1, 1)
    print("Baryon decomposition (exact):")
    print(f"  W(quark,   (2,1,0,0)) = 1/(2!·1!·0!·0!) = 1/2 = {w_quark}")
    print(f"  W(fermion, (1,1,1,1)) = 1/(1!·1!·1!·1!) = 1   = {w_fermion}")
    print(f"  W_baryon = 1/2 + 1 = 3/2 = {w_quark + w_fermion}")
    assert abs((w_quark + w_fermion) - 1.5) < 1e-12

    # Main computation at max_n=12
    print()
    print("Enumerating all N-vectors with 0 <= n_k <= 12 satisfying S_BDG > 0...")
    res = enumerate_weights(max_n=12)
    ratio = res["W_other"] / res["W_baryon"]

    print()
    print(f"  W_baryon       = {res['W_baryon']:.6f}  (exact: 1.500000)")
    print(f"  W_elementary_other = {res['W_elem_other']:.6f}  "
          f"(non-baryon elementary S>0)")
    print(f"  W_other        = {res['W_other']:.6f}  "
          f"(non-elementary, non-baryon, S>0)")
    print(f"  W_total (S>0)  = {res['W_total_pos']:.6f}")
    print()
    print(f"  RATIO: W_other / W_baryon = {ratio:.4f}")
    print()

    # Stability table
    print("Stability check — ratio as function of enumeration cutoff max_n:")
    stability_table()

    # Paper claim
    print()
    print("-" * 72)
    print("Paper II §4.9 claim: W_other / W_baryon = 17.32")
    print(f"Computed value:     W_other / W_baryon = {ratio:.4f}")
    print(f"Agreement to two decimal places: "
          f"{'YES' if abs(ratio - 17.32) < 0.01 else 'NO'}")
    print()
    print("f_0 = (W_other / W_baryon) × α_s(2 m_p) = 17.32 × 0.312 = 5.40")
    print("Planck: Ω_DM / Ω_b = 5.416 ± 0.015. Match: 0.3%.")
    print()
    print("NOTE: The 17.32 is fully RA-native (BDG enumeration, zero free")
    print("parameters). The α_s(2 m_p) = 0.312 uses standard SM QCD RG")
    print("running from the RA-native UV fixed point α_s(m_Z) = 1/√72")
    print("down to the hadronic scale. This RG step is not a free parameter")
    print("but is an external input to the f_0 calculation. See Paper II")
    print("§4.9 epistemic note.")
    print("-" * 72)


if __name__ == "__main__":
    main()
