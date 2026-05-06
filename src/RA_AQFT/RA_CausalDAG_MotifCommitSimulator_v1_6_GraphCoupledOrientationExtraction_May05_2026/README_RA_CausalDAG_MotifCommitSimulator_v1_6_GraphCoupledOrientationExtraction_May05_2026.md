# RA Causal-DAG Motif Commit Simulator v1.6 — Graph-Coupled Orientation-Link Extraction (corrected)

This corrected v1.6 packet closes the **rescue/topology disconnection** identified in v1.5 by extracting the rescue event and graph-coupled orientation-link overlap from the **same v0.9 `CausalDAG` instance per trial**.

The honesty progression is:

```text
v1.2 synthetic orientation surface          (row-metadata-derived)
v1.3 native theorem-catalog surface         (Lean source catalog)
v1.4 per-graph/per-member tokens            (simulator state + catalog)
v1.5 concrete topology corpus               (parallel corpus, still not the v0.9 rescue graphs)
v1.6 matched graph extraction               (rescue + orientation from the same v0.9 DAG per trial)
```

## What was corrected from the original v1.6 packet

1. **Overlap statistic clarified and repaired.** The original code described `graph_coupled_orientation_link_overlap` as mean pairwise Jaccard but computed parent-anchored Jaccard. The corrected packet now computes:
   - `v1_6_graph_coupled_orientation_link_overlap`: **all-pairs mean Jaccard** across family-member witnesses.
   - `v1_6_parent_anchored_orientation_link_overlap`: parent-to-member mean Jaccard, retained as a secondary diagnostic.
2. **Partial-correlation report corrected.** The original narrative said rescue residual variance collapsed to zero across all cells. That contradicted the CSV. The corrected report records the actual nonzero residuals for ledger/orientation cells and zero residuals only for selector-stress controls.
3. **“Canonical” language removed.** The included run is a **subset matched-graph diagnostic run**, not a canonical 100-seed/full-sweep run.
4. **CLI controls exposed.** The run script now accepts severance seeds, modes, severities, threshold fractions, and family semantics without editing Python.
5. **Validation log regenerated.** In this packet environment, 6 tests pass, including the small integration test when an adjacent/external v0.9 simulator directory is available.

## Method

For each trial, v1.6:

1. Builds a v0.9 `ChannelSeedState`.
2. Calls `evaluate_native_overlap_certified_family(...)` to obtain the v0.9 rescue event and native-overlap fields.
3. Builds the same support family used by v0.9.
4. Extracts edge-pair-sign orientation-link witnesses from the same `state.dag` around each family-member cut.
5. Computes all-pairs and parent-anchored Jaccard overlap diagnostics.
6. Aggregates by `(mode, family_semantics, severity, threshold_fraction, support_width)`.

There is no hash-keyed mapping from rescue rows to separate graph corpora.

## Included subset run

The included output run uses:

```text
seeds = 17..20
severance_seeds = [101]
modes = ledger_failure, orientation_degradation, selector_stress
severities = [0.5]
threshold_fractions = [0.5]
family_semantics = at_least_k, augmented_exact_k
max_targets = 8
trials = 192
per-cell rows = 24
```

This is a **matched-graph subset diagnostic**, not a canonical result.

## Corrected headline

The matched-graph extraction works and closes the v1.5 disconnection:

```text
v1_6_disconnection_closed = true
graph_coupled_orientation_surface_decoupled = true
selector_guardrail_passed = true
orientation_specificity_resolved_on_matched_graphs = false
```

Specificity table in the subset run:

```text
orientation_degradation / at_least_k:       gap = -0.146, reversed_or_negative
orientation_degradation / augmented_exact_k: gap = -0.229, reversed_or_negative
ledger_failure: ledger_control_not_resolved_by_graph_coupled_orientation
selector_stress: not_certification_channel
```

Because there are only four rows per `(mode, semantics)` specificity cell, this should be read as a **warning/corrigendum**, not as a robust reverse-sign finding.

## Correct interpretation

v1.6 establishes:

```text
1. The graph-coupled extraction method works.
2. Rescue and orientation overlap are measured on the same DAG per trial.
3. The v1.5 orientation-specificity / cross-validation claim is not robust to matched-graph extraction at this subset scale.
4. The subset does not establish robust reverse orientation specificity.
```

## What v1.6 does not establish

v1.6 does **not** establish:

```text
Nature-facing orientation specificity
robust reverse orientation specificity
canonical-scale graph-coupled orientation behavior
the final/topologically correct orientation-link keying
```

## Run command

```bash
python scripts/run_graph_coupled_orientation_extraction_v1_6.py \
  --v0-9-simulator-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/simulator \
  --output-dir outputs \
  --seed-start 17 \
  --seed-stop 21 \
  --max-targets 8 \
  --severance-seeds 101 \
  --modes ledger_failure,orientation_degradation,selector_stress \
  --severities 0.5 \
  --threshold-fractions 0.5 \
  --family-semantics at_least_k,augmented_exact_k
```

## Outputs

```text
ra_v1_6_trial_rows.csv
ra_v1_6_per_cell_aggregated.csv
ra_v1_6_decoupling_audit.csv
ra_v1_6_partial_correlation.csv
ra_v1_6_specificity.csv
ra_v1_6_summary.csv
ra_v1_6_summary.md
ra_v1_6_state.json
```

## Next step

Build/run **v1.7 Graph-Coupled Orientation Extraction — canonical sweep** with enough cells for meaningful specificity bins, and compute both all-pairs and parent-anchored overlap diagnostics. No orientation-specific rescue claim should be promoted unless it survives matched-graph extraction at canonical scale.
