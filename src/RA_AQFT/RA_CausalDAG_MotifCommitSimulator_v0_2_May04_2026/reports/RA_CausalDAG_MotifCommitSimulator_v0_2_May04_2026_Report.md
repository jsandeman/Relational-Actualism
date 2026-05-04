# RA Causal-DAG Motif-Commit Simulator v0.2 Report — May 4, 2026

## Purpose

This packet advances the causal-DAG simulator from the v0.1 strict commit predicate to a first concrete simulator-level interpretation of the Lean relation:

```text
Γ.supports M Q
```

The goal is to prevent the simulation from treating arbitrary finite support cuts as valid evidence. Instead, a support cut must be certified before it can participate in readiness, commit, or incompatibility exclusion.

## What changed from v0.1

v0.1 used:

```text
supports(M, Q) := M.certified and M.support_cut == Q
```

v0.2 adds:

```text
GraphSupportCertifier
SupportGateResult
SupportEvaluation
support-failure diagnostics
support-evaluation CSV output
parameter sweep output
```

The new certifier checks:

```text
motif_certified_flag
known_carrier_vertices
known_support_vertices
support_cut_matches_declared
empty_support_allowed
candidate_past_declared
candidate_past_vertices_known
candidate_past_down_closed
support_cut_is_hasse_frontier
support_reaches_carrier
bdg_local_gate
ledger_local_gate
orientation_closure_gate
```

Optional experimental bounds are also available:

```text
support_width_bound
support_depth_span_bound
```

## RA interpretation

The important structural point is this:

```text
support_cut_of_finite_hasse_frontier(P)
```

is no longer just a data-construction. In v0.2, it is part of a certification path:

```text
declared candidate past
  → down-closed check
  → finite Hasse frontier extraction
  → support cut equality
  → carrier reachability
  → BDG / ledger / orientation gates
  → Γ.supports M Q
```

This is closer to the context-gated Lean semantics of `RA_MotifCommitProtocol`, where commit requires both readiness and certified support.

## Demo run

Command:

```bash
python simulator/ra_causal_dag_simulator.py \
  --steps 24 \
  --seed 17 \
  --conflict-rate 0.30 \
  --defect-rate 0.12 \
  --run-sweep
```

Observed output:

```text
nodes=25 edges=31 motifs=37
summary={'sites': 24, 'total_committed': 324, 'total_blocked': 136, 'total_unsupported': 26, 'mean_support_width': 1.0, 'last_site': 24}
sweep_rows=48
```

The final site showed:

```text
site=24
depth=24
support_cut=[23]
supported_count=35
unsupported_count=2
committed_count=25
blocked_count=10
support_failure_histogram={'ledger_local_gate': 1, 'orientation_closure_gate': 1}
```

## Parameter sweep observation

The included sweep varies conflict rate and defect rate across four seeds. A useful qualitative behavior appears:

- Higher conflict rate increases blocked-ready motifs when support certification is clean.
- Higher defect rate increases unsupported motifs.
- Defective alternatives may reduce blocking, because uncertified competitors do not participate in commit exclusion.

This last point is important: support certification is not merely stricter. It changes the exclusion ecology. A malformed competitor can fail out before it blocks a well-supported motif.

## Validation

Tests run in the assistant container:

```text
python -m unittest discover -s tests -v
Ran 11 tests in 0.012s
OK
```

The tests cover:

```text
Hasse-frontier extraction
readiness and future monotonicity
support certification success
non-Hasse support rejection
ledger-gate rejection
mutual blocking of certified incompatible motifs
non-blocking by uncertified competitors
unique certified-ready commit
depth finality
demo generation
parameter sweep generation
v0.1 default context compatibility
```

## Remaining limitations

The BDG, ledger, and orientation gates are explicit metadata gates. They are not yet derived from RA arithmetic, incidence closure, orientation closure, or selector closure.

The simulator still uses a simple default incompatibility relation based on `exclusion_domain`. This is useful for testing strict safety behavior, but it is not yet tied to `RA_GraphOrientationClosure` or a boundary ledger.

The simulator does not yet implement merge-compatible motif composition or selector-closure narrowing.

## Recommended next step

Add a selector-closure mode after support certification:

```text
certified candidates
  → ready candidates
  → selector closure narrows incompatible alternatives
  → strict commit rule evaluates on selected set
```

That would let the simulator distinguish two cases that are currently conflated:

1. true stalemate: two certified-ready incompatible motifs remain available;
2. selected actualization: an RA-native selector has narrowed the candidate set before commit.
