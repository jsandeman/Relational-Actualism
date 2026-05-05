# RA Causal-DAG Motif-Commit Simulator v0.7.2 — Support-Family Metric Repair Report

## Status

This packet is a metric-repair / audit packet. It does not change the formal support-family semantics, the simulator intervention semantics, or the compiled Lean stack.

```text
formal status: no new Lean
simulation status: packet-local tests passed
RAKB status: proposals included; canonical-run promotion pending
```

## Motivation

The v0.7.1 audit showed that a previous reading of exact-k certification behavior was too coarse. In cut-level certification modes, exact-k families at threshold < 1.0 can omit the original parent support cut. If certification stress samples only from `family.cuts`, then the family members are targeted while the strict parent cut may be untouched.

That creates a metric mismatch:

```text
strict_loss:
  parent support cut loss

family_loss:
  family member loss
```

When the parent cut is absent from the family, these quantities are not automatically comparable.

## Metric repair

v0.7.2 adds four explicit diagnostic layers:

```text
1. target-domain audit
   parent and family are marked as same-domain or different-domain targets.

2. apples-to-apples comparison
   strict-vs-family loss deltas are computed only when the comparison is valid.

3. family-internal resilience
   certification-channel survival is measured inside family.cuts.

4. artifact-risk flagging
   exact-k / cut-level / parent-absent rows are marked as invalid for strict-parent-vs-family loss comparison.
```

## Packet-local validation

```text
Ran 6 tests
OK
```

The tests verify:

```text
cut-level certification with parent absent is flagged as incomparable
parent-shared certification remains comparable
exact-k omits the parent cut when k < width
at-least-k includes the parent cut
demo run produces metric-artifact flags
support-channel comparisons remain valid even when the parent is absent from an exact-k family
```

## Packet-local demo result

```text
actual_evaluations=46,080
support_width_classes=[1,2,3,4]
comparison_valid_rate=0.989149
metric_artifact_risk_rate=0.008681
strict_parent_losses=26,917
family_internal_losses=25,618
strict_rescues=1,439
family_internal_resilience_events=5,102
```

## Corrected interpretation

The v0.7 / v0.7.1 certification result should be read as:

```text
Certification-channel comparisons require width-stratified and parent-in-family-aware metrics.
```

The corrected claim is not:

```text
exact-k support families structurally amplify certification failure.
```

The corrected claim is:

```text
strict-parent rescue, family-internal survival, and apples-to-apples loss delta are distinct diagnostics.
```

## Scientific value

This repair improves the workbench without weakening the support-family program. It clarifies that support-family redundancy is channel-specific:

```text
support/reachability/availability channels:
  strict-rescue metrics are meaningful

certification channels:
  family-internal survival and certificate-targeting domains must be tracked

selector channels:
  not a support-family rescue channel
```

## Recommended canonical run

```bash
python scripts/run_support_family_metric_repair_v0_7_2.py \
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
