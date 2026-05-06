# RA Track B.2 — Active Simulator Graph Witness Extraction

## Motivation

Track B.1 established a typed graph/cut witness surface and packet-local extraction. Track B.2 asks whether that extraction surface can be applied to active simulator graph states from the v0.9 native-certificate-overlap workbench.

This is a prerequisite for any future orientation-specific analysis. It is not itself an orientation-specific result.

## Extraction surface

For each active v0.9 seed state, target motif, threshold fraction, support-family semantics, and family member cut, the extractor records orientation-link tokens derived from:

- graph parent incidence into cut vertices,
- graph child incidence out of cut vertices,
- through-links parent → cut vertex → child,
- local depth / parity signatures.

The extractor deliberately avoids member-index labels. A separate bad-control tokenization appends member-index suffixes to show that such keying would be detected as unstable.

## Outputs

The main outputs are witness-member rows, family-level overlap rows, member-index audit rows, fixed-bin coverage, width/family-size estimability, and a summary.

## Interpretation

A successful Track B.2 run shows:

1. active simulator states can be used for graph/cut witness extraction;
2. witness tokens are member-index-free;
3. fixed orientation-overlap bins can be audited;
4. support-width × family-size estimability can be reported.

It does not show orientation-specific rescue.

## Relation to Track A and v1.x

Track B.2 sits downstream of Track A.3 comparison-domain validity and the v1.9 orientation-specificity retraction chain. Any future rescue analysis must satisfy those guardrails before promotion.
