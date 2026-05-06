# RA Track A Certification Resilience Formal Chain

**Date**: 2026-05-06.
**Anchor**: `RA-MOTIF-TRACKA-FORMAL-CHAIN-METHOD-001`.
**Status**: synthesis-only; the three Lean modules below are individually lake-build-confirmed (no sorry/admit/axiom).

This document narrates the compile-confirmed Track A spine and explains what it formalizes vs what it leaves to the simulator.

## The chain

Three Lean modules, layered:

```
RA_MotifCertifiedSupportFamilyBridge        ← upstream foundation
        │
        ▼
RA_MotifCertificationResilienceConsolidation
        │   (RA-MOTIF-CERT-RESILIENCE-CONSOL-001)
        │   StrictParentRescueAt /
        │   FamilyInternalResilienceAt
        ▼
RA_MotifCertificateCorrelationBridge
        │   (RA-MOTIF-CERT-CORRELATION-BRIDGE-001)
        │   CertificateFateContext
        │   (coupled / shared-fate / member-distinct / weakly shared)
        ▼
RA_MotifNativeOverlapCorrelationBridge
        │   (RA-MOTIF-NATIVE-OVERLAP-CORRELATION-BRIDGE-001)
        │   NativeOverlapFateBridge
        │   sharedFate_of_highEndpoint
        ▼
   Refines into upstream layers:
      certified-family readiness ← family-internal resilience
      family readiness ← certified-family readiness
```

Each layer adds vocabulary; none asserts a numerical law.

## What each module formalizes

### Layer 1: `RA_MotifCertificationResilienceConsolidation`

Separates two notions that the simulator chain treated as distinct (per the v0.7.2 metric repair, `RA-SIM-SUPPORT-FAMILY-METRIC-001`) but that prior Lean modules conflated:

```
DAGStrictParentRescueAt G Γ M F Ξ Qparent x
  := F.cuts Qparent ∧ ¬DAGReadyAt G Qparent x
     ∧ DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x

DAGFamilyInternalResilienceAt G Γ M F Ξ x
  := DAGIndependentCertifiedFamilyReadyAt G Γ M F Ξ x
```

Plus the chain of refinement theorems (`.to_family_internal_resilience`, `.parent_not_ready`, `.to_certified_family_ready`, `.to_family_ready`, and `.future_mono` along DAG precedence / Graph reachability). Graph counterparts of all of the above.

The structural payoff: any layer downstream that asserts strict-parent rescue automatically refines into family readiness, certified-family readiness, and family-internal resilience. The metric-repair distinction lives in Lean as a Type-valued separation rather than as a simulator-side accounting note.

### Layer 2: `RA_MotifCertificateCorrelationBridge`

Introduces qualitative certificate-fate vocabulary:

```
DAGCertificateFateContext   -- coupled relation + reflexivity / symmetry / cert_equiv_of_coupled
DAGSharedFateFamily         -- ∀ Q Q' ∈ F, coupled Q Q'
DAGMemberDistinctFates      -- Ξ.member_distinct ∧ ∃ Q₁ Q₂ certified, ¬coupled
DAGWeaklySharedFates        -- qualitative middle-range marker
DAGCertificateSharingPreorder -- placeholder for future qualitative ordering
```

Plus refinement theorems:
- `DAGSharedFateFamily.cert_equiv` — any two family members have equivalent certification status under shared fate.
- `DAGSharedFateFamily.certifies_iff_parent` — shared-fate collapses every member to the parent.
- `DAGMemberDistinctFates.member_distinct_marker` — exposes the underlying `Ξ.member_distinct` flag.
- `DAGMemberDistinctCertificateResilienceAt` and `DAGSharedFateResilienceAt` with their `.to_family_internal_resilience` / `.to_certified_family_ready` / `.future_mono` cascade. Graph counterparts of all.

This layer does NOT encode the v0.8.1 simulator-side decay (rescue rate monotone non-increasing as certificate correlation goes 0→1, reaching 0 at correlation=1). That decay is the simulator's empirical observation; Lean only formalizes the **vocabulary** (shared-fate vs member-distinct) within which such an observation could be expressed.

### Layer 3: `RA_MotifNativeOverlapCorrelationBridge`

Connects native-overlap evidence (from `RA_MotifNativeCertificateOverlapBridge.DAGNativeCertificateOverlapContext.overlaps`) to the certificate-fate vocabulary of Layer 2:

```
DAGNativeOverlapFateBridge (Ω) (Φ)   -- structure carrying:
  lowOverlapWitness : Prop
  memberDistinct_of_lowOverlap : lowOverlapWitness → DAGMemberDistinctFates Ξ Φ
  coupled_of_nativeOverlap : Ω.overlaps Q Q' → Φ.coupled Q Q'

DAGHighNativeOverlapEndpoint (Ω) := ∀ Q Q' ∈ F, Ω.overlaps Q Q'
DAGLowNativeOverlapCertificateResilienceAt   -- low-overlap witness + family-internal resilience
DAGHighNativeOverlapSharedFateResilienceAt   -- high-overlap endpoint + family-internal resilience
```

The structural payoff theorem:

