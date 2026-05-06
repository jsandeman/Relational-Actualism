# RA Track B.3 — v1.8.1-Compliant Witness Coverage Sweep

This packet audits whether Track B graph/cut orientation-witness extraction outputs have enough fixed-bin coverage to support a future v1.8.1-compliant matched-graph orientation-rescue analysis.

It is an infrastructure / coverage packet only:

- no Lean changes
- no simulator semantic changes
- no orientation-rescue claim
- no Nature-facing claim

The controlling standard is v1.8.1 fixed-bin joint `support_width × family_size` discipline. If a joint stratum lacks both low and high orientation-overlap bins under the fixed global/cell bins, the signal is non-estimable rather than rescued by local re-binning.

## Run

```bash
python scripts/run_trackB3_v181_witness_coverage.py \
  --input-dirs ../RA_TrackB_ActiveSimulatorGraphWitnessExtraction_May06_2026/outputs,../RA_CausalDAG_MotifCommitSimulator_v1_7_OrientationKeyingAblation_May06_2026/outputs \
  --output-dir outputs
```

## Outputs

- `ra_trackB3_normalized_witness_coverage_rows.csv`
- `ra_trackB3_fixed_bin_coverage_by_config.csv`
- `ra_trackB3_joint_width_family_strata.csv`
- `ra_trackB3_v181_estimability_by_config.csv`
- `ra_trackB3_width_family_distribution_by_bin.csv`
- `ra_trackB3_sampler_recommendations.csv`
- `ra_trackB3_witness_coverage_summary.csv`
- `ra_trackB3_witness_coverage_summary.md`

## Interpretation

A coverage success does not establish orientation-specific rescue. It only says the comparison domain is sufficiently populated to run a future rescue analysis. A coverage failure means the sampler/configuration cannot support such a comparison yet.
