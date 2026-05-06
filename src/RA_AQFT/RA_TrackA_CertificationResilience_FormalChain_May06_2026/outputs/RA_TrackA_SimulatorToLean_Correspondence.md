# Simulator → Lean correspondence (Track A)

This document maps each robust positive simulator finding to its Lean qualitative support surface (where one exists) or marks it as **simulator-only**.

The pattern: simulator findings are **numerical**; Lean entries are **structural** vocabulary the numerical findings can be cited within. Lean does not derive any of the numbers; it provides the type-valued frame in which they live.

## Convention

Each row labels:

- **Simulator finding** — the empirical observation, with its controlling claim ID.
- **Lean qualitative support** — the structural Type-valued counterpart, or "simulator-only" if no Lean counterpart exists.
- **Discipline note** — what Lean does NOT assert about this finding.

## Severance signatures (v0.5.x)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| Saturating-loss / strict-channel / graded-delay severance classification holds at 100-seed scale (`RA-SIM-SEVERANCE-SIGNATURE-001..005`) | **simulator-only** | Severance modes are simulator-side names; no Lean module formalizes mode-specific structure. |

## Channel separation (v0.6)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| 100-seed v0.6 channel-resolved separation: frontier_dropout vs ledger_failure distance=1.726, cosine=0.484 (`RA-SIM-SEVERANCE-CHANNEL-001..004`) | **simulator-only** | Channel-distance metrics are simulator-side; no Lean structure expresses inter-channel distance. |

## Support-family rescue (v0.7)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| Threshold-controlled support-family rescue: 30-56% rescue for reachability/availability disruption; 0% for ledger/orientation; selector_stress=0 (`RA-SIM-SUPPORT-FAMILY-001..003`) | `RA-MOTIF-SUPPORT-FAMILY-001` formal bridge (upstream of Track A) | Lean has no rescue-rate formula. |

## Support-family monotonicity (v0.7.1)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| `at_least_k` and `augmented_exact_k` give 0 monotonicity violations on 1.7M-eval run; `exact_k` gives 9,887 violations (10.3% of `cut_level × ledger/orientation` cohort) (`RA-SIM-SUPPORT-FAMILY-MONO-001..003`) | `RA-MOTIF-SUPPORT-FAMILY-MONO-001` formal bridge (upstream of Track A) | Lean has the qualitative inclusion / monotonicity structure but does not derive the 9,887 violation count or the 10.3% rate. Track A.2 would lift the cohort-specific no-violation statement to a Type-valued statement. |

## Support-family metric repair (v0.7.2)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| `comparison_valid_rate=0.982`; mean apples-to-apples loss delta -0.049 (family helps 5%); strict_rescue undercounts family resilience by ~2.76× (`RA-SIM-SUPPORT-FAMILY-METRIC-001..004`) | `DAGStrictParentRescueAt` vs `DAGFamilyInternalResilienceAt` separation in **Track A Layer 1** (`RA-MOTIF-CERT-RESILIENCE-CONSOL-001`) | The 2.76× factor is simulator-only. The Lean module formalizes the **categorical** distinction between strict rescue and family-internal resilience; that the latter is a strict superset is implicit in the refinement chain `to_family_internal_resilience`. |

## Certification-family rescue (v0.8)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| 4M-evaluation: parent_shared rescue=0; independent_member rescue positive in cert modes; cert rescue declines monotonically with correlation 0→1 (`RA-SIM-CERT-FAMILY-001..003`) | `DAGFamilyInternalResilienceAt` (Track A Layer 1) + `DAGCertificateFateContext` (Track A Layer 2) | Lean has the existential/structural shape (some independently certified family member ready). Numerical decay 0.221 → 0.176 → 0.121 → 0.091 → 0.000 is simulator-only. |

## Certificate-correlation decay (v0.8.1)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| 64 correlation decay curves; 61/64 strictly non-increasing; rescue → 0 at correlation=1.0 universal; aggregate AUC 0.044-0.050 (`RA-SIM-CERT-CORRELATION-001..004`) | `DAGSharedFateFamily.cert_equiv` and `DAGSharedFateFamily.certifies_iff_parent` (Track A Layer 2) at the qualitative endpoint | Lean does not derive monotone decay or AUC values. The `certifies_iff_parent` theorem is the **endpoint** structural counterpart of "rescue → 0 at correlation=1.0": when certificate fate is fully shared, certification status collapses to the parent member's, which formally captures the "no independent member to rescue from" structural condition. |

## Native overlap (v0.9 / v0.9.1 / v0.9.2)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| Native overlap induces certification rescue with low/medium/high binning: 0.218 → 0.138 → 0.001 for `ledger_failure / augmented_exact_k` (`RA-SIM-NATIVE-CERT-OVERLAP-001..002`) | `DAGNativeOverlapFateBridge` (Track A Layer 3) with `coupled_of_nativeOverlap` and `memberDistinct_of_lowOverlap` | Lean does not encode the numerical 0.218 → 0.138 → 0.001 trend or any monotonicity theorem on it. The bridge expresses **structurally** that low-overlap evidence supports member-distinct fates and high-overlap evidence supports coupling; the empirical decay sits at the simulator level. |
| Weight-profile robustness: ablation_monotone_pass_rate=1.0; balanced gap mean 0.058 (`RA-SIM-NATIVE-CERT-ROBUST-001..002`) | **simulator-only** | Weight-sensitivity audit is simulator-side machinery; no Lean module formalizes weight-profile robustness. |
| External-correlation calibration: `close_rate_match` / `qualitative_rate_match` / `steeper_or_uncalibrated` regimes (`RA-SIM-NATIVE-CERT-CALIB-001..002`) | **simulator-only** | Calibration regime classification has no Lean counterpart. |

