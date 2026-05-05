# RA Channel-Separated Severance Signature Note — v0.6

This note is RA-native. It reports simulator signatures for separated actualization-fragility channels.

## Scale

- run_count: 100
- steps: 32
- actual_evaluations: 72000
- support_width_classes: [1, 2, 3, 4]

## Mode classifications

- edge_dropout: causal_reachability_channel (support_cert=0.0, causal_reach=0.880417, availability=0.0, ledger=0.0, orientation=0.0, selector=0.0).
- frontier_dropout: frontier_availability_channel (support_cert=0.0, causal_reach=1.0, availability=1.0, ledger=0.0, orientation=0.0, selector=0.0).
- ledger_failure: ledger_certification_channel (support_cert=0.564375, causal_reach=0.0, availability=0.0, ledger=0.588333, orientation=0.0, selector=0.0).
- orientation_degradation: orientation_witness_certification_channel (support_cert=0.564375, causal_reach=0.0, availability=0.0, ledger=0.0, orientation=0.588333, selector=0.0).
- selector_stress: selector_exclusion_channel (support_cert=0.0, causal_reach=0.0, availability=0.0, ledger=0.0, orientation=0.0, selector=0.96).
- support_delay: delay_recovery_channel (support_cert=0.0, causal_reach=1.0, availability=0.0, ledger=0.0, orientation=0.0, selector=0.0).

## Separability check

- zero-distance mode pairs: 0.
- nearest pairs:
  - edge_dropout vs support_delay: distance=0.715432, cosine=0.936426.
  - ledger_failure vs orientation_degradation: distance=0.832029, cosine=0.734088.
  - edge_dropout vs frontier_dropout: distance=1.049739, cosine=0.848378.
  - edge_dropout vs ledger_failure: distance=1.288144, cosine=0.55565.
  - edge_dropout vs orientation_degradation: distance=1.288144, cosine=0.55565.

## Interpretation

v0.6 separates support certification, causal reachability, support availability, and selector exclusion. Therefore a high commitment-loss rate no longer compresses distinct severance modes into a single undiagnosed failure channel.

The support-diverse generator also exposes frontier widths greater than one, enabling support-width fragility analysis that was blocked in the v0.5.1/v0.5.2 ensembles.
