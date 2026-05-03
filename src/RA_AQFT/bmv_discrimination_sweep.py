"""
bmv_discrimination_sweep.py
Relational Actualism — BMV discriminator regime sweep (Tier 4)

Scans the BMV parameter space (m, dX, d, T) under a fixed experimental
environment to locate the regime where the protocol can actually
distinguish RA from quantized gravity. The discrimination criterion:

    realistic peak concurrence C_realistic(p, env) >= C_floor

where C_realistic is the peak concurrence over the time window under
the quantized-gravity model WITH decoherence applied at the realistic
rate Gamma_decoh from Tier 3a. If C_realistic < C_floor for a given
(p, env), the protocol cannot distinguish RA from quantized gravity
for any value of measurement sensitivity at or above C_floor.

Tier 1-3 results carried forward:
  - Bose 2017 nominal (m=1e-14 kg, dX=250 um): unitary C ~ 0.16 but
    realistic C ~ 0 because Gamma_decoh ~ 1e6 /s >> gamma_ESD ~ 0.06 /s.
  - At smaller m, both signal and decoherence drop, and the trade-off
    is non-monotone in the protocol parameters. This module sweeps to
    find the discriminating frontier.

Authors: Joshua F. Sandeman (framework); Claude/Anthropic (computation)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from bmv_comparator import (
    BMVEnvironment,
    BMVParams,
    DecoherenceParams,
    actualization_rate_from_environment,
    concurrence,
    density_matrix_with_decoherence,
    state_quantized,
)


# ── canonical reference parameter points ──────────────────────────────
BOSE_2017 = BMVParams(m=1e-14, dX=250e-6, d=450e-6, T=2.5)
CARNEY_NOMINAL = BMVParams(m=1e-19, dX=1e-6, d=2e-6, T=10.0)
"""Hypothetical Carney-style smaller-mass point. Whether it actually
discriminates is the empirical question this module answers."""

ADVANCED_NEAR_TERM = BMVParams(m=1e-15, dX=10e-6, d=20e-6, T=10.0)
"""A more aggressive but still 'within decade' alternative."""

ENV_BOSE_IDEAL = BMVEnvironment(pressure_Pa=1e-12, T_gas_K=0.1, T_blackbody_K=0.1)
ENV_FROZEN_LAB = BMVEnvironment(pressure_Pa=1e-15, T_gas_K=0.01, T_blackbody_K=0.01)
"""Frozen-lab: pushed to the edge of what may ever be physically realizable."""


# ── core discrimination check ─────────────────────────────────────────
@dataclass(frozen=True)
class DiscriminationVerdict:
    """Discrimination check for a (BMVParams, BMVEnvironment) pair."""
    m: float
    dX: float
    d: float
    T: float
    geometry: str
    pressure_Pa: float
    T_gas_K: float
    gamma_decoh_per_s: float
    unitary_peak_C: float
    realistic_peak_C: float
    discriminating: bool
    c_floor: float


def realistic_peak_concurrence(
    p: BMVParams,
    env: BMVEnvironment,
    n_t: int = 51,
) -> tuple[float, float, float]:
    """Peak concurrence over [0, T] under quantized-gravity with realistic
    Tier-3a decoherence applied. Returns (unitary peak, realistic peak,
    gamma_decoh)."""
    rates = actualization_rate_from_environment(env, p)
    gamma = rates["total"]
    decoh = DecoherenceParams.symmetric(gamma)
    t_array = np.linspace(0.0, p.T, n_t)
    c_unitary_max = 0.0
    c_realistic_max = 0.0
    for t in t_array:
        psi = state_quantized(p, t)
        c_unitary_max = max(c_unitary_max,
                            concurrence(density_matrix_with_decoherence(
                                psi, t, DecoherenceParams())))
        c_realistic_max = max(c_realistic_max,
                              concurrence(density_matrix_with_decoherence(
                                  psi, t, decoh)))
    return c_unitary_max, c_realistic_max, gamma


def discrimination_check(
    p: BMVParams,
    env: BMVEnvironment,
    c_floor: float = 0.01,
    n_t: int = 51,
) -> DiscriminationVerdict:
    c_u, c_r, g = realistic_peak_concurrence(p, env, n_t=n_t)
    return DiscriminationVerdict(
        m=p.m, dX=p.dX, d=p.d, T=p.T, geometry=p.geometry,
        pressure_Pa=env.pressure_Pa, T_gas_K=env.T_gas_K,
        gamma_decoh_per_s=g,
        unitary_peak_C=c_u,
        realistic_peak_C=c_r,
        discriminating=(c_r >= c_floor),
        c_floor=c_floor,
    )


# ── 2D sweep over (m, T) ──────────────────────────────────────────────
def sweep_mass_time(
    m_array: np.ndarray,
    T_array: np.ndarray,
    dX: float,
    d: float,
    env: BMVEnvironment,
    geometry: str = "parallel",
    c_floor: float = 0.01,
    n_t: int = 31,
) -> dict[str, np.ndarray]:
    """2D sweep of discrimination over (m, T) at fixed (dX, d, env).

    Returns dict of 2D arrays indexed by [i_m, j_T]:
      m, T, gamma_decoh, unitary_peak_C, realistic_peak_C, discriminating
    """
    nm, nT = len(m_array), len(T_array)
    out = {
        "m": np.zeros((nm, nT)),
        "T": np.zeros((nm, nT)),
        "gamma_decoh": np.zeros((nm, nT)),
        "unitary_peak_C": np.zeros((nm, nT)),
        "realistic_peak_C": np.zeros((nm, nT)),
        "discriminating": np.zeros((nm, nT), dtype=bool),
    }
    for i, m in enumerate(m_array):
        for j, T in enumerate(T_array):
            p = BMVParams(m=float(m), dX=dX, d=d, T=float(T), geometry=geometry)
            v = discrimination_check(p, env, c_floor=c_floor, n_t=n_t)
            out["m"][i, j] = m
            out["T"][i, j] = T
            out["gamma_decoh"][i, j] = v.gamma_decoh_per_s
            out["unitary_peak_C"][i, j] = v.unitary_peak_C
            out["realistic_peak_C"][i, j] = v.realistic_peak_C
            out["discriminating"][i, j] = v.discriminating
    return out


def find_minimum_discriminating_mass(
    sweep: dict[str, np.ndarray],
) -> dict[str, float]:
    """Given a sweep over (m, T), return the smallest m that discriminates
    for at least one T in the sweep, and the corresponding T."""
    disc = sweep["discriminating"]
    if not disc.any():
        return {"m_min": float("inf"), "T_at_m_min": float("nan"),
                "discriminating_count": 0}
    # for each row (fixed m), check if any T discriminates
    row_any = disc.any(axis=1)
    i_min = int(np.argmax(row_any))  # first True row
    j_min = int(np.argmax(disc[i_min]))  # first True T in that row
    return {
        "m_min": float(sweep["m"][i_min, j_min]),
        "T_at_m_min": float(sweep["T"][i_min, j_min]),
        "discriminating_count": int(disc.sum()),
    }


# ── main: characterize the discriminator regime ───────────────────────
def main() -> None:
    print("=" * 78)
    print("BMV DISCRIMINATION SWEEP — Tier 4")
    print("=" * 78)
    print("""\
