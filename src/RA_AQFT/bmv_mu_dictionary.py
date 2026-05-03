"""
bmv_mu_dictionary.py
Relational Actualism — BMV μ-dictionary catalog (Tier 3b closure, partial)

Catalogs candidate identifications of the BDG kernel parameter μ for a
test mass in the BMV apparatus, and computes the actualization-rate
prediction under each. Each identification (each "dictionary") is a
proposed mapping
        μ_dict(m, dX, env, ...) : ℝ≥0
that takes the experimental scenario to a dimensionless kernel parameter.
The Tier 3b filtered actualization rate then reads
        λ_pos = Γ_cand · P_acc(μ_dict)
and the bridge interpretation (Tier 3a, Γ_cand = Γ_decoh = standard
decoherence rate) gives a numerical prediction per dictionary.

────────────────────────────────────────────────────────────────────────
SCOPE — WHAT THIS DOES, WHAT IT DOES NOT
────────────────────────────────────────────────────────────────────────
- DOES: enumerate five candidate dictionaries with explicit assumptions;
        compute the BMV-relevant μ for each; report the BDG suppression
        factor each predicts.
- DOES: identify the empirically-distinguishable regime — under which
        dictionary, if any, does the BDG suppression deviate from 1
        (i.e. saturate strongly enough to matter)?
- DOES NOT: derive μ from RA principles. That requires closing
            RA-OPEN-MU-ESTIMATOR-001 ("Define μ_RA from normal-form
            frontier/closure data") and is downstream of the
            mass-emergence work (RA-MOTIF-* and Causal Firewall claims).
- DOES NOT: claim any dictionary is RA-native. Each is labeled with
            its provenance and explicit assumption set.

Authors: Joshua F. Sandeman (framework); Claude/Anthropic (computation)
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log
from pathlib import Path
import csv

from bmv_comparator import (
    BMVEnvironment,
    BMVParams,
    actualization_rate_from_environment,
)
from bdg_actualization import (
    bdg_acceptance_probability,
    kernel_regime,
)


# ── Reference parameters ──────────────────────────────────────────────
BOSE_2017 = BMVParams(m=1e-14, dX=250e-6, d=450e-6, T=2.5)
ENV_BOSE_IDEAL = BMVEnvironment(pressure_Pa=1e-12, T_gas_K=0.1, T_blackbody_K=0.1)

# Physical constants (SI)
PLANCK_LENGTH_M = 1.616255e-35   # m
PLANCK_TIME_S = 5.391247e-44     # s
ATOMIC_MASS_UNIT_KG = 1.66053907e-27  # kg


# ── Dictionary catalog ────────────────────────────────────────────────
@dataclass(frozen=True)
class MuDictionary:
    """A candidate identification μ(m, dX, env, ...). Each instance
    carries its name, a one-line provenance / motivating assumption,
    and a callable that computes μ from the BMV scenario."""
    name: str
    provenance: str
    assumption: str
    fn: callable

    def evaluate(self, p: BMVParams, env: BMVEnvironment) -> float:
        return float(self.fn(p, env))


# Dictionary A: μ proportional to environmental candidate-generation rate
# per Planck time. The "every Planck tick is a candidate" assumption.
def _dict_A_env_planck(p: BMVParams, env: BMVEnvironment) -> float:
    rates = actualization_rate_from_environment(env, p)
    return rates["total"] * PLANCK_TIME_S


# Dictionary B: μ proportional to the number of atoms in the test mass
# (test-mass internal complexity).
def _dict_B_atom_count(p: BMVParams, env: BMVEnvironment) -> float:
    # an atom is ~1 amu; this is order-of-magnitude
    return p.m / ATOMIC_MASS_UNIT_KG


# Dictionary C: μ scales as (dX / Planck length)^d for d = 4.
# Geometric / dimensionality argument.
def _dict_C_geometric(p: BMVParams, env: BMVEnvironment) -> float:
    return (p.dX / PLANCK_LENGTH_M) ** 4


# Dictionary D: μ is a fixed point of the kernel structure, μ ≈ d = 4.
# A kernel-native conjecture: the "natural" μ is the dimensionality.
def _dict_D_dimensionality(p: BMVParams, env: BMVEnvironment) -> float:
    return 4.0


# Dictionary E: μ scales as log(m / m_Planck), a "running" identification.
# Motivated by analogy with running couplings in QFT (cartographic, not
# RA-native).
def _dict_E_log_mass_ratio(p: BMVParams, env: BMVEnvironment) -> float:
    m_planck_kg = 2.176434e-8  # kg
    ratio = p.m / m_planck_kg
    if ratio <= 0:
        return 0.0
    return abs(log(ratio))


CATALOG: list[MuDictionary] = [
    MuDictionary(
        name="A_env_planck",
        provenance="conjecture",
        assumption=("μ = Γ_env × τ_Planck. Assumes every environmental "
                    "scattering event is a BDG candidate at the Planck scale."),
        fn=_dict_A_env_planck,
    ),
    MuDictionary(
        name="B_atom_count",
        provenance="conjecture",
        assumption=("μ = N_atoms = m / m_atomic. Identifies kernel "
                    "candidates with internal degrees of freedom."),
        fn=_dict_B_atom_count,
    ),
    MuDictionary(
        name="C_geometric",
        provenance="conjecture",
        assumption=("μ = (dX / l_Planck)^d for d = 4. Geometric "
                    "identification using the Planck length."),
        fn=_dict_C_geometric,
    ),
    MuDictionary(
        name="D_dimensionality",
        provenance="kernel-structural conjecture",
        assumption=("μ = d = 4. The 'natural' μ is the dimensionality, "
                    "placing the kernel structurally at the selective "
                    "minimum P_acc ~ 0.4 universally. RA-leaning but not "
                    "derived from any RA-MOTIF-* or RA-LLC-* claim."),
        fn=_dict_D_dimensionality,
    ),
    MuDictionary(
        name="E_log_mass_ratio",
        provenance="cartographic (QFT-analogy)",
        assumption=("μ = |log(m / m_Planck)|. Borrowed from QFT running-"
                    "coupling analogies; not RA-native, included for "
                    "comparison only."),
        fn=_dict_E_log_mass_ratio,
    ),
]


# ── Per-dictionary BMV prediction ─────────────────────────────────────
@dataclass(frozen=True)
class DictionaryPrediction:
    name: str
    mu: float
    p_acc: float
    suppression_factor: float
    regime: str
    lambda_pos_per_s: float
    bridge_lambda_pos_per_s: float
    deviates_from_bridge: bool


def predict(
    d: MuDictionary,
    p: BMVParams,
    env: BMVEnvironment,
    n_samples: int = 50_000,
    saturation_cutoff: float = 50.0,
) -> DictionaryPrediction:
    """Compute the BMV-prediction for a candidate μ-dictionary.

    For μ above `saturation_cutoff` we short-circuit using the kernel
    saturation theorem (proved in kernel_saturation.py): P_acc(μ) ≥ 1 −
    24/μ⁴ via the Chebyshev bound, so P_acc ≥ 0.999996 at μ = 50.
    Direct Monte Carlo at extreme μ is numerically infeasible because
    λ_k = μ^(k+1)/(k+1)! overflows NumPy's Poisson sampler.
    """
    mu = d.evaluate(p, env)
    rates = actualization_rate_from_environment(env, p)
    gamma_cand = rates["total"]
    if mu >= saturation_cutoff:
        p_acc = 1.0
    else:
        p_acc = bdg_acceptance_probability(mu, n_samples=n_samples)
    return DictionaryPrediction(
        name=d.name,
        mu=mu,
        p_acc=p_acc,
        suppression_factor=(1.0 / p_acc if p_acc > 0 else float("inf")),
        regime=kernel_regime(mu, p_acc=p_acc),
        lambda_pos_per_s=gamma_cand * p_acc,
        bridge_lambda_pos_per_s=gamma_cand,
        deviates_from_bridge=(p_acc < 0.99),
    )


# ── Main: BMV catalog ─────────────────────────────────────────────────
def main() -> None:
    print("=" * 78)
    print("BMV μ-DICTIONARY CATALOG — Tier 3b closure (partial)")
    print("=" * 78)
    print("""\
