# RA Causal-DAG Motif Commit Simulator v1.6 — Graph-Coupled Orientation-Link Extraction

**This packet was revised 2026-05-05 after the original release: a bug in
the witness keying was identified, the analysis was re-run, and the
empirical conclusions were retracted/sharpened. See "Bug fix" below.**

This packet **closes the rescue/topology disconnection** identified as the
central honesty caveat of v1.5.

The honesty progression:

```text
v1.2 synthetic orientation surface          (hash of row metadata)
v1.3 native theorem-catalog surface         (Lean source files parsed)
v1.4 per-graph/per-member tokens            (simulator state + catalog)
v1.5 concrete graph topology                (parallel reference corpus)
v1.6 graph-coupled extraction               (rescue + orientation from the
                                             SAME v0.9 CausalDAG per trial)
```

## Method

v1.6 imports the v0.9 simulator directly and replays a constrained subset
of v0.9's parameter sweep. For each trial:

1. Build `ChannelSeedState` for the seed.
2. Run `evaluate_native_overlap_certified_family` → get the v0.9 row with
   `certification_rescue_event` and native overlap fields.
3. **Inline** on the same `state.dag`: compute v1.5-style edge-pair-sign
   orientation-link witnesses across the family cuts, take mean pairwise
   Jaccard → `v1_6_graph_coupled_orientation_link_overlap`.
4. Pair them in the trial row; aggregate per (mode, semantics, severity,
   threshold, support_width) cell; run the audit (decoupling, partial
   correlation, specificity).

Rescue and orientation_overlap come from the **same** `CausalDAG` per trial.

## Bug fix (2026-05-05)

The original v1.5/v1.6 `graph_coupled_orientation_link_witness` function
included `member_idx` in **both** the sign formula
(`(depth(v) + depth(p) + member_idx) % 2`) **and** the witness tag
(`m{member_idx % 3}`). For chains and other regular topologies where
edges have constant depth-parity, this made siblings produce **disjoint**
witness sets — member 0 got sign=1 on every edge while member 1 got
sign=0 — forcing intra-family Jaccard to 0 regardless of actual cut/edge
sharing.

Per-cell output **before the fix**: 18/24 cells had orientation_overlap
= 0 EXACTLY (only sw=4 had non-zero values, accidentally).

The corrected witness has sign = `(depth(v) + depth(p)) % 2` (a topological
invariant of the edge alone, not a per-sibling sign flip) and no member
tag. Intra-family Jaccard now reflects actual cut/edge sharing.

The same bug exists in v1.5's
`ra_concrete_graph_orientation_extraction.py`. v1.5 results should be
re-audited with the corrected keying before any v1.5 specificity finding
is cited.

## Run

```bash
python scripts/run_graph_coupled_orientation_extraction_v1_6.py \
  --v0-9-simulator-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/simulator \
  --output-dir outputs \
  --seed-start 17 --seed-stop 21 \
  --max-targets 8
```

Default config now: 4 seeds × 1 severance × 3 modes × 5 severities × 4
thresholds × 2 semantics × 8 targets = **3840 trials, 480 per-cell rows
(matches v1.0 component CSV structure)**, < 1s wall-clock.

## Results (post-fix, full coverage)

```text
n_trials                                   : 3840
n_per_cell_rows                            : 480
decoupled_count / decoupled_total          : 12 / 12 (100%)
graph_coupled_orientation_surface_decoupled: true
selector_guardrail_passed                  : true
v1_6_disconnection_closed                  : true
orientation_specificity_resolved_on_matched_graphs: false
```

### Specificity audit (post-fix, full coverage)

| mode | semantics | low_rescue | med | high | gap | verdict |
|---|---|---|---|---|---|---|
| ledger_failure | at_least_k | 0.000 | 0.062 | 0.156 | −0.156 | ledger_control_not_resolved |
| ledger_failure | augmented_exact_k | 0.000 | 0.043 | 0.150 | −0.150 | ledger_control_not_resolved |
| orientation_degradation | at_least_k | 0.000 | 0.052 | 0.138 | −0.138 | reversed_or_negative |
| orientation_degradation | augmented_exact_k | 0.000 | 0.029 | 0.127 | −0.127 | reversed_or_negative |
| selector_stress | both | 0.000 | 0.000 | 0.000 | 0.000 | not_certification_channel |

