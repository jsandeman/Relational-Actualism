# RAKB Stage B Python Computation Audit — Apr 28, 2026

## Executive verdict

The uploaded Python surface is scientifically useful, but it is not a uniform proof surface. It contains canonical deterministic enumerations, Monte Carlo diagnostics, phenomenological forecast generators, bridge/cartography scripts, and external quantum-chemistry probes. The audit therefore treats each script as an evidence artifact with an explicit relation type rather than as automatic proof support.

Scope checked:

- Python source files: 58
- Data CSV artifacts in source bundle: 3
- Static audit outputs supplied: 14 files
- Total source lines in Python inventory: 16,759
- AST parse success: 57/58
- `py_compile` blocker: `src/RA_AQFT/mu_int_derive.py`

## Support-strength distribution

- `native_candidate`: 17
- `hybrid_candidate`: 13
- `phenomenology`: 12
- `bridge_cartography`: 10
- `external_dependency`: 3
- `native_strong`: 1
- `needs_repair`: 1
- `kb_tool`: 1

## Most important positive findings

1. `d4u02_enumeration.py` is the strongest Python artifact. It is deterministic, has a main guard, self-tests against document values, and reproduces the canonical constants: `P_acc(mu=1)=0.548435673810`, `Delta_S_star=0.600685282698`, `mu*=1.018777361164`, `mu_QCD=4.7118366652`.
2. `f0_enumeration.py` is a strong native enumeration for the BDG path-weight ratio. It reproduces `W_other/W_baryon=17.3152`. The subsequent `f0` comparison remains hybrid because it multiplies by an external/SM RG `alpha_s(2m_p)` step.
3. `D1_BDG_MCMC_simulation.py`, `RA_BDG_Simulation.py`, `RA_RASM_Verification.py`, `sigma_*`, `rho_native.py`, and `pathwise_exit.py` form a substantial matter/motif computational programme. They should be linked to RA-MOTIF/RA-OPEN/RA-PRED targets as candidate or benchmark support, with caveats about imported constants and fitted scales.
4. `ra_desi_verify.py`, `ra_dark_energy.py`, and `t1_forecast_deliverables_v2.py` form a coherent phenomenology/forecast layer for RA-PRED-005. These should not be proof edges; they are target/forecast support edges.
5. `assembly_mapper.py` runs successfully as a topological complexity probe. The DFT scripts are blocked locally by missing `pyscf`, so they should remain pending until a reproducible chemistry environment and output logs are archived.

## Blockers / repairs

- `mu_int_derive.py` has a syntax error at line 132 caused by an unquoted em dash inside an f-string. A patch is included.
- `ra_flat_rotation_curve.py` runs but emits an invalid escape-sequence warning from its docstring and uses `plt.show()` rather than an archived output file. A small docstring patch is included.
- `ra_verify_heraclitus.py` parsed successfully but timed under a 30-second smoke test before producing output. Add a fast mode or cached grid before using it as reproducible evidence.
- `actualization_thermo.py` and `thermo_batch_b3lyp.py` require `pyscf`; they failed locally on missing dependency.

## Evidence policy by family

### Promote after output archival

- `d4u02_enumeration.py` → `RA-D4-001`, `RA-D4-002`, `RA-ARITH-005` as `computes`.
- `f0_enumeration.py` → `RA-ARITH-006` as native enumeration and `RA-PRED-004` as hybrid benchmark.

### Candidate computational support

- Matter/motif: `RA_BDG_Simulation.py`, `RA_D1_Proof.py`, `D1_BDG_MCMC_simulation.py`, `sigma_analysis.py`, `sigma_table.py`, `pathwise_exit.py`, `rho_native.py`, `n_eff_*`.
- Gravity/cosmology: `kernel_saturation.py`, `severed_outdegree.py`, `antichain_drift.py`, `ra_dark_energy.py`, `ra_desi_verify.py`, `t1_forecast_deliverables_v2.py`.

### Bridge/cartography only

- `born_rule_derivation.py`, `casimir_benchmark.py`, `rindler_relative_entropy.py`, and most `berry_*` scripts should not be active proof support yet. They should be preserved as restoration candidates or bridge appendices.

## Main governance recommendation

Add the Python artifacts and edges to RAKB, but preserve relation types. In particular, do not collapse `computes`, `benchmarks`, `candidate_support`, `generated_output_for`, and `do_not_promote` into a single support status.

## Generated files

- `reports/RAKB_python_source_classification_Apr28_2026.csv`
- `reports/RAKB_python_reproduction_smoke_tests_Apr28_2026.csv`
- `reports/RAKB_python_hardening_queue_Apr28_2026.csv`
- `reports/RAKB_python_top_level_execution_audit_Apr28_2026.csv`
- `registry_patch_v1/RAKB_python_artifacts_upsert_v1_Apr28_2026.csv`
- `registry_patch_v1/RAKB_python_claim_artifact_edges_upsert_v1_Apr28_2026.csv`
- `registry_patch_v1/RAKB_python_restoration_candidates_upsert_v1_Apr28_2026.csv`
- `patches/patch_mu_int_derive_syntax.diff`
- `patches/patch_ra_flat_rotation_curve_docstring.diff`
