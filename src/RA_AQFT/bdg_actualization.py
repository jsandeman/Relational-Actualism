"""
bdg_actualization.py
Relational Actualism — BDG-kernel positional actualization rate (Tier 3b)

Derives the positional actualization rate lambda_pos directly from the
BDG acceptance kernel
        K(N | mu) = Poisson(N; lambda(mu)) * 𝟙[S(N)>0] / P_acc(mu)
rather than identifying lambda_pos with conventional decoherence rates
(the bridge interpretation used in Tier 3a). The BDG coefficient vector
c = (1, -1, 9, -16, 8) is shared with kernel_saturation.py and the Lean
file RA_BDG_Coefficient_Arithmetic.lean.

────────────────────────────────────────────────────────────────────────
SCOPE AND LIMITATIONS (read first)
────────────────────────────────────────────────────────────────────────
This is NOT a complete first-principles derivation. RA does not yet have
a closed mapping from continuum BMV parameters (m, dX, environmental
coupling) to the BDG kernel parameter mu — that requires the open
mass-emergence work (RA-MOTIF-* and RA-OPEN-* targets). What this
module DOES provide:

  1. The BDG-kernel filtered actualization rate as a function of two
     parameters: candidate-generation rate Gamma_cand (per second) and
     dimensionless kernel saturation parameter mu.
  2. The three regimes of the kernel (saturated / selective /
     strongly selective) and their physical interpretation.
  3. The bridge-interpretation limit (lambda_pos = Gamma_cand) as a
     special case in the saturated regime.
  4. A NEW prediction: in the strongly-selective regime, RA predicts
     SUPPRESSED positional decoherence relative to standard theory.

What's left open (RA-PRED-008 next_tasks 3b, 4):
  - First-principles determination of mu for a given BMV apparatus.
  - Lean formalization of the actualization-rate construction.
  - Cross-check against an alternative kernel parameterization (e.g.
    if mu is set by environmental temperature vs by dX vs by m).

Authors: Joshua F. Sandeman (framework); Claude/Anthropic (computation)
"""

from __future__ import annotations

from dataclasses import dataclass
from math import factorial, log
from pathlib import Path
import csv

import numpy as np

# ── BDG coefficients (shared with kernel_saturation.py and Lean) ──────
C_BDG: tuple[int, ...] = (1, -1, 9, -16, 8)  # c0, c1, c2, c3, c4 (d=4)


# ── Acceptance probability of the BDG filter ──────────────────────────
def bdg_acceptance_probability(
    mu: float,
    n_samples: int = 200_000,
    rng: np.random.Generator | None = None,
) -> float:
    """Monte Carlo estimate of P_acc(mu) = P(S>0 | candidate ~ Poisson-CSG(mu)).

    The Poisson-CSG sampling: for each interval depth k ∈ {1,2,3,4},
    draw N_k ~ Poisson(mu^(k+1)/(k+1)!), then S = c0 + sum_k c_k * N_k.
    P_acc is the empirical fraction with S > 0. Matches the construction
    in kernel_saturation.py exactly.
    """
    if rng is None:
        rng = np.random.default_rng(42)
    lam = [mu ** (k + 1) / factorial(k + 1) for k in range(4)]
    S_vals = np.full(n_samples, C_BDG[0], dtype=float)
    for k in range(4):
        N_k = rng.poisson(lam[k], n_samples)
        S_vals += C_BDG[k + 1] * N_k
    return float(np.mean(S_vals > 0))


