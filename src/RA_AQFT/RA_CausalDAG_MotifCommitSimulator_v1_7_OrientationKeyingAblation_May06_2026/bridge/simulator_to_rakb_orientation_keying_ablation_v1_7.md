# Simulator-to-RAKB bridge: v1.7 orientation-keying ablation

v1.7 should be recorded as a diagnostic packet. It tests whether the v1.6 matched-graph result depends on member-indexed orientation-link tokenization.

Suggested framing:

- Treat `member_indexed_edge_pair` as the v1.6 provenance control.
- Treat non-member graph keyings as the first real matched-graph ablation.
- Do not promote reverse orientation specificity unless it survives multiple non-member keyings and a larger matched-graph run.
