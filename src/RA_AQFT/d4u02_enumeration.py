"""
Canonical D4U02 Enumeration
============================
Reproduces the exact values from d4u02_proof_v2.docx (Sandeman, April 2026).

For d=4 BDG coefficients c = (1, -1, 9, -16, 8), computes:
  - P_acc(mu)       = P(S(mu) > 0) where S = 1 - N_1 + 9 N_2 - 16 N_3 + 8 N_4
  - Delta_S_star    = -log P_acc(mu)
  - dP_acc/dmu at mu=1 via Stein-Papangelou identity (exact)
  - d^2 P_acc/dmu^2 at mu=1 via second-order finite differences
  - mu* (first local maximum of Delta_S_star) via Taylor expansion
  - mu_QCD = exp(sqrt(4 * Delta_S_star))   (derived, zero free parameters)

This is the CANONICAL reference script for d=4 D4U02 computations.
All downstream RA scripts should obtain P_acc and Delta_S_star by
calling compute_d4u02() rather than hardcoding rounded values.

Joshua F. Sandeman + Claude (Opus 4.7), April 2026.
"""

import numpy as np
from math import exp, log, factorial
from itertools import product


# Canonical d=4 BDG coefficients from Benincasa-Dowker-Glaser (2013),
# Lean-verified via O14 uniqueness (RA_O14_Uniqueness.lean, 47 theorems,
# zero sorry).
#
# S(mu) = 1 + (-1)*N_1 + 9*N_2 + (-16)*N_3 + 8*N_4
BDG_D4 = (1, -1, 9, -16, 8)


def enumerate_S_distribution(mu, c, N_max):
    """
    Enumerate the full distribution P(S = n) for
      S = c[0] + sum_{k=1}^{K} c[k] * N_k
    where N_k ~ Pois(mu^k / k!) independently.

    Returns (dist, truncation_error).
    dist is a {n: P(S=n)} dictionary.
    """
    K = len(c) - 1
    lam = [mu ** k / factorial(k) for k in range(1, K + 1)]

    poisson_pmfs = []
    for k_idx, lam_k in enumerate(lam):
        M = N_max[k_idx]
        pmf = [exp(-lam_k) * lam_k ** n / factorial(n) for n in range(M + 1)]
        poisson_pmfs.append(pmf)

    dist = {}
    total_prob = 0.0
    ranges = [range(len(pmf)) for pmf in poisson_pmfs]
    for tup in product(*ranges):
        p = 1.0
        for i, n_k in enumerate(tup):
            p *= poisson_pmfs[i][n_k]
        s = c[0] + sum(c[k + 1] * n_k for k, n_k in enumerate(tup))
        dist[s] = dist.get(s, 0.0) + p
        total_prob += p

    return dist, 1.0 - total_prob


def P_acc(mu, c, N_max):
    """P(S > 0) at density mu for coefficients c."""
    dist, _ = enumerate_S_distribution(mu, c, N_max)
    return sum(p for s, p in dist.items() if s > 0)


def dPacc_dmu_stein(mu, c, N_max):
    """
    dP_acc/dmu via Stein-Papangelou identity:
      dP_acc/dmu = sum_{k=1}^{K} E[f(S + c_k) - f(S)] * mu^(k-1)/(k-1)!
    where f(x) = 1[x > 0].  Exact, no finite differences.
    """
    dist, _ = enumerate_S_distribution(mu, c, N_max)
    K = len(c) - 1
    P_base = sum(p for s, p in dist.items() if s > 0)
    total = 0.0
    for k in range(1, K + 1):
        ck = c[k]
        weight = mu ** (k - 1) / factorial(k - 1)
        P_shifted = sum(p for s, p in dist.items() if s + ck > 0)
        total += weight * (P_shifted - P_base)
    return total


def weight_function(c):
    """
    Closed-form w(n) at mu=1:
      w(n) = sum_{k=1}^{K} (1[n + c_k > 0] - 1[n > 0]) / (k-1)!

    For d=4, reproduces document section 4.
    """
    K = len(c) - 1
    c_vals = c[1:]
    min_n = min(-abs(ck) for ck in c_vals) - 1
    max_n = max(abs(ck) for ck in c_vals) + 1
    w_table = {}
    for n in range(min_n, max_n + 1):
        w_n = 0.0
        for k in range(1, K + 1):
            ck = c[k]
            ind_shifted = 1 if n + ck > 0 else 0
            ind_base = 1 if n > 0 else 0
            w_n += (ind_shifted - ind_base) / factorial(k - 1)
        if w_n != 0:
            w_table[n] = w_n
    return w_table


def tight_N_max(mu, c, target_truncation=1e-13):
    """Find smallest N_max giving truncation error < target_truncation."""
    K = len(c) - 1
    N_max = []
    for k in range(1, K + 1):
        lam_k = mu ** k / factorial(k)
        p = exp(-lam_k)
        cum = p
        M = 0
        threshold = target_truncation / K
        while 1 - cum > threshold and M < 100:
            M += 1
            p = p * lam_k / M
            cum += p
        N_max.append(M + 2)
    return tuple(N_max)


