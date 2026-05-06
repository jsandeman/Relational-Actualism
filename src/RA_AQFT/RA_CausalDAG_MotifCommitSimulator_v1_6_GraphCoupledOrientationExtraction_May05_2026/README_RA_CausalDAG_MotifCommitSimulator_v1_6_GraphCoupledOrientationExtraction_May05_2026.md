# RA Causal-DAG Motif Commit Simulator v1.6 — Graph-Coupled Orientation-Link Extraction

This packet **closes the rescue/topology disconnection** identified as the
central honesty caveat of v1.5.

The honesty progression:

```text
v1.2 synthetic orientation surface          (hash of row metadata)
v1.3 native theorem-catalog surface         (Lean source files parsed)
v1.4 per-graph/per-member tokens            (simulator state + catalog)
v1.5 concrete graph topology                (parallel reference corpus, NOT
                                             the v0.9 simulator's actual graphs)
v1.6 graph-coupled extraction               (rescue + orientation from the
                                             SAME v0.9 CausalDAG instance per trial)
```

## Method

v1.6 imports the v0.9 simulator directly (`ra_causal_dag_native_cert_overlap`,
`ra_causal_dag_channel_workbench`, `ra_causal_dag_support_family_monotonicity`)
and replays a small subset of v0.9's parameter sweep. For each trial:

1. Build `ChannelSeedState` for the seed.
2. Run `evaluate_native_overlap_certified_family` → get the v0.9 row with
   `certification_rescue_event` (binary 0/1) plus all native overlap fields.
3. **Inline** on the SAME `state.dag`: compute v1.5-style edge-pair-sign
   orientation-link witnesses across the family cuts, take mean pairwise
   Jaccard → `v1_6_graph_coupled_orientation_link_overlap`.
4. Pair them in the trial row; aggregate per (mode, semantics, severity,
   threshold, support_width) cell; run the v1.5 audit (decoupling, partial
   correlation, specificity).

Rescue and orientation_overlap now come from the **same** `CausalDAG`
instance. There is no hash-keyed mapping from cells to graphs.

## Run

```bash
python scripts/run_graph_coupled_orientation_extraction_v1_6.py \
  --v0-9-simulator-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/simulator \
  --output-dir outputs \
  --seed-start 17 --seed-stop 21 \
  --max-targets 8
```

Default config: 4 seeds × 1 severance × 3 modes × 1 severity × 1 threshold
× 2 semantics × 8 targets = 192 trials, ~30s.

## Headline result

The v1.5 "orientation specificity" verdict does **NOT** replicate when
rescue and orientation come from the same graphs.

| metric | v1.5 (disconnected) | v1.6 (matched) |
|---|---|---|
| disconnection closed | no | **yes** |
| decoupling vs support/frontier/legacy/ledger | 12/12 | **12/12** |
| selector_guardrail | passed | **passed** |
| orientation_degradation specificity verdict | augmented_exact_k → `concrete_orientation_specific_surface_detected` (gap +0.028) | both semantics → **`reversed_or_negative`** (gap −0.146 / −0.229) |
| orientation_specificity_resolved | true | **false** |

The reversal of sign for orientation_degradation (rescue HIGHER at HIGH
orientation_overlap, not LOW) directly contradicts the v1.5 specificity
claim. Two interpretations are consistent with the data:

1. **The v1.5 specificity was a sampling artifact** of the hash-to-graph
   mapping (this matches the v1.5 caveat we explicitly flagged).
2. **Orientation rescue is genuinely correlated with high overlap on
   matched graphs**, the opposite direction from the v1.x narrative — but
   this needs more samples before it can be a positive claim.

Either way, **the v1.5 "v1.5 cross-validates v0.9.2 family-semantics
asymmetry" claim is now retracted**. v0.9.2's family-semantics asymmetry
remains a v0.9-internal finding; v1.5/v1.6 do not provide independent
cross-validation.

## Honesty caveats

1. **Subset of v0.9 sweep.** v1.6 runs 4 seeds × 1 severance × 1 severity
   × 1 threshold = 4 cells per (mode × semantics) — much smaller than v0.9's
   full sweep. The reversal is therefore a small-sample finding; v1.7+
   should expand to canonical 100-seed coverage before the negative
   reversal is promoted as a positive claim.
2. **Orientation-link witness keying.** v1.6 reuses the v1.5 edge-pair-sign
   keying scheme (parent→child + depth-mod-2 + member-index parity). This
   is one specific topological keying among many. A different keying (e.g.
   chirality, sign-source pairs, native-ledger orientation) might produce
   different results. v1.6 doesn't claim this is THE correct topological
   orientation key — only that it's a v0.9-graph-matched extension of the
   v1.5 keying.
3. **Rescue is per-trial binary, not aggregated rate.** v1.6 averages
   `certification_rescue_event` across trials per cell. v0.9's published
   CSVs aggregate over many more samples; v1.6's per-cell rescue rates
   are noisier than v0.9's.

## Outputs

```text
ra_v1_6_trial_rows.csv             (per-trial rescue event + matched orientation overlap)
ra_v1_6_per_cell_aggregated.csv    (per-cell mean rescue + mean overlap)
ra_v1_6_decoupling_audit.csv       (graph_coupled vs support/frontier/legacy/ledger)
ra_v1_6_partial_correlation.csv    (OLS partial corr after support+frontier control)
ra_v1_6_specificity.csv            (low/medium/high quantile rescue gap)
ra_v1_6_summary.csv                (single-row summary)
ra_v1_6_summary.md                 (narrative)
ra_v1_6_state.json                 (state JSON)
```

## What v1.6 does NOT establish

- v1.6 does NOT claim Nature's orientation rescue is reverse-correlated
  with orientation overlap. The reversal is a small-sample observation on
  one keying scheme; it might be noise.
- v1.6 does NOT validate the v0.9.2 family-semantics asymmetry — that
  asymmetry remains a v0.9 internal finding.

## What v1.6 DOES establish

- The methodological setup for graph-coupled extraction works: rescue and
  orientation now come from the same `CausalDAG` per trial.
- The v1.5 "orientation specificity" result is **not robust** to closing
  the disconnection — confirming the v1.5 caveat we explicitly flagged.
- Decoupling of orientation_link from support/frontier/legacy_orientation
  /ledger holds even on matched graphs (12/12 cells).
- Selector_stress remains a clean control.
