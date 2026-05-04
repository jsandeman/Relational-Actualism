# RAKB Stage C Paper-Pruning / Restoration Audit  
**Date:** April 28, 2026  
**Inputs:** canonical four-paper TeX bundle, RAKB v0.5 registry after Lean + Python upserts, April 16/17 historical reference bundle.

## Executive conclusion

The latest canonical four-paper suite is **not simply missing the April-16 results**. It does three different things:

1. **Keeps or explicitly handles many results** in a more disciplined form.
2. **Correctly demotes** several April-16 claims whose status was too strong under the later native-framing discipline.
3. **Actually over-prunes or under-registers** a smaller set of results and targets that should be preserved in RAKB as restoration candidates, targets, or paper-level caveated notes.

The most important practical conclusion is that the canonical papers are now **cleaner than the April-16 monolithic state**, but the registry should remember more than the papers currently present. The right remedy is not to re-expand the papers indiscriminately; it is to preserve the lost material in typed KB space and restore only the parts whose support status is honest.

## Quantitative summary

Historical D-series claims assessed: **43** (`D09`–`D51`).

- `present_or_explicitly_handled`: 23
- `candidate_for_restoration_or_target`: 12
- `absent_but_correctly_demoted_or_archived`: 8

Canonical TeX section mapping:

- sections/subsections scanned: **113**
- sections mapped to at least one RAKB node: **83**
- distinct mapped node IDs: **63**

Important structural observation:

> The canonical TeX files contain no explicit `RA-*` registry IDs.  
> The Stage C crosswalk is therefore a carefully curated section-title/content map, not a deterministic ID extraction.

Future paper maintenance will be much easier if the TeX includes comments such as:

```tex
% RAKB: RA-GRAV-003; RA-GRAV-004
```

above relevant sections.

---

## Paper-by-paper audit

### Paper I — kernel / spacetime / actualization

Paper I is mostly **healthy and well disciplined**. It preserves the native kernel, graph, BDG, actualization, selectivity, D4, and formal verification surface without using downstream numerical overlays as kernel support.

Strongly represented:

- causal graph ontology;
- seven axioms;
- BDG action and coefficient arithmetic;
- second-order cancellation;
- sequential growth rule;
- BDG acceptance kernel;
- actualization criterion hierarchy;
- D4U02 numerical/computational support;
- Lean verification surface;
- antichain drift as local statistic.

Stage C found three important Paper-I items that are **in the paper but not yet properly typed in RAKB**:

| Candidate | Status | Recommendation |
|---|---|---|
| `RA-KIN-BANDWIDTH-001` | present in canonical TeX | consider promotion or keep as restoration candidate |
| `RA-KIN-PROPER-TIME-001` | present in canonical TeX | consider promotion or keep as restoration candidate |
| `RA-D4-CASCADE-001` | present in canonical TeX | decide whether it belongs in `claims.yaml` or remains a Paper-II/Paper-I bridge candidate |

Paper I also correctly does **not** restore historical `D47` / `D50` as closed claims. The current paper treats wave-equation/frequency-law closure as an open native target, which is the safer status.

### Paper II — matter / motifs / interactions

Paper II has been aggressively but mostly correctly de-risked. It preserves the active structural matter programme while demoting several older numerical or Standard-Model-adjacent overlays.

Strongly represented:

- stable motif census;
- finite closure windows;
- extension census;
- orientation / charge spectrum;
- confinement-as-renewal;
- Koide `K=2/3` as mathematical support;
- strong-density and path-weight computations as caveated computational support;
- proton programme as PI/CN rather than theorem.

Important current decisions:

- The proton-mass cascade is present, but the text explicitly marks `N_eff = L_q^3 = 64` as conjectural. That is correct.
- `W_other / W_baryon = 17.32` is present as native computation, while the later `f0` abundance comparison remains cartography. That is correct.
- Charge quantization is present.
- Matter-sector excess is present as a severance-initial-condition target, not as a derived baryogenesis theory.

