# RA Causal-DAG Motif-Commit Simulator v0.8 — Independent Certified Support Families

This packet introduces the v0.8 independent certified support-family workbench.

## Purpose

v0.7 showed that support-cut families can provide support/readiness resilience, but v0.7.2 clarified that strict-parent rescue and family-internal resilience must be measured separately. v0.8 asks the next RA-native question:

> Can support-family alternatives rescue ledger/orientation certification failure when family members carry independent or partially correlated certification witnesses?

## Status

- Python simulator layer: validated packet-local run.
- Lean bridge: source-level formal bridge pending local compile.
- New RA ontology: none asserted as Nature-level law.
- Methodological stance: RA-native diagnostics first; inherited-theory language excluded from the operational layer.

## Core distinction

v0.8 compares three certification regimes:

```text
parent_shared
  one parent certificate gates the strict parent cut and all family members

cut_level
  family-member cuts are targeted as a set, preserving the v0.7/v0.7.2 audit surface

independent_member
  strict parent and family members receive member-level certificate fates
```

The `independent_member` regime sweeps:

```text
certificate_correlation ∈ {0.0, 0.25, 0.5, 0.75, 1.0}
```

where:

```text
0.0 = member certificate failures are independent
1.0 = member certificate failures share one fate
```

The marginal failure probability of each certificate remains severity-controlled.

## Outputs

The run writes:

```text
ra_independent_cert_family_summary_v0_8.csv
ra_independent_cert_family_runs_v0_8.csv
ra_independent_cert_family_aggregate_v0_8.csv
ra_certification_correlation_sweep_v0_8.csv
ra_certification_resilience_by_regime_v0_8.csv
ra_independent_cert_family_by_width_v0_8.csv
ra_independent_cert_selector_guardrail_v0_8.csv
ra_independent_cert_family_evaluations_sample_v0_8.csv
ra_independent_cert_family_predictions_v0_8.md
ra_independent_cert_family_state_v0_8.json
```

## Packet-local validation

Unit tests:

```text
Ran 6 tests
OK
```

Packet-local demo:

```text
run_count = 2
steps = 12
actual_evaluations = 8,640
support_width_classes = [1, 2, 4]
certification_regimes = [cut_level, independent_member, parent_shared]
certificate_correlations = [0.0, 0.5, 1.0]
certification_rescues = 56
family_certification_resilience_events = 718
selector support-family rescue events = 0
```

## Recommended canonical run

```bash
python scripts/run_independent_certified_families_v0_8.py \
  --seed-start 17 \
  --seed-stop 117 \
  --steps 32 \
  --max-targets 12 \
  --sample-limit 5000 \
  --threshold-fractions 1.0,0.75,0.5,0.25 \
  --family-semantics at_least_k,augmented_exact_k \
  --certification-regimes parent_shared,cut_level,independent_member \
  --certificate-correlations 0.0,0.25,0.5,0.75,1.0 \
  --output-dir outputs
```

## Main scientific criteria

1. Parent-shared certification should not rescue parent-certificate failure.
2. Independent-member certification should produce certification rescue in ledger/orientation modes when alternative certified family members survive.
3. Certification rescue should decline as certificate correlation approaches 1.
4. Selector stress should remain outside support-family certification rescue.
5. Support-route resilience and certification-witness resilience should remain distinct diagnostics.

## Formal bridge

The packet includes:

```text
lean/RA_MotifCertifiedSupportFamilyBridge.lean
```

It imports:

```lean
import RA_MotifSupportFamilyMonotonicity
```

and defines abstract certificate-family contexts:

```text
DAGFamilyCertificateContext
DAGIndependentCertifiedFamilyReadyAt
GraphFamilyCertificateContext
GraphIndependentCertifiedFamilyReadyAt
```

The bridge intentionally stays abstract: concrete member-distinct certificates still need to be justified by BDG-LLC / frontier / orientation / ledger evidence.