## Native overlap component anchoring (v1.0)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| Component-anchored proxy with explicit honest caveat that orientation, support, and frontier overlap components coincide numerically (`RA-SIM-NATIVE-CERT-ANCHOR-001`) | `DAGNativeCertificateOverlapContext` and the `RA_MotifNativeCertificateComponents` Type-valued component context (upstream of Track A Layer 3) | Lean encodes the **component vocabulary** and the refinement chain into native overlap. The numerical mean values 0.857 / 0.839 (ledger) and 0.742 / 0.710 (the support/frontier/orientation triplet) are simulator-only. |

## Component decoupling audit (v1.1)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| `orientation_confounded_with_support_frontier` verdict at the component level (`RA-SIM-NATIVE-COMPONENT-DECOUPLE-001..002`) | **simulator-only** | This is a negative diagnostic by the audit machinery itself; it does not have a Lean counterpart and does not need one. The `RA-SIM-NATIVE-COMPONENT-DECOUPLE-METHOD-001` framing entry holds the methodological discipline. |

## Matched-graph extraction methodology (v1.6)

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| Rescue and orientation_overlap from the same v0.9 `CausalDAG` per trial (the v1.5 rescue/topology disconnection closed) (`RA-SIM-GRAPH-COUPLED-ORIENT-001`) | **simulator-only** (methodology) | The matched-graph extraction is a simulator-pipeline property; no Lean module asserts it. The empirical orientation-rescue numbers from this packet were later shown to be a binning artifact (see retracted-chain document); the methodology itself stands. |

## v1.7 + v1.8.1 retraction chain

| Simulator finding | Lean qualitative support | Discipline note |
|---|---|---|
| v1.5 +0.028 specificity / v1.6 reversed-sign gap / v1.7 keying ablation / v1.8 width-only / v1.8.1 joint matching all converge on **no orientation-specific signal under matched-graph extraction** (`RA-SIM-ORIENT-KEYING-001`, `RA-SIM-ORIENT-KEYING-002`, `RA-SIM-CONFOUND-V18-1-001`, `RA-SIM-CONFOUND-V18-1-PACKET-001`) | **explicitly excluded from Track A** | Per `RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001`. Track A introduces no orientation-specific Lean structure beyond the existing v1.0/v1.2/v1.3/v1.4/v1.5 qualitative bridges, which themselves never asserted orientation-specific rescue (only Type-valued refinement structure). |

## Lean qualitative bridges (motif-side, pre-Track A)

| Lean module | Track-A relation |
|---|---|
| `RA_MotifOrientationLinkSurface` (`RA-MOTIF-ORIENTATION-LINK-SURFACE-001`) | Upstream of Track A Layer 3; provides the Type-valued context within which orientation-link evidence can be expressed without numerical commitment. Track A does not extend this module. |
| `RA_MotifNativeOrientationLinkDerivation` (`RA-MOTIF-NATIVE-ORIENT-LINK-001`) | Upstream of Track A Layer 3; native-orientation catalog vocabulary. Track A does not extend it. |
| `RA_MotifPerGraphOrientationWitness` (`RA-MOTIF-PER-GRAPH-ORIENT-WITNESS-001`) | Upstream of Track A Layer 3; per-graph witness vocabulary. Track A does not extend it. |
| `RA_MotifConcreteGraphOrientationWitness` (`RA-MOTIF-CONCRETE-GRAPH-ORIENT-WITNESS-001`) | Upstream of Track A Layer 3; concrete-edge-pair-sign witness vocabulary. Track A does not extend it. |
| `RA_MotifCertifiedSupportFamilyBridge` (`RA-MOTIF-CERT-FAMILY-001`) | **Direct upstream of Track A Layer 1**. Provides `DAGFamilyCertificateContext` and `DAGIndependentCertifiedFamilyReadyAt` that Track A Layer 1 separates into strict-rescue vs family-internal-resilience. |
| `RA_MotifNativeCertificateOverlapBridge` (`RA-MOTIF-NATIVE-CERT-OVERLAP-001`) | **Direct upstream of Track A Layer 3**. Provides `DAGNativeCertificateOverlapContext.overlaps`, the relation Track A Layer 3 reads as evidence for certificate-fate coupling. |
| `RA_MotifNativeCertificateComponents` (`RA-MOTIF-NATIVE-CERT-COMPONENTS-001`) | **Direct upstream of Track A Layer 3**. Provides the v1.0 component-anchoring context. |

## Take-away

The Track A spine is a **pure structural refinement** of pre-existing Lean modules. It introduces no new mechanism, no probability, no calibration. What it adds is the **vocabulary** in which the v0.7..v0.9.x positive findings can be cited as instances of a Lean-typed concept rather than as standalone simulator observations. Numerical content lives in the simulator outputs and stays there.

For paper drafting: cite the simulator finding for **values**, cite the Track A Lean anchor for **structural correctness**, and cite this correspondence document for **the explicit separation between the two**.
