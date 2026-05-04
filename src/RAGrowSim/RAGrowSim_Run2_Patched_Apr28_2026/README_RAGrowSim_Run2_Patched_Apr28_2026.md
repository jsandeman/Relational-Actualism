# RAGrowSim Run-2 patched methodology packet — Apr 28 2026

This packet supersedes the earlier `RAGrowSim_Run2_Methodology_Apr28_2026` scripts only for the conditional-Poisson comparison.

## What changed

Claude correctly found that the previous `run_analysis_v3_conditional_poisson.jl` called `loggamma` without importing `SpecialFunctions`. Rather than add a dependency, the patched default script uses a dependency-free Poisson PMF recurrence.

Recommended script:

```bash
scripts/run_analysis_v3_conditional_poisson_no_specfun.jl
```

For convenience, the canonical filename is also replaced with the no-dependency implementation:

```bash
scripts/run_analysis_v3_conditional_poisson.jl
```

## What did not change

The methodology is unchanged:

1. Run Neutral BDG growth on multiple seeds.
2. Record realized/accepted vertex profiles.
3. Compare simulator profiles against both raw Poisson and accepted-conditional Poisson.
4. Treat results as exploratory until candidate-measure diagnostics are complete.

No RAKB update is recommended yet.

## Install

From the RAGrowSim repo root:

```bash
cp <packet>/scripts/run_analysis_v3_conditional_poisson_no_specfun.jl scripts/
cp <packet>/scripts/run_analysis_v2_mu_estimators.jl scripts/
cp <packet>/scripts/run_candidate_measure_diagnostics.jl scripts/
```

Optionally also replace the canonical v3 filename:

```bash
cp <packet>/scripts/run_analysis_v3_conditional_poisson.jl scripts/
```

## Run order

First, accepted-conditional Poisson:

```bash
julia --project=. scripts/run_analysis_v3_conditional_poisson_no_specfun.jl \
  25 50 outputs/conditional_poisson
```

Second, candidate-measure diagnostics:

```bash
julia --project=. scripts/run_candidate_measure_diagnostics.jl \
  25 20 outputs/candidate_measure 4
```

Optional μ-estimator comparison:

```bash
julia --project=. scripts/run_analysis_v2_mu_estimators.jl \
  25 50 outputs/mu_estimators
```

## Output files to send back

Please send:

```text
outputs/conditional_poisson/conditional_summary_mu_depth.csv
outputs/conditional_poisson/conditional_summary_mu_v4.csv
outputs/conditional_poisson/per_vertex_records_conditional.csv
outputs/candidate_measure/candidate_measure_step_summary.csv
outputs/candidate_measure/candidate_measure_profile_summary.csv
outputs/mu_estimators/mu_estimator_records.csv                 # optional
outputs/mu_estimators/mu_estimator_bin_summary.csv             # optional
```

## Source-code patch options

Two patch files are included:

```text
patches/patch_run_analysis_v3_no_specfun.diff
patches/patch_run_analysis_v3_specialfunctions.diff
```

Use the no-special-functions patch by default. Use the `SpecialFunctions` patch only if you want to keep the original log-PMF form and add the dependency.

## RAKB status

The YAML under `registry_hold/` is intentionally hold-only. It records likely future issues but should not be applied until the conditional-Poisson and candidate-measure diagnostics are read.
