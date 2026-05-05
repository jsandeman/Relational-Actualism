# RA Causal-DAG Motif-Commit Simulator v0.5.2 Ensemble Analysis Report

Date: May 05, 2026

## Summary

v0.5.2 adds a severance-signature analysis layer over the v0.5.1 large-ensemble causal-severance workbench. It is designed to consume the committed v0.5.1 ensemble outputs and classify RA-native actualization-fragility profiles.

This packet is not a new simulator dynamics layer and not a new Lean formalization. It is an analysis packet.

## RA-native analysis targets

The analysis extracts:

- mode-by-severity fragility profiles;
- threshold saturation scores;
- channel classifications;
- support-width fragility summaries;
- finality-depth shift signatures;
- recovery-length signatures;
- pairwise mode separability scores.

## Channel classification

The analyzer distinguishes:

```text
threshold_saturating_support_loss
  support/readiness/commitment loss saturates once nonzero severance is applied

graded_delay_without_support_loss
  support remains present, but readiness/commitment/finality shift with severity

strict_channel_threshold_saturation
  strict commitment fails while support/readiness/selected commitment survive
```

These are simulator-regime signatures. They should not be overpromoted into Nature-facing claims until linked to observable RA targets.

## User-reported canonical run context

The local operator reported the canonical 100-seed run:

```text
Seeds: 100 (17-117)
Steps per run: 32
Workers: 4
Actual evaluations: 120,000
Sampled evaluations: 5,000
Wall time: 60.13s
Throughput: ~1,996 eval/s
Aggregate losses: support 62,081; readiness 77,617; strict_commit 93,153; selected_commit 77,617
```

The operator also reported that `edge_dropout`, `frontier_dropout`, and `ledger_failure` show near-uniform nonzero severity loss around 0.971, indicating threshold-like saturation in the current v0.5.1 intervention semantics.

## Packet-local demo result

The demo run in this packet used the v0.5.1 output files available in this environment, which were the earlier 20-seed packet-local outputs. It produced the expected v0.5.2 analysis outputs and classified modes as follows:

```text
edge_dropout: threshold_saturating_support_loss
frontier_dropout: threshold_saturating_support_loss
ledger_failure: threshold_saturating_support_loss
orientation_degradation: threshold_saturating_support_loss
selector_stress: strict_channel_threshold_saturation
support_delay: graded_delay_without_support_loss
```

## Important caveat

The packet-local demo outputs are not the canonical 100-seed outputs. To promote the candidate RAKB signature claims, rerun the analyzer against the committed 100-seed outputs.

## Validation

Unit tests:

```text
Ran 4 tests
OK
```

Tested behavior:

- threshold-saturating support loss classification;
- support-delay classification as readiness/finality/recovery shift without support loss;
- selector-stress classification as strict-commit incompatibility channel;
- end-to-end writing of all expected analysis outputs.

## Next step

Run the analyzer against the committed 100-seed v0.5.1 outputs and inspect:

```text
outputs/ra_severance_mode_signatures_v0_5_2.csv
outputs/ra_mode_separability_scores_v0_5_2.csv
outputs/ra_severance_signature_summary_v0_5_2.md
```

Then promote only the confirmed signature claims into RAKB.
