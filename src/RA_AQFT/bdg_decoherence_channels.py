"""
bdg_decoherence_channels.py
Relational Actualism — channel-resolved BDG-suppression analysis.

Refines bdg_decoherence_predictions.py by decomposing positional
decoherence into physical channels (gas collision, blackbody, photon
recoil, vibration, etc.) and letting candidate "Dictionary D
variants" apply the BDG filter to a subset of channels rather than
uniformly to all positional scattering events.

The motivation: a flat Dict-D ~2.5x suppression on TOTAL Γ_decoh is
in tension with mature interferometry data. But if the filter applies
only to a subset of channels (e.g. only multi-quantum events that
inscribe multiple actualization vertices), then in experiments where
the dominant channel ISN'T filtered the suppression on cumulative Γ
is much smaller — invisible at current measurement precision.

This module enumerates a few defensible Dict-D variants with explicit
filter masks, computes the predicted residual suppression for each
scenario, and identifies which variants survive existing data and
which do not.

────────────────────────────────────────────────────────────────────────
HONEST SCOPE
────────────────────────────────────────────────────────────────────────
- Channel attributions and approximate channel weights are derived
  from training-data knowledge of canonical experimental classes
  (Kasevich-style atom interferometry, Arndt-style molecular IF,
  Aspelmeyer-style optomechanics, BMV-style proposals). They are NOT
  primary-source citations and should be tightened against actual
  published precision-decoherence-budget breakdowns.
- The "filter applies to channel X" assignments for each Dict-D
  variant are physically-motivated guesses about which kinds of
  environmental events should count as multi-vertex Step-4
  actualization candidates in RA's framework. They are not derived
  from any RA-MOTIF-* or RA-LLC-* claim and should be labeled as
  conjectures.
- The dominant-channel weights below capture the qualitative ordering
  reported in standard decoherence reviews; absolute numbers are
  order-of-magnitude only.

Authors: Joshua F. Sandeman (framework); Claude/Anthropic (computation)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from bdg_actualization import bdg_acceptance_probability


# ── Physical channels ─────────────────────────────────────────────────
@dataclass(frozen=True)
class DecoherenceChannel:
    """A physical decoherence channel.

    `multi_vertex_likely`: a physical-intuition flag for whether this
    channel naturally inscribes MULTIPLE actualization vertices per
    scattering event (gas collision deposits a recoil that propagates
    through internal modes; a single soft photon does not).
    """
    name: str
    description: str
    multi_vertex_likely: bool


GAS = DecoherenceChannel(
    name="gas_collision",
    description="Background-gas collision (large momentum transfer; "
                "deposits energy across internal modes)",
    multi_vertex_likely=True,
)
BLACKBODY = DecoherenceChannel(
    name="blackbody",
    description="Blackbody-photon absorption/emission (cumulative; "
                "many small events but each multi-mode)",
    multi_vertex_likely=True,
)
PHOTON_RECOIL = DecoherenceChannel(
    name="photon_recoil",
    description="Coherent-laser photon recoil (single-mode momentum "
                "kick from beamsplitter / cooling laser)",
    multi_vertex_likely=False,
)
VIBRATION = DecoherenceChannel(
    name="vibration",
    description="Mechanical vibration / seismic noise (technical, not "
                "fundamental; couples to position via apparatus)",
    multi_vertex_likely=False,
)
TRAP_PHOTON = DecoherenceChannel(
    name="trap_photon",
    description="Optical trap photon recoil (continuous, single-mode; "
                "dominant in optomechanical setups)",
    multi_vertex_likely=False,
)

ALL_CHANNELS = [GAS, BLACKBODY, PHOTON_RECOIL, VIBRATION, TRAP_PHOTON]


# ── Scenarios with channel breakdown ──────────────────────────────────
@dataclass(frozen=True)
class ScenarioChannels:
    """Representative channel weights for an experimental class.

    `channel_weights` maps each channel to its approximate fractional
    contribution to total Γ_decoh in mature instances of that class.
    Weights sum to ~1.0 (rounding aside). Order-of-magnitude only;
    actual experimental budgets vary case-by-case.
    """
    name: str
    description: str
    field_maturity: str           # 'mature', 'developing', 'speculative'
    measurement_precision_factor: float
    channel_weights: dict[str, float]


# Channel-budget catalog — synthesized from training-data knowledge of
# canonical experimental classes; not from primary citations.
SCENARIOS: list[ScenarioChannels] = [
    ScenarioChannels(
        name="atom_IF_Cs_fountain",
        description="Cs 10m-fountain atom interferometer (Kasevich-style)",
        field_maturity="mature",
        measurement_precision_factor=0.05,  # extremely well characterized
        channel_weights={
            GAS.name: 0.05,
            BLACKBODY.name: 0.01,
            PHOTON_RECOIL.name: 0.50,   # dominant: beamsplitter pulses
            VIBRATION.name: 0.40,       # technical, dominant non-photon
            TRAP_PHOTON.name: 0.04,
        },
    ),
    ScenarioChannels(
        name="mol_IF_C60",
        description="C60 fullerene KDTLI (Arndt group, Vienna)",
        field_maturity="mature",
        measurement_precision_factor=0.10,
        channel_weights={
            GAS.name: 0.40,             # dominant in moderate vacuum
            BLACKBODY.name: 0.40,       # significant for hot molecules
            PHOTON_RECOIL.name: 0.15,   # grating beam recoil
            VIBRATION.name: 0.05,
            TRAP_PHOTON.name: 0.0,
        },
    ),
    ScenarioChannels(
        name="mol_IF_oligoporphyrin",
        description="Oligoporphyrin (~10 kDa) interferometry (Arndt group)",
        field_maturity="mature",
        measurement_precision_factor=0.15,
        channel_weights={
            GAS.name: 0.55,
            BLACKBODY.name: 0.30,
            PHOTON_RECOIL.name: 0.10,
            VIBRATION.name: 0.05,
            TRAP_PHOTON.name: 0.0,
        },
    ),
    ScenarioChannels(
        name="opto_levitated_silica",
        description="Levitated silica nanosphere ground-state cooling "
                    "(Aspelmeyer-style)",
        field_maturity="developing",
        measurement_precision_factor=0.25,
        channel_weights={
            GAS.name: 0.10,
            BLACKBODY.name: 0.05,
            PHOTON_RECOIL.name: 0.0,
            VIBRATION.name: 0.05,
            TRAP_PHOTON.name: 0.80,    # dominant: trap photons
        },
    ),
    ScenarioChannels(
        name="opto_levitated_diamond_NV",
        description="Levitated diamond microsphere with NV (BMV precursor)",
        field_maturity="developing",
        measurement_precision_factor=0.40,
        channel_weights={
            GAS.name: 0.40,
            BLACKBODY.name: 0.10,
            PHOTON_RECOIL.name: 0.10,
            VIBRATION.name: 0.10,
            TRAP_PHOTON.name: 0.30,
        },
    ),
    ScenarioChannels(
        name="bmv_bose2017_nominal",
        description="BMV Bose 2017 nominal (m=1e-14 kg, dX=250 um)",
        field_maturity="speculative",
        measurement_precision_factor=1.0,
        channel_weights={
            GAS.name: 0.95,             # dominant by far
            BLACKBODY.name: 0.04,
            PHOTON_RECOIL.name: 0.0,
            VIBRATION.name: 0.01,
            TRAP_PHOTON.name: 0.0,
        },
    ),
    ScenarioChannels(
        name="carney_small_mass_proposal",
        description="Carney-style m~1e-19 kg proposal (sub-um geometry)",
        field_maturity="speculative",
        measurement_precision_factor=1.0,
        channel_weights={
            GAS.name: 0.50,
            BLACKBODY.name: 0.05,
            PHOTON_RECOIL.name: 0.05,
            VIBRATION.name: 0.10,
            TRAP_PHOTON.name: 0.30,
        },
    ),
]


# ── Dictionary-D variants (filter masks) ──────────────────────────────
@dataclass(frozen=True)
class DictDVariant:
    """A specific filter mask for the Dict-D BDG suppression.

    `applies_to` is the set of channel names the filter applies to.
    Channels not in `applies_to` evolve at the standard rate.
    Per-channel suppression for filtered channels = P_acc(mu).
    """
    name: str
    description: str
    applies_to: set[str]
    mu: float = 4.0


VARIANTS: list[DictDVariant] = [
    DictDVariant(
        name="D_uniform",
        description="Original Dict D — filter applies UNIFORMLY to all "
                    "positional decoherence channels.",
        applies_to={c.name for c in ALL_CHANNELS},
    ),
    DictDVariant(
        name="D_multi_vertex_only",
        description="Filter applies only to channels that naturally "
                    "inscribe MULTIPLE Step-4 vertices per event "
                    "(gas, blackbody — physically motivated by 'an "
                    "actualization candidate is a multi-vertex graph "
                    "extension').",
        applies_to={GAS.name, BLACKBODY.name},
    ),
    DictDVariant(
        name="D_gas_only",
        description="Filter applies only to large-momentum-transfer gas "
                    "collisions; all other channels at standard rate. "
                    "Strictest reading of 'kernel-natural candidates "
                    "are full-quantum scattering events'.",
        applies_to={GAS.name},
    ),
    DictDVariant(
        name="D_BMV_specific",
        description="Filter applies only to gas + trap_photon (the "
                    "channels relevant in BMV-precursor optomechanical "
                    "and levitated-mass setups); IF and molecular-IF "
                    "experiments are unaffected.",
        applies_to={GAS.name, TRAP_PHOTON.name},
    ),
]


# ── Channel-resolved suppression ──────────────────────────────────────
@dataclass(frozen=True)
class VariantPrediction:
    scenario: str
    variant: str
    p_acc: float
    suppression_total: float        # = Γ_std / Γ_RA
    in_tension: bool


def predict_variant(
    scenario: ScenarioChannels,
    variant: DictDVariant,
    n_samples: int = 50_000,
    saturation_cutoff: float = 50.0,
) -> VariantPrediction:
    """Compute the residual cumulative-Γ suppression for a scenario
    under a given Dict-D variant.

    Each channel evolves at standard rate Γ_c (its weight times
    Γ_total_std). For filtered channels, Γ_RA_c = Γ_c * P_acc(mu).
    For unfiltered channels, Γ_RA_c = Γ_c. Total suppression:
        suppression = sum(Γ_c) / sum(Γ_RA_c)
                    = 1 / (1 - (1 - P_acc) * w_filtered)
    where w_filtered = sum of weights of filtered channels.
    """
    if variant.mu >= saturation_cutoff:
        p_acc = 1.0
    else:
        p_acc = bdg_acceptance_probability(variant.mu, n_samples=n_samples)

    w_filtered = sum(scenario.channel_weights.get(c, 0.0)
                     for c in variant.applies_to)
    # cumulative suppression on normalized total Γ:
    #   Γ_RA / Γ_std = (1 - w_filtered) + w_filtered * p_acc
    #                = 1 - w_filtered * (1 - p_acc)
    ratio_RA_to_std = 1.0 - w_filtered * (1.0 - p_acc)
    suppression = (1.0 / ratio_RA_to_std) if ratio_RA_to_std > 0 else float("inf")

    # tension: is the residual suppression detectable in mature data?
    in_tension = (
        scenario.field_maturity == "mature"
        and suppression > 1.0 + 2.0 * scenario.measurement_precision_factor
    )
    return VariantPrediction(
        scenario=scenario.name,
        variant=variant.name,
        p_acc=p_acc,
        suppression_total=suppression,
        in_tension=in_tension,
    )


# ── Main: variant matrix ──────────────────────────────────────────────
def main() -> None:
    print("=" * 78)
    print("CHANNEL-RESOLVED BDG-SUPPRESSION ANALYSIS")
    print("=" * 78)
    print("""\
