# Simulator v0.5 → Future Lean Causal-Severance Bridge

The simulator suggests a small future Lean module:

```text
RA_MotifCausalSeveranceBridge.lean
```

Recommended abstract declarations:

```lean
GraphCausalSeverance
GraphSupportCutSurvives
GraphReadinessSurvivesSeverance
GraphSupportCutDestroyed
GraphCommitBlockedBySupportDestruction
GraphFinalityDepthShift
GraphRecoveryLength
```

Recommended first theorem schemas:

```text
1. If every required support vertex still reaches the site after severance,
   readiness survives.

2. If at least one required support vertex is unavailable or no longer reaches
   the site, readiness fails for that support cut.

3. If support remains certified but delayed, readiness can recover at a later
   causal depth.
```

The simulator currently distinguishes support-certification failure from causal-readiness failure. That distinction should be preserved in Lean.
