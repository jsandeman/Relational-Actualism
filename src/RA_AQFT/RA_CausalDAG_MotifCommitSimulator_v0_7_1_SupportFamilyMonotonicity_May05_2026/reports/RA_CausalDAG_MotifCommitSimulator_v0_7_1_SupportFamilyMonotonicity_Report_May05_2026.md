# RA Causal-DAG Motif-Commit Simulator v0.7.1 — Support-Family Monotonicity Report

## Purpose

v0.7 established that support-cut families can rescue support/reachability/availability-channel failure.  It also revealed that exact-threshold support families can sometimes worsen certification-channel fragility.  v0.7.1 audits this by separating exact-k replacement from monotone family augmentation.

## Formal bridge

`RA_MotifSupportFamilyMonotonicity.lean` defines family inclusion and proves that any-cut readiness, certified family readiness, and family commitment are monotone under family inclusion.

This is the formal version of the slogan:

```text
If a support family is augmented by adding cuts, any existing readiness witness remains available.
```

## Simulator semantics

The simulator compares:

```text
exact_k
  k-sized subcuts only; may exclude the original strict cut.

at_least_k
  all cuts of size >= k; always includes the original strict cut.

augmented_exact_k
  exact-k subcuts plus the original strict cut.
```

and:

```text
cut_level certification
  individual family cuts can fail certification.

parent_shared certification
  one parent certificate gates the strict cut and all family cuts.
```

## Packet-local validation

```text
Ran 6 tests
OK
```

## Packet-local demo summary

```text
run_count = 4
steps = 16
actual_evaluations = 46,080
evaluations_per_second ≈ 16,553
support_width_classes = [1, 2, 3, 4]
total_strict_losses = 26,917
total_family_losses = 25,618
total_family_rescues = 1,439
total_no_worse_violations = 140
monotone_semantics_no_worse_violations = 0
```

## Interpretation

The packet-local result supports the expected distinction:

```text
exact_k / cut_level
  can violate no-worse behavior because the original strict cut may be absent.

at_least_k and augmented_exact_k
  have zero no-worse violations in this demo because they include the original strict cut.
```

Thus, v0.7.1 repairs the ambiguity in the term "redundancy": true additive support-family redundancy requires family inclusion or an equivalent monotone augmentation relation.

## Status

This is a simulator-analysis and source-level formal bridge packet.  It does not modify the BDG-LLC foundation and does not introduce inherited-theory apparatus.  Concrete support-family certification remains downstream of BDG-LLC / frontier / orientation / ledger evidence.
