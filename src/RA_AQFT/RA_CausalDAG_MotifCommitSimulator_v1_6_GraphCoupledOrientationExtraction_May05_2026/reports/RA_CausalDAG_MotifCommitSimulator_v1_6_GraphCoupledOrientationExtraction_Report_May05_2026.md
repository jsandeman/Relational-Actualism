# RA Causal-DAG Motif Commit Simulator v1.6 — Corrected Graph-Coupled Orientation-Link Extraction Report

Date: 2026-05-05.

## Purpose

v1.6 is a matched-graph diagnostic packet. It closes the v1.5 rescue/topology disconnection by computing both the v0.9 rescue event and the orientation-link overlap from the same `CausalDAG` instance per trial.

## Corrections relative to the original v1.6 packet

1. The primary graph-coupled overlap column is now **all-pairs mean Jaccard** across family-member witnesses. Parent-anchored mean Jaccard is retained separately.
2. Partial-correlation narrative now matches the CSV: rescue residual variance is nonzero for ledger/orientation cells and zero only for selector-stress controls.
3. The included run is described as a **subset matched-graph diagnostic**, not as canonical.
4. The CLI exposes modes, severities, thresholds, family semantics, and severance seeds.
5. Validation log is non-empty and records 6 passing tests when v0.9 simulator files are available for the integration test.

## Included subset run

```text
seeds: 17..20
severance_seeds: 101
modes: ledger_failure, orientation_degradation, selector_stress
severity: 0.5
threshold_fraction: 0.5
family_semantics: at_least_k, augmented_exact_k
max_targets: 8
trials: 192
per-cell rows: 24
```

## Summary

```text
v1_6_disconnection_closed = true
graph_coupled_orientation_surface_decoupled = true
selector_guardrail_passed = true
orientation_specificity_resolved_on_matched_graphs = false
run_scope = subset_matched_graph_diagnostic_run_not_canonical
```

## Decoupling audit

The graph-coupled all-pairs orientation-link overlap is decoupled from support, frontier, legacy orientation, and ledger overlap means across all three modes.

Representative values:

```text
vs support/frontier/legacy orientation: mean_abs_diff ≈ 0.545
vs ledger: mean_abs_diff ≈ 0.746
max_abs_diff = 1.0
```

## Specificity audit

Subset specificity rows:

```text
ledger_failure / at_least_k:
  low=0.000, medium=0.429, high=0.375, gap=-0.375
  verdict=ledger_control_not_resolved_by_graph_coupled_orientation

ledger_failure / augmented_exact_k:
  low=0.000, medium=0.429, high=0.292, gap=-0.292
  verdict=ledger_control_not_resolved_by_graph_coupled_orientation

orientation_degradation / at_least_k:
  low=0.000, medium=0.429, high=0.146, gap=-0.146
  verdict=reversed_or_negative

orientation_degradation / augmented_exact_k:
  low=0.000, medium=0.429, high=0.229, gap=-0.229
  verdict=reversed_or_negative

selector_stress:
  gap=0.000
  verdict=not_certification_channel
```

Because each specificity cell has only four per-cell rows, these reversed gaps are **not** promoted as a robust reverse-sign result. They show that v1.5's positive orientation-specificity/cross-validation claim does not survive this matched-graph subset.

## Partial-correlation audit

The corrected partial-correlation table is:

```text
ledger_failure / at_least_k:
  graph_coupled_residual_std=0.020933
  rescue_residual_std=0.074654
  partial_corr=0.926909

ledger_failure / augmented_exact_k:
  graph_coupled_residual_std=0.009285
  rescue_residual_std=0.037028
  partial_corr=-0.653847

orientation_degradation / at_least_k:
  graph_coupled_residual_std=0.020933
  rescue_residual_std=0.090415
  partial_corr=-0.523325

orientation_degradation / augmented_exact_k:
  graph_coupled_residual_std=0.009285
  rescue_residual_std=0.077066
  partial_corr=-0.023100

selector_stress:
  rescue_residual_std=0.000000
  partial_corr blank/undefined
```

Thus, the earlier statement that support/frontier explain all rescue variation across all cells was incorrect. That statement applies only to selector-stress controls in this subset.

## Interpretation

v1.6 establishes a methodological correction:

```text
rescue event and orientation-link overlap are graph-coupled per trial.
```

It also shows that:

```text
v1.5's cross-validation interpretation should be retracted or superseded.
```

The subset does not establish the opposite positive claim. A larger matched-graph sweep is required.

## Recommended next step

v1.7 should run graph-coupled extraction at canonical scale, with full CLI-controlled coverage over:

```text
seeds
severance_seeds
modes
severities
threshold_fractions
family_semantics
```

v1.7 should report both:

```text
all-pairs mean Jaccard
parent-anchored mean Jaccard
```

and should not promote any orientation-specific rescue result unless it survives matched-graph extraction at scale.
