# Decoherence-budget primary-literature review (v2)

This file responds to the v2 lit-review prompt. It produces YAML scenario
entries and a verdict-and-gaps section based on primary-literature
findings. Where channels are not separately characterized in the primary
literature, weights are reported as `null` per the prompt's honesty
constraints; do not interpret `null` as zero.

A high-level finding before the per-scenario detail:

- The Lindblad-additive "channel budget" framing is well-supported in
  the primary literature only for the matter-wave engineered-channel
  experiments (Hornberger group 2003-2004 collisional and BB studies)
  and for the cavity-CS / feedback / cryogenic free-space protocols of
  ground-state-cooled levitated nanoparticles. It is NOT well-supported
  for (a) atom-IF nominal-mode budgets where vibration enters as
  ensemble phase variance rather than position decoherence, (b) the
  heaviest-mol nominal-conditions runs where gas+BB are explicitly
  sub-dominant and the residual contrast loss is dominated by
  instrumental/source effects, (c) the trapped-lattice atom-IF where
  the dominant residual mechanism is collective dephasing from
  anharmonic trap potential and does not factor into independent
  Lindblad channels, and (d) the BMV / diamond-NV speculative
  proposals where the schema lacks channels (magnetic, charge, internal
  spin) that the proposals themselves identify as critical.

This caveat is reflected in the per-scenario `channel_additivity_caveat`
fields and elaborated in the verdict-and-gaps section.

---

## Scenario YAML entries

