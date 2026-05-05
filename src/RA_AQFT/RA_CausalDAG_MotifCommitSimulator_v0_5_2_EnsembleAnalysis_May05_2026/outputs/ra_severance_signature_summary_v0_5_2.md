# RA v0.5.2 Ensemble Severance-Signature Summary

This analysis is RA-native: it classifies causal-support disruption profiles, not inherited-theory formalisms.

## Analyzed run summary
- version: 0.5.1
- run_count: 100
- steps: 32
- workers: 4
- actual_evaluations: 120000
- sampled_evaluations: 5000
- elapsed_seconds: 60.129149
- evaluations_per_second: 1995.704287

## User-reported canonical large-run context
These values were supplied by the local run operator and are not independently reconstructed from packet-local files here.
- run_count: 100 seeds (17-117)
- steps: 32
- workers: 4
- actual_evaluations: 120000
- sampled_evaluations: 5000
- wall_time_seconds: 60.13
- throughput_eval_per_second: 1996
- aggregate_losses: support=62081; readiness=77617; strict_commit=93153; selected_commit=77617
- reported_saturation: edge_dropout, frontier_dropout, and ledger_failure saturate near 0.971 at all nonzero severity tiers

## Mode signatures
### edge_dropout
- response_class: threshold_saturating_support_loss
- primary_failure_channel: support_certification_or_frontier_loss
- loss_saturation_score: 0.983714
- finality_shift_mean_nonzero: -2.365287
- recovery_length_mean_nonzero: 0.471344
- RA interpretation: reachability-structure disruption; may destroy or delay support reachability

### frontier_dropout
- response_class: threshold_saturating_support_loss
- primary_failure_channel: support_certification_or_frontier_loss
- loss_saturation_score: 1.000000
- finality_shift_mean_nonzero: 
- recovery_length_mean_nonzero: 
- RA interpretation: direct support-frontier removal; destroys support evidence at the cut

### ledger_failure
- response_class: threshold_saturating_support_loss
- primary_failure_channel: support_certification_or_frontier_loss
- loss_saturation_score: 1.000000
- finality_shift_mean_nonzero: 0.000000
- recovery_length_mean_nonzero: 0.000000
- RA interpretation: local ledger gate failure; support certification is blocked at the witness layer

### orientation_degradation
- response_class: threshold_saturating_support_loss
- primary_failure_channel: support_certification_or_frontier_loss
- loss_saturation_score: 1.000000
- finality_shift_mean_nonzero: 0.000000
- recovery_length_mean_nonzero: 0.000000
- RA interpretation: orientation-support witness failure; certification loss without a separate reachability story

### selector_stress
- response_class: strict_channel_threshold_saturation
- primary_failure_channel: strict_commit_incompatibility_channel
- loss_saturation_score: 1.000000
- finality_shift_mean_nonzero: 0.000000
- recovery_length_mean_nonzero: 0.000000
- RA interpretation: compatibility/selector-channel stress; strict commitment can fail while selected commitment survives

### support_delay
- response_class: graded_delay_without_support_loss
- primary_failure_channel: readiness_delay_without_support_loss
- loss_saturation_score: 1.000000
- finality_shift_mean_nonzero: 3.000000
- recovery_length_mean_nonzero: 3.000000
- RA interpretation: support remains certified but reaches the site only later, shifting finality/recovery depth

## Pairwise mode separability
- edge_dropout vs support_delay: distance=12.889350, cosine=-0.053802, note=strongly_separated_signature
- selector_stress vs support_delay: distance=9.977110, cosine=0.191060, note=strongly_separated_signature
- frontier_dropout vs support_delay: distance=9.786284, cosine=0.286590, note=strongly_separated_signature
- ledger_failure vs support_delay: distance=9.786284, cosine=0.286590, note=strongly_separated_signature
- orientation_degradation vs support_delay: distance=9.786284, cosine=0.286590, note=strongly_separated_signature
- edge_dropout vs selector_stress: distance=7.140669, cosine=0.261440, note=strongly_separated_signature
- edge_dropout vs frontier_dropout: distance=6.306094, cosine=0.522880, note=strongly_separated_signature
- edge_dropout vs ledger_failure: distance=6.306094, cosine=0.522880, note=strongly_separated_signature
- edge_dropout vs orientation_degradation: distance=6.306094, cosine=0.522880, note=strongly_separated_signature
- frontier_dropout vs selector_stress: distance=3.363643, cosine=0.500000, note=strongly_separated_signature

## Support-width fragility
Only one support width appears in the analyzed output. This prevents a genuine support-width fragility curve; v0.6-level simulator development should increase support-frontier width diversity.
- support_width=1: lost_readiness_mean_nonzero=0.808510, samples=120000

## Candidate RA-native findings
1. Threshold-like severance signatures are visible when nonzero severity tiers produce nearly constant loss rates.
2. Support-delay signatures are separable when support loss remains low while readiness/commit loss and finality/recovery shift increase.
3. Selector-stress signatures are separable when strict commitment fails without support/readiness/selected-commit loss.
4. Support-width fragility cannot yet be strongly assessed unless the ensemble contains multiple support-frontier widths.
