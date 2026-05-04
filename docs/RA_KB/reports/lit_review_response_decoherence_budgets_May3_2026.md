# Decoherence-budget literature review — Claude chat response (May 3, 2026)

> **Provenance.** This is the response to the prompt at
> `lit_review_prompt_decoherence_budgets_May3_2026.md`. Returned by a fresh
> Claude chat with web-browse capability. Citations are primary-source.
> Used to refine `src/RA_AQFT/bdg_decoherence_channels.py` `SCENARIOS`
> catalog and the empirical-tension verdict on Dict-D-style BDG-suppression
> conjectures.
>
> **Status.** Verbatim record of the lit-review chat output. Treated as
> primary-source-cited; supersedes the training-data-synthesized values in
> the previous version of `bdg_decoherence_channels.py`.

---

## YAML output

```yaml
- name: atom_IF_Cs_fountain
  description: "Long-baseline Rb/Cs atom fountain interferometers (Stanford 10m fountain, Berkeley Müller group, MAGIS-style); see Asenbaum 2017, Panda 2023"
  field_maturity: mature
  directly_measured_quantity: "interferometer fringe contrast vs interrogation time T (and inferred Γ_decoh from contrast model)"
  measurement_precision_factor: 0.10
  channel_weights:
    gas_collision: 0.02
    blackbody: 0.01
    photon_recoil: 0.30   # spontaneous emission + Raman/Bragg pulse decoherence; NOT coherent beamsplitter recoil
    vibration: 0.55       # dominant in free-fall geometries
    trap_photon: 0.00     # not applicable to fountain mode
    other_unattributed: 0.12   # detection shot noise, magnetic field gradients, AC Stark shifts, wavefront aberrations
  primary_citations:
    channel_budget:
      - "Panda et al., arXiv:2301.13315 (2023): trapped-lattice IF suppresses vibration phase variance by 3-4 orders of magnitude, identified as 'the dominant noise source in atom-interferometric gravimeters'"
      - "Le Gouët et al., Appl. Phys. B 92 (2008), hal-00203007: detailed phase-noise analysis of compact atom gravimeter; vibration compensation via co-located seismometer"
      - "Miffre et al., EPL (2006), arXiv:quant-ph/0604028: model calculation of seismic-noise-induced phase noise in Mach-Zehnder atom IF"
      - "Hogan, Johnson, Kasevich, arXiv:0806.3261 (2008): light-pulse atom interferometry review with noise-budget discussion"
    precision:
      - "Asenbaum et al., Phys. Rev. Lett. 118, 183602 (2017), DOI:10.1103/PhysRevLett.118.183602"
      - "Sugarbaker et al., Phys. Rev. Lett. 111, 113002 (2013): single-shot phase/contrast readout via phase shear"
      - "Kovachy et al., Nature 528, 530 (2015), DOI:10.1038/nature16155: half-metre-scale superposition"
  notes: |
    The "photon_recoil" label in the original schema is conceptually misleading
    here: in atom IF, coherent Bragg/Raman beamsplitter pulses do NOT cause
    decoherence in the ideal limit. The decoherence-relevant photon channels
    are spontaneous emission from off-resonant scattering and laser
    phase/intensity noise, both bundled here as 0.30. Vibration dominates in
    free-fall fountain mode (Panda 2023, Xu 2019 explicitly identify it as
    such). The Berkeley optical-lattice approach (Panda 2023) is a different
    operating regime where vibration is suppressed by orders of magnitude and
    the noise budget shifts toward laser-related channels. Existing table's
    photon_recoil=0.50 / vibration=0.40 reverses the dominant-channel ordering
    documented in the literature.

- name: mol_IF_C60
  description: "C60/C70 fullerene Talbot-Lau interferometry (Arndt group, Vienna); see Hackermüller 2003, Hornberger 2003"
  field_maturity: mature
  directly_measured_quantity: "fringe visibility V vs background-gas pressure P (collisional studies) or vs molecular internal temperature T (BB studies)"
  measurement_precision_factor: 0.10
  channel_weights:
    # NOMINAL OPERATING CONDITIONS (P ~ 2e-8 mbar, source ~900K, no laser heating):
    gas_collision: 0.10
    blackbody: 0.05
    photon_recoil: 0.00   # no laser-IF beamsplitters in original 3-grating Talbot-Lau
    vibration: 0.40       # Stibor 2004 documents acoustic vibration as significant dephasing
    trap_photon: 0.00
    other_unattributed: 0.45  # detection statistics, Casimir-Polder van der Waals interaction with grating bars, source velocity distribution
  primary_citations:
    channel_budget:
      - "Hornberger, Uttenthaler, Brezger, Hackermüller, Arndt, Zeilinger, Phys. Rev. Lett. 90, 160401 (2003), DOI:10.1103/PhysRevLett.90.160401: collisional decoherence of C70 quantitatively confirmed under deliberately raised pressure (up to 1e-6 mbar)"
      - "Hackermüller, Hornberger, Brezger, Zeilinger, Arndt, Nature 427, 711 (2004), DOI:10.1038/nature02276: BB decoherence of C70 confirmed under deliberate laser heating to 2000-3000 K"
      - "Hornberger, Hackermüller, Arndt, Phys. Rev. A 70, 053608 (2004), arXiv:quant-ph/0412003: theory of decoherence in matter-wave Talbot-Lau, including channel cross-sections"
      - "Stibor, Hornberger, Hackermüller, Zeilinger, Arndt, arXiv:quant-ph/0411118 (2004): acoustic vibration as significant dephasing source in Talbot-Lau"
      - "Hornberger, Sipe, Phys. Rev. A 68, 012105 (2003): collisional decoherence theory framework"
    precision:
      - "Hackermüller et al. 2004 demonstrate quantitative agreement with theory at the ~10-20% level on inferred decoherence rate vs T"
      - "Hornberger et al. 2003 demonstrate quantitative agreement with theory at the ~10% level on inferred decoherence rate vs P"
  notes: |
    CRITICAL operating-conditions issue: the Hornberger 2003 and Hackermüller
    2004 channel-resolved measurements were obtained under deliberately
    engineered conditions where the channel under study was the dominant one
    (raised pressure for collisional; laser-heated molecules for BB). At
    nominal operating conditions (UHV ~2e-8 mbar baseline, source 900 K
    without external heating), neither gas nor BB is dominant — both are
    sub-dominant to technical noise (vibration, detection statistics, grating
    interactions). The existing-table values gas=0.40 + BB=0.40 reflect
    measured dominance under engineered conditions, NOT the nominal-run
    budget. The above weights are for nominal operation; for engineered
    studies of either channel, the channel under study reaches ~0.5-0.9.

- name: mol_IF_oligoporphyrin
  description: "Functionalized oligoporphyrin and fluorous-tagged molecule libraries (>10 kDa to >25 kDa); KDTLI / 2-m Talbot-Lau interferometers (Arndt group); see Eibenberger 2013, Fein 2019"
  field_maturity: mature
  directly_measured_quantity: "fringe visibility V at fixed mass; mass-resolved interference at >25 kDa"
  measurement_precision_factor: 0.20
  channel_weights:
    # Channel-resolved budget for the heaviest species is NOT separately published.
    # Theoretical expectation extrapolating Hornberger framework to high mass:
    gas_collision: null      # theoretically dominant by extrapolation but not separately measured for >10 kDa
    blackbody: null          # theoretically expected ~0.1-0.3 from internal heat capacity scaling but not measured
    photon_recoil: 0.10      # KDTLI uses an optical phase grating (Kapitza-Dirac) for G2 — laser phase noise on G2 contributes
    vibration: null
    trap_photon: 0.00
    other_unattributed: null
  primary_citations:
    channel_budget:
      - "Eibenberger, Gerlich, Arndt, Mayor, Tüxen, Phys. Chem. Chem. Phys. 15, 14696 (2013), DOI:10.1039/C3CP51500A, arXiv:1310.8343: matter-wave interference of >10 kDa molecules; channels not budgeted"
      - "Fein, Geyer, Zwick, Kiałka, Pedalino, Mayor, Gerlich, Arndt, Nat. Phys. 15, 1242 (2019), DOI:10.1038/s41567-019-0663-9: matter-wave interference of >25 kDa oligoporphyrins; channels not budgeted"
      - "Hornberger et al., Rev. Mod. Phys. 84, 157 (2012): review of matter-wave interferometry with large molecules"
      - "Gerlich et al., Nat. Phys. 3, 711 (2007), DOI:10.1038/nphys701: Kapitza-Dirac-Talbot-Lau interferometer description"
    precision:
      - "Fein 2019: contrast measurements at the ~10-15% level for the heaviest species; reduced significance for absolute Γ_decoh extraction"
  notes: |
    The literature does NOT publish a channel-resolved decoherence budget for
    heavy oligoporphyrin runs. The 2013 Eibenberger and 2019 Fein papers
    demonstrate quantum interference and benchmark against the
    Hornberger-Hackermüller decoherence framework but do not separately
    quantify gas vs BB vs vibration contributions for the >25 kDa runs. The
    existing-table values gas=0.55 + BB=0.30 are theoretically plausible by
    extrapolation but not directly measured. Recommend channel weights remain
    null/uncertain pending a dedicated channel-resolved measurement.

- name: opto_levitated_silica
  description: "Optically levitated silica nanospheres in cavity-assisted coherent scattering (Aspelmeyer/Vienna) or cold-damped (Novotny/ETH) configurations; ground-state-cooled CoM motion. See Delić 2020, Magrini 2021, Tebbenjohanns 2021"
  field_maturity: mature  # platform mature; CoM superposition still speculative
  directly_measured_quantity: "phonon occupation number n̄ via heterodyne sideband asymmetry; thermal decoherence rate Γ_th from heating-rate measurements"
  measurement_precision_factor: 0.20
  channel_weights:
    # Post-ground-state-cooling, UHV (~1e-8 to 1e-9 mbar):
    gas_collision: 0.10
    blackbody: 0.05
    photon_recoil: 0.00      # no separate beamsplitter laser; this lives in trap_photon
    vibration: 0.05          # trap displacement noise; usually subdominant in passive isolation
    trap_photon: 0.75        # photon recoil from continuous trap laser; the dominant channel
    other_unattributed: 0.05  # laser intensity noise, residual phase noise (Kamba 2020 shows phase noise can match recoil before mitigation)
  primary_citations:
    channel_budget:
      - "Delić, Reisenbauer, Dare, Grass, Vuletić, Kiesel, Aspelmeyer, Science 367, 892 (2020), DOI:10.1126/science.aba3993: cavity-CS ground-state cooling; recoil-heating limited"
      - "Magrini, Rosenzweig, Bach, ..., Aspelmeyer, Nature 595, 373 (2021), DOI:10.1038/s41586-021-03617-w: optimal feedback ground-state cooling at room T"
      - "Tebbenjohanns, Mattana, Rossi, Frimmer, Novotny, Nature 595, 378 (2021): cryogenic-free-space ground-state cooling"
      - "Gonzalez-Ballestero et al., Phys. Rev. A 100, 013805 (2019), arXiv:1902.01282: master-equation theory with explicit decoherence rates from recoil heating, gas pressure, trap displacement noise"
      - "Romero-Isart, Phys. Rev. A 84, 052121 (2011), arXiv:1110.4495: theoretical decoherence framework (BB and gas only — does not include trap-photon recoil since this is specific to the protocol)"
      - "Kamba, Kiuchi, Yotsuya, Aikawa, arXiv:2011.12507 (2020): laser phase noise as dominant heating mechanism in optical-lattice traps before mitigation"
    precision:
      - "Heating-rate measurements quote Γ_recoil at ~10-20% precision in best ground-state-cooling demonstrations; absolute Γ_decoh inferred via heating rate at similar precision"
  notes: |
    Trap-laser photon recoil is the consensus-dominant channel in ground-state
    cooled levitated silica. Multiple post-2020 experiments explicitly state
    recoil-heating-limited operation. Existing table's trap_photon=0.80 is
    well-supported. Gas collision becomes comparable below ~1e-9 mbar
    (Tebbenjohanns 2021). Note: Romero-Isart 2011 framework includes ONLY
    "unavoidable" channels (BB + gas) and explicitly excludes trap-photon
    recoil because that's specific to optical levitation; for this scenario,
    trap_photon must be added back in.

- name: opto_levitated_diamond_NV
  description: "Optically/Paul-trapped nanodiamonds with NV-center spin qubits; proposed BMV-precursor and matter-wave interferometer platforms. See Bose 2017, Frangeskou 2018, Jin 2024"
  field_maturity: speculative   # CoM superposition with NV-diamonds NOT YET DEMONSTRATED
  directly_measured_quantity: "internal NV spin coherence T2 (currently); CoM Γ_decoh has not been measured at high vacuum"
  measurement_precision_factor: 0.50
  channel_weights:
    # No CoM-superposition experiment exists; channel weights below are theoretical
    # estimates from proposals at projected operating conditions:
    gas_collision: 0.20
    blackbody: 0.15      # internal heating from trap laser (Frangeskou 2018) makes diamond emit BB strongly
    photon_recoil: 0.05
    vibration: 0.05
    trap_photon: 0.30
    other_unattributed: 0.25   # graphitization/burning at high vacuum is the dominant practical limit, doesn't fit cleanly in the schema
  primary_citations:
    channel_budget:
      - "Frangeskou et al., New J. Phys. 20, 043016 (2018): pure nanodiamonds for levitated optomechanics; internal heating analysis"
      - "Hsu et al., Sci. Rep. 6, 36514 (2016), arXiv:1510.07555: burning/graphitization of optically levitated nanodiamonds in vacuum; internal-temperature measurement"
      - "Jin, Shen, Ju, Gao, Zu, Grine, Li, Nat. Commun. 15, 5063 (2024), DOI:10.1038/s41467-024-49175-3: first ODMR of nanodiamond at high vacuum (<1e-5 Torr) using Paul trap"
      - "Scala, Kim, Morley, Barker, Bose, Phys. Rev. Lett. 111, 180403 (2013): proposed spin-CoM coupling for levitated nano-oscillator"
      - "Yin, Li, Zhang, Duan, Phys. Rev. A 88, 033614 (2013): proposed spin-optomechanical coupling for nanodiamonds"
    precision:
      - "Not applicable — no CoM Γ_decoh has been measured. Internal NV spin T2 measurements quoted to ~10-20% in best in-vacuum runs (Jin 2024)"
  notes: |
    The diamond-NV CoM superposition platform is NOT YET OPERATIONAL at the
    parameter regime relevant to BMV-style proposals. Optical levitation of
    nanodiamonds was historically restricted to P > 1 Torr due to laser-
    induced heating and burning (Frangeskou 2018, Hsu 2016). Jin 2024 only
    recently achieved Paul-trap levitation with ODMR at <1e-5 Torr — and this
    measures internal spin coherence, not CoM decoherence. The dominant
    practical limit is internal heating leading to graphitization/burning,
    which doesn't fit the 5-channel position-decoherence schema cleanly.
    Recommend marking field_maturity=speculative (existing table has
    "developing" — NOT supported by current literature for the CoM-IF use
    case). Existing values are theoretical estimates only.

- name: bmv_bose2017_nominal
  description: "Bose-Marletto-Vedral 2017 proposal for gravitationally-induced entanglement of two diamond microspheres with NV spins. NO measurement exists; values are theoretical estimates from the proposal itself."
  field_maturity: speculative
  directly_measured_quantity: "none — paper specifies design constraints only"
  measurement_precision_factor: 1.0   # theoretical-model uncertainty, not statistical precision
  channel_weights:
    # Per Bose 2017 PRL 119 240401 explicit text: P=1e-15 Pa, T=0.15 K, Δx~250 μm,
    # collisional decoherence time matched to fall time τ + 2τ_acc ~ 3.5 s,
    # thermal decoherence "negligible".
    gas_collision: 0.85    # the channel the proposal is designed against — at the edge of feasibility
    blackbody: 0.05
    photon_recoil: 0.00
    vibration: 0.05
    trap_photon: 0.00
    other_unattributed: 0.05   # NV spin decoherence (separate from CoM); Casimir-Polder; gravity gradient noise
  primary_citations:
    channel_budget:
      - "Bose, Mazumdar, Morley, Ulbricht, Toroš, Paternostro, Geraci, Barker, Kim, Milburn, Phys. Rev. Lett. 119, 240401 (2017), DOI:10.1103/PhysRevLett.119.240401, arXiv:1707.06050"
      - "Marletto, Vedral, Phys. Rev. Lett. 119, 240402 (2017), DOI:10.1103/PhysRevLett.119.240402"
    precision:
      - "Not applicable — no measurement. Theoretical-uncertainty factor reflects modelling assumptions about pressure, temperature, and superposition geometry"
  notes: |
    Bose 2017 explicitly states (Sec. on decoherence times): at P=1e-15 Pa,
    T=0.15 K, for Δx~250 μm, "the collisional decoherence time ... is the same
    order of magnitude as the total microsphere's fall time τ + 2τ_acc ~3.5
    s, while the thermal decoherence mechanism, due to scattering, emission,
    and absorption of environmental photons, is negligible." So gas collision
    is the channel the proposal is most designed against, but is at the edge
    of feasibility (Γ_gas·τ_exp ~ 1, not <<1). The 0.85 weight reflects
    "channel of dominant concern" rather than "measured fraction." Existing
    table's 0.95 is approximately right in spirit but slightly overweights
    given the proposal explicitly puts the design point at the edge.

- name: carney_small_mass_proposal
  description: "Carney-style tabletop quantum-gravity proposals at m~1e-19 kg scale. UNDERSPECIFIED in the original prompt — no single canonical proposal."
  field_maturity: speculative
  directly_measured_quantity: "none"
  measurement_precision_factor: 1.0
  channel_weights:
    gas_collision: null
    blackbody: null
    photon_recoil: null
    vibration: null
    trap_photon: null
    other_unattributed: null
  primary_citations:
    channel_budget:
      - "Carney, Stamp, Taylor, Class. Quantum Grav. 36, 034001 (2019), DOI:10.1088/1361-6382/aaf9ca, arXiv:1807.11494: 'Tabletop experiments for quantum gravity: a user's manual' — review covering many proposals; not a single specification"
      - "Carney, Krnjaic, Moore et al., Snowmass 2021 white paper, arXiv:2203.11846 (2022): tabletop experiments for IR quantum gravity"
      - "Carney, Müller, Taylor, PRX Quantum 2, 030330 (2021): coherent-channel proposal"
    precision:
      - "Not applicable — class of proposals, not a single experiment"
  notes: |
    The "carney_small_mass_proposal" tag does NOT correspond to a specific
    experimental proposal in the literature. Carney et al. have authored
    multiple proposals across mass scales in their reviews; without pinning to
    a specific arXiv ID and parameter set, channel weights cannot be
    populated. STRONG RECOMMENDATION: either remove this scenario from the
    catalog, or replace it with a specific pinned proposal (e.g., Carney
    Krnjaic Moore Snowmass 2021 white paper Sec. X for a stated parameter
    set). Existing table's values (gas=0.50, trap=0.30, etc.) are not
    traceable to any single primary source.
```

