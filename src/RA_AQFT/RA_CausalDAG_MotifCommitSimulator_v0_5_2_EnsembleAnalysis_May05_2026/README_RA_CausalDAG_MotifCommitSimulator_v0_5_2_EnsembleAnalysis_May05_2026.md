# RA Causal-DAG Motif-Commit Simulator v0.5.2 — Ensemble Severance-Signature Analysis

Date: May 05, 2026

This packet adds an analysis layer over the v0.5.1 large-ensemble causal-severance workbench. It does not modify simulator dynamics, Lean formalizations, or motif-commit semantics.

## Purpose

v0.5.1 made large causal-severance ensembles practical. v0.5.2 asks what those ensembles show in RA-native terms:

- Which severance modes saturate once nonzero disruption is applied?
- Which modes produce graded delay, recovery, or finality-depth signatures?
- Which modes are separable by actualization-fragility channel?
- Does the current run contain enough support-frontier width diversity to test support-width fragility?

The analysis vocabulary is RA-native: support, readiness, strict commitment, selected commitment, finality-depth shift, recovery length, and support-frontier width.

## Main module

```text
analysis/ra_causal_dag_ensemble_analysis.py
```

## Usage against canonical v0.5.1 outputs

From the packet root:

```bash
python scripts/run_ensemble_analysis_v0_5_2.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_5_1_LargeEnsemble_May04_2026/outputs \
  --output-dir outputs
```

To include the user-reported 100-seed run context in the markdown summary:

```bash
python scripts/run_ensemble_analysis_v0_5_2.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_5_1_LargeEnsemble_May04_2026/outputs \
  --output-dir outputs \
  --include-user-reported-100-seed-context
```

## Outputs

```text
ra_fragility_by_mode_and_severity_v0_5_2.csv
ra_severance_mode_signatures_v0_5_2.csv
ra_fragility_by_support_width_v0_5_2.csv
ra_mode_separability_scores_v0_5_2.csv
ra_finality_shift_by_mode_v0_5_2.csv
ra_recovery_length_by_mode_v0_5_2.csv
ra_severance_signature_summary_v0_5_2.md
ra_ensemble_analysis_state_v0_5_2.json
```

## Validation

```text
python -m unittest discover -s tests -v
```

Packet-local validation:

```text
Ran 4 tests
OK
```

## Canonical-run note

The demo outputs included in this packet were generated using the packet-local v0.5.1 outputs available in this environment. The user has separately run and committed the canonical 100-seed / 32-step large ensemble. For RAKB promotion of signature claims, rerun this v0.5.2 analyzer against those committed 100-seed outputs.

User-reported canonical context:

```text
seeds: 100 (17-117)
steps: 32
workers: 4
actual_evaluations: 120,000
sampled_evaluations: 5,000
wall_time: 60.13s
throughput: ~1,996 eval/s
aggregate losses: support=62,081; readiness=77,617; strict_commit=93,153; selected_commit=77,617
```

## Status

This is an analysis/tooling packet. It introduces no new Lean module. The compiled formal anchor remains `RA_MotifCausalSeveranceBridge.lean` and the validated simulator anchor remains v0.5/v0.5.1.
