# Simulator-to-Lean Bridge: Motif Selector Closure v0.3 → RA_MotifSelectorClosure

This bridge keeps RA-native vocabulary primary. The simulator is not a QM simulator and not a consensus simulator; comparison vocabulary belongs only in explicitly marked interpretation sections.

## Direct correspondence

| Simulator v0.3 concept | Lean bridge declaration | RA-native meaning |
|---|---|---|
| `MotifCandidate` | `MotifCandidate`, `GraphMotifCandidate` | finite candidate motif carrier |
| `SupportCut` | `CausalSupportCut`, `GraphSupportCut` | finite support evidence |
| `GraphSupportCertifier.supports` | `DAGCommitContext.supports`, `GraphCommitContext.supports` | certified support relation |
| `ready_at` | `DAGReadyAt`, `GraphReadyAt` | support lies in causal past / reachable past |
| certified-ready candidate | `DAGCertifiedReadyAt`, `GraphCertifiedReadyAt` | certified support plus readiness at a site |
| strict `decision(...).commits` | `DAGCommitsAt`, `GraphCommitsAt` | strict commitment with no certified-ready incompatible competitor |
| `selector_closure_at` | `DAGSelectorClosureAt`, `GraphSelectorClosureAt` | RA-native local selector closure over motif/support-cut pairs |
| selector completeness | `DAGSelectorCompleteAt`, `GraphSelectorCompleteAt` | every certified-ready pair is selected |
| `selected_decision(...).commits` | `DAGSelectedCommitsAt`, `GraphSelectedCommitsAt` | selected commitment after selector narrowing |
| stalemate trace | `DAGUnresolvedIncompatibilityAt`, `GraphUnresolvedIncompatibilityAt` | unresolved certified-ready incompatible alternatives |
| Hasse-frontier support | `GraphHasseFrontierSelectedCommitsAt` | selected commitment via finite Hasse-frontier support |

## Important distinction

`DAGSelectedCommitsAt` / `GraphSelectedCommitsAt` are not synonyms for strict `DAGCommitsAt` / `GraphCommitsAt`.

Selected commitment requires:

```text
certified-ready support ∧ selected motif/support-cut pair
```

Strict commitment additionally requires:

```text
no certified-ready incompatible alternative remains at the same site
```

The theorem connecting them is:

```lean
DAGSelectedCommitsAt.to_strict_commits_of_complete
GraphSelectedCommitsAt.to_strict_commits_of_complete
```

## Guardrail language

Use these as primary terms:

```text
pre-actualized multiplicity
candidate motif family
causal support cut
certified readiness
selector closure
selected commitment
strict commitment
causal finality
unresolved incompatibility
```

Use inherited theory vocabulary only in comparison sections.
