# RA Motif Selector Closure Formal Bridge — May 4, 2026

This packet adds a source-level Lean bridge from the compile-confirmed, context-gated `RA_MotifCommitProtocol` interface to an abstract selector-closure interface.

The target is RA-native actualization discipline, not QM, GR, blockchain consensus, or distributed-system machinery. The module formalizes only the following internal RA ladder:

```text
certified support
  → causal readiness at a local site
  → certified readiness
  → selector closure over certified-ready alternatives
  → selected commitment
  → strict commitment when selector closure is complete
  → unresolved incompatibility when incompatible alternatives remain unselected
```

## Contents

```text
lean/RA_MotifSelectorClosure.lean
patches/patch_lakefile_add_RA_MotifSelectorClosure.diff
scripts/apply_motif_selector_closure_bridge.py
bridge/simulator_to_lean_selector_bridge_v0_3.md
registry_proposals/RAKB_motif_selector_closure_proposed_claims.yaml
reports/RA_MotifSelectorClosure_FormalBridge_Report_May04_2026.md
reports/source_audit_RA_MotifSelectorClosure_May04_2026.log
reports/apply_script_dry_run.log
reports/simulator_to_lean_bridge_map_May04_2026.csv
```

## Required upstream interface

This file targets the context-gated / compile-confirmed `RA_MotifCommitProtocol` interface containing:

```lean
DAGCommitContext.supports
GraphCommitContext.supports
DAGCommitsAt.supports
GraphCommitsAt.supports
DAGCommitsAt.ready
GraphCommitsAt.ready
GraphReadyAt_supportCutOfFiniteHasseFrontier_iff
```

If your local `RA_MotifCommitProtocol.lean` still has only an `incompatible` field and no `supports` field, first apply the context-gated motif-commit update.

## Apply

From your Lean project root:

```bash
python /path/to/packet/scripts/apply_motif_selector_closure_bridge.py \
  --lean-project . \
  --packet-root /path/to/packet \
  --update-lakefile
```

Dry run:

```bash
python /path/to/packet/scripts/apply_motif_selector_closure_bridge.py \
  --lean-project . \
  --packet-root /path/to/packet \
  --update-lakefile \
  --dry-run
```

Then check locally:

```bash
lake env lean RA_MotifSelectorClosure.lean
```

and, if added as a Lake root:

```bash
lake build
```

## Main declarations

DAG layer:

```text
DAGCertifiedReadyAt
DAGSelectorClosureAt
DAGSelectorCompleteAt
DAGSelectedCommitsAt
DAGSelectedCommitsAt.to_strict_commits_of_complete
DAGSelectorClosureAt.no_certified_ready_incompatible_of_complete
DAGUnresolvedIncompatibilityAt
```

Graph layer:

```text
GraphCertifiedReadyAt
GraphSelectorClosureAt
GraphSelectorCompleteAt
GraphSelectedCommitsAt
GraphSelectedCommitsAt.to_strict_commits_of_complete
GraphSelectorClosureAt.no_certified_ready_incompatible_of_complete
GraphUnresolvedIncompatibilityAt
GraphHasseFrontierSelectedCommitsAt
GraphHasseFrontierSelectedCommitsAt.frontier_reaches_site
```

## RAKB handling

The included YAML is a proposal only. Do not mark the Lean declarations `compile_confirmed` until your local Lean environment checks the file.

Recommended pre-compile status:

```text
source-level formal bridge draft
```

Recommended post-compile status:

```text
Lean-compiled formal bridge, no sorry/admit/axiom
```
