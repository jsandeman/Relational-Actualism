import Lake
open Lake DSL

package «RelationalActualism»

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git"

/-
  Active roots — May 4, 2026 (post version-suffix cleanup pass).

  Naming-convention pass: stripped `_v1`, `_v2`, `_draft` suffixes from
  filenames; metadata about file age/version now lives in file
  comments instead. Semantic role suffixes `_Core` and `_Native` are
  retained because they distinguish files that coexist
  (`RA_GraphCore` vs `RA_GraphCore_Native`).

  Earlier passes (preserved for context):
    - Apr 21, 2026 cleanup: fixed import plumbing + 2 small bugs in
      RA_MotifDynamics_Core; restored RA_GraphCore, RA_AmpLocality,
      RA_KvalRatio, RA_BDG_LLC_Kernel, RA_CausalOrientation_Core to
      roots.
    - Apr 21, 2026 rename: SM-flavored identifiers in RA_D1_Core
      renamed to motif-native names (gluon→sym_branch,
      quark→asym_branch, confinement→filter_horizon, n2→depth2, etc.).
      File renames: RA_Koide → RA_KvalRatio, RA_Spin2_Macro →
      RA_BDG_LLC_Kernel.
    - May 3, 2026: added RA_BDG_ActualizationRate (Tier 3c) and
      RA_BDG_PAccMeasure (Tier 3d) for the BMV-pipeline Lean
      formalization of the actualization-rate construction.
    - May 4, 2026: added RA_O01_KernelLocality (Tier A bedrock; kernel
      locality dependency) and RA_MotifCommitProtocol (Tier B native
      content; consensus-inspired motif-commit semantics with
      finite-Hasse-frontier ↔ causal-support-cut bridge).

  Structure:
    Tier A (fully native bedrock):
      RA_GraphCore, RA_O14_ArithmeticCore, RA_BDG_Coefficient_Arithmetic,
      RA_BDG_ActualizationRate, RA_BDG_PAccMeasure, RA_O01_KernelLocality
    Tier B (native content + native names):
      RA_D1_Core, RA_KvalRatio, RA_BDG_LLC_Kernel, RA_MotifCommitProtocol
    Tier C (half-native — Complex.exp amplitude, flagged for later review):
      RA_AmpLocality
    Native-vocabulary wrappers:
      RA_GraphCore_Native, RA_AmpLocality_Native,
      RA_MotifDynamics_Core, RA_CausalOrientation_Core

  Retired from active roots (zipped into archive_lean_deprecated_May4_2026.zip):
    RA_AQFT_Proofs, RA_AQFT_Proofs_v2, RA_AQFT_Proofs_v10
                       — QFT-as-mechanism (IC46 framing violation)
    RA_AQFT_CFC_Patch  — patch for retired AQFT_Proofs_v10
    RA_CFC_Port        — broken against current Mathlib
    RA_BaryonChirality — faithfully renamed in RA_CausalOrientation_Core
    RA_AmpLocality_v2  — duplicate of RA_AmpLocality
    RA_GraphCore_v2    — "v2 sorry closure attempt"; superseded
    RA_O14_Uniqueness, RA_O14_Uniqueness_Core_draft
                       — superseded by RA_O14_ArithmeticCore
    RA_D1_Proofs       — older D1 proofs; superseded by D1_Core + D1_Native* family
    RA_BDG_Coefficient_Arithmetic_v2 — content moved into canonical file
    RA_Alpha_EM_Proof, RA_PACT_conservation_lean, RA_Proofs_Lean4
                       — exploratory; never in roots
    RA_Koide           — renamed to RA_KvalRatio
    RA_Spin2_Macro     — renamed to RA_BDG_LLC_Kernel
    lakefile_v1.lean   — prior lakefile config; superseded
-/

