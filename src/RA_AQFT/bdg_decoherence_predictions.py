"""
bdg_decoherence_predictions.py
Relational Actualism — BDG-suppression predictions across the
positional-decoherence experimental landscape.

Tier 3b mass-emergence work (bmv_mu_dictionary.py) identified that
under Dictionary D (μ = d = 4, kernel-structural conjecture), RA
predicts a universal ~2.5x suppression of positional decoherence
relative to standard theory. This module:

  1. Catalogs representative positional-decoherence experiments
     spanning ~10 orders of magnitude in mass (atom interferometry
     through BMV-scale levitated diamond).
  2. Computes the standard-theory prediction Γ_standard for each
     using the Tier 3a gas + blackbody formulas.
  3. Computes the RA-conjectured Γ_RA(μ) for several μ values, with
     emphasis on Dictionary D's μ = 4 prediction.
  4. Compares to typical experimental measurement precision (~10–20%
     for mature systems, ~50% for poorly-characterized systems) to
     assess where Dictionary D would already be in tension with data.

────────────────────────────────────────────────────────────────────────
HONEST SCOPE — WHAT THIS DOES NOT DO
────────────────────────────────────────────────────────────────────────
- Does NOT consult primary experimental literature for measured
  decoherence rates. Standard-theory predictions are computed from
  first principles using documented order-of-magnitude formulas.
- The simplified gas cross-section sigma = pi * dX^2 from Tier 3a
  (bmv_comparator.gas_collision_rate) is appropriate when dX is much
  larger than the thermal de Broglie wavelength of background gas
  molecules — true for the BMV regime (dX ~ 250 um) but a significant
  OVER-ESTIMATE for atom/molecular interferometry (where the relevant
  cross-section is the atomic / molecular geometric cross-section
  ~1e-19 m^2, much smaller than pi * dX^2). The absolute Gamma_standard
  values for atom/molecular IF entries below are therefore unphysical;
  what is reliable is the SUPPRESSION FACTOR Gamma_std / Gamma_RA,
  which under Dictionary D is universally ~2.5x INDEPENDENT of how
  Gamma_std is computed. The verdict on Dictionary D rests on this
  suppression factor vs. measurement precision, not on absolute rates.
- Does NOT settle which decoherence channels the BDG filter applies
  to. The simplest assumption (filter applies to ALL positional
  scattering events uniformly) gives the strongest empirical
  constraint; under more refined assumptions (filter applies only
  to multi-vertex motif transitions, etc.) the constraint weakens.
- Does NOT close RA-OPEN-BMV-MU-DICTIONARY-001 — only provides
  empirical constraints on which candidate dictionaries are
  consistent with existing data under simplest interpretation.

Authors: Joshua F. Sandeman (framework); Claude/Anthropic (computation)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from bmv_comparator import (
    BMVEnvironment,
    BMVParams,
    actualization_rate_from_environment,
)
from bdg_actualization import bdg_acceptance_probability


# ── Experimental scenario templates ───────────────────────────────────
@dataclass(frozen=True)
class DecoherenceScenario:
    """Representative parameters for a positional-decoherence experiment.

    `measurement_precision_factor` is the rough fractional uncertainty
    on Γ_decoh in mature instances of this experimental class, used to
    judge whether a predicted RA suppression would be empirically
    detectable. E.g., 0.1 means Γ is known to ±10%.
    """
    name: str
    description: str
    m: float                                 # test mass (kg)
    dX: float                                # superposition splitting (m)
    pressure_Pa: float                       # background gas pressure (Pa)
    T_gas_K: float                           # gas/wall temperature (K)
    T_blackbody_K: float                     # blackbody temperature (K)
    measurement_precision_factor: float
    field_maturity: str                      # 'mature', 'developing', 'speculative'

    def to_params(self) -> BMVParams:
        return BMVParams(m=self.m, dX=self.dX, d=max(self.dX * 2, self.dX + 1e-12),
                         T=1.0, geometry="parallel")

    def to_environment(self) -> BMVEnvironment:
        return BMVEnvironment(
            pressure_Pa=self.pressure_Pa,
            T_gas_K=self.T_gas_K,
            T_blackbody_K=self.T_blackbody_K,
        )


# Representative parameter points across the experimental landscape.
# Numbers are order-of-magnitude representative, not specific to any
# single experimental run.
SCENARIOS: list[DecoherenceScenario] = [
    DecoherenceScenario(
        name="atom_interferometry_Cs",
        description="Cs atom interferometry (cold-atom, room-T vacuum)",
        m=2.2e-25,            # Cs atom mass
        dX=1e-3,              # mm-scale arm separation (typical)
        pressure_Pa=1e-9,     # standard UHV
        T_gas_K=300.0,
        T_blackbody_K=300.0,
        measurement_precision_factor=0.1,  # decoherence well-characterized
        field_maturity="mature",
    ),
    DecoherenceScenario(
        name="molecular_interferometry_C60",
        description="C60 fullerene interferometry (Arndt et al. style)",
        m=1.2e-24,            # C60 mass
        dX=1e-7,              # 100 nm grating pitch order
        pressure_Pa=1e-7,
        T_gas_K=300.0,
        T_blackbody_K=900.0,  # hot source
        measurement_precision_factor=0.2,
        field_maturity="mature",
    ),
    DecoherenceScenario(
        name="molecular_interferometry_oligoporphyrin",
        description="Large-molecule (~10 kDa) interferometry",
        m=1.6e-23,            # ~10000 amu
        dX=1e-7,
        pressure_Pa=1e-9,
        T_gas_K=300.0,
        T_blackbody_K=300.0,
        measurement_precision_factor=0.2,
        field_maturity="mature",
    ),
    DecoherenceScenario(
        name="levitated_nanosphere_silica",
        description="Levitated silica nanosphere (~100 nm radius)",
        m=1e-18,              # ~100 nm silica sphere
        dX=1e-9,              # nm-scale superposition (proposed)
        pressure_Pa=1e-10,
        T_gas_K=4.0,          # cryogenic
        T_blackbody_K=4.0,
        measurement_precision_factor=0.3,
        field_maturity="developing",
    ),
    DecoherenceScenario(
        name="bmv_bose2017_nominal",
        description="BMV Bose 2017 nominal (m=1e-14 kg, dX=250 um)",
        m=1e-14,
        dX=250e-6,
        pressure_Pa=1e-12,
        T_gas_K=0.1,
        T_blackbody_K=0.1,
        measurement_precision_factor=1.0,  # not yet measured
        field_maturity="speculative",
    ),
]


# ── Predictions per scenario ──────────────────────────────────────────
@dataclass(frozen=True)
class ScenarioPrediction:
    name: str
    field_maturity: str
    gamma_standard_per_s: float
    gamma_RA_dict_D_per_s: float            # at μ = 4
    suppression_factor: float                # = Γ_std / Γ_RA
    measurement_precision_factor: float
    detectability_ratio: float              # suppression / measurement_precision
    distinguishable: bool                   # can the experiment see the suppression?
    in_tension_with_data: bool              # is dict D ruled out by this scenario?


def predict_scenario(s: DecoherenceScenario, mu: float = 4.0) -> ScenarioPrediction:
    """Compute standard and RA-conjectured decoherence rates for a
    scenario, plus a verdict on whether dictionary D is in tension
    with that scenario's existing data."""
    rates = actualization_rate_from_environment(s.to_environment(), s.to_params())
    gamma_std = rates["total"]
    p_acc = bdg_acceptance_probability(mu, n_samples=50_000)
    gamma_RA = gamma_std * p_acc
    suppression = (gamma_std / gamma_RA) if gamma_RA > 0 else float("inf")
    # detectability: is the suppression bigger than the measurement uncertainty?
    detectability = suppression / (1.0 + s.measurement_precision_factor)
    distinguishable = detectability > 1.0 and s.field_maturity != "speculative"
    in_tension = (s.field_maturity == "mature" and
                  suppression > (1.0 + 2.0 * s.measurement_precision_factor))
    return ScenarioPrediction(
        name=s.name,
        field_maturity=s.field_maturity,
        gamma_standard_per_s=gamma_std,
        gamma_RA_dict_D_per_s=gamma_RA,
        suppression_factor=suppression,
        measurement_precision_factor=s.measurement_precision_factor,
        detectability_ratio=detectability,
        distinguishable=distinguishable,
        in_tension_with_data=in_tension,
    )


