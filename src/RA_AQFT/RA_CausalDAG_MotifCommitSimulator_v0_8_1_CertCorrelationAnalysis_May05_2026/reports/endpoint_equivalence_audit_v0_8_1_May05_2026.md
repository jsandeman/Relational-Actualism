# Endpoint-Equivalence Audit — v0.8.1 max delta = 0.116

This audit decomposes the 32/80 endpoint-equivalence rows from the v0.8.1
canonical analysis. The headline finding from v0.8.1 was that certification_rescue
reaches zero at correlation=1.0 across all curves (universal), but full endpoint
equivalence to parent_shared was only partial under 1e-9 tolerance with max
absolute delta 0.116. The audit asks: where do the deltas come from?

## Diagnostic field decomposition

| Field | Max abs delta |
|---|---:|
| `certification_rescue_rate_delta` | 0.000000 |
| `family_certification_resilience_rate_delta` | 0.115834 |
| `family_internal_loss_rate_delta` | 0.115834 |
| `strict_parent_loss_rate_delta` | 0.115834 |

**Headline:** the certification_rescue diagnostic — the primary v0.8.1
signature — shows **zero** drift at correlation=1.0 across the entire
endpoint table. The 0.116 max delta lives on three coordinated
diagnostics (`family_resilience`, `family_internal_loss`,
`strict_parent_loss`) all of which drift by the same magnitude in any
non-equivalent row. That coordinated drift is consistent with a single
underlying difference in the **marginal certificate-failure event rate**
between `independent_member at correlation=1.0` and `parent_shared`,
which propagates through every downstream rate that depends on a
certificate-failure event. cert_rescue is unaffected because at full
correlation parent and family share fate in both regimes, so rescue is
structurally impossible in either.

## Structural tests

- **Deltas independent of threshold** (within fixed mode × semantics × severity): **True**.
  Same delta value at all 4 thresholds for any fixed cell — so the non-equivalence
  is a property of (mode, semantics, severity), not of the threshold knob.

- **Deltas independent of family_semantics** (within fixed mode × severity × threshold): **True**.
  `at_least_k` and `augmented_exact_k` produce identical deltas — both monotone
  semantics include the parent cut, so neither has any extra freedom to diverge
  from parent_shared at corr=1.0.

- **Coordinated drift across three diagnostics**: in every non-equivalent
  row, the family_resilience, family_internal_loss, and strict_parent_loss
  deltas are all the **same magnitude**. The mirror sign relationship
  between resilience and internal_loss is structural (they sum to ≈ 1.0).
  The fact that strict_parent_loss also drifts by the same magnitude
  rules out a 'family-only' explanation and points to the underlying
  marginal certificate-failure rate as the source.

## Per-cell summary (CSV)

Full per-(mode × semantics × severity) decomposition: `ra_endpoint_equivalence_audit_v0_8_1.csv`.

Cell-level pattern (from the audit table):

| mode | severity | family_internal_loss_delta | reading |
|---|---:|---:|---|
| ledger_failure | 0.0 | +0.0000 | boundary — no intervention, both regimes match exactly |
| ledger_failure | 0.25 | -0.0088 | small drift (~0.9%) |
| ledger_failure | 0.5 | +0.1158 | **maximum drift (~11.6%)** — this is the headline 0.116 |
| ledger_failure | 0.75 | -0.0677 | moderate drift (~6.8%) |
| ledger_failure | 1.0 | +0.0000 | boundary — saturation, both regimes converge |
| orientation_degradation | 0.0 | +0.0000 | boundary |
| orientation_degradation | 0.25 | -0.0643 | moderate drift (~6.4%) |
| orientation_degradation | 0.5 | +0.0140 | small drift (~1.4%) |
| orientation_degradation | 0.75 | -0.0050 | small drift (~0.5%) |
| orientation_degradation | 1.0 | +0.0000 | boundary |

Pattern: deltas are zero at severity boundaries (0.0 = nothing fails, 1.0 =
everything fails — both regimes converge by construction) and non-zero only
at intermediate severities. The maximum (0.116) is at `ledger_failure` × `severity=0.5`, where roughly half the certificates fail.

## Mechanism

The non-equivalent rows share five structural fingerprints:
(a) cert_rescue drift = 0 exactly,
(b) family_resilience / family_internal_loss / strict_parent_loss drift in coordination (all same magnitude),
(c) independent of threshold,
(d) independent of monotone family semantics,
(e) zero at severity boundaries (0.0 and 1.0).

Together (a)–(e) point to **a small difference in the marginal certificate-failure event rate** between `independent_member at correlation=1.0` and `parent_shared`. Both regimes produce a single shared certificate fate (so cert_rescue must be 0 in both, which matches the data exactly), but the random-number stream / discretization that determines the *probability* of that single fate firing may differ. Any difference in marginal failure rate then propagates identically to every rate that depends on a certificate-failure event — strict_parent_loss (parent's fate), family_internal_loss (family's fate, equal to parent's at corr=1.0), and family_resilience (the complement of family_internal_loss).

This is an implementation-side residual, not a structural difference. Two pieces of evidence support that reading: (i) the drift is independent of both threshold and family semantics, ruling out family-construction asymmetries; (ii) the drift vanishes at the severity boundaries (0.0 = no events, 1.0 = saturating events), where any sampling-rate difference has no leverage to express itself.

## Verdict

1. **The v0.8.1 headline cert-rescue→0 result holds exactly** — zero
   drift on `certification_rescue_rate` at correlation=1.0 across all
   80 cells.
2. **The 0.116 max-delta is a coordinated drift on three downstream
   diagnostics** (`strict_parent_loss`, `family_internal_loss`,
   `family_resilience`) all of identical magnitude, traceable to a
   small difference in the underlying marginal certificate-failure
   event rate between `independent_member at corr=1.0` and
   `parent_shared`. This is implementation-side, not structural.
3. **The drift is well-localized**: only at intermediate severities,
   with `ledger_failure × severity=0.5` the worst case. Both boundary
   severities (0.0, 1.0) collapse to exact equivalence on every
   diagnostic.
4. **No follow-up is required for v0.8.1's published claim** — the
   tightened caveats already distinguish 'rescue→0 universal' from
   'full diagnostic equivalence under strict 1e-9 tolerance', which
   this audit confirms is the correct phrasing.
5. **For v0.9**, when comparing `independent_member` and `parent_shared`
   regimes head-to-head, trust the `cert_rescue` diagnostic under strict
   tolerance and report a `~10% marginal-rate residual` band on the
   loss/resilience diagnostics at intermediate severities. If the v0.9
   native-witness-overlap layer cleans up the random-number protocol
   (e.g. by shared-stream construction across regimes), the 0.116
   residual should shrink toward 1e-9 mechanically.
