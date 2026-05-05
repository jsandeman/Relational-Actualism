# RA Support-Family Monotonicity Audit — v0.7.1

This note is RA-native.  It distinguishes exact-threshold family replacement from monotone family augmentation.

## Scale

- run_count: 100
- steps: 32
- actual_evaluations: 1728000
- support_width_classes: [1, 2, 3, 4]
- family_semantics: ['at_least_k', 'augmented_exact_k', 'exact_k']
- certification_regimes: ['cut_level', 'parent_shared']

## Monotonicity reading

Exact-k support families may remove the original strict support cut.  At-least-k and augmented-exact-k families include the strict cut and therefore implement additive support-family augmentation at the readiness level.

- total_no_worse_violations: 9888
- monotone_semantics_no_worse_violations: 0

## Highest rescue regimes

- semantics=at_least_k regime=cut_level mode=frontier_dropout severity=0.25 threshold=0.25: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.
- semantics=at_least_k regime=cut_level mode=frontier_dropout severity=0.25 threshold=0.5: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.
- semantics=at_least_k regime=cut_level mode=frontier_dropout severity=0.5 threshold=0.25: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.
- semantics=at_least_k regime=parent_shared mode=frontier_dropout severity=0.25 threshold=0.25: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.
- semantics=at_least_k regime=parent_shared mode=frontier_dropout severity=0.25 threshold=0.5: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.
- semantics=at_least_k regime=parent_shared mode=frontier_dropout severity=0.5 threshold=0.25: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.
- semantics=augmented_exact_k regime=cut_level mode=frontier_dropout severity=0.25 threshold=0.25: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.
- semantics=augmented_exact_k regime=cut_level mode=frontier_dropout severity=0.25 threshold=0.5: rescue=0.560833 strict_loss=1.0 family_loss=0.439167 no_worse=0.0.

## Non-monotone regimes

- semantics=exact_k regime=cut_level mode=ledger_failure severity=1.0 threshold=0.25: no_worse_violation_rate=0.560833 family_loss=1.0 strict_loss=0.439167.
- semantics=exact_k regime=cut_level mode=ledger_failure severity=1.0 threshold=0.5: no_worse_violation_rate=0.560833 family_loss=1.0 strict_loss=0.439167.
- semantics=exact_k regime=cut_level mode=orientation_degradation severity=1.0 threshold=0.25: no_worse_violation_rate=0.560833 family_loss=1.0 strict_loss=0.439167.
- semantics=exact_k regime=cut_level mode=orientation_degradation severity=1.0 threshold=0.5: no_worse_violation_rate=0.560833 family_loss=1.0 strict_loss=0.439167.
- semantics=exact_k regime=cut_level mode=ledger_failure severity=0.75 threshold=0.25: no_worse_violation_rate=0.3775 family_loss=0.816667 strict_loss=0.439167.
- semantics=exact_k regime=cut_level mode=ledger_failure severity=0.75 threshold=0.5: no_worse_violation_rate=0.3775 family_loss=0.816667 strict_loss=0.439167.
- semantics=exact_k regime=cut_level mode=orientation_degradation severity=0.75 threshold=0.25: no_worse_violation_rate=0.3775 family_loss=0.816667 strict_loss=0.439167.
- semantics=exact_k regime=cut_level mode=orientation_degradation severity=0.75 threshold=0.5: no_worse_violation_rate=0.3775 family_loss=0.816667 strict_loss=0.439167.

## Methodological caution

The simulator comparison is diagnostic.  The formal monotonicity theorem applies to family inclusion; concrete support-family certification still has to be justified by BDG-LLC / frontier / orientation / ledger evidence.
