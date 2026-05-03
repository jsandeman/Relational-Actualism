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
    BOSE_2017_PERP,
    BMVEnvironment,
    MODELS,
    NO_DECOHERENCE,
    DecoherenceParams,
    actualization_rate_from_environment,
    blackbody_decoherence_rate,
    branch_phases,
    coherence_budget_scan,
    concurrence,
    critical_gamma,
    density_matrix,
    density_matrix_with_decoherence,
    gas_collision_rate,
    in_branch_coherent_regime,
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


# ── Tier 2: decoherence tests ────────────────────────────────────────
def test_decoherence_zero_reproduces_unitary() -> None:
    print("\n[10] gamma=0 reproduces the unitary (Tier 1) result")
    t_array = np.linspace(0.0, BOSE_2017.T, 11)
    res_unitary = sweep(BOSE_2017, t_array, "quantized")
    res_decoh0 = sweep(BOSE_2017, t_array, "quantized", decoherence=NO_DECOHERENCE)
    err_c = float(np.max(np.abs(res_unitary["concurrence"] - res_decoh0["concurrence"])))
    err_n = float(np.max(np.abs(res_unitary["negativity"] - res_decoh0["negativity"])))
    check("  concurrence matches unitary at gamma=0", err_c < 1e-12, f"err={err_c:.2e}")
    check("  negativity matches unitary at gamma=0", err_n < 1e-12, f"err={err_n:.2e}")


def test_decoherence_preserves_trace_and_hermiticity() -> None:
    print("\n[11] Local sigma_z dephasing preserves trace and Hermiticity")
    decoh = DecoherenceParams.symmetric(2.0)  # strong dephasing
    psi = state_quantized(BOSE_2017, BOSE_2017.T)
    rho = density_matrix_with_decoherence(psi, BOSE_2017.T, decoh)
    tr = float(np.real(np.trace(rho)))
    herm_err = float(np.max(np.abs(rho - rho.conj().T)))
    check("  trace == 1", abs(tr - 1.0) < 1e-12, f"tr={tr:.6f}")
    check("  Hermitian (rho == rho^†)", herm_err < 1e-14, f"err={herm_err:.2e}")


def test_decoherence_preserves_positivity() -> None:
    print("\n[12] Decohered density matrix is positive semi-definite")
    decoh = DecoherenceParams.symmetric(0.5)
    psi = state_quantized(BOSE_2017, BOSE_2017.T)
    rho = density_matrix_with_decoherence(psi, BOSE_2017.T, decoh)
    eigvals = np.linalg.eigvalsh(rho)
    min_eig = float(np.min(eigvals))
    check("  all eigenvalues >= -1e-12", min_eig >= -1e-12, f"min eig={min_eig:.2e}")


def test_decoherence_kills_entanglement_in_limit() -> None:
    print("\n[13] gamma → ∞ kills concurrence (quantized model)")
    t_array = np.linspace(0.01, BOSE_2017.T, 11)
    res_strong = sweep(BOSE_2017, t_array, "quantized",
                       decoherence=DecoherenceParams.symmetric(1e6))
    c_max = float(np.max(res_strong["concurrence"]))
    check("  C_max < 1e-6 at very strong gamma", c_max < 1e-6, f"C_max={c_max:.2e}")


def test_RA_unaffected_by_decoherence() -> None:
    print("\n[14] RA model: concurrence still ≡ 0 with decoherence on")
    t_array = np.linspace(0.0, BOSE_2017.T, 11)
    res = sweep(BOSE_2017, t_array, "RA",
                decoherence=DecoherenceParams.symmetric(1.0))
    c_max = float(np.max(res["concurrence"]))
    check("  RA concurrence with gamma=1/s < 1e-10", c_max < 1e-10, f"C_max={c_max:.2e}")


def test_coherence_budget_monotone_decreasing() -> None:
    print("\n[15] Quantized-gravity max-concurrence is monotone decreasing in gamma")
    gamma_array = np.logspace(-2, 1, 21)
    scan = coherence_budget_scan(BOSE_2017, gamma_array, model="quantized", n_t=21)
    diffs = np.diff(scan["max_concurrence"])
    # allow tiny numerical noise
    monotone = bool(np.all(diffs <= 1e-12))
    check("  C_max[i+1] <= C_max[i] for all i", monotone,
          f"max increase = {float(np.max(diffs)):.2e}")
    check("  C_max strictly decreases (not constant)",
          scan["max_concurrence"][0] > scan["max_concurrence"][-1] + 1e-6,
          f"C_max[0]={scan['max_concurrence'][0]:.4f}, "
          f"C_max[-1]={scan['max_concurrence'][-1]:.4f}")


def test_entanglement_sudden_death() -> None:
    print("\n[16b] Entanglement sudden death: C drops to identically 0 above some gamma")
    # at gamma = 0.5/s, decoherence is far stronger than the entangling rate;
    # the state should be truly separable (C exactly 0), not just suppressed.
    decoh = DecoherenceParams.symmetric(0.5)
    ts = np.linspace(0.0, BOSE_2017.T, 21)
    cs = []
    for t in ts:
        rho = density_matrix_with_decoherence(state_quantized(BOSE_2017, t), t, decoh)
        cs.append(concurrence(rho))
    c_max = float(max(cs))
    check("  C(t) == 0 exactly for all t at gamma=0.5/s",
          c_max == 0.0, f"max C = {c_max:.4e}")
    # naive coherence-decay would predict C ≈ 0.156 * exp(-2.5) ≈ 0.013, not 0;
    # the fact that C is identically zero is the ESD signature.