def kernel_regime(mu: float, p_acc: float | None = None) -> str:
    """Classify the kernel regime at given mu.

    Thresholds match kernel_saturation.py's nomenclature (D_KL = -log P_acc,
    TV = 1 - P_acc):

    'saturated'          : P_acc > 0.99   (TV < 0.01; bridge interpretation)
    'near_saturation'    : 0.9 < P_acc    (TV < 0.10)
    'gentle'             : 0.67 < P_acc   (D_KL < 0.4; mild filtering)
    'selective'          : 0.449 < P_acc  (D_KL > 0.4; non-trivial filtering)
    'strongly_selective' : P_acc <= 0.449 (D_KL > 0.8; RA predicts ~2x
                                           or stronger suppression vs bridge)

    Note that P_acc is NOT monotone in mu: it has a selective minimum
    around mu ~ 3-5 (P_acc ~ 0.4) before climbing to 1.0 in saturation
    (mu >> 5). Both small-mu and large-mu limits give P_acc → 1; the
    BDG filter actively suppresses only at intermediate mu.
    """
    if p_acc is None:
        p_acc = bdg_acceptance_probability(mu)
    if p_acc > 0.99:
        return "saturated"
    if p_acc > 0.9:
        return "near_saturation"
    if p_acc > 0.670:
        return "gentle"
    if p_acc > 0.449:
        return "selective"
    return "strongly_selective"


# ── Tier 3b actualization rate ────────────────────────────────────────
@dataclass(frozen=True)
class BDGActualizationResult:
    """Result of evaluating the BDG-filtered actualization rate."""
    gamma_cand_per_s: float       # input candidate-generation rate
    mu: float                     # input dimensionless kernel parameter
    p_acc: float                  # BDG acceptance probability at mu
    lambda_pos_per_s: float       # filtered rate = Gamma_cand * P_acc
    regime: str                   # one of: saturated, near_saturation, ...
    bridge_ratio: float           # lambda_pos / Gamma_cand (= P_acc)


def actualization_rate(
    gamma_cand_per_s: float,
    mu: float,
    n_samples: int = 200_000,
) -> BDGActualizationResult:
    """BDG-kernel-filtered positional actualization rate.

    lambda_pos = Gamma_cand * P_acc(mu)

    Interpretation: the environment generates candidate Step-4 events
    at rate Gamma_cand. The BDG action filter S>0 accepts fraction
    P_acc(mu). The accepted events are Step-4 actualizations.
    """
    p = bdg_acceptance_probability(mu, n_samples=n_samples)
    return BDGActualizationResult(
        gamma_cand_per_s=gamma_cand_per_s,
        mu=mu,
        p_acc=p,
        lambda_pos_per_s=gamma_cand_per_s * p,
        regime=kernel_regime(mu, p_acc=p),
        bridge_ratio=p,
    )


def bridge_interpretation_rate(gamma_decoh_per_s: float) -> float:
    """The Tier 3a bridge: lambda_pos = Gamma_decoh.

    Equivalent to actualization_rate(Gamma_decoh, mu→∞) via the
    saturation theorem (P_acc → 1). Provided for explicit comparison.
    """
    return gamma_decoh_per_s


# ── RA-native prediction window ───────────────────────────────────────
def critical_mu_for_branch_coherent(
    gamma_cand_per_s: float,
    gamma_esd_per_s: float,
    mu_search_range: tuple[float, float] = (0.01, 100.0),
    n_pts: int = 200,
    n_samples: int = 100_000,
) -> dict[str, float]:
    """Find the largest mu at which lambda_pos = Gamma_cand * P_acc(mu)
    still falls below gamma_esd (i.e., the BDG kernel keeps the system
    in the branch-coherent regime even though the candidate-generation
    rate exceeds gamma_esd).

    If gamma_cand <= gamma_esd, returns mu = +inf (any mu works).
    If even at mu→0, gamma_cand * P_acc < gamma_esd is impossible to
    satisfy (e.g. at mu=0, P_acc(0)=1 since S=c0=1>0 trivially), the
    function returns mu = 0 with rate = gamma_cand.

    This is the RA-specific testable window: for a given environmental
    coupling, RA predicts the kernel can suppress decoherence below the
    standard-theory rate by a factor 1/P_acc(mu).
    """
    if gamma_cand_per_s <= gamma_esd_per_s:
        return {
            "mu_critical": float("inf"),
            "p_acc_critical": 1.0,
            "lambda_pos_critical": gamma_cand_per_s,
            "suppression_factor": 1.0,
            "branch_coherent_achievable": True,
        }
    p_acc_target = gamma_esd_per_s / gamma_cand_per_s
    mu_array = np.geomspace(mu_search_range[0], mu_search_range[1], n_pts)
    rng = np.random.default_rng(42)
    p_array = np.array([
        bdg_acceptance_probability(float(m), n_samples=n_samples, rng=rng)
        for m in mu_array
    ])
    # find the LARGEST mu where P_acc <= p_acc_target
    below = p_array <= p_acc_target
    if not below.any():
        # even the smallest mu has P_acc > target — i.e. branch-coherent
        # regime is unachievable (kernel cannot suppress enough)
        return {
            "mu_critical": 0.0,
            "p_acc_critical": float(p_array[0]),
            "lambda_pos_critical": gamma_cand_per_s * float(p_array[0]),
            "suppression_factor": 1.0 / float(p_array[0]),
            "branch_coherent_achievable": False,
        }
    if below.all():
        # all mu in range satisfy the bound; return the largest
        i = len(mu_array) - 1
    else:
        # find the boundary
        i = int(np.argmax(~below)) - 1
        if i < 0:
            i = 0
    mu_c = float(mu_array[i])
    p_c = float(p_array[i])
    return {
        "mu_critical": mu_c,
        "p_acc_critical": p_c,
        "lambda_pos_critical": gamma_cand_per_s * p_c,
        "suppression_factor": 1.0 / p_c if p_c > 0 else float("inf"),
        "branch_coherent_achievable": True,
    }


