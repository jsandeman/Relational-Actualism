import Lake
open Lake DSL

package «RelationalActualism»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

-- CFC proof chain ported from Lean-QuantumInfo (see RA_CFC_Port.lean header).
-- No LQI dependency needed; port is Mathlib-only. Toolchain mismatch with LQI
-- (LQI on v4.23-rc2, RA on v4.29) is sidestepped.

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
    `RA_O14_Uniqueness,
    -- Baryon conservation + chirality (D3a, D3b)
    `RA_BaryonChirality
  ]