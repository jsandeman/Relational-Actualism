# RA Native Rename Docket v1

## `RA_GraphCore.lean`

- `horizon_partition` → move to translation layer (do not keep in native root)
- `MarkovBlanket` → `CausalShield`
- `MarkovBlanket.boundary` → `CausalShield.boundary`

## `RA_AmpLocality.lean`

- `quantum_measure` → `extension_weight_normsq` or `bdg_readout_measure`
- `bdg_causal_invariance` → `bdg_extension_order_invariance`

## `RA_O14_Uniqueness.lean`

Move these out of the native core:
- `alpha_inv_137`
- `twelve_squared`
- `screening_seven`
- `alpha_s_weight`

Keep the arithmetic O14 core under its present names if desired.

## `RA_D1_Proofs.lean`

Native replacements should shift from particle labels to motif / N-vector labels.

Suggested first-pass renames:

- `D1b_sym_yjoin` → `D1b_symmetric_Y_motif`
- `D1b_asym_yjoin` → `D1b_asymmetric_Y_motif`
- `D1c_gluon_confined` → `D1c_symmetric_Y_extension_filtered`
- `D1c_quark_step1_stable` → `D1c_asymmetric_Y_first_extension_stable`
- `D1c_quark_confined` → `D1c_asymmetric_Y_second_extension_filtered`
- `D1d_gluon_convergence` → `D1d_symmetric_Y_convergence`
- `D1d_quark_convergence` → `D1d_asymmetric_Y_convergence`
- `gluon_confinement_length` → `symmetric_Y_confinement_length`
- `quark_confinement_length` → `asymmetric_Y_confinement_length`
- `D1f_n2_values` → `D1f_N2_winding_values`
- `D1f_gluon_n2_preserved` → `D1f_symmetric_Y_N2_preserved`
- `D1f_quark_escape_sequential` → `D1f_asymmetric_Y_escape_to_sequential`
- `D1g_chain4_symmetric` → `D1g_chain4_depth_symmetry`
- `D1g_transition_asymmetric` → `D1g_transition_depth_asymmetry`
- `D1g_unique_symmetric_stable` → `D1g_unique_symmetric_fixed_point`

Move these entirely out of the native root:
- all `D1h_*`
- `relative_entropy_self_zero`
- `vacuum_stress_energy_zero`
- `P_act_linear_zero`
- `P_act_conservation`
- `RA_field_equation_unique`
- `universe_closure` (or rewrite the alias in neutral language)
