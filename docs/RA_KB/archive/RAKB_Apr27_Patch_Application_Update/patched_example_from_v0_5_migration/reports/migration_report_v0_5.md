# RAKB v0.5 Migration Report

## What changed

The monolithic v0.4.5 registry was split into typed state files:

| v0.5 file | Contents |
|---|---|
| `registry/claims.yaml` | Active foundations and results only |
| `registry/issues.yaml` | Open Native Targets and unresolved tasks |
| `registry/targets.yaml` | prediction / empirical benchmark targets |
| `registry/framing.yaml` | non-target and translation-policy claims |
| `archive/legacy_registries/archived_claims_from_v0_4_5.yaml` | archived v0.4.5 nodes |
| `registry/artifacts.csv` | migrated artifact inventory |
| `registry/claim_artifact_edges.csv` | source-support edges |

## Node split

- Active claims: 39
- Open issues: 12
- Prediction targets: 7
- Framing policies: 3
- Archived claims: 2

## Edge split

- Total migrated dependencies: 97
- Active claim-to-claim proof edges: 58
- Issue dependency edges: 23
- Target dependency edges: 16

## Top active proof-leverage claims

- `RA-ONT-001` — Finite causal graph ontology (reach 38, children 5)
- `RA-ONT-003` — Structured potentia / adjacent possible (reach 30, children 2)
- `RA-KERNEL-001` — Four-dimensional BDG acceptance kernel (reach 29, children 8)
- `RA-ONT-002` — Irreversible actualization (reach 19, children 1)
- `RA-ARITH-001` — BDG coefficient arithmetic spine (reach 18, children 5)
- `RA-LLC-001` — Local Ledger Condition (reach 18, children 5)
- `RA-D4-001` — D4U02 selectivity ceiling (reach 14, children 4)
- `RA-MOTIF-001` — Native motif sector definition (reach 8, children 1)
- `RA-MOTIF-002` — Stable motif census (reach 7, children 3)
- `RA-COMP-001` — Tier hierarchy (reach 7, children 2)

## Archive moves

- `RA_results_master_v0_1.yaml` → `archive/legacy_registries/RA_results_master_v0_1.yaml`
- `RA_results_master_v0_2.yaml` → `archive/legacy_registries/RA_results_master_v0_2.yaml`
- `RA_results_master_v0_3_expanded.yaml` → `archive/legacy_registries/RA_results_master_v0_3_expanded.yaml`
- `RA_results_master_v0_3_summary.md` → `archive/legacy_registries/RA_results_master_v0_3_summary.md`
- `RA_results_master_v0_4_5.yaml` → `archive/legacy_registries/RA_results_master_v0_4_5.yaml`
- `RA_dependency_graph_analysis_v0_3.md` → `archive/derived_outputs/v0_3/RA_dependency_graph_analysis_v0_3.md`
- `RA_dependency_graph_v0_3.dot` → `archive/derived_outputs/v0_3/RA_dependency_graph_v0_3.dot`
- `RA_dependency_graph_v0_3.png` → `archive/derived_outputs/v0_3/RA_dependency_graph_v0_3.png`
- `RA_dependency_metrics_v0_3.csv` → `archive/derived_outputs/v0_3/RA_dependency_metrics_v0_3.csv`
- `RAKB_v0_4_5_dependency_analysis.md` → `archive/derived_outputs/v0_4_5/RAKB_v0_4_5_dependency_analysis.md`
- `RAKB_v0_4_5_validation_audit.md` → `archive/derived_outputs/v0_4_5/RAKB_v0_4_5_validation_audit.md`
- `RA_artifact_inventory_v0_4_5.csv` → `archive/derived_outputs/v0_4_5/RA_artifact_inventory_v0_4_5.csv`
- `RA_dependency_graph_v0_4_5_proof_only.dot` → `archive/derived_outputs/v0_4_5/RA_dependency_graph_v0_4_5_proof_only.dot`
- `RA_dependency_graph_v0_4_5_proof_only.png` → `archive/derived_outputs/v0_4_5/RA_dependency_graph_v0_4_5_proof_only.png`
- `RA_dependency_metrics_v0_4_5_proof_only.csv` → `archive/derived_outputs/v0_4_5/RA_dependency_metrics_v0_4_5_proof_only.csv`
- `RA_prose_only_DR_audit_v0_4_5.csv` → `archive/derived_outputs/v0_4_5/RA_prose_only_DR_audit_v0_4_5.csv`
- `RA_targeted_prediction_search_matches_Apr20_Apr24.csv` → `archive/prediction_linkage_audits/2026-04-20_to_2026-04-24/RA_targeted_prediction_search_matches_Apr20_Apr24.csv`
- `RA_targeted_prediction_search_report.md` → `archive/prediction_linkage_audits/2026-04-20_to_2026-04-24/RA_targeted_prediction_search_report.md`
- `RAKB_prediction_linkage_candidates/RA_prediction_source_candidates_ranked.csv` → `archive/prediction_linkage_audits/2026-04-20_to_2026-04-24/RA_prediction_source_candidates_ranked.csv`
- `RAKB_prediction_linkage_candidates/RA_prediction_source_linkage_candidate_report.md` → `archive/prediction_linkage_audits/2026-04-20_to_2026-04-24/RA_prediction_source_linkage_candidate_report.md`
- `RAKB_Update_Prompt.txt` → `archive/prompt_protocols_v0_4/RAKB_Update_Prompt.txt`
- `RA_Dependency_Analysis_Prompt.txt` → `archive/prompt_protocols_v0_4/RA_Dependency_Analysis_Prompt.txt`
- `RA_Integrity_Check_Prompt.txt` → `archive/prompt_protocols_v0_4/RA_Integrity_Check_Prompt.txt`
- `RA_Paper_Sync_Prompt.txt` → `archive/prompt_protocols_v0_4/RA_Paper_Sync_Prompt.txt`
- `RA_Target_Prompt.txt` → `archive/prompt_protocols_v0_4/RA_Target_Prompt.txt`
- `RA_Audit_Consolidation_Apr20_Apr24.md` → `archive/audit_logs/RA_Audit_Consolidation_Apr20_Apr24.md`
- `rakb_pipeline.py` → `archive/legacy_scripts/rakb_pipeline_v0_4_scaffold.py`
- `README_RAKB.md` → `archive/legacy_readmes/README_RAKB_v0_4.md`

## Delete rather than archive

- `__MACOSX/._RAKB_Update_Prompt.txt`
- `__MACOSX/._RA_Dependency_Analysis_Prompt.txt`
- `__MACOSX/._RA_Integrity_Check_Prompt.txt`
- `__MACOSX/._RA_Paper_Sync_Prompt.txt`
- `__MACOSX/._RA_Target_Prompt.txt`
- `__MACOSX/._RA_dependency_graph_analysis_v0_3.md`
- `__MACOSX/._RA_dependency_graph_v0_3.dot`
- `__MACOSX/._RA_dependency_graph_v0_3.png`
- `__MACOSX/._RA_dependency_metrics_v0_3.csv`
- `__MACOSX/._RA_results_master_v0_2.yaml`
- `__MACOSX/._RA_results_master_v0_3_expanded.yaml`
- `__MACOSX/._RA_results_master_v0_3_summary.md`
- `__MACOSX/._README_RAKB.md`
- `__MACOSX/._rakb_pipeline.py`
- `__MACOSX/RAKB_prediction_linkage_candidates/._RA_prediction_source_linkage_candidate_report.md`

## Caveat

This migration did not inspect the true source corpus; it only restructured the KB bundle. The next required step is to regenerate the artifact manifest from the repo and attach hashes/Git SHAs.
