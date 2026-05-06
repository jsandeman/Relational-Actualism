# RA v1.8.1 Joint Width × Family-Size Confound Audit

This refines v1.8 by stratifying simultaneously on support_width AND family_size (and threshold/severity/mode/semantics).

## Summary metrics

- **version**: v1.8.1
- **input_rows**: 1166400
- **keying_count**: 6
- **n_stratum_combinations**: 216
- **n_strata_with_data**: 1296
- **n_strata_estimable_any_keying**: 126
- **selector_guardrail_passed**: True
- **mean_abs_raw_gap_graph_keyings**: 0.12914351851851852
- **mean_abs_width_matched_gap_graph_keyings**: 0.11992490447912953
- **mean_abs_joint_matched_gap_graph_keyings**: 0.003236121791916203
- **mean_abs_joint_matched_gap_shuffled**: 0.0029269142470236867
- **mean_abs_graph_minus_shuffled_joint**: 0.005013189208029935
- **fraction_explained_by_width_graph**: 0.07030541528772771
- **fraction_explained_by_joint_graph**: 1.0088682371390565
- **estimable_strata_fraction_graph**: 0.14583333333333334
- **v1_8_1_posture**: joint_width_family_matched_confound_audit_complete

## Per-cell decomposition (orientation_degradation)

| keying | family_semantics | raw | width-matched | joint-matched | verdict |
|---|---|---|---|---|---|
| catalog_augmented_edge_pair | at_least_k | -0.2088 | -0.1795 | 0.0099 | joint_matched_gap_collapses_to_zero |
| catalog_augmented_edge_pair | augmented_exact_k | -0.1879 | -0.1801 | 0.0034 | joint_matched_gap_collapses_to_zero |
| edge_direction_only | at_least_k | -0.1983 | -0.1772 | n/a | joint_matched_non_estimable |
| edge_direction_only | augmented_exact_k | -0.1886 | -0.1826 | n/a | joint_matched_non_estimable |
| edge_pair_signed_no_member | at_least_k | -0.1983 | -0.1772 | n/a | joint_matched_non_estimable |
| edge_pair_signed_no_member | augmented_exact_k | -0.1886 | -0.1826 | n/a | joint_matched_non_estimable |
| incidence_role_signed | at_least_k | -0.1983 | -0.1772 | n/a | joint_matched_non_estimable |
| incidence_role_signed | augmented_exact_k | -0.1886 | -0.1826 | n/a | joint_matched_non_estimable |
| member_indexed_edge_pair | at_least_k | -0.1209 | -0.0624 | 0.0205 | joint_matched_gap_weak_residual |
| member_indexed_edge_pair | augmented_exact_k | -0.0294 | -0.0042 | -0.0106 | joint_matched_gap_collapses_to_zero |
| shuffled_overlap_control | at_least_k | -0.1931 | 0.1709 | -0.0011 | joint_matched_gap_collapses_to_zero |
| shuffled_overlap_control | augmented_exact_k | -0.1539 | -0.0130 | 0.0071 | joint_matched_gap_collapses_to_zero |

## Graph vs shuffled within joint strata (orientation_degradation)

| graph_keying | family_semantics | graph_mean | shuffled_mean | delta | interpretation |
|---|---|---|---|---|---|
| catalog_augmented_edge_pair | at_least_k | 0.0099 | -0.0011 | 0.0110 | graph_collapses_to_shuffled_after_joint_matching |
| catalog_augmented_edge_pair | augmented_exact_k | 0.0034 | 0.0071 | -0.0036 | graph_collapses_to_shuffled_after_joint_matching |

## Interpretation discipline

- If joint-matched graph gap collapses (|gap| < 0.02), the v1.7 reversed gap is fully explained by support_width × family_size structure (Case A).
- If joint-matched graph gap survives (|gap| >= 0.05) AND graph differs from shuffled in joint strata, there is a candidate residual orientation-overlap association (Case B).
- If non-estimable strata dominate, a redesigned sampler is needed (Case C).
- This packet remains analysis-only; nothing here is a Nature-facing claim.

