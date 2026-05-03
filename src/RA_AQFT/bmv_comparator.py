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
) -> dict[str, np.ndarray]:
    """Compute (Delta phi, negativity, concurrence) over a time sweep."""
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
        rho = density_matrix(state_fn(p, t))
        out["negativity"][i] = negativity(rho)
        out["concurrence"][i] = concurrence(rho)
    return out


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

    # falsification reminder
    print("\n" + "=" * 78)
    print("FALSIFICATION CONDITION")
    print("=" * 78)
    print("""\
A measured nonzero concurrence (or negativity above the experimental floor)
attributed to gravity, after exclusion of all nongravitational channels,
falsifies the RA Step-2/Step-5 separation. The Bose 2017 nominal protocol
predicts (under quantized gravity) a concurrence of order
{:.3f} at T = {:.2f}s, giving the experiment in-principle discriminating
power against the RA-null floor.""".format(
        results["quantized"]["concurrence"][-1], BOSE_2017.T
    ))


if __name__ == "__main__":
    main()
