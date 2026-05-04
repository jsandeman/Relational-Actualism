"""
bdg_decoherence_channels.py
Relational Actualism — channel-resolved BDG-suppression analysis (v2).

────────────────────────────────────────────────────────────────────────
v2 — POST-LIT-REVIEW REWRITE (May 4, 2026)
────────────────────────────────────────────────────────────────────────
Refactored against the v2 primary-literature review at
docs/RA_KB/reports/decoherence_litreview_v2.md, which identified
critical issues with the v1 analysis:

  1. LINDBLAD ADDITIVITY IS NOT UNIVERSALLY VALID. The "channel
     budget" framing applies cleanly only in:
       • Engineered-channel matter-wave measurements (Hornberger 2003
         collisional, Hackermüller 2004 BB)
       • Cavity-CS / feedback / cryogenic free-space ground-state
         cooled levitated nanoparticles
     It does NOT apply to:
       • Atom-IF nominal (vibration enters as ensemble phase
         variance, not Lindblad position decoherence)
       • Atom-IF trapped-lattice (dominant residual is collective
         dephasing from anharmonic trap)
       • Heavy-mol nominal (residual is instrumental, not Lindblad)
       • Diamond-NV CoM (graphitization, not in any decoherence
         schema)
       • BMV (schema lacks magnetic-gradient + charge-multipole
         channels Bose 2017 identifies as critical)
  2. Scenarios should be SPLIT by protocol_variant. v1 lumped
     "atom_IF_Cs" across fountain + lattice; "mol_IF_C60" across
     nominal + collisional-engineered + BB-engineered; "opto_silica"
     across cavity-CS + feedback + cryo-freespace.
  3. Channels split: blackbody → self_emission + environmental;
     photon_recoil → spontaneous_emission + laser_phase_noise;
     vibration → seismic + technical.
  4. THE RIGHT ANALYTICAL FRAMING is per-channel constraint from
     engineered-condition measurements, NOT cumulative-Γ across mixed
     scenarios. Hornberger 2003 measures Γ_gas at ~10% precision in a
     gas-engineered run; this DIRECTLY BOUNDS any flat per-channel
     suppression of gas at <10%. Dict-D's 60% suppression prediction
     is then ruled out at ~6σ by that single measurement.

POST-V2 VERDICT (see per_channel_constraint_analysis output):
  All four enumerated Dict-D variants (D_uniform, D_multi_vertex_only,
  D_gas_only, D_BMV_specific) are FALSIFIED at high confidence by
  per-channel engineered measurements. Each variant touches at least
  one of {gas, BB_self, trap_photon_recoil}, all of which have direct
  Lindblad-theory-vs-data agreement at 10-15% precision in clean
  engineered runs (Hornberger 2003, Hackermüller 2004, Delić 2020,
  Tebbenjohanns 2021).

  The kernel-structural conjecture μ=d=4-universally is therefore
  essentially closed — except via narrow escape routes that filter only
  channels for which no precision per-channel measurement exists
  (spontaneous emission, laser phase noise), or via a non-universal
  μ-dictionary (which is the open RA-OPEN-MU-ESTIMATOR-001 question).

────────────────────────────────────────────────────────────────────────
HONEST SCOPE
────────────────────────────────────────────────────────────────────────
- The schema-additivity-valid flag determines which scenarios can
  honestly be used in cumulative-Γ analysis. Scenarios where the
  dominant residual mechanism is non-Lindblad (vibration phase
  variance, instrumental, anharmonic-trap collective dephasing,
  graphitization) are SKIPPED in the cumulative variant matrix.
- Per-channel constraints from engineered scenarios are the strongest
  bound. They operate on the per-event Lindblad rate prediction, not
  on cumulative scenario-level Γ.
- Channel weights from the v2 review are primary-source-cited where
  measured; null where not separately published. We do NOT fabricate
  representative numbers for unknown channels.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from bdg_actualization import bdg_acceptance_probability


# ── Physical channels (v2 schema) ─────────────────────────────────────
@dataclass(frozen=True)
class DecoherenceChannel:
    name: str
    description: str
    multi_vertex_likely: bool


GAS = DecoherenceChannel(
    name="gas_collision",
    description="Background-gas momentum-transfer collisions",
    multi_vertex_likely=True,
)
BB_SELF = DecoherenceChannel(
    name="blackbody_self_emission",
    description="Internal-thermal blackbody photon emission from the test "
                "particle (matters most for hot molecules)",
    multi_vertex_likely=True,
)
BB_ENV = DecoherenceChannel(
    name="blackbody_environmental",
    description="Blackbody photon absorption from environmental thermal "
                "background (matters when ambient T is not cryogenic)",
    multi_vertex_likely=True,
)
SPONTANEOUS_EMISSION = DecoherenceChannel(
    name="spontaneous_emission",
    description="Off-resonant atomic spontaneous emission during "
                "Bragg/Raman pulses; engineered low",
    multi_vertex_likely=False,
)
LASER_PHASE_NOISE = DecoherenceChannel(
    name="laser_phase_noise",
    description="Laser phase / intensity noise on the interferometer or "
                "trap beam",
    multi_vertex_likely=False,
)
TRAP_PHOTON_RECOIL = DecoherenceChannel(
    name="trap_photon_recoil",
    description="Optical-trap photon recoil heating; dominant in "
                "ground-state-cooled levitated optomechanics",
    multi_vertex_likely=False,
)
VIBRATION_SEISMIC = DecoherenceChannel(
    name="vibration_seismic",
    description="Seismic / acoustic vibration coupling to position; "
                "ensemble phase variance for free-fall atom IF",
    multi_vertex_likely=False,
)
VIBRATION_TECHNICAL = DecoherenceChannel(
    name="vibration_technical",
    description="Technical vibration (lasers, mounts, electronics)",
    multi_vertex_likely=False,
)
DETECTION_STATISTICS = DecoherenceChannel(
    name="detection_statistics",
    description="Detection shot noise / readout statistics — not a "
                "physical decoherence channel; a contrast-loss budget item",
    multi_vertex_likely=False,
)
OTHER_UNATTRIBUTED = DecoherenceChannel(
    name="other_unattributed",
    description="Catch-all for channels not in the schema (instrumental "
                "visibility loss, magnetic gradients, charge multipoles, "
                "Casimir-Polder, graphitization, anharmonic trap...). The "
                "BDG filter cannot apply to these even in principle; they "
                "are listed for accounting only.",
    multi_vertex_likely=False,
)

ALL_CHANNELS = [
    GAS, BB_SELF, BB_ENV,
    SPONTANEOUS_EMISSION, LASER_PHASE_NOISE,
    TRAP_PHOTON_RECOIL,
    VIBRATION_SEISMIC, VIBRATION_TECHNICAL,
    DETECTION_STATISTICS,
    OTHER_UNATTRIBUTED,
]

# Channels the BDG filter could in principle apply to (excluding pure
# measurement noise and instrumental catch-alls).
ACTUALIZATION_CHANNELS = [
    GAS, BB_SELF, BB_ENV,
    SPONTANEOUS_EMISSION, LASER_PHASE_NOISE,
    TRAP_PHOTON_RECOIL,
    VIBRATION_SEISMIC, VIBRATION_TECHNICAL,
]

# Channels for which the v2 lit-review identifies a HIGH-PRECISION
# engineered-condition Lindblad-vs-data measurement that directly bounds
# any flat per-channel suppression. These are what falsify Dict-D
# variants at high confidence.
PER_CHANNEL_PRECISION_BOUNDS = {
    GAS.name: (0.10, "Hornberger et al. PRL 90, 160401 (2003) — "
                     "C70 collisional decoherence, P scan up to 1e-6 mbar"),
    BB_SELF.name: (0.15, "Hackermüller et al. Nature 427, 711 (2004) — "
                         "C70 BB-self-emission, laser-heated to 2000-3000K"),
    TRAP_PHOTON_RECOIL.name: (0.14, "Delić et al. Science 367, 892 (2020) — "
                                    "cavity-CS recoil heating Γ_x = 21±3 kHz"),
}


# ── Scenarios (v2 schema with protocol_variant splits) ────────────────
@dataclass(frozen=True)
class ScenarioChannels:
    name: str
    description: str
    field_maturity: str           # 'mature', 'developing', 'speculative'
    protocol_variant: str
    operating_conditions: str     # 'nominal', 'engineered_*', 'theoretical'
    measurement_precision_factor: float
    channel_weights: dict[str, float]
    # POST-v2: scenarios where the dominant residual mechanism is NOT a
    # Lindblad-form independent channel (e.g. ensemble phase variance,
    # collective dephasing, instrumental, graphitization). Cumulative-Γ
    # analysis is ill-defined for these.
    channel_additivity_valid: bool
    unknown_fraction: float       # weight of the budget that is unaccounted-for
    confidence: str               # 'measured', 'theoretical_extrapolation', 'uncharacterized'
    additivity_caveat: str
    primary_citations: tuple[str, ...] = ()


SCENARIOS: list[ScenarioChannels] = [
    # ── atom IF — split by protocol_variant ───────────────────────────
    ScenarioChannels(
        name="atom_IF_Cs_fountain_freefall",
        description="Cs/Rb 10m free-fall fountain; Kasevich/Müller-style",
        field_maturity="mature",
        protocol_variant="free_fall_fountain",
        operating_conditions="nominal",
        measurement_precision_factor=0.20,
        channel_additivity_valid=False,
        confidence="measured",
        channel_weights={
            GAS.name: 0.01,
            BB_SELF.name: 0.00,
            BB_ENV.name: 0.01,
            SPONTANEOUS_EMISSION.name: 0.05,
            TRAP_PHOTON_RECOIL.name: 0.00,
            VIBRATION_SEISMIC.name: 0.70,
            DETECTION_STATISTICS.name: 0.05,
            OTHER_UNATTRIBUTED.name: 0.18,
        },
        unknown_fraction=0.18,
        additivity_caveat=(
            "Vibration in fountain mode enters as ENSEMBLE PHASE VARIANCE, "
            "not as Lindblad position decoherence. The contrast-vs-T "
            "exponential framing is approximate (Miffre 2006). Cumulative-Γ "
            "analysis is ill-defined; do NOT use this scenario to constrain "
            "Dict-D variants."
        ),
        primary_citations=(
            "Panda et al. Nat. Phys. 20, 1234 (2024) arXiv:2210.07289",
            "Miffre et al. EPL 75 (2006) arXiv:quant-ph/0604022",
            "Asenbaum et al. PRL 118, 183602 (2017)",
        ),
    ),
    ScenarioChannels(
        name="atom_IF_Cs_lattice",
        description="Cs/Rb optical-lattice atom IF (Panda/Müller-style)",
        field_maturity="mature",
        protocol_variant="trapped_lattice",
        operating_conditions="nominal",
        measurement_precision_factor=0.30,
        channel_additivity_valid=False,
        confidence="measured",
        channel_weights={
            GAS.name: 0.05,
            BB_ENV.name: 0.01,
            VIBRATION_SEISMIC.name: 0.001,  # suppressed by 10^3-10^4 vs fountain
            DETECTION_STATISTICS.name: 0.05,
            OTHER_UNATTRIBUTED.name: 0.89,
        },
        unknown_fraction=0.89,
        additivity_caveat=(
            "Dominant residual is COLLECTIVE DEPHASING from anharmonic "
            "trap-induced motion through inhomogeneous lattice potential — "
            "NOT a Lindblad channel. Forcing into 'trap_photon_recoil' "
            "would be misleading. Cumulative-Γ analysis is ill-defined."
        ),
        primary_citations=(
            "Panda et al. Nat. Phys. 20, 1234 (2024) arXiv:2210.07289",
            "Panda et al. Nature 631, 515 (2024) arXiv:2310.01344",
        ),
    ),
    # ── mol_IF_C60 — split by operating_conditions ────────────────────
    ScenarioChannels(
        name="mol_IF_C60_nominal",
        description="C70 Talbot-Lau IF, Vienna group, nominal conditions",
        field_maturity="mature",
        protocol_variant="TLI_baseline",
        operating_conditions="nominal",
        measurement_precision_factor=0.20,
        channel_additivity_valid=False,
        confidence="measured",
        channel_weights={
            GAS.name: 0.05,
            BB_SELF.name: 0.05,
            BB_ENV.name: 0.00,
            VIBRATION_SEISMIC.name: 0.30,
            DETECTION_STATISTICS.name: 0.10,
            OTHER_UNATTRIBUTED.name: 0.50,
        },
        unknown_fraction=0.50,
        additivity_caveat=(
            "At nominal conditions the residual visibility loss is "
            "dominated by INSTRUMENTAL effects (grating period precision, "
            "alignment, source velocity dispersion). Hornberger-Sipe "
            "Lindblad formalism applies to gas+BB but explicitly excludes "
            "instrumental effects. Cumulative-Γ analysis ill-defined."
        ),
        primary_citations=(
            "Hornberger et al. PRL 90, 160401 (2003)",
            "Stibor et al. arXiv:quant-ph/0411118 (2004)",
            "Hackermüller et al. Appl. Phys. B 77, 781 (2003)",
        ),
    ),
    ScenarioChannels(
        name="mol_IF_C60_collisional_engineered",
        description="C70 TLI with raised gas pressure (Hornberger 2003)",
        field_maturity="mature",
        protocol_variant="TLI_collisional_pressure_scan",
        operating_conditions="engineered_gas_collision",
        measurement_precision_factor=0.10,
        channel_additivity_valid=True,    # the canonical clean case
        confidence="measured",
        channel_weights={
            GAS.name: 0.85,
            BB_SELF.name: 0.05,
            VIBRATION_SEISMIC.name: 0.05,
            DETECTION_STATISTICS.name: 0.05,
        },
        unknown_fraction=0.0,
        additivity_caveat=(
            "Hornberger-Sipe-Vacchini cross-section formalism quantitatively "
            "reproduces visibility-vs-pressure over decades of P. Channel "
            "additivity well-supported in this regime. THE per-channel "
            "constraint scenario for gas."
        ),
        primary_citations=(
            "Hornberger et al. PRL 90, 160401 (2003) arXiv:quant-ph/0303093",
            "Hornberger Sipe Arndt PRA 70, 053608 (2004)",
        ),
    ),
    ScenarioChannels(
        name="mol_IF_C60_blackbody_engineered",
        description="C70 TLI with laser-heated molecules (Hackermüller 2004)",
        field_maturity="mature",
        protocol_variant="TLI_BB_temperature_scan",
        operating_conditions="engineered_blackbody",
        measurement_precision_factor=0.15,
        channel_additivity_valid=True,
        confidence="measured",
        channel_weights={
            GAS.name: 0.05,
            BB_SELF.name: 0.85,
            VIBRATION_SEISMIC.name: 0.05,
            DETECTION_STATISTICS.name: 0.05,
        },
        unknown_fraction=0.0,
        additivity_caveat=(
            "Quantitative agreement with microscopic decoherence theory "
            "in the data range. THE per-channel constraint scenario for "
            "blackbody self-emission. (At T → 2800 K, fragmentation "
            "begins to compete; Hackermüller stays below this regime.)"
        ),
        primary_citations=(
            "Hackermüller et al. Nature 427, 711 (2004) arXiv:quant-ph/0402146",
            "Hornberger Sipe Arndt PRA 70, 053608 (2004)",
        ),
    ),
    # ── oligoporphyrin — schema-incompatible ─────────────────────────
    ScenarioChannels(
        name="mol_IF_oligoporphyrin",
        description="Oligoporphyrin 10-27 kDa (Eibenberger 2013, Fein 2019)",
        field_maturity="mature",
        protocol_variant="KDTLI_or_LUMI_baseline",
        operating_conditions="nominal",
        measurement_precision_factor=0.20,
        channel_additivity_valid=False,
        confidence="uncharacterized",
        channel_weights={
            OTHER_UNATTRIBUTED.name: 1.0,
        },
        unknown_fraction=1.0,
        additivity_caveat=(
            "Channel-resolved budgets NOT separately published. Primary "
            "lit explicitly states gas+BB are sub-dominant at nominal "
            "conditions (Fein 2019, Eibenberger 2013). Residual visibility "
            "loss is INSTRUMENTAL (grating period, source coherence, "
            "velocity dispersion). v1's gas=0.55 / BB=0.30 was contradicted "
            "by primary lit. CANNOT constrain any predicted suppression."
        ),
        primary_citations=(
            "Fein et al. Nat. Phys. 15, 1242 (2019)",
            "Eibenberger et al. PCCP 15, 14696 (2013) arXiv:1310.8343",
            "Kiałka et al. AVS Quantum Sci. 4, 020502 (2022)",
        ),
    ),
    # ── opto-levitated silica — split by protocol ────────────────────
    ScenarioChannels(
        name="opto_levitated_silica_cavityCS",
        description="Cavity coherent-scattering ground-state cooling "
                    "(Delić 2020)",
        field_maturity="developing",
        protocol_variant="cavity_CS",
        operating_conditions="nominal",
        measurement_precision_factor=0.14,
        channel_additivity_valid=True,
        confidence="measured",
        channel_weights={
            GAS.name: 0.30,
            BB_ENV.name: 0.05,
            TRAP_PHOTON_RECOIL.name: 0.60,
            DETECTION_STATISTICS.name: 0.05,
        },
        unknown_fraction=0.0,
        additivity_caveat=(
            "Lindblad-additive at leading order; both gas and recoil are "
            "independent momentum-transfer channels. THE per-channel "
            "constraint scenario for trap_photon_recoil."
        ),
        primary_citations=(
            "Delić et al. Science 367, 892 (2020) arXiv:1911.04406",
            "Jain et al. PRL 116, 243601 (2016)",
            "Romero-Isart PRA 84, 052121 (2011)",
        ),
    ),
    ScenarioChannels(
        name="opto_levitated_silica_feedback_RT",
        description="Levitated silica, room-T feedback (Magrini 2021)",
        field_maturity="developing",
        protocol_variant="feedback_room_T",
        operating_conditions="nominal",
        measurement_precision_factor=0.20,
        channel_additivity_valid=False,    # cross-mode hybridization noted
        confidence="measured",
        channel_weights={
            TRAP_PHOTON_RECOIL.name: 0.80,
            OTHER_UNATTRIBUTED.name: 0.20,
        },
        unknown_fraction=0.20,
        additivity_caveat=(
            "Magrini 2021 notes 'cross-mode hybridization' between "
            "transverse and longitudinal motion is non-negligible — "
            "coupled-channel effect not captured by single-mode "
            "Lindblad-additive budgets."
        ),
        primary_citations=(
            "Magrini et al. Nature 595, 373 (2021)",
            "Gonzalez-Ballestero et al. arXiv:1902.01282",
        ),
    ),
    ScenarioChannels(
        name="opto_levitated_silica_cryo_freespace",
        description="Cryogenic free-space feedback (Tebbenjohanns 2021)",
        field_maturity="developing",
        protocol_variant="cryogenic_freespace_feedback",
        operating_conditions="nominal",
        measurement_precision_factor=0.20,
        channel_additivity_valid=True,
        confidence="measured",
        channel_weights={
            GAS.name: 0.05,
            BB_ENV.name: 0.05,
            TRAP_PHOTON_RECOIL.name: 0.85,
            DETECTION_STATISTICS.name: 0.05,
        },
        unknown_fraction=0.0,
        additivity_caveat=(
            "Cleanest example of photon-recoil-dominant decoherence. "
            "Cryogenics decouples thermal channels. Realizes the regime "
            "predicted by Romero-Isart 2011 with recoil added back in."
        ),
        primary_citations=(
            "Tebbenjohanns et al. Nature 595, 378 (2021) arXiv:2103.03853",
            "Romero-Isart PRA 84, 052121 (2011)",
        ),
    ),
    # ── diamond NV — split spin vs CoM ─────────────────────────────────
    ScenarioChannels(
        name="opto_levitated_diamond_NV_spin_only",
        description="Diamond NV electron-spin coherence in vacuum (Jin 2024)",
        field_maturity="developing",
        protocol_variant="NV_spin_coherence_only",
        operating_conditions="nominal",
        measurement_precision_factor=0.10,
        channel_additivity_valid=False,
        confidence="measured",
        channel_weights={
            DETECTION_STATISTICS.name: 0.10,
            OTHER_UNATTRIBUTED.name: 0.90,
        },
        unknown_fraction=0.90,
        additivity_caveat=(
            "NV electron-spin coherence is governed by 13C nuclear spin "
            "bath dynamics, NV-NV cross-talk, magnetic field stability — "
            "none of which are v2 schema channels. NOT relevant to CoM "
            "positional decoherence Dict-D analysis."
        ),
        primary_citations=(
            "Jin et al. Nat. Commun. 15, 5063 (2024) arXiv:2309.05821",
        ),
    ),
    ScenarioChannels(
        name="opto_levitated_diamond_NV_CoM_proposal",
        description="Diamond NV CoM positional decoherence (NEVER MEASURED)",
        field_maturity="speculative",
        protocol_variant="CoM_matterwave_proposal",
        operating_conditions="theoretical",
        measurement_precision_factor=1.0,
        channel_additivity_valid=False,
        confidence="uncharacterized",
        channel_weights={
            OTHER_UNATTRIBUTED.name: 1.0,
        },
        unknown_fraction=1.0,
        additivity_caveat=(
            "Dominant practical limit is GRAPHITIZATION at high vacuum "
            "(Frangeskou 2018, Hsu 2016) — not a Lindblad channel. "
            "v2 schema cannot represent this scenario."
        ),
        primary_citations=(
            "Frangeskou et al. NJP 20, 043016 (2018)",
            "Hsu et al. Sci. Rep. 6, 36514 (2016) arXiv:1510.07555",
            "Bose et al. PRL 119, 240401 (2017)",
        ),
    ),
    # ── BMV / Carney — speculative ─────────────────────────────────────
    ScenarioChannels(
        name="bmv_bose2017_nominal",
        description="Bose-Marletto-Vedral 2017 spin-witness QGEM proposal",
        field_maturity="speculative",
        protocol_variant="Bose2017_design_parameters",
        operating_conditions="theoretical",
        measurement_precision_factor=1.0,
        channel_additivity_valid=False,
        confidence="theoretical_extrapolation",
        channel_weights={
            GAS.name: 0.95,
            BB_SELF.name: 0.02,
            BB_ENV.name: 0.02,
            DETECTION_STATISTICS.name: 0.01,
        },
        unknown_fraction=0.0,
        additivity_caveat=(
            "Bose 2017 puts design at EDGE of gas-feasibility (Γ_gas·τ ~ 1, "
            "not <<1). The 0.95 weight reflects 'channel of dominant "
            "concern' rather than measured fraction. Schema LACKS magnetic-"
            "gradient and charge-multipole channels Bose 2017 explicitly "
            "identifies as critical."
        ),
        primary_citations=(
            "Bose et al. PRL 119, 240401 (2017) arXiv:1707.06050",
            "Marletto Vedral PRL 119, 240402 (2017)",
            "Chevalier Paige Kim PRA 102, 022428 (2020) arXiv:2005.13922",
        ),
    ),
    ScenarioChannels(
        name="carney_small_mass_proposal",
        description="Carney-class quantum-gravity proposals (UNDERSPECIFIED)",
        field_maturity="speculative",
        protocol_variant="UNDERSPECIFIED",
        operating_conditions="theoretical",
        measurement_precision_factor=1.0,
        channel_additivity_valid=False,
        confidence="uncharacterized",
        channel_weights={
            OTHER_UNATTRIBUTED.name: 1.0,
        },
        unknown_fraction=1.0,
        additivity_caveat=(
            "Class-typical label, not a single primary source. v2 lit "
            "review recommends pinning to a specific arxiv ID + parameter "
            "set or removing entirely."
        ),
        primary_citations=(
            "Carney Stamp Taylor CQG 36, 034001 (2019) arXiv:1807.11494",
            "Carney Krnjaic Moore Snowmass arXiv:2203.11846 (2022)",
        ),
    ),
]


# ── Dictionary-D variants ─────────────────────────────────────────────
@dataclass(frozen=True)
class DictDVariant:
    name: str
    description: str
    applies_to: set[str]
    mu: float = 4.0


VARIANTS: list[DictDVariant] = [
    DictDVariant(
        name="D_uniform",
        description="Filter applies UNIFORMLY to all actualization-candidate "
                    "channels (excludes detection_statistics + other_unattributed).",
        applies_to={c.name for c in ACTUALIZATION_CHANNELS},
    ),
    DictDVariant(
        name="D_multi_vertex_only",
        description="Filter applies only to channels likely inscribing "
                    "multiple Step-4 vertices per event (gas + both BB).",
        applies_to={GAS.name, BB_SELF.name, BB_ENV.name},
    ),
    DictDVariant(
        name="D_gas_only",
        description="Filter applies only to large-momentum-transfer gas "
                    "collisions.",
        applies_to={GAS.name},
    ),
    DictDVariant(
        name="D_BMV_specific",
        description="Filter applies to gas + trap_photon_recoil "
                    "(channels relevant in BMV-precursor optomechanical "
                    "and levitated-mass setups).",
        applies_to={GAS.name, TRAP_PHOTON_RECOIL.name},
    ),
]


# ── Per-channel constraint analysis (the v2 KEY analytical move) ──────
@dataclass(frozen=True)
class PerChannelConstraint:
    channel: str
    precision_bound: float       # fractional ± from engineered measurement
    citation: str
    dict_D_predicted_suppression: float  # = 1 - P_acc(mu=4) ~ 0.6
    sigma_falsification: float   # = predicted_suppression / precision_bound


def per_channel_constraints(mu: float = 4.0,
                             n_samples: int = 50_000) -> list[PerChannelConstraint]:
    """Compute the per-channel falsification verdict for Dict-D at given μ.

    For each channel with a high-precision engineered Lindblad-vs-data
    measurement (gas, BB_self, trap_photon_recoil), compute:
      • Dict-D's predicted per-channel suppression: 1 - P_acc(μ)
      • The precision bound from the engineered measurement
      • The falsification σ: ratio of predicted to bound.

    A σ > ~3 indicates the variant filter applied to that channel is
    falsified by direct measurement.
    """
    if mu >= 50.0:
        p_acc = 1.0
    else:
        p_acc = bdg_acceptance_probability(mu, n_samples=n_samples)
    predicted_suppression = 1.0 - p_acc
    constraints = []
    for ch_name, (bound, citation) in PER_CHANNEL_PRECISION_BOUNDS.items():
        sigma = predicted_suppression / bound if bound > 0 else float("inf")
        constraints.append(PerChannelConstraint(
            channel=ch_name,
            precision_bound=bound,
            citation=citation,
            dict_D_predicted_suppression=predicted_suppression,
            sigma_falsification=sigma,
        ))
    return constraints


def variant_per_channel_falsification(
    variant: DictDVariant,
    constraints: list[PerChannelConstraint],
) -> dict[str, float]:
    """Return the channels touched by this variant that have a per-channel
    constraint, mapped to their falsification σ. Empty dict if the
    variant touches no constrained channel."""
    return {
        c.channel: c.sigma_falsification
        for c in constraints
        if c.channel in variant.applies_to
    }


# ── Cumulative-Γ analysis (v1-style, restricted to additivity-valid) ──
@dataclass(frozen=True)
class VariantPrediction:
    scenario: str
    variant: str
    p_acc: float
    suppression_total: float
    in_tension: bool
    additivity_skipped: bool


def predict_variant(
    scenario: ScenarioChannels,
    variant: DictDVariant,
    n_samples: int = 50_000,
    saturation_cutoff: float = 50.0,
) -> VariantPrediction:
    """Cumulative-Γ analysis. Returns additivity_skipped=True for
    scenarios where Lindblad additivity is invalid; suppression
    computation is reported but should not be interpreted as a
    constraint."""
    if variant.mu >= saturation_cutoff:
        p_acc = 1.0
    else:
        p_acc = bdg_acceptance_probability(variant.mu, n_samples=n_samples)
    w_filtered = sum(scenario.channel_weights.get(c, 0.0)
                     for c in variant.applies_to)
    ratio_RA_to_std = 1.0 - w_filtered * (1.0 - p_acc)
    suppression = (1.0 / ratio_RA_to_std) if ratio_RA_to_std > 0 else float("inf")
    detectable = suppression > 1.0 + 2.0 * scenario.measurement_precision_factor
    in_tension = (
        scenario.channel_additivity_valid
        and scenario.field_maturity == "mature"
        and scenario.confidence == "measured"
        and detectable
    )
    return VariantPrediction(
        scenario=scenario.name,
        variant=variant.name,
        p_acc=p_acc,
        suppression_total=suppression,
        in_tension=in_tension,
        additivity_skipped=not scenario.channel_additivity_valid,
    )


# ── Main ──────────────────────────────────────────────────────────────
def main() -> None:
    print("=" * 78)
    print("CHANNEL-RESOLVED BDG-SUPPRESSION ANALYSIS — v2 (post-lit-review)")
    print("=" * 78)
    print("""\
