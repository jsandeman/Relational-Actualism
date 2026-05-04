"""
test_bdg_decoherence_channels.py
Sanity tests for the v2 channel-resolved BDG suppression analysis.

Run from src/RA_AQFT:  python test_bdg_decoherence_channels.py
"""

from __future__ import annotations

import sys

from bdg_decoherence_channels import (
    ALL_CHANNELS,
    ACTUALIZATION_CHANNELS,
    GAS,
    BB_SELF,
    TRAP_PHOTON_RECOIL,
    OTHER_UNATTRIBUTED,
    PER_CHANNEL_PRECISION_BOUNDS,
    SCENARIOS,
    VARIANTS,
    DictDVariant,
    ScenarioChannels,
    per_channel_constraints,
    predict_variant,
    variant_per_channel_falsification,
)


_FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        _FAILS.append(name)


def test_v2_schema_split_scenarios_present() -> None:
    print("\n[1] v2 scenario splits are present (12+ scenarios)")
    expected_substrings = [
        "atom_IF_Cs_fountain_freefall",
        "atom_IF_Cs_lattice",
        "mol_IF_C60_nominal",
        "mol_IF_C60_collisional_engineered",
        "mol_IF_C60_blackbody_engineered",
        "opto_levitated_silica_cavityCS",
        "opto_levitated_silica_cryo_freespace",
        "opto_levitated_diamond_NV_spin_only",
        "opto_levitated_diamond_NV_CoM_proposal",
    ]
    actual = {s.name for s in SCENARIOS}
    for sub in expected_substrings:
        check(f"  catalog has {sub}", sub in actual)
    check("  catalog has at least 12 scenarios", len(SCENARIOS) >= 12,
          f"got {len(SCENARIOS)}")


def test_per_channel_constraints_falsify_dict_D() -> None:
    print("\n[2] CORE FINDING: per-channel constraints falsify Dict-D at >3σ")
    constraints = per_channel_constraints()
    expected_channels = {GAS.name, BB_SELF.name, TRAP_PHOTON_RECOIL.name}
    actual_channels = {c.channel for c in constraints}
    check("  per-channel constraints cover gas, BB_self, trap_photon_recoil",
          actual_channels == expected_channels,
          f"got {actual_channels}")
    for c in constraints:
        check(f"  {c.channel}: σ-falsify > 3.0",
              c.sigma_falsification > 3.0,
              f"got {c.sigma_falsification:.1f}σ")


def test_all_dict_D_variants_falsified() -> None:
    print("\n[3] All 4 Dict-D variants are falsified by per-channel constraints")
    constraints = per_channel_constraints()
    for v in VARIANTS:
        falsified_by = variant_per_channel_falsification(v, constraints)
        max_sigma = max(falsified_by.values()) if falsified_by else 0.0
        check(f"  {v.name}: falsified at >3σ", max_sigma > 3.0,
              f"max σ = {max_sigma:.1f}")


def test_d_uniform_falsified_by_three_channels() -> None:
    print("\n[4] D_uniform falsified by all 3 per-channel constraints")
    v_uniform = next(v for v in VARIANTS if v.name == "D_uniform")
    constraints = per_channel_constraints()
    falsified = variant_per_channel_falsification(v_uniform, constraints)
    check("  D_uniform touches all 3 constrained channels",
          len(falsified) == 3, f"got {len(falsified)}")


def test_d_gas_only_falsified_by_gas_alone() -> None:
    print("\n[5] D_gas_only falsified by Hornberger 2003 alone")
    v_gas = next(v for v in VARIANTS if v.name == "D_gas_only")
    constraints = per_channel_constraints()
    falsified = variant_per_channel_falsification(v_gas, constraints)
    check("  D_gas_only touches exactly gas", set(falsified.keys()) == {GAS.name})
    check("  σ > 5", list(falsified.values())[0] > 5.0,
          f"σ = {list(falsified.values())[0]:.1f}")