Potential over-pruning / candidates:

- proton stability / proton decay prohibition (`D29`);
- Majorana neutrino prediction (`D37`);
- Regge / flux-tube trajectory result (`D25`);
- optional flavor numerics (`D35`, `D36`) only if clearly marked conjectural.

### Paper III — gravity / severance / cosmology

Paper III is where the largest apparent pruning occurred, but much of it is **correct demotion** rather than loss.

Strongly represented:

- causal severance;
- severed-link entropy observable;
- finite boundary law;
- joint BDG/LLC macro-kernel;
- sparse-regime response as a programme;
- historical source-depth hypothesis;
- environment-sensitive expansion as target;
- low-ell / rotating-boundary programme as target.

Correct demotions:

- `D09` RACL seven-step GR chain;
- `D10` Bianchi-as-LLC dissolution;
- `D11` Lorentz-as-causal-invariance dissolution;
- `D12` continuum field-equation uniqueness.

The canonical Paper III deliberately says continuum field equations and Lorentz-frame theorem language are not active native support. That is a good correction under the native-framing rule.

Potential over-pruning / candidates:

- `D16` heat-death prohibition;
- `D18` cosmic-web attractor;
- `D20` DESI `w0/wa` transition fit;
- maybe `D31` no-Page-curve, but only as a severance-information comparison note, not as a theorem.

### Paper IV — complexity / life / agency

Paper IV is also mostly correctly de-risked. It keeps the native complexity architecture and explicitly demotes the areas that were previously too strong.

Strongly represented:

- tier hierarchy;
- recursive closure;
- Causal Firewall;
- substrate independence;
- persistence windows as an open native target;
- RA assembly depth;
- glycolysis and E. coli depth estimates;
- origin-of-life sandwich bound;
- biosignature criteria;
- perception/agency/consciousness constraints.

Correct demotions:

- Markov-blanket theorem as active support (`D39`);
- DFT/F1 computations as active support (`D42`);
- Landauer/KCB/spin-bath as active support.

Potential over-pruning / target preservation:

- `D43` Kinematic Coherence Bound;
- `D44` spin-bath collapse target;
- `D46` Maxwell-demon / actualization-thermodynamics target.

These can remain in RAKB as frontier targets without becoming active paper claims.

---

## Historical D-series assessment

### Present or explicitly handled

| historical_id   | historical_status   | canonical_assessment       | recommended_action                                                                                 |
|:----------------|:--------------------|:---------------------------|:---------------------------------------------------------------------------------------------------|
| D11             | DR                  | present_only_as_comparison | do_not_restore as active support                                                                   |
| D13             | DR                  | present_weakened           | keep as open sparse-regime topology target; do not restore numeric threshold                       |
| D14             | DR                  | present_weakened           | link to RA-PRED-006/RA-OPEN-003; restore formula only as historical source-law candidate           |
| D15             | AR                  | present_weakened           | keep as cluster-lensing target; do not restore numeric 10^8 headroom without source-law derivation |
| D17             | DR                  | partially_present          | restore short explicit arrow-of-time corollary under ontology; map to RA-ONT-002                   |
| D19             | DR                  | present_demoted            | keep under RA-PRED-005/RA-OPEN-004; do not restore zero-parameter ΩΛ claim as DR                   |
| D21             | DR                  | present_weakened_correctly | keep PI/CN; do not promote until N_eff derived                                                     |
| D22             | DR                  | present                    | retain; consider cross-reference from Paper II to Paper I d=4 cascade criterion                    |
| D23             | DR                  | present_weakened           | restore as secondary target table only, not active support                                         |
| D24             | DR                  | present_weakened           | keep as structural interaction hierarchy; formulas remain future work                              |
| D31             | DR                  | partially_present_weakened | restore only as severance-information comparison note; not as Page-curve theorem                   |
| D32             | DR                  | present_weakened           | keep as open matter-sector excess target                                                           |
| D33             | DR                  | present                    | retain as active/caveated orientation-charge result                                                |
| D38             | CV                  | present_weakened_correctly | retain native 17.32 ratio; keep final f0 abundance comparison as bridge/cartography                |
| D39             | DR                  | explicitly_demoted         | do not restore as Markov-blanket theorem; keep RA-OPEN-006 causal shield target                    |
| D40             | AR                  | present_weakened_correctly | retain structural perception/agency/consciousness framework; no numeric threshold yet              |
| D41             | CV                  | present                    | retain; map to RA-COMP-006                                                                         |
| D42             | CV                  | present_as_open_target     | do not promote DFT as active support; keep computational target                                    |
| D45             | DR                  | demoted_to_nonactive       | keep thermodynamic actualization as future target; no active theorem                               |
| D47             | CV                  | present_only_as_comparison | keep under RA-OPEN-009 frequency-law target; do not restore as Schrödinger derivation              |
| D48             | DR                  | present                    | promote/source-reference as Stage-C restoration candidate or claim if desired                      |
| D49             | DR                  | present                    | promote/source-reference as Stage-C restoration candidate or claim if desired                      |
| D51             | DR                  | present_weakened           | map to RA-GRAV-003 and RA-GRAV-SINGULARITY-001; keep as saturation/partition conjecture            |

