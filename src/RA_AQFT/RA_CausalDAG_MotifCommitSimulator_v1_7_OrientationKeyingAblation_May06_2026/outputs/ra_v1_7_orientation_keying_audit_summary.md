# RA v1.7 Orientation-Keying Ablation Summary

v1.7 compares multiple graph-coupled orientation-link keyings on the same matched v0.9 trial stream.
The goal is to determine whether v1.6's negative/reversed orientation-specificity result is stable or keying-dependent.

## Summary

- version: v1.7
- base_matched_trials: 194400
- keyed_rows: 1166400
- keying_count: 6
- keyings: member_indexed_edge_pair;edge_pair_signed_no_member;edge_direction_only;incidence_role_signed;catalog_augmented_edge_pair;shuffled_overlap_control
- seed_start: 17
- seed_stop: 117
- steps: 32
- max_targets: 12
- run_scope: keying_ablation_matched_graph_diagnostic
- per_cell_rows: 1296
- specificity_rows: 36
- partial_correlation_rows: 36
- selector_guardrail_passed: True
- orientation_member_indexed_mean_gap: -0.131267
- orientation_no_member_mean_gap: -0.200566
- any_positive_non_member_orientation_specificity: False
- v1_7_posture: keying_ablation_diagnostic_not_canonical_physical_claim

## Interpretation guardrail

This is a keying-ablation diagnostic, not a Nature-facing result.  No orientation-specific rescue claim should be promoted unless it survives matched-graph extraction under non-member graph/native keyings at canonical scale.