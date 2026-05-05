# RA Causal-DAG Motif-Commit Simulator v0.7 — Support-Family Redundancy

This packet introduces a **support-family redundancy workbench** downstream of the v0.6 channel-resolving support-width workbench.

v0.6 showed that a wider single Hasse-frontier support cut is not automatically redundancy. Under strict `GraphReadyAt` semantics, every vertex in one support cut is required; width is a conjunctive support burden. v0.7 therefore introduces a separate RA-native object:

```text
support-cut family
```

A support-cut family is a family of alternative sufficient support cuts for the same motif. In this simulator packet, the concrete instantiation is a threshold subfamily: for a base support cut of width `n`, a threshold `k` family contains all `k`-subsets of that support cut. Family readiness holds when at least one certified member cut is ready.

## RA-native ladder

```text
single support cut
  → all vertices in Q are required
  → width is exposure / coordination burden

support-cut family
  → one certified ready cut in F suffices
  → alternative cuts can provide true redundancy
```

## Files

```text
lean/RA_MotifSupportFamilyBridge.lean
simulator/ra_causal_dag_support_family_workbench.py
scripts/run_support_family_redundancy_v0_7.py
tests/test_v0_7_support_family.py
outputs/*.csv, *.md, *.json
reports/*
registry_proposals/*
```

## Validation

Python tests:

```text
Ran 7 tests
OK
```

Source audit:

```text
sorry/admit/axiom: 0
superposition/wavefunction/collapse/quorum/vote/leader/message-round: 0
```

The Lean bridge is source-level pending local compile in this container. It imports only:

```lean
import RA_MotifCommitProtocol
```

and defines abstract support-family semantics without changing the compiled motif-commit stack.

## Packet-local demo

Included demo command:

```bash
python scripts/run_support_family_redundancy_v0_7.py \
  --seed-start 17 \
  --seed-stop 19 \
  --steps 8 \
  --max-targets 4 \
  --sample-limit 100 \
  --output-dir outputs
```

Demo summary:

```text
actual_evaluations=1920
support_width_classes=[1, 4]
threshold_fractions=[0.25, 0.5, 0.75, 1.0]
total_strict_readiness_losses=1160
total_family_readiness_losses=1140
total_family_rescues=44
```

## Canonical run suggestion

After installing the packet, run:

```bash
python scripts/run_support_family_redundancy_v0_7.py \
  --seed-start 17 \
  --seed-stop 117 \
  --steps 32 \
  --max-targets 12 \
  --sample-limit 5000 \
  --threshold-fractions 1.0,0.75,0.5,0.25 \
  --output-dir outputs
```

Main success criteria:

```text
1. threshold=1.0 recovers strict single-cut readiness.
2. threshold<1.0 can rescue strict readiness loss under partial support loss.
3. rescue rates are mode-dependent, not universal.
4. selector_stress is not counted as support-family rescue.
5. support-family resilience improves only where the failure channel is support/reachability/certification-local.
```

## Methodological caution

The threshold-subfamily construction is a simulator instantiation of the support-family bridge, not yet a derived RA law. Concrete support families must ultimately be justified by BDG-LLC / finite-frontier / orientation / ledger / native-closure evidence.
