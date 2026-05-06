# Open formal gaps after the four-module Track A spine

This document lists what is **not** Lean-derived after Track A.2. It supersedes (in scope) the gap list in the earlier `RA_TrackA_CertificationResilience_FormalChain_May06_2026/outputs/RA_TrackA_OpenFormalGaps.md`, by the addition of Layer 4 (Track A.2 taxonomy). The earlier list is still correct for the items it covered; this document tracks the four-module state.

## What Track A.2 closed

Compared to the three-module gap list, the addition of `RA_MotifSupportFamilyRescueTaxonomy` closes:

- The augmentation vs replacement formal distinction (`FamilyStrictlyAugments` vs `FamilyIncomparable`).
- The certified-augmentation no-worse statement at the structural level (`FamilyInternalResilienceAt.mono_certified_augmentation`).
- The augmentation-rescue refinement into strict-parent rescue (`FamilyAugmentationRescueAt.to_strict_parent_rescue`).

These were "Track A.2" gaps in the earlier note; they are now formal theorems.

## What remains simulator-only (numerical content)

### Decay laws

- Certification rescue decreases monotonically as certificate correlation goes 0 → 1, reaching ~0 at correlation=1. 61/64 curves strictly non-increasing on the v0.8.1 4M-eval ensemble. Source: `RA-SIM-CERT-CORRELATION-001`..`-004`.
- Native-overlap rescue across low/medium/high bins: 0.218 → 0.138 → 0.001 for `ledger_failure / augmented_exact_k`. Source: `RA-SIM-NATIVE-CERT-OVERLAP-001`..`-002`.
- Native AUC vs external-correlation AUC: 0.079-0.105 vs 0.044-0.049. Source: `RA-SIM-NATIVE-CERT-ROBUST-002`.

Lean has only the structural endpoints (`DAGSharedFateFamily.certifies_iff_parent` for correlation=1; `DAGNativeOverlapFateBridge.sharedFate_of_highEndpoint` for high-overlap endpoint). The intermediate decay shape is not Lean-derived.

### Calibration coefficients

- `close_rate_match` / `qualitative_rate_match` / `steeper_or_uncalibrated_native_curve` regimes from `RA-SIM-NATIVE-CERT-CALIB-001`..`-002`.
- Mean external_calibration_residual_abs=0.046, max=0.129.

No Lean calibration mapping. Native bins are *structural* on the Lean side.

### Metric-repair coefficients

- The 2.76× ratio between `family_internal_resilience_events` (228,766) and `strict_rescues` (82,732) on the v0.7.2 100-seed run.
- `mean_valid_apples_to_apples_loss_delta = -0.049` (family loss is 5% lower than strict).

Lean encodes the categorical separation between strict and family-internal resilience (`DAGStrictParentRescueAt` vs `DAGFamilyInternalResilienceAt`). The factor-of-2.76 is simulator-only.

### Monotonicity-violation counts

- `at_least_k` and `augmented_exact_k`: 0 violations on 1.7M-eval v0.7.1 run.
- `exact_k` under `cut_level` certification: 9,887 violations (10.3% of cohort) entirely from `ledger_failure` (4,943) and `orientation_degradation` (4,944).

Lean has the categorical no-violation property in `RA_MotifSupportFamilyMonotonicity` (upstream of Track A) and now in Layer 4 the `FamilyStrictlyAugments` / `FamilyIncomparable` separation. The cohort-specific 9,887 violation count is not lifted. Future Track A.3 could lift it, but only if a paper section needs the specific cohort statement.

### Endpoint-equivalence partial result

- v0.8.1: 32/80 rows match `parent_shared` regime within strict 1e-9 tolerance; max delta 0.116.

`DAGSharedFateFamily.certifies_iff_parent` formalizes the structural endpoint. Numerical endpoint equivalence (whether observed rescue rates exactly match `parent_shared`) is partial under strict tolerance and is not promoted in the registry as full equivalence.

### AUC, rescue rates, residual standard deviations

Any AUC, rescue rate, or residual std in the registry is simulator-only. Lean has none of them.

## Unbridged simulator findings

These have **no** Lean counterpart and are unlikely to acquire one without a dedicated Track:

- Severance signature classifications (`RA-SIM-SEVERANCE-SIGNATURE-001..005`) — saturating-loss / strict-channel / graded-delay severance modes.
- Channel-resolved severance separation distances (`RA-SIM-SEVERANCE-CHANNEL-001..004`).
- Weight-profile robustness audit (`RA-SIM-NATIVE-CERT-ROBUST-001..002`).
- v0.9.2 family-semantics asymmetry (augmented_exact_k vs at_least_k strong-signal asymmetry).
- v1.0 component-anchoring numerical coincidence (orientation = support = frontier at 0.742 / 0.710).
- v1.1 component decoupling audit verdict (`orientation_confounded_with_support_frontier`).

## Excluded by discipline

- Orientation-specific certification rescue. Excluded per `RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001` until a future native per-graph witness extractor satisfies the six requirements in `docs/.../v1_9_*/outputs/ra_open_native_witness_requirements_v1_9.md`.
- Probability laws, loss-rate formulas. Excluded as a matter of discipline; the Lean side has no measure-theoretic apparatus on family resilience events.

## Candidate next formal targets

Listed in order of how immediately they support a paper section:

1. **Track A.3: Comparison-domain validity predicate.** Formalize the apples-to-apples condition: `ValidFamilyComparison`, `ValidRescueComparison`, `SameTargetingDomain`, `CertificatePreservationDomain`, `ComparableSupportFamilies`. This would give the v0.7.2 `comparison_valid_rate=0.982` simulator-side acceptance criterion a Lean-typed predicate. Useful only if a specific paper section needs it.

2. **Track A.4 (speculative): Cohort-specific monotonicity violation lift.** Formalize the 9,887-violation pattern at the cohort level. Requires encoding the certification regime distinction (cut_level vs parent_shared) on the Lean side as a separate field, then proving that exact_k under cut_level admits structural counterexamples in the certification-channel cohort. High effort, low marginal gain unless the paper specifically argues from this cohort.

3. **Track B (deferred): Native per-graph witness extraction.** Closed by `RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001` until the v1.9 native-witness gate is satisfied.

The recommendation in `RA_TrackA_FormalResilienceChain.md` is to **stop formal expansion here and write the technical paper section**. Track A.3 / A.4 / B are right only if a specific paper section requires them.
