# RA Causal-DAG Motif-Commit Simulator v0.3

**Date:** May 4, 2026  
**Status:** Python simulator extension; unit-tested in container  
**Upstream formal anchor:** `RA_MotifCommitProtocol.lean` compile-confirmed by user-local Lean environment

## Purpose

v0.3 extends the v0.2 causal-DAG motif-commit simulator with a downstream **selector-closure layer**.

The strict simulator path remains aligned with the compiled Lean predicate:

```text
CommitsAt(M,Q,x) iff
  Γ.supports M Q
  and Q is ready at x
  and no certified-ready incompatible motif competes at x.
```

The selector-closed path adds an experimental layer:

```text
certified-ready motifs at x
  -> selector closure narrows incompatible alternatives
  -> strict commit predicate is evaluated on the selected set
```

This lets the simulator distinguish:

- strict stalemate: incompatible certified-ready motifs block each other;
- selector-resolved actualization: a selected compatible subset remains;
- selector stalemate: a tie remains unresolved without an admissible selector witness.

## Files

```text
simulator/ra_causal_dag_simulator.py
simulator/run_demo.py
scripts/run_selector_comparison.py
tests/test_ra_causal_dag_simulator.py
outputs/ra_causal_dag_demo_summary_v0_3.csv
outputs/ra_causal_dag_support_evaluations_v0_3.csv
outputs/ra_causal_dag_selector_components_v0_3.csv
outputs/ra_causal_dag_parameter_sweep_v0_3.csv
outputs/ra_causal_dag_selector_comparison_v0_3.csv
outputs/ra_causal_dag_demo_state_v0_3.json
patches/patch_ra_causal_dag_simulator_v0_2_to_v0_3.diff
reports/RA_CausalDAG_MotifCommitSimulator_v0_3_May04_2026_Report.md
```

## New concepts in v0.3

### `SelectorPolicy`

A downstream selector over certified-ready candidates.

Modes:

```text
none
  Selects every eligible motif. This reproduces strict v0.2 blocking.

greedy
  Builds a deterministic compatible subset from each incompatibility component.
```

Tie policies:

```text
lexicographic
  Uses priority, support width, kind rank, and name as a deterministic simulator tie-break.

stalemate
  Refuses to name-break tied top-ranked incompatible candidates and records a selector stalemate.
```

The lexicographic tie-break is a simulator convenience, not an RA theorem.

### `SelectorClosureResult`

Records the eligible, selected, rejected, and stalemated candidates at a site.

### `SelectedCommitDecision`

Records the commit decision after selector closure has narrowed the eligible candidate set.

## Validation

The included tests were run with:

```bash
python -m unittest discover -s tests -v
```

Result:

```text
Ran 12 tests
OK
```

The default demo was run with:

```bash
python simulator/ra_causal_dag_simulator.py --run-sweep
```

Default demo summary:

```text
nodes=25 edges=31 motifs=37
summary={
  'sites': 24,
  'total_strict_committed': 324,
  'total_strict_blocked': 136,
  'total_selector_committed': 392,
  'total_selector_rejected': 68,
  'total_selector_stalemates': 0,
  'total_unsupported': 26,
  'mean_support_width': 1.0,
  'last_site': 24
}
```

The compact parameter sweep produced 32 rows.

## Interpretation

v0.3 does not change the strict Lean-aligned commit semantics. It adds a downstream experimental selector phase to ask:

> If RA selector closure narrows the eligible frontier first, which previously blocked alternatives can actualize without violating strict incompatible-commit exclusion?

This is the clean simulator bridge toward `RA_ActualizationSelector`-style modeling.
