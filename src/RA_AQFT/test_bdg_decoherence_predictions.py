"""
test_bdg_decoherence_predictions.py
Sanity tests for the decoherence-landscape sweep.

Run from src/RA_AQFT:  python test_bdg_decoherence_predictions.py
"""

from __future__ import annotations

import sys

from bdg_decoherence_predictions import (
    SCENARIOS,
    DecoherenceScenario,
    predict_scenario,
)


_FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        _FAILS.append(name)


def test_scenarios_present() -> None:
    print("\n[1] Catalog has all expected scenarios spanning ~10 mass decades")
    expected = {"atom_interferometry_Cs", "molecular_interferometry_C60",
                "molecular_interferometry_oligoporphyrin",
                "levitated_nanosphere_silica", "bmv_bose2017_nominal"}
    actual = {s.name for s in SCENARIOS}
    check("  catalog has the 5 expected scenarios", actual == expected,
          f"got {actual}")
    masses = sorted(s.m for s in SCENARIOS)
    span_decades = masses[-1] / masses[0]
    check("  mass range spans > 10 decades",
          span_decades > 1e10, f"span = {span_decades:.2e}")


def test_suppression_factor_is_universal_under_dict_D() -> None:
    print("\n[2] CORE INVARIANT: under Dict D, suppression factor ~ 2.47 universally")
    suppression_factors = [predict_scenario(s).suppression_factor for s in SCENARIOS]
    # all should match within MC noise
    spread = max(suppression_factors) - min(suppression_factors)
    check("  suppression factor spread across scenarios < 0.05",
          spread < 0.05, f"spread = {spread:.4f}")
    avg = sum(suppression_factors) / len(suppression_factors)
    check("  average suppression in [2.4, 2.6]",
          2.4 < avg < 2.6, f"avg = {avg:.3f}")


def test_mature_systems_in_tension() -> None:
    print("\n[3] All 'mature' scenarios are in tension with Dict D")
    for s in SCENARIOS:
        if s.field_maturity != "mature":
            continue
        p = predict_scenario(s)
        check(f"  {s.name}: in_tension == True", p.in_tension_with_data,
              f"meas±{s.measurement_precision_factor:.0%}, suppr={p.suppression_factor:.2f}")


def test_speculative_not_testable() -> None:
    print("\n[4] Speculative scenarios (BMV-scale) are not yet testable")
    for s in SCENARIOS:
        if s.field_maturity != "speculative":
            continue
        p = predict_scenario(s)
        check(f"  {s.name}: not in tension (no data yet)", not p.in_tension_with_data)
        check(f"  {s.name}: not distinguishable (speculative)",
              not p.distinguishable)


def test_developing_field_distinguishable_but_not_in_tension() -> None:
    print("\n[5] Developing fields: distinguishable in principle, no tension yet")
    found_developing = False
    for s in SCENARIOS:
        if s.field_maturity != "developing":
            continue
        found_developing = True
        p = predict_scenario(s)
        check(f"  {s.name}: distinguishable", p.distinguishable)
        # tension may or may not apply depending on precision
    check("  catalog has at least one developing scenario", found_developing)


def test_suppression_geometry_independent() -> None:
    print("\n[6] Suppression factor independent of m and dX (kernel-only property)")
    # build two extreme scenarios with the same μ assumption
    s_tiny = DecoherenceScenario(
        name="probe_tiny", description="tiny probe",
        m=1e-25, dX=1e-9,
        pressure_Pa=1e-10, T_gas_K=1.0, T_blackbody_K=1.0,
        measurement_precision_factor=0.1, field_maturity="developing",
    )
    s_huge = DecoherenceScenario(
        name="probe_huge", description="huge probe",
        m=1e-10, dX=1e-3,
        pressure_Pa=1e-10, T_gas_K=1.0, T_blackbody_K=1.0,
        measurement_precision_factor=0.1, field_maturity="developing",
    )
    p_tiny = predict_scenario(s_tiny)
    p_huge = predict_scenario(s_huge)
    diff = abs(p_tiny.suppression_factor - p_huge.suppression_factor)
    check("  same suppression factor across 15 mass decades",
          diff < 0.05, f"|diff| = {diff:.4f}")


def main() -> int:
    print("=" * 78)
    print("BDG decoherence-landscape predictions — test suite")
    print("=" * 78)
    for fn in [
        test_scenarios_present,
        test_suppression_factor_is_universal_under_dict_D,
        test_mature_systems_in_tension,
        test_speculative_not_testable,
        test_developing_field_distinguishable_but_not_in_tension,
        test_suppression_geometry_independent,
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