# ── Main: scan and verdict ────────────────────────────────────────────
def main() -> None:
    print("=" * 78)
    print("BDG SUPPRESSION ACROSS THE DECOHERENCE LANDSCAPE")
    print("=" * 78)
    print("""\
Under Dictionary D (μ = d = 4), RA predicts a universal ~2.5x
suppression of positional decoherence vs standard theory. This module
computes the standard prediction for representative experimental
scenarios and asks: would Dictionary D already be in tension with
existing precision data?
""")

    # NOTE: Gamma_standard values shown are from the simplified
    # geometric formula (sigma = pi * dX^2) and OVER-ESTIMATE the
    # actual measurement-relevant Gamma for atom/molecular IF (where
    # the proper cross-section is ~1e-19 m^2, not pi * dX^2). What
    # matters for the Dict-D verdict is the SUPPRESSION FACTOR vs.
    # measurement precision — that is independent of how Gamma_std is
    # computed and is the column to read.
    print(f"\n  {'scenario':<38}{'suppr.':>9}{'meas±':>8}"
          f"{'verdict':>14}    Γ_std (model, 1/s)")
    print("  " + "-" * 95)
    predictions = []
    for s in SCENARIOS:
        p = predict_scenario(s)
        predictions.append((s, p))
        verdict = ("TENSION" if p.in_tension_with_data
                   else "distinguishable" if p.distinguishable
                   else "not testable")
        print(f"  {s.name:<38}{p.suppression_factor:>9.2f}"
              f"{p.measurement_precision_factor:>7.0%}{verdict:>14}    "
              f"{p.gamma_standard_per_s:.2e}")

    print(f"\n  Verdict legend:")
    print(f"    TENSION         — mature field; suppression > 2σ measurement; "
          f"Dict. D in tension with existing data")
    print(f"    distinguishable — measurable in principle but not yet "
          f"high-precision-tested in this regime")
    print(f"    not testable    — speculative experimental regime "
          f"(BMV-scale; no measurements yet)")

    # how many in tension?
    n_tension = sum(1 for _, p in predictions if p.in_tension_with_data)
    n_distinguishable = sum(1 for _, p in predictions if p.distinguishable)
    n_not_testable = sum(1 for _, p in predictions if not p.distinguishable
                         and not p.in_tension_with_data)
    print(f"\n  Summary across {len(predictions)} scenarios:")
    print(f"    in tension with existing data : {n_tension}")
    print(f"    distinguishable (untested)    : {n_distinguishable}")
    print(f"    not testable (speculative)    : {n_not_testable}")

    # CSV
    out_path = Path(__file__).parent / "bdg_decoherence_predictions.csv"
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scenario", "description", "field_maturity",
                    "m_kg", "dX_m", "pressure_Pa", "T_gas_K",
                    "gamma_standard_per_s", "gamma_RA_dict_D_per_s",
                    "suppression_factor", "measurement_precision_factor",
                    "in_tension_with_data", "distinguishable"])
        for s, p in predictions:
            w.writerow([
                s.name, s.description, s.field_maturity,
                f"{s.m:.3e}", f"{s.dX:.3e}", f"{s.pressure_Pa:.3e}",
                f"{s.T_gas_K:.2f}",
                f"{p.gamma_standard_per_s:.6e}",
                f"{p.gamma_RA_dict_D_per_s:.6e}",
                f"{p.suppression_factor:.6f}",
                f"{p.measurement_precision_factor:.3f}",
                int(p.in_tension_with_data),
                int(p.distinguishable),
            ])
    print(f"\n  Predictions CSV written to: {out_path}")

    # honest closing
    print("\n" + "=" * 78)
    print("HONEST READING")
    print("=" * 78)
    print(f"""\
If Dictionary D applies UNIFORMLY to every positional-scattering event
(the simplest interpretation), then mature interferometry data already
constrain it: in atom and molecular interferometry, decoherence is
characterized to ~{int(0.1*100)}–{int(0.2*100)}% precision, well below the predicted 2.5x
discrepancy. Under that assumption, Dictionary D is essentially ruled out
for those systems by existing data — though no precision-decoherence
experiment in this catalog has explicitly been designed to look for a
flat suppression factor.

What this does NOT settle:
  - Whether the BDG filter applies to ALL positional scattering events
    or only to a specific subset (e.g. multi-vertex motif transitions).
    Under restricted application, the suppression factor would apply to
    a small subset of channels and could be invisible in cumulative Γ.
  - Whether the test mass actually maps to μ=4 or to some other μ
    (the open RA-OPEN-MU-ESTIMATOR-001 question).
  - Whether there exist experimental regimes (different mass scale,
    geometry, or coupling) where μ_RA naturally lands in the
    selective regime even if it doesn't there.

Operationally: the empirical constraints on Dictionary D
(RA-OPEN-BDG-DECOHERENCE-CONSTRAINTS-001) sharpen the open
mass-emergence work but do not settle it.""")


if __name__ == "__main__":
    main()
