# Open native-witness requirements

This document specifies what would be required, methodologically and data-wise, to revisit orientation-specific certification rescue without restarting the same confound chain.

## What the v1.x audit chain actually closed

The chain established that **the orientation-overlap surfaces tested in v1.5 / v1.6 / v1.7 cannot independently support an orientation-specific rescue inference at canonical scale**:

- The v1.5 surface was hash-keyed (rescue/topology disconnected).
- The v1.6 surface was matched-graph but member-indexed (witness keying ties orientation to family-member position rather than to a native invariant).
- The v1.7 keying-ablation showed that even non-member graph-derived keyings produced orientation_overlap that is structurally a function of `(support_width, family_size)` -- so within fixed-structure joint strata there is no orientation-overlap variation left to test for an orientation-specific rescue effect.

This is a result about **the surfaces we have**, not about Nature. Nothing in the chain refutes orientation-specific rescue as a possibility; it refutes the specific surfaces tested as instruments to detect it.

## What a credible re-attempt would require

### Requirement 1: a truly native orientation witness extractor

The witness must be derived from RA-native orientation structure, not from row metadata, not from a deterministic hash of cell coordinates, not from edge-pair-sign tags computed on the simulator graph. Candidate sources:

- **Sign-source pairs from `RA_CausalOrientation_Core`**. The Lean module already encodes one-way precedence and forward/reverse winding theorems; their per-vertex / per-edge sign assignments are a candidate native witness.
- **Native ledger orientation chirality from `RA_D1_NativeLedgerOrientation`**. The ledger-orientation chirality fields are Type-valued evidence in Lean; an extractor that maps ledger chirality assignments to per-cut tokens would be native in the sense the Lean side is native.
- **Closure-orientation witnesses from `RA_D1_NativeClosure`**. Closure-orientation witnesses are also Type-valued in Lean and not tied to the v1.0 component coordinates.
- A combined extractor that takes the `RA_MotifConcreteGraphOrientationWitness` / `RA_MotifPerGraphOrientationWitness` qualitative bridges from v1.0 .. v1.4 / v1.5-Lean-side and instantiates their `Type`-valued evidence fields with concrete data from one of the above three sources.

The witness must NOT use:

- Row metadata (mode, severity, threshold, support_width, family_size, semantics) as part of the keying.
- The trial seed or family-member index.
- Hashes of any of the above.

### Requirement 2: within-stratum orientation variation

The witness must produce orientation_overlap values that vary within a fixed `(mode, family_semantics, threshold_fraction, severity, support_width, family_size)` stratum. Concretely:

- For each cell `(keying, mode, family_semantics, severity, threshold_fraction)`, tertile-bin orientation_overlap at the cell level (per `RA-SIM-CONFOUND-METHOD-001` rule (e)).
- Check: does each `(support_width, family_size)` stratum within the cell contain both low and high bins under the fixed cell-level binning? This is the v1.8.1 estimability check.
- If estimability < 0.2 across graph keyings, the witness has the same structural-co-determination flaw as the v1.x extractors and the audit will be non-estimable.

The fixed-bin discipline (rule (f)) is essential: do NOT re-tertile-bin within stratum to manufacture in-stratum variation.

### Requirement 3: shuffled-overlap control

A deterministic shuffled-overlap control must be evaluated within the same joint strata. Per `RA-SIM-ORIENT-KEYING-METHOD-001` and `RA-SIM-CONFOUND-METHOD-001` rule (b), any orientation-specific specificity gap must dissociate from the shuffled control's gap within strata where both are estimable. v1.7 showed that raw-aggregate shuffled controls are insufficient -- they can match graph keyings even when both are structural artifacts.

### Requirement 4: support+frontier OLS partial-correlation control

The partial correlation between orientation_overlap (residualized on support and frontier overlap) and `certification_rescue_event` (residualized on the same controls) must be reported per cell. Per `RA-SIM-ORIENT-KEYING-METHOD-001`, member-indexed keying is identifiable here as a near-zero residual_std anomaly.

### Requirement 5: canonical scale

At least the v1.7 sweep scale: 100 seeds × 3 severance × 3 modes × 3 severities × 3 thresholds × 2 family_semantics × 12 targets = 64,800 base trials × `n_keyings`. Fewer trials produce small-sample artifacts (the v1.6 192-trial subset showed how this fails).

### Requirement 6: fix the b742034 / 3b40be2 regression first

Before any new extractor is run, the witness function in `RA_CausalDAG_MotifCommitSimulator_v1_6_GraphCoupledOrientationExtraction_May05_2026/analysis/ra_graph_coupled_orientation_extraction.py` should be re-patched (b742034 fix re-applied to remove `member_idx` from the sign and the `:m` tag), and any new packet that reuses that file should pin the SHA in its README.

## Signals to look for

A credible new extractor should produce, on the v1.7 trial-rows or a re-run with the new keying:

- Estimable joint strata fraction ≥ 0.5 across graph keyings (currently 0.0 in v1.8.1 cell-level).
- Within-stratum graph-derived gap that differs from the shuffled control's within-stratum gap by |delta| ≥ 0.05 (currently 0.005 in v1.8.1).
- Partial correlation |r| ≥ 0.10 with `residual_std ≥ 0.05` (currently |r| ≤ 0.13 with residual_std ~ 0.10-0.17 in non-member graph keyings; member-indexed has residual_std ≤ 0.02 and is therefore disqualified by rule (d)).

## Process gate

Per `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001`, no new orientation-overlap rescue claim should be promoted to `proof_status: simulation_validated_canonical_run_confirmed` without satisfying all six requirements above. Any v1.10+ packet attempting orientation-specific certification rescue must include in its registry-proposals YAML an explicit checklist showing each requirement satisfied or explicitly waived.

## What this list IS NOT

- It is not a research priority list. The v1.x chain landed a strong negative result, and the next productive direction is the positive line (certification-rescue, certificate-correlation, severance-channel, support-family) rather than another orientation-rescue attempt.
- It is not a list of necessary kernel proofs. The Lean qualitative bridges (`RA_MotifOrientationLinkSurface`, `RA_MotifNativeOrientationLinkDerivation`, etc.) are sufficient as Type-valued refinement structure; the missing piece is a per-graph instantiation of their Type-valued evidence with non-co-determined values.
