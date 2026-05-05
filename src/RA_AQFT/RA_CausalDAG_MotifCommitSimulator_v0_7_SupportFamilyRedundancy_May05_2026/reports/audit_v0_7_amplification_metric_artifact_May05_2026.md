# Audit: v0.7 cert-channel "amplification" (SUPPORT-FAMILY-005) — exact-k vs metric-definition

Date: 2026-05-05
Subject: RA-SIM-SUPPORT-FAMILY-005 "Exact-threshold subfamilies can amplify
certification-channel fragility" — and the related "0% rescue on cert modes"
reading of RA-SIM-SUPPORT-FAMILY-004.

## Methodology

The original finding compared **aggregate** `strict_readiness_loss_rate`
(0.439) to aggregate `family_readiness_loss_rate` (0.817) at
ledger_failure / severity 0.75 / threshold 0.25 in the canonical 100-seed
v0.7 run, and reported "family worsens cert failure".

This audit decomposes those rates by support_width to separate:
- **Exact-k structural effects** — real properties of how the
  exact-threshold subfamily operator interacts with cert-mode sampling.
- **Metric-definition effects** — artifacts of comparing two rates whose
  denominators measure different things.

## Provenance of the 0.439 vs 0.817 gap

Width-stratified breakdown at ledger_failure / sev 0.75 / threshold 0.25:

| width | n    | strict_loss | family_loss | parent ∈ family? | family content |
| :---: | ---: | ----------: | ----------: | :--------------: | -------------- |
| 1     | 1054 | 1.000       | 1.000       | yes              | family = {parent} (k=1, width=1) |
| 2     |  430 | 0.000       | 1.000       | no               | 2 singleton 1-subsets; both uncertified at sev 0.75 |
| 3     |  476 | 0.000       | 1.000       | no               | 3 singleton 1-subsets; all uncertified at sev 0.75 (`ceil(3·0.75)=3`) |
| 4     |  440 | 0.000       | 0.000       | no               | 4 singleton 1-subsets; 3 uncertified, 1 reachable |

- Aggregate `strict_loss = 1054 / 2400 = 0.4392` — **entirely from width=1**.
- Aggregate `family_loss = (1054 + 430 + 476 + 0) / 2400 = 0.8167`.

The strict_loss baseline is artificially low because for **every cohort
with width ≥ 2 at threshold < 1.0**, the parent cut is *not* a member of
`family.cuts`. Cert modes (`ledger_failure`, `orientation_degradation`)
sample `uncertified ⊆ family.cuts` and do not change reachability.
Therefore `strict_uncertified ≡ False` and `strict_lost_readiness ≡ False`
**by construction** in those cohorts.

## (A) Metric-definition artifact

`strict_lost_readiness` measures the parent cut's fate; `family_lost_readiness`
measures family-of-k-subsets survival. At threshold < 1.0 and width ≥ 2:
- the parent is excluded from `family.cuts`;
- cert modes can damage family members without touching the parent;
- so the two rates are **not measuring the same event**.

Comparing them produces the "amplification" gap mechanically. This gap
is **not a property of redundancy**; it is a property of comparing two
metrics whose intersection is non-trivial.

The same artifact afflicts the "0% rescue on cert modes" reading
(SUPPORT-FAMILY-004): `family_rescue_rate` requires `strict_lost ∧
family_after_ready`. At width ≥ 2 / cert mode / threshold < 1.0,
`strict_lost` is structurally false, so rescue counts to zero — even
when the family genuinely survives. **The rescue metric is structurally
blind to cert-channel resilience at width ≥ 2.**

## (B) Genuine exact-k effects (apples-to-apples comparison)

The right comparison for "does redundancy help here" is `family_loss` at
threshold = 1.0 (where family = {parent}) versus `family_loss` at
threshold < 1.0 (where family = subsets), within a fixed width slice
and severity.

For ledger_failure / width ≥ 2 / sev 0.75:

| threshold | family_loss | reading |
| :---: | ---: | --- |
| 1.00 | 1.000 | family = {parent}; parent always uncertified at sev 0.75 |
| 0.75 | 1.000 | for w∈{2,3}, k=width so family={parent}, same outcome; for w=4, k=3 with 4 cuts, sev 0.75 → all uncertified |
| 0.50 | 0.673 | resilience appears at w=4 (k=2, 6 cuts, 5 uncertified, 1 reachable 2-subset); w∈{2,3} still all-fail |
| 0.25 | 0.673 | resilience persists for w=4; w∈{2,3} still all-fail |

So the *family_loss-vs-threshold* curve at fixed width ≥ 2 is **monotonically
non-increasing as threshold drops**, including in cert modes. There is no
genuine amplification.

The only exact-k effect that does emerge: cert-mode resilience requires
sufficient width relative to threshold so that `severity · family_size <
family_size − 1`, i.e. at least one family member survives sampling.
Below that boundary, family_loss tracks 1.0 regardless of threshold. This
is a real structural property of exact-threshold subfamilies + cut-level
cert sampling, but it is "less rescue at high severity", not amplification.

## Verdict

1. **SUPPORT-FAMILY-005 (amplification) is largely retracted.** The
   width-stratified comparison shows family_loss is non-increasing as
   threshold decreases in cert modes too. The original aggregate
   "0.44 vs 0.82" reading mixed metrics with structurally different
   denominators.

2. **SUPPORT-FAMILY-004's "0% cert rescue" reading is amended.** The
   `rescue_rate` metric is structurally blind to cert-channel
   resilience at width ≥ 2 (because `strict_lost` is false there by
   construction). Reachability/availability modes show rescue because
   strict can fail; cert modes don't, but family still benefits from
   threshold reduction — invisible to this metric.

3. **The right metric** for cross-channel comparison is
   `family_loss(threshold | width, severity)` within fixed width and
   severity slices, not `strict_loss vs family_loss` and not
   `rescue_rate`.

4. **A genuine exact-k structural effect remains:** at fixed width ≥ 2
   and high severity, cert-mode resilience requires sufficient family
   size that severity-sampling does not exhaust the family. Until that
   threshold is reached, family_loss tracks 1.0; after it, family_loss
   drops abruptly. This is a property of exact-threshold subfamilies +
   cut-level cert sampling that the rescue metric obscures.

## Recommended RAKB amendments

- New claim **RA-SIM-SUPPORT-FAMILY-006** records the audit corrigendum
  (cert-channel resilience is real and is monotone in threshold, not
  amplified). Supersedes SF-005's interpretation.
- New claim **RA-SIM-SUPPORT-FAMILY-007** records the metric-blindness
  of `rescue_rate` to cert-channel resilience.
- New framing **RA-SIM-SUPPORT-FAMILY-METHOD-004** records the
  apples-to-apples discipline for future comparison-metric design.
- SF-004 and SF-005 remain in the registry as provenance — they record
  the rates as measured. Their interpretations are amended by SF-006/007.

## Recommended next-step v0.8 work

A `family_loss(threshold)` slice within width-stratified data is the
diagnostic to publish; the strict-vs-family aggregate is misleading on
its own. Future packets should also report a "metric-blind" diagnostic
flag that fires when `rescue_rate = 0` while
`family_loss < strict_loss-comparable` in some apples-to-apples sense.
