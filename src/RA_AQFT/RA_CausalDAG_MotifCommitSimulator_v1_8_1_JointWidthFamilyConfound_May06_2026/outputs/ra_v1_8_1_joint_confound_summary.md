# RA v1.8.1 Joint Width × Family-Size Confound Audit

This analysis extends v1.8 by matching low/high orientation-overlap bins within exact support_width × family_size strata. It is analysis-only and makes no Lean or simulator-semantics changes.

## Summary metrics

- **version**: v1.8.1
- **input_rows**: 1166400
- **keying_count**: 6
- **width_classes**: 1;2;3;4
- **family_size_classes**: 1;3;4;5;7;11;15
- **selector_guardrail_passed**: True
- **raw_gap_rows**: 324
- **width_matched_gap_rows**: 324
- **joint_matched_gap_rows**: 324
- **graph_vs_shuffled_joint_rows**: 216
- **estimable_joint_group_fraction_graph**: 0.0
- **mean_abs_raw_gap_graph**: 0.1242669478059048
- **mean_abs_width_gap_graph**: nan
- **mean_abs_joint_gap_graph**: nan
- **mean_abs_graph_minus_shuffled_joint_gap**: nan
- **mean_joint_gap_reduction_from_raw_graph**: nan
- **v1_8_1_posture**: joint_width_family_matching_not_estimable_redesign_sampler_needed

## Decision discipline

- If graph-derived gaps shrink under joint width × family-size matching, the residual v1.8 signal is explained by family-structure confounding.
- If graph-derived gaps survive and differ from shuffled controls inside the same joint strata, the result supports a candidate residual graph-derived orientation association.
- If few or no joint strata are estimable, the current sampler cannot decide the question and a redesigned matched sampler is required.

## Orientation-degradation focus

- catalog_augmented_edge_pair / at_least_k / sev=0.25 / th=0.25: raw=-0.164, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.25 / th=0.5: raw=-0.1094, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.25 / th=0.75: raw=-0.09242, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.5 / th=0.25: raw=-0.2985, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.5 / th=0.5: raw=-0.2032, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.5 / th=0.75: raw=-0.15, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.75 / th=0.25: raw=-0.3323, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.75 / th=0.5: raw=-0.2584, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / at_least_k / sev=0.75 / th=0.75: raw=-0.1909, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.25 / th=0.25: raw=-0.1499, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.25 / th=0.5: raw=-0.1331, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.25 / th=0.75: raw=-0.09242, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.5 / th=0.25: raw=-0.2194, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.5 / th=0.5: raw=-0.2189, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.5 / th=0.75: raw=-0.15, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.75 / th=0.25: raw=-0.2322, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.75 / th=0.5: raw=-0.2365, width=nan, joint=nan, joint_matching_not_estimable
- catalog_augmented_edge_pair / augmented_exact_k / sev=0.75 / th=0.75: raw=-0.1909, width=nan, joint=nan, joint_matching_not_estimable
- edge_direction_only / at_least_k / sev=0.25 / th=0.25: raw=-0.1608, width=nan, joint=nan, joint_matching_not_estimable
- edge_direction_only / at_least_k / sev=0.25 / th=0.5: raw=-0.1136, width=nan, joint=nan, joint_matching_not_estimable