# ── Main: regime characterization ─────────────────────────────────────
def main() -> None:
    print("=" * 78)
    print("BDG ACTUALIZATION RATE — Tier 3b")
    print("=" * 78)
    print(f"  BDG coefficients (d=4): c = {C_BDG}")
    print(f"  Kernel: K(N|mu) = Poisson(N; lambda(mu)) * indicator[S>0] / P_acc(mu)")
    print(f"  Filtered rate: lambda_pos = Gamma_cand * P_acc(mu)")

    # 1. Regime table
    print("\n" + "-" * 78)
    print("Kernel regime as a function of mu (Monte Carlo, N=200k samples):")
    print("-" * 78)
    print(f"  {'mu':>6}  {'P_acc':>8}  {'1/P_acc':>10}  {'regime':>22}")
    print("  " + "-" * 50)
    rows = []
    rng = np.random.default_rng(42)
    for mu in [0.1, 0.3, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 20.0, 50.0]:
        p = bdg_acceptance_probability(mu, rng=rng)
        regime = kernel_regime(mu, p_acc=p)
        suppression = 1.0 / p if p > 0 else float("inf")
        print(f"  {mu:>6.1f}  {p:>8.4f}  {suppression:>10.3f}  {regime:>22}")
        rows.append((mu, p, suppression, regime))

    # 2. Bridge limit recovery
    print("\n" + "-" * 78)
    print("Bridge-limit recovery (Tier 3a as a special case of Tier 3b):")
    print("-" * 78)
    p_sat = bdg_acceptance_probability(50.0, rng=rng)
    print(f"  At mu = 50.0:  P_acc ≈ {p_sat:.4f}, suppression factor ≈ {1/p_sat:.3f}")
    print(f"  → lambda_pos / Gamma_cand = {p_sat:.4f} ≈ 1.0  (bridge holds)")
    p_sel = bdg_acceptance_probability(1.0, rng=rng)
    print(f"  At mu =  1.0:  P_acc ≈ {p_sel:.4f}, suppression factor ≈ {1/p_sel:.3f}")
    print(f"  → lambda_pos / Gamma_cand = {p_sel:.4f}  (bridge UNDER-PREDICTS lambda_pos by 1/{p_sel:.2f}x)")
    p_strict = bdg_acceptance_probability(3.0, rng=rng)
    print(f"  At mu =  3.0:  P_acc ≈ {p_strict:.4f}, suppression factor ≈ {1/p_strict:.3f}")
    print(f"  → lambda_pos / Gamma_cand = {p_strict:.4f}  (RA suppresses decoherence by ~{1/p_strict:.1f}x)")
    print(f"  Note: the selective minimum sits around mu ~ 3-5 with P_acc ~ 0.4.")
    print(f"  Both mu << 1 and mu >> 5 give P_acc → 1 (no BDG suppression).")

    # 3. BMV-relevant prediction window
    print("\n" + "-" * 78)
    print("BMV branch-coherent regime via BDG suppression (Bose 2017 nominal):")
    print("-" * 78)
    print("  Tier 2 result: gamma_ESD ~ 0.06 /s")
    print("  Tier 3a result: Gamma_decoh ~ 1.2e6 /s at idealized cryo UHV")
    print("  ⇒ bridge ratio Gamma_decoh / gamma_ESD ~ 2e7")
    print("\n  For RA to keep the system in the branch-coherent regime via the")
    print("  BDG suppression alone, we need P_acc <= gamma_ESD / Gamma_cand ~ 5e-8")
    print("  This is FAR below P_acc(mu) for any positive mu in our tabulation;")
    print("  P_acc(mu→0) → 1 since S = c0 = 1 > 0 trivially with no candidates.")
    print("  Therefore the BDG kernel CANNOT alone rescue the BMV protocol at")
    print("  the Bose 2017 mass scale; smaller candidate-generation rates")
    print("  (i.e. better isolation, smaller test mass) are still required.")

    # 4. Comparison to bridge interpretation
    print("\n" + "-" * 78)
    print("Tier 3a (bridge) vs Tier 3b (BDG-filtered) — a worked example:")
    print("-" * 78)
    print(f"  Suppose Gamma_cand = 100 /s (a hypothetical cleaner BMV apparatus).")
    for mu in [0.5, 1.0, 2.0, 4.0, 10.0]:
        r = actualization_rate(100.0, mu, n_samples=200_000)
        print(f"    mu = {mu:>4.1f}: lambda_pos = {r.lambda_pos_per_s:>7.2f} /s "
              f"({r.regime}, suppression {1/r.p_acc:.2f}x)")
    print("  → In the strongly-selective regime, RA predicts ~2-2.5x SLOWER")
    print("    positional decoherence than standard theory. This is a NEW")
    print("    (modest) testable signal independent of the BMV null prediction;")
    print("    the suppression is bounded above because P_acc never falls")
    print("    below ~0.4 in the d=4 BDG kernel — the Yu-Eberly-style sharp")
    print("    suppression seen in Tier 2's ESD does NOT recur here.")

    # 5. Write results CSV
    out_path = Path(__file__).parent / "bdg_actualization_regimes.csv"
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["mu", "P_acc", "suppression_factor", "regime"])
        for row in rows:
            w.writerow([f"{row[0]:.4f}", f"{row[1]:.6f}",
                        f"{row[2]:.6f}", row[3]])
    print(f"\n  Regime table written to: {out_path}")

    # 6. What's still open
    print("\n" + "=" * 78)
    print("WHAT'S OPEN (Tier 3b boundary)")
    print("=" * 78)
    print("""\
The BDG-filtered actualization rate lambda_pos = Gamma_cand * P_acc(mu)
is a parametric prediction with ONE free parameter (mu) once Gamma_cand
is given. To pin mu down from first principles, RA needs:

  1. A graph-patch model of a massive test particle (open: mass-emergence
     work, RA-MOTIF-* and Causal Firewall claims).
  2. A dictionary mapping (m, dX, environmental coupling) to the BDG
     candidate-generation parameters.
  3. A justification for whether mu is set by environmental coupling rate,
     test-mass internal complexity, dX in graph units, or a combination.

Until these are specified, Tier 3b's value is structural: it identifies
the saturation threshold mu_crit ~ 5 below which RA predicts suppressed
decoherence relative to standard theory, and provides the explicit
numerical relationship lambda_pos / Gamma_cand = P_acc(mu) for any mu.

Tier 3b is therefore (a) a working RA-native rate calculator that recovers
the bridge interpretation in its appropriate regime, and (b) an explicit
catalog of the open parameter space where RA could in principle make
predictions distinct from standard decoherence theory.""")


if __name__ == "__main__":
    main()
