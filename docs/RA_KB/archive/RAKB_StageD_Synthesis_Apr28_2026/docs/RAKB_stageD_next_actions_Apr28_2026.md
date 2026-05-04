# Stage D Next Actions

## Immediate commit hygiene

1. Move or delete `registry/*.bak_20260428_*` backup files before committing, unless intentionally preserving them under `reports/backups/`.
2. Apply the Stage D v0.5.1 registry upsert for D2 build-status hardening.
3. Re-run `python scripts/validate_rakb_v0_5.py`.
4. Commit Stage D reports.

## Optional source patch

Apply `patch_RA_D3_CosmologicalExpansion_unused_hN2.diff` to silence the only current Lean warning.

## Next science/governance work

1. Decide high-priority restoration candidates: bandwidth, proper time, d=4 cascade, singularity termination, D2/HadronMassTriad.
2. Add `% RAKB: ...` comments to canonical TeX using `RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv`.
3. Work through Python hardening queue before promoting candidate computations.
4. Regenerate graph metrics after the source-text layer is committed.