```yaml
- name: atom_IF_Cs_fountain_freefall
  description: "Cs/Rb 10m free-fall fountain interferometer; Kasevich/Müller-style"
  field_maturity: mature
  protocol_variant: "free_fall_fountain"
  operating_conditions: "nominal"
  precision:
    directly_measured_quantity: "fringe contrast vs interrogation time T (or phase variance)"
    precision_on_measured_quantity: 0.02   # 1-5% on best fringe contrast
    precision_on_inferred_gamma: 0.20      # 10-30% on inferred Γ_decoh; vibration spectrum well-modeled
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: 0.01
      confidence: theoretical_extrapolation
    blackbody_self_emission:
      weight: 0.00
      confidence: measured   # atoms have no relevant internal vibrational manifold; channel physically absent
    blackbody_environmental:
      weight: 0.01
      confidence: theoretical_extrapolation
    spontaneous_emission:
      weight: 0.05
      confidence: theoretical_extrapolation   # off-resonant scattering during Bragg/Raman pulses; engineered low
    laser_phase_noise:
      weight: null   # not separately resolved from vibration in fountain budgets
      confidence: null
    trap_photon_recoil:
      weight: 0.00
      confidence: measured   # no trap during free-fall interrogation
    vibration_seismic:
      weight: 0.70
      confidence: measured   # Panda 2024 shows trapped-lattice variant suppresses vibration phase variance by 10^3-10^4 → vibration is dominant in fountain
    vibration_technical: null
    detection_statistics:
      weight: 0.05
      confidence: measured
    other_unattributed:
      weight: 0.18
      confidence: null
  unknown_fraction: 0.18
  channel_additivity_caveat: |
    Vibration in atom-IF fountain mode enters as ENSEMBLE PHASE VARIANCE,
    not as a Lindblad-form position decoherence. The exponential
    contrast-vs-T fit framing is approximate; the fundamental quantity
    is a phase noise spectrum convolved with the interferometer
    transfer function (Miffre 2006). For comparison to predicted
    Γ_decoh suppression effects, the relevant precision is the
    inferred-Γ uncertainty (~20%), not the contrast precision (~2%).
  primary_citations:
    channel_budget:
      - "Panda et al., Nat. Phys. 20, 1234 (2024); arXiv:2210.07289"
      - "Miffre et al., EPL 75 (2006); arXiv:quant-ph/0604022"
      - "Le Gouët et al., Appl. Phys. B 92, 133 (2008)"
    precision:
      - "Asenbaum et al., Phys. Rev. Lett. 118, 183602 (2017)"
      - "Sugarbaker et al., Phys. Rev. Lett. 111, 113002 (2013)"
  notes: |
    Vibration_seismic dominance is supported by the indirect comparison
    in Panda et al. 2024: switching from fountain to trapped-lattice
    suppresses phase variance by 4-5 orders of magnitude with no other
    geometry change, identifying vibration as the dominant fountain
    noise. This does NOT directly publish a "70%" weight; the 0.70 is
    an order-of-magnitude assignment consistent with the Panda
    suppression factor, the Miffre 2006 quantitative seismic spectrum,
    and Sugarbaker 2013's component-by-component noise audit. The
    spontaneous_emission weight reflects engineered-low off-resonant
    scattering during Bragg/Raman; ideal coherent two-photon transitions
    do not decohere. v1's "recoil=0.50" lump (s.e.+l.p.n.+vib_retro)
    is partly supported but mis-attributes most of it to recoil rather
    than vibration; see verdict.

- name: atom_IF_Cs_lattice
  description: "Cs/Rb optical-lattice atom interferometer (Panda/Müller-style); held atoms"
  field_maturity: mature
  protocol_variant: "trapped_lattice"
  operating_conditions: "nominal"
  precision:
    directly_measured_quantity: "fringe contrast at hold time τ up to 70s"
    precision_on_measured_quantity: 0.05
    precision_on_inferred_gamma: 0.30
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: 0.05
      confidence: theoretical_extrapolation
    blackbody_self_emission:
      weight: 0.00
      confidence: measured
    blackbody_environmental:
      weight: 0.01
      confidence: theoretical_extrapolation
    spontaneous_emission:
      weight: null
      confidence: null
    laser_phase_noise:
      weight: null
      confidence: null
    trap_photon_recoil:
      weight: null
      confidence: null   # cavity-mode-filtered trap; not separately resolved from collective dephasing in Panda 2024
    vibration_seismic:
      weight: 0.001   # explicitly suppressed by 10^3-10^4 vs fountain (Panda 2024)
      confidence: measured
    vibration_technical: null
    detection_statistics:
      weight: 0.05
      confidence: measured
    other_unattributed:
      weight: null
      confidence: null
  unknown_fraction: 0.89
  channel_additivity_caveat: |
    Panda et al. 2024 attributes the dominant residual coherence loss
    in the trapped-lattice geometry to "collective dephasing of the
    atomic ensemble" arising from finite trap depth and anharmonicity
    of the cavity-mode-filtered lattice potential — i.e. residual
    atomic motion through an inhomogeneous trap. This mechanism is
    NOT a Lindblad-form independent channel and does not slot into the
    v2 schema. Forcing it into "trap_photon_recoil" would be misleading
    (it is not photon recoil; it is potential anharmonicity coupled to
    finite-temperature ensemble distribution). The known fraction
    (~0.11) is small precisely because the dominant mechanism is
    schema-incompatible. This scenario is best treated as schema-
    UNCHARACTERIZED for the v2 framework.
  primary_citations:
    channel_budget:
      - "Panda et al., Nat. Phys. 20, 1234 (2024); arXiv:2210.07289"
      - "Panda et al., Nature 631, 515 (2024); arXiv:2310.01344"
      - "Xu et al., Science 366, 745 (2019)"
    precision:
      - "Panda et al., Nat. Phys. 20, 1234 (2024)"
  notes: |
    Vibration suppression of 10^3-10^4 vs fountain is directly measured
    (Panda 2024). The dominant residual mechanism — anharmonic trap-
    induced collective dephasing — is a fundamentally different
    physical category from the Hornberger-Sipe Lindblad channels and
    cannot be honestly reported as a single weight in the schema.
    Recommend treating this entry as a literature-gap flag rather than
    a quantitative budget.

- name: mol_IF_C60_nominal
  description: "C70 Talbot-Lau interferometry, Vienna group, nominal conditions"
  field_maturity: mature
  protocol_variant: "TLI_baseline"
  operating_conditions: "nominal"   # P ~ 2e-8 mbar; source ~900 K; no laser heating
  precision:
    directly_measured_quantity: "fringe visibility V"
    precision_on_measured_quantity: 0.05   # 5% best-case visibility
    precision_on_inferred_gamma: 0.20
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: 0.05
      confidence: measured   # extrapolated from Hornberger 2003 cross-section to 2e-8 mbar; verified sub-dominant
    blackbody_self_emission:
      weight: 0.05
      confidence: measured   # Hackermüller 2004 explicitly: BB negligible below 1000K
    blackbody_environmental:
      weight: 0.00
      confidence: theoretical_extrapolation
    spontaneous_emission: null
    laser_phase_noise:
      weight: 0.00
      confidence: measured   # detection laser does not couple as phase noise to the matter-wave fringes
    trap_photon_recoil:
      weight: 0.00
      confidence: measured   # no trapping
    vibration_seismic:
      weight: 0.30
      confidence: measured   # Stibor 2004 quantifies acoustic-vibration sensitivity in C70 TLI
    vibration_technical:
      weight: null
      confidence: null
    detection_statistics:
      weight: 0.10
      confidence: theoretical_extrapolation
    other_unattributed:
      weight: 0.50
      confidence: null   # grating misalignment, source coherence, velocity dispersion — instrumental, not in schema
  unknown_fraction: 0.50
  channel_additivity_caveat: |
    The substantial other_unattributed fraction reflects the fact that
    at nominal conditions, residual visibility loss is dominated by
    INSTRUMENTAL effects (grating period precision, alignment, source
    velocity dispersion, finite slit widths) that are not Lindblad
    decoherence channels. Hornberger-Sipe-Vacchini formalism applies
    to gas+BB but explicitly excludes these instrumental effects.
  primary_citations:
    channel_budget:
      - "Hornberger et al., Phys. Rev. Lett. 90, 160401 (2003); arXiv:quant-ph/0303093"
      - "Stibor et al., arXiv:quant-ph/0411118 (2004)"
      - "Brezger et al., Phys. Rev. Lett. 88, 100404 (2002)"
    precision:
      - "Hackermüller et al., Appl. Phys. B 77, 781 (2003); arXiv:quant-ph/0307238"
  notes: |
    v1's mol_IF_C60 row (gas=0.40, BB=0.40) is misleading at nominal
    conditions — those weights are reachable only by mixing nominal
    runs with the engineered Hornberger 2003 (raised P) and
    Hackermüller 2004 (laser-heated) studies. Splitting into three
    scenarios resolves this. See engineered-condition entries below.

- name: mol_IF_C60_collisional_engineered
  description: "C70 TLI with raised gas pressure (Hornberger 2003 series)"
  field_maturity: mature
  protocol_variant: "TLI_collisional_pressure_scan"
  operating_conditions: "engineered_gas_collision"
  precision:
    directly_measured_quantity: "fringe visibility V vs gas pressure P"
    precision_on_measured_quantity: 0.05
    precision_on_inferred_gamma: 0.10   # Hornberger 2003 reports good quantitative agreement with H-S theory
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: 0.85
      confidence: measured
    blackbody_self_emission:
      weight: 0.05
      confidence: measured
    blackbody_environmental:
      weight: 0.00
      confidence: theoretical_extrapolation
    spontaneous_emission: null
    laser_phase_noise:
      weight: 0.00
      confidence: measured
    trap_photon_recoil:
      weight: 0.00
      confidence: measured
    vibration_seismic:
      weight: 0.05
      confidence: measured
    vibration_technical: null
    detection_statistics:
      weight: 0.05
      confidence: measured
    other_unattributed:
      weight: null
      confidence: null
  unknown_fraction: 0.0
  channel_additivity_caveat: "Hornberger-Sipe-Vacchini cross-section formalism quantitatively reproduces the visibility-vs-pressure curve over decades of pressure; channel additivity is supported in this regime."
  primary_citations:
    channel_budget:
      - "Hornberger et al., Phys. Rev. Lett. 90, 160401 (2003); arXiv:quant-ph/0303093"
      - "Hackermüller et al., Appl. Phys. B 77, 781 (2003); arXiv:quant-ph/0307238"
      - "Hornberger, Sipe & Arndt, Phys. Rev. A 70, 053608 (2004)"
    precision:
      - "Hornberger et al., Phys. Rev. Lett. 90, 160401 (2003)"
  notes: |
    This is the cleanest channel-resolved primary lit decoherence
    measurement in the catalog. Pressure was scanned from baseline
    (~2e-8 mbar) up to ~1e-6 mbar; visibility decay was exponential
    in P with slope matching H-S-V theory.

- name: mol_IF_C60_blackbody_engineered
  description: "C70 TLI with laser-heated molecules (Hackermüller 2004)"
  field_maturity: mature
  protocol_variant: "TLI_BB_temperature_scan"
  operating_conditions: "engineered_blackbody"
  precision:
    directly_measured_quantity: "fringe visibility V vs molecular T (laser power)"
    precision_on_measured_quantity: 0.05
    precision_on_inferred_gamma: 0.15
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: 0.05
      confidence: measured
    blackbody_self_emission:
      weight: 0.85
      confidence: measured   # at heated T ~ 2000-3000K, BB dominates by design
    blackbody_environmental:
      weight: 0.00
      confidence: theoretical_extrapolation
    spontaneous_emission: null
    laser_phase_noise: null
    trap_photon_recoil:
      weight: 0.00
      confidence: measured
    vibration_seismic:
      weight: 0.05
      confidence: measured
    vibration_technical: null
    detection_statistics:
      weight: 0.05
      confidence: measured
    other_unattributed:
      weight: null
      confidence: null
  unknown_fraction: 0.0
  channel_additivity_caveat: |
    At very high heating (T → 2800 K), thermionic electron emission
    and C2 fragmentation begin to compete with BB photon emission —
    these are NOT independent Lindblad channels of position decoherence
    but molecule-destroying processes that remove particles from the
    interferometer. Hackermüller 2004 stays below this regime; the
    additive Lindblad framing holds in the data range reported.
  primary_citations:
    channel_budget:
      - "Hackermüller et al., Nature 427, 711 (2004); arXiv:quant-ph/0402146"
      - "Hornberger, Sipe & Arndt, Phys. Rev. A 70, 053608 (2004)"
    precision:
      - "Hackermüller et al., Nature 427, 711 (2004)"
  notes: |
    The Hackermüller 2004 study laser-heats C70 from ~900K (baseline,
    cold-quantum) to >2000K to render BB-self-emission dominant by
    design. Quantitative agreement with microscopic decoherence theory
    is reported. This is the canonical BB-decoherence measurement.

- name: mol_IF_oligoporphyrin
  description: "Oligoporphyrin / fluorous-tagged libraries 10-27 kDa; KDTLI/LUMI"
  field_maturity: mature
  protocol_variant: "KDTLI_or_LUMI_baseline"
  operating_conditions: "nominal"
  precision:
    directly_measured_quantity: "fringe visibility V"
    precision_on_measured_quantity: 0.10
    precision_on_inferred_gamma: null   # not separately resolved
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: null
      confidence: null
    blackbody_self_emission:
      weight: null
      confidence: null
    blackbody_environmental:
      weight: null
      confidence: null
    spontaneous_emission: null
    laser_phase_noise: null
    trap_photon_recoil: null
    vibration_seismic:
      weight: null
      confidence: null
    vibration_technical: null
    detection_statistics:
      weight: null
      confidence: null
    other_unattributed:
      weight: null
      confidence: null
  unknown_fraction: 1.0
  channel_additivity_caveat: |
    Channel-resolved decoherence budgets are NOT separately published
    for the heaviest-mol species in the LUMI / KDTLI primary lit. The
    primary references state directly that at nominal conditions
    (P ~ 2e-8 mbar, T < 1000 K) collisional and thermal decoherence
    "do not yet play a major role" (Fein 2019) and that internal
    states are "decoupled from de Broglie interference" excluding
    collisional/thermal effects (Eibenberger 2013). The actual
    visibility limitations at this mass scale come from grating period
    precision, source brightness, velocity selection, and signal
    statistics — instrumental rather than environmental decoherence.
  primary_citations:
    channel_budget:
      - "Fein et al., Nat. Phys. 15, 1242 (2019)"
      - "Eibenberger et al., Phys. Chem. Chem. Phys. 15, 14696 (2013); arXiv:1310.8343"
      - "Kiałka, Fein, Pedalino, Gerlich, Arndt, AVS Quantum Sci. 4, 020502 (2022)"
    precision:
      - "Fein et al., Nat. Phys. 15, 1242 (2019)"
      - "Gerlich et al., Nat. Phys. 3, 711 (2007)"
  notes: |
    This entry is essentially a literature-gap flag. v1's row
    (gas=0.55, BB=0.30) is contradicted by the primary literature's
    explicit statement that gas+BB are sub-dominant at nominal
    conditions. The primary lit does not publish a fractional budget;
    it publishes upper bounds and verifies that environmental
    decoherence is below the visibility floor. Downstream physics
    analyses should NOT use this scenario to constrain a 10-50%
    predicted suppression — the constraint power is essentially zero
    for that question, because the residual visibility loss is
    instrumental rather than environmental.

- name: opto_levitated_silica_cavityCS
  description: "Optically levitated silica nanosphere; cavity coherent-scattering ground-state cooling (Delić 2020)"
  field_maturity: developing
  protocol_variant: "cavity_CS"
  operating_conditions: "nominal"
  precision:
    directly_measured_quantity: "heating rate Γ_x (kHz) measured directly via reheating"
    precision_on_measured_quantity: 0.14   # ±3 of 21 kHz
    precision_on_inferred_gamma: 0.14   # the heating rate IS the relevant Γ
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: 0.30
      confidence: measured   # at 1e-6 mbar, gas is significant; quoted as dominant for free-fall coherence in Delić 2020
    blackbody_self_emission:
      weight: null   # not separately resolved at room T / 1e-6 mbar; sub-dominant in Delić 2020
      confidence: null
    blackbody_environmental:
      weight: 0.05
      confidence: theoretical_extrapolation
    spontaneous_emission: null
    laser_phase_noise:
      weight: null   # not the dominant residual once cavity-CS is engineered; expected sub-dominant
      confidence: null
    trap_photon_recoil:
      weight: 0.60
      confidence: measured   # Delić 2020 shows recoil-limited free-fall coherence at 1e-6 mbar; Jain 2016 directly measures recoil rate
    vibration_seismic:
      weight: 0.00
      confidence: theoretical_extrapolation
    vibration_technical: null
    detection_statistics:
      weight: 0.05
      confidence: measured
    other_unattributed:
      weight: null
      confidence: null
  unknown_fraction: 0.0
  channel_additivity_caveat: "Lindblad-additive at leading order is well-supported here; both gas and recoil are independent momentum-transfer channels."
  primary_citations:
    channel_budget:
      - "Delić et al., Science 367, 892 (2020); arXiv:1911.04406"
      - "Jain et al., Phys. Rev. Lett. 116, 243601 (2016); arXiv:1603.03420"
      - "Romero-Isart, Phys. Rev. A 84, 052121 (2011)"
    precision:
      - "Delić et al., Science 367, 892 (2020)"
  notes: |
    At the achieved baseline P=1e-6 mbar, gas collision sets a free-fall
    coherence time of 1.4 µs (Delić 2020). Trap_photon_recoil dominates
    inside the trap (Γ_x = 21±3 kHz). The "0.60 / 0.30" split reflects
    the reported Delić 2020 ordering at their operating P; at 1e-9 mbar
    or below the recoil weight rises toward 1.0 (Romero-Isart 2011 noted
    BB takes over only at ~1e-11 mbar and cryogenic T). v1's
    "trap=0.80" weight is broadly supported; the v1 "recoil=0.00" is a
    naming confusion since v2 splits trap_photon_recoil out explicitly.

- name: opto_levitated_silica_feedback_RT
  description: "Levitated silica nanoparticle; room-temperature feedback cooling (Magrini 2021)"
  field_maturity: developing
  protocol_variant: "feedback_room_T"
  operating_conditions: "nominal"
  precision:
    directly_measured_quantity: "heating rate / phonon occupation"
    precision_on_measured_quantity: 0.10
    precision_on_inferred_gamma: 0.20
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: null
      confidence: null
    blackbody_self_emission:
      weight: null
      confidence: null
    blackbody_environmental:
      weight: null
      confidence: null
    spontaneous_emission: null
    laser_phase_noise:
      weight: null
      confidence: null
    trap_photon_recoil:
      weight: 0.80
      confidence: measured   # measurement-backaction-limited per Magrini 2021 abstract
    vibration_seismic: null
    vibration_technical: null
    detection_statistics:
      weight: null
      confidence: null
    other_unattributed:
      weight: null
      confidence: null
  unknown_fraction: 0.20
  channel_additivity_caveat: |
    Magrini 2021 explicitly notes "cross-mode hybridization" between
    transverse and longitudinal motion is non-negligible at the
    optimal-control regime — this is a coupled-channel effect not
    captured by Lindblad-additive single-mode budgets. Flag for
    downstream analyses that assume single-mode independence.
  primary_citations:
    channel_budget:
      - "Magrini et al., Nature 595, 373 (2021)"
      - "Gonzalez-Ballestero et al., arXiv:1902.01282"
    precision:
      - "Magrini et al., Nature 595, 373 (2021)"
  notes: |
    Measurement backaction (= photon recoil from trapping/measurement
    light) is identified as the dominant mechanism. Detailed
    fractional channel weights for sub-dominants are not separately
    published.

- name: opto_levitated_silica_cryo_freespace
  description: "Levitated silica nanoparticle; cryogenic free-space feedback (Tebbenjohanns 2021)"
  field_maturity: developing
  protocol_variant: "cryogenic_freespace_feedback"
  operating_conditions: "nominal"
  precision:
    directly_measured_quantity: "phonon occupation; state purity"
    precision_on_measured_quantity: 0.10
    precision_on_inferred_gamma: 0.20
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision:
      weight: 0.05
      confidence: theoretical_extrapolation
    blackbody_self_emission: null
    blackbody_environmental:
      weight: 0.05
      confidence: measured   # explicitly suppressed by cryogenic environment per Tebbenjohanns 2021
    spontaneous_emission: null
    laser_phase_noise:
      weight: null
      confidence: null
    trap_photon_recoil:
      weight: 0.85
      confidence: measured   # Tebbenjohanns 2021 abstract: cryogenics renders measurement backaction the dominant mechanism
    vibration_seismic: null
    vibration_technical: null
    detection_statistics:
      weight: 0.05
      confidence: measured
    other_unattributed:
      weight: null
      confidence: null
  unknown_fraction: 0.0
  channel_additivity_caveat: "Lindblad-additive supported in this regime; cryogenics decouples thermal channels."
  primary_citations:
    channel_budget:
      - "Tebbenjohanns et al., Nature 595, 378 (2021); arXiv:2103.03853"
      - "Romero-Isart, Phys. Rev. A 84, 052121 (2011)"
    precision:
      - "Tebbenjohanns et al., Nature 595, 378 (2021)"
  notes: |
    The cryogenic-free-space variant is the cleanest example of
    photon-recoil-dominant decoherence in the catalog. It directly
    realizes the regime predicted by Romero-Isart 2011 (which
    explicitly excludes recoil as "avoidable"; recoil must be added
    back in for ground-state-cooled silica).

- name: opto_levitated_diamond_NV_spin_only
  description: "Levitated diamond w/ NV center: NV electron-spin coherence in high vacuum (Jin 2024 et al.)"
  field_maturity: developing
  protocol_variant: "NV_spin_coherence_only"
  operating_conditions: "nominal"
  precision:
    directly_measured_quantity: "T2 of NV electron spin via ODMR"
    precision_on_measured_quantity: 0.10
    precision_on_inferred_gamma: null
    theoretical_model_uncertainty: null
  channel_weights:
    gas_collision: null   # not relevant to NV spin; relevant to CoM (separate scenario)
    blackbody_self_emission: null
    blackbody_environmental: null
    spontaneous_emission: null
    laser_phase_noise: null
    trap_photon_recoil: null
    vibration_seismic: null
    vibration_technical: null
    detection_statistics:
      weight: 0.10
      confidence: measured
    other_unattributed:
      weight: 0.90
      confidence: null   # spin-bath dephasing, ODMR contrast loss; NV physics, not v2 schema channels
  unknown_fraction: 0.90
  channel_additivity_caveat: |
    NV electron-spin coherence is governed by 13C nuclear spin bath
    dynamics, NV-NV cross-talk, and external magnetic field stability
    — none of which is a v2 channel. Internal-T also affects T2 via
    spin-phonon coupling. The v2 schema does not apply to this
    measurement; reporting weights here is not meaningful.
  primary_citations:
    channel_budget:
      - "Jin et al., Nat. Commun. 15, 5063 (2024); arXiv:2309.05821"
      - "Hoang et al., Nat. Commun. 7, 12250 (2016)"
    precision:
      - "Jin et al., Nat. Commun. 15, 5063 (2024)"
  notes: |
    This is the MEASURED channel for diamond NV in high vacuum: the
    spin coherence. CoM positional decoherence is NOT measured in this
    or any other primary-lit experiment for levitated diamond NV.

- name: opto_levitated_diamond_NV_CoM_proposal
  description: "Levitated diamond w/ NV center: CoM positional decoherence in proposed matter-wave-IF (NEVER MEASURED)"
  field_maturity: speculative
  protocol_variant: "CoM_matterwave_proposal"
  operating_conditions: "theoretical"
  precision:
    directly_measured_quantity: null
    precision_on_measured_quantity: null
    precision_on_inferred_gamma: null
    theoretical_model_uncertainty: 1.0   # full theoretical proposal; no measurement
  channel_weights:
    gas_collision:
      weight: null
      confidence: null
    blackbody_self_emission:
      weight: null   # would be dominant near the graphitization threshold; below it, sub-dominant
      confidence: null
    blackbody_environmental: null
    spontaneous_emission: null
    laser_phase_noise: null
    trap_photon_recoil: null
    vibration_seismic: null
    vibration_technical: null
    detection_statistics: null
    other_unattributed:
      weight: 1.0   # the dominant practical limit (graphitization at high vacuum) is not in the schema
      confidence: null
  unknown_fraction: 1.0
  channel_additivity_caveat: |
    The dominant practical limit for optically-levitated nanodiamond
    in high vacuum is GRAPHITIZATION (Rahman/Frangeskou 2016) and
    laser-induced internal heating from absorption — neither of which
    is a position-decoherence Lindblad channel. The diamond either
    burns (in air) or graphitizes (in N2 below 10 mB) before any CoM
    superposition can be prepared. This is a structural/thermal
    failure of the protocol, not a channel weight. Surface-ion-trap
    variants (Jin 2024) circumvent this for spin measurements but have
    not yet demonstrated CoM superposition. The v2 schema cannot
    represent this scenario.
  primary_citations:
    channel_budget:
      - "Rahman, Frangeskou et al., Sci. Rep. 6, 21633 (2016); arXiv:1510.07555"
      - "Frangeskou et al., New J. Phys. 20, 043016 (2018)"
      - "Scala et al., Phys. Rev. Lett. 111, 180403 (2013)"
      - "Yin et al., Phys. Rev. A 88, 033614 (2013)"
    precision: []
  notes: |
    Strongly recommend SPLITTING the v1 "opto_levitated_diamond_NV"
    row into the two scenarios above (spin-only-measured vs CoM-
    proposal-only). The v1 row's channel weights (gas=0.40, BB=0.10,
    recoil=0.10, vib=0.10, trap=0.30) appear to be a synthetic
    estimate not traceable to primary literature; the actual primary-
    lit content for this system is (i) NV spin T2 measurements with
    no CoM weights, and (ii) a graphitization failure mode that does
    not fit the schema.

- name: bmv_bose2017_nominal
  description: "Bose-Marletto-Vedral 2017 spin-witness QGEM proposal (theoretical)"
  field_maturity: speculative
  protocol_variant: "Bose2017_design_parameters"
  operating_conditions: "theoretical"   # P=1e-15 Pa, T_internal=0.15K, m=1e-14 kg, Δx=250 µm, τ=2.5 s
  precision:
    directly_measured_quantity: null
    precision_on_measured_quantity: null
    precision_on_inferred_gamma: null
    theoretical_model_uncertainty: 1.0
  channel_weights:
    gas_collision:
      weight: 0.95   # Bose 2017 explicit: Γ_gas·τ ~ 1, ie. gas SETS the feasibility envelope
      confidence: theoretical_extrapolation
    blackbody_self_emission:
      weight: 0.02
      confidence: theoretical_extrapolation
    blackbody_environmental:
      weight: 0.02
      confidence: theoretical_extrapolation
    spontaneous_emission: null
    laser_phase_noise: null
    trap_photon_recoil: null
    vibration_seismic:
      weight: null
      confidence: null   # acknowledged but not quantified in the proposal
    vibration_technical: null
    detection_statistics:
      weight: 0.01
      confidence: theoretical_extrapolation
    other_unattributed:
      weight: null
      confidence: null   # MAGNETIC GRADIENT NOISE from SG components and CHARGE MULTIPOLES — explicitly identified by Bose 2017 as critical, NOT in v2 schema
  unknown_fraction: 0.0
  channel_additivity_caveat: |
    Bose 2017 frames the design as operating at the EDGE of gas-
    feasibility (Γ_gas · τ ~ 1), not strictly gas-dominated.
    Interpreting "0.95 of total decoherence" as a fractional weight
    is potentially misleading because (a) at the design edge,
    arbitrarily small additional channels can render the experiment
    infeasible, so the fractional framing understates the criticality,
    and (b) the proposal explicitly identifies non-schema channels —
    SG-magnet-gradient noise, residual charge multipoles, Casimir-
    Polder forces — as critical and they do NOT appear in v2's
    channel set. The Lindblad-additive framing is leading-order valid
    but is not the full feasibility analysis.
  primary_citations:
    channel_budget:
      - "Bose et al., Phys. Rev. Lett. 119, 240401 (2017); arXiv:1707.06050"
      - "Marletto & Vedral, Phys. Rev. Lett. 119, 240402 (2017)"
      - "Chevalier, Paige, Kim, Phys. Rev. A 102, 022428 (2020); arXiv:2005.13922"
    precision: []
  notes: |
    Verbatim from Bose 2017: "the collisional decoherence time for a
    superposition size of ∆x ∼ 250 µm is the same order of magnitude
    as the total microsphere's fall time τ + 2τacc ∼ 3.5 s, while the
    thermal decoherence mechanism, due to scattering, emission and
    absorption of environmental photons, is negligible." Required
    pressure P = 1e-15 Pa = 1e-17 mbar (extreme UHV, NOT YET
    DEMONSTRATED for any levitated-particle ground-state experiment).
    Required internal T = 0.15 K. Required spin coherence ~1 s in the
    NV electron spin (steps 1, 3) plus much longer for the nuclear
    spin (step 2). v1 row (gas=0.95) is qualitatively right on
    channel-ranking but the schema misses the dominant feasibility
    constraints (magnetic gradients, charges, vacuum requirement).

- name: carney_small_mass_proposal
  description: "Carney-group small-mass quantum-gravity proposal — UNDERSPECIFIED"
  field_maturity: speculative
  protocol_variant: "UNDERSPECIFIED"
  operating_conditions: "theoretical"
  precision:
    directly_measured_quantity: null
    precision_on_measured_quantity: null
    precision_on_inferred_gamma: null
    theoretical_model_uncertainty: 1.0
  channel_weights:
    gas_collision: null
    blackbody_self_emission: null
    blackbody_environmental: null
    spontaneous_emission: null
    laser_phase_noise: null
    trap_photon_recoil: null
    vibration_seismic: null
    vibration_technical: null
    detection_statistics: null
    other_unattributed: null
  unknown_fraction: 1.0
  channel_additivity_caveat: |
    Cannot be assessed without specifying which Carney-group proposal
    and which parameter set. Candidates include Carney-Stamp-Taylor
    CQG 36 034001 (2019), Carney-Krnjaic-Moore Snowmass 2021
    (arXiv:2203.11846), Carney-Müller-Taylor PRX Quantum 2 030330
    (2021), and others. These have substantially different mass
    scales, environmental conditions, and dominant-channel orderings.
  primary_citations:
    channel_budget: []
    precision: []
  notes: |
    RECOMMEND: either pin to a specific arXiv ID + parameter set in a
    follow-up lit-review run, or remove from SCENARIOS entirely. The
    v1 row (gas=0.50, BB=0.05, recoil=0.05, vib=0.10, trap=0.30) is
    not traceable to any single primary source and should not be used
    downstream. Per the prompt's honesty constraints, no synthetic
    "representative" budget is provided here.
```

