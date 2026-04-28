# RA Python Computation Audit — Static Report

Repository root: `/Users/jsandeman/projects/Relational-Actualism`
Python files scanned: **58**
AST parse success: **57/58**

## Domain distribution
- `general`: 26
- `berry_phase`: 9
- `matter_interactions`: 9
- `gravity_cosmology`: 6
- `dimensionality_arithmetic`: 4
- `complexity_life_thermo`: 3
- `kb_tooling`: 1

## Role distribution
- `script`: 37
- `computational_derivation_candidate`: 11
- `computational_experiment_or_benchmark`: 7
- `report_generator`: 2
- `kb_tool`: 1

## Highest-priority review files

These are ranked by a heuristic combining bridge-language hits, randomness, IO, plotting, parse problems, and missing explicit claim references. High score does not mean wrong; it means review first.

| risk | path | domain | role | bridge hits | RA-native hits | IO | random | claim refs |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 36 | `src/RA_AQFT/t1_forecast_deliverables_v2.py` | general | computational_experiment_or_benchmark | 117 | 0 | 4 | 0 | 0 |
| 35 | `src/RA_AQFT/mu_int_derive.py` | general | computational_derivation_candidate | 80 | 16 | 0 | 0 | 0 |
| 34 | `src/RA_AQFT/RA_BDG_Simulation.py` | general | computational_experiment_or_benchmark | 35 | 15 | 0 | 5 | 0 |
| 34 | `src/RA_AQFT/bdg_multicoupling.py` | general | script | 144 | 16 | 0 | 1 | 0 |
| 34 | `src/RA_AQFT/kernel_saturation.py` | general | script | 30 | 9 | 0 | 2 | 0 |
| 34 | `src/RA_AQFT/n_eff_alternative.py` | general | script | 27 | 7 | 0 | 5 | 0 |
| 34 | `src/RA_AQFT/n_eff_factorization.py` | general | script | 26 | 8 | 0 | 5 | 0 |
| 34 | `src/RA_AQFT/o14_incidence_algebra.py` | dimensionality_arithmetic | script | 33 | 27 | 0 | 1 | 0 |
| 34 | `src/RA_AQFT/ra_dark_energy.py` | gravity_cosmology | script | 75 | 9 | 0 | 5 | 0 |
| 34 | `src/RA_AQFT/ra_early_bh.py` | general | script | 67 | 21 | 0 | 1 | 0 |
| 34 | `src/RA_AQFT/ra_structure_formation.py` | gravity_cosmology | script | 47 | 4 | 0 | 6 | 0 |
| 34 | `src/RA_AQFT/severed_outdegree.py` | general | script | 55 | 26 | 0 | 6 | 0 |
| 32 | `src/RA_AQFT/antichain_drift.py` | general | script | 23 | 12 | 0 | 3 | 0 |
| 30 | `src/RA_AQFT/D1_BDG_MCMC_simulation.py` | matter_interactions | computational_experiment_or_benchmark | 135 | 17 | 0 | 6 | 3 |
| 30 | `src/RA_AQFT/d2_two_phases.py` | matter_interactions | script | 56 | 20 | 0 | 5 | 6 |
| 30 | `src/RA_AQFT/rindler_relative_entropy.py` | gravity_cosmology | script | 64 | 20 | 0 | 7 | 1 |
| 30 | `src/ra_audit.py` | kb_tooling | kb_tool | 208 | 41 | 0 | 4 | 0 |
| 29 | `src/RA_AQFT/RA_RASM_Verification.py` | general | script | 27 | 13 | 0 | 0 | 0 |
| 29 | `src/RA_AQFT/berry_bridge.py` | berry_phase | script | 43 | 24 | 0 | 0 | 0 |
| 29 | `src/RA_AQFT/berry_computation.py` | berry_phase | script | 35 | 18 | 0 | 0 | 0 |
| 29 | `src/RA_AQFT/berry_decomposition.py` | berry_phase | script | 39 | 6 | 0 | 0 | 0 |
| 29 | `src/RA_AQFT/berry_derive_f.py` | berry_phase | computational_derivation_candidate | 28 | 19 | 0 | 0 | 0 |
| 29 | `src/RA_AQFT/berry_final.py` | berry_phase | script | 65 | 12 | 0 | 0 | 0 |
| 29 | `src/RA_AQFT/berry_gauge.py` | berry_phase | script | 62 | 23 | 0 | 0 | 0 |
| 29 | `src/RA_AQFT/berry_theorems.py` | berry_phase | script | 46 | 2 | 0 | 0 | 0 |

## Generated outputs
- `python_file_inventory.csv`
- `python_import_edges.csv`
- `python_declarations.csv`
- `python_constants.csv`
- `python_numeric_literals.csv`
- `python_io_calls.csv`
- `python_randomness.csv`
- `python_plot_calls.csv`
- `python_claim_refs.csv`
- `python_bridge_terms.csv`
- `python_call_edges.csv`
- `python_audit_graph.jsonl`

## Evidence policy

Static audit evidence is not yet computational reproduction evidence. Promote a Python artifact to `computes` or `reproduces` only after recording inputs, command, environment, output files, and deterministic/non-deterministic status.
