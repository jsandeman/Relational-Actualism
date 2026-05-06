# RA Track A Formal Resilience Chain (Compile-Confirmed)

**Date**: 2026-05-06.
**Anchor**: `RA-MOTIF-TRACKA-FORMAL-RESILIENCE-CHAIN-METHOD-001`.
**Status**: synthesis-only; the four Lean modules below are individually lake-build-confirmed (no sorry/admit/axiom).

This document narrates the four-module Track A spine as a single coherent formal chain. The chain is **structural**: it formalizes vocabulary and refinement morphisms; it does not derive numerical decay, calibration, or rescue-rate laws. Numerical content stays at the simulator level.

## The four-module spine

```
RA_MotifCertifiedSupportFamilyBridge        ← upstream foundation
RA_MotifSupportFamilyMonotonicity           ← upstream support-family inclusion
RA_MotifNativeCertificateOverlapBridge      ← upstream native-overlap context
RA_MotifNativeCertificateComponents         ← upstream component anchoring
        │
        ▼
Layer 1 — RA_MotifCertificationResilienceConsolidation
            (RA-MOTIF-CERT-RESILIENCE-CONSOL-001)
            StrictParentRescueAt vs FamilyInternalResilienceAt
        │
        ▼
Layer 2 — RA_MotifCertificateCorrelationBridge
            (RA-MOTIF-CERT-CORRELATION-BRIDGE-001)
            CertificateFateContext: shared / member-distinct / weakly-shared
        │
        ▼
Layer 3 — RA_MotifNativeOverlapCorrelationBridge
            (RA-MOTIF-NATIVE-OVERLAP-CORRELATION-BRIDGE-001)
            NativeOverlapFateBridge: high-overlap → shared-fate family
        │
        ▼
Layer 4 — RA_MotifSupportFamilyRescueTaxonomy
            (RA-MOTIF-SUPPORT-FAMILY-RESCUE-TAXONOMY-001)
            FamilyEquivalent / StrictlyAugments / Comparable / Incomparable
            CertifiedFamilyAugments + AugmentationRescueAt
```

Each layer is independently lake-build-confirmed and contributes a structural advance:

- **Layer 1 (Resilience consolidation)** introduces the categorical separation between strict-parent rescue and family-internal resilience that the v0.7.2 metric-repair audit established empirically. The two notions are no longer conflated as one "rescue" event; they have distinct Type-valued definitions and a refinement morphism `to_family_internal_resilience` from the strict to the family-internal variant.

- **Layer 2 (Certificate-correlation bridge)** lifts the v0.8.1 simulator-side certificate-correlation chain into a Lean vocabulary: `DAGCertificateFateContext` carries a `coupled` relation on family members with the only morphism the program actually uses (`cert_equiv_of_coupled`), and the shared-fate / member-distinct endpoints are typed as separate predicates. The `DAGSharedFateFamily.certifies_iff_parent` theorem encodes the structural endpoint of the v0.8.1 `rescue → 0 at correlation=1.0` empirical observation: when fate is fully shared, every member's certification status collapses to the parent's, so no independent member is available to rescue.

- **Layer 3 (Native-overlap correlation bridge)** wires the v1.0 native-overlap component context into Layer 2's certificate-fate vocabulary. The structural payoff theorem `DAGNativeOverlapFateBridge.sharedFate_of_highEndpoint` says: given a high-overlap endpoint (every pair of family members overlaps) plus the bridge's `coupled_of_nativeOverlap` morphism, the certificate-fate context is a shared-fate family. This is the formal counterpart of "high witness overlap behaves like shared certificate fate" without committing to a numerical monotone law.

- **Layer 4 (Support-family rescue taxonomy)** closes the v0.7 metric-repair circle by formalizing the augmentation vs replacement distinction. `FamilyStrictlyAugments` (one-way inclusion) is separated from `FamilyIncomparable` (replacement regime where no augmentation no-worse theorem is available from inclusion alone). `CertifiedFamilyAugments` adds certificate preservation to inclusion. The structural payoff theorems are `FamilyInternalResilienceAt.mono_certified_augmentation` (resilience preserved by certified augmentation) and `FamilyAugmentationRescueAt.to_strict_parent_rescue` (augmentation rescue refines into strict-parent rescue in the augmented family).

## Why the chain matters

The simulator-side empirical findings could in principle be cited individually, but doing so would re-introduce the v0.7-style ambiguity in which `exact_k` replacement behavior was occasionally read as additive redundancy. With the four Lean modules in place:

- The **augmentation vs replacement** distinction is now a Lean-typed predicate (`FamilyStrictlyAugments` vs `FamilyIncomparable`), not just a simulator-side accounting note. Citing `FamilyAugmentationRescueAt.to_strict_parent_rescue` makes "augmented family rescued the parent failure" a structured claim about a specific augmentation morphism rather than a loose narrative event.