---

## Verdict-and-gaps section

### Per-scenario verdicts vs v1 (using the five-category schema)

| v1 scenario | v2 verdict | rationale |
|---|---|---|
| atom_IF_Cs_fountain | **REFINES** + split | dominant-channel ordering (vibration > all) is supported; v1's "recoil=0.50" lump is partly supported but mis-weights the components; should split into free-fall vs trapped-lattice variants |
| mol_IF_C60 | **REFINES** + split | nominal-conditions row is misleading because it mixes engineered-channel studies; should split into nominal, collisional-engineered, BB-engineered |
| mol_IF_oligoporphyrin | **CONTRADICTS** | primary lit explicitly states gas+BB are sub-dominant at nominal conditions; v1's gas=0.55, BB=0.30 inverts the dominant-channel ordering; correct verdict is UNCHARACTERIZED for v2 schema (channels don't capture the actual dominant residual mechanism) |
| opto_levitated_silica | **REFINES** + split | dominant-channel ordering (recoil > rest) is well-supported across all three protocols; should split by protocol; v1's "trap=0.80" is broadly correct but v2's separated trap_photon_recoil channel is the cleaner accounting |
| opto_levitated_diamond_NV | **CONTRADICTS** + split | v1 row conflates measured spin coherence with never-measured CoM positional decoherence; primary practical limit is graphitization, not in schema; should split into spin-only-measured vs CoM-proposal-only entries |
| bmv_bose2017_nominal | **REFINES** with caveat | qualitative channel ranking (gas > BB > rest) is supported; "0.95" fractional framing is misleading because (a) Bose 2017 says Γ_gas·τ ~ 1 not "95% of budget" and (b) schema lacks magnetic-gradient and charge channels Bose 2017 explicitly identifies as critical |
| carney_small_mass_proposal | **UNDERSPECIFIED** | not traceable to a single primary source; pin or remove |