Discrimination criterion: realistic peak concurrence (under quantized gravity
with Tier-3a decoherence applied) must reach C_floor = 0.01 for at least
one t in the interaction window.
""")

    # 1. canonical reference points
    print("-" * 78)
    print("Canonical reference points (Bose 2017 ideal cryo UHV environment):")
    print("-" * 78)
    points = [
        ("Bose 2017 nominal (m=1e-14, dX=250um, d=450um, T=2.5s)", BOSE_2017),
        ("Advanced near-term (m=1e-15, dX=10um, d=20um, T=10s)", ADVANCED_NEAR_TERM),
        ("Carney nominal (m=1e-19, dX=1um, d=2um, T=10s)", CARNEY_NOMINAL),
    ]
    print(f"\n  {'point':<60}{'C_unitary':>11}{'C_real':>10}{'discr?':>10}")
    print("  " + "-" * 90)
    for label, p in points:
        v = discrimination_check(p, ENV_BOSE_IDEAL)
        verdict = "YES" if v.discriminating else "NO"
        print(f"  {label:<60}{v.unitary_peak_C:>11.4e}"
              f"{v.realistic_peak_C:>10.2e}{verdict:>10}")

    # 2. push to "frozen lab" environment
    print("\n  Same points under FROZEN LAB environment (P=1e-15, T=0.01 K):")
    print(f"\n  {'point':<60}{'C_unitary':>11}{'C_real':>10}{'discr?':>10}")
    print("  " + "-" * 90)
    for label, p in points:
        v = discrimination_check(p, ENV_FROZEN_LAB)
        verdict = "YES" if v.discriminating else "NO"
        print(f"  {label:<60}{v.unitary_peak_C:>11.4e}"
              f"{v.realistic_peak_C:>10.2e}{verdict:>10}")

    # 3. sweep over (m, T) to locate the discriminating frontier
    print("\n" + "-" * 78)
    print("2D sweep over (m, T) at fixed (dX=1um, d=2um, FROZEN LAB env):")
    print("-" * 78)
    m_array = np.logspace(-22, -12, 21)  # 10^-22 to 10^-12 kg, 11 decades
    T_array = np.array([0.1, 1.0, 10.0, 100.0, 1000.0])
    print(f"  m sweep: {m_array[0]:.0e} ... {m_array[-1]:.0e} kg ({len(m_array)} pts)")
    print(f"  T sweep: {list(T_array)} s")
    sweep = sweep_mass_time(
        m_array=m_array,
        T_array=T_array,
        dX=1e-6, d=2e-6,
        env=ENV_FROZEN_LAB,
        c_floor=0.01,
        n_t=21,
    )

    # ASCII map of the discriminating region
    print(f"\n  Discrimination map (Y = discriminating, . = not):")
    print(f"  {'m \\\\ T':<14}" + "".join(f"{T:>11.1g}" for T in T_array))
    for i in range(len(m_array)):
        row = "  " + f"{m_array[i]:.2e}".ljust(14)
        for j in range(len(T_array)):
            row += f"{'Y' if sweep['discriminating'][i,j] else '.':>11}"
        print(row)

    # frontier
    front = find_minimum_discriminating_mass(sweep)
    if front["discriminating_count"] == 0:
        print("\n  No (m, T) combination in the sweep clears the discrimination floor.")
    else:
        print(f"\n  Frontier: smallest m that discriminates at any T in sweep:")
        print(f"    m_min        = {front['m_min']:.3e} kg")
        print(f"    T at m_min   = {front['T_at_m_min']:.3g} s")
        print(f"    total grid points discriminating: {front['discriminating_count']}"
              f" / {len(m_array) * len(T_array)}")

    # 4. realistic-environment frontier
    print("\n" + "-" * 78)
    print("Same sweep under Bose 2017 IDEAL environment (P=1e-12, T=0.1 K):")
    print("-" * 78)
    sweep_ideal = sweep_mass_time(
        m_array=m_array,
        T_array=T_array,
        dX=1e-6, d=2e-6,
        env=ENV_BOSE_IDEAL,
        c_floor=0.01,
        n_t=21,
    )
    print(f"\n  Discrimination map:")
    print(f"  {'m \\\\ T':<14}" + "".join(f"{T:>11.1g}" for T in T_array))
    for i in range(len(m_array)):
        row = "  " + f"{m_array[i]:.2e}".ljust(14)
        for j in range(len(T_array)):
            row += f"{'Y' if sweep_ideal['discriminating'][i,j] else '.':>11}"
        print(row)

    front_ideal = find_minimum_discriminating_mass(sweep_ideal)
    if front_ideal["discriminating_count"] == 0:
        print("\n  Bose 2017 IDEAL environment: NO discriminating (m, T) point in sweep.")
    else:
        print(f"\n  Frontier under Bose 2017 IDEAL: m_min = {front_ideal['m_min']:.3e} kg")

    # 4b. nanoscale-geometry sweep — does Carney's 1e-19 kg become reachable
    # if we also shrink the geometry to nm scale (where dX^2/d^3 is much
    # larger so the gravitational signal scales up)?
    print("\n" + "-" * 78)
    print("Sweep at NANOSCALE geometry (dX=10nm, d=20nm), FROZEN LAB env:")
    print("(probes Carney-style m=1e-19 kg target)")
    print("-" * 78)
    sweep_nano = sweep_mass_time(
        m_array=m_array,
        T_array=T_array,
        dX=10e-9, d=20e-9,
        env=ENV_FROZEN_LAB,
        c_floor=0.01,
        n_t=21,
    )
    print(f"\n  Discrimination map:")
    print(f"  {'m \\\\ T':<14}" + "".join(f"{T:>11.1g}" for T in T_array))
    for i in range(len(m_array)):
        row = "  " + f"{m_array[i]:.2e}".ljust(14)
        for j in range(len(T_array)):
            row += f"{'Y' if sweep_nano['discriminating'][i,j] else '.':>11}"
        print(row)
    front_nano = find_minimum_discriminating_mass(sweep_nano)
    if front_nano["discriminating_count"] == 0:
        print("\n  Nanoscale geometry frontier: NO discriminating point in sweep.")
    else:
        print(f"\n  Nanoscale frontier: m_min = {front_nano['m_min']:.3e} kg "
              f"at T = {front_nano['T_at_m_min']:.3g} s")

    # 5. write CSV
    out_path = Path(__file__).parent / "bmv_discrimination_sweep.csv"
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["environment", "m_kg", "T_s",
                    "gamma_decoh_per_s", "unitary_peak_C",
                    "realistic_peak_C", "discriminating"])
        for env_label, sw in [("frozen_lab_um", sweep),
                              ("bose_ideal_um", sweep_ideal),
                              ("frozen_lab_nm", sweep_nano)]:
            for i in range(len(m_array)):
                for j in range(len(T_array)):
                    w.writerow([
                        env_label,
                        f"{sw['m'][i,j]:.3e}",
                        f"{sw['T'][i,j]:.3g}",
                        f"{sw['gamma_decoh'][i,j]:.3e}",
                        f"{sw['unitary_peak_C'][i,j]:.4e}",
                        f"{sw['realistic_peak_C'][i,j]:.4e}",
                        int(sw['discriminating'][i,j]),
                    ])
    print(f"\n  Discrimination sweep CSV written to: {out_path}")

    # 6. closing summary
    print("\n" + "=" * 78)
    print("TIER 4 SUMMARY")
    print("=" * 78)
    print(f"""\
