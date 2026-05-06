# Track B.4 locked-envelope matched-graph rescue analysis

This packet analyzes only the B.3b narrow envelope:

- keying: `incidence_role_signed`
- family semantics: `augmented_exact_k`
- threshold fraction: `0.25`

It compares graph-derived incidence-role-signed orientation overlap against shuffled controls under fixed-bin, joint support-width × family-size discipline.

## Summary

- input_rows: 10742400
- locked_envelope_rows: 304200
- graph_rows: 271800
- control_rows: 32400
- rescue_column_used: certification_rescue_event
- overlap_column_used: v1_7_orientation_overlap_all_pairs
- estimable_joint_strata_graph: 0
- estimable_joint_strata_control: 27
- graph_mean_joint_gap: None
- control_mean_joint_gap: 0.011192424329714875
- graph_minus_control_gap: None
- selector_guardrail_passed: True
- orientation_rescue_claim_made: False
- posture: locked_envelope_not_estimable_under_joint_strata

## Guardrail

`orientation_rescue_claim_made` is always false in this packet. B.4 reports a locked-envelope candidate diagnostic only; registry promotion requires human review and must not generalize beyond the B.3b envelope.

## Graph vs shuffled controls

| mode                    | family_semantics   |   threshold_fraction |   severity |   graph_gap |   control_gap |   graph_minus_control_gap |   graph_estimable_joint_strata |   control_estimable_joint_strata | verdict             |
|:------------------------|:-------------------|---------------------:|-----------:|------------:|--------------:|--------------------------:|-------------------------------:|---------------------------------:|:--------------------|
| ledger_failure          | augmented_exact_k  |                 0.25 |       0.25 |         nan |     0.0154684 |                       nan |                            nan |                                3 | graph_not_estimable |
| ledger_failure          | augmented_exact_k  |                 0.25 |       0.5  |         nan |    -0.011676  |                       nan |                            nan |                                3 | graph_not_estimable |
| ledger_failure          | augmented_exact_k  |                 0.25 |       0.75 |         nan |     0.0140348 |                       nan |                            nan |                                3 | graph_not_estimable |
| orientation_degradation | augmented_exact_k  |                 0.25 |       0.25 |         nan |     0.0103507 |                       nan |                            nan |                                3 | graph_not_estimable |
| orientation_degradation | augmented_exact_k  |                 0.25 |       0.5  |         nan |     0.056208  |                       nan |                            nan |                                3 | graph_not_estimable |
| orientation_degradation | augmented_exact_k  |                 0.25 |       0.75 |         nan |     0.0163459 |                       nan |                            nan |                                3 | graph_not_estimable |
| selector_stress         | augmented_exact_k  |                 0.25 |       0.25 |         nan |     0         |                       nan |                            nan |                                3 | graph_not_estimable |
| selector_stress         | augmented_exact_k  |                 0.25 |       0.5  |         nan |     0         |                       nan |                            nan |                                3 | graph_not_estimable |
| selector_stress         | augmented_exact_k  |                 0.25 |       0.75 |         nan |     0         |                       nan |                            nan |                                3 | graph_not_estimable |