**The "reversed_or_negative" verdict is a support_width confound, not
topology-causal anti-specificity.** Cells with support_width=1 have
orientation_overlap=0 (single-cut family) AND rescue=0 (narrow cuts cannot
rescue independent of any orientation channel). Sorting cells by
orientation_overlap therefore essentially sorts by family-structure-
richness, which determines rescue independently of the orientation channel.

### Partial correlation (after support+frontier OLS control)

| mode | semantics | partial_corr | n |
|---|---|---|---|
| ledger_failure | at_least_k | +0.014 | 80 |
| ledger_failure | augmented_exact_k | +0.132 | 80 |
| orientation_degradation | at_least_k | **−0.101** (v1.5 direction) | 80 |
| orientation_degradation | augmented_exact_k | **+0.123** (opposite) | 80 |
| selector_stress | both | NaN (rescue residual = 0) | 80 |

At n=80 per cell, **|r|<0.15 is below the noise floor** (p~0.4 for r=0.10).
None of the partial correlations is statistically significant.

## Honest conclusion

At v1.6 sample size, with the bug fixed and the disconnection closed,
**there is no statistically detectable topology-specific correlation
between graph_coupled_orientation_link_overlap and certification_rescue
on matched v0.9 simulator graphs — in either direction — for this
edge-pair-sign keying.**

Both retracted:
- v1.5 "specificity gap +0.028" → likely an artifact of the keying bug
  combined with hash-keyed cell-to-graph mapping. With both eliminated,
  the matched signal is noise.
- The original v1.6 "specificity reversal" conclusion → driven by
  support_width confound, not topology-causal anti-specificity.

The v0.9.2 family-semantics asymmetry remains a v0.9-internal finding.
The v1.x orientation-link program (v1.2 through v1.6) does **not** provide
independent topology-causal evidence for or against it at v1.6 sample
size.

## Discipline (going forward)

Any future orientation-link rescue claim must be:

1. **Measured on matched graphs** (rescue and orientation_overlap from
   the same `CausalDAG` per trial).
2. **Audited via partial correlation against support+frontier overlap**
   (specificity-by-quantile is unreliable when cell structure correlates
   with rescue independently of the orientation channel).
3. **Verified at sample size that resolves |r|>0.2 reliably (n>200
   per cell)** — v1.6's n=80 is too low.
4. **Tested against multiple orientation keyings** before any
   keying-specific conclusion. The edge-pair-sign keying may simply be
   the wrong feature; alternate keyings (sign-source pairs from
   `RA_CausalOrientation_Core`, ledger-orientation chirality from
   `RA_D1_NativeLedgerOrientation`) deserve testing.

## Outputs

```text
ra_v1_6_trial_rows.csv             (3840 trial rows)
ra_v1_6_per_cell_aggregated.csv    (480 per-cell rows matching v1.0 schema)
ra_v1_6_decoupling_audit.csv       (12/12 cells decoupled)
ra_v1_6_partial_correlation.csv    (clean test, n=80 per (mode x semantics))
ra_v1_6_specificity.csv            (confounded by support_width; do not cite as topology-causal)
ra_v1_6_summary.csv                (single-row summary)
ra_v1_6_summary.md                 (narrative)
ra_v1_6_state.json                 (state JSON)
```

## What v1.6 establishes (post-fix)

- The methodological setup for graph-coupled extraction works: rescue
  and orientation_overlap come from the same `CausalDAG` per trial.
- Decoupling of orientation_link from support/frontier/legacy_orientation
  /ledger holds even on matched graphs (12/12 cells).
- Selector_stress remains a clean control.
- The witness-keying bug shared between v1.5 and v1.6 has been
  identified and fixed.

## What v1.6 does NOT establish (post-fix)

- Whether matched orientation_overlap correlates with rescue (in either
  direction) — at n=80 per cell, the signal is too weak to distinguish
  from zero.
- Whether the v0.9.2 family-semantics asymmetry has any topology-causal
  basis — that's an open question for v1.7+.
- Anything about Nature — v1.6 is operational diagnostic only.
