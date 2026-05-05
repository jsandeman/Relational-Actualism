# RA Independent Certified Support Families — v0.8

This workbench tests certification-witness redundancy. It distinguishes parent-shared, cut-level, and independent-member certificate regimes and sweeps certificate correlation.

## Scale

- run_count: 100
- steps: 32
- actual_evaluations: 4032000
- support_width_classes: [1, 2, 3, 4]
- certification_regimes: ['cut_level', 'independent_member', 'parent_shared']
- certificate_correlations: [0.0, 0.25, 0.5, 0.75, 1.0]

## Reading

Independent-member certification is the first simulator regime in this line that can rescue ledger/orientation certificate failure through alternative certified family members. Parent-shared certification should not rescue a parent-certificate failure, and rescue should decline as certificate correlation approaches one.

## Highest independent-member certification rescue rows

- mode=orientation_degradation semantics=at_least_k sev=0.75 threshold=0.25 corr=0.0: cert_rescue=0.319167 family_cert_resilience=0.510417 loss=0.489583
- mode=ledger_failure semantics=at_least_k sev=0.75 threshold=0.25 corr=0.0: cert_rescue=0.312917 family_cert_resilience=0.592917 loss=0.407083
- mode=orientation_degradation semantics=at_least_k sev=0.75 threshold=0.5 corr=0.0: cert_rescue=0.300833 family_cert_resilience=0.475417 loss=0.524583
- mode=orientation_degradation semantics=augmented_exact_k sev=0.75 threshold=0.5 corr=0.0: cert_rescue=0.289167 family_cert_resilience=0.455833 loss=0.544167
- mode=orientation_degradation semantics=at_least_k sev=0.75 threshold=0.25 corr=0.25: cert_rescue=0.277917 family_cert_resilience=0.534583 loss=0.465417
- mode=orientation_degradation semantics=at_least_k sev=0.5 threshold=0.25 corr=0.0: cert_rescue=0.264583 family_cert_resilience=0.740833 loss=0.259167
- mode=orientation_degradation semantics=augmented_exact_k sev=0.5 threshold=0.25 corr=0.0: cert_rescue=0.261667 family_cert_resilience=0.725 loss=0.275
- mode=orientation_degradation semantics=augmented_exact_k sev=0.75 threshold=0.25 corr=0.0: cert_rescue=0.25875 family_cert_resilience=0.443333 loss=0.556667
- mode=ledger_failure semantics=at_least_k sev=0.75 threshold=0.5 corr=0.0: cert_rescue=0.252917 family_cert_resilience=0.537083 loss=0.462917
- mode=ledger_failure semantics=augmented_exact_k sev=0.75 threshold=0.5 corr=0.0: cert_rescue=0.247917 family_cert_resilience=0.53 loss=0.47

## Correlation sweep slice: independent_member, severity=0.5, threshold=0.5

- mode=ledger_failure corr=0.0: rescue=0.2075 resilience=0.795833 loss=0.204167
- mode=ledger_failure corr=0.0: rescue=0.197917 resilience=0.795833 loss=0.204167
- mode=ledger_failure corr=0.25: rescue=0.159167 resilience=0.660417 loss=0.339583
- mode=ledger_failure corr=0.25: rescue=0.164583 resilience=0.660417 loss=0.339583
- mode=ledger_failure corr=0.5: rescue=0.106667 resilience=0.5725 loss=0.4275
- mode=ledger_failure corr=0.5: rescue=0.112083 resilience=0.5725 loss=0.4275
- mode=ledger_failure corr=0.75: rescue=0.099583 resilience=0.566667 loss=0.433333
- mode=ledger_failure corr=0.75: rescue=0.0775 resilience=0.566667 loss=0.433333
- mode=ledger_failure corr=1.0: rescue=0.0 resilience=0.423333 loss=0.576667
- mode=ledger_failure corr=1.0: rescue=0.0 resilience=0.423333 loss=0.576667
- mode=orientation_degradation corr=0.0: rescue=0.244167 resilience=0.727083 loss=0.272917
- mode=orientation_degradation corr=0.0: rescue=0.246667 resilience=0.727083 loss=0.272917
- mode=orientation_degradation corr=0.25: rescue=0.197083 resilience=0.653333 loss=0.346667
- mode=orientation_degradation corr=0.25: rescue=0.17375 resilience=0.653333 loss=0.346667
- mode=orientation_degradation corr=0.5: rescue=0.094167 resilience=0.66375 loss=0.33625
- mode=orientation_degradation corr=0.5: rescue=0.102083 resilience=0.66375 loss=0.33625
- mode=orientation_degradation corr=0.75: rescue=0.054167 resilience=0.421667 loss=0.578333
- mode=orientation_degradation corr=0.75: rescue=0.060417 resilience=0.421667 loss=0.578333
- mode=orientation_degradation corr=1.0: rescue=0.0 resilience=0.475 loss=0.525
- mode=orientation_degradation corr=1.0: rescue=0.0 resilience=0.475 loss=0.525

## Selector guardrail

- Selector stress produced no support-family certification rescue events in this run.

## RAKB caution

The certification-correlation model is exploratory. The RA-native claim is not that Nature uses this stochastic mechanism; the claim is that certification-level support-family resilience requires member-distinct certificates or equivalent native witnesses rather than a shared parent certificate.
