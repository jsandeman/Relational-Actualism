# Track B.4 Locked-Envelope Matched-Graph Orientation Rescue Analysis

This packet is a tightly scoped analysis over the narrow coverage envelope found by Track B.3b:

- `keying = incidence_role_signed`
- `family_semantics = augmented_exact_k`
- `threshold_fraction = 0.25`

It compares the graph-derived locked keying to `shuffled_overlap_control` under fixed-bin, joint `support_width × family_size` discipline.

## Scope discipline

This packet does **not** generalize beyond the B.3b envelope and does **not** make a Nature-facing or general orientation-rescue claim. It reports whether the locked envelope contains an estimable graph-vs-shuffled residual association.

## Canonical run

```bash
python scripts/run_trackB4_locked_envelope_rescue.py \
  --input-dirs ../RA_CausalDAG_MotifCommitSimulator_v1_7_OrientationKeyingAblation_May06_2026/outputs,../RA_TrackB3b_OrientationWitnessSamplerRebalance_May06_2026/outputs \
  --output-dir outputs \
  --min-rows-per-bin 25
```

If the input rows do not include rescue-event columns, the packet reports non-estimability rather than manufacturing a rescue analysis from coverage-only data.

## Outputs

- `ra_trackB4_locked_envelope_trials.csv`
- `ra_trackB4_fixed_bin_gaps.csv`
- `ra_trackB4_joint_stratum_gaps.csv`
- `ra_trackB4_width_family_matched_gap.csv`
- `ra_trackB4_graph_vs_shuffled_controls.csv`
- `ra_trackB4_power_coverage.csv`
- `ra_trackB4_summary.csv`
- `ra_trackB4_locked_envelope_summary.md`

## Guardrail

`orientation_rescue_claim_made = false` by construction. Human review is required before any registry claim can be promoted, and any claim must remain locked to the B.3b envelope unless a broader coverage audit is passed.
