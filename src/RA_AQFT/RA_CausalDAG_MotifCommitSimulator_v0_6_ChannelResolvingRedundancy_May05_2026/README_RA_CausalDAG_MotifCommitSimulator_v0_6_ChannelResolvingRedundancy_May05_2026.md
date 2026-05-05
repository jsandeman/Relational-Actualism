# RA Causal-DAG Motif-Commit Simulator v0.6 — Channel-Resolving Redundancy Workbench

Date: May 05, 2026

This packet extends the v0.5/v0.5.1/v0.5.2 causal-severance workbench with two RA-native corrections identified by the canonical 100-seed v0.5.2 analysis:

1. **Support-frontier width diversity**: generated motif support cuts now include multiple finite Hasse-frontier widths, so support-width fragility is no longer blocked by `support_width_count = 1`.
2. **Channel-resolved diagnostics**: severance modes now report separated failure channels rather than compressing all failures into a single support/readiness/commitment loss vector.

The operational ladder remains RA-native:

```text
candidate motif
  → finite Hasse-frontier support cut
  → orientation-gated support witness
  → certified support
  → causal readiness
  → operational support availability
  → strict / selected commitment
  → channel-resolved severance diagnostics
```

No Lean module is changed in this packet. The compiled `RA_MotifCausalSeveranceBridge` remains the formal anchor; v0.6 is a simulator-analysis workbench refinement.

## Key additions

New module:

```text
simulator/ra_causal_dag_channel_workbench.py
```

New command:

```bash
python scripts/run_channel_resolving_redundancy_v0_6.py   --seed-start 17   --seed-stop 21   --steps 16   --max-targets 8   --sample-limit 500   --severance-seeds 101,103   --severities 0.0,0.25,0.50,0.75,1.0   --output-dir outputs
```

## Demo validation

Unit tests:

```text
Ran 6 tests
OK
```

Demo run summary:

```text
run_count=4
steps=16
actual_evaluations=1440
sampled_evaluations=500
support_width_classes=[1, 2, 3, 4]
support_width_count=4
total_lost_support_certification=198
total_lost_causal_reachability=551
total_lost_support_availability=192
total_lost_operational_readiness=726
total_lost_strict_commit=910
total_lost_selected_commit=726
```

## Channel outcomes in the packet demo

```text
edge_dropout              → causal_reachability_channel
frontier_dropout          → frontier_availability_channel
ledger_failure            → ledger_certification_channel
orientation_degradation   → orientation_witness_certification_channel
selector_stress           → selector_exclusion_channel
support_delay             → delay_recovery_channel
```

The former v0.5.2 degeneracy among `frontier_dropout`, `ledger_failure`, and `orientation_degradation` is broken in the demo:

```text
frontier_dropout vs ledger_failure: distance=1.714665, cosine=0.485531
frontier_dropout vs orientation_degradation: distance=1.714665, cosine=0.485531
ledger_failure vs orientation_degradation: distance=0.751301, cosine=0.738639
```

## Outputs

```text
ra_channel_separation_summary_v0_6.csv
ra_channel_separation_runs_v0_6.csv
ra_channel_separation_aggregate_v0_6.csv
ra_channel_resolved_fragility_v0_6.csv
ra_gate_failure_decomposition_v0_6.csv
ra_support_width_fragility_v0_6.csv
ra_support_width_fragility_curve_v0_6.csv
ra_redundancy_survival_profiles_v0_6.csv
ra_channel_mode_signatures_v0_6.csv
ra_threshold_vs_graded_classification_v0_6.csv
ra_channel_mode_separability_v0_6.csv
ra_mode_separability_channel_resolved_v0_6.csv
ra_channel_evaluations_sample_v0_6.csv
ra_channel_separation_predictions_v0_6.md
ra_channel_separation_state_v0_6.json
```

## RAKB handling

Active-schema proposal files are included under `registry_proposals/`. There is intentionally no auto-apply script. Apply manually using the active RAKB v0.5 workflow after running a canonical v0.6 ensemble.

## Caveat

The included demo is a packet validation run, not a canonical ensemble. The RAKB proposals are marked as pending canonical v0.6 run confirmation.
