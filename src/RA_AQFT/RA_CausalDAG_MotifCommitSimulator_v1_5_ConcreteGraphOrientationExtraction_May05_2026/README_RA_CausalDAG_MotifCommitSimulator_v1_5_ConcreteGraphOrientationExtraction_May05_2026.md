# RA Causal-DAG Motif Commit Simulator v1.5 — Concrete-Graph Orientation-Link Extraction

This packet advances the orientation-link line one step beyond v1.4.

The honesty progression:

```text
v1.2 synthetic orientation-link surface          (hash of row metadata)
  → v1.3 native theorem-catalog surface          (Lean source files parsed)
  → v1.4 per-graph/per-member token surface      (simulator-state + catalog tokens)
  → v1.5 concrete-graph topology surface         (parent/child edges + topology-derived signs)
  → v1.6+ extraction from v0.9 simulator's actual ActualizationDAG instances
```

v1.5 introduces a small reference corpus of `ActualizationDAG`-shaped Python
objects (chains, balanced/asymmetric branches, diamonds) and derives
orientation-link witnesses directly from each graph's parent/child edges,
tagged with topology-derived signs (depth-mod-2 + member index). This is
genuinely topology-derived, not row-metadata-derived or token-derived.

## Status

- **Analysis layer:** canonical/demo runnable; 9 unit tests pass.
- **Lean bridge:** `RA_MotifConcreteGraphOrientationWitness` lake-build-confirmed
  (8287/8287 jobs, ~70s, 0 sorry/admit/axiom).
- **RAKB proposals:** active-schema.

## Honesty caveat

The reference corpus is **synthetic-deterministic**, not extracted from the
v0.9 simulator's actual `ActualizationDAG` instances. Witnesses come from
real graph topology (parent/child edges with depth-derived signs), but the
corpus itself is a parallel Python construction. v1.6+ should integrate with
v0.9's actual simulator graphs OR with an `RA_GraphCore`-side Lean extractor.

## Inputs

```text
ra_native_certificate_components_v1_0.csv  (from v1.0; for cell structure + rescue rates)
```

## Run

```bash
python scripts/run_concrete_graph_orientation_extraction_v1_5.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v1_0_NativeCertificateAnchoring_May05_2026/outputs \
  --output-dir outputs
```

## Outputs

```text
ra_concrete_graph_corpus_summary_v1_5.csv
ra_concrete_components_v1_5.csv
ra_concrete_orientation_decoupling_audit_v1_5.csv
ra_concrete_orientation_partial_correlation_v1_5.csv
ra_concrete_orientation_specificity_v1_5.csv
ra_concrete_orientation_matched_strata_v1_5.csv
ra_concrete_orientation_witness_summary_v1_5.csv
ra_concrete_orientation_witness_summary_v1_5.md
ra_concrete_orientation_witness_state_v1_5.json
```

## Canonical results

```text
corpus_size                                  : 58 graphs
v1_0_input_rows -> concrete_component_rows   : 480 -> 480
decoupled_count / decoupled_total            : 12 / 12 (100%)
concrete_orientation_surface_decoupled       : true
matched_orientation_variation_available      : true
orientation_specificity_resolved             : true
selector_guardrail_passed                    : true
mean_concrete_orientation_residual_std       : 0.0389
```

Specificity verdicts:

- `orientation_degradation / augmented_exact_k` → `concrete_orientation_specific_surface_detected` (low_minus_high gap +0.028)
- `orientation_degradation / at_least_k` → `weak_or_tied` (gap −0.002)
- `ledger_failure / both` → `ledger_control_not_resolved_by_concrete_orientation`
- `selector_stress / both` → `not_certification_channel`

The augmented_exact_k vs at_least_k asymmetry continues to track the
family-semantics asymmetry first identified in v0.9.2 (concrete topology
preserves the same signal posture).

## Lean bridge

`lean/RA_MotifConcreteGraphOrientationWitness.lean` defines
`DAGConcreteEdgePairSignContext` / `GraphConcreteEdgePairSignContext` plus
refinement theorems `.to_per_graph`, `.to_native_catalog`,
`.to_orientation_link_surface`. The bridge is **qualitative**: it states
that concrete edge-pair-sign witness data instantiates the abstract v1.4
type, not that any specific numerical rescue law follows.

## Success criteria

1. Per-graph orientation-link witness keys are edge-based, not vertex-based. ✓
2. `concrete_orientation_link_overlap_v1_5` is decoupled from support / frontier / orientation / ledger overlap. ✓
3. Matched support/frontier strata contain multiple concrete orientation values. ✓
4. `orientation_degradation` rescue varies with concrete orientation overlap (augmented_exact_k cell resolves). ✓ (with at_least_k weak_or_tied — known semantics asymmetry)
5. `ledger_failure` remains a control. ✓
6. `selector_stress` remains outside certification rescue. ✓
7. Lean bridge compiles in the active RA Lean project. ✓ (8287/8287 jobs)