## Verdict and gaps

| scenario | verdict | confidence |
|---|---|---|
| atom_IF_Cs_fountain | REFINES — dominant-channel ordering should reverse: vibration > photon-related > gas/BB | High (multiple primary sources confirm vibration dominance in fountain-mode gravimeters) |
| mol_IF_C60 | REFINES with caveat — existing values describe engineered demonstrations of channels, not nominal operating conditions | High (Hornberger 2003 + Hackermüller 2004 are the canonical sources and explicitly engineered the dominance) |
| mol_IF_oligoporphyrin | UNCHARACTERIZED — channel-resolved budget for heaviest species not separately published | Medium (Eibenberger 2013, Fein 2019 demonstrate interference but don't decompose the budget; theoretical extrapolation only) |
| opto_levitated_silica | SUPPORTS — trap_photon dominance well-documented in Delić 2020, Magrini 2021, Tebbenjohanns 2021 | High |
| opto_levitated_diamond_NV | CONTRADICTS existing field_maturity: developing — should be speculative for CoM superposition; channel breakdown is theoretical only | High on maturity assessment (Jin 2024 is the first high-vacuum ODMR with a nanodiamond, but this is internal-spin not CoM) |
| bmv_bose2017_nominal | REFINES slightly — Bose 2017 explicitly puts design point at edge of feasibility (Γ_gas·τ ~ 1), not at strict gas-dominance | High (direct text of Bose 2017) |
| carney_small_mass_proposal | UNDERSPECIFIED — does not correspond to a single primary source; recommend removal or pinning | High |

### Gaps worth flagging

1. **Heavy-molecule channel-resolved budget is a literature gap.** No paper
   in the Vienna program publishes a separate decoherence-channel
   decomposition for >10 kDa species. Existing-table values
   (gas=0.55 + BB=0.30 for oligoporphyrin) are theoretical
   extrapolations dressed as measurements. If your downstream verdict
   ride on this, mark it explicitly low-confidence.

2. **The 5-channel schema mis-bins atom-IF noise.** "photon_recoil"
   should be split into `spontaneous_emission` and
   `laser_phase_noise`; coherent Bragg/Raman beamsplitter pulses don't
   decohere in the ideal limit and shouldn't be in this category at
   all. Existing-table values for atom IF are conceptually muddled
   regardless of the numerical weights.

3. **Diamond-NV CoM matter-wave decoherence has never been measured.**
   All channel weights for `opto_levitated_diamond_NV` and
   `bmv_bose2017_nominal` are theoretical estimates. The downstream
   verdict for these scenarios should carry an explicit "no empirical
   channel-resolved data exists" warning.

4. **"Operating conditions matter" is missing from the schema.** C60
   collisional and BB experiments measured channel dominance under
   engineered conditions. The same setup at nominal vacuum + nominal
   source temperature has a completely different channel ordering. The
   catalog should record `operating_conditions` (engineered vs nominal)
   per scenario, or pick one consistently.

5. **Precision factors blur three different epistemic regimes.**
   Contrast-measurement precision (~1-5%), Γ_decoh-from-fit precision
   (~10-20%), and theoretical-model uncertainty for unmeasured
   platforms (~100%) are not commensurable. The single
   `measurement_precision_factor` field hides this.

### Quick action items for `bdg_decoherence_channels.py`

- **Atom-IF**: invert vibration/photon-recoil ratio; split photon-recoil into sub-categories if schema allows
- **C60**: add `operating_conditions: nominal` and reduce gas+BB to ~0.15 combined; add `vibration: ~0.40`
- **Oligoporphyrin**: change null to channel weights with `confidence: theoretical_extrapolation`
- **Levitated silica**: keep as-is; add Tebbenjohanns 2021 + Magrini 2021 citations
- **Diamond NV**: change `field_maturity` to `speculative`; mark all weights theoretical
- **BMV**: 0.85 vs 0.95 is a small refinement; main fix is documenting the "edge-of-feasibility" framing
- **Carney**: pin to a specific arXiv ID or remove
