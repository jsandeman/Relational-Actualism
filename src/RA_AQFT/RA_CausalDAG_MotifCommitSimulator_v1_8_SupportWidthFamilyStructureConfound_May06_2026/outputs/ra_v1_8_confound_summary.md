# RA v1.8 Support-Width / Family-Structure Confound Audit

This analysis audits whether v1.7 orientation-overlap gaps are explained by support-width, family-size, and binning structure rather than orientation-link specificity.

## Summary metrics

- **version**: v1.8
- **input_rows**: 1166400
- **keying_count**: 6
- **width_classes**: 1;2;3;4
- **family_size_classes**: 1;3;4;5;7;11;15
- **selector_guardrail_passed**: True
- **raw_orientation_gap_rows**: 36
- **width_matched_gap_rows**: 36
- **graph_vs_shuffled_width_rows**: 24
- **mean_abs_raw_gap_graph_keyings**: 0.12914351851851852
- **mean_abs_width_matched_gap_graph_keyings**: 0.11992490447912953
- **mean_abs_graph_minus_shuffled_width_gap**: 0.133677619113775
- **support_width_bin_association_mean_abs**: 0.6341048122090346
- **family_size_bin_association_mean_abs**: 0.6668007842464604
- **v1_8_posture**: confound_audit_outputs_ready_for_canonical_v1_7_inputs

## Interpretation discipline

- A persistent graph-vs-shuffled match within width/family strata supports a binning/family-structure artifact interpretation.
- A graph-derived gap that survives width/family matching and differs from shuffled controls would motivate renewed orientation-specific investigation.
- This packet is analysis-only and does not introduce new Lean or simulator semantics.

