# Confirmed resilience signatures (v0.5.x .. v1.8.1)

This document collects the **robust positive findings** from the simulator chain. Each entry cites the controlling claim ID(s) and the canonical run scale. These are findings that survived all subsequent audits in the chain.

## Severance and channel separation (v0.5.x — v0.6)

### v0.5.1: severance signature classifications hold at 100-seed scale
- **Claims**: `RA-SIM-SEVERANCE-SIGNATURE-001`..`-005`.
- Saturating-loss modes (`edge_dropout`, `frontier_dropout`, `ledger_failure`, `orientation_degradation`), strict-channel mode (`selector_stress`), and graded-delay mode (`support_delay`) classify cleanly.
- Separability tightens vs v0.5.0: edge_dropout vs frontier-cluster Euclidean distance 3.14 → 6.31; cosine 0.78 → 0.52.
- The frontier_dropout / ledger_failure / orientation_degradation trio remains nearly-degenerate (cosine=1, distance=0) -- structural, not sampling artifact.
- Caveat: only `support_width=1` in this ensemble; width-stratified fragility is not generalizable from v0.5.x alone.

### v0.6: width-stratified channel separation at 100-seed scale
- **Claims**: `RA-SIM-SEVERANCE-CHANNEL-001`..`-004`.
- Run: 72,000 evaluations in 272s; `support_width_classes=[1,2,3,4]`.
- Channel separation confirmed: frontier_dropout vs ledger_failure distance=1.726, cosine=0.484 (was 0/1 in v0.5.2); ledger_failure vs orientation_degradation distance=0.832, cosine=0.734.
- Width-stratified fragility curves emerge: edge_dropout 0.72 → 0.97 as width 1→4 at severity 0.5.

## Support-family rescue (v0.7 — v0.7.2)

### v0.7: threshold-controlled support-family rescue
- **Claims**: `RA-SIM-SUPPORT-FAMILY-001`..`-003`.
- Run: 288,000 evaluations across 4 thresholds in 19.3s.
- All five README success criteria reproduce: threshold=1.0 family-loss = strict-loss; threshold<1.0 rescues 30-56% of strict losses for reachability/availability disruption; rescue rates differ sharply by mode (edge_dropout 30-44%, frontier_dropout up to 56%, ledger_failure / orientation_degradation 0%); selector_stress=0 across all thresholds; resilience appears only where the failure channel is reachability/availability-local.

### v0.7.1: monotone family semantics give zero violations
- **Claims**: `RA-SIM-SUPPORT-FAMILY-MONO-001`..`-003`.
- Run: 1,728,000 evaluations in 104.4s.
- `at_least_k` and `augmented_exact_k` both produce 0 monotonicity violations under cut_level and parent_shared certification.
- `exact_k` produces 9,887 violations (10.3% of cohort), all in ledger_failure / orientation_degradation under cut_level certification. This identifies `exact_k` as a non-monotone variant; the disciplined choice for downstream audits is `at_least_k` and `augmented_exact_k`.

### v0.7.2: metric-repair discipline holds at 100-seed scale
- **Claims**: `RA-SIM-SUPPORT-FAMILY-METRIC-001`..`-004`.
- Run: 1,728,000 evaluations.
- comparison_valid_rate=0.982; metric_artifact_risk_rate=0.0145.
- `mean_valid_apples_to_apples_loss_delta = -0.049` -- when comparison is valid, family loss is on average 5% LOWER than strict.
- `family_internal_resilience_events = 228,766` vs `strict_rescues = 82,732` -- the v0.7 strict_rescue metric undercounts family resilience by ~2.76×.

## Certification-family rescue and correlation (v0.8 — v0.8.1)

### v0.8: 4M-evaluation certified-support-family rescue
- **Claims**: `RA-SIM-CERT-FAMILY-001`..`-003`.
- Run: 4,032,000 evaluations in 235.6s (17,114 eval/s).
- comparison_valid_rate=1.0; metric_artifact_risk_events=0.
- Counts: certification_rescues=129,249; family_certification_resilience_events=778,581; strict_rescues=192,567.
- Five README criteria reproduce: parent_shared rescue=0; independent_member rescue positive in cert modes; cert rescue declines monotonically with correlation 0.0→1.0 (e.g. ledger / at_least_k / sev=0.5 / thr=0.25: 0.221 → 0.176 → 0.121 → 0.091 → 0.000); selector_guardrail_passed across all selector_stress rows; support-route resilience and certification-witness resilience remain distinct diagnostics.