### Candidate for restoration or target tracking

| historical_id   | historical_status   | canonical_assessment        | recommended_action                                                                                          |
|:----------------|:--------------------|:----------------------------|:------------------------------------------------------------------------------------------------------------|
| D16             | DR                  | absent_overpruned_candidate | add restoration candidate; possible Paper III/IV consequence section if caveated                            |
| D18             | DR                  | mostly_absent               | add cosmology restoration candidate only if source-law programme wants it                                   |
| D20             | DR                  | absent_demoted_to_target    | keep as target/forecast only with script provenance; do not restore as DR                                   |
| D25             | DR                  | absent_overpruned_candidate | add low-priority restoration candidate for Regge/flux-tube comparison                                       |
| D29             | LV                  | absent_overpruned_candidate | create candidate linked to chirality/orientation Lean support; phrase as proton-stability target, not proof |
| D35             | Conjecture          | absent_candidate_only       | optional restoration candidate under flavor numerics                                                        |
| D36             | Conjecture          | absent_candidate_only       | optional restoration candidate under flavor numerics                                                        |
| D37             | DR                  | absent_target_candidate     | optional neutrino/Majorana target candidate if source-backed                                                |
| D43             | DR                  | mostly_absent_target        | add restoration candidate/target for KCB if desired; not active support                                     |
| D44             | DR                  | mostly_absent_target        | add restoration candidate/target for spin-bath collapse if desired                                          |
| D46             | DR                  | absent_candidate_only       | optional future thermodynamics target                                                                       |
| D50             | DR                  | absent_open_target          | add restoration candidate under RA-OPEN-009; no active claim yet                                            |

### Absent but correctly demoted or archived

| historical_id   | historical_status   | canonical_assessment                 | recommended_action                                                      |
|:----------------|:--------------------|:-------------------------------------|:------------------------------------------------------------------------|
| D09             | DR                  | absent_or_rejected_as_active_support | do_not_restore_as_DR; optionally preserve as bridge-cartography issue   |
| D10             | DR                  | absent_correctly_demoted             | do_not_restore_as proof; optional comparison note                       |
| D12             | DR                  | absent_correctly_demoted             | do_not_restore as uniqueness theorem without native derivation          |
| D26             | CV                  | absent_correctly_demoted             | keep bridge/candidate only                                              |
| D27             | DR                  | absent_archive_or_bridge             | do not restore unless a comparison appendix is desired                  |
| D28             | Conjecture          | absent_demoted_to_cartography        | keep as conjectural cartography, not active target                      |
| D30             | DR                  | absent_archive_or_bridge             | do not restore as DR; possible speculative comparison note              |
| D34             | DR                  | absent_correctly_demoted             | keep as downstream numerical cartography; do not restore in active text |