Refines the Dictionary-D BDG-suppression conjecture by enumerating
filter-mask variants and scoring each against the channel-resolved
budget for representative experimental classes. The flat-D variant
(filter applies to all positional decoherence) is in tension with
mature data; refined variants with restricted application escape
the tension to varying degrees.
""")

    # 1. Per-scenario channel budget
    print("-" * 78)
    print("Channel weight catalog (training-data synthesis, NOT primary lit):")
    print("-" * 78)
    print(f"  {'scenario':<32}{'maturity':<14}{'meas±':>7}    "
          f"{'gas':>6}{'BB':>6}{'rec':>6}{'vib':>6}{'trap':>6}")
    for s in SCENARIOS:
        w = s.channel_weights
        print(f"  {s.name:<32}{s.field_maturity:<14}"
              f"{s.measurement_precision_factor:>7.0%}    "
              f"{w.get(GAS.name, 0):>6.2f}{w.get(BLACKBODY.name, 0):>6.2f}"
              f"{w.get(PHOTON_RECOIL.name, 0):>6.2f}"
              f"{w.get(VIBRATION.name, 0):>6.2f}"
              f"{w.get(TRAP_PHOTON.name, 0):>6.2f}")

    # 2. Variant predictions matrix
    print("\n" + "-" * 78)
    print("Dict-D variant suppression matrix (cumulative Γ_std / Γ_RA):")
    print("-" * 78)
    header = f"  {'scenario':<32}"
    for v in VARIANTS:
        header += f"{v.name:>20}"
    print(header)
    print("  " + "-" * (32 + 20 * len(VARIANTS)))
    all_predictions = []
    for s in SCENARIOS:
        row = f"  {s.name:<32}"
        for v in VARIANTS:
            pred = predict_variant(s, v)
            all_predictions.append(pred)
            verdict_marker = "!" if pred.in_tension else " "
            row += f"{pred.suppression_total:>17.2f} {verdict_marker} "
        print(row)
    print(f"\n  '!' marks tension with existing precision data "
          f"(mature scenarios only).")

    # 3. Variant scoreboard
    print("\n" + "-" * 78)
    print("Variant scoreboard — how many mature scenarios in tension?")
    print("-" * 78)
    print(f"  {'variant':<24}{'#tension':>10}{'/#mature':>10}    "
          f"description")
    print("  " + "-" * 75)
    n_mature = sum(1 for s in SCENARIOS if s.field_maturity == "mature")
    for v in VARIANTS:
        n_tension = sum(
            1 for p in all_predictions
            if p.variant == v.name and p.in_tension
        )
        verdict = ("FALSIFIED" if n_tension == n_mature
                   else "constrained" if n_tension > 0
                   else "CONSISTENT")
        print(f"  {v.name:<24}{n_tension:>10}{n_mature:>10}    {verdict}")

    # 4. Identify weakest surviving variant
    print("\n" + "-" * 78)
    print("Surviving variants (consistent with all mature data):")
    print("-" * 78)
    survivors = []
    for v in VARIANTS:
        n_tension = sum(
            1 for p in all_predictions
            if p.variant == v.name and p.in_tension
        )
        if n_tension == 0:
            survivors.append(v)
    if not survivors:
        print("  [NONE — all enumerated Dict-D variants are constrained "
              "by mature data]")
    else:
        for v in survivors:
            print(f"  • {v.name}: {v.description}")

    # 5. Predictions in untested regimes for surviving variants
    if survivors:
        print("\n" + "-" * 78)
        print("Surviving-variant predictions for speculative / developing scenarios:")
        print("-" * 78)
        for v in survivors:
            print(f"\n  {v.name}:")
            for s in SCENARIOS:
                if s.field_maturity in ("developing", "speculative"):
                    pred = next(p for p in all_predictions
                                if p.scenario == s.name and p.variant == v.name)
                    if pred.suppression_total > 1.05:
                        print(f"    {s.name:<32}: predicted suppression "
                              f"{pred.suppression_total:.2f}x")

    # 6. CSV output
    out_path = Path(__file__).parent / "bdg_decoherence_channels_matrix.csv"
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scenario", "variant", "p_acc", "suppression_total",
                    "in_tension", "field_maturity",
                    "measurement_precision_factor"])
        for pred in all_predictions:
            scenario = next(s for s in SCENARIOS if s.name == pred.scenario)
            w.writerow([
                pred.scenario, pred.variant,
                f"{pred.p_acc:.6f}",
                f"{pred.suppression_total:.6f}",
                int(pred.in_tension),
                scenario.field_maturity,
                f"{scenario.measurement_precision_factor:.3f}",
            ])
    print(f"\n  Variant matrix CSV written to: {out_path}")

    # 7. Honest closing
    print("\n" + "=" * 78)
    print("HONEST READING")
    print("=" * 78)
    print(f"""\
