# RA_MotifOrientationSupportBridge Formal Bridge — May 4, 2026

This packet adds a certificate-level bridge from graph-orientation closure to the RA motif-commit / selector-closure layer.

## Scope

The bridge is RA-native and conditional. It does not import simulator policies, voting rules, collapse vocabulary, or other inherited apparatus as primitives. It records the formal interface by which orientation closure can certify motif support and witness incompatibility.

## New Lean module

```lean
import RA_MotifSelectorClosure
import RA_GraphOrientationClosure
```

Main declarations:

```text
GraphOrientedMotifSupport
GraphOrientedMotifSupport.certified
GraphOrientationSupports
GraphOrientationConflictWitness
GraphOrientationActualizationContext
GraphOrientationActualizationContext.toCommitContext
GraphOrientationSelectorClosureAt
GraphOrientationSelectedCommitsAt
GraphOrientationUnresolvedIncompatibilityAt
```

Main theorems:

```text
GraphOrientedMotifSupport.support_eq_hasse_frontier
GraphOrientedMotifSupport.ready_iff_frontier_reaches_site
GraphOrientedMotifSupport.signSource_eval
GraphOrientedMotifSupport.ledger_qN1_seven
GraphOrientationSelectedCommitsAt.has_oriented_frontier_witness
GraphOrientationSelectedCommitsAt.to_strict_commits_of_complete
GraphOrientationUnresolvedIncompatibilityAt.has_conflict_witness
GraphOrientationActualizationContext.incompatible_symm
```

## Apply locally

Dry run:

```bash
python scripts/apply_motif_orientation_support_bridge.py   --lean-project /path/to/RA_Lean   --packet-root /path/to/RA_MotifOrientationSupportBridge_FormalBridge_May04_2026   --update-lakefile   --dry-run
```

Apply:

```bash
python scripts/apply_motif_orientation_support_bridge.py   --lean-project /path/to/RA_Lean   --packet-root /path/to/RA_MotifOrientationSupportBridge_FormalBridge_May04_2026   --update-lakefile
```

Check:

```bash
lake env lean RA_MotifOrientationSupportBridge.lean
lake build
```

## RAKB proposals

The `registry_proposals/` directory contains YAML/CSV proposals for the active `claims.yaml`, `framing.yaml`, `artifacts.csv`, and `claim_artifact_edges.csv` schema. Because this is not yet compile-confirmed, leave statuses as source-level pending compile until the local Lean check succeeds.

Dry-run RAKB proposal application:

```bash
python scripts/apply_motif_orientation_support_rakb_proposals.py   --registry /path/to/RAKB/registry   --packet-root /path/to/RA_MotifOrientationSupportBridge_FormalBridge_May04_2026   --dry-run
```

## Status

Source-level formal bridge, pending local Lean compile. The included source audit reports no `sorry`, `admit`, or `axiom` tokens.