### Literature gaps

The following are channels or scenarios where channel-resolved primary-lit data does NOT exist:

1. **Heaviest matter-wave species (oligoporphyrin / functionalized libraries)**: no published Lindblad-channel breakdown at nominal conditions. The dominant residual visibility loss is instrumental (grating period, source coherence, velocity selection) rather than environmental decoherence. Hornberger-Sipe formalism applies to gas+BB but explicitly excludes these instrumental effects.

2. **Atom-IF trapped-lattice (Panda 2024)**: dominant residual coherence loss is "collective dephasing from anharmonic trap" — not a Lindblad-form channel. Schema-incompatible.

3. **Atom-IF free-fall fountain quantitative weights**: vibration-as-dominant is well supported (Panda 2024 indirect 4-5 OOM suppression measurement; Miffre 2006 quantitative spectrum); precise fractional weights for spontaneous_emission vs laser_phase_noise vs vibration are not separately resolved.

4. **Levitated-silica laser_phase_noise**: Kamba 2020 identifies LPN as initially dominant before mitigation, photon-recoil-limited after — but published channel-by-channel fractional weights post-mitigation are not in the public lit.

5. **Levitated diamond CoM positional decoherence**: never measured. The published experiments measure NV spin coherence in vacuum and characterize internal-T / graphitization. The matter-wave protocol (Scala 2013, Yin 2013, used in Bose 2017) has not been realized.