def test_perpendicular_geometry_larger_budget() -> None:
    print("\n[16c] Perpendicular geometry gives larger coherence budget than parallel")
    gamma_array = np.logspace(-3, 1, 41)
    scan_par = coherence_budget_scan(BOSE_2017,      gamma_array, n_t=21)
    scan_per = coherence_budget_scan(BOSE_2017_PERP, gamma_array, n_t=21)
    g_par = critical_gamma(scan_par, 0.01)
    g_per = critical_gamma(scan_per, 0.01)
    check("  perpendicular gamma_crit > parallel gamma_crit (at C=0.01)",
          g_per > g_par, f"par={g_par:.3e}, perp={g_per:.3e}")
    check("  perpendicular peak C > parallel peak C",
          scan_per["max_concurrence"][0] > scan_par["max_concurrence"][0],
          f"par={scan_par['max_concurrence'][0]:.3f}, "
          f"perp={scan_per['max_concurrence'][0]:.3f}")


def test_critical_gamma_basic() -> None:
    print("\n[16] critical_gamma returns a sensible threshold")
    gamma_array = np.logspace(-3, 2, 81)
    scan = coherence_budget_scan(BOSE_2017, gamma_array, model="quantized")
    g_low = critical_gamma(scan, 0.001)
    g_high = critical_gamma(scan, 0.1)
    check("  critical_gamma(C=0.001) > critical_gamma(C=0.1)",
          g_low > g_high, f"g(0.001)={g_low:.3e}, g(0.1)={g_high:.3e}")
    # for C floor above the gamma=0 maximum, returns 0.0
    c_unattainable = scan["max_concurrence"][0] * 1.5
    g_unattainable = critical_gamma(scan, c_unattainable)
    check("  critical_gamma returns 0 when floor is unreachable",
          g_unattainable == 0.0, f"g={g_unattainable}")


# ── Tier 3: positional actualization rate tests ──────────────────────
def test_environment_rates_scale_with_pressure() -> None:
    print("\n[17] gas-collision rate scales linearly with pressure")
    env_lo = BMVEnvironment(pressure_Pa=1e-12, T_gas_K=4.0)
    env_hi = BMVEnvironment(pressure_Pa=1e-6,  T_gas_K=4.0)
    g_lo = gas_collision_rate(env_lo, BOSE_2017)
    g_hi = gas_collision_rate(env_hi, BOSE_2017)
    ratio = g_hi / g_lo
    check("  rate ratio ~ pressure ratio (1e6)",
          5e5 < ratio < 5e6, f"ratio = {ratio:.3e}")


def test_blackbody_T9_scaling() -> None:
    print("\n[18] blackbody-photon rate scales as T^9")
    p = BOSE_2017
    g_1K = blackbody_decoherence_rate(BMVEnvironment(T_blackbody_K=1.0), p)
    g_2K = blackbody_decoherence_rate(BMVEnvironment(T_blackbody_K=2.0), p)
    ratio = g_2K / g_1K
    expected = 2.0 ** 9
    rel_err = abs(ratio - expected) / expected
    check("  rate(2K)/rate(1K) ~ 2^9 = 512", rel_err < 1e-9,
          f"ratio={ratio:.1f}, expected={expected}")


def test_room_temperature_violates_branch_coherent_regime() -> None:
    print("\n[19] Room-temperature high vacuum violates branch-coherent regime")
    env_room = BMVEnvironment(pressure_Pa=1e-6, T_gas_K=300.0, T_blackbody_K=300.0)
    # use a representative gamma_ESD; any reasonable Bose 2017 protocol
    # has gamma_ESD in [0.01, 1] /s
    v = in_branch_coherent_regime(env_room, BOSE_2017, gamma_esd=0.06)
    check("  branch_coherent == False at room temp", not v["branch_coherent"],
          f"lambda_pos = {v['lambda_pos_per_s']:.3e} /s")
    check("  lambda_pos >> gamma_ESD by many decades",
          v["margin_factor"] < 1e-3,
          f"margin = {v['margin_factor']:.3e}x (i.e. {1/v['margin_factor']:.1e}x over budget)")


def test_actualization_rate_components() -> None:
    print("\n[20] actualization_rate_from_environment returns gas + blackbody = total")
    env = BMVEnvironment(pressure_Pa=1e-10, T_gas_K=4.0, T_blackbody_K=4.0)
    rates = actualization_rate_from_environment(env, BOSE_2017)
    check("  gas + blackbody == total",
          abs(rates["gas"] + rates["blackbody"] - rates["total"]) < 1e-30,
          f"gas={rates['gas']:.3e}, bb={rates['blackbody']:.3e}, "
          f"total={rates['total']:.3e}")


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
        test_decoherence_zero_reproduces_unitary,
        test_decoherence_preserves_trace_and_hermiticity,
        test_decoherence_preserves_positivity,
        test_decoherence_kills_entanglement_in_limit,
        test_RA_unaffected_by_decoherence,
        test_coherence_budget_monotone_decreasing,
        test_entanglement_sudden_death,
        test_perpendicular_geometry_larger_budget,
        test_critical_gamma_basic,
        test_environment_rates_scale_with_pressure,
        test_blackbody_T9_scaling,
        test_room_temperature_violates_branch_coherent_regime,
        test_actualization_rate_components,
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
