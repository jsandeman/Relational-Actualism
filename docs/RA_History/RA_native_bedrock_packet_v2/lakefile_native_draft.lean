import Lake
open Lake DSL

package «RelationalActualismNative»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

@[default_target]
lean_lib «RelationalActualismNative» where
  roots := #[
    `RA_GraphCore,
    `RA_AmpLocality,
    `RA_O14_Uniqueness_Core_draft,
    `RA_D1_Core_draft
  ]
