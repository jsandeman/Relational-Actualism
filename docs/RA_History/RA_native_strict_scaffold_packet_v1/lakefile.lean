import Lake
open Lake DSL

package «RelationalActualism»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «RelationalActualism» where
  roots := #[
    `RA_GraphCore_Native,
    `RA_AmpLocality_Native,
    `RA_BDG_Coefficient_Arithmetic,
    `RA_MotifDynamics_Core,
    `RA_CausalOrientation_Core
  ]
