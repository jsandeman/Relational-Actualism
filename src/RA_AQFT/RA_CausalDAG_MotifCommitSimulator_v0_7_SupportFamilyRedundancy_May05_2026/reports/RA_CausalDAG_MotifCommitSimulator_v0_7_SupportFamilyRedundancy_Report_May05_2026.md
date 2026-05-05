# RA Causal-DAG Motif-Commit Simulator v0.7 — Support-Family Redundancy Report

## Purpose

v0.7 follows the canonical v0.6 finding that support-frontier width is not itself redundancy under strict all-support readiness. The v0.7 packet introduces support-cut families as a separate RA-native abstraction.

## Formal bridge

The Lean bridge:

```text
lean/RA_MotifSupportFamilyBridge.lean
```

defines:

```text
DAGSupportCutFamily
DAGSingletonSupportCutFamily
DAGFamilyReadyAt
DAGFamilyAllReadyAt
DAGCertifiedFamilyReadyAt
DAGFamilyCommitsAt
GraphSupportCutFamily
GraphSingletonSupportCutFamily
GraphFamilyReadyAt
GraphFamilyAllReadyAt
GraphCertifiedFamilyReadyAt
GraphFamilyCommitsAt
```

and theorems including:

```text
DAGFamilyReadyAt_singleton_iff
GraphFamilyReadyAt_singleton_iff
DAGFamilyReadyAt.future_mono
GraphFamilyReadyAt.future_mono
DAGFamilyCommitsAt.certified_family_ready
GraphFamilyCommitsAt.certified_family_ready
```

This bridge is source-level pending local compile.

## Simulator instantiation

The simulator uses threshold support families. For a base support cut of width `n`, threshold `k=ceil(fraction*n)` yields all `k`-element subcuts. Family readiness holds when some member cut is ready and certified.

This separates:

```text
strict single-cut readiness:
  all vertices in Q must be ready

family readiness:
  some certified Qᵢ in F must be ready
```

## Validation

Python validation:

```text
Ran 7 tests
OK
```

Test coverage includes:

```text
threshold-k bounds
singleton threshold recovers strict semantics
threshold family rescues strict reachability loss
support-diverse generation exposes width > 1
selector stress is not miscounted as support-family rescue
end-to-end output generation
```

## Demo result

```text
actual_evaluations=1920
support_width_classes=[1, 4]
total_strict_readiness_losses=1160
total_family_readiness_losses=1140
total_family_rescues=44
```

The demo is small and should not be promoted as canonical science. It verifies that the v0.7 workbench distinguishes strict-cut loss from support-family rescue.

## Interpretation

The key conceptual move is:

```text
width of one cut ≠ redundancy
family of alternative cuts = redundancy candidate
```

This preserves the v0.6 result while opening a new testable question: under which RA-native support-family semantics does support breadth become resilience rather than exposure?

## Recommended canonical run

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

## RAKB status

Active-schema proposal files are included under `registry_proposals/`. They should be applied manually after canonical v0.7 outputs are generated and reviewed. Do not promote packet-local demo results as canonical.
