# RA Causal-DAG Motif-Commit Simulator v0.5 Report

Date: May 04, 2026

## Purpose

v0.5 adds a causal-severance / actualization-fragility workbench to the RA-native causal-DAG motif-commit simulator.

The purpose is to test how certified motif actualization behaves when causal support is disrupted, delayed, or locally uncertified. The operational target remains RA-native:

```text
support certification
  → causal readiness
  → selected / strict commitment
  → causal-severance intervention
  → survival, loss, finality-shift, and recovery diagnostics
```

## New intervention modes

```text
edge_dropout
frontier_dropout
support_delay
orientation_degradation
ledger_failure
selector_stress
```

## New diagnostics

```text
lost_support
lost_readiness
lost_strict_commit
lost_selected_commit
finality_depth_before
finality_depth_after
finality_depth_shift
recovery_length
fragility profile by mode/severity/support_width
```

## Validation

Unit tests:

```text
python -m unittest discover -s tests -v
```

Result:

```text
Ran 16 tests
OK
```

## Demo run

Demo command used for packet outputs:

```bash
python simulator/ra_causal_dag_simulator.py --steps 8 --max-targets 5
```

Demo summary:

```text
nodes=9 edges=11 motifs=15
severance_evaluations=72
fragility_profiles=18
sweep_rows=18
total_lost_support=32
total_lost_readiness=40
total_lost_strict_commit=48
total_lost_selected_commit=40
```

## Main output artifacts

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

## Interpretation

v0.5 separates several failure modes that would otherwise be conflated:

```text
support-certification loss
causal-readiness loss
commitment loss from incompatibility/selector stress
finality shift without permanent support destruction
recovery after delayed support
```

This gives RA a sharper language for actualization fragility: a motif can fail to actualize because its support is no longer certified, because its support no longer reaches the site, because readiness is delayed, or because selector structure changes among certified-ready alternatives.

## Methodological guardrail

This simulator remains an RA-native actualization workbench. It does not treat inherited theoretical machinery as an operational target. Comparisons to prior theories should be made only in explicitly marked correspondence sections after RA-native diagnostics are stable.

## Included Lean bridge draft

`lean/RA_MotifCausalSeveranceBridge.lean` is included as a source-level bridge draft. It introduces abstract post-severance readiness, destroyed-support, post-severance commit, and post-severance finality predicates. Compilation status is pending local Lean/Lake check.

## Optional Lean bridge skeleton

The packet includes `lean/RA_MotifCausalSeveranceBridge.lean` as a source-level bridge skeleton. It is intentionally not promoted to compile-confirmed status here. The next formal step is to install it in the Lean project, repair any local namespace/import issues, and run:

```bash
lake build RA_MotifCausalSeveranceBridge
```
