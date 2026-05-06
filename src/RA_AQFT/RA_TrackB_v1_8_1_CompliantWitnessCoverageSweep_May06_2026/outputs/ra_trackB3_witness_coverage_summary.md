# Track B.3 v1.8.1-Compliant Witness Coverage Summary

- input_rows: 1176000
- sources: 2
- keyings: 7
- surfaces: 2
- support_width_classes: 1;2;3;4
- family_size_classes: 1;3;4;5;7;11;15
- fixed_bin_classes: high;low;medium
- joint_strata_rows: 464
- estimable_joint_strata: 111
- estimable_joint_strata_fraction: 0.239224
- configs_with_low_medium_high: 108
- orientation_rescue_claim_made: False
- posture: v1_8_1_valid_comparison_domains_available

## Recommendation counts

{
  "rebalance_width_family_bins_or_sampler": 72,
  "coverage_sufficient_for_v1_8_1_audit": 36,
  "increase_high_overlap_coverage": 8
}

## Interpretation

This packet audits coverage only. It does not compute or promote orientation-specific rescue claims. A future rescue analysis is valid only if fixed orientation bins populate low/high contrasts inside support_width × family_size strata under the v1.8.1 rule.
