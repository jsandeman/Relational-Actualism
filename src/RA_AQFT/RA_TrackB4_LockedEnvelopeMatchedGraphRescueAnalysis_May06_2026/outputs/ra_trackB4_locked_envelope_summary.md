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
- overlap_column_used: orientation_overlap
- estimable_joint_strata_graph: 0
- estimable_joint_strata_control: 0
- graph_mean_joint_gap: None
- control_mean_joint_gap: None
- graph_minus_control_gap: None
- selector_guardrail_passed: True
- orientation_rescue_claim_made: False
- posture: locked_envelope_not_estimable_under_joint_strata

## Guardrail

`orientation_rescue_claim_made` is always false in this packet. B.4 reports a locked-envelope candidate diagnostic only; registry promotion requires human review and must not generalize beyond the B.3b envelope.