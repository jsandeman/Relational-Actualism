"""
bmv_comparator.py
Relational Actualism — BMV (Bose-Marletto-Vedral) Comparator

Computes the predicted gravity-mediated entanglement signal for the
BMV protocol under three competing hypotheses:

  1. Quantized gravity   — branch-resolved Newtonian phases (Bose 2017,
                            Marletto-Vedral 2017). Each branch |ij> picks
                            up its own phase phi_ij = G m^2 t / (hbar d_ij).
  2. Semiclassical gravity — common potential sourced by <T_munu>; the
                            phase is the source-averaged value, common to
                            all branches. No entanglement.
  3. Relational Actualism — Step-5 metric is sourced only by the
                            actualized ledger (Step-4 inscriptions). In
                            the branch-coherent regime, the gravitational
                            phase is common-mode and the entangling phase
                            invariant vanishes identically:
                                Delta phi_grav = 0.
                            See docs/RA_History/RA_BMV_Note.tex.

Three entanglement measures are computed for each model:
  - Phase invariant     Delta phi = phi_LL + phi_RR - phi_LR - phi_RL
                        (the entangling-phase generator; nonzero ⇒
                         entangled in the quantized model)
  - Concurrence         C(rho) = max(0, lambda_1 - lambda_2 - lambda_3
                                      - lambda_4)  (Wootters formula).
                        This is the entanglement measure the Bose 2017
                        spin-correlator witness operationalizes; the
                        proposed measurement scheme bounds C from below
                        via spin-correlator combinations.
  - Negativity          N(rho) = (||rho^{T_B}||_1 - 1) / 2
                        For 2-qubit pure states, N = C/2.

Default parameter set: Bose 2017 nominal
  m = 1e-14 kg          (mesoscopic test mass)
  Delta X = 250e-6 m    (positional splitting)
  d = 450e-6 m          (inter-mass center separation; chosen > Delta X
                          for the parallel-along-axis geometry; the paper
                          uses a perpendicular geometry with d=200e-6,
                          which is selectable via geometry='perpendicular')
  T = 2.5 s             (interaction time)

Geometry options
----------------
'parallel'     : both masses split along the line of centers.
                 d_LL = d_RR = d,  d_LR = d + dX,  d_RL = d - dX
                 (requires d > dX). Maximum Delta phi for given d, dX.
'perpendicular': each mass split perpendicular to the line of centers.
                 d_LL = d_RR = d,  d_LR = d_RL = sqrt(d^2 + dX^2)
                 No d > dX constraint.

Authors: Joshua F. Sandeman (framework); Claude/Anthropic (computation)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from math import sqrt
from pathlib import Path

import numpy as np

# ── Physical constants (SI) ───────────────────────────────────────────
G_NEWTON = 6.67430e-11      # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34      # J s


# ── Parameter container ───────────────────────────────────────────────
@dataclass(frozen=True)
class BMVParams:
    """Bose-Marletto-Vedral protocol parameters."""
    m: float = 1.0e-14          # mass per particle (kg)
    dX: float = 250.0e-6        # positional splitting (m)
    d: float = 450.0e-6         # inter-mass center separation (m)
    T: float = 2.5              # total interaction time (s)
    geometry: str = "parallel"  # 'parallel' or 'perpendicular'

    def branch_distances(self) -> dict[str, float]:
        """Return d_LL, d_LR, d_RL, d_RR for the chosen geometry."""
        if self.geometry == "parallel":
            if self.d <= self.dX:
                raise ValueError(
                    f"parallel geometry requires d > dX; got d={self.d}, dX={self.dX}"
                )
            return {
                "LL": self.d,
                "RR": self.d,
                "LR": self.d + self.dX,
                "RL": self.d - self.dX,
            }
        if self.geometry == "perpendicular":
            diag = sqrt(self.d * self.d + self.dX * self.dX)
            return {"LL": self.d, "RR": self.d, "LR": diag, "RL": diag}
        raise ValueError(f"unknown geometry: {self.geometry!r}")


BOSE_2017 = BMVParams()
BOSE_2017_PERP = BMVParams(geometry="perpendicular", d=200.0e-6, dX=250.0e-6)
"""Bose 2017 paper's actual geometry: closer approach (d < dX) but
splitting perpendicular to the line of centers, so d_LR = d_RL = sqrt(d^2 + dX^2).
Yields larger Delta phi than the default parallel geometry and a roughly 2x
larger coherence budget."""


@dataclass(frozen=True)
class DecoherenceParams:
    """Local position-basis dephasing rates (per second) on each mass.

    Models the dominant BMV decoherence channel: environmental scattering
    (background gas, blackbody, residual photons) that distinguishes |L>
    from |R>. Equivalent Lindblad operators L_X = sqrt(gamma_X) sigma_z^X
    on each mass, where sigma_z is diagonal in the |L>, |R> basis.

    Because [H_grav, sigma_z^X] = 0 for the BMV Hamiltonian (both
    diagonal in the position basis), the master equation has a closed
    form: each off-diagonal density-matrix element rho_{(ij),(kl)} is
    multiplied by exp(-Gamma_eff * t) where
        Gamma_eff = gamma_A * [i != k] + gamma_B * [j != l].
    Diagonal elements (populations) are unchanged. Trace and CP-positivity
    are preserved.

    Bose 2017 estimate: gamma <= 0.4 / s required for the protocol.
    Achievable in good vacuum (1e-6 Pa) with diamond traps at low T.
    """
    gamma_A: float = 0.0   # 1/s, local dephasing on mass A
    gamma_B: float = 0.0   # 1/s, local dephasing on mass B

    @classmethod
    def symmetric(cls, gamma: float) -> "DecoherenceParams":
        return cls(gamma_A=gamma, gamma_B=gamma)


NO_DECOHERENCE = DecoherenceParams()


# ── Tier 3: positional actualization rate from environment ────────────
@dataclass(frozen=True)
class BMVEnvironment:
    """Experimental environment for the BMV apparatus.

    Used in Tier 3 to estimate the positional actualization rate
    lambda_pos via the bridge interpretation lambda_pos = Gamma_decoh.

    Default: a near-ideal cryogenic UHV setup. Realistic experimental
    conditions are typically orders of magnitude worse than these
    defaults.
    """
    pressure_Pa: float = 1.0e-12       # background gas pressure
    T_gas_K: float = 0.1               # gas temperature
    T_blackbody_K: float = 0.1         # background radiation temperature
    gas_molar_mass_kg: float = 4.65e-26  # N2 molecule (default)


# physical constants for environment computations
_K_BOLTZ = 1.380649e-23  # J/K


def gas_collision_rate(env: BMVEnvironment, p: BMVParams) -> float:
    """Position-distinguishing gas-collision decoherence rate (1/s).

    Standard estimate: rate at which background-gas molecules scatter
    off the test mass and acquire which-path information. The
    geometric cross-section is taken to be pi * dX^2 (each scattered
    molecule resolves the L vs R alternative when its de Broglie
    wavelength is shorter than dX, which holds for thermal gas).
    """
    n_gas = env.pressure_Pa / (_K_BOLTZ * env.T_gas_K)
    v_thermal = sqrt(8.0 * _K_BOLTZ * env.T_gas_K / (3.14159265 * env.gas_molar_mass_kg))
    sigma_eff = 3.14159265 * p.dX * p.dX
    return n_gas * v_thermal * sigma_eff


def blackbody_decoherence_rate(env: BMVEnvironment, p: BMVParams) -> float:
    """Blackbody-photon scattering decoherence rate (1/s).

    Order-of-magnitude scaling from Joos-Zeh / Romero-Isart:
    Gamma_BB ~ 1e36 * (T_BB/300)^9 * dX^2 (SI units, dX in m).

    The T^9 dependence makes blackbody negligible at cryogenic
    temperatures; gas collisions dominate.
    """
    return 1.0e36 * (env.T_blackbody_K / 300.0)**9 * p.dX * p.dX


def actualization_rate_from_environment(
    env: BMVEnvironment, p: BMVParams
) -> dict[str, float]:
    """RA positional actualization rate lambda_pos (1/s) via the bridge
    interpretation lambda_pos = Gamma_decoh = Gamma_gas + Gamma_BB.

    BRIDGE INTERPRETATION (not native derivation):
      Each environmental scattering event in standard physics
      corresponds, in RA, to a Step-4 actualization that records
      position information about the test mass — the local DAG
      gains a vertex whose causal structure distinguishes L from R.
      Therefore the BDG-kernel positional actualization rate equals
      the conventional decoherence rate to leading order.

    NATIVE DERIVATION (open; tracked in RA-PRED-008.next_tasks 3b):
      A first-principles derivation would specify the test mass's
      graph patch, apply the BDG kernel K(N|mu) = Poisson(N;lambda) *
      [S>0] / P_acc with environmentally-determined mu, and count
      position-distinguishing actualization events directly. That
      derivation is outside Tier 3a scope.
    """
    g_gas = gas_collision_rate(env, p)
    g_bb = blackbody_decoherence_rate(env, p)
    return {
        "gas": g_gas,
        "blackbody": g_bb,
        "total": g_gas + g_bb,
    }


def in_branch_coherent_regime(
    env: BMVEnvironment,
    p: BMVParams,
    gamma_esd: float,
) -> dict[str, float | bool]:
    """Test whether the experimental environment keeps the protocol
    in the branch-coherent regime (lambda_pos < gamma_ESD).

    Returns a dict with components and verdict.
    """
    rates = actualization_rate_from_environment(env, p)
    lam = rates["total"]
    return {
        "lambda_pos_per_s": lam,
        "gamma_ESD_per_s": gamma_esd,
        "margin_factor": gamma_esd / lam if lam > 0 else float("inf"),
        "branch_coherent": lam < gamma_esd,
        "gas_rate_per_s": rates["gas"],
        "blackbody_rate_per_s": rates["blackbody"],
    }


# ── Branch phases ─────────────────────────────────────────────────────
def branch_phases(p: BMVParams, t: float) -> dict[str, float]:
    """Quantized-gravity Newtonian branch phases at time t.

    phi_ij(t) = G m^2 t / (hbar * d_ij)
    """
    prefactor = G_NEWTON * p.m * p.m * t / HBAR
    return {label: prefactor / dist for label, dist in p.branch_distances().items()}


def phase_invariant(phases: dict[str, float]) -> float:
    """Entangling phase invariant: phi_LL + phi_RR - phi_LR - phi_RL."""
    return phases["LL"] + phases["RR"] - phases["LR"] - phases["RL"]


# ── State evolution per model ─────────────────────────────────────────
# Basis ordering: |LL>, |LR>, |RL>, |RR>  (index 0..3, with A as MSB)
BASIS_LABELS = ("LL", "LR", "RL", "RR")


def _initial_amplitudes() -> np.ndarray:
    """Equal-superposition product state |+>_A |+>_B."""
    return 0.5 * np.ones(4, dtype=complex)


def state_quantized(p: BMVParams, t: float) -> np.ndarray:
    """Each branch acquires its own gravitational phase."""
    phases = branch_phases(p, t)
    return _initial_amplitudes() * np.array(
        [np.exp(1j * phases[lab]) for lab in BASIS_LABELS]
    )


def state_semiclassical(p: BMVParams, t: float) -> np.ndarray:
    """All branches acquire the source-averaged phase (common-mode).

    The semiclassical metric is sourced by <T_munu>; for the symmetric
    superposition the four configurations contribute equally, giving an
    averaged inverse-distance:  <1/d> = mean of 1/d_ij over branches.
    """
    distances = p.branch_distances()
    inv_d_avg = np.mean([1.0 / distances[lab] for lab in BASIS_LABELS])
    phi_common = G_NEWTON * p.m * p.m * t / HBAR * inv_d_avg
    return _initial_amplitudes() * np.exp(1j * phi_common)


def state_RA(p: BMVParams, t: float) -> np.ndarray:
    """Common-mode Step-5 phase from the actualized ledger.

    In the branch-coherent regime the Step-5 metric is sourced by the
    pre-interaction ledger configuration G_n alone (Lemma 'Step-2 non-
    sourcing'). All branches evolve under the same background potential,
    so the gravitational contribution is a global phase. We absorb it
    into U_0 = -G m^2 / d (background two-body potential at center
    separation d) for definiteness; any choice cancels in observables
    because it is global.
    """
    phi_common = -G_NEWTON * p.m * p.m * t / (HBAR * p.d)
    return _initial_amplitudes() * np.exp(1j * phi_common)


MODELS = {
    "quantized": state_quantized,
    "semiclassical": state_semiclassical,
    "RA": state_RA,
}


# ── Entanglement measures ─────────────────────────────────────────────
def density_matrix(state: np.ndarray) -> np.ndarray:
    return np.outer(state, np.conj(state))


# Off-diagonal decoherence factor table for local sigma_z dephasing.
# basis indexing: (i, j) ∈ {0,1}² with 0=L, 1=R; flat index 2i+j.
# Gamma_eff(ij, kl) = gamma_A * [i!=k] + gamma_B * [j!=l].
def _flip_count_table() -> tuple[np.ndarray, np.ndarray]:
    """Returns (n_A, n_B) where n_A[a,b] = [i_a != i_b], n_B[a,b] = [j_a != j_b]."""
    n_A = np.zeros((4, 4), dtype=int)
    n_B = np.zeros((4, 4), dtype=int)
    for a in range(4):
        ia, ja = a >> 1, a & 1
        for b in range(4):
            ib, jb = b >> 1, b & 1
            n_A[a, b] = int(ia != ib)
            n_B[a, b] = int(ja != jb)
    return n_A, n_B


_NA, _NB = _flip_count_table()


def density_matrix_with_decoherence(
    state: np.ndarray,
    t: float,
    decoh: DecoherenceParams,
) -> np.ndarray:
    """Apply local-dephasing Lindblad evolution to the unitary state.

    Closed-form: rho_{ab}(t) = rho_{ab}^{unitary}(t) * exp(-Gamma_eff(a,b) * t).
    Diagonals unchanged ⇒ trace preserved; positivity preserved (each
    coherence factor is real and ≤ 1).
    """
    rho = density_matrix(state)
    if decoh.gamma_A == 0.0 and decoh.gamma_B == 0.0:
        return rho
    gamma_eff = decoh.gamma_A * _NA + decoh.gamma_B * _NB
    return rho * np.exp(-gamma_eff * t)


def partial_transpose_B(rho: np.ndarray) -> np.ndarray:
    """Partial transpose on the second qubit. rho is 4x4 in basis |ij>."""
    rho_pt = np.empty_like(rho)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l_ in range(2):
                    # swap j <-> l in the second-subsystem indices
                    rho_pt[2 * i + j, 2 * k + l_] = rho[2 * i + l_, 2 * k + j]
    return rho_pt


def negativity(rho: np.ndarray) -> float:
    """N(rho) = sum of |negative eigenvalues of rho^{T_B}|.

    Equivalent to (||rho^{T_B}||_1 - 1) / 2 for valid density matrices.
    """
    eigvals = np.linalg.eigvalsh(partial_transpose_B(rho))
    return float(-np.sum(eigvals[eigvals < 0]))


# Pauli operators (single-qubit)
SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def concurrence(rho: np.ndarray) -> float:
    """Wootters concurrence for a 2-qubit density matrix.

    C(rho) = max(0, sqrt(l1) - sqrt(l2) - sqrt(l3) - sqrt(l4))
    where l_i are the eigenvalues (in decreasing order) of
    R = rho * (Y⊗Y) * rho^* * (Y⊗Y).

    This is the operational entanglement amount the Bose 2017 protocol
    measures via spin-correlator combinations. C ∈ [0, 1]; C = 0 iff
    the state is separable.
    """
    YY = np.kron(SIGMA_Y, SIGMA_Y)
    rho_tilde = YY @ np.conj(rho) @ YY
    R = rho @ rho_tilde
    eigvals = np.linalg.eigvals(R)
    # numerical noise can give tiny negative reals; clip
    eigvals = np.real(eigvals)
    eigvals = np.clip(eigvals, 0.0, None)
    sqrt_lams = np.sort(np.sqrt(eigvals))[::-1]  # descending
    return float(max(0.0, sqrt_lams[0] - sqrt_lams[1] - sqrt_lams[2] - sqrt_lams[3]))


def spin_correlators(rho: np.ndarray) -> dict[str, float]:
    """Return ⟨σ_a ⊗ σ_b⟩ for a, b ∈ {x, y, z}.

    These are the experimentally measured quantities in Bose 2017
    (Stern-Gerlach-decoded spin correlations); concurrence and other
    witnesses are reconstructed from them.
    """
    paulis = {"x": SIGMA_X, "y": SIGMA_Y, "z": SIGMA_Z}
    out: dict[str, float] = {}
    for a, P in paulis.items():
        for b, Q in paulis.items():
            out[f"{a}{b}"] = float(np.real(np.trace(rho @ np.kron(P, Q))))
    return out


# ── Sweep / driver ────────────────────────────────────────────────────
def sweep(
    p: BMVParams,
    t_array: np.ndarray,
    model: str,
    decoherence: DecoherenceParams = NO_DECOHERENCE,
) -> dict[str, np.ndarray]:
    """Compute (Delta phi, negativity, concurrence) over a time sweep.

    With decoherence != NO_DECOHERENCE, applies local sigma_z dephasing
    on each mass during the unitary evolution (see DecoherenceParams).
    """
    state_fn = MODELS[model]
    n = len(t_array)
    out = {
        "t": np.asarray(t_array, dtype=float),
        "delta_phi": np.zeros(n),
        "negativity": np.zeros(n),
        "concurrence": np.zeros(n),
    }
    for i, t in enumerate(t_array):
        if model == "quantized":
            out["delta_phi"][i] = phase_invariant(branch_phases(p, t))
        else:
            out["delta_phi"][i] = 0.0
        rho = density_matrix_with_decoherence(state_fn(p, t), t, decoherence)
        out["negativity"][i] = negativity(rho)
        out["concurrence"][i] = concurrence(rho)
    return out


# ── Tier 2: coherence-budget scan ─────────────────────────────────────
def coherence_budget_scan(
    p: BMVParams,
    gamma_array: np.ndarray,
    model: str = "quantized",
    n_t: int = 51,
) -> dict[str, np.ndarray]:
    """For each gamma (symmetric per-mass dephasing), return the maximum
    concurrence and negativity achieved over the interaction window [0, T].

    The output is the experimental discriminator curve: at each gamma,
    can the model produce a witnessable signal? For RA and semiclassical
    models the curve is identically zero. For quantized gravity it
    decreases monotonically with gamma; the gamma at which the curve
    crosses an experimental sensitivity floor is the maximum tolerated
    decoherence rate.
    """
    t_array = np.linspace(0.0, p.T, n_t)
    state_fn = MODELS[model]
    n = len(gamma_array)
    out = {
        "gamma": np.asarray(gamma_array, dtype=float),
        "tau_coh_s": np.where(np.asarray(gamma_array) > 0.0,
                              1.0 / np.where(np.asarray(gamma_array) > 0.0,
                                             gamma_array, 1.0),
                              np.inf),
        "max_concurrence": np.zeros(n),
        "max_negativity": np.zeros(n),
        "t_at_peak_s": np.zeros(n),
    }
    for i, g in enumerate(gamma_array):
        decoh = DecoherenceParams.symmetric(float(g))
        cs = np.zeros(len(t_array))
        ns = np.zeros(len(t_array))
        for k, t in enumerate(t_array):
            rho = density_matrix_with_decoherence(state_fn(p, t), t, decoh)
            cs[k] = concurrence(rho)
            ns[k] = negativity(rho)
        i_peak = int(np.argmax(cs))
        out["max_concurrence"][i] = cs[i_peak]
        out["max_negativity"][i] = ns[i_peak]
        out["t_at_peak_s"][i] = t_array[i_peak]
    return out


def critical_gamma(
    scan: dict[str, np.ndarray],
    sensitivity_floor: float,
) -> float:
    """Largest gamma at which max_concurrence still exceeds the
    sensitivity_floor (linearly interpolated). Returns +inf if the
    floor is never reached, 0.0 if it is exceeded at gamma=0 only.
    """
    g = scan["gamma"]
    c = scan["max_concurrence"]
    above = c >= sensitivity_floor
    if not above.any():
        return 0.0
    if above.all():
        return float("inf")
    # find the largest gamma where c crosses sensitivity_floor going down
    # (assumes c is monotonically decreasing in gamma — true for the
    #  closed-form local-dephasing model)
    idx = int(np.argmax(~above))  # first False after Trues
    if idx == 0:
        return 0.0
    g_lo, g_hi = g[idx - 1], g[idx]
    c_lo, c_hi = c[idx - 1], c[idx]
    if c_lo == c_hi:
        return float(g_lo)
    frac = (c_lo - sensitivity_floor) / (c_lo - c_hi)
    return float(g_lo + frac * (g_hi - g_lo))


def write_csv(results: dict[str, dict[str, np.ndarray]], path: Path) -> None:
    """results: {model_name: sweep_dict}. Writes long-format CSV."""
    with path.open("w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["model", "t_s", "delta_phi_rad", "negativity", "concurrence"])
        for model, data in results.items():
            for i in range(len(data["t"])):
                writer.writerow([
                    model,
                    f"{data['t'][i]:.6e}",
                    f"{data['delta_phi'][i]:.6e}",
                    f"{data['negativity'][i]:.6e}",
                    f"{data['concurrence'][i]:.6e}",
                ])


# ── Main: Bose 2017 nominal sweep ─────────────────────────────────────
def main() -> None:
    p = BOSE_2017
    print("=" * 78)
    print("BMV COMPARATOR — Bose 2017 nominal parameters")
    print("=" * 78)
    print(f"  m         = {p.m:.3e} kg")
    print(f"  dX        = {p.dX*1e6:.1f} um")
    print(f"  d         = {p.d*1e6:.1f} um")
    print(f"  T         = {p.T:.2f} s")
    print(f"  geometry  = {p.geometry}")
    distances = p.branch_distances()
    print("  branch distances (um): "
          + ", ".join(f"{k}={v*1e6:.1f}" for k, v in distances.items()))

    # phase scale
    phi_per_t = phase_invariant(branch_phases(p, 1.0))
    print(f"\n  Delta phi per second (quantized gravity) = {phi_per_t:.4e} rad/s")
    print(f"  Delta phi at T={p.T}s                       = {phi_per_t * p.T:.4e} rad")

    # time sweep
    t_array = np.linspace(0.0, p.T, 51)
    results = {model: sweep(p, t_array, model) for model in MODELS}

    print("\n" + "-" * 78)
    print(f"{'Model':<16}{'Delta phi(T)':>18}{'Negativity(T)':>18}{'Concurrence(T)':>18}")
    print("-" * 78)
    for name, data in results.items():
        print(f"{name:<16}"
              f"{data['delta_phi'][-1]:>18.6e}"
              f"{data['negativity'][-1]:>18.6e}"
              f"{data['concurrence'][-1]:>18.6e}")
    print("-" * 78)

    # discriminator: peak signal under quantized gravity
    q = results["quantized"]
    i_peak_neg = int(np.argmax(q["negativity"]))
    i_peak_con = int(np.argmax(q["concurrence"]))
    print(f"\nQuantized-gravity peak negativity : {q['negativity'][i_peak_neg]:.4f} "
          f"at t = {q['t'][i_peak_neg]:.3f} s")
    print(f"Quantized-gravity peak concurrence: {q['concurrence'][i_peak_con]:.4f} "
          f"at t = {q['t'][i_peak_con]:.3f} s")
    print(f"\nRA prediction: negativity ≡ 0  and  concurrence ≡ 0  for all t.")
    print(f"  RA negativity max over sweep  = "
          f"{np.max(results['RA']['negativity']):.2e}  (machine epsilon ~1e-16)")
    print(f"  RA concurrence max over sweep = "
          f"{np.max(results['RA']['concurrence']):.2e}")

    # write CSV
    out_path = Path(__file__).parent / "bmv_comparator_results.csv"
    write_csv(results, out_path)
    print(f"\nResults written to: {out_path}")

    # ── Tier 2: coherence-budget scan ────────────────────────────────
    print("\n" + "=" * 78)
    print("TIER 2 — COHERENCE BUDGET (local sigma_z dephasing per mass)")
    print("=" * 78)
    gamma_array = np.logspace(-3, 2, 81)  # 1e-3 .. 1e2 per second, 5 decades
    scan_q = coherence_budget_scan(BOSE_2017, gamma_array, model="quantized")
    scan_ra = coherence_budget_scan(BOSE_2017, gamma_array, model="RA")
    scan_q_perp = coherence_budget_scan(BOSE_2017_PERP, gamma_array, model="quantized")

    print(f"\n  Sweeping gamma over [{gamma_array[0]:.0e}, {gamma_array[-1]:.0e}] /s "
          f"({len(gamma_array)} points, log-spaced)")
    print(f"  At each gamma: max concurrence over t in [0, {BOSE_2017.T} s]")

    print("\n  gamma (1/s)   tau_coh (s)   C_max (quantized)   C_max (RA)")
    print("  " + "-" * 60)
    sample_idx = [0, 16, 32, 48, 64, 80]  # spaced log samples
    for i in sample_idx:
        g = scan_q["gamma"][i]
        tau = 1.0 / g if g > 0 else float("inf")
        print(f"  {g:>10.3e}   {tau:>9.2e}   {scan_q['max_concurrence'][i]:>17.4e}"
              f"   {scan_ra['max_concurrence'][i]:>10.2e}")

    # critical gamma for several sensitivity floors
    print("\n  Critical decoherence rate for the quantized-gravity model")
    print("  to remain detectable at given experimental concurrence floor:")
    print("\n  C_floor       gamma_crit (1/s)   tau_coh_min (s)")
    print("  " + "-" * 50)
    for c_floor in [0.001, 0.005, 0.01, 0.05, 0.1]:
        g_crit = critical_gamma(scan_q, c_floor)
        tau_min = 1.0 / g_crit if 0 < g_crit < float("inf") else float("inf")
        print(f"  {c_floor:>5.3f}    {g_crit:>12.4e}      {tau_min:>10.3e}")

    # locate the ESD threshold (gamma at which C drops identically to 0)
    def _esd_bracket(scan: dict[str, np.ndarray]) -> tuple[float, float] | None:
        nz = scan["max_concurrence"] > 0.0
        if not nz.any() or nz.all():
            return None
        i = int(np.argmax(~nz))
        return float(scan["gamma"][i - 1]), float(scan["gamma"][i])

    bracket = _esd_bracket(scan_q)
    if bracket is not None:
        print(f"\n  Entanglement sudden death (Yu-Eberly) onset:")
        print(f"    gamma_ESD ∈ [{bracket[0]:.3e}, {bracket[1]:.3e}] /s")
        print(f"    Above this threshold, C(t) ≡ 0 for all t in [0, T] —")
        print(f"    not asymptotic decay; the state becomes truly separable.")

    # ── geometry comparison: parallel vs perpendicular ───────────────
    print("\n  Geometry comparison (Bose 2017 nominal, T=2.5s):")
    print(f"    {'metric':<40}{'parallel':>14}{'perpendicular':>16}")
    print("    " + "-" * 70)
    print(f"    {'unitary peak C':<40}"
          f"{scan_q['max_concurrence'][0]:>14.4f}"
          f"{scan_q_perp['max_concurrence'][0]:>16.4f}")
    bracket_p = _esd_bracket(scan_q_perp)
    g_esd_par = bracket[1] if bracket else float('inf')
    g_esd_per = bracket_p[1] if bracket_p else float('inf')
    print(f"    {'gamma_ESD upper bound (1/s)':<40}"
          f"{g_esd_par:>14.3e}{g_esd_per:>16.3e}")
    g_par_001 = critical_gamma(scan_q, 0.01)
    g_per_001 = critical_gamma(scan_q_perp, 0.01)
    print(f"    {'gamma_crit at C=0.01 (1/s)':<40}"
          f"{g_par_001:>14.3e}{g_per_001:>16.3e}")
    print(f"    {'tau_coh required at C=0.01 (s)':<40}"
          f"{1.0/g_par_001:>14.2f}{1.0/g_per_001:>16.2f}")
    print("\n    Perpendicular gives ~2x larger budget because Delta phi is")
    print("    ~2x larger at the closer approach distance d=200 um (vs d=450 um")
    print("    in the parallel geometry where d > dX is required).")

    # write Tier 2 CSV (parallel + perpendicular side by side)
    budget_path = Path(__file__).parent / "bmv_coherence_budget.csv"
    with budget_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["gamma_per_s", "tau_coh_s",
                    "C_max_quantized_parallel", "N_max_quantized_parallel",
                    "t_at_peak_s_parallel",
                    "C_max_quantized_perpendicular",
                    "N_max_quantized_perpendicular",
                    "t_at_peak_s_perpendicular",
                    "C_max_RA", "N_max_RA"])
        for i in range(len(gamma_array)):
            g = gamma_array[i]
            tau = 1.0 / g if g > 0 else float("inf")
            w.writerow([
                f"{g:.6e}",
                f"{tau:.6e}",
                f"{scan_q['max_concurrence'][i]:.6e}",
                f"{scan_q['max_negativity'][i]:.6e}",
                f"{scan_q['t_at_peak_s'][i]:.6e}",
                f"{scan_q_perp['max_concurrence'][i]:.6e}",
                f"{scan_q_perp['max_negativity'][i]:.6e}",
                f"{scan_q_perp['t_at_peak_s'][i]:.6e}",
                f"{scan_ra['max_concurrence'][i]:.6e}",
                f"{scan_ra['max_negativity'][i]:.6e}",
            ])
    print(f"\n  Coherence-budget table written to: {budget_path}")

    # ── Tier 3: positional actualization rate from environment ────────
    print("\n" + "=" * 78)
    print("TIER 3 — POSITIONAL ACTUALIZATION RATE (bridge interpretation)")
    print("=" * 78)
    print("""\
RA reinterpretation: each environmental scattering event = one Step-4
actualization that records position info ⇒ lambda_pos = Gamma_decoh.
A native BDG-kernel derivation is open (tracked in RA-PRED-008 Tier 3b).
""")
    g_esd_par = bracket[1] if bracket else float("inf")

    scenarios = [
        ("Bose 2017 ideal (cryo UHV)",
         BMVEnvironment(pressure_Pa=1e-12, T_gas_K=0.1, T_blackbody_K=0.1)),
        ("Standard UHV at 4 K",
         BMVEnvironment(pressure_Pa=1e-10, T_gas_K=4.0, T_blackbody_K=4.0)),
        ("Standard UHV at 77 K (LN2)",
         BMVEnvironment(pressure_Pa=1e-9, T_gas_K=77.0, T_blackbody_K=77.0)),
        ("Room-temperature high vacuum",
         BMVEnvironment(pressure_Pa=1e-6, T_gas_K=300.0, T_blackbody_K=300.0)),
    ]
    print(f"  Bose 2017 nominal (parallel geometry), gamma_ESD <= {g_esd_par:.3e} /s")
    print(f"\n  {'Scenario':<32}{'lambda_pos':>14}{'margin':>14}{'coherent?':>12}")
    print("  " + "-" * 72)
    for name, env in scenarios:
        v = in_branch_coherent_regime(env, BOSE_2017, g_esd_par)
        margin = v["margin_factor"]
        margin_str = (f"{margin:.2e}x" if margin < 1e6 else "huge")
        verdict = "YES" if v["branch_coherent"] else "NO"
        print(f"  {name:<32}{v['lambda_pos_per_s']:>11.3e} /s"
              f"{margin_str:>14}{verdict:>12}")
    print("\n  Component breakdown (Bose 2017 ideal scenario):")
    rates = actualization_rate_from_environment(scenarios[0][1], BOSE_2017)
    print(f"    gas-collision rate     : {rates['gas']:.3e} /s")
    print(f"    blackbody-photon rate  : {rates['blackbody']:.3e} /s")
    print(f"    total lambda_pos       : {rates['total']:.3e} /s")
    print(f"    gamma_ESD margin       : {g_esd_par/rates['total']:.2e}x"
          if rates['total'] > 0 else "    gamma_ESD margin       : infinite")

    # falsification reminder
    print("\n" + "=" * 78)
    print("FALSIFICATION CONDITION (Tier 1 + Tier 2 + Tier 3)")
    print("=" * 78)
    g_crit_01 = critical_gamma(scan_q, 0.01)
    print("""\
Tier 1: a measured nonzero concurrence attributed to gravity (after
exclusion of nongravitational channels) falsifies the RA Step-2/Step-5
separation. At Bose 2017 nominal parameters with no decoherence the
quantized-gravity prediction is C ≈ {c_q:.3f} at T = {T:.2f}s.

Tier 2: the experiment can only discriminate models if the coherence
time tau_coh = 1/gamma is long enough to preserve a witnessable signal.
For an experimental sensitivity floor of C >= 0.01 the quantized-gravity
prediction requires gamma <= {g_crit:.3e} /s, i.e., tau_coh >= {tau_min:.3e} s.
A null result above this gamma threshold is decoherence-limited and
does NOT discriminate RA from quantized gravity.

Tier 3: in the bridge interpretation, lambda_pos = Gamma_decoh, so the
above gamma threshold is also the maximum tolerable RA Step-4 positional
actualization rate. For the Bose 2017 nominal protocol this requires
extreme cryogenic UHV conditions (pressure < 1e-11 Pa, T < ~1 K). At
standard cryogenic vacuum (4K, 1e-10 Pa) the gas-collision rate alone
already exceeds gamma_ESD. The native BDG-kernel derivation of
lambda_pos (Tier 3b) remains open.""".format(
        c_q=results["quantized"]["concurrence"][-1],
        T=BOSE_2017.T,
        g_crit=g_crit_01,
        tau_min=1.0 / g_crit_01 if g_crit_01 > 0 else float("inf"),
    ))


if __name__ == "__main__":
    main()
