# RA Causal-DAG Motif Commit Simulator v1.8 — Support-Width / Family-Structure Confound Audit

## Purpose

v1.7 showed that orientation-specific certification rescue does not survive matched-graph orientation-keying ablation. The graph-derived keyings and shuffled overlap control produced nearly the same low/high rescue gaps, suggesting that the apparent orientation gaps may be driven by support-width, family-size, and binning structure rather than orientation-link specificity.

v1.8 is an analysis-only packet over v1.7 outputs. It introduces no Lean module, no simulator semantics, and no new rescue mechanism.

## Inputs

The packet expects a v1.7 output directory containing:

```text
ra_v1_7_keyed_trial_rows.csv
```

## Outputs

```text
ra_v1_8_width_by_orientation_bin.csv
ra_v1_8_family_size_by_orientation_bin.csv
ra_v1_8_rescue_by_width_matched_bins.csv
ra_v1_8_orientation_gap_after_width_matching.csv
ra_v1_8_shuffled_vs_graph_within_width.csv
ra_v1_8_orientation_bin_association.csv
ra_v1_8_confound_summary.csv
ra_v1_8_confound_summary.md
ra_v1_8_state.json
```

## Interpretation

The key question is:

```text
Are low/medium/high orientation-overlap bins actually sorting by support width or family size?
```

If low-overlap bins are dominated by narrow support cuts or singleton families, then low rescue rates may reflect the absence of possible support-family rescue rather than an orientation-link effect.

## Canonical run command

```bash
python scripts/run_support_width_family_confound_v1_8.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v1_7_OrientationKeyingAblation_May06_2026/outputs \
  --output-dir outputs
```

## Packet-local demo result

Against the packet-local v1.7 subset outputs:

```text
input_rows = 1152
keying_count = 6
width_classes = 1;2;3;4
family_size_classes = 1;3;4;7;11
selector_guardrail_passed = true
mean_abs_raw_gap_graph_keyings ≈ 0.171
support_width_bin_association_mean_abs ≈ 0.759
family_size_bin_association_mean_abs ≈ 0.563
```

The packet-local subset has no width stratum containing both low and high orientation bins. That is itself evidence of bin/width entanglement in the small v1.7 subset. Canonical v1.7 outputs should provide the controlling analysis.

## RAKB status

The registry proposals are active-schema style and intentionally include no auto-apply script. Promote claims only after running against the canonical v1.7 sweep outputs.
