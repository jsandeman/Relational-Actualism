# v1.7 Orientation-Keying Ablation Report

This packet compares multiple graph-coupled orientation-link keying schemes on the same matched v0.9 trial stream. It is a forensic follow-up to v1.6, whose default extractor used member-indexed orientation tokens.

The packet is deliberately diagnostic. It should not be used to promote orientation-specific rescue unless a non-member graph/native keying survives matched-graph extraction at canonical scale.

## Core correction target

The v1.6 token form included `member_idx`, e.g. `olink:p->v:s0:m1`. This can make identical graph-local links fail to match when they occur in different support-family member slots. v1.7 therefore compares this keying against non-member-indexed alternatives.

## Outputs

- `ra_v1_7_keyed_trial_rows.csv`
- `ra_v1_7_keying_per_cell.csv`
- `ra_v1_7_specificity_by_keying.csv`
- `ra_v1_7_partial_correlation_by_keying.csv`
- `ra_v1_7_overlap_distribution_by_keying.csv`
- `ra_v1_7_permutation_control.csv`
- `ra_v1_7_summary.csv`
- `ra_v1_7_orientation_keying_audit_summary.md`
