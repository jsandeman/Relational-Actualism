# Simulator v0.5 ↔ Lean Causal-Severance Bridge

Simulator v0.5 clarifies which predicates should be formalized in the next Lean bridge, tentatively named:

```lean
RA_MotifCausalSeveranceBridge.lean
```

## Suggested Lean surface

```lean
GraphCausalSeveranceProfile
GraphReadyAtAfterSeverance
GraphSupportCutDestroyedAt
GraphSupportCutDelayedAt
GraphSupportCertificationLostAt
GraphCommitSurvivesSeverance
GraphCommitLostUnderSeverance
GraphFinalityDepthShift
GraphReadinessRecoveryLength
```

## Minimal first theorems

```text
1. If every support vertex still reaches the site after severance, readiness survives.
2. If a required support vertex is dropped, readiness fails for that support cut.
3. If support certification is lost, selected commitment cannot be established through that support witness.
4. If support delay is finite and a later site receives every support vertex, readiness can recover at that later site.
```

## Simulator-to-Lean mapping

| Simulator v0.5 | Lean bridge target |
|---|---|
| `CausalSeveranceIntervention` | `GraphCausalSeveranceProfile` |
| `edge_dropout` | removed graph edges / altered reachability |
| `frontier_dropout` | destroyed support vertex availability |
| `support_delay` | delayed support availability predicate |
| `orientation_degradation` | support-certification failure |
| `ledger_failure` | local ledger certification failure |
| `selector_stress` | changed certified-ready incompatibility neighborhood |
| `min_finality_depth` | depth-indexed finalization witness |
| `readiness_recovery_length` | first later depth satisfying readiness |

## Guardrail

The Lean bridge should remain abstract and RA-native. It should not encode simulator-specific random interventions. The simulator supplies examples; Lean should formalize the structural predicates.
