# RA Causal-DAG Motif-Commit Simulator v1.2 — Distinct Orientation-Link Surface

This packet addresses the v1.1 finding that the v0.9/v1.0 component layer had
an exact confounding:

```text
support_overlap = frontier_overlap = orientation_overlap
```

v1.2 introduces a **separately keyed orientation-link/sign-source surface** and
audits whether orientation-degradation rescue can vary with orientation-link
overlap while support/frontier overlap is held fixed.

## Status

This is a focused simulator/analysis refinement plus a conservative Lean-facing
surface.  It does not derive the orientation-link surface from the full native
orientation stack yet, and it does not assert a numerical rescue law in Lean.

## Run

```bash
python scripts/run_orientation_link_surface_v1_2.py   --input-dir ../RA_CausalDAG_MotifCommitSimulator_v1_0_NativeCertificateAnchoring_May05_2026/outputs   --output-dir outputs
```

## Success criteria

1. `orientation_link_overlap` is no longer numerically identical to `support_overlap` / `frontier_overlap`.
2. Matched support/frontier strata contain multiple orientation-link bins.
3. `orientation_degradation` rescue decreases as orientation-link overlap increases.
4. `ledger_failure` remains a ledger-control channel.
5. `selector_stress` remains outside certification rescue.
6. `augmented_exact_k` remains the primary signal-carrier and `at_least_k` remains the guardrail semantics.

## Interpretation guardrail

The v1.2 orientation-link surface is a prototype distinct surface.  It should be
replaced or constrained by `RA_CausalOrientation_Core`,
`RA_D1_NativeLedgerOrientation`, and related native orientation/closure modules
before making stronger Nature-facing claims.
