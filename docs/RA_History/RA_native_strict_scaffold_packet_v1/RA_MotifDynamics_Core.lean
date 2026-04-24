import RA_D1_Core_draft

/-!
# RA_MotifDynamics_Core

Transitional native wrapper for the D1 core.

The purpose of this file is to present the active theorem frontier in native
motif/depth/orientation language while the underlying `RA_D1_Proofs` split is
performed in-repo. The final step should be to move these declarations into a
compile-tested source file and retire the old translation-facing names.
-/

noncomputable section

abbrev bdg_weight_birth := bdg_c0
abbrev bdg_weight_depth1 := bdg_c1
abbrev bdg_weight_depth2 := bdg_c2
abbrev bdg_weight_depth3 := bdg_c3
abbrev bdg_weight_depth4 := bdg_c4

theorem chain_window_fixed_point := D1a_fixed_point
theorem chain_score_positive_iff := D1a_positive_iff
theorem stable_chain_profiles := D1a_three_stable_nvectors
theorem chain_unstable_depths := D1a_unstable_depths

theorem symmetric_branch_join_stable := D1b_sym_yjoin
theorem asymmetric_branch_join_stable := D1b_asym_yjoin
theorem minimal_branch_joins_stable := D1b_both_stable

theorem symmetric_branch_extension_filtered_after_one := D1c_gluon_confined
theorem asymmetric_branch_extension_step1_stable := D1c_quark_step1_stable
theorem asymmetric_branch_extension_filtered_after_two := D1c_quark_confined
theorem branch_motif_bounded_vs_chain_persistent := D1c_confinement_vs_propagation

abbrev extensionScore_sym_branch := extensionScore_gluon
abbrev extensionScore_asym_branch := extensionScore_quark

theorem symmetric_branch_extension_exhaustive := D1c_gluon_complete
theorem asymmetric_branch_extension_exhaustive := D1c_quark_complete

theorem boundary_profile_score := D1_boundary_score
theorem boundary_profile_threshold := D1_boundary_threshold
theorem boundary_profile_between_filter_and_stable := D1_boundary_between_filter_and_stable

theorem depth2_load_profiles := D1f_n2_values
theorem symmetric_branch_depth2_preserved := D1f_gluon_n2_preserved
theorem asym_branch_escape_to_chain_preserves_depth2 := D1f_quark_escape_sequential

theorem chain_depth4_orientation_symmetric := D1g_chain4_symmetric
theorem transition_profile_orientation_asymmetric := D1g_transition_asymmetric
theorem unique_symmetric_stable_profile := D1g_unique_symmetric_stable

theorem motif_window_lengths := confinement_lengths
