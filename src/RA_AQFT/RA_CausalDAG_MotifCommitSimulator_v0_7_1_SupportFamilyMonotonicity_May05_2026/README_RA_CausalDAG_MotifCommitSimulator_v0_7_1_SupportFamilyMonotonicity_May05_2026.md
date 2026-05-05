# RA Causal-DAG Motif-Commit Simulator v0.7.1 — Support-Family Monotonicity Audit

This packet follows v0.7.  v0.7 introduced support-cut families and showed that threshold families can rescue support/reachability/availability-channel loss.  It also exposed a subtle distinction: an **exact-k** threshold family may replace the original strict support cut rather than augment it.

v0.7.1 separates three support-family semantics:

```text
exact_k
  all k-subsets of a base support cut.
  This is the v0.7 semantics and need not include the original full cut.

at_least_k
  all subsets of size >= k.
  This includes the original full cut and is monotone as k decreases.

augmented_exact_k
  exact-k subcuts plus the original full cut.
  This is the minimal additive-redundancy repair of exact-k.
```

It also separates two certification regimes:

```text
cut_level
  family member cuts can fail certification independently.

parent_shared
  one parent support certificate gates the strict cut and the whole family.
```

The RA-native point is:

```text
support-cut width
  = all-of-n exposure

exact-k family
  = alternative subcut replacement, not necessarily monotone redundancy

at-least-k / augmented-exact-k family
  = monotone family augmentation at the readiness level
```

## Lean bridge

The packet includes:

```text
lean/RA_MotifSupportFamilyMonotonicity.lean
```

It imports:

```lean
import RA_MotifSupportFamilyBridge
```

and defines:

```text
DAGFamilyIncluded
DAGFamilyAugments
DAGFamilyUnion
DAGFamilyReadyAt.mono_family
DAGCertifiedFamilyReadyAt.mono_family
DAGFamilyCommitsAt.mono_family
DAGFamilyAllReadyAt.mono_subfamily

GraphFamilyIncluded
GraphFamilyAugments
GraphFamilyUnion
GraphFamilyReadyAt.mono_family
GraphCertifiedFamilyReadyAt.mono_family
GraphFamilyCommitsAt.mono_family
GraphFamilyAllReadyAt.mono_subfamily
```

The central theorem family is:

```text
If F is included in F', then readiness/certified-readiness/commitment through F propagates to F'.
```

This bridge is source-level pending local compile in this packet.

## Simulator audit

The new simulator file is:

```text
simulator/ra_causal_dag_support_family_monotonicity.py
```

The run script is:

```bash
python scripts/run_support_family_monotonicity_v0_7_1.py --output-dir outputs
```

Packet-local demo run:

```text
run_count = 4
steps = 16
actual_evaluations = 46,080
support_width_classes = [1,2,3,4]
family_semantics = [at_least_k, augmented_exact_k, exact_k]
certification_regimes = [cut_level, parent_shared]
monotone_semantics_no_worse_violations = 0
total_no_worse_violations = 140
```

The no-worse violations occur only in `exact_k / cut_level`, as expected.

## Validation

Python tests:

```text
Ran 6 tests
OK
```

Source audit:

```text
sorry/admit/axiom = 0
superposition/wavefunction/collapse/quorum/vote/leader/message-round = 0
```

## Recommended canonical run

After installing and compiling the Lean bridge, run:

```bash
python scripts/run_support_family_monotonicity_v0_7_1.py \
  --seed-start 17 \
  --seed-stop 117 \
  --steps 32 \
  --max-targets 12 \
  --sample-limit 5000 \
  --threshold-fractions 1.0,0.75,0.5,0.25 \
  --family-semantics exact_k,at_least_k,augmented_exact_k \
  --certification-regimes cut_level,parent_shared \
  --output-dir outputs
```

The primary success criteria are:

```text
1. at_least_k and augmented_exact_k have zero no-worse violations.
2. exact_k can show no-worse violations under cut_level certification.
3. threshold=1.0 recovers strict single-cut readiness.
4. rescue remains mode-dependent and is not misattributed to selector stress.
5. parent_shared certification separates support-route redundancy from certification-level redundancy.
```
