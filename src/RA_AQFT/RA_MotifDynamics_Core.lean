import RA_D1_Core

/-!
# RA_MotifDynamics_Core

Native-vocabulary front-end for the D1 core.

The purpose of this file is to present the active theorem frontier in
human-readable native names while the underlying file uses the `D1a`/`D1b`/...
derivation labels from RASM.

## Apr 21, 2026 history

This file was simplified twice. First (cleanup pass): the broken
`bdg_weight_*` Prop-aliasing abbrevs and the broken `motif_window_lengths`
reference were removed. Second (rename pass): the underlying D1 file was
renamed from `gluon`/`quark` SM labels to `sym_branch`/`asym_branch` motif
labels, so the two `extensionScore_sym_branch`/`extensionScore_asym_branch`
abbrevs that used to translate the names are now redundant — the D1 file
already uses these names directly.

After both passes, this file is purely an `D1*` → human-friendly-name layer.
-/

noncomputable section

alias chain_window_fixed_point := D1a_fixed_point
alias chain_score_positive_iff := D1a_positive_iff
alias stable_chain_profiles := D1a_three_stable_nvectors
alias chain_unstable_depths := D1a_unstable_depths

alias symmetric_branch_join_stable := D1b_sym_yjoin
alias asymmetric_branch_join_stable := D1b_asym_yjoin
alias minimal_branch_joins_stable := D1b_both_stable

alias symmetric_branch_extension_filtered_after_one := D1c_sym_branch_filtered_step1
alias asymmetric_branch_extension_step1_stable := D1c_asym_branch_step1_stable
alias asymmetric_branch_extension_filtered_after_two := D1c_asym_branch_filtered_step2
alias branch_motif_bounded_vs_chain_persistent := D1c_branch_filter_vs_chain_propagate

alias symmetric_branch_extension_exhaustive := D1c_sym_branch_complete
alias asymmetric_branch_extension_exhaustive := D1c_asym_branch_complete

alias boundary_profile_score := D1_boundary_score
alias boundary_profile_threshold := D1_boundary_threshold
alias boundary_profile_between_filter_and_stable := D1_boundary_between_filter_and_stable

alias depth2_load_profiles := D1f_depth2_values
alias symmetric_branch_depth2_preserved := D1f_sym_branch_depth2_preserved
alias asym_branch_escape_to_chain_preserves_depth2 := D1f_asym_branch_escape_to_chain

alias chain_depth4_orientation_symmetric := D1g_chain4_symmetric
alias transition_profile_orientation_asymmetric := D1g_transition_asymmetric
alias unique_symmetric_stable_profile := D1g_unique_symmetric_stable
