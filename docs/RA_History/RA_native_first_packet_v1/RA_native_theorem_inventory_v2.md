# RA-Native Theorem Inventory v2

This is the original declaration inventory retagged by file-level nativeness and proof hygiene metrics.

## File-level summary

| file                           | file_nativeness_class    |   executable_sorry_count |   executable_axiom_count |   theorem_count |   lemma_count | file_rationale                                                                                      |
|:-------------------------------|:-------------------------|-------------------------:|-------------------------:|----------------:|--------------:|:----------------------------------------------------------------------------------------------------|
| RA_AQFT_CFC_Patch.lean         | deferred-bridge          |                        0 |                        0 |               0 |             0 | AQFT patch helper.                                                                                  |
| RA_AQFT_Proofs.lean            | deferred-bridge          |                        7 |                        3 |               4 |             3 | Shadow AQFT file.                                                                                   |
| RA_AQFT_Proofs_v10.lean        | deferred-bridge          |                        1 |                        2 |               4 |             5 | AQFT adapter, not on current critical path.                                                         |
| RA_AQFT_Proofs_v2.lean         | deferred-bridge          |                        0 |                        0 |              10 |            10 | Legacy AQFT file.                                                                                   |
| RA_CFC_Port.lean               | deferred-bridge          |                        0 |                        0 |               5 |             0 | Support file for AQFT adapter.                                                                      |
| RA_Spin2_Macro.lean            | deferred-bridge          |                        0 |                        0 |               1 |             1 | Macro/continuum spin-2 bridge.                                                                      |
| RA_PACT_conservation_lean.lean | mixed-rewrite            |                        0 |                        1 |               6 |             0 | Potentially important conservation file, but current naming/bridge status is unclear.               |
| RA_Proofs_Lean4.lean           | mixed-rewrite            |                        1 |                        3 |               9 |             8 | Legacy omnibus file; contains bridge and older scaffolding.                                         |
| RA_AmpLocality.lean            | native-bedrock           |                        0 |                        0 |               2 |             3 | Amplitude locality and causal invariance closure.                                                   |
| RA_D1_Proofs.lean              | native-bedrock           |                        0 |                        0 |              67 |             9 | Discrete proof spine for stability, confinement, and motif classes.                                 |
| RA_GraphCore.lean              | native-bedrock           |                        0 |                        0 |               2 |            11 | Graph/DAG primitives, cuts, and horizon partition.                                                  |
| RA_O14_Uniqueness.lean         | native-bedrock           |                        0 |                        0 |              50 |             0 | BDG integer uniqueness / Möbius inversion backbone.                                                 |
| RA_Alpha_EM_Proof.lean         | native-candidate         |                        0 |                        0 |              14 |             6 | Nature-facing numeric target; audit hidden imported formulas carefully.                             |
| RA_BaryonChirality.lean        | native-candidate         |                        0 |                        0 |              12 |             1 | Native if interpreted through N2 winding and DAG chirality rather than imported labels.             |
| RA_Koide.lean                  | native-candidate         |                        0 |                        0 |               7 |             5 | Mass-pattern theorem chain, still needs input/category audit.                                       |
| RA_Complexity_Proofs.lean      | native-candidate-nonroot |                      nan |                      nan |             nan |           nan | Complexity/life extension outside default root; mature theorems should migrate inward once cleaned. |

## Bedrock declaration frontier

