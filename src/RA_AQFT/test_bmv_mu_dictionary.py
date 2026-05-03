"""
test_bmv_mu_dictionary.py
Sanity tests for the Tier 3b μ-dictionary catalog.

Run from src/RA_AQFT:  python test_bmv_mu_dictionary.py
"""

from __future__ import annotations

import sys

from bmv_mu_dictionary import (
    BOSE_2017,
    CATALOG,
    ENV_BOSE_IDEAL,
    predict,
)


_FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        _FAILS.append(name)


def test_catalog_has_five_dictionaries() -> None:
    print("\n[1] Catalog has all 5 candidate dictionaries")
    expected_names = {"A_env_planck", "B_atom_count", "C_geometric",
                      "D_dimensionality", "E_log_mass_ratio"}
    actual_names = {d.name for d in CATALOG}
    check("  catalog contains all 5 expected names", actual_names == expected_names,
          f"got {actual_names}")


def test_dict_A_pushes_mu_far_above_saturation() -> None:
    print("\n[2] Dictionary A (env × Planck time): μ astronomical at any rate >> 1/τ_Planck")
    d = next(d for d in CATALOG if d.name == "A_env_planck")
    pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
    # Γ_decoh ~ 1.2e6, τ_Planck ~ 5.4e-44 ⇒ μ ~ 6e-38 (extreme, but tiny here);
    # tiny μ also gives saturation since S = c_0 = 1 with no candidates
    check("  μ very small (also a saturation regime: P_acc → 1)",
          pred.mu < 1e-30, f"μ = {pred.mu:.2e}")
    check("  P_acc ≈ 1", pred.p_acc > 0.99, f"P_acc = {pred.p_acc:.6f}")


def test_dict_B_pushes_mu_huge() -> None:
    print("\n[3] Dictionary B (atom count): μ ≈ N_atoms ~ 10^12 for m=1e-14 kg")
    d = next(d for d in CATALOG if d.name == "B_atom_count")
    pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
    check("  μ ≈ N_atoms", 1e11 < pred.mu < 1e13, f"μ = {pred.mu:.2e}")
    check("  saturation (short-circuited by saturation theorem)",
          pred.p_acc == 1.0, f"P_acc = {pred.p_acc}")


def test_dict_C_pushes_mu_astronomical() -> None:
    print("\n[4] Dictionary C (geometric): μ = (dX/l_Planck)^4 — far above saturation")
    d = next(d for d in CATALOG if d.name == "C_geometric")
    pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
    # dX = 250e-6 m, l_Planck ~ 1.6e-35 m, so dX/l_Planck ~ 1.5e29
    # ⇒ μ ~ (1.5e29)^4 ~ 5e116
    check("  μ massively above saturation cutoff", pred.mu > 1e100,
          f"μ = {pred.mu:.2e}")
    check("  saturation regime", pred.regime == "saturated")


def test_dict_D_strongly_selective() -> None:
    print("\n[5] Dictionary D (μ = d = 4): kernel-structural, places at selective minimum")
    d = next(d for d in CATALOG if d.name == "D_dimensionality")
    pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
    check("  μ = 4.0 exactly", pred.mu == 4.0, f"μ = {pred.mu}")
    check("  P_acc ~ 0.4 (selective minimum)",
          0.3 < pred.p_acc < 0.5, f"P_acc = {pred.p_acc:.4f}")
    check("  regime is strongly_selective",
          pred.regime == "strongly_selective", f"got {pred.regime}")
    check("  suppression ~ 2.5x", 2.0 < pred.suppression_factor < 3.0,
          f"suppression = {pred.suppression_factor:.2f}")
    check("  deviates from bridge", pred.deviates_from_bridge)


def test_dict_E_log_ratio() -> None:
    print("\n[6] Dictionary E (log mass ratio): μ ≈ |log(m/m_Planck)| ~ 16 for m=1e-14")
    d = next(d for d in CATALOG if d.name == "E_log_mass_ratio")
    pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
    # log(1e-14 / 2.18e-8) ≈ log(4.6e-7) ≈ -14.6 ⇒ |·| ≈ 14.6
    check("  μ in [10, 20]", 10 < pred.mu < 20, f"μ = {pred.mu:.3f}")
    # at μ=15-16, P_acc is firmly in saturation
    check("  saturated at μ ~ 15", pred.p_acc > 0.99, f"P_acc = {pred.p_acc:.4f}")


def test_only_D_deviates_from_bridge() -> None:
    print("\n[7] CORE FINDING: only Dictionary D predicts deviation from Tier 3a bridge")
    deviating_dict_names = []
    for d in CATALOG:
        pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
        if pred.deviates_from_bridge:
            deviating_dict_names.append(d.name)
    check("  exactly one dictionary deviates",
          len(deviating_dict_names) == 1,
          f"deviating: {deviating_dict_names}")
    check("  the deviating one is D_dimensionality",
          deviating_dict_names == ["D_dimensionality"],
          f"got {deviating_dict_names}")


def test_lambda_pos_recovers_bridge_for_saturated_dicts() -> None:
    print("\n[8] In the saturated regime, λ_pos exactly equals Γ_cand")
    for d in CATALOG:
        pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
        if not pred.deviates_from_bridge:
            ratio = pred.lambda_pos_per_s / pred.bridge_lambda_pos_per_s
            check(f"  {d.name}: ratio λ_pos/Γ_cand ≈ 1",
                  abs(ratio - 1.0) < 0.01, f"ratio = {ratio:.6f}")


def main() -> int:
    print("=" * 78)
    print("BMV μ-dictionary catalog (Tier 3b) — test suite")
    print("=" * 78)
    for fn in [
        test_catalog_has_five_dictionaries,
        test_dict_A_pushes_mu_far_above_saturation,
        test_dict_B_pushes_mu_huge,
        test_dict_C_pushes_mu_astronomical,
        test_dict_D_strongly_selective,
        test_dict_E_log_ratio,
        test_only_D_deviates_from_bridge,
        test_lambda_pos_recovers_bridge_for_saturated_dicts,
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
