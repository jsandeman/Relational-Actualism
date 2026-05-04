# RA Causal-DAG Motif-Commit Simulator v0.3 Report

**Date:** May 4, 2026  
**Simulator packet:** `RA_CausalDAG_MotifCommitSimulator_v0_3_May04_2026`  
**Status:** Unit-tested Python simulator extension

## Executive summary

v0.3 adds a selector-closure phase to the v0.2 RA causal-DAG motif-commit simulator.

The key change is conceptual rather than merely computational:

```text
v0.2:
  support certification -> readiness -> strict commit exclusion

v0.3:
  support certification -> readiness -> selector closure -> strict commit exclusion on selected candidates
```

This lets the simulator separate three cases that were conflated under strict commit alone:

1. **unsupported candidate**: fails before readiness;
2. **strict incompatible stalemate**: certified-ready alternatives block each other;
3. **selector-resolved actualization**: a selected compatible subset survives and commits.

## Relation to the compiled Lean layer

The strict path remains the direct Python counterpart of `RA_MotifCommitProtocol.lean`:

- `GraphSupportCertifier.supports` approximates `Γ.supports`;
- `CausalDAG.ready_at` approximates `GraphReadyAt`;
- `MotifCommitProtocol.decision` approximates strict `GraphCommitsAt`.

The selector path is explicitly downstream:

- `SelectorPolicy`
- `SelectorClosureResult`
- `SelectedCommitDecision`

It is not claimed to be part of the compiled Lean module yet.

## Selector modes

### `mode='none'`

All certified-ready motifs are selected. This reproduces strict behavior: incompatible certified-ready candidates remain selected and block each other.

### `mode='greedy', tie_policy='lexicographic'`

Each incompatibility component is narrowed to a deterministic compatible subset. The ordering uses:

```text
higher priority
then smaller support width
then kind rank
then motif name
```

This is useful for simulator experiments but should not be interpreted as a physical RA selector theorem.

### `mode='greedy', tie_policy='stalemate'`

If the top-ranked alternatives are tied before name-breaking and are mutually incompatible, the selector records a stalemate and selects none from that component.

This is the conservative mode for studying unresolved actualization ambiguity.

## Validation

Command:

```bash
cd RA_CausalDAG_MotifCommitSimulator_v0_3_May04_2026
python -m unittest discover -s tests -v
```

Result:

```text
Ran 12 tests in 0.004s
OK
```

The tests cover:

- Hasse-frontier extraction;
- readiness future monotonicity;
- strict incompatible blocking;
- disabled selector equivalence to strict blocking;
- greedy selector resolution by priority;
- stalemate tie policy;
- lexicographic simulator tie-break;
- unsupported competitors not blocking certified motifs;
- Hasse-cut rejection;
- selector component traces;
- depth-indexed finality;
- generated-demo summary fields and selector outputs.

## Demo result

Default command:

```bash
python simulator/ra_causal_dag_simulator.py --run-sweep
```

Default demo:

```text
nodes=25 edges=31 motifs=37
```

Summary:

```text
sites=24
total_strict_committed=324
total_strict_blocked=136
total_selector_committed=392
total_selector_rejected=68
total_selector_stalemates=0
total_unsupported=26
mean_support_width=1.0
last_site=24
```

The selector comparison file shows the key contrast for the same generated run:

```text
selector none:
  total_selector_committed = 324
  total_selector_rejected = 0

selector greedy / lexicographic:
  total_selector_committed = 392
  total_selector_rejected = 68

selector greedy / stalemate:
  total_selector_committed = 324
  total_selector_stalemates = 136
```

Interpretation:

- strict/no-selector mode preserves all certified-ready conflicts and therefore blocks alternatives;
- greedy/lexicographic mode resolves conflicts by simulator tie-break;
- greedy/stalemate refuses to break equal top-rank conflicts and records them as unresolved.

## Main caution

The selector phase is deliberately marked experimental. It is a simulator-level model of how an RA selector might narrow eligible motifs before commit. The next Lean step should not simply import the greedy algorithm; it should formalize a minimal abstract selector relation and prove that selected subsets preserve strict safety.

## Recommended next Lean theorem target

A natural next module would introduce an abstract selector relation:

```lean
Γ.selectsAt x M
```

or a selected predicate over motifs at a site:

```lean
SelectedAt Γ x M
```

Then prove:

```text
selected_commit_safety:
  selected-ready commits cannot include incompatible pairs
```

with the selector constraints kept abstract initially.
