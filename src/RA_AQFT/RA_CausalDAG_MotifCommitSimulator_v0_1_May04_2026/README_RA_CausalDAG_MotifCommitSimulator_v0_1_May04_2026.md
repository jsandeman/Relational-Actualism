# RA Causal-DAG Motif-Commit Simulator v0.1 — May 4, 2026

This simulator is the first Python workbench aligned with the compiled `RA_MotifCommitProtocol` interface.

It deliberately models RA-native objects rather than engineered consensus machinery:

```text
MotifCandidate
SupportCut
support_cut_of_finite_hasse_frontier
ready_at
CommitContext.supports
CommitContext.incompatible
CommitsAt
FinalizedAtDepth
```

There are no agents, leaders, votes, rounds, or network messages in this simulator. The core operation is purely causal-graph-theoretic:

```text
A motif commits at a site iff its support cut is certified, all support vertices reach the site, and no certified-ready incompatible motif competes there.
```

## Run the demo

From the packet root:

```bash
python simulator/ra_causal_dag_simulator.py   --steps 24   --seed 17   --conflict-rate 0.30   --csv outputs/ra_causal_dag_demo_summary.csv   --json outputs/ra_causal_dag_demo_state.json
```

or:

```bash
python simulator/run_demo.py
```

## Run tests

From the packet root:

```bash
python -m unittest discover -s tests -v
```

The test suite checks:

```text
- Hasse frontier extraction over a downset
- readiness and future monotonicity
- strict same-site incompatible-motif exclusion
- successful commit for a unique certified-ready motif
- depth-indexed finality
```

## Outputs

The included demo run writes:

```text
outputs/ra_causal_dag_demo_summary.csv
outputs/ra_causal_dag_demo_state.json
```

The CSV is a site-level summary. The JSON contains full nodes, edges, depths, motif candidates, and site summaries.
