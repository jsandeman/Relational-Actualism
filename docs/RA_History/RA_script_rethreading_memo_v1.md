# RA Script Rethreading Memo v1

## Purpose

This memo threads the current benchmark scripts through the suite-primary weak-field source-law dictionary.

## Script map

| file | present role | safe status now | required relabel / next step |
| --- | --- | --- | --- |
| `ra_solar_system_benchmarks.py` | dense-regime Schwarzschild / PPN benchmark | **CV conditional on the Paper III bridge** | keep as dense-regime bridge consequence |
| `ra_lensing_benchmarks.py` | dense-regime solar + thin-lens benchmark | **translation-level calculational witness** | keep; cite source-law note so users do not read it as a direct discrete derivation |
| `ra_flat_rotation_curve.py` | illustrative halo correction demo | **illustrative only** | relabel explicitly: calibrated demonstration, not coefficient derivation |
| `bullet_cluster.py` | open historical-source stress test | **open computational target** | keep as an honest hard-wall memo, not flagship benchmark |
| `casimir_benchmark.py` | AQFT benchmark | unchanged by this source-law note | pair with formal AQFT roadmap |

## Recommended header language

### Dense-regime scripts
Use:
> This file evaluates dense-regime benchmark consequences of the recovered Einstein sector under the suite-primary weak-field source-law note. It is not a direct discrete coefficient-level derivation.

### Halo scripts
Use:
> This file explores the current effective actualization-gradient ansatz for the sparse halo regime. It is illustrative and should not be read as a coefficient-level proof until the canonical source-law operator is closed.

### Cluster / historical-source scripts
Use:
> This file probes an open closure target involving accumulated causal depth and mixed-regime lensing. It is a stress test, not a closed benchmark.

## Immediate cleanup

1. `ra_flat_rotation_curve.py`
   - keep the decomposition into accumulated source + correction term
   - remove any wording implying first-principles closure
   - explicitly state that `xi` is calibrated from a target flat velocity in the current file

2. `bullet_cluster.py`
   - keep the honest final verdict
   - replace any language suggesting the metric source is already canonically identified with the script’s internal quantity names

3. `ra_solar_system_benchmarks.py` and `ra_lensing_benchmarks.py`
   - add a one-line import or docstring pointer to the suite-primary source-law note
   - keep these scripts as the safe calculational front end of the gravity programme

## Bottom line

The scripts now fall into three clear buckets:

- **bridge-supported dense benchmarks**
- **effective sparse-regime ansatz explorations**
- **open historical-source stress tests**

That is a healthier and more honest computational architecture than treating all scripts as equally probative.
