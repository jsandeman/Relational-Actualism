# RA Causal-DAG Motif Commit Simulator v1.8.1
## Joint Width × Family-Size Confound Audit

This packet is an analysis-only follow-up to v1.8.

v1.8 showed that width-only matching changes the interpretation of the v1.7 orientation-keying ablation: shuffled-control gaps are strongly width/binning-driven, while graph-derived keyings may retain a residual low/high orientation-overlap rescue gap after support-width matching. However, v1.8 also showed strong association between orientation-overlap bins and `family_size`.

v1.8.1 therefore performs stricter matching:

```text
support_width × family_size
```

The goal is not to introduce new orientation semantics. The goal is to decide whether the v1.8 residual graph-derived orientation gap survives the next confound control.

## Inputs

Requires a v1.7 output directory containing:

```text
ra_v1_7_keyed_trial_rows.csv
```

## Outputs

```text
ra_v1_8_1_raw_specificity_gaps.csv
ra_v1_8_1_width_matched_gap.csv
ra_v1_8_1_joint_stratum_gaps.csv
ra_v1_8_1_joint_width_family_matched_gap.csv
ra_v1_8_1_graph_vs_shuffled_joint_matched.csv
ra_v1_8_1_estimability_by_stratum.csv
ra_v1_8_1_orientation_gap_decomposition.csv
ra_v1_8_1_joint_confound_summary.csv
ra_v1_8_1_joint_confound_summary.md
ra_v1_8_1_state.json
```

## Canonical run

```bash
python scripts/run_joint_width_family_confound_v1_8_1.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v1_7_OrientationKeyingAblation_May06_2026/outputs \
  --output-dir outputs
```

## Decision rules

If graph-derived gaps shrink under joint matching and match shuffled controls, the v1.8 residual is explained by family-structure confounding.

If graph-derived gaps survive joint matching and differ from shuffled controls inside the same joint strata, the v1.8 residual remains a candidate graph-derived orientation association.

If too few joint strata are estimable, the current sampler cannot decide the question; a redesigned matched sampler is required.

## Packet-local demo

The included packet-local run used the v1.7 subset outputs available in this environment. It found no estimable joint strata for graph keyings, which is a useful demonstration of the non-estimability branch, not a canonical scientific conclusion.

