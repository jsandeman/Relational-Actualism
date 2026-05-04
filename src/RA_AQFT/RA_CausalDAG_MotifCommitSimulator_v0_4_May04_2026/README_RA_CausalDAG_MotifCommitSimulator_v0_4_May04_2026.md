# RA Causal-DAG Motif-Commit Simulator v0.4

Date: May 04, 2026

This packet adds **orientation-gated support certification** to the RA causal-DAG motif-commit simulator.

The simulator remains RA-native. It does not simulate Quantum Mechanics, General Relativity, blockchain consensus, voting, message rounds, or observer-driven collapse. It explores the RA vocabulary introduced by the compiled formal stack:

```text
RA_MotifCommitProtocol
  -> support cuts, readiness, strict commitment
RA_MotifSelectorClosure
  -> selector closure and selected commitment
RA_MotifOrientationSupportBridge
  -> graph-oriented support witnesses and witnessed incompatibility
```

## New v0.4 layer

v0.3 certified support mainly by checking graph-native Hasse-frontier support, local gates, and selector closure behavior. v0.4 requires a concrete simulator witness:

```text
GraphOrientedMotifSupport
  candidate_past
  support_cut
  OrientationClosureCertificate
  frontier_sufficient_for_motif
  local_ledger_compatible
  carrier_represented_by_frontier
```

The orientation closure certificate carries these gates:

```text
selector_compatible
no_extra_random_labels
no_particle_label_primitives
qN1_signature = 7
local_conserved
sign_links
```

A motif is supported only if the ordinary support-cut gates and the orientation witness gates all pass.

## Important simulator/Lean caveat

The Lean bridge states a `carrier_in_candidate_past` obligation. The simulator represents motif carriers as actualization-site carriers, so v0.4 uses an operational proxy:

```text
support frontier reaches every carrier vertex
AND witness.carrier_represented_by_frontier = true
```

This avoids collapsing support cuts into the actualization site while still enforcing a native support-representation discipline. The report records this explicitly.

## Validation

Run:

```bash
python3 -m unittest discover -s tests -v
```

Recorded result:

```text
Ran 8 tests
OK
```

The demo run produced:

```text
nodes=25
edges=33
motifs=41
sites=24
total_strict_committed=328
total_strict_blocked=70
total_selector_committed=363
total_selector_rejected=35
total_selector_stalemates=0
total_unsupported=140
total_orientation_failures=68
mean_support_width=1.0
```

## Main files

```text
simulator/ra_causal_dag_simulator.py
tests/test_v0_4_orientation_support.py
outputs/ra_causal_dag_demo_summary_v0_4.csv
outputs/ra_causal_dag_support_evaluations_v0_4.csv
outputs/ra_causal_dag_selector_components_v0_4.csv
outputs/ra_causal_dag_orientation_witnesses_v0_4.csv
outputs/ra_causal_dag_orientation_conflicts_v0_4.csv
outputs/ra_causal_dag_orientation_comparison_v0_4.csv
outputs/ra_causal_dag_parameter_sweep_v0_4.csv
outputs/ra_causal_dag_demo_state_v0_4.json
reports/validation_unittest_v0_4.log
reports/demo_run_v0_4.log
```

## How to run

From the packet root:

```bash
python3 simulator/ra_causal_dag_simulator.py --run-sweep
```

or simply:

```bash
python3 simulator/ra_causal_dag_simulator.py
```

## RAKB status

The registry proposal files in `registry_proposals/` are written for the active v0.5-style schema, not the older flat proposal schema. They are proposals, not auto-applied mutations.