def compute_d4u02(verbose=True, tight_window=True):
    """
    Certified computation of mu* for d=4 per d4u02_proof_v2.docx.

    Parameters
    ----------
    verbose : bool
        Print intermediate results with comparison to document values.
    tight_window : bool
        If True, expand N_max beyond document's [15,8,5,3] to get
        truncation < 1e-13.  If False, use document's window exactly.
    """
    c = BDG_D4
    if tight_window:
        N_max = tight_N_max(1.0, c, target_truncation=1e-13)
    else:
        N_max = (15, 8, 5, 3)

    if verbose:
        print("=" * 70)
        print("D4U02 Certified Computation (d=4)")
        print("  Source: d4u02_proof_v2.docx (Sandeman, April 2026)")
        print("=" * 70)
        print(f"  BDG coefficients: {c}")
        print(f"  S(mu) = 1 - N_1 + 9 N_2 - 16 N_3 + 8 N_4")
        print(f"  Enumeration window: {N_max}")
        print()

    dist_mu1, trunc_err = enumerate_S_distribution(1.0, c, N_max)

    # Document's six key probabilities
    P_S_eq_1 = dist_mu1.get(1, 0.0)
    P_neg7_to_0 = sum(p for s, p in dist_mu1.items() if -7 <= s <= 0)
    P_S_eq_m8 = dist_mu1.get(-8, 0.0)
    P_2_to_16 = sum(p for s, p in dist_mu1.items() if 2 <= s <= 16)
    P_acc_mu1 = sum(p for s, p in dist_mu1.items() if s > 0)

    # dP_acc/dmu by two methods (independent check)
    dP_via_w = (P_S_eq_m8
                + (7 / 6) * P_neg7_to_0
                - (3 / 2) * P_S_eq_1
                - (1 / 2) * P_2_to_16)
    dP_via_stein = dPacc_dmu_stein(1.0, c, N_max)

    # d^2 P_acc/dmu^2 via finite differences (h=0.01)
    h = 0.01
    P_plus = P_acc(1.0 + h, c, N_max)
    P_minus = P_acc(1.0 - h, c, N_max)
    d2P = (P_plus - 2 * P_acc_mu1 + P_minus) / h ** 2

    # Delta_S_star and derivatives
    Delta_S_star = -log(P_acc_mu1)
    dDS_dmu = -dP_via_stein / P_acc_mu1
    d2DS_dmu2 = -(d2P * P_acc_mu1 - dP_via_stein ** 2) / P_acc_mu1 ** 2

    # Taylor location of mu*
    mu_star = 1.0 - dDS_dmu / d2DS_dmu2

    # O(eps^2) correction bound (document: |d^3 Delta_S*/dmu^3| <= 5)
    correction_bound = (abs(mu_star - 1) ** 2) / 2 * 5.0

    if verbose:
        print(f"  Truncation error: {trunc_err:.2e}")
        print()
        print("  Probabilities (canonical):")
        print(f"    P(S = 1)          = {P_S_eq_1:.10f}   (doc: 0.18371114)")
        print(f"    P(-7 <= S <= 0)   = {P_neg7_to_0:.10f}   (doc: 0.34424489)")
        print(f"    P(S = -8)         = {P_S_eq_m8:.10f}   (doc: 0.00881220)")
        print(f"    P(2 <= S <= 16)   = {P_2_to_16:.10f}   (doc: 0.28505634)")
        print(f"    P_acc(mu=1)       = {P_acc_mu1:.10f}   (doc: 0.54843555)")
        print()
        print("  dP_acc/dmu at mu=1:")
        print(f"    via w(n) decomposition: {dP_via_w:+.10f}")
        print(f"    via Stein-Papangelou:   {dP_via_stein:+.10f}")
        print(f"    document reports:       -0.007664")
        print(f"  d^2 P_acc/dmu^2 (h={h}):    {d2P:.6f}   (doc: 0.40821)")
        print()
        print("  Delta_S_star and derivatives:")
        print(f"    Delta_S_star(mu=1)           = {Delta_S_star:.8f}  (doc: 0.60069)")
        print(f"    d Delta_S_star/dmu|_{{mu=1}}   = {dDS_dmu:+.8f}  (doc: +0.014034)")
        print(f"    d^2 Delta_S_star/dmu^2|_{{mu=1}} = {d2DS_dmu2:+.8f}  (doc: -0.744120)")
        print()
        print("  Taylor location of mu*:")
        print(f"    mu* = 1 - ({dDS_dmu:+.6f}) / ({d2DS_dmu2:+.6f})")
        print(f"        = {mu_star:.6f}   (doc: 1.01886)")
        print(f"    |mu* - 1| = {abs(mu_star - 1):.4f}")
        print(f"    certified interval: ({mu_star - correction_bound:.4f},"
              f" {mu_star + correction_bound:.4f})")
        print(f"    document's certified: (1.017, 1.021)")

    return {
        "c": c,
        "N_max": N_max,
        "truncation_error": trunc_err,
        "P_S_eq_1": P_S_eq_1,
        "P_neg7_to_0": P_neg7_to_0,
        "P_S_eq_m8": P_S_eq_m8,
        "P_2_to_16": P_2_to_16,
        "P_acc_mu1": P_acc_mu1,
        "Delta_S_star": Delta_S_star,
        "dP_acc_dmu_via_w": dP_via_w,
        "dP_acc_dmu_via_stein": dP_via_stein,
        "d2P_acc_dmu2": d2P,
        "dDS_dmu": dDS_dmu,
        "d2DS_dmu2": d2DS_dmu2,
        "mu_star": mu_star,
        "correction_bound": correction_bound,
    }