### v0.8.1: certification rescue → 0 at correlation=1.0 is universal
- **Claims**: `RA-SIM-CERT-CORRELATION-001`..`-004`.
- Run: 4,032,000-evaluation v0.8 ensemble re-analyzed; 64 correlation decay curves.
- 61/64 strictly non-increasing; the 3 deviations (all in orientation_degradation) are finite-sample (max step-increase 0.0146; all reach zero at correlation=1.0).
- Endpoint cert-rescue → 0 at correlation=1.0 is universal in the data.
- Aggregate AUC ~0.044-0.050 across both monotone family semantics.
- Highest decay curves: orientation_degradation / at_least_k / sev=0.75 / thr=0.25 (0.319 → 0); ledger_failure / at_least_k / sev=0.75 / thr=0.25 (0.313 → 0).

## Native-overlap signature (v0.9 — v0.9.2)

### v0.9: native overlap induces certification rescue with overlap-sensitivity
- **Claims**: `RA-SIM-NATIVE-CERT-OVERLAP-001`..`-002`.
- Run: 100-seed v0.9.
- Overlap-induced rescue curves are monotone non-increasing across populated bins: ledger_failure / augmented_exact_k 0.218 → 0.138 → 0.001 (low_minus_high 0.218); orientation_degradation / augmented_exact_k 0.215 → 0.138 → 0.001 (low_minus_high 0.214). `at_least_k` produces only medium/high bins at this run scale.
- Parent-shared baseline: 0 certification rescue across the entire comparison.
- selector_stress remains outside support/certification-family rescue.

### v0.9.1: weight-profile robustness
- **Claims**: `RA-SIM-NATIVE-CERT-ROBUST-001`..`-002`.
- weight_sensitivity_rows=36; ablation_monotone_pass_rate=1.0; balanced_low_high_gap_mean=0.058.
- Endpoint separation from parent_shared: rescue max delta 0.5; resilience max delta 0.667.
- Caveat: weight profiles are diagnostic; no profile is the derived RA-native overlap law.

### v0.9.2: external-correlation calibration mapping
- **Claims**: `RA-SIM-NATIVE-CERT-CALIB-001`..`-002`.
- Calibration regime breakdown: 4 cells `close_rate_match` (high-overlap bins; native rescue ~0.0007 vs corr=1.0 endpoint); 4 cells `qualitative_rate_match` (medium bins; residual 0.043-0.060); 2 cells `steeper_or_uncalibrated_native_curve` (augmented_exact_k low bins; residuals 0.120 / 0.129).
- All AUC and decay deltas are positive: native curves are uniformly steeper than the external-correlation baseline.
- Caveat: native bins are structural, not numerical equivalents of external correlation values; absolute calibration is not yet established. Family-semantics asymmetry is v0.9-internal and is NOT cross-validated by v1.x (see retracted-chain document).

## Component anchoring (v1.0)

### v1.0: native-overlap proxy with explicit component-attribution caveat
- **Claim**: `RA-SIM-NATIVE-CERT-ANCHOR-001`.
- Run: 480 component rows, 10 native overlap profiles, 3 bins (low/medium/high).
- ledger separates cleanly for ledger_failure (highest-mean component 0.857 / 0.839 across semantics).
- **Honest caveat baked into v1.0 itself**: orientation, support, and frontier overlap components coincide numerically (mean 0.742 / 0.710). v1.0 records this faithfully; it claims a component-anchored proxy exists but does NOT claim orientation_degradation is specifically controlled by an independently measured orientation surface.

## Audit machinery (v1.1)

