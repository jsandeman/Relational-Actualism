# RAKB Stage B Launch Report — Python Computation Audit

## Stage A closeout

The RAKB v5 upsert application succeeded and structural validation passed:

```text
claims=39 issues=12 targets=7 framing=3 archived=2
claim_edges=58 all_dependency_edges=97 artifacts=126 claim_artifact_edges=64
```

The D2-root Lake build also completed successfully:

```text
Build completed successfully (8284 jobs).
```

The remaining warning is the known unused variable `hN2` in `RA_D3_CosmologicalExpansion.lean`.

## Stage B objective

The Python audit must classify computational artifacts by evidence role rather than treating all scripts as claim support.

The critical distinction is:

```text
static relevance != reproduced computation != claim support
```

## Primary Stage B source roots

Use these roots first:

```text
src/RA_AQFT/*.py
src/RA_Complexity/*.py
src/ra_audit.py
data/DFT_Survey/*.py
```

Do not initially include historical scripts under `docs/RA_History/` unless a canonical paper or claim edge explicitly cites them.

## First-pass audit products

The static audit script produces:

```text
python_file_inventory.csv
python_import_edges.csv
python_declarations.csv
python_constants.csv
python_numeric_literals.csv
python_io_calls.csv
python_randomness.csv
python_plot_calls.csv
python_claim_refs.csv
python_bridge_terms.csv
python_call_edges.csv
python_audit_graph.jsonl
python_audit_report.md
```

These outputs support triage. They do not by themselves prove or reproduce any scientific result.

## Review priority

Review in this order:

1. Scripts that feed empirical prediction targets: `f0_enumeration.py`, `d3_alpha_s_BDG.py`, `qcd_running_proof.py`, `ra_dark_energy.py`, `ra_desi_verify.py`, `ra_flat_rotation_curve.py`.
2. Scripts that support dimensionality/arithmetic claims: `d4u02_enumeration.py`, `cross_dimensional_exclusion.py`, `o14_incidence_algebra.py`, `o14_proof.py`.
3. Scripts that support matter/motif claims: `D1_BDG_MCMC_simulation.py`, `d1_BDG_string_tension.py`, `d2_two_phases.py`, `n_eff_*.py`, `mu_*.py`.
4. Scripts that support complexity/life claims: `assembly_mapper.py`, `actualization_thermo.py`, `thermo_batch_b3lyp.py`.
5. Scripts likely to be bridge/interpretation only: `berry_*`, `born_rule_derivation.py`, `casimir_benchmark.py`, `rindler_relative_entropy.py`.

## Promotion policy

Only promote a Python file to active `computes`, `enumerates`, `simulates`, or `benchmarks` support after exact command/output reproduction.

Until then, use `candidate_support`, `static_reviewed`, or `legacy_provenance`.
