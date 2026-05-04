# Decoherence-budget literature review — task prompt for a Claude chat

> **How to use this file.** Paste the entire `## Prompt` section below into
> a fresh Claude conversation (preferably one with web search / browse
> capability so primary sources can be retrieved). The prompt is
> self-contained and does not require any context from the Relational
> Actualism project. Output should be pastable back into
> `src/RA_AQFT/bdg_decoherence_channels.py` to refine the
> `SCENARIOS` catalog.
>
> **Why this exists.** The current channel-budget weights and measurement
> precision factors in `bdg_decoherence_channels.py` were synthesized from
> training-data knowledge, not primary literature. This is recorded as a
> `next_task` on `RA-OPEN-BDG-DECOHERENCE-CONSTRAINTS-001`. A
> primary-source pass would tighten the empirical-tension verdict on the
> Dict-D-style BDG-suppression conjecture significantly.

---

## Prompt

I am running a project that compares predicted vs measured positional-
decoherence rates across a range of experimental classes (atom
interferometry, molecular interferometry, levitated nanoparticles, and
proposed gravitationally-mediated-entanglement experiments). I have
approximate channel-budget breakdowns synthesized from general field
knowledge, and I need to upgrade these to primary-literature-cited values
so that a downstream physics analysis (assessing predicted ~10–50%
suppression effects against measurement precision) is empirically
defensible.

Please conduct a focused literature review per the structure below. Use
primary sources (peer-reviewed papers, arXiv preprints by the
experimental groups themselves, and widely-cited theoretical
decoherence-budget papers — e.g. Hornberger & Sipe; Joos & Zeh;
Romero-Isart). Do **not** cite Wikipedia, blogs, popular-science
articles, or secondary reviews unless they are widely-cited
authoritative reviews from the field.

### What I need

For each experimental class below, find:

1. **Channel-budget breakdown.** What fractions of the total positional
   decoherence rate `Γ_decoh` come from each channel:
   - `gas_collision` — background-gas momentum-transfer collisions
   - `blackbody` — blackbody-photon absorption / emission (thermal radiation
     from molecule, walls, or surroundings)
   - `photon_recoil` — coherent-laser photon recoil from beamsplitter /
     measurement / cooling pulses (NOT trap-laser)
   - `vibration` — mechanical / seismic / technical noise that couples
     to position
   - `trap_photon` — optical-trap photon recoil (continuous, single-mode;
     dominant in optomechanical setups)

   Weights should sum to 1.0. Order of magnitude is fine; the goal is
   "is gas 5%, 50%, or 95% of the budget?" — not "47% vs 51%".

2. **Measurement precision factor.** To what fractional precision is total
   `Γ_decoh` known (or the directly-measured quantity, typically
   contrast-loss vs time) in the best published implementations of this
   experimental class? E.g., `0.1` means ±10% on the cumulative rate.

3. **Key citations.** The 1–3 most authoritative papers for the channel
   budget *and* for the precision claim, with DOIs or arXiv IDs.

### Experimental classes to research

#### 1. `atom_IF_Cs_fountain`

Cs (or Rb) atom interferometers, especially long-baseline (Kasevich
10m fountain at Stanford; MAGIS-style; Müller group at Berkeley).
Channel-resolved decoherence budget for state-of-the-art runs.
Suggested starting points: Kasevich group publications 2010–present;
reviews by Tino, Kasevich, Bouchendira; Hogan et al. on long-baseline
atom IF.

#### 2. `mol_IF_C60`

C60 fullerene matter-wave interferometry — Arndt group at Vienna
(Hackermüller, Brezger, Hornberger, et al.). Channel-resolved
decoherence in the original Talbot-Lau and KDTLI runs.
Suggested starting points: Hackermüller et al. PRL 2003;
Hornberger / Sipe theoretical decoherence-budget papers (2003–2006);
Brezger et al. PRL 2002.

#### 3. `mol_IF_oligoporphyrin`

Larger-molecule (10+ kDa) interferometry — Arndt group OTIMA, KDTLI-2,
and recent biomolecule runs. Channel-resolved decoherence for the
heaviest-tested species.
Suggested starting points: Eibenberger et al. PCCP 2013; Fein et al.
Nature Physics 2019; recent Vienna group reviews (2020+).

#### 4. `opto_levitated_silica`

Optically levitated silica nanospheres approaching ground-state motional
cooling — Aspelmeyer group (Vienna), Novotny group (ETH Zürich),
Romero-Isart theory.
Suggested starting points: Aspelmeyer group 2020+ ground-state cooling
papers (Delić et al., Magrini et al.); Romero-Isart 2011 NJP review on
mesoscopic superpositions; Chang et al. 2010.

#### 5. `opto_levitated_diamond_NV`

Levitated diamond microspheres with NV centers (BMV precursor
experiments) — Bose group, Geraci group, related diamond-trap
proposals.
Suggested starting points: Carney 2021 review (arXiv:2105.04531 or
related); Bose et al. 2017 PRL supplementary; recent levitated-diamond
experimental papers from Geraci, Bose, Hsu.

#### 6. `bmv_bose2017_nominal`

The Bose–Marletto–Vedral 2017 proposal — review of theoretical
decoherence-budget estimates for the proposed apparatus. Note:
no measured Γ_decoh exists; precision factor will reflect
theoretical uncertainty only.
Suggested starting points: Bose et al. PRL 119, 240401 (2017);
Marletto & Vedral PRL 119, 240402 (2017); Carney et al. 2021 review.

