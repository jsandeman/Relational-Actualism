# RA Large-Ensemble Causal-Severance Note — v0.5.1

This note is RA-native. It reports support/readiness/commitment/finality diagnostics over a seed ensemble.

## Ensemble scale

- run_count: 100
- actual_evaluations: 120000
- sampled_evaluations: 5000
- evaluations_per_second: 1995.704287

## Highest-loss settings

- mode=edge_dropout, severity=0.5: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.
- mode=edge_dropout, severity=0.75: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.
- mode=edge_dropout, severity=1.0: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.
- mode=frontier_dropout, severity=0.25: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.
- mode=frontier_dropout, severity=0.5: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.
- mode=frontier_dropout, severity=0.75: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.
- mode=frontier_dropout, severity=1.0: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.
- mode=ledger_failure, severity=0.25: support_loss_rate=0.971, readiness_loss_rate=0.971, strict_commit_loss_rate=0.971, selected_commit_loss_rate=0.971.

## Ensemble-level diagnostics to track

1. Certification/readiness separation: orientation and ledger interventions should primarily move support certification, while edge/frontier interventions should primarily move reachability/readiness.
2. Support-width fragility: frontier-dropout rates should stratify by support width when redundant support is present.
3. Delay/recovery relation: support delay should move finality/recovery diagnostics without necessarily destroying support certification.
4. Selector-stress response: selector stress should alter selected commitment while leaving support/readiness diagnostics largely intact.

These are simulator diagnostics for RA actualization dynamics; physical correspondence tests remain separate tasks.
