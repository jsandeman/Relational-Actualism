import Lake
open Lake DSL

package «RelationalActualism»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

/-
  Active roots (Apr 21, 2026 — post rename pass).

  This iteration completed two passes on the same day:
    1. Cleanup pass — fixed import plumbing and 2 small bugs in
       RA_MotifDynamics_Core; restored RA_GraphCore, RA_AmpLocality,
       RA_Koide, RA_Spin2_Macro, RA_CausalOrientation_Core to roots.
    2. Rename pass — renamed SM-flavored identifiers in RA_D1_Core_draft to
       motif-native names (gluon→sym_branch, quark→asym_branch,
       confinement→filter_horizon, n2→depth2, etc.). File renames:
         RA_Koide.lean        → RA_KvalRatio.lean
         RA_Spin2_Macro.lean  → RA_BDG_LLC_Kernel.lean

  Structure:
    Tier A (fully native bedrock):
      RA_GraphCore, RA_O14_Uniqueness_Core_draft,
      RA_BDG_Coefficient_Arithmetic
    Tier B (native content + native names):
      RA_D1_Core_draft, RA_KvalRatio, RA_BDG_LLC_Kernel
    Tier C (half-native — Complex.exp amplitude, flagged for later review):
      RA_AmpLocality
    Native-vocabulary wrappers:
      RA_GraphCore_Native, RA_AmpLocality_Native,
      RA_MotifDynamics_Core, RA_CausalOrientation_Core

  Retired from active roots (archival files remain in directory):
    RA_AQFT_Proofs_v10  — QFT-as-mechanism (IC46 framing violation)
    RA_CFC_Port         — support for AQFT, broken against current Mathlib
    RA_BaryonChirality  — faithfully renamed in RA_CausalOrientation_Core
    RA_Koide            — renamed to RA_KvalRatio
    RA_Spin2_Macro      — renamed to RA_BDG_LLC_Kernel
-/

@[default_target]
lean_lib «RelationalActualism» where
  roots := #[
    -- Tier A — bedrock
    `RA_GraphCore,
    `RA_O14_ArithmeticCore_v1,
    `RA_BDG_Coefficient_Arithmetic,
    `RA_BDG_ActualizationRate,  -- Tier 3c (May 3 2026): formalizes the
                                -- BDG-kernel actualization-rate construction
                                -- λ_pos = Γ_cand · P_acc(μ); arithmetic and
                                -- algebraic content (probability layer is
                                -- abstract, deferred to Tier 3d).

    -- Tier B — native content
    `RA_D1_Core_draft,
    `RA_KvalRatio,
    `RA_BDG_LLC_Kernel,
    `RA_D1_NativeKernel_v1,
    `RA_D1_NativeConfinement_v1,
    `RA_D1_NativeClosure_v1,
    `RA_D1_NativeLedgerOrientation_v1,
    `RA_D1_GraphCutCombinatorics,
    `RA_D1_NativeDimensionality_v1,
    `RA_ActualizationSelector_v1,
    `RA_FrontierIncidence_v1,
    `RA_FrontierGraphBridge_v1,
    `RA_HasseFrontier_v1,
    `RA_HasseFrontier_Maximal_v1,
    `RA_HasseFrontier_FiniteMax_v1,
    `RA_HasseFrontier_FiniteMaxExist_v1,
    `RA_IncidenceCharge_v1,
    `RA_IncidenceSignSource_v1,
    `RA_GraphOrientationChart_v1,
    `RA_GraphOrientationClosure_v1,
    `RA_D3_CausalSeverance,
    `RA_D3_CosmologicalExpansion,
    `RA_D4_CausalFirewall,

    -- Tier C — flagged for native-content review (not yet repaired)
    `RA_AmpLocality,

    -- Native-vocabulary wrappers
    `RA_GraphCore_Native,
    `RA_AmpLocality_Native,
    `RA_MotifDynamics_Core,
    `RA_CausalOrientation_Core,
    `RA_D2_MatterCartography,
    `RA_D2_HadronMassTriad
  ]
