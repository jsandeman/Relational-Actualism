# RA Causal-DAG Motif Commit Simulator v1.6 — Graph-Coupled Orientation-Link Extraction Report

Date: 2026-05-05.

## Purpose

v1.6 closes the rescue/topology disconnection identified as the central
honesty caveat of v1.5. v1.5 paired v0.9-derived rescue with orientation
overlaps from a parallel synthetic corpus; v1.6 imports the v0.9 simulator
directly and extracts both quantities from the same `CausalDAG` instance
per trial.

## Method

The v1.6 driver imports v0.9's `ChannelSeedState`, `build_channel_seed_state`,
`evaluate_native_overlap_certified_family`, `target_motifs_for_channel_severance`,
and `support_family_by_semantics`. It runs a constrained subset of v0.9's
parameter sweep (4 seeds × 1 severance × 3 modes × 1 severity × 1 threshold
× 2 semantics × 8 targets = 192 trials in ~30s wall-clock).

For each trial, the driver:

1. Calls `evaluate_native_overlap_certified_family(state, motif, site, ...)` →
   v0.9 trial row with `certification_rescue_event`, `support_overlap`,
   `frontier_overlap`, `orientation_overlap`, `ledger_overlap`.
2. Calls `support_family_by_semantics(motif, fraction, semantics)` to get
   the same `SupportCutFamily` v0.9 used for that trial.
3. On the same `state.dag`, computes
   `graph_coupled_orientation_link_overlap` as the mean pairwise Jaccard of
   edge-pair-sign witnesses across family members, where each member's
   witness is keyed by parent→child edges around the cut with sign =
   `(depth(p) + depth(v) + member_idx) mod 2`.

Rescue and orientation_overlap therefore come from the same `CausalDAG`
instance. The v1.5 hash-keyed cell-to-graph mapping is eliminated.

## Canonical results

### Decoupling audit (12 / 12 decoupled)

The graph-coupled orientation surface is decoupled from each of
{support, frontier, legacy_orientation, ledger}_overlap_mean across all
three modes:

| mode | comparison | max_abs_diff | mean_abs_diff |
|---|---|---|---|
| ledger_failure | vs support_overlap | 1.0 | 0.536 |
| ledger_failure | vs frontier_overlap | 1.0 | 0.536 |
| ledger_failure | vs legacy_orientation | 1.0 | 0.536 |
| ledger_failure | vs ledger_overlap | 1.0 | 0.743 |
| orientation_degradation | vs support_overlap | 1.0 | 0.536 |
| orientation_degradation | vs frontier_overlap | 1.0 | 0.536 |
| orientation_degradation | vs legacy_orientation | 1.0 | 0.536 |
| orientation_degradation | vs ledger_overlap | 1.0 | 0.743 |
| selector_stress | vs support_overlap | 1.0 | 0.536 |
| selector_stress | vs frontier_overlap | 1.0 | 0.536 |
| selector_stress | vs legacy_orientation | 1.0 | 0.536 |
| selector_stress | vs ledger_overlap | 1.0 | 0.743 |

Decoupling is preserved on matched graphs.

### Specificity (low_minus_high gap)

| mode | semantics | low_rescue | medium_rescue | high_rescue | gap | verdict |
|---|---|---|---|---|---|---|
| ledger_failure | at_least_k | 0.000 | 0.429 | 0.375 | **−0.375** | ledger_control_not_resolved_by_graph_coupled_orientation |
| ledger_failure | augmented_exact_k | 0.000 | 0.429 | 0.292 | **−0.292** | ledger_control_not_resolved_by_graph_coupled_orientation |
| orientation_degradation | at_least_k | 0.000 | 0.429 | 0.146 | **−0.146** | **`reversed_or_negative`** |
| orientation_degradation | augmented_exact_k | 0.000 | 0.429 | 0.229 | **−0.229** | **`reversed_or_negative`** |
| selector_stress | at_least_k | 0.000 | 0.000 | 0.000 | 0.000 | not_certification_channel |
| selector_stress | augmented_exact_k | 0.000 | 0.000 | 0.000 | 0.000 | not_certification_channel |

**The v1.5 specificity finding does not replicate.** Both
orientation_degradation cells show **reversed_or_negative** verdicts —
rescue is higher at high orientation_overlap, the opposite of the v1.5
claim that low orientation_overlap correlates with high rescue.

### Partial correlation

