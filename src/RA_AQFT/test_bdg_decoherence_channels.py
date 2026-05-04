"""
test_bdg_decoherence_channels.py
Sanity tests for the channel-resolved BDG suppression analysis.

Run from src/RA_AQFT:  python test_bdg_decoherence_channels.py
"""

from __future__ import annotations

import sys

from bdg_decoherence_channels import (
    ALL_CHANNELS,
    GAS,
    SCENARIOS,
    VARIANTS,
    DictDVariant,
    PHOTON_RECOIL,
    ScenarioChannels,
    predict_variant,
)


_FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        _FAILS.append(name)


def test_channel_weights_normalized() -> None:
    print("\n[1] Channel weights sum to ~1 for each scenario")
    for s in SCENARIOS:
        total = sum(s.channel_weights.values())
        check(f"  {s.name}: sum = {total:.3f}", abs(total - 1.0) < 0.01,
              f"sum = {total:.4f}")


def test_d_uniform_suppression_depends_on_other_unattributed_weight() -> None:
    print("\n[2] D_uniform suppression depends on other_unattributed weight")
    # POST-LIT-REVIEW: D_uniform applies to the 5 actualization-candidate
    # channels but NOT to other_unattributed (detection / measurement
    # noise). So suppression = 1 / (1 - (1 - w_other) * (1 - P_acc)),
    # which equals the flat 2.47x only when w_other = 0.
    v_uniform = next(v for v in VARIANTS if v.name == "D_uniform")
    for s in SCENARIOS:
        pred = predict_variant(s, v_uniform)
        # all suppressions should be > 1 (filter must do something)
        check(f"  {s.name}: suppression > 1", pred.suppression_total > 1.0,
              f"= {pred.suppression_total:.3f}")
        # scenarios with no other_unattributed should give exactly 2.47
        from bdg_decoherence_channels import OTHER_UNATTRIBUTED
        if s.channel_weights.get(OTHER_UNATTRIBUTED.name, 0) == 0:
            check(f"  {s.name}: matches flat 2.47x (no other_unattributed)",
                  2.4 < pred.suppression_total < 2.6,
                  f"= {pred.suppression_total:.3f}")


def test_unfiltered_channels_pass_through() -> None:
    print("\n[3] When filter applies to no channels, suppression == 1")
    v_empty = DictDVariant(name="D_none", description="empty filter mask",
                           applies_to=set())
    for s in SCENARIOS:
        pred = predict_variant(s, v_empty)
        check(f"  {s.name}: suppression == 1.0", abs(pred.suppression_total - 1.0) < 1e-9,
              f"= {pred.suppression_total:.6f}")


def test_d_uniform_falsified_by_mature_measured_data() -> None:
    print("\n[4] D_uniform falsified by ALL mature + measured scenarios")
    v_uniform = next(v for v in VARIANTS if v.name == "D_uniform")
    n_mature_measured_in_tension = 0
    n_mature_measured = 0
    for s in SCENARIOS:
        if s.field_maturity != "mature" or s.confidence != "measured":
            continue
        n_mature_measured += 1
        pred = predict_variant(s, v_uniform)
        if pred.in_tension:
            n_mature_measured_in_tension += 1
    check("  every mature+measured scenario in tension under D_uniform",
          n_mature_measured_in_tension == n_mature_measured,
          f"{n_mature_measured_in_tension} of {n_mature_measured} mature+measured")
    check("  at least 2 mature+measured scenarios exist (Cs IF + C60)",
          n_mature_measured >= 2,
          f"got {n_mature_measured}")


def test_atom_IF_escapes_under_gas_only_variant() -> None:
    print("\n[5] D_gas_only escapes Cs atom IF tension (gas weight is small there)")
    s_atom = next(s for s in SCENARIOS if s.name == "atom_IF_Cs_fountain")
    v_gas = next(v for v in VARIANTS if v.name == "D_gas_only")
    pred = predict_variant(s_atom, v_gas)
    check("  Cs atom IF: not in tension under D_gas_only",
          not pred.in_tension,
          f"suppression = {pred.suppression_total:.3f}, "
          f"meas±{s_atom.measurement_precision_factor:.0%}")