| file                   | kind    | name                                  |   line |
|:-----------------------|:--------|:--------------------------------------|-------:|
| RA_AmpLocality.lean    | lemma   | interval_subset_past                  |     52 |
| RA_AmpLocality.lean    | lemma   | interval_eq_interval_past             |     62 |
| RA_AmpLocality.lean    | lemma   | bdg_increment_depends_on_past_only    |     83 |
| RA_AmpLocality.lean    | theorem | bdg_amplitude_locality                |    127 |
| RA_AmpLocality.lean    | theorem | bdg_causal_invariance                 |    171 |
| RA_D1_Proofs.lean      | lemma   | bdg_c0                                |     62 |
| RA_D1_Proofs.lean      | lemma   | bdg_c1                                |     63 |
| RA_D1_Proofs.lean      | lemma   | bdg_c2                                |     64 |
| RA_D1_Proofs.lean      | lemma   | bdg_c3                                |     66 |
| RA_D1_Proofs.lean      | lemma   | bdg_c4                                |     67 |
| RA_D1_Proofs.lean      | lemma   | chain_score_via_bdg_0                 |     88 |
| RA_D1_Proofs.lean      | lemma   | chain_score_via_bdg_2                 |     89 |
| RA_D1_Proofs.lean      | lemma   | chain_score_via_bdg_3                 |     90 |
| RA_D1_Proofs.lean      | lemma   | chain_score_via_bdg_4                 |     91 |
| RA_D1_Proofs.lean      | theorem | D1a_fixed_point                       |     96 |
| RA_D1_Proofs.lean      | theorem | D1a_positive_iff                      |    102 |
| RA_D1_Proofs.lean      | theorem | D1a_three_stable_nvectors             |    116 |
| RA_D1_Proofs.lean      | theorem | D1a_unstable_depths                   |    125 |
| RA_D1_Proofs.lean      | theorem | D1b_sym_yjoin                         |    158 |
| RA_D1_Proofs.lean      | theorem | D1b_asym_yjoin                        |    162 |
| RA_D1_Proofs.lean      | theorem | D1b_both_stable                       |    165 |
| RA_D1_Proofs.lean      | theorem | D1c_gluon_confined                    |    205 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_step1_stable                |    208 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_confined                    |    211 |
| RA_D1_Proofs.lean      | theorem | D1c_confinement_vs_propagation        |    216 |
| RA_D1_Proofs.lean      | theorem | D1_master                             |    245 |
| RA_D1_Proofs.lean      | theorem | D1c_gluon_step0                       |    300 |
| RA_D1_Proofs.lean      | theorem | D1c_gluon_step1                       |    301 |
| RA_D1_Proofs.lean      | theorem | D1c_gluon_step2                       |    302 |
| RA_D1_Proofs.lean      | theorem | D1c_gluon_step3                       |    303 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_step0                       |    306 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_step1                       |    307 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_step2                       |    308 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_step3                       |    309 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_step4                       |    310 |
| RA_D1_Proofs.lean      | theorem | D1c_gluon_has_filter                  |    313 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_has_filter                  |    316 |
| RA_D1_Proofs.lean      | theorem | D1d_gluon_convergence                 |    334 |
| RA_D1_Proofs.lean      | theorem | D1d_quark_convergence                 |    344 |
| RA_D1_Proofs.lean      | theorem | D1e_finite_confinement                |    379 |
| RA_D1_Proofs.lean      | theorem | D1_extended_master                    |    408 |
| RA_D1_Proofs.lean      | theorem | D1c_gluon_complete                    |    568 |
| RA_D1_Proofs.lean      | theorem | D1c_quark_complete                    |    579 |
| RA_D1_Proofs.lean      | theorem | D1_gluon_extension_scores             |    609 |
| RA_D1_Proofs.lean      | theorem | D1_quark_extension_scores             |    619 |
| RA_D1_Proofs.lean      | theorem | D1_closure                            |    632 |
| RA_D1_Proofs.lean      | theorem | D1_closure_quark_t1                   |    757 |
| RA_D1_Proofs.lean      | theorem | D1_closure_gluon_t2                   |    764 |
| RA_D1_Proofs.lean      | theorem | D1_closure_complete                   |    774 |
| RA_D1_Proofs.lean      | theorem | D1_boundary_score                     |    814 |
| RA_D1_Proofs.lean      | theorem | D1_boundary_threshold                 |    817 |
| RA_D1_Proofs.lean      | theorem | D1_boundary_between_filter_and_stable |    822 |
| RA_D1_Proofs.lean      | theorem | D1f_n2_values                         |    851 |
| RA_D1_Proofs.lean      | theorem | D1f_gluon_n2_preserved                |    863 |
| RA_D1_Proofs.lean      | theorem | D1f_quark_escape_sequential           |    873 |
| RA_D1_Proofs.lean      | theorem | D1g_chain4_symmetric                  |    907 |
| RA_D1_Proofs.lean      | theorem | D1g_transition_asymmetric             |    910 |
| RA_D1_Proofs.lean      | theorem | D1g_unique_symmetric_stable           |    920 |
| RA_D1_Proofs.lean      | theorem | D1h_singlet_amplitude_sq              |    984 |
| RA_D1_Proofs.lean      | theorem | D1h_doublet_amplitude_sq              |    988 |
| RA_D1_Proofs.lean      | theorem | D1h_amplitude_ratio                   |    992 |
| RA_D1_Proofs.lean      | theorem | D1h_clebsch_gordan                    |    998 |
| RA_D1_Proofs.lean      | theorem | D1h_doublet_equal_amplitudes          |   1002 |
| RA_D1_Proofs.lean      | theorem | D1h_lepton_doublet_delta              |   1007 |
| RA_D1_Proofs.lean      | theorem | D1h_quark_doublet_delta               |   1010 |
| RA_D1_Proofs.lean      | theorem | D1h_hypercharge_ratio                 |   1014 |
| RA_D1_Proofs.lean      | theorem | D1h_GMN_electron                      |   1018 |
| RA_D1_Proofs.lean      | theorem | D1h_GMN_up_quark                      |   1025 |
| RA_D1_Proofs.lean      | theorem | D1h_GMN_down_quark                    |   1030 |
| RA_D1_Proofs.lean      | theorem | D1h_isospin_master                    |   1038 |
| RA_D1_Proofs.lean      | theorem | delta_at_zero_times_zero              |   1110 |
| RA_D1_Proofs.lean      | theorem | distributional_product_zero           |   1116 |
| RA_D1_Proofs.lean      | theorem | relative_entropy_self_zero            |   1123 |
| RA_D1_Proofs.lean      | theorem | vacuum_stress_energy_zero             |   1127 |
| RA_D1_Proofs.lean      | theorem | LLC_conservation_consequence          |   1132 |
| RA_D1_Proofs.lean      | theorem | P_act_linear_zero                     |   1136 |
| RA_D1_Proofs.lean      | theorem | P_act_conservation                    |   1149 |
| RA_D1_Proofs.lean      | theorem | RA_field_equation_unique              |   1157 |
| RA_D1_Proofs.lean      | theorem | confinement_lengths                   |   1175 |
| RA_D1_Proofs.lean      | theorem | universe_closure                      |   1181 |
| RA_D1_Proofs.lean      | theorem | structural_fragility                  |   1197 |
| RA_GraphCore.lean      | lemma   | outgoing_pairwise_disjoint            |     86 |
| RA_GraphCore.lean      | lemma   | incoming_pairwise_disjoint            |     94 |
| RA_GraphCore.lean      | lemma   | outgoing_pairwise_disjoint_VL         |    102 |
| RA_GraphCore.lean      | lemma   | incoming_pairwise_disjoint_VL         |    107 |
| RA_GraphCore.lean      | lemma   | biUnion_outgoing_eq_src_in_VL         |    113 |
| RA_GraphCore.lean      | lemma   | biUnion_incoming_eq_dst_in_VL         |    122 |
| RA_GraphCore.lean      | lemma   | internal_flux_disjoint                |    131 |
| RA_GraphCore.lean      | lemma   | src_in_VL_eq_internal_union_boundary  |    138 |
| RA_GraphCore.lean      | lemma   | dst_in_VL_eq_internal                 |    155 |
| RA_GraphCore.lean      | lemma   | sum_outgoing_decompose                |    170 |
| RA_GraphCore.lean      | lemma   | sum_incoming_decompose                |    184 |
| RA_GraphCore.lean      | theorem | RA_graph_cut_theorem                  |    200 |
| RA_GraphCore.lean      | theorem | horizon_partition                     |    214 |
| RA_O14_Uniqueness.lean | theorem | yeats_r0                              |     24 |
| RA_O14_Uniqueness.lean | theorem | yeats_r1                              |     25 |
| RA_O14_Uniqueness.lean | theorem | yeats_r2                              |     26 |
| RA_O14_Uniqueness.lean | theorem | yeats_r3                              |     27 |
| RA_O14_Uniqueness.lean | theorem | yeats_r4                              |     28 |
| RA_O14_Uniqueness.lean | theorem | choose_0_0                            |     44 |
| RA_O14_Uniqueness.lean | theorem | choose_1_0                            |     45 |
| RA_O14_Uniqueness.lean | theorem | choose_1_1                            |     46 |
| RA_O14_Uniqueness.lean | theorem | choose_2_0                            |     47 |
| RA_O14_Uniqueness.lean | theorem | choose_2_1                            |     48 |
| RA_O14_Uniqueness.lean | theorem | choose_2_2                            |     49 |
| RA_O14_Uniqueness.lean | theorem | choose_3_0                            |     50 |
| RA_O14_Uniqueness.lean | theorem | choose_3_1                            |     51 |
| RA_O14_Uniqueness.lean | theorem | choose_3_2                            |     52 |
| RA_O14_Uniqueness.lean | theorem | choose_3_3                            |     53 |
| RA_O14_Uniqueness.lean | theorem | choose_4_1                            |     56 |
| RA_O14_Uniqueness.lean | theorem | choose_4_2                            |     57 |
| RA_O14_Uniqueness.lean | theorem | choose_4_3                            |     58 |
| RA_O14_Uniqueness.lean | theorem | choose_4_4                            |     59 |
| RA_O14_Uniqueness.lean | theorem | C1_eq                                 |     74 |
| RA_O14_Uniqueness.lean | theorem | C2_eq                                 |     77 |
| RA_O14_Uniqueness.lean | theorem | C3_eq                                 |     80 |
| RA_O14_Uniqueness.lean | theorem | C4_eq                                 |     83 |
| RA_O14_Uniqueness.lean | theorem | bdg_C_vector                          |     86 |
| RA_O14_Uniqueness.lean | theorem | bdg_action_vector                     |     93 |
| RA_O14_Uniqueness.lean | theorem | second_order                          |    104 |