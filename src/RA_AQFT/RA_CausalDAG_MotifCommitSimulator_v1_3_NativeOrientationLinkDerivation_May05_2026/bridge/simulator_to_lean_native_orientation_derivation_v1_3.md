# Simulator-to-Lean Bridge: v1.3 Native Orientation-Link Derivation

The simulator side computes a native orientation-link overlap surface from a Lean theorem/sign-source manifest. The Lean side provides an abstract refinement structure:

```text
native orientation catalog evidence
  → orientation-link evidence
  → generic orientation component evidence
```

This bridge is qualitative. Numerical overlap scores and rescue diagnostics remain simulator-side.

The intended future direction is to replace theorem-catalog token selection with per-graph orientation-link witness extraction from native RA structures.