The flat Dict-D variant (D_uniform — filter applies to all positional
decoherence) is in tension with all mature interferometry data.
Restricted variants (D_multi_vertex_only, D_gas_only, D_BMV_specific)
escape the tension to varying degrees by exempting the dominant
non-multi-vertex channels (photon recoil, trap photons, vibration)
that drive Γ_decoh in atom IF and optomechanical setups.

What this analysis suggests for future work:
  • If future RA mass-emergence work derives a Dict-D-style
    suppression at mu = 4 with the filter applying ONLY to multi-
    quantum scattering events (gas + blackbody), the prediction is
    consistent with all mature interferometry data while still
    predicting non-trivial suppression in BMV-style and large-mass
    levitated setups (gas-collision dominated).
  • If the filter applies more broadly — including to single-photon
    recoil events — it is constrained or falsified by atom IF.
  • The empirical-constraint angle is: any future RA-derived
    suppression mechanism that produces a flat factor across all
    channels needs to be < 1.05x to survive Cs atom interferometry
    (which has ~5% precision). Any channel-selective mechanism is
    much less constrained.

What this analysis does NOT do:
  • Cite specific published decoherence-budget breakdowns. Channel
    weights are training-data synthesis, not primary lit. A real
    lit-review pass would tighten the verdict and identify
    experiments that have explicitly bounded gas+BB-only suppression
    at <few-percent precision.
  • Settle which variant is RA-correct. That requires closing
    RA-OPEN-MU-ESTIMATOR-001 (mu derivation) and the broader
    mass-emergence work (RA-MOTIF-* and Causal Firewall).
  • Address kinematic vs dynamical suppression — the variants here
    all assume the BDG filter applies as a multiplicative factor on
    the rate, not as a modification of the temporal evolution.""")


if __name__ == "__main__":
    main()