Refactored against the v2 lit review at
docs/RA_KB/reports/decoherence_litreview_v2.md, which identified that:
  (a) Lindblad additivity is NOT universally valid — atom-IF, heavy-mol
      nominal, diamond-NV CoM, and BMV all have schema-incompatible
      dominant residual mechanisms.
  (b) The right analytical move is per-channel constraint from
      ENGINEERED-condition measurements (Hornberger 2003 for gas,
      Hackermüller 2004 for BB, Delić 2020 for trap-photon recoil).
""")

    # 1. Per-channel constraints (the v2 KEY analysis)
    print("-" * 78)
    print("PER-CHANNEL CONSTRAINTS from engineered-condition measurements:")
    print("-" * 78)
    constraints = per_channel_constraints()
    print(f"\n  Dict-D predicted suppression at μ=4 (per-channel): "
          f"{constraints[0].dict_D_predicted_suppression:.3f}")
    print(f"  ({1-constraints[0].dict_D_predicted_suppression:.3f}× residual = "
          f"{constraints[0].dict_D_predicted_suppression*100:.1f}% suppression)")
    print()
    print(f"  {'channel':<28}{'bound':>10}{'σ-falsify':>12}    measurement")
    print("  " + "-" * 76)
    for c in constraints:
        print(f"  {c.channel:<28}{c.precision_bound*100:>9.0f}%"
              f"{c.sigma_falsification:>11.1f}σ    "
              f"{c.citation[:50]}")

    # 2. Variant per-channel verdict
    print("\n" + "-" * 78)
    print("DICT-D VARIANT VERDICTS via per-channel constraints:")
    print("-" * 78)
    print(f"\n  Variant FALSIFIED if it touches a channel where σ-falsification > 3.0\n")
    print(f"  {'variant':<24}{'falsifying channels (σ)':<60}")
    print("  " + "-" * 76)
    for v in VARIANTS:
        falsified_by = variant_per_channel_falsification(v, constraints)
        falsified_by_strong = {ch: s for ch, s in falsified_by.items() if s > 3.0}
        if falsified_by_strong:
            verdict_str = " ".join(f"{ch[:6]}({s:.1f}σ)"
                                   for ch, s in falsified_by_strong.items())
            print(f"  {v.name:<24}FALSIFIED: {verdict_str}")
        elif falsified_by:
            verdict_str = " ".join(f"{ch[:6]}({s:.1f}σ)" for ch, s in falsified_by.items())
            print(f"  {v.name:<24}weak: {verdict_str}")
        else:
            print(f"  {v.name:<24}no per-channel constraint touches "
                  "filtered channels")

    # 3. Cumulative-Γ analysis (only over additivity-valid scenarios)
    print("\n" + "-" * 78)
    print("CUMULATIVE-Γ ANALYSIS (additivity-valid scenarios only):")
    print("-" * 78)
    valid_scenarios = [s for s in SCENARIOS if s.channel_additivity_valid]
    print(f"\n  {len(valid_scenarios)} of {len(SCENARIOS)} scenarios are "
          "additivity-valid; the rest are SKIPPED (schema-incompatible).")
    print(f"\n  {'scenario':<42}", end="")
    for v in VARIANTS:
        print(f"{v.name:>20}", end="")
    print()
    print("  " + "-" * (42 + 20 * len(VARIANTS)))
    all_predictions = []
    for s in SCENARIOS:
        for v in VARIANTS:
            pred = predict_variant(s, v)
            all_predictions.append(pred)
        if not s.channel_additivity_valid:
            continue
        row = f"  {s.name:<42}"
        for v in VARIANTS:
            pred = next(p for p in all_predictions
                        if p.scenario == s.name and p.variant == v.name)
            marker = "!" if pred.in_tension else " "
            row += f"{pred.suppression_total:>17.2f} {marker} "
        print(row)
    print(f"\n  '!' = in tension at >2σ measurement precision.")

    # 4. Skipped scenarios audit
    print("\n  Skipped scenarios (schema-incompatible) and why:")
    for s in SCENARIOS:
        if s.channel_additivity_valid:
            continue
        print(f"    • {s.name:<42} — {s.additivity_caveat[:60]}...")

    # 5. CSV
    out_path = Path(__file__).parent / "bdg_decoherence_channels_matrix.csv"
    with out_path.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scenario", "variant", "p_acc", "suppression_total",
                    "in_tension", "additivity_skipped",
                    "field_maturity", "confidence",
                    "operating_conditions",
                    "measurement_precision_factor"])
        for pred in all_predictions:
            scenario = next(s for s in SCENARIOS if s.name == pred.scenario)
            w.writerow([
                pred.scenario, pred.variant,
                f"{pred.p_acc:.6f}", f"{pred.suppression_total:.6f}",
                int(pred.in_tension), int(pred.additivity_skipped),
                scenario.field_maturity, scenario.confidence,
                scenario.operating_conditions,
                f"{scenario.measurement_precision_factor:.3f}",
            ])
    print(f"\n  Variant matrix CSV written to: {out_path}")

    # 6. Closing
    print("\n" + "=" * 78)
    print("POST-V2 VERDICT")
    print("=" * 78)
    n_falsified_strong = sum(
        1 for v in VARIANTS
        if any(s > 3.0 for s in
               variant_per_channel_falsification(v, constraints).values())
    )
    print(f"""\
