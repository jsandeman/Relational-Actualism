# v1.7 packet-local keying-ablation demo findings

The packet-local run used the same small matched subset as v1.6:

- seeds 17..20
- severance seed 101
- modes: ledger_failure, orientation_degradation, selector_stress
- severity: 0.5
- threshold_fraction: 0.5
- family semantics: at_least_k, augmented_exact_k
- six orientation keyings

The demo is diagnostic, not canonical.

## Main packet-local finding

The negative/reversed orientation-degradation low-minus-high gaps persist across all tested keyings in this tiny subset. Removing `member_idx` does not restore the v1.5-style positive orientation-specificity signal in this subset.

However, keying choice changes the residual/partial-correlation surface. Member-indexed keying produces weaker residual structure than several non-member keyings, so v1.7 still supports moving away from member-indexed tokens for any future canonical matched-graph analysis.

## Key caution

The specificity bins still contain only four per-cell rows in this packet-local diagnostic. The result should be treated as keying-forensic evidence, not as a robust canonical conclusion.
