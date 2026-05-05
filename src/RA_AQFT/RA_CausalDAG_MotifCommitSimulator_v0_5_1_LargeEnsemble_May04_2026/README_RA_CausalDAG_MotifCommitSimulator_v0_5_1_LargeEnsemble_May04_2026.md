# RA Causal-DAG Motif-Commit Simulator v0.5.1 — Large-Ensemble Optimization

This packet extends simulator v0.5 without changing its RA-native severance semantics.

v0.5.1 is an optimization layer for larger causal-severance ensembles. It keeps the existing ladder:

```text
candidate motif
  → finite Hasse-frontier support cut
  → graph-oriented support witness
  → orientation-gated support certification
  → causal readiness
  → strict / selected commitment
  → causal-severance intervention
  → support/readiness/commitment/finality survival diagnostics
```

## What changed

v0.5's audited growth generator records per-site support, selector, orientation, and conflict rows. Those audit tables are valuable for single-run inspection, but the severance workbench only needs the final DAG and motif family.

v0.5.1 adds:

```text
generate_growth_state_fast
CachedSeedState
evaluate_severance_cached
StreamingBuckets
EnsembleRunConfig
run_large_ensemble
```

The optimizations are:

1. **Fast final-state generation**: builds the same final DAG/motif state as the audited generator, but skips unused per-site audit tables.
2. **Per-seed support cache**: reuses baseline support evaluations and finality-depth values across severance interventions.
3. **Short-circuit support-delay/frontier-dropout cases**: avoids rebuilding an unchanged post-intervention protocol when the v0.5 logic only adjusts support availability or delay.
4. **Streaming aggregation**: aggregates ensemble summaries without retaining every severance row in memory.
5. **Bounded deterministic row sampling**: keeps a reproducible sample of evaluations for audit while permitting larger ensembles.
6. **Optional worker sharding**: independent seed shards can be evaluated with `--workers N`.

No inherited-theory apparatus is introduced. The operational layer remains RA-native.

## Run tests

```bash
python -m unittest discover -s tests -v
```

Expected result in this packet:

```text
Ran 20 tests
OK
```

## Run the large-ensemble demo

From the packet root:

```bash
python scripts/run_large_ensemble_v0_5_1.py \
  --seed-start 17 \
  --seed-stop 37 \
  --steps 16 \
  --max-targets 12 \
  --sample-limit 1000 \
  --benchmark-repeats 2
```

Default output files:

```text
outputs/ra_causal_dag_ensemble_summary_v0_5_1.csv
outputs/ra_causal_dag_ensemble_runs_v0_5_1.csv
outputs/ra_causal_dag_ensemble_aggregate_v0_5_1.csv
outputs/ra_causal_dag_ensemble_fragility_v0_5_1.csv
outputs/ra_causal_dag_ensemble_evaluations_sample_v0_5_1.csv
outputs/ra_causal_dag_ensemble_predictions_v0_5_1.md
outputs/ra_causal_dag_ensemble_state_v0_5_1.json
outputs/ra_causal_dag_ensemble_benchmark_v0_5_1.csv
```

## Demo scale in this packet

The included demo uses:

```text
run_count = 20
steps = 16
actual_evaluations = 14400
sampled_evaluations = 1000
workers = 1
```

Observed demo throughput in this container:

```text
evaluations_per_second ≈ 900.56
wall time ≈ 18.39 s including CSV/JSON/benchmark writing
```

The fast growth-state benchmark in this run reports:

```text
fast_growth mean ≈ 0.001307 s
audited_growth mean ≈ 0.076061 s
speedup ≈ 58.2× for final-state generation
```

The exact throughput on the user machine will vary, but the important structural improvement is that large ensembles no longer pay the per-site audit-table cost.

## Compatibility

This packet includes the original v0.5 simulator, Lean severance bridge, and tests. The v0.5.1 optimizer is additive:

```text
simulator/ra_causal_dag_simulator.py      # original v0.5 semantic core
simulator/ra_causal_dag_ensemble.py       # new v0.5.1 ensemble optimizer
```

## RAKB note

This is primarily a simulator engineering / ensemble-scaling packet. It does not require a new Lean module. Suggested RAKB treatment is either:

```text
simulation_validated / packet_provenance artifact update
```

or a small simulator claim if you want to record the new large-ensemble workbench surface explicitly.
