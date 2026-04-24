import Lake
open Lake DSL

package «RelationalActualism»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «RelationalActualism» where
  roots := #[`RA_AQFT_Proofs_v2, `RA_AQFT_Proofs_v10, `RA_D1_Proofs, `RA_Alpha_EM_Proof, `RA_AmpLocality, `RA_Spin2_Macro, `RA_Involutions, `RA_SteinChen, `RA_Threshold, `RA_O14_Uniqueness]