### v1.1: orientation/support/frontier confounding detected (negative result that the audit should produce)
- **Claims**: `RA-SIM-NATIVE-COMPONENT-DECOUPLE-001`..`-002`.
- Run: 480 v1.0 component rows.
- Triplet decoupling status: `orientation_confounded_with_support_frontier` (max_abs_diff=0.0 across all three pairwise comparisons; ablation residual=0.0 in all six (mode, semantics) cells).
- Ledger overlap is decoupled (max_abs_diff 0.383); orientation is confounded.
- selector_stress correctly classifies as `not_certification_channel`.
- The audit functions as designed by refusing to manufacture a component-specific signal where the surface does not exist.

## Matched-graph extraction methodology (v1.6 + v1.7)

### v1.6: rescue and orientation_overlap from the same v0.9 CausalDAG per trial
- **Claim**: `RA-SIM-GRAPH-COUPLED-ORIENT-001` (the methodology, not the empirical reading).
- Closes the v1.5 rescue/topology disconnection: rescue and orientation overlap are now extracted from the same `CausalDAG` instance per trial, not from a parallel synthetic corpus via deterministic-hash mapping.
- decoupled_count=12/12; selector_guardrail_passed=true; v1_6_disconnection_closed=true.
- The empirical orientation-rescue reading from this packet was later shown to be a binning artifact (see retracted-chain document); the matched-graph extraction methodology itself stands.

### v1.7: keying-ablation canonical sweep on matched graphs
- **Claims**: `RA-SIM-ORIENT-KEYING-001`..`-002`, `RA-SIM-ORIENT-KEYING-METHOD-001`.
- Run: 194,400 base trials × 6 keyings = 1,166,400 keyed rows; 36 cells per (keying, mode, semantics).
- selector_guardrail_passed=true; any_positive_non_member_orientation_specificity=false.
- The ablation canonically retracts the v1.5 +0.028 specificity gap; the framing entry `RA-SIM-ORIENT-KEYING-METHOD-001` becomes the standard discipline for any future orientation-overlap rescue audit.

## Joint-confound discipline (v1.8 + v1.8.1)

### v1.8.1: joint width × family-size matching closes the orientation-overlap audit
- **Claims**: `RA-SIM-CONFOUND-V18-1-001` (Case A under within-stratum re-binning), `RA-SIM-CONFOUND-V18-1-PACKET-001` (Case C under cell-level binning), `RA-SIM-CONFOUND-METHOD-001` (the methodological guardrail).
- Within-stratum re-binning: gap collapses to |0.003|; graph keyings match shuffled control to within 0.005.
- Cell-level binning + estimability check: estimable_joint_group_fraction_graph=0.0 -- orientation_overlap is nearly a deterministic function of (support_width, family_size) at cell level.
- Both readings converge on no orientation-specific signal under matched-graph extraction. The packet's reading is the methodologically conservative formulation.
- This closes the v1.x orientation-overlap audit.

## Lean qualitative bridges

The following Lean modules are lake-build-confirmed (no sorry/admit/axiom) and contribute qualitative refinement structure (Type-valued evidence + refines-morphisms into the next-coarser layer). They do NOT assert numerical orientation-rescue laws or probabilities.

- `RA_MotifOrientationLinkSurface` (claim `RA-MOTIF-ORIENTATION-LINK-SURFACE-001`)
- `RA_MotifNativeOrientationLinkDerivation` (claim `RA-MOTIF-NATIVE-ORIENT-LINK-001`)
- `RA_MotifPerGraphOrientationWitness` (claim `RA-MOTIF-PER-GRAPH-ORIENT-WITNESS-001`)
- `RA_MotifConcreteGraphOrientationWitness` (claim `RA-MOTIF-CONCRETE-GRAPH-ORIENT-WITNESS-001`)

These bridges express what a qualitative refinement chain from a concrete edge-pair-sign witness up to a v1.0 component context could look like; the formal anchor is `Type`-valued and `Prop`-placeholder, not a probability law.

## What this list IS NOT

- It is **not** a list of orientation-specific rescue findings. The orientation-specific rescue interpretation is retracted (see `ra_retracted_orientation_specificity_chain_v1_9.md`).
- It is **not** a list of Nature predictions. These are RA-internal simulator signatures and methodological discipline; promotion to a Nature-target requires a separate empirical bridge that the simulator chain has not yet provided.