```
DAGNativeOverlapFateBridge.sharedFate_of_highEndpoint :
  DAGHighNativeOverlapEndpoint Ω → DAGSharedFateFamily Φ
```

This is the formal counterpart of the simulator-side intuition "high witness overlap behaves like shared certificate fate", expressed at the structural-vocabulary level only. The bridge is conservative: it requires a downstream construction of the `coupled_of_nativeOverlap` morphism, which is what would be supplied by a future native-witness extractor (per `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001` rules; the v1.x extractors did not satisfy the within-stratum-variation requirement, so they are not admissible upstream constructions for this bridge).

Plus refinement theorems:
- Low overlap → `DAGMemberDistinctCertificateResilienceAt` (member-distinct branch).
- Low overlap → family-internal resilience → certified-family readiness, future-monotone.
- High overlap (via `sharedFate_of_highEndpoint`) → `DAGSharedFateResilienceAt`, certified-family readiness.

Graph counterparts of all.

## Theorem surface that is NOT in Lean

The following remain **simulator-supported only** (see `RA_TrackA_OpenFormalGaps.md` for details):

- The numerical monotone decay: rescue rate decreases as certificate correlation goes 0 → 1, reaching exactly 0 at correlation = 1 (`RA-SIM-CERT-CORRELATION-001`..`-004`).
- The numerical native-overlap signature: e.g. `ledger_failure / augmented_exact_k` rescue 0.218 → 0.138 → 0.001 across low/medium/high overlap bins (`RA-SIM-NATIVE-CERT-OVERLAP-001`).
- The factor-of-2.76× metric undercount of strict_rescue vs family_internal_resilience (`RA-SIM-SUPPORT-FAMILY-METRIC-001`..`-004`).
- The 4M-evaluation parent_shared baseline reading (zero certification rescue across the entire comparison).
- The external-correlation calibration (native AUC 0.079-0.105 vs external 0.044-0.049; native curves uniformly steeper).
- The selector_stress guardrail (zero certification rescue across all selector_stress rows at every scale).
- Any AUC, slope, residual_std, or calibration coefficient.

These are not Lean theorems. They are simulator observations; the Lean chain is the qualitative skeleton against which they can be cited, not the source of their truth.

## Dependency map

```
RA-MOTIF-NATIVE-OVERLAP-CORRELATION-BRIDGE-001
    ├─ proof_dep → RA-MOTIF-CERT-CORRELATION-BRIDGE-001
    ├─ proof_dep → RA-MOTIF-NATIVE-CERT-OVERLAP-001
    └─ proof_dep → RA-MOTIF-NATIVE-CERT-COMPONENTS-001

RA-MOTIF-CERT-CORRELATION-BRIDGE-001
    └─ proof_dep → RA-MOTIF-CERT-RESILIENCE-CONSOL-001

RA-MOTIF-CERT-RESILIENCE-CONSOL-001
    ├─ proof_dep → RA-MOTIF-SUPPORT-FAMILY-001
    ├─ proof_dep → RA-MOTIF-SUPPORT-FAMILY-MONO-001
    ├─ proof_dep → RA-MOTIF-CERT-FAMILY-001
    └─ proof_dep → RA-SIM-SUPPORT-FAMILY-METRIC-001
```

The simulator-side `RA-SIM-SUPPORT-FAMILY-METRIC-001` is the only simulator-side `proof_dep` of the Track A spine — that's the v0.7.2 metric-repair finding that motivated the strict_rescue / family_internal_resilience separation. Everything else upstream is on the Lean side already.

## Build receipts

| Module | jobs | wall | sorry/admit/axiom |
|---|---|---|---|
| `RA_MotifCertificationResilienceConsolidation` | 8275/8275 | ~81s | none |
| `RA_MotifCertificateCorrelationBridge` | 8276/8276 | ~87s | none |
| `RA_MotifNativeOverlapCorrelationBridge` | 8279/8279 | ~83s | none |

All three modules build clean against the active RA Lean tree (post the 2026-05-05 `chainScore` namespace fix in `RA_D1_NativeKernel`).

## Next safe targets

Two options on the table after this completion note:

- **Track A.2: support-family inclusion / rescue taxonomy refinement.** Lift the v0.7.1 monotonicity audit (`RA-SIM-SUPPORT-FAMILY-MONO-001`..`-003`) into a Type-valued statement that `at_least_k` and `augmented_exact_k` give a no-violation refinement of strict-parent loss, with `exact_k` admitting structural counterexamples in the `cut_level × certification-channel` cohort. This sharpens the metric-repair semantics already encoded.
- **Stop formal expansion and write the RA actualization-resilience technical paper.** The chain is now substantial enough to support a paper section on its own (motif → support-family → certification-family → native-overlap), and the v1.5..v1.8.1 retraction is documented in `RA_CausalDAG_MotifCommitSimulator_v1_9_CertificationResilienceSynthesis_May06_2026/`.

The technical synthesis (`RA_MotifActualizationResilience_TechnicalSynthesis_May06_2026/outputs/RA_MotifActualizationResilience_TechnicalNote_May06_2026.md` § 9) recommended Track A first and a paper second; with Track A landed, paper-writing is now the next productive move. Track A.2 is the right move only if a specific paper section needs the sharper monotonicity formalization before drafting.
