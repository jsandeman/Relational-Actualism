
# RA Causal-DAG Motif-Commit Simulator v0.6 Channel-Resolving Redundancy Report

Date: May 05, 2026

## Purpose

v0.6 responds to the v0.5.2 result that `frontier_dropout`, `ledger_failure`, and `orientation_degradation` were observationally degenerate under the earlier loss-vector diagnostics. The new workbench separates the actualization-fragility channels into:

```text
support certification
causal reachability
support availability
operational readiness
strict commitment
selected commitment
ledger-gate loss
orientation-gate loss
selector-stress loss
finality-depth shift
recovery length
```

It also introduces a support-diverse generator so support cuts are not restricted to width one.

## Validation

Python tests passed:

```text
Ran 6 tests
OK
```

The tests verify:

```text
support-diverse generation produces width > 1
frontier dropout is availability loss rather than certification loss
ledger failure is certification loss rather than reachability loss
orientation degradation is graded across an ensemble
frontier/ledger/orientation modes are no longer degenerate
summary contains support-width diversity
```

## Packet demo run

```text
run_count=4
steps=16
actual_evaluations=1440
sampled_evaluations=500
elapsed_seconds=14.49401
evaluations_per_second=99.351385
support_width_classes=[1, 2, 3, 4]
support_width_count=4
```

Loss totals:

```text
support_certification=198
causal_reachability=551
support_availability=192
operational_readiness=726
strict_commit=910
selected_commit=726
```

## Mode signatures

| Mode | Classification | Main separated channel |
|---|---|---|
| edge_dropout | causal_reachability_channel | cert=0.0, reach=0.869792, avail=0.0, ledger=0.0, orient=0.0, selector=0.0 |
| frontier_dropout | frontier_availability_channel | cert=0.0, reach=1.0, avail=1.0, ledger=0.0, orient=0.0, selector=0.0 |
| ledger_failure | ledger_certification_channel | cert=0.515625, reach=0.0, avail=0.0, ledger=0.53125, orient=0.0, selector=0.0 |
| orientation_degradation | orientation_witness_certification_channel | cert=0.515625, reach=0.0, avail=0.0, ledger=0.0, orient=0.53125, selector=0.0 |
| selector_stress | selector_exclusion_channel | cert=0.0, reach=0.0, avail=0.0, ledger=0.0, orient=0.0, selector=0.958333 |
| support_delay | delay_recovery_channel | cert=0.0, reach=1.0, avail=0.0, ledger=0.0, orient=0.0, selector=0.0 |


## Former degeneracy check

| Pair | Euclidean distance | Cosine similarity |
|---|---:|---:|
| frontier_dropout vs ledger_failure | 1.714665 | 0.485531 |
| frontier_dropout vs orientation_degradation | 1.714665 | 0.485531 |
| ledger_failure vs orientation_degradation | 0.751301 | 0.738639 |


The packet demo separates all three formerly degenerate channels. A canonical run should confirm whether this separation remains stable at the 100-seed scale.

## Status

```text
source_status: simulation_packet_validated_no_lean_changes
proof_status: simulation_validated_pending_canonical_v0_6_run
```

## Recommended canonical run

```bash
python scripts/run_channel_resolving_redundancy_v0_6.py   --seed-start 17   --seed-stop 117   --steps 32   --max-targets 20   --sample-limit 5000   --severance-seeds 101,103   --severities 0.0,0.25,0.50,0.75,1.0   --output-dir outputs
```

If runtime becomes high, first reduce `max-targets` to 12–16 before reducing seed count.