- The **metric-repair distinction** between strict_rescue and family_internal_resilience is a Lean-typed refinement chain (`DAGStrictParentRescueAt → DAGFamilyInternalResilienceAt → DAGCertifiedFamilyReadyAt → DAGFamilyReadyAt`). Citing the chain is more precise than citing the v0.7.2 metric-repair audit alone.

- The **certificate-correlation endpoint** (rescue → 0 at correlation=1.0) has a structural counterpart (`DAGSharedFateFamily.certifies_iff_parent`) that future papers can cite without needing to reconstruct the numerical decay curve.

- The **native-overlap signature** (low-overlap families have higher rescue rates than high-overlap families) has a structural support surface (`DAGNativeOverlapFateBridge` with `memberDistinct_of_lowOverlap` and `sharedFate_of_highEndpoint`) that records the asymmetry without claiming a numerical trend.

This is the **conservative formalization pattern**: simulator findings motivate vocabulary; Lean only proves structural refinements; the gap between the two stays explicit.

## Theorem-surface summary

| Layer | Key structures | Key theorems | Status |
|---|---|---|---|
| 1 | `StrictParentRescueAt`, `FamilyInternalResilienceAt` | `to_family_internal_resilience`, `parent_not_ready`, `to_certified_family_ready`, `to_family_ready`, `future_mono` | lean_build_confirmed |
| 2 | `CertificateFateContext`, `SharedFateFamily`, `MemberDistinctFates`, `WeaklySharedFates` | `cert_equiv`, `certifies_iff_parent`, `member_distinct_marker`, plus `MemberDistinctCertificateResilienceAt.future_mono` | lean_build_confirmed |
| 3 | `NativeOverlapFateBridge`, `HighNativeOverlapEndpoint`, `LowNativeOverlapCertificateResilienceAt` | `sharedFate_of_highEndpoint`, refinements to member-distinct / shared-fate resilience, `future_mono` | lean_build_confirmed |
| 4 | `FamilyEquivalent`, `FamilyStrictlyAugments`, `FamilyComparable`, `FamilyIncomparable`, `CertifiedFamilyAugments`, `FamilyAugmentationRescueAt` | `mono_certified_augmentation`, `to_strict_parent_rescue`, `to_family_internal_resilience`, `to_certified_family_ready`, plus `FamilyEquivalent.refl` / `.symm` | lean_build_confirmed |

All four modules use the DAG / Graph parallel pair pattern; every DAG-side theorem has a Graph-side counterpart.

## What stays simulator-only

- Numerical decay laws (rescue rate vs certificate correlation; rescue rate vs native overlap).
- Calibration coefficients (native AUC vs external correlation AUC; close_rate_match / qualitative_rate_match / steeper regimes).
- Metric-repair coefficients (the 2.76× ratio between family_internal_resilience_events and strict_rescues; the 5% mean apples-to-apples loss delta).
- Monotonicity violation counts (9,887 violations of family_loss > strict_loss in the exact_k × cut_level × ledger/orientation cohort on the 1.7M-eval v0.7.1 run).
- All AUC, rescue rates, and residual standard deviations.

See `RA_TrackA_OpenFormalGaps.md` for the per-item list.

## Build receipts (compile-confirmed)

| Module | Jobs | Wall | Lex check |
|---|---|---|---|
| `RA_MotifCertificationResilienceConsolidation` | 8275/8275 | ~81s | clean |
| `RA_MotifCertificateCorrelationBridge` | 8276/8276 | ~87s | clean |
| `RA_MotifNativeOverlapCorrelationBridge` | 8279/8279 | ~83s | clean |
| `RA_MotifSupportFamilyRescueTaxonomy` | 8276/8276 | ~82s | clean |

Total: ~33,106 jobs over ~5.6 minutes wall-clock, all clean. See `RA_TrackA_CompileConfirmed_Report.md` for environment details.

## Recommended next step

**Stop formal expansion here and write the technical paper section.** Track A has reached a natural milestone: four modules, every robust-positive simulator lesson has a structural Lean counterpart, and the augmentation-rescue refinement closes the v0.7 metric-repair circle.

The next formal target, if a paper section requires it:

- **Track A.3: Comparison-domain validity predicate.** Formalize the apples-to-apples condition more directly via `ValidFamilyComparison`, `ValidRescueComparison`, `SameTargetingDomain`, `CertificatePreservationDomain`, `ComparableSupportFamilies`. This would give the v0.7.2 `comparison_valid_rate=0.982` simulator-side acceptance criterion a Lean-typed predicate. Useful only if a specific paper section needs it; otherwise defer.

The recommended path remains **paper-writing** before any new Lean target.