Bose 2017 ideal environment (P=1e-12 Pa, 0.1 K):
  Discriminating region: {'present' if front_ideal['discriminating_count']>0 else 'EMPTY'}
  {('m_min = ' + f"{front_ideal['m_min']:.3e}" + ' kg') if front_ideal['discriminating_count']>0 else 'No (m, T) in sweep clears C_floor=0.01.'}

Frozen lab environment (P=1e-15 Pa, 0.01 K — beyond current capability):
  Discriminating region: {'present' if front['discriminating_count']>0 else 'EMPTY'}
  {('m_min = ' + f"{front['m_min']:.3e}" + ' kg') if front['discriminating_count']>0 else 'No (m, T) in sweep clears C_floor=0.01.'}

Nanoscale geometry (dX=10 nm, d=20 nm) under frozen lab env:
  Discriminating region: {'present' if front_nano['discriminating_count']>0 else 'EMPTY'}
  {('m_min = ' + f"{front_nano['m_min']:.3e}" + ' kg') if front_nano['discriminating_count']>0 else 'No (m, T) in sweep clears C_floor=0.01.'}

Implication for RA-PRED-008:
  The BMV null prediction is empirically distinguishable from quantized
  gravity only in the regime where (a) the gravitational signal is large
  enough to give C >= 0.01 and (b) decoherence is below the ESD threshold.
  At fixed (dX=1um, d=2um), shrinking m below the frontier kills the
  signal faster than it kills decoherence, so RA's null becomes
  vacuously consistent with all observations.""")


if __name__ == "__main__":
    main()
