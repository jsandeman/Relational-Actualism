# RA v0.8.1 Certified-Support-Family Correlation Analysis Report

## Status

Analysis-only packet.  No simulator semantics changed.  No Lean module was introduced.

Python validation:

```text
Ran 4 tests
OK
```

## Purpose

v0.8 demonstrated that independent or weakly correlated family-member certification witnesses can rescue ledger/orientation certification failures.  The clean reported canonical signature was:

```text
certificate_correlation:       0.00 -> 0.25 -> 0.50 -> 0.75 -> 1.00
certification_rescue_rate:     0.221 -> 0.176 -> 0.121 -> 0.091 -> 0.000
```

v0.8.1 extracts this into explicit analysis artifacts:

```text
correlation rescue decay curve
monotonicity diagnostics
endpoint equivalence to parent-shared certification
rescue AUC / sensitivity metrics
width- and threshold-conditioned rescue curves
selector guardrail preservation
```

## Packet-local demonstration

The packet-local outputs were generated against the smaller v0.8 demo data shipped in the prior packet.  They are useful for code validation but should not be treated as the canonical scientific result.

Packet-local state:

```text
correlation_decay_rows = 48
sensitivity_rows = 16
endpoint_equivalence_rows = 24
monotone_curves = 15 / 16
selector_guardrail_passed = true
```

The non-canonical demo has limited sample size and coarse correlation points; rerun v0.8.1 on canonical v0.8 outputs before RAKB promotion.

## Interpretation discipline

The analysis preserves the RA-native distinction:

```text
support-route redundancy
  distinct support routes / cuts rescue reachability or availability failures

certification-witness redundancy
  member-distinct certification witnesses rescue ledger/orientation certification failures
```

The correlation parameter remains a simulator control.  The next deeper step is to replace external correlation knobs with RA-native witness-overlap measures.

## Recommended next step after canonical v0.8.1

Proceed to native certificate anchoring:

```text
v0.9 Native Certificate Overlap / BDG-LLC anchoring
```

The central question becomes:

```text
What makes two family-member certification witnesses genuinely distinct in RA-native terms?
```

Candidate overlap channels:

```text
support-cut overlap
Hasse-frontier overlap
orientation-sign-link overlap
native ledger overlap
causal-past overlap
BDG-LLC kernel overlap
causal-firewall / severance exposure overlap
```
