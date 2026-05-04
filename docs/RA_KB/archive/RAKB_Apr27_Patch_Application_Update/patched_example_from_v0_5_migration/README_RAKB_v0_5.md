# RAKB v0.5 Migration Draft

This bundle is a typed migration of `RA_results_master_v0_4_5.yaml`.

## Principle

The v0.4.5 registry mixed foundations, derived claims, formalized claims, open targets, predictions, framing policies, archived claims, source artifacts, and generated reports in one monolithic state. v0.5 separates those roles.

## Active files

- `registry/claims.yaml` — active foundations and results only.
- `registry/issues.yaml` — open native targets / unresolved tasks.
- `registry/targets.yaml` — empirical-facing prediction and benchmark targets.
- `registry/framing.yaml` — non-target and translation-discipline policies.
- `registry/artifacts.csv` — artifact inventory migrated from v0.4.5; source files were not present in the ZIP, so hashes are blank.
- `registry/claim_artifact_edges.csv` — claim-to-artifact support edges.
- `registry/claim_edges.csv` — active proof dependencies only.
- `registry/all_dependency_edges.csv` — all migrated dependency edges, including issue/target edges.
- `reports/archive_move_plan_v0_5.csv` — files from the old bundle that should be archived.
- `reports/delete_plan_v0_5.csv` — OS metadata files that should be deleted.
- `scripts/validate_rakb_v0_5.py` — deterministic structural validator.

## Counts

- Source result nodes in v0.4.5: 63
- Active claims in `claims.yaml`: 39
- Open issues in `issues.yaml`: 12
- Prediction / benchmark targets in `targets.yaml`: 7
- Framing policies in `framing.yaml`: 3
- Archived claims preserved: 2
- v0.4.5 dependency edges: 97
- Active claim-to-claim edges: 58
- Artifact rows migrated: 97
- Claim-artifact edges migrated: 44

## Important limitation

The uploaded ZIP contains the KB artifacts but not the underlying Lean/Python/Markdown source corpus. This migration preserves the v0.4.5 source references and artifact IDs, but it cannot independently verify Lean compilation, Python execution, or markdown derivations. Regenerate `registry/artifacts.csv` from the actual repo before treating v0.5 as source-backed.

## Recommended next command sequence

```bash
python scripts/validate_rakb_v0_5.py
```

Then regenerate artifacts from the actual RA repo and replace blank `sha256`, `git_sha`, and `repo_relative_path` fields.