def test_schema_incompatible_scenarios_skipped() -> None:
    print("\n[6] Schema-incompatible scenarios are flagged (not used in cumulative)")
    n_invalid = sum(1 for s in SCENARIOS if not s.channel_additivity_valid)
    n_valid = sum(1 for s in SCENARIOS if s.channel_additivity_valid)
    check("  most scenarios are schema-incompatible (per v2)",
          n_invalid > n_valid,
          f"{n_invalid} invalid, {n_valid} valid")
    # specifically: atom_IF_Cs_fountain_freefall is ensemble-phase-variance,
    # which is NOT Lindblad
    s_fountain = next(s for s in SCENARIOS
                      if s.name == "atom_IF_Cs_fountain_freefall")
    check("  fountain marked schema-incompatible (ensemble phase variance)",
          not s_fountain.channel_additivity_valid)
    # mol_IF_C60_nominal is instrumental-dominated, schema-incompatible
    s_nominal = next(s for s in SCENARIOS if s.name == "mol_IF_C60_nominal")
    check("  C60 nominal marked schema-incompatible (instrumental dominant)",
          not s_nominal.channel_additivity_valid)


def test_engineered_scenarios_are_additivity_valid() -> None:
    print("\n[7] Engineered-condition scenarios are additivity-valid")
    for name in ["mol_IF_C60_collisional_engineered",
                 "mol_IF_C60_blackbody_engineered",
                 "opto_levitated_silica_cavityCS",
                 "opto_levitated_silica_cryo_freespace"]:
        s = next(s for s in SCENARIOS if s.name == name)
        check(f"  {name} is additivity-valid", s.channel_additivity_valid)


def test_predict_variant_skips_invalid_for_in_tension() -> None:
    print("\n[8] predict_variant: in_tension is False for additivity-invalid")
    s_invalid = next(s for s in SCENARIOS
                     if s.name == "mol_IF_C60_nominal")  # invalid
    v_uniform = next(v for v in VARIANTS if v.name == "D_uniform")
    pred = predict_variant(s_invalid, v_uniform)
    check("  additivity_skipped == True", pred.additivity_skipped)
    check("  in_tension == False (cannot constrain)", not pred.in_tension)


def test_engineered_C60_collisional_in_tension_under_gas_filter() -> None:
    print("\n[9] Hornberger-2003 engineered C60 in tension with D_gas_only "
          "(this is the per-channel constraint, in cumulative form)")
    s = next(s for s in SCENARIOS
             if s.name == "mol_IF_C60_collisional_engineered")
    v = next(v for v in VARIANTS if v.name == "D_gas_only")
    pred = predict_variant(s, v)
    check("  in_tension == True", pred.in_tension,
          f"suppression = {pred.suppression_total:.3f}, "
          f"meas±{s.measurement_precision_factor:.0%}")


def test_speculative_never_in_tension() -> None:
    print("\n[10] Speculative scenarios never in tension (no measurement)")
    for s in SCENARIOS:
        if s.field_maturity != "speculative":
            continue
        for v in VARIANTS:
            pred = predict_variant(s, v)
            check(f"  {s.name} not in tension under {v.name}",
                  not pred.in_tension)


def test_per_channel_bound_dictionary() -> None:
    print("\n[11] PER_CHANNEL_PRECISION_BOUNDS has the three expected channels")
    expected = {GAS.name, BB_SELF.name, TRAP_PHOTON_RECOIL.name}
    actual = set(PER_CHANNEL_PRECISION_BOUNDS.keys())
    check("  bounds dict has exactly the 3 measured channels",
          actual == expected, f"got {actual}")
    for ch_name, (bound, citation) in PER_CHANNEL_PRECISION_BOUNDS.items():
        check(f"  {ch_name}: bound is reasonable (5-30%)",
              0.05 <= bound <= 0.30, f"bound = {bound}")
        check(f"  {ch_name}: citation is non-empty",
              len(citation) > 0)


def main() -> int:
    print("=" * 78)
    print("Channel-resolved BDG suppression v2 — test suite")
    print("=" * 78)
    for fn in [
        test_v2_schema_split_scenarios_present,
        test_per_channel_constraints_falsify_dict_D,
        test_all_dict_D_variants_falsified,
        test_d_uniform_falsified_by_three_channels,
        test_d_gas_only_falsified_by_gas_alone,
        test_schema_incompatible_scenarios_skipped,
        test_engineered_scenarios_are_additivity_valid,
        test_predict_variant_skips_invalid_for_in_tension,
        test_engineered_C60_collisional_in_tension_under_gas_filter,
        test_speculative_never_in_tension,
        test_per_channel_bound_dictionary,
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
