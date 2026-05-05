# RA Support-Family Redundancy Signature Note — v0.7

This note is RA-native. It compares strict single-cut readiness with support-family readiness.

## Scale

- run_count: 100
- steps: 32
- actual_evaluations: 288000
- support_width_classes: [1, 2, 3, 4]
- threshold_fractions: [0.25, 0.5, 0.75, 1.0]

## Interpretation

A wider single support cut is an all-of-n obligation. A support-cut family is a set of alternative sufficient cuts. v0.7 therefore tests when support breadth becomes resilience rather than exposure.

## Highest observed rescue regimes

- mode=frontier_dropout severity=0.25 threshold=0.25: family_rescue_rate=0.560833, strict_loss=1.0, family_loss=0.439167.
- mode=frontier_dropout severity=0.25 threshold=0.5: family_rescue_rate=0.560833, strict_loss=1.0, family_loss=0.439167.
- mode=frontier_dropout severity=0.5 threshold=0.25: family_rescue_rate=0.560833, strict_loss=1.0, family_loss=0.439167.
- mode=edge_dropout severity=0.5 threshold=0.25: family_rescue_rate=0.441667, strict_loss=0.814583, family_loss=0.372917.
- mode=frontier_dropout severity=0.5 threshold=0.5: family_rescue_rate=0.3625, strict_loss=1.0, family_loss=0.6375.
- mode=edge_dropout severity=0.25 threshold=0.25: family_rescue_rate=0.357917, strict_loss=0.76125, family_loss=0.403333.
- mode=edge_dropout severity=0.25 threshold=0.5: family_rescue_rate=0.321667, strict_loss=0.76125, family_loss=0.439583.
- mode=edge_dropout severity=0.75 threshold=0.25: family_rescue_rate=0.308333, strict_loss=0.994167, family_loss=0.685833.

## Methodological caution

The threshold-subfamily construction is a simulator instantiation of the formal support-family bridge. It is not yet a derived physical law. Canonical runs should test whether the structural distinction between single-cut exposure and support-family resilience is robust under alternative family-generation rules.
