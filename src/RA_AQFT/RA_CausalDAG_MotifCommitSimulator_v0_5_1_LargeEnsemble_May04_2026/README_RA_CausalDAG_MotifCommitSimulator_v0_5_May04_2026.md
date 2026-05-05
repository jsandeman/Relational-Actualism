# RA Causal-DAG Motif-Commit Simulator v0.5

This packet adds a causal-severance / actualization-fragility workbench to the RA-native motif-commit simulator.

The v0.5 ladder is:

```text
candidate motif
  → finite Hasse-frontier support cut
  → graph-oriented support witness
  → orientation-gated support certification
  → causal readiness
  → strict commitment / selected commitment
  → causal-severance intervention
  → support/readiness/commitment/finality survival diagnostics
```

The simulator remains RA-native. It does not model messages, votes, observer-triggered collapse, inherited spacetime geometry, or inherited Hilbert-space structure as targets.

## Main additions

- `CausalSeveranceIntervention`
- `SeveranceEvaluation`
- `evaluate_severance`
- `run_severance_workbench`
- `summarize_severance_sweep`
- `summarize_fragility`
- `min_finality_depth`
- `readiness_recovery_length`

## Intervention modes

```text
edge_dropout
frontier_dropout
support_delay
orientation_degradation
ledger_failure
selector_stress
```

## Main outputs

```text
outputs/ra_causal_dag_severance_summary_v0_5.csv
outputs/ra_causal_dag_severance_evaluations_v0_5.csv
outputs/ra_causal_dag_severance_sweep_v0_5.csv
outputs/ra_causal_dag_fragility_profiles_v0_5.csv
outputs/ra_causal_dag_finality_depth_shift_v0_5.csv
outputs/ra_causal_dag_recovery_lengths_v0_5.csv
outputs/ra_causal_dag_severance_predictions_v0_5.md
outputs/ra_causal_dag_severance_state_v0_5.json
```

## Run

```bash
python simulator/ra_causal_dag_simulator.py
python -m unittest discover -s tests -v
```

The default run is intentionally modest (`steps=8`, `max_targets=4`) so the severance workbench remains fast in ordinary development environments.

## Included Lean bridge draft

The packet also includes:

```text
lean/RA_MotifCausalSeveranceBridge.lean
```

This is a source-level bridge draft. It defines post-severance readiness and commitment predicates over the existing graph motif-commit stack. It has not been compiled in this container.

## Optional Lean bridge skeleton

The packet also includes:

```text
lean/RA_MotifCausalSeveranceBridge.lean
```

This file is a source-level bridge skeleton for the next Lean step. It is not marked compile-confirmed in this packet; run local `lake build RA_MotifCausalSeveranceBridge` before promoting any RAKB status derived from it.
