import Lake
open Lake DSL

package «RelationalActualism»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

-- Uncomment the following to discharge the CFC sorry in RA_AQFT_Proofs_v10:
-- require «lean-quantuminfo» from git
--   "https://github.com/Timeroot/Lean-QuantumInfo.git"

@[default_target]
lean_lib «RelationalActualism» where
  roots := #[
    -- Core graph-theoretic foundations (L01, L02, L03)
    `RA_GraphCore,
    -- BDG particle classification (L08, L10, L11, L12, D1a–D1h)
    `RA_D1_Proofs,
    -- Koide lepton mass formula (L09)
    `RA_Koide,
    -- AQFT: frame independence, Rindler, CPTP (L04–L07)
    `RA_AQFT_Proofs_v10,
    -- Amplitude locality + causal invariance (O01, O02)
    `RA_AmpLocality,
    -- Spin-2 DOF count (O10s)
    `RA_Spin2_Macro,
    -- BDG uniqueness: Yeats → Möbius → coefficients (O14)
    `RA_O14_Uniqueness
  ]