#### 7. `carney_small_mass_proposal` (optional)

Carney-style m ~ 10⁻¹⁹ kg proposals for sub-μm-scale gravity-quantum
tests.
Suggested starting points: Carney, Stamp, Taylor 2019/2021 reviews on
tabletop gravity-quantum tests; recent (2022+) follow-up proposals.

### Output format

For each experimental class, produce a YAML block of this exact form,
suitable for direct paste into a Python catalog:

```yaml
- name: atom_IF_Cs_fountain
  description: "Cs 10m-fountain atom interferometer (Kasevich-style); see Hogan et al. 2011"
  field_maturity: mature   # mature / developing / speculative
  measurement_precision_factor: 0.05   # fractional ± on Γ_decoh in best runs
  channel_weights:
    gas_collision: 0.05
    blackbody: 0.01
    photon_recoil: 0.50
    vibration: 0.40
    trap_photon: 0.04
  primary_citations:
    - "Hogan, Johnson, Kasevich. arXiv:0806.3261 (2008)"
    - "..."
  notes: |
    Photon-recoil dominant from beamsplitter pulses; vibration is
    technical and can be reduced. Channel attribution per Hogan et al.
    Sec. III; precision per Asenbaum 2017 contrast-vs-time fits.
```

After all experimental classes, please also produce a "verdict and
gaps" section:

- For each experimental class, state whether the literature
  **SUPPORTS** / **REFINES** / **CONTRADICTS** the approximate values
  in the comparison table below.
- List any classes where the channel-resolved budget is NOT
  well-characterized in the literature (so the downstream verdict
  carries lower confidence there).

### Existing approximate values (for comparison / sanity check)

These are the training-data-synthesized values currently in the
catalog — please flag whether the primary literature supports them:

| scenario | maturity | meas± | gas | BB | recoil | vib | trap |
|---|---|---|---|---|---|---|---|
| atom_IF_Cs_fountain | mature | 5% | 0.05 | 0.01 | 0.50 | 0.40 | 0.04 |
| mol_IF_C60 | mature | 10% | 0.40 | 0.40 | 0.15 | 0.05 | 0.00 |
| mol_IF_oligoporphyrin | mature | 15% | 0.55 | 0.30 | 0.10 | 0.05 | 0.00 |
| opto_levitated_silica | developing | 25% | 0.10 | 0.05 | 0.00 | 0.05 | 0.80 |
| opto_levitated_diamond_NV | developing | 40% | 0.40 | 0.10 | 0.10 | 0.10 | 0.30 |
| bmv_bose2017_nominal | speculative | 100% | 0.95 | 0.04 | 0.00 | 0.01 | 0.00 |
| carney_small_mass_proposal | speculative | 100% | 0.50 | 0.05 | 0.05 | 0.10 | 0.30 |

### Constraints on the output

- DO use primary literature where possible. Cite by DOI or arXiv ID.
- DO be explicit when a channel-budget breakdown isn't reported in
  the literature — say "not directly characterized" rather than
  guessing.
- DO note whether the quoted measurement precision is on contrast loss,
  total Γ, or a specific decoherence parameter (e.g. coherence time τ).
- Do NOT include any non-decoherence physics analysis (no
  speculation, no model fitting, no prediction comparisons). This
  is a pure decoherence-experimental literature review.
- Do NOT mention or cite this prompt or whoever sent it. Cite only the
  actual experimental groups.
- Aim for 2–4 pages of YAML + 1 page of verdict-and-gaps text.

### Useful pointers for the literature

- **Hornberger & Sipe** (especially their 2003–2008 work) give the
  cleanest channel-resolved decoherence formulas for matter-wave
  interferometry, with explicit cross-section dependencies.
- **Romero-Isart 2011** (NJP) and successors are the standard reference
  for optomechanical / levitated-particle decoherence budgets.
- For **BMV** the published numbers are largely theoretical
  predictions, not measurements — the precision factor should be
  large (~1.0) reflecting theoretical-model uncertainty, not
  experimental statistical uncertainty.
- For atom IF, **Asenbaum et al. 2017** (PRL) and surrounding
  Kasevich-group papers give explicit decoherence-budget breakdowns
  for the 10m fountain.

---

## Notes for the project owner

When the lit-review chat returns its YAML output, you (or a future
Claude Code session) should:

1. Compare each scenario's returned values to the existing entries in
   `src/RA_AQFT/bdg_decoherence_channels.py` (`SCENARIOS` list).
2. For each scenario where the literature SUPPORTS the existing values,
   no code change is needed — just update the docstring or add a
   citation comment.
3. For scenarios that are REFINED or CONTRADICTED, update the
   `channel_weights` and/or `measurement_precision_factor` fields in
   `SCENARIOS`, re-run `python bdg_decoherence_channels.py`, and
   re-run `python test_bdg_decoherence_channels.py`. Tests may need
   threshold adjustments if the new precision factors push specific
   verdicts (e.g. `D_gas_only` may now be CONSISTENT or FALSIFIED for
   different scenarios).
4. Update the RAKB issue `RA-OPEN-BDG-DECOHERENCE-CONSTRAINTS-001`
   `next_tasks` to mark the lit-review pass as completed and to note
   any sharpened empirical envelope.
5. Commit the changes with a message describing what was tightened and
   what stayed the same.
