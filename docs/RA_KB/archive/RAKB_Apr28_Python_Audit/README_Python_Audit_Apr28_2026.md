# RAKB Python Audit Patch Application — Apr 28, 2026

This packet contains Stage B Python audit outputs and registry upserts. These are CSV upserts, not `git apply` source patches, except files under `patches/`.

## Registry upsert files

- `registry_patch_v1/RAKB_python_artifacts_upsert_v1_Apr28_2026.csv` → merge into `docs/RA_KB/registry/artifacts.csv`.
- `registry_patch_v1/RAKB_python_claim_artifact_edges_upsert_v1_Apr28_2026.csv` → merge into `docs/RA_KB/registry/claim_artifact_edges.csv`.
- `registry_patch_v1/RAKB_python_restoration_candidates_upsert_v1_Apr28_2026.csv` → merge into or create `docs/RA_KB/registry/restoration_candidates.csv`.

Use the same `apply_rakb_upserts.py` script as before. From `docs/RA_KB`:

```bash
mkdir -p reports/patches/Apr28_python_v1
cp <packet>/registry_patch_v1/*.csv reports/patches/Apr28_python_v1/
cp <packet>/scripts/apply_rakb_python_upserts.py scripts/
cp <packet>/reports/RAKB_python_*.csv reports/patches/Apr28_python_v1/
python scripts/apply_rakb_python_upserts.py --registry ./registry --patch-dir ./reports/patches/Apr28_python_v1 --reports ./reports --dry-run
python scripts/apply_rakb_python_upserts.py --registry ./registry --patch-dir ./reports/patches/Apr28_python_v1 --reports ./reports
python scripts/validate_rakb_v0_5.py
```

## Source-code patches

The two `.diff` files under `patches/` are actual source-code patches:

- `patch_mu_int_derive_syntax.diff` fixes a Python syntax error.
- `patch_ra_flat_rotation_curve_docstring.diff` fixes an invalid docstring escape warning.

Apply them from the repository root with `git apply`, inspect the changes, then run:

```bash
python -m py_compile src/RA_AQFT/mu_int_derive.py src/RA_AQFT/ra_flat_rotation_curve.py
```

## Policy reminder

Python artifacts should not be promoted as proof support solely because they run. They should be recorded as `computes`, `benchmarks`, `candidate_support`, `generated_output_for`, or `do_not_promote` according to the classification table.
