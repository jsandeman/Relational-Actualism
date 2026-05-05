# RA Causal-DAG Motif-Commit Simulator v0.5.1 — Large-Ensemble Optimization Report

## Status

```text
simulation_optimization_validated
```

The v0.5.1 optimizer is additive. It preserves the v0.5 causal-severance semantics and adds a faster ensemble runner.

## Optimization target

v0.5 was intentionally diagnostic-heavy. It built per-site audit tables even when the severance workbench needed only the final DAG/motif state. For larger ensembles, this made repeated seed runs unnecessarily expensive.

v0.5.1 optimizes the large-ensemble path while keeping the original audited v0.5 path available.

## New simulator surface

```text
EnsembleRunConfig
StreamingBuckets
CachedSeedState
generate_growth_state_fast
build_cached_seed_state
evaluate_severance_cached
iter_severance_rows_for_seed
run_large_ensemble
benchmark_fast_vs_audited
```

## Semantic preservation checks

The test suite includes:

```text
fast growth final-state equivalence for a fixed seed
streaming bucket aggregation behavior
large-ensemble output table production
benchmark row production
all prior v0.5 causal-severance tests
```

Validation result:

```text
Ran 20 tests
OK
```

## Demo ensemble

Included run:

```text
run_count = 20
steps = 16
workers = 1
actual_evaluations = 14400
sampled_evaluations = 1000
```

Summary:

```text
evaluations_per_second = 900.561499
total_lost_support = 7477
total_lost_readiness = 9349
total_lost_strict_commit = 11221
total_lost_selected_commit = 9349
```

Wall time including output writing and benchmark:

```text
18.39 s
```

## Benchmark

For seed 17, steps 16, repeats 2:

```text
fast_growth mean_seconds = 0.001307
audited_growth mean_seconds = 0.076061
speedup_fast_vs_audited = 58.195103
```

This benchmark measures final-state generation only, not the entire severance evaluation path.

## RA-native discipline

The optimizer does not introduce external primitives. It accelerates:

```text
candidate motif generation
support/readiness severance evaluation
commitment-loss aggregation
finality/recovery diagnostics
```

The operational vocabulary remains:

```text
candidate motif
causal support cut
oriented support witness
certified readiness
selector closure
selected commitment
causal finality
causal-severance fragility
```

## Caveats

- The v0.5.1 packet is a simulator optimization packet, not a new Lean formalization packet.
- Multiprocess worker sharding is optional; single-worker streaming is the validation baseline used for the included output files.
- `edge_dropout` still requires post-intervention DAG recomputation; support-delay/frontier-dropout and orientation/ledger/selector interventions benefit most from the cache path.