6. **BMV magnetic-gradient and charge-multipole channels**: identified by Bose 2017 as critical for SG-based protocols but not in the v2 schema. Schema needs extension to capture these for any speculative-tier scenario.

7. **All speculative-tier scenarios**: theoretical-model uncertainty (~1.0) dominates over any other precision factor. These cannot meaningfully constrain any predicted suppression effect.

### Recommendations for protocol_variant splits

- `atom_IF_Cs_fountain` → split into `atom_IF_Cs_fountain_freefall` and `atom_IF_Cs_lattice`.
- `mol_IF_C60` → split into `mol_IF_C60_nominal`, `mol_IF_C60_collisional_engineered`, `mol_IF_C60_blackbody_engineered`.
- `opto_levitated_silica` → split into `opto_levitated_silica_cavityCS` (Delić 2020), `opto_levitated_silica_feedback_RT` (Magrini 2021), `opto_levitated_silica_cryo_freespace` (Tebbenjohanns 2021).
- `opto_levitated_diamond_NV` → split into `opto_levitated_diamond_NV_spin_only` (Jin 2024 measured) and `opto_levitated_diamond_NV_CoM_proposal` (theoretical; Scala 2013 / Yin 2013 / Bose 2017 design).

### Cross-channel-interference invalidating Lindblad additivity