Of {len(VARIANTS)} enumerated Dict-D variants, {n_falsified_strong} are FALSIFIED at >3σ
by per-channel engineered-condition measurements. Each touches at least
one of {{gas, BB_self, trap_photon_recoil}} — all channels for which
the Lindblad-vs-data agreement is published at 10-15% precision in
clean engineered runs.

The kernel-structural conjecture μ=d=4-universally is therefore
broadly closed by direct measurement. The remaining escape routes are:

  1. A non-universal μ-dictionary where μ(scenario) varies and lands
     in the saturated (P_acc → 1) regime for all measured scenarios.
     This is the open RA-OPEN-MU-ESTIMATOR-001 question.

  2. A filter that touches ONLY channels for which no high-precision
     per-channel engineered measurement exists (spontaneous emission
     and laser phase noise are candidates). But these are single-photon
     events, not multi-vertex Step-4 actualization candidates by any
     natural reading — so the kernel-structural motivation for the
     filter doesn't naturally land there.

  3. Dict-D is wrong (the conjecture μ=d=4 doesn't survive even
     before deriving μ from RA principles).

This is a real and substantive negative result. The post-v1
"narrowing of escape routes" finding was an artifact of the
cumulative-Γ analysis being the wrong analytical framing; the v2
per-channel framing closes the question much more cleanly.""")


if __name__ == "__main__":
    main()
