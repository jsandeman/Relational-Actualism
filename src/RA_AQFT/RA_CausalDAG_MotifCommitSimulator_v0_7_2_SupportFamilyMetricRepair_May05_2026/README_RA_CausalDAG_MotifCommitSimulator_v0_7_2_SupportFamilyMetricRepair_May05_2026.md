# RA Causal-DAG Motif-Commit Simulator v0.7.2 — Support-Family Metric Repair

This packet is a corrective analysis layer over v0.7 / v0.7.1. It introduces no new RA ontology and no new Lean module. It repairs the metric interpretation around support-cut families by separating three quantities that were previously too easy to conflate:

```text
strict-parent loss
  the original parent support cut loses readiness

family-internal loss / survival
  the support-cut family loses or preserves any-cut readiness

strict rescue
  the strict parent cut fails while some family member survives
```

The motivating audit showed that the earlier reading “exact-k support families can amplify ledger/orientation certification failure” was largely a metric-definition artifact. In exact-k / cut-level certification modes, when the parent cut is absent from `family.cuts`, strict parent loss and family-member loss are not apples-to-apples. This packet flags those rows explicitly rather than allowing aggregate comparisons to blur them.

## New module

```text
simulator/ra_causal_dag_support_family_metric_repair.py
```

The module keeps v0.7.1 intervention semantics unchanged and adds metric fields:

```text
parent_cut_in_family
parent_targeted_by_intervention
family_targeted_by_intervention
targeting_domain
strict_parent_loss
family_internal_loss
strict_rescue_rate_event
family_internal_survival
family_internal_resilience_event
comparison_valid_strict_vs_family
metric_artifact_risk
apples_to_apples_loss_delta
certified_family_member_count
uncertified_family_member_fraction
```

## Interpretation discipline

This packet should be read as a corrigendum layer:

```text
wrong / too coarse:
  family_loss > strict_loss ⇒ exact-k structurally amplifies certification failure

correct:
  strict-parent and family-member losses must be compared only when they share a targeting domain;
  otherwise use family-internal survival/resilience metrics.
```

## Validation

Packet-local tests:

```text
Ran 6 tests
OK
```

## Included demo run

Packet-local run:

```text
seeds=17..20
steps=16
modes=edge_dropout, frontier_dropout, ledger_failure, orientation_degradation, selector_stress, support_delay
thresholds=1.0, 0.75, 0.5, 0.25
family_semantics=exact_k, at_least_k, augmented_exact_k
certification_regimes=cut_level, parent_shared
actual_evaluations=46,080
```

Demo summary:

```text
support_width_classes=[1,2,3,4]
comparison_valid_rate=0.989149
metric_artifact_risk_rate=0.008681
strict_parent_losses=26,917
family_internal_losses=25,618
strict_rescues=1,439
family_internal_resilience_events=5,102
```

## Outputs

```text
ra_support_family_metric_repair_summary_v0_7_2.csv
ra_support_family_metric_repair_runs_v0_7_2.csv
ra_support_family_apples_to_apples_v0_7_2.csv
ra_support_family_width_stratified_metrics_v0_7_2.csv
ra_support_family_targeting_audit_v0_7_2.csv
ra_support_family_certification_resilience_v0_7_2.csv
ra_support_family_metric_artifact_flags_v0_7_2.csv
ra_support_family_metric_repair_sample_v0_7_2.csv
ra_support_family_metric_repair_summary_v0_7_2.md
ra_support_family_metric_repair_state_v0_7_2.json
```

## Canonical run recommendation

```bash
python scripts/run_support_family_metric_repair_v0_7_2.py \
  --seed-start 17 \
  --seed-stop 117 \
  --steps 32 \
  --max-targets 12 \
  --sample-limit 5000 \
  --threshold-fractions 1.0,0.75,0.5,0.25 \
  --family-semantics exact_k,at_least_k,augmented_exact_k \
  --certification-regimes cut_level,parent_shared \
  --output-dir outputs
```

The key canonical criteria are:

```text
1. metric_artifact_risk rows appear only where cut-level certification targets family members while the parent is absent from family.cuts.
2. apples_to_apples_loss_delta is computed only for valid targeting-domain comparisons.
3. certification-channel resilience is measured by family_internal_survival / family_internal_resilience, not strict_rescue alone.
4. selector_stress remains separate from support-family rescue.
```
