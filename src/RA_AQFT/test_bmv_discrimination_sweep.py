"""
test_bmv_discrimination_sweep.py
Sanity tests for the Tier 4 discrimination-sweep module.

Run from src/RA_AQFT:  python test_bmv_discrimination_sweep.py
"""

from __future__ import annotations

import sys

import numpy as np

from bmv_comparator import BMVEnvironment, BMVParams
from bmv_discrimination_sweep import (
    BOSE_2017,
    CARNEY_NOMINAL,
    ENV_BOSE_IDEAL,
    ENV_FROZEN_LAB,
    discrimination_check,
    find_minimum_discriminating_mass,
    realistic_peak_concurrence,
    sweep_mass_time,
)


_FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        _FAILS.append(name)


def test_bose_2017_realistic_C_is_zero() -> None:
    print("\n[1] Bose 2017 nominal: realistic peak C = 0 (decoherence-limited)")
    v = discrimination_check(BOSE_2017, ENV_BOSE_IDEAL)
    check("  unitary C > 0.1", v.unitary_peak_C > 0.1,
          f"C_unitary={v.unitary_peak_C:.4f}")
    check("  realistic C exactly 0 (ESD wipeout)",
          v.realistic_peak_C == 0.0, f"C_real={v.realistic_peak_C:.2e}")
    check("  not discriminating", not v.discriminating)


def test_carney_unitary_signal_is_tiny() -> None:
    print("\n[2] Carney nominal (m=1e-19): unitary C is tiny (signal-limited)")
    c_u, c_r, gamma = realistic_peak_concurrence(CARNEY_NOMINAL, ENV_FROZEN_LAB)
    check("  unitary C < 1e-5 (gravitational signal too small)",
          c_u < 1e-5, f"C_unitary={c_u:.2e}")
    check("  realistic C also ~ 0", c_r < 1e-5, f"C_real={c_r:.2e}")


def test_no_decoherence_recovers_unitary() -> None:
    print("\n[3] Vanishing-environment limit recovers unitary concurrence")
    # an essentially-zero environment
    env_void = BMVEnvironment(pressure_Pa=1e-30, T_gas_K=1e-10, T_blackbody_K=1e-10)
    p = BMVParams(m=1e-15, dX=1e-6, d=2e-6, T=10.0)
    c_u, c_r, _ = realistic_peak_concurrence(p, env_void)
    rel_err = abs(c_u - c_r) / max(c_u, 1e-15)
    check("  realistic C ≈ unitary C in void limit", rel_err < 1e-6,
          f"C_u={c_u:.4e}, C_r={c_r:.4e}, rel_err={rel_err:.2e}")


def test_discriminating_region_at_appropriate_scale() -> None:
    print("\n[4] (dX=1um, d=2um) frozen-lab sweep has a discriminating region")
    m_array = np.logspace(-16, -13, 7)
    T_array = np.array([1.0, 10.0])
    sweep = sweep_mass_time(
        m_array, T_array, dX=1e-6, d=2e-6,
        env=ENV_FROZEN_LAB, c_floor=0.01, n_t=11,
    )
    n_disc = int(sweep["discriminating"].sum())
    check("  at least one (m, T) discriminates", n_disc > 0,
          f"discriminating points = {n_disc}")
    check("  m=1e-13 kg discriminates at T=10s",
          bool(sweep["discriminating"][-1, 1]),
          f"value = {sweep['discriminating'][-1, 1]}")


def test_frontier_finder() -> None:
    print("\n[5] find_minimum_discriminating_mass returns a sensible result")
    m_array = np.logspace(-18, -13, 11)
    T_array = np.array([1.0, 10.0, 100.0])
    sweep = sweep_mass_time(
        m_array, T_array, dX=10e-9, d=20e-9,
        env=ENV_FROZEN_LAB, c_floor=0.01, n_t=11,
    )
    front = find_minimum_discriminating_mass(sweep)
    check("  at least one grid point discriminates",
          front["discriminating_count"] > 0,
          f"count = {front['discriminating_count']}")
    if front["discriminating_count"] > 0:
        check("  m_min lies in the swept range",
              m_array[0] <= front["m_min"] <= m_array[-1],
              f"m_min={front['m_min']:.2e}")
    # negative case
    m_array_too_small = np.logspace(-30, -25, 5)  # gravitational signal vanishes
    T_array_short = np.array([0.1])
    sweep_dark = sweep_mass_time(
        m_array_too_small, T_array_short, dX=1e-6, d=2e-6,
        env=ENV_FROZEN_LAB, c_floor=0.01, n_t=5,
    )
    front_dark = find_minimum_discriminating_mass(sweep_dark)
    check("  no-discriminating sweep returns m_min = inf",
          front_dark["m_min"] == float("inf"),
          f"m_min = {front_dark['m_min']}")


def test_bose_environment_more_restrictive_than_frozen() -> None:
    print("\n[6] Bose-ideal env gives smaller discriminating region than frozen lab")
    m_array = np.logspace(-16, -13, 7)
    T_array = np.array([1.0, 10.0])
    s_bose = sweep_mass_time(m_array, T_array, dX=1e-6, d=2e-6,
                             env=ENV_BOSE_IDEAL, c_floor=0.01, n_t=11)
    s_frozen = sweep_mass_time(m_array, T_array, dX=1e-6, d=2e-6,
                               env=ENV_FROZEN_LAB, c_floor=0.01, n_t=11)
    n_bose = int(s_bose["discriminating"].sum())
    n_frozen = int(s_frozen["discriminating"].sum())
    check("  frozen-lab discriminating count >= bose-ideal count",
          n_frozen >= n_bose, f"frozen={n_frozen}, bose={n_bose}")


def main() -> int:
    print("=" * 78)
    print("BMV discrimination sweep (Tier 4) — test suite")
    print("=" * 78)
    for fn in [
        test_bose_2017_realistic_C_is_zero,
        test_carney_unitary_signal_is_tiny,
        test_no_decoherence_recovers_unitary,
        test_discriminating_region_at_appropriate_scale,
        test_frontier_finder,
        test_bose_environment_more_restrictive_than_frozen,
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