```
ledger_failure / at_least_k         : graph_coupled_residual_std=0.028, rescue_residual_std=0.000, partial_corr=NaN
ledger_failure / augmented_exact_k  : graph_coupled_residual_std=0.032, rescue_residual_std=0.000, partial_corr=NaN
orientation_degradation / at_least_k: graph_coupled_residual_std=0.028, rescue_residual_std=0.000, partial_corr=NaN
orientation_degradation / augmented_exact_k: graph_coupled_residual_std=0.032, rescue_residual_std=0.000, partial_corr=NaN
selector_stress (both)              : graph_coupled_residual_std=0.028/0.032, rescue_residual_std=0.000, partial_corr=NaN
```

After OLS partial control, **rescue residual variance collapses to zero**
in the v1.6 subset — meaning the support+frontier overlap fields explain
all the rescue variation in this sample. This is a signature of the
small-sample regime: the v0.9 trial-level rescue events at severity=0.5
with only 192 trials are too sparse for the partial correlation audit to
extract independent rescue variation. The v1.5 partial correlation result
(at_least_k −0.147, augmented_exact_k −0.070) is therefore **not
reproducible at v1.6's sample size on matched graphs**.

## Interpretation

Three findings are robust at v1.6:

1. **Disconnection closed.** Rescue and orientation_overlap are now
   measured on the same `CausalDAG` per trial. This is the methodological
   advance over v1.5.
2. **Decoupling holds.** graph_coupled_orientation_link_overlap is
   structurally distinct from support/frontier/legacy_orientation/ledger
   overlap on matched graphs (12/12 decoupled).
3. **Selector_stress remains a clean control.**

One finding is **negative** (no orientation specificity on matched graphs):

4. **The v1.5 "orientation specificity" result does not replicate when
   the disconnection is closed.** Both orientation_degradation cells show
   reversed-sign rescue gaps. This confirms the v1.5 honesty caveat: the
   v1.5 specificity was an artifact of the hash-to-graph mapping, not a
   topology-causal signal.

## Caveats

1. **Small-sample.** 192 trials on 24 per-cell rows. The reversed-sign
   verdict is a small-sample observation. Run v1.7+ at canonical 100-seed
   coverage before promoting reversal as a positive claim.
2. **Specific keying.** v1.6 reuses the v1.5 edge-pair-sign keying. Other
   topological orientation keys (sign-sources, ledger-orientation,
   chirality witnesses from `RA_CausalOrientation_Core`) may produce
   different results.
3. **Rescue floor.** v1.6 uses per-trial `certification_rescue_event`
   (binary 0/1); v0.9's published rates aggregate over many more samples.
4. **Retraction.** v1.5's claim of "cross-validating v0.9.2 family-
   semantics asymmetry" is **retracted** — that cross-validation depended
   on the hash-keyed mapping that v1.6 has now eliminated.

## What this means for the orientation-link program

The v1.x orientation-link program established:

- v1.0: confounding identified
- v1.1: confounding confirmed (orientation = support = frontier in v0.9)
- v1.2: synthetic orientation surface produces specificity (audit-machinery
  validation only; surface is hash-keyed)
- v1.3: catalog-derived surface produces specificity (still hash-keyed)
- v1.4: per-graph/per-member tokens produce specificity (still simulator-
  state, hash-keyed)
- v1.5: concrete-topology corpus produces specificity (still hash-keyed
  to v0.9 rescue)
- **v1.6: when the hash-keying is removed and rescue + orientation come
  from the same DAG, specificity does NOT persist (in this small sample).**

The honest reading of v1.2-v1.5 is: those packets demonstrated the v1.1
audit machinery resolves orientation specificity *if* a topology-derived
surface is provided AND the rescue values happen to correlate with that
surface via the keying. v1.6 shows the second condition does not hold on
matched graphs at v1.6's sample size — at least for this orientation
keying. Whether a different orientation keying (e.g. one rooted in
RA_CausalOrientation_Core's chirality theorems) would produce specificity
on matched graphs remains an open question for v1.7+.

## Recommended next step

**v1.7**: scale v1.6 to canonical v0.9 parameter coverage (50-100 seeds,
all severities, all thresholds) to determine whether the reversed-sign
verdict is small-sample noise or a robust finding. If reversal persists
at scale, that is a positive result in the opposite direction from v1.5
and worth documenting as such. If specificity emerges at scale (positive
gap), the v1.5 reading would be rehabilitated. Either outcome closes
the question.

**Or v1.7-alt**: try a different orientation keying (sign-source pairs,
ledger-orientation chirality from `RA_CausalOrientation_Core`) on matched
graphs and see whether THAT keying produces orientation specificity. If
yes, the v1.x program is keying-dependent, which is itself an important
finding.