Five candidate identifications of the BDG kernel parameter μ for the
BMV apparatus. Each gives a different prediction for the BDG-filtered
actualization rate. Tier 3b closure requires picking one (or proving
that another identification is correct), which is the open work of
RA-OPEN-MU-ESTIMATOR-001 plus mass-emergence (RA-MOTIF-* and
Causal Firewall).
""")
    print("Reference scenario: Bose 2017 nominal at idealized cryo UHV")
    print(f"  m  = {BOSE_2017.m:.0e} kg")
    print(f"  dX = {BOSE_2017.dX*1e6:.0f} μm")
    print(f"  P  = {ENV_BOSE_IDEAL.pressure_Pa:.0e} Pa, T_gas = {ENV_BOSE_IDEAL.T_gas_K:.2f} K")

    rates_ref = actualization_rate_from_environment(ENV_BOSE_IDEAL, BOSE_2017)
    print(f"  ⇒ Γ_cand (Tier 3a bridge rate) = {rates_ref['total']:.3e} /s")

    print("\n" + "-" * 78)
    print("Per-dictionary BMV predictions:")
    print("-" * 78)
    print(f"  {'dict':<20}{'μ':>13}{'P_acc':>10}{'1/P_acc':>10}"
          f"{'regime':>22}")
    print("  " + "-" * 75)
    predictions = []
    for d in CATALOG:
        pred = predict(d, BOSE_2017, ENV_BOSE_IDEAL)
        predictions.append((d, pred))
        # format huge mu values cleanly
        mu_str = (f"{pred.mu:>13.3e}" if pred.mu > 1e6 or pred.mu < 1e-3
                  else f"{pred.mu:>13.3f}")
        print(f"  {d.name:<20}{mu_str}{pred.p_acc:>10.4f}"
              f"{pred.suppression_factor:>10.3f}{pred.regime:>22}")

    print("\n  Provenance labels:")
    for d in CATALOG:
        print(f"    {d.name:<20}  {d.provenance}")

    # 1. which dictionaries deviate from bridge?
    print("\n" + "-" * 78)
    print("Which dictionaries deviate from the Tier 3a bridge limit?")
    print("-" * 78)
    deviating = [d for d, p in predictions if p.deviates_from_bridge]
    saturating = [d for d, p in predictions if not p.deviates_from_bridge]
    print(f"  In the saturated regime (P_acc > 0.99, bridge holds):")
    for d in saturating:
        print(f"    • {d.name}")
    print(f"\n  Deviating from bridge (BDG suppression matters):")
    if not deviating:
        print(f"    • [none — all dictionaries give saturation in the BMV regime]")
    for d in deviating:
        pred = next(p for dx, p in predictions if dx is d)
        print(f"    • {d.name}: 1/P_acc = {pred.suppression_factor:.2f}x")

    # 2. predicted lambda_pos comparison
    print("\n" + "-" * 78)
    print("Predicted positional actualization rate λ_pos (per second):")
    print("-" * 78)
    print(f"  Tier 3a bridge prediction (saturation limit): {rates_ref['total']:.3e} /s")
    for d, pred in predictions:
        ratio = pred.lambda_pos_per_s / rates_ref['total']
        print(f"  {d.name:<20} : {pred.lambda_pos_per_s:.3e} /s  "
              f"(ratio to bridge: {ratio:.4f})")

    # 3. write CSV
    out_path = Path(__file__).parent / "bmv_mu_dictionary_predictions.csv"
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["dictionary", "provenance", "mu", "P_acc",
                    "suppression_factor", "regime", "lambda_pos_per_s",
                    "bridge_lambda_pos_per_s", "deviates_from_bridge"])
        for d, pred in predictions:
            w.writerow([
                d.name, d.provenance,
                f"{pred.mu:.6e}", f"{pred.p_acc:.6f}",
                f"{pred.suppression_factor:.6f}", pred.regime,
                f"{pred.lambda_pos_per_s:.6e}",
                f"{pred.bridge_lambda_pos_per_s:.6e}",
                int(pred.deviates_from_bridge),
            ])
    print(f"\n  Predictions CSV written to: {out_path}")

    # 4. summary
    print("\n" + "=" * 78)
    print("WHAT TIER 3b CLOSURE ACTUALLY NEEDS")
    print("=" * 78)
    print("""\