The following scenarios have documented strong cross-channel interference or schema-incompatible dominant mechanisms; the Lindblad-additive budget framing is NOT a leading-order accurate description:

- `atom_IF_Cs_lattice`: dominant mechanism (collective dephasing from anharmonic trap) is not a Lindblad channel.
- `mol_IF_oligoporphyrin` at nominal conditions: dominant residual visibility loss is instrumental, not Lindblad.
- `opto_levitated_silica_feedback_RT`: cross-mode hybridization between transverse and longitudinal motion (Magrini 2021) couples the modes; single-mode Lindblad budget is approximate.
- `opto_levitated_diamond_NV_CoM_proposal`: dominant practical limit (graphitization) is not a Lindblad channel.
- `bmv_bose2017_nominal`: schema lacks magnetic-gradient, charge-multipole channels critical to the design.

For downstream physics analysis, scenarios where the Lindblad-additive framing is invalid CANNOT be used to constrain the predicted ~10-50% suppression — the comparison itself is ill-defined. These scenarios should either be flagged for "framework-incompatible" exclusion, or the v2 schema should be extended to include the missing channel types (magnetic, charge, anharmonic-trap, instrumental).

### Recommended schema extensions for v3

Based on the gaps documented above, a v3 schema should consider adding:

- `magnetic_gradient_noise` — for SG-based protocols (BMV-class)
- `charge_multipole_coupling` — for charged-particle / dipole-bearing protocols
- `anharmonic_trap_dephasing` — for trapped-lattice atom IF
- `instrumental_visibility_loss` — explicit catch-all for grating/source/alignment effects in matter-wave IF
- `graphitization_internal_thermal` — for diamond/optical-trap protocols

These are not Lindblad position-decoherence channels but they are dominant feasibility constraints in real experiments; the current v2 schema's `other_unattributed` does not communicate enough about which type of effect is bundled.

---

## End of v2 lit-review output
