# Python + Julia cleanup plan — May 4, 2026

## Scope

Companion to `lean_corpus_cleanup_plan_May4_2026.md`. Apply
similar housekeeping to Python; archive Julia entirely.

## Python — naming / archive

### Group 1 — RENAME (RA-prefixed CamelCase → snake_case, no prefix)

| current | new |
|---|---|
| `src/RA_AQFT/RA_BDG_Simulation.py` | `src/RA_AQFT/bdg_simulation.py` |
| `src/RA_AQFT/RA_D1_Proof.py` | `src/RA_AQFT/d1_proof.py` |
| `src/RA_AQFT/RA_RASM_Verification.py` | `src/RA_AQFT/rasm_verification.py` |

(All three are outliers in `src/RA_AQFT/` — every other Python file
already uses snake_case without the `RA_` prefix.)

### Group 2 — REPLACE (drop `_v2` version suffix)

| current | new |
|---|---|
| `src/RA_AQFT/t1_forecast_deliverables_v2.py` | replace `src/RA_AQFT/t1_forecast_deliverables.py` content; archive original |

### Group 3 — ARCHIVE (one-shot historical migration scripts)

`docs/RA_KB/scripts/apply_*_upserts.py` (17 scripts). These are
historical RAKB upsert helpers from late-April registry migrations,
explicitly described as "historical, not part of a CI loop" in
`CLAUDE.md`. Each ran once during a specific Stage-A/B/C/D
migration; the RAKB state they produced is now in the registry, so
the scripts themselves are dead code.

To archive: `archive_python_deprecated_May4_2026.zip` in repo root.
Files:
- `apply_frontier_graph_v2_compile_upserts.py`
- `apply_frontier_v2_compile_upserts.py`
- `apply_graph_orientation_closure_v2_compile_upserts.py`
- `apply_graph_orientation_v1_upserts.py`
- `apply_hasse_finite_max_exist_v2_compile_upserts.py`
- `apply_hasse_finite_max_v1_upserts.py`
- `apply_hasse_maximal_v2_compile_upserts.py`
- `apply_hasse_v1_upserts.py`
- `apply_incidence_charge_v2_compile_upserts.py`
- `apply_incidence_sign_source_v1_upserts.py`
- `apply_rakb_charge_upserts.py`
- `apply_rakb_framework_upserts.py`
- `apply_rakb_python_upserts.py`
- `apply_rakb_selector_upserts.py`
- `apply_rakb_stageC_upserts.py`
- `apply_rakb_stageD_v0_5_1_upserts.py`
- `apply_rakb_upserts.py`
- `apply_selector_v2_upserts.py`
- `t1_forecast_deliverables.py` (superseded by _v2)

That's 19 files.

Plus: keep `validate_rakb_v0_5.py`, `ra_python_static_audit.py`,
`rakb_extract_bibitems.py`, `rakb_generate_tex_ids.py` — these are
active tools used by Makefile.rakb and ongoing validation.

### Group 4 — FLAG-AND-ASK (do NOT touch without explicit user confirmation)

These could plausibly be archived but I don't have enough signal to
decide without you:

- **8 `berry_*.py` scripts** (`berry_bridge`, `berry_computation`,
  `berry_decomposition`, `berry_derive_f`, `berry_final`,
  `berry_gauge`, `berry_theorems`, `berry_thinning`,
  `berry_transfer`). Per `RA_Berry_Phase_Derived.md` session log,
  these represent "8 successive computations, each of which failed
  in a diagnostic way" until the breakthrough. I don't know which
  is the keeper (some look final, some look intermediate). Leaving
  alone.
- `mu_int_derive.py` — RAKB status `blocked_repair_required`. Could
  be retired if you've decided not to fix it.
- `actualization_thermo.py` — RAKB status
  `blocked_missing_dependency_pending_reproduction`. Same question.
- `RA_BDG_Simulation.py` (will be renamed to `bdg_simulation.py`).
  Long file, several different simulation kernels — possibly
  superseded by `bmv_comparator.py` + `bdg_actualization.py`. Leaving
  alone.

If you want any of these archived, let me know.

### Group 5 — UNTOUCHED (active modules, all snake_case already)

Everything else in `src/RA_AQFT/*.py`, `data/DFT_Survey/*.py`,
`src/RA_Complexity/`, `src/ra_audit.py`. ~55 files. RAKB-tracked
with `uploaded_verified` / `uploaded_static_audited` /
`uploaded_smoke_tested_ok` status.

## Julia — full archival

User directive: "The Julia scripts can be archived."

Archive the entire `src/RAGrowSim/` subtree to
`archive_julia_ragrowsim_May4_2026.zip` in repo root and remove
from the working tree. Includes:

- `src/RAGrowSim/Project.toml`, `README.md`
- `src/RAGrowSim/src/` (8 `.jl` modules: RAGrowSim.jl, BDGGrow.jl,
  Ledger.jl, LedgerRules.jl, Antichains.jl, Seeds.jl, Dynamics.jl,
  Observables.jl)
- `src/RAGrowSim/test/` (7 test files)
- `src/RAGrowSim/scripts/` (8 analysis/run scripts)
- `src/RAGrowSim/RAGrowSim_Run2_*` (prior-run output dirs)
- `src/RAGrowSim/RAGrowSim_Run4_*_Packet.zip`
- `src/RAGrowSim/RAGrowSim_Run2_*_Packet.zip`
- `src/RAGrowSim/outputs/`

Also archive the standalone `src/RAGrowSim.tar.gz`.

## RAKB updates

After Python rename + archive, update:
- `artifacts.csv` `repo_relative_path` for renamed Python files
  (3 renamed; 1 replaced)
- Mark `apply_*_upserts.py` artifacts (if any) as `archived`
- For Julia: update all `ART-SIM-RAGROWSIM-*` and
  `ART-DATA-RAGROWSIM-*` artifacts: change status to `archived` and
  update `repo_relative_path` to point inside the new archive zip
  (or set `notes` to point to the zip)
- Add 2 new archive artifacts: `ART-PYTHON-DEPRECATED-ARCHIVE-MAY4-2026`
  and `ART-JULIA-RAGROWSIM-ARCHIVE-MAY4-2026`

## Execution order

1. Python rename (Group 1) via `git mv` where tracked, plain `mv`
   otherwise; update internal imports if any
2. Python replace (Group 2): copy v2 over original, archive original
3. Create `archive_python_deprecated_May4_2026.zip`, then remove
   originals
4. Create `archive_julia_ragrowsim_May4_2026.zip`, then remove
   `src/RAGrowSim/` and `src/RAGrowSim.tar.gz`
5. Update RAKB (artifacts.csv, claim_artifact_edges, source_status
   in claims/issues/targets that reference renamed/archived files)
6. Run validator
7. Run Python tests in src/RA_AQFT (verify no rename broke imports)
8. Commit