def mu_QCD(Delta_S_star):
    """
    mu_QCD = exp(sqrt(4 * Delta_S_star))

    Derived (not fitted) per RA session log April 11, 2026.
    Chain: d=4 -> BDG integers -> P_acc(1) -> Delta_S_star -> mu_QCD.
    Zero free parameters.
    """
    return exp(np.sqrt(4 * Delta_S_star))


def self_test_document_reproduction():
    """Verify reproduction of all six canonical document values."""
    results = compute_d4u02(verbose=False, tight_window=False)
    expected = {
        "P_S_eq_1": 0.18371114,
        "P_neg7_to_0": 0.34424489,
        "P_S_eq_m8": 0.00881220,
        "P_2_to_16": 0.28505634,
        "P_acc_mu1": 0.54843555,
    }
    passes = []
    for key, expected_val in expected.items():
        actual = results[key]
        err = abs(actual - expected_val)
        ok = err < 5e-9
        passes.append(ok)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {key}: {actual:.10f} vs {expected_val:.8f}   (err {err:.2e})")
    return all(passes)


def check_weight_function():
    """Reproduce the w(n) table from document section 4."""
    w = weight_function(BDG_D4)
    checks = [
        (-8, 1.0, "c_2=9 only"),
        (-7, 7/6, "c_2 + c_4/6"),
        (0, 7/6, "c_2 + c_4/6"),
        (1, -3/2, "c_1 + c_3/2"),
        (2, -1/2, "c_3 only"),
        (16, -1/2, "c_3 only"),
    ]
    passes = []
    for n, expected_w, note in checks:
        actual_w = w.get(n, 0.0)
        ok = abs(actual_w - expected_w) < 1e-15
        passes.append(ok)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] n={n:>3}: w={actual_w:+.6f}   ({note})")

    outside = [w.get(n, 0.0) for n in [-9, -10, 17, 18]]
    ok = all(x == 0.0 for x in outside)
    passes.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] w = 0 outside support {{-8,...,16}}")
    return all(passes)


if __name__ == "__main__":
    # Primary: document reproduction
    print("PRIMARY COMPUTATION (document window [15, 8, 5, 3])")
    print()
    results = compute_d4u02(verbose=True, tight_window=False)

    print()
    print("=" * 70)
    print("Weight function w(n) verification (document section 4)")
    print("=" * 70)
    w_ok = check_weight_function()

    print()
    print("=" * 70)
    print("Document-value self-test")
    print("=" * 70)
    doc_ok = self_test_document_reproduction()
    print(f"\n  Overall: {'ALL PASS' if (doc_ok and w_ok) else 'FAILURES'}")

    print()
    print("=" * 70)
    print("CANONICAL CONSTANTS (tight enumeration window)")
    print("=" * 70)
    tight = compute_d4u02(verbose=False, tight_window=True)
    print(f"  Enumeration window: {tight['N_max']}")
    print(f"  Truncation error:   {tight['truncation_error']:.2e}")
    print(f"  P_acc(mu=1):        {tight['P_acc_mu1']:.12f}")
    print(f"  Delta_S_star:       {tight['Delta_S_star']:.12f}")
    print(f"  mu*:                {tight['mu_star']:.12f}")
    print()

    DS = tight['Delta_S_star']
    mu_QCD_val = mu_QCD(DS)
    print(f"  mu_QCD = exp(sqrt(4 * Delta_S_star))")
    print(f"         = exp({np.sqrt(4 * DS):.10f})")
    print(f"         = {mu_QCD_val:.10f}")
    print()
    print("Downstream RA scripts should import via:")
    print("    from d4u02_enumeration import compute_d4u02, mu_QCD")
    print("    results = compute_d4u02(verbose=False)")
    print("    DS = results['Delta_S_star']")
    print("    mu_QCD_val = mu_QCD(DS)")