@[default_target]
lean_lib «RelationalActualism» where
  roots := #[
    -- Tier A — bedrock
    `RA_GraphCore,
    `RA_O14_ArithmeticCore,
    `RA_BDG_Coefficient_Arithmetic,
    `RA_BDG_ActualizationRate,  -- Tier 3c (May 3 2026): formalizes the
                                -- BDG-kernel actualization-rate construction
                                -- λ_pos = Γ_cand · P_acc(μ); arithmetic and
                                -- algebraic content (probability layer is
                                -- abstract, deferred to Tier 3d).
    `RA_BDG_PAccMeasure,        -- Tier 3d (May 3 2026): measure-theoretic
                                -- interface — lifts P_acc from abstract real
                                -- to (Measure BDGProfile → ℝ) via Mathlib's
                                -- MeasureTheory; full Poisson-CSG product
                                -- construction (Tier 3e) still open.
    `RA_O01_KernelLocality,     -- (May 4 2026) kernel-locality lemma; new
                                -- bedrock dependency for RA_MotifCommitProtocol.

    -- Tier B — native content
    `RA_D1_Core,
    `RA_KvalRatio,
    `RA_BDG_LLC_Kernel,
    `RA_D1_NativeKernel,
    `RA_D1_NativeConfinement,
    `RA_D1_NativeClosure,
    `RA_D1_NativeLedgerOrientation,
    `RA_D1_GraphCutCombinatorics,
    `RA_D1_NativeDimensionality,
    `RA_ActualizationSelector,
    `RA_FrontierIncidence,
    `RA_FrontierGraphBridge,
    `RA_HasseFrontier,
    `RA_HasseFrontier_Maximal,
    `RA_HasseFrontier_FiniteMax,
    `RA_HasseFrontier_FiniteMaxExist,
    `RA_IncidenceCharge,
    `RA_IncidenceSignSource,
    `RA_GraphOrientationChart,
    `RA_GraphOrientationClosure,
    `RA_MotifCommitProtocol,    -- (May 4 2026) consensus-inspired motif-commit
                                -- semantics; finite-Hasse-frontier ↔ causal-
                                -- support-cut bridge for motif readiness.
    `RA_MotifSelectorClosure,   -- (May 4 2026) selector-closure bridge for
                                -- motif-commit semantics; certified-readiness
                                -- → selector closure → selected commitment.
    `RA_MotifOrientationSupportBridge,  -- (May 4 2026) certificate-level
                                -- bridge from graph-orientation closure into
                                -- motif support / selector closure.
    `RA_MotifCausalSeveranceBridge,     -- (May 4 2026) post-severance
                                -- readiness / commitment / depth-finality
                                -- predicates over the graph motif-commit
                                -- stack; abstract reachability profile.
    `RA_MotifSupportFamilyBridge,       -- (May 5 2026) support-cut family
                                -- (alternative-cut redundancy) layer over
                                -- motif-commit; AnyCutReadyAt /
                                -- AllCutReadyAt / FamilyCommitsAt.
    `RA_MotifSupportFamilyMonotonicity, -- (May 5 2026) family inclusion +
                                -- monotonicity theorems for FamilyReadyAt /
                                -- CertifiedFamilyReadyAt / FamilyCommitsAt.
    `RA_MotifCertifiedSupportFamilyBridge, -- (May 5 2026) certificate-family
                                -- contexts; IndependentCertifiedFamilyReadyAt
                                -- + .of_member + .to_certified_family_ready
                                -- + .mono_certificates + .future_mono.
    `RA_MotifNativeCertificateOverlapBridge, -- (May 5 2026) native-overlap
                                -- bridge: Type-valued witness data,
                                -- overlaps relation, NativelyWitnessed
                                -- predicate, NativeOverlapCertifiedFamily
                                -- ReadyAt + .of_member + refinements.
    `RA_MotifNativeCertificateComponents, -- (May 5 2026) v1.0 component
                                -- anchoring: 7-component Type-valued
                                -- witness contexts, packaging into native
                                -- overlap, refinement to independent
                                -- certified-family readiness, future_mono.
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
