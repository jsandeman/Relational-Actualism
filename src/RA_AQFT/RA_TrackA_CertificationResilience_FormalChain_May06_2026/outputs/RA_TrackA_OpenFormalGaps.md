# Open formal gaps after Track A

This document lists what is **not** Lean-derived in the Track A chain. It is meant to prevent over-reading the Track A formalization: every entry below is a place where the simulator chain has empirical content but the Lean side stops short.

## Numerical content not in Lean

The following are simulator observations only. Lean has either no counterpart, or only a structural-vocabulary counterpart that does not derive the number.

### Decay laws

- The monotone decline of certification rescue with certificate correlation: rescue rate goes from ~0.221 at correlation=0 to ~0.000 at correlation=1 across `ledger / at_least_k / sev=0.5 / thr=0.25` (and similar cohorts). 61/64 curves strictly non-increasing. Source: `RA-SIM-CERT-CORRELATION-001`..`-004`.
- Native-overlap rescue across low/medium/high bins: 0.218 → 0.138 → 0.001 for `ledger_failure / augmented_exact_k`. Source: `RA-SIM-NATIVE-CERT-OVERLAP-001`..`-002`.
- Native AUC vs external-correlation AUC: 0.079-0.105 vs 0.044-0.049 (native curves uniformly steeper). Source: `RA-SIM-NATIVE-CERT-ROBUST-002`.

Lean has no theorem that asserts any of these decay shapes.

### Calibration coefficients

- The mapping `close_rate_match` / `qualitative_rate_match` / `steeper_or_uncalibrated_native_curve` regimes between native-overlap bins and external correlation values. Source: `RA-SIM-NATIVE-CERT-CALIB-001`..`-002`.
- Mean external_calibration_residual_abs=0.046, max=0.129 across the 10-row calibration table.

Lean has no calibration mapping at all. The native bins remain *structural* on the Lean side; their numerical equivalents to external correlation values are simulator-only.

### Metric-repair coefficients

- The 2.76× ratio between `family_internal_resilience_events` (228,766) and `strict_rescues` (82,732) on the v0.7.2 100-seed run. Source: `RA-SIM-SUPPORT-FAMILY-METRIC-001`..`-004`.
- `mean_valid_apples_to_apples_loss_delta = -0.049` (family loss is 5% lower than strict when comparison is valid).

Lean only encodes the categorical separation between the two notions. The factor is simulator-only.

### Monotonicity-violation counts

- `at_least_k` and `augmented_exact_k`: 0 violations on the 1,728,000-eval v0.7.1 run.
- `exact_k` under `cut_level` certification: 9,887 violations entirely from `ledger_failure` (4,943) and `orientation_degradation` (4,944), violation_rate 0.103 each.

Lean's `RA_MotifSupportFamilyMonotonicity` asserts the categorical no-violation property, but does NOT derive the cohort-specific violation rate of `exact_k` × `cut_level` × certification-channel modes. Track A.2 (a follow-on Lean target proposed in `RA_TrackA_CertificationResilience_FormalChain.md`) would lift this cohort-specific structure.

### AUC, rescue rates, residual standard deviations

Any AUC value, rescue rate, or residual standard deviation in the registry is simulator-only. Lean has none of them.

## Endpoint-equivalence partial result

- v0.8.1 endpoint-equivalence audit: 32/80 rows match the parent_shared regime within strict 1e-9 tolerance; max delta 0.116. Source: `RA-SIM-CERT-CORRELATION-001`.

The Lean counterpart `DAGSharedFateFamily.certifies_iff_parent` formalizes the **structural** endpoint (when fate is fully shared, certification status collapses to parent). The numerical endpoint equivalence (whether observed rescue rates exactly match the parent_shared regime) is a simulator-side empirical question; it is partial under strict tolerance and the full equivalence claim is not promoted in the registry.

## Unbridged simulator findings

These have **no** Lean counterpart and likely will not unless an additional Lean target is built:

- Severance signature classifications (`RA-SIM-SEVERANCE-SIGNATURE-001..005`) — saturating-loss / strict-channel / graded-delay severance modes are simulator-side names with no Lean structural representation.
- Channel-resolved severance separation distances (`RA-SIM-SEVERANCE-CHANNEL-001..004`).
- Weight-profile robustness audit (`RA-SIM-NATIVE-CERT-ROBUST-001..002`) — the audit machinery itself is simulator-side.
- v0.9.2 family-semantics asymmetry (augmented_exact_k carries strong rescue signal vs at_least_k). This is a v0.9-internal finding; v1.x did not cross-validate it (the orientation-overlap chain failed to provide the cross-validation), so it lives at the simulator level.
- v1.0 component-anchoring honest caveat: orientation, support, and frontier overlap components coincide numerically (`mean=0.742 / 0.710`). Lean has the component vocabulary (`RA_MotifNativeCertificateComponents`); the numerical coincidence is simulator-only.
- v1.1 component decoupling audit verdict (`orientation_confounded_with_support_frontier`) — diagnostic-only, no Lean target.

## Excluded by discipline

These are deliberately **not** added to Track A even though Lean structures could in principle express them:

- Orientation-specific certification rescue. Excluded per `RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001` until a future native per-graph witness extractor satisfies the six requirements in `docs/.../v1_9_*/outputs/ra_open_native_witness_requirements_v1_9.md` (truly native witness extractor; within-stratum variation; shuffled control; partial-correlation control; canonical scale; member_idx fix re-applied).
- Probability laws over rescue events. Excluded as a matter of discipline: the simulator chain provides empirical rates, not derived probability distributions, and the Lean side has no measure-theoretic apparatus on `IndependentCertifiedFamilyReadyAt` family events.
- Loss-rate formulas. Excluded for the same reason.

## What a deeper formal target would look like

If a future packet wants to close one of the gaps above:

- **Track A.2** (support-family inclusion / rescue taxonomy refinement): lift the v0.7.1 cohort-specific monotonicity finding into a Type-valued statement that `at_least_k` and `augmented_exact_k` admit no `family_loss > strict_loss` instance, with `exact_k` admitting structural counterexamples in the `cut_level × certification-channel` cohort. This is the most adjacent Lean target.
- **Track B** (native per-graph witness extractor — closed by `RA-MOTIF-CERT-RESILIENCE-CONSOL-METHOD-001` until the six v1.9 requirements are satisfied): would also require a new simulator audit cycle.
- **Calibration formal target**: not currently feasible — the calibration is between RA-internal native-overlap bins and an externally-imposed correlation parameter; both sides exist in Lean only as Type-valued evidence with no numerical interpretation.
- **Decay theorem**: the right Lean-side approach would be to express monotonicity of `IndependentCertifiedFamilyReadyAt` under a structural ordering on `Ξ.certifies` strictness rather than under a numerical correlation parameter. This is a nontrivial formal-target design step and not currently on the recommended roadmap.

The recommendation in `RA_TrackA_CertificationResilience_FormalChain.md` § "Next safe targets" is to **stop formal expansion** here and write the technical paper section. Track A.2 is justified only if a specific paper section needs the sharper monotonicity formalization to ground a citation.
