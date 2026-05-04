# RA Causal-DAG Motif-Commit Simulator v0.2 — May 4, 2026

This packet extends the v0.1 RA causal-DAG motif-commit simulator by making `CommitContext.supports` concrete through a graph-native support certifier.

The simulator remains RA-native: it does not model agents, messages, votes, rounds, leaders, or blockchain finality. It models support-cut readiness and motif commit over a finite causal DAG.

## Core addition in v0.2

`GraphSupportCertifier` instantiates the abstract Lean-side relation:

```text
GraphCommitContext.supports : GraphMotifCandidate G → GraphSupportCut G → Prop
```

with a Python predicate that checks whether a proposed support cut is:

1. declared by the motif;
2. graph-native and finite;
3. the Hasse frontier of the motif's declared candidate past;
4. causally prior to every carrier vertex;
5. within optional width/depth-span bounds;
6. accepted by explicit placeholder gates for future BDG, local-ledger, and orientation-closure checks.

The BDG/local-ledger/orientation gates are simulator gates only. They are not presented as derived physics. They are explicit attachment points for later Lean or RAKB content.

## Lean-to-Python correspondence

```text
Lean MotifCandidate / GraphMotifCandidate
  ↔ Python MotifCandidate

Lean CausalSupportCut / GraphSupportCut
  ↔ Python SupportCut = frozenset[node_id]

Lean supportCutOfFiniteHasseFrontier
  ↔ CausalDAG.support_cut_of_finite_hasse_frontier

Lean DAGReadyAt / GraphReadyAt
  ↔ CausalDAG.ready_at

Lean DAGCommitContext.supports / GraphCommitContext.supports
  ↔ GraphSupportCertifier.supports, wrapped by CommitContext

Lean incompatible relation
  ↔ CommitContext.incompatible

Lean DAGCommitsAt / GraphCommitsAt
  ↔ MotifCommitProtocol.decision(...).commits

Lean DAGFinalizedAtDepth / GraphFinalizedAtDepth
  ↔ CausalDAG.finalized_at_depth
```

## Packet contents

```text
simulator/ra_causal_dag_simulator.py
simulator/run_demo.py
simulator/__init__.py
tests/test_ra_causal_dag_simulator.py
outputs/ra_causal_dag_demo_summary_v0_2.csv
outputs/ra_causal_dag_support_evaluations_v0_2.csv
outputs/ra_causal_dag_demo_state_v0_2.json
outputs/ra_causal_dag_parameter_sweep_v0_2.csv
patches/patch_ra_causal_dag_simulator_v0_1_to_v0_2.diff
reports/RA_CausalDAG_MotifCommitSimulator_v0_2_May04_2026_Report.md
scripts/run_tests.sh
scripts/run_demo_and_sweep.sh
```

## Run tests

From the packet root:

```bash
python -m unittest discover -s tests -v
```

Validated in the assistant container:

```text
Ran 11 tests in 0.012s
OK
```

## Run the demo

```bash
python simulator/ra_causal_dag_simulator.py \
  --steps 24 \
  --seed 17 \
  --conflict-rate 0.30 \
  --defect-rate 0.12 \
  --run-sweep
```

Validated demo output:

```text
nodes=25 edges=31 motifs=37
summary={'sites': 24, 'total_committed': 324, 'total_blocked': 136, 'total_unsupported': 26, 'mean_support_width': 1.0, 'last_site': 24}
sweep_rows=48
```

## Interpretation

The important new behavior is that an incompatible motif blocks another motif only if the competitor is itself support-certified and ready. A support-defective competitor does not block a certified-ready motif.

This matches the context-gated Lean semantics: arbitrary finite support sets do not count as evidence unless `Γ.supports M Q` certifies them.
