"""
test_bdg_actualization.py
Sanity tests for the Tier 3b BDG-kernel actualization rate calculator.

Run from src/RA_AQFT:  python test_bdg_actualization.py
"""

from __future__ import annotations

import sys

import numpy as np

from bdg_actualization import (
    C_BDG,
    actualization_rate,
    bdg_acceptance_probability,
    bridge_interpretation_rate,
    critical_mu_for_branch_coherent,
    kernel_regime,
)


_FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        _FAILS.append(name)


def test_bdg_coefficients_match_lean() -> None:
    print("\n[1] BDG coefficients match the Lean source of truth")
    # RA_BDG_Coefficient_Arithmetic.lean: c0..c4 = (1, -1, 9, -16, 8)
    check("  C_BDG == (1, -1, 9, -16, 8)", C_BDG == (1, -1, 9, -16, 8),
          f"got {C_BDG}")


def test_acceptance_probability_at_zero_mu() -> None:
    print("\n[2] At mu=0 the kernel has P_acc = 1 (S = c0 = 1 > 0 trivially)")
    p = bdg_acceptance_probability(0.0, n_samples=10_000)
    check("  P_acc(0) == 1", abs(p - 1.0) < 1e-10, f"P_acc={p:.6f}")


def test_acceptance_saturates_at_large_mu() -> None:
    print("\n[3] P_acc(mu) → 1 in the saturation limit (kernel saturation theorem)")
    p = bdg_acceptance_probability(50.0, n_samples=50_000)
    check("  P_acc(50) > 0.99", p > 0.99, f"P_acc={p:.4f}")


def test_acceptance_below_one_in_selective_regime() -> None:
    print("\n[4] In the selective regime, P_acc < 1")
    p = bdg_acceptance_probability(2.0, n_samples=200_000)
    check("  0.1 < P_acc(2) < 0.9", 0.1 < p < 0.9, f"P_acc={p:.4f}")


def test_regime_classification() -> None:
    print("\n[5] Regime classifier returns expected labels at canonical mu values")
    # P_acc is non-monotone in mu: it dips through a selective minimum near
    # mu ~ 3-5 (P_acc ~ 0.4) and then saturates to 1.0 above mu ~ 8.
    # Both mu << 1 and mu >> 5 give P_acc → 1.
    rng = np.random.default_rng(42)
    cases = [
        (50.0, "saturated"),         # P_acc ~ 1.0
        (10.0, "saturated"),         # P_acc ~ 1.0 (just above the climb)
        (4.0,  "strongly_selective"),# P_acc ~ 0.40 (in the selective trough)
        (5.0,  "strongly_selective"),# P_acc ~ 0.43 (still in the trough)
        (0.3,  "gentle"),            # P_acc ~ 0.75 (small-mu near-trivial)
    ]
    for mu, expected in cases:
        p = bdg_acceptance_probability(mu, n_samples=50_000, rng=rng)
        actual = kernel_regime(mu, p_acc=p)
        check(f"  mu={mu}: expect {expected}, got {actual}",
              actual == expected, f"P_acc={p:.4f}")


def test_actualization_rate_matches_bridge_in_saturation() -> None:
    print("\n[6] actualization_rate matches bridge in saturated regime")
    gamma_cand = 1000.0
    r = actualization_rate(gamma_cand, mu=50.0, n_samples=50_000)
    bridge = bridge_interpretation_rate(gamma_cand)
    rel_err = abs(r.lambda_pos_per_s - bridge) / bridge
    check("  |lambda_pos - Gamma_cand| / Gamma_cand < 1%", rel_err < 0.01,
          f"rel_err={rel_err:.4f}")


def test_actualization_rate_suppressed_in_selective_regime() -> None:
    print("\n[7] actualization_rate < bridge at the selective minimum (mu ~ 3-4)")
    gamma_cand = 1000.0
    r = actualization_rate(gamma_cand, mu=3.0, n_samples=200_000)
    bridge = bridge_interpretation_rate(gamma_cand)
    suppression = bridge / r.lambda_pos_per_s
    check("  bridge over-predicts by > 2x at mu=3", suppression > 2.0,
          f"suppression={suppression:.2f}x")


