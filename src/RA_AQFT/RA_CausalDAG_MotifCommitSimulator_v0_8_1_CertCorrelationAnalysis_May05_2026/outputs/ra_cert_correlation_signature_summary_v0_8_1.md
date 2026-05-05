# RA v0.8.1 Certified-Support-Family Correlation Signature Analysis

This analysis packet consumes v0.8 Independent Certified Support Families outputs and extracts the RA-native certification-correlation signature.

## Scope

- Analysis-only packet: no simulator semantic changes and no new Lean module.
- Target quantities: certification rescue, family-internal certification resilience, endpoint equivalence, and selector-stress guardrail preservation.
- Nature-target discipline: these are RA-native simulation diagnostics, not direct claims about Nature.

## Top-line diagnostics

- Correlation decay curves analyzed: **64**
- Monotone non-increasing curves: **61/64**
- Endpoint equivalence rows: **32/80** within tolerance `1e-09`
- Maximum endpoint delta: **0.115834**
- Selector-stress guardrail passed: **yes**

## Highest rescue-decay curves

- orientation_degradation / at_least_k / severity=0.75 / threshold=0.25: 0.319167 → 0 (decay=0.319167, monotone=true)
- ledger_failure / at_least_k / severity=0.75 / threshold=0.25: 0.312917 → 0 (decay=0.312917, monotone=true)
- orientation_degradation / at_least_k / severity=0.75 / threshold=0.5: 0.300833 → 0 (decay=0.300833, monotone=true)
- orientation_degradation / augmented_exact_k / severity=0.75 / threshold=0.5: 0.289167 → 0 (decay=0.289167, monotone=true)
- orientation_degradation / at_least_k / severity=0.5 / threshold=0.25: 0.264583 → 0 (decay=0.264583, monotone=true)
- orientation_degradation / augmented_exact_k / severity=0.5 / threshold=0.25: 0.261667 → 0 (decay=0.261667, monotone=true)
- orientation_degradation / augmented_exact_k / severity=0.75 / threshold=0.25: 0.25875 → 0 (decay=0.25875, monotone=true)
- ledger_failure / at_least_k / severity=0.75 / threshold=0.5: 0.252917 → 0 (decay=0.252917, monotone=true)

## Rescue AUC by mode and family semantics

- ledger_failure / at_least_k: mean rescue AUC=0.0494791, mean decay=0.0968751, all monotone=true
- ledger_failure / augmented_exact_k: mean rescue AUC=0.0461556, mean decay=0.0894011, all monotone=true
- orientation_degradation / at_least_k: mean rescue AUC=0.0487305, mean decay=0.0999479, all monotone=false
- orientation_degradation / augmented_exact_k: mean rescue AUC=0.0444173, mean decay=0.0941927, all monotone=false

## Interpretation

The core v0.8 signature is strengthened when certification rescue is monotone non-increasing as certificate-correlation increases, and when the correlation=1.0 endpoint matches the parent-shared certification shape.  That pattern supports the RA-native distinction between support-route redundancy and certification-witness redundancy.

The main structural hypothesis is:

```text
member-distinct / weakly correlated certification witnesses
  → certification-channel resilience

fully shared certification fate
  → parent-shared failure shape
```

The analysis should be rerun on canonical v0.8 outputs before RAKB promotion. Packet-local outputs are demonstration artifacts unless explicitly replaced by canonical-run outputs.
