"""
test_bmv_comparator.py
Sanity tests for the BMV comparator.

Run from src/RA_AQFT:  python test_bmv_comparator.py
"""

from __future__ import annotations

import sys

import numpy as np

from bmv_comparator import (
    BMVParams,
    BOSE_2017,
    MODELS,
    branch_phases,
    concurrence,
    density_matrix,
    negativity,
    partial_transpose_B,
    phase_invariant,
    state_quantized,
    state_RA,
    state_semiclassical,
    sweep,
)


# ── tiny test framework ──────────────────────────────────────────────
_FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    print(f"  [{status}] {name}" + (f"  — {detail}" if detail else ""))
    if not cond:
        _FAILS.append(name)


# ── tests ────────────────────────────────────────────────────────────
def test_initial_state_is_separable() -> None:
    print("\n[1] At t=0, every model gives a separable product state")
    for model_name, fn in MODELS.items():
        rho = density_matrix(fn(BOSE_2017, 0.0))
        n = negativity(rho)
        check(f"  {model_name}: negativity(t=0) ~ 0", n < 1e-12, f"N={n:.2e}")


def test_RA_negativity_identically_zero() -> None:
    print("\n[2] RA model: negativity ≡ 0 for all t (structural prediction)")
    t_array = np.linspace(0.0, 10.0, 41)
    res = sweep(BOSE_2017, t_array, "RA")
    n_max = float(np.max(res["negativity"]))
    check("  max negativity over 0..10s < 1e-12", n_max < 1e-12, f"max N={n_max:.2e}")
    check("  delta_phi[t=T] is exactly zero",
          res["delta_phi"][-1] == 0.0,
          f"Δφ={res['delta_phi'][-1]}")


def test_RA_concurrence_identically_zero() -> None:
    print("\n[3] RA model: concurrence ≡ 0 (no entanglement, ever)")
    res = sweep(BOSE_2017, np.linspace(0.0, BOSE_2017.T, 11), "RA")
    c_max = float(np.max(res["concurrence"]))
    check("  max concurrence < 1e-10", c_max < 1e-10, f"max C={c_max:.2e}")


def test_quantized_gravity_generates_entanglement() -> None:
    print("\n[4] Quantized-gravity model: generates entanglement at finite t")
    t_array = np.linspace(0.0, BOSE_2017.T, 51)
    res = sweep(BOSE_2017, t_array, "quantized")
    n_max = float(np.max(res["negativity"]))
    c_max = float(np.max(res["concurrence"]))
    check("  peak negativity > 0", n_max > 0.0, f"N_max={n_max:.4f}")
    check("  peak concurrence > 0", c_max > 0.0, f"C_max={c_max:.4f}")
    # for 2-qubit pure states, N = C/2 exactly
    rel_err = abs(c_max - 2.0 * n_max) / max(c_max, 1e-15)
    check("  C ≈ 2N (pure-state identity)", rel_err < 1e-8,
          f"|C-2N|/C = {rel_err:.2e}")


def test_semiclassical_no_entanglement() -> None:
    print("\n[5] Semiclassical model: source-averaged phase ⇒ no entanglement")
    t_array = np.linspace(0.0, BOSE_2017.T, 21)
    res = sweep(BOSE_2017, t_array, "semiclassical")
    n_max = float(np.max(res["negativity"]))
    check("  max negativity < 1e-12", n_max < 1e-12, f"max N={n_max:.2e}")


def test_partial_transpose_involution() -> None:
    print("\n[6] Partial transpose is an involution")
    psi = state_quantized(BOSE_2017, BOSE_2017.T)
    rho = density_matrix(psi)
    rho_pt_pt = partial_transpose_B(partial_transpose_B(rho))
    err = float(np.max(np.abs(rho - rho_pt_pt)))
    check("  PT(PT(rho)) == rho", err < 1e-12, f"err={err:.2e}")


def test_phase_invariant_geometry() -> None:
    print("\n[7] Phase invariant matches the analytic formula (parallel geometry)")
    p = BOSE_2017
    t = p.T
    phi = branch_phases(p, t)
    delta_analytic = (
        2.0 / p.d - 1.0 / (p.d + p.dX) - 1.0 / (p.d - p.dX)
    ) * (6.67430e-11 * p.m * p.m * t / 1.054571817e-34)
    delta_numeric = phase_invariant(phi)
    rel_err = abs(delta_numeric - delta_analytic) / abs(delta_analytic)
    check("  Δφ matches G m^2 t/ℏ × geometry factor", rel_err < 1e-12,
          f"rel_err={rel_err:.2e}")


def test_perpendicular_geometry_still_entangles() -> None:
    print("\n[8] Perpendicular geometry: d_LR == d_RL but Δφ ≠ 0 (still entangles)")
    p_perp = BMVParams(geometry="perpendicular", d=200.0e-6)
    phi = branch_phases(p_perp, p_perp.T)
    check("  d_LR == d_RL", abs(phi["LR"] - phi["RL"]) < 1e-15)
    delta = phase_invariant(phi)
    check("  Δφ ≠ 0 (LL+RR ≠ LR+RL)", abs(delta) > 1e-3,
          f"Δφ={delta:.4e}")
    # entanglement is generated but smaller than parallel for given (d, dX)
    res_perp = sweep(p_perp, np.array([p_perp.T]), "quantized")
    check("  perpendicular geometry produces entanglement",
          res_perp["concurrence"][0] > 0.0,
          f"C={res_perp['concurrence'][0]:.4e}")


def test_parallel_geometry_validation() -> None:
    print("\n[9] Parallel geometry rejects d <= dX")
    bad = BMVParams(d=100e-6, dX=200e-6, geometry="parallel")
    raised = False
    try:
        bad.branch_distances()
    except ValueError:
        raised = True
    check("  ValueError raised for d <= dX", raised)


# ── runner ───────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 78)
    print("BMV comparator — test suite")
    print("=" * 78)
    for fn in [
        test_initial_state_is_separable,
        test_RA_negativity_identically_zero,
        test_RA_concurrence_identically_zero,
        test_quantized_gravity_generates_entanglement,
        test_semiclassical_no_entanglement,
        test_partial_transpose_involution,
        test_phase_invariant_geometry,
        test_perpendicular_geometry_still_entangles,
        test_parallel_geometry_validation,
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