def test_bridge_recovery_when_gamma_cand_below_esd() -> None:
    print("\n[8] If Gamma_cand <= gamma_ESD, branch-coherent regime is automatic")
    result = critical_mu_for_branch_coherent(
        gamma_cand_per_s=0.01, gamma_esd_per_s=0.06)
    check("  mu_critical = +inf", result["mu_critical"] == float("inf"))
    check("  branch_coherent_achievable == True",
          result["branch_coherent_achievable"])


def test_critical_mu_unachievable_for_BMV_nominal() -> None:
    print("\n[9] BMV nominal: BDG suppression alone cannot rescue branch-coherent regime")
    # Tier 3a values: Gamma_cand ~ 1.2e6 /s, gamma_ESD ~ 0.06 /s
    # P_acc would need to be ~5e-8 to bring lambda_pos below gamma_ESD,
    # but P_acc is bounded above 0 and in our tabulation never goes below ~0.1
    result = critical_mu_for_branch_coherent(
        gamma_cand_per_s=1.2e6,
        gamma_esd_per_s=0.06,
        n_samples=50_000,
    )
    check("  branch_coherent_achievable == False",
          not result["branch_coherent_achievable"],
          f"mu_critical={result['mu_critical']}, P_acc={result['p_acc_critical']:.3e}")


def test_acceptance_climbs_to_saturation_above_selective_min() -> None:
    print("\n[10] P_acc(mu) climbs to saturation above the selective minimum (mu >= 6)")
    # P_acc has a selective minimum near mu ~ 3-5, then climbs monotonically
    # to 1.0 in saturation. We test the monotonic-climb regime only.
    rng = np.random.default_rng(42)
    mus = [6.0, 8.0, 12.0, 20.0]
    ps = [bdg_acceptance_probability(m, n_samples=100_000, rng=rng) for m in mus]
    monotone = all(ps[i] <= ps[i + 1] + 0.01 for i in range(len(ps) - 1))
    check("  P_acc nondecreasing for mu >= 6", monotone,
          f"P_acc values = {[f'{p:.3f}' for p in ps]}")
    check("  P_acc(20) > 0.99 (saturation reached)", ps[-1] > 0.99,
          f"P_acc(20)={ps[-1]:.4f}")


def test_selective_minimum_exists() -> None:
    print("\n[10b] P_acc has a selective minimum near mu ~ 3-5 (non-monotonic)")
    # P_acc(small) and P_acc(large) both → 1, but P_acc(mu_min) ~ 0.4-0.5.
    rng = np.random.default_rng(42)
    p_small = bdg_acceptance_probability(0.3, n_samples=100_000, rng=rng)
    p_min   = bdg_acceptance_probability(4.0, n_samples=100_000, rng=rng)
    p_large = bdg_acceptance_probability(50.0, n_samples=100_000, rng=rng)
    check("  P_acc(4) < P_acc(0.3)", p_min < p_small,
          f"P_acc(0.3)={p_small:.3f}, P_acc(4)={p_min:.3f}")
    check("  P_acc(4) < P_acc(50)", p_min < p_large,
          f"P_acc(4)={p_min:.3f}, P_acc(50)={p_large:.3f}")
    check("  P_acc(4) < 0.55 (selective minimum)", p_min < 0.55,
          f"P_acc(4)={p_min:.3f}")


def main() -> int:
    print("=" * 78)
    print("BDG actualization (Tier 3b) — test suite")
    print("=" * 78)
    for fn in [
        test_bdg_coefficients_match_lean,
        test_acceptance_probability_at_zero_mu,
        test_acceptance_saturates_at_large_mu,
        test_acceptance_below_one_in_selective_regime,
        test_regime_classification,
        test_actualization_rate_matches_bridge_in_saturation,
        test_actualization_rate_suppressed_in_selective_regime,
        test_bridge_recovery_when_gamma_cand_below_esd,
        test_critical_mu_unachievable_for_BMV_nominal,
        test_acceptance_climbs_to_saturation_above_selective_min,
        test_selective_minimum_exists,
    ]:
        fn()
    print("\n" + "=" * 78)
    if _FAILS:
        print(f"FAILED ({len(_FAILS)}): " + ", ".join(_FAILS))
        return 1
    print("ALL TESTS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