---

## Recommended registry changes

This packet proposes two registry updates:

1. `source_text_references.csv` upserts  
   These add canonical TeX section references for claims/issues/targets/candidates.

2. `restoration_candidates.csv` upserts  
   These preserve Stage C candidates that are either:
   - present in canonical TeX but missing from typed registry state; or
   - present in the April-16 historical state but absent from canonical TeX and worth tracking as targets/frontier work.

Do **not** blindly promote these candidates into `claims.yaml`.

Promotion should require:

- an exact statement;
- a support-status decision;
- source-artifact edge(s);
- paper destination;
- caveats.

---

## Immediate action queue

| action_id   | priority   | area               | action                                                                                  | rationale                                                                                                                                         |
|:------------|:-----------|:-------------------|:----------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
| A1          | high       | registry           | Add Stage C canonical TeX source-text references                                        | Merge reviewed `source_text_references_upsert_v1` after checking section labels; this lets every paper section point into RAKB nodes.             |
| A2          | high       | registry           | Add Stage C restoration candidates                                                      | Merge only after review; candidates include kinematic results present in canonical TeX but not in claims.yaml and absent historical targets.      |
| A3          | high       | Paper I / registry | Decide whether c-bandwidth and proper-time results are claims                           | They are explicit in Paper I and historical D48/D49; either promote to claims.yaml or keep as restoration candidates.                             |
| A4          | high       | Paper I / registry | Keep frequency law open                                                                 | Historical D50 is absent and should sit under RA-OPEN-009 until derived.                                                                          |
| A5          | medium     | Paper II           | Restore optional caveated target table for proton stability, Majorana, Regge if desired | Only as targets/candidates; avoid active-support phrasing unless source support is mapped.                                                        |
| A6          | medium     | Paper III          | Do not restore RACL/field-equation uniqueness chain as active theorem                   | D09-D12 are absent because the current paper deliberately avoids continuum field-equation proof claims. Preserve as bridge-cartography if needed. |
| A7          | medium     | Paper III          | Consider a caveated cosmology-consequences subsection                                   | D16 heat-death, D18 cosmic web, D20 DESI w0/wa can be preserved as targets/candidates if source provenance is retained.                           |
| A8          | medium     | Paper IV           | Keep Markov blanket, DFT, KCB, spin-bath, Landauer claims non-active                    | Current Paper IV correctly demotes them; KCB/spin-bath may be explicit deferred targets rather than active support.                               |
| A9          | low        | Lean/source        | Clean unused hN2 warning                                                                | Rename hN2 to _hN2 in RA_D3_CosmologicalExpansion.lean.                                                                                           |
| A10         | medium     | papers             | Add RAKB IDs as comments or margin notes in canonical TeX                               | No canonical TeX currently contains explicit RA-* IDs; adding `% RAKB: RA-...` comments will make future audits deterministic.                    |

---

## Files in this packet

- `reports/RAKB_stageC_paper_claim_crosswalk_Apr28_2026.csv`
- `reports/RAKB_stageC_historical_restoration_assessment_Apr28_2026.csv`
- `reports/RAKB_stageC_overpruned_results_backlog_Apr28_2026.csv`
- `reports/RAKB_stageC_paper_action_queue_Apr28_2026.csv`
- `registry_upserts_v1/RAKB_stageC_source_text_references_upsert_v1_Apr28_2026.csv`
- `registry_upserts_v1/RAKB_stageC_restoration_candidates_upsert_v1_Apr28_2026.csv`
- `scripts/apply_rakb_stageC_upserts.py`

## Recommended next phase

Apply the Stage C registry upserts only after review, then run validation. After that, the next useful phase is **Stage D synthesis**:

- regenerate claim/artifact/source-text graph metrics;
- identify claims with paper text but no source support;
- identify source-backed results missing from the paper suite;
- produce an integrated RAKB v0.5.1 release report.