def test_C60_nominal_escapes_restricted_variants_post_lit_review() -> None:
    print("\n[6] POST-LIT-REVIEW: C60 (nominal) ESCAPES restricted Dict-D variants")
    # Lit review found that gas+BB at nominal C60 conditions are only
    # ~15% of the channel budget (Hornberger 2003 / Hackermüller 2004
    # measurements engineered specific channels to dominate).
    # Restricted variants therefore largely escape C60 nominal in tension.
    s_mol = next(s for s in SCENARIOS if s.name == "mol_IF_C60")
    for v in VARIANTS:
        if v.name == "D_uniform":
            continue  # still in tension (touches all 5 channels)
        pred = predict_variant(s_mol, v)
        check(f"  C60 nominal: NOT in tension under {v.name}",
              not pred.in_tension,
              f"suppression = {pred.suppression_total:.3f}, "
              f"meas±{s_mol.measurement_precision_factor:.0%}")


def test_oligoporphyrin_extrapolation_constrains_some_variants() -> None:
    print("\n[6b] Oligoporphyrin extrapolation constrains gas-touching variants")
    s_olig = next(s for s in SCENARIOS if s.name == "mol_IF_oligoporphyrin")
    check("  oligoporphyrin confidence is theoretical_extrapolation",
          s_olig.confidence == "theoretical_extrapolation",
          f"got {s_olig.confidence}")
    # under D_multi_vertex_only with extrapolated weights gas+BB ~ 0.75,
    # suppression should be substantial
    v_multi = next(v for v in VARIANTS if v.name == "D_multi_vertex_only")
    pred = predict_variant(s_olig, v_multi)
    check("  D_multi_vertex_only: constrained_by_extrapolation == True",
          pred.constrained_by_extrapolation,
          f"suppression = {pred.suppression_total:.3f}")
    # but in_tension should be False (extrapolation, not measured)
    check("  D_multi_vertex_only: in_tension == False (extrapolation, not measured)",
          not pred.in_tension)


def test_speculative_scenarios_never_in_tension() -> None:
    print("\n[7] Speculative scenarios never in tension (no data)")
    # Post-lit-review: diamond_NV, BMV, Carney are all speculative.
    for s in SCENARIOS:
        if s.field_maturity != "speculative":
            continue
        for v in VARIANTS:
            pred = predict_variant(s, v)
            check(f"  {s.name} not in tension under {v.name}",
                  not pred.in_tension and not pred.constrained_by_extrapolation,
                  f"suppression = {pred.suppression_total:.3f}")


def test_channel_decomposition_internally_consistent() -> None:
    print("\n[8] Suppression formula: 1 - w_filtered * (1 - P_acc)")
    # at p_acc = 0.4 and gas-only filter on a scenario with gas weight 0.5,
    # ratio = 1 - 0.5 * (1 - 0.4) = 0.7, suppression = 1/0.7 ≈ 1.429
    s_synthetic = ScenarioChannels(
        name="synthetic_test", description="for testing",
        field_maturity="developing", measurement_precision_factor=0.1,
        channel_weights={
            GAS.name: 0.5,
            PHOTON_RECOIL.name: 0.5,
        },
    )
    v_gas_only = DictDVariant(
        name="D_gas_test", description="gas-only test",
        applies_to={GAS.name}, mu=4.0,
    )
    pred = predict_variant(s_synthetic, v_gas_only)
    expected_min = 1.40  # for P_acc ≈ 0.4
    expected_max = 1.45
    check("  synthetic 50%-gas scenario gives suppression in [1.40, 1.45]",
          expected_min <= pred.suppression_total <= expected_max,
          f"got {pred.suppression_total:.4f}")


def main() -> int:
    print("=" * 78)
    print("Channel-resolved BDG suppression — test suite")
    print("=" * 78)
    for fn in [
        test_channel_weights_normalized,
        test_d_uniform_suppression_depends_on_other_unattributed_weight,
        test_unfiltered_channels_pass_through,
        test_d_uniform_falsified_by_mature_measured_data,
        test_atom_IF_escapes_under_gas_only_variant,
        test_C60_nominal_escapes_restricted_variants_post_lit_review,
        test_oligoporphyrin_extrapolation_constrains_some_variants,
        test_speculative_scenarios_never_in_tension,
        test_channel_decomposition_internally_consistent,
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