Of the five cataloged dictionaries:
  • A, B, C, E all push μ to extreme values (>> 5 or << 0.01) for
    macroscopic test masses, landing the kernel firmly in the saturated
    regime. Under any of these, the Tier 3a bridge interpretation
    (λ_pos = Γ_decoh) is exactly recovered and BDG suppression has no
    operational consequence.
  • D (μ = d = 4) is the ONLY dictionary that places the kernel in the
    strongly-selective regime universally, predicting a constant ~2.5x
    BDG suppression of positional decoherence relative to standard
    theory. This would be a NEW testable signal — but it is a
    kernel-structural conjecture, not derived from the existing
    RA-MOTIF-* or RA-LLC-* claims.

The Tier 3b closure question is therefore:

  Does any RA principle pick out one of {A, B, C, D, E}, or some other
  dictionary, as the correct identification of μ for a macroscopic test
  mass?

This is downstream of the open issues:
  • RA-OPEN-MU-ESTIMATOR-001  (Define μ_RA from frontier/closure data)
  • RA-OPEN-ACTUALIZATION-SELECTOR-001
  • RA-OPEN-GROWTH-MEASURE-001
  • Mass emergence (RA-MOTIF-001..009 and Causal Firewall claims)

Without those, μ for BMV remains parametric. With dictionary D the
prediction window opens; with the others it does not.""")


if __name__ == "__main__":
    main()
