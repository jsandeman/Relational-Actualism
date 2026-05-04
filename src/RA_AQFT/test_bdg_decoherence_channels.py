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


def test_d_uniform_recovers_flat_suppression() -> None:
    print("\n[2] D_uniform variant matches the flat Dict-D 2.5x suppression")
    v_uniform = next(v for v in VARIANTS if v.name == "D_uniform")
    for s in SCENARIOS:
        pred = predict_variant(s, v_uniform)
        # under uniform variant, suppression should be ~ 1/0.4 = 2.47
        check(f"  {s.name}: suppression in [2.4, 2.6]",
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


def test_d_uniform_falsified_by_mature_data() -> None:
    print("\n[4] D_uniform falsified by ALL mature scenarios")
    v_uniform = next(v for v in VARIANTS if v.name == "D_uniform")
    n_mature_in_tension = 0
    n_mature = 0
    for s in SCENARIOS:
        if s.field_maturity != "mature":
            continue
        n_mature += 1
        pred = predict_variant(s, v_uniform)
        if pred.in_tension:
            n_mature_in_tension += 1
    check("  every mature scenario in tension under D_uniform",
          n_mature_in_tension == n_mature,
          f"{n_mature_in_tension} of {n_mature} mature scenarios")


def test_atom_IF_escapes_under_gas_only_variant() -> None:
    print("\n[5] D_gas_only escapes Cs atom IF tension (gas weight is small there)")
    s_atom = next(s for s in SCENARIOS if s.name == "atom_IF_Cs_fountain")
    v_gas = next(v for v in VARIANTS if v.name == "D_gas_only")
    pred = predict_variant(s_atom, v_gas)
    check("  Cs atom IF: not in tension under D_gas_only",
          not pred.in_tension,
          f"suppression = {pred.suppression_total:.3f}, "
          f"meas±{s_atom.measurement_precision_factor:.0%}")


def test_molecular_IF_remains_in_tension_under_restricted_variants() -> None:
    print("\n[6] Molecular IF (Arndt-style) stays in tension under restricted variants")
    s_mol = next(s for s in SCENARIOS if s.name == "mol_IF_C60")
    for v in VARIANTS:
        if v.name == "D_uniform":
            continue  # trivially in tension
        pred = predict_variant(s_mol, v)
        check(f"  C60 IF in tension under {v.name}",
              pred.in_tension,
              f"suppression = {pred.suppression_total:.3f}")


def test_speculative_scenarios_never_in_tension() -> None:
    print("\n[7] Speculative scenarios (BMV, Carney) never in tension (no data)")
    for s in SCENARIOS:
        if s.field_maturity != "speculative":
            continue
        for v in VARIANTS:
            pred = predict_variant(s, v)
            check(f"  {s.name} not in tension under {v.name}",
                  not pred.in_tension,
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
        test_d_uniform_recovers_flat_suppression,
        test_unfiltered_channels_pass_through,
        test_d_uniform_falsified_by_mature_data,
        test_atom_IF_escapes_under_gas_only_variant,
        test_molecular_IF_remains_in_tension_under_restricted_variants,
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
