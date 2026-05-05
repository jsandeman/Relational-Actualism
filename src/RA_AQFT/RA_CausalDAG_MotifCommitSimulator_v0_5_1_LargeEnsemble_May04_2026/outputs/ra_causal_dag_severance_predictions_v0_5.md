# RA Causal-Severance Prediction Note — Simulator v0.5

This note states RA-native diagnostics only. It does not treat any inherited theory as the target.

## Workbench predicates

- support loss: orientation/ledger/support certification no longer holds after intervention.
- readiness loss: the required support cut no longer reaches the tested site, or its availability is delayed beyond the tested site.
- commitment loss: a motif that committed before the intervention no longer commits after it.
- recovery length: the first later depth at which the same support cut is again ready, when such a depth exists in the finite run.

## Observed support-width classes

Observed support widths in this run: [1].

## Highest-loss intervention settings

- mode=edge_dropout, severity=0.5: strict_commit_loss_rate=1.0, readiness_loss_rate=1.0, support_loss_rate=1.0.
- mode=edge_dropout, severity=1.0: strict_commit_loss_rate=1.0, readiness_loss_rate=1.0, support_loss_rate=1.0.
- mode=frontier_dropout, severity=0.5: strict_commit_loss_rate=1.0, readiness_loss_rate=1.0, support_loss_rate=1.0.
- mode=frontier_dropout, severity=1.0: strict_commit_loss_rate=1.0, readiness_loss_rate=1.0, support_loss_rate=1.0.
- mode=ledger_failure, severity=0.5: strict_commit_loss_rate=1.0, readiness_loss_rate=1.0, support_loss_rate=1.0.

## RA-native prediction families to track

1. Frontier-width fragility: narrower support cuts should show higher loss rates under frontier dropout when support redundancy is absent.
2. Reachability/certification separation: edge and frontier interventions should primarily alter readiness, while orientation and ledger interventions should primarily alter support certification.
3. Delay-induced finality shift: support delay should preserve recoverability when the support remains connected, but move readiness/finality deeper into the causal future.
4. Selector-stress ambiguity: increasing certified incompatible alternatives should alter selected commitment without necessarily damaging support readiness.

These are simulator diagnostics, not empirical claims. Their role is to sharpen RA-native prediction language before physical correspondence tests are proposed.
