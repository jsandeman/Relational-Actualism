# RA Causal-DAG Motif Commit Simulator v1.9 — Certification Resilience Synthesis

This packet is **synthesis-only**. It introduces no new simulator semantics, no new Lean module, and no new audit. Its purpose is to consolidate the v0.x / v1.x simulator chain into one place so future sessions do not accidentally resurrect retracted findings (in particular the v1.5 orientation-specific certification-rescue interpretation).

## Why this packet exists

The v1.5 → v1.6 → v1.7 → v1.8 → v1.8.1 audit chain landed a strong, cleanly-documented negative result on orientation-specific certification rescue. That negative result is easy to mis-cite back into a positive one if the chain is split across many caveats. v1.9 collects the chain into four documents that future sessions can read in any order:

```text
ra_confirmed_resilience_signatures_v1_9.md
  Robust positive findings from v0.5.x .. v1.8.1, with cell-level
  citations to the controlling claim IDs.

ra_retracted_orientation_specificity_chain_v1_9.md
  Narrative timeline of v1.5 .. v1.8.1 with the methodological pivots
  (witness-keying bug, member_idx regression, joint stratification,
  fixed-bin discipline).

ra_open_native_witness_requirements_v1_9.md
  What would be required, methodologically and data-wise, to revisit
  orientation-specific certification rescue without restarting the same
  confound chain.

ra_v1_series_epistemic_status_matrix.csv
  Per-packet status table: principal claim, status (confirmed_robust /
  superseded / retracted / methodological_only / pending), key caveat,
  controlling claim IDs, last audit event.
```

## Generator

`scripts/build_status_matrix.py` reads `docs/RA_KB/registry/claims.yaml` and `audit_events.csv`, applies a small per-packet rule table (in the script), and emits `ra_v1_series_epistemic_status_matrix.csv`. Re-run when claims change.

## Discipline going forward

Two rules from this synthesis:

1. **Cite the synthesis, not the chain**. When citing the orientation-overlap result in papers, cite `ra_retracted_orientation_specificity_chain_v1_9.md` and the framing entry `RA-SIM-V1-SERIES-SYNTHESIS-METHOD-001`. Do NOT pull v1.5 +0.028 or any pre-v1.8.1 reading directly.
2. **Fixed-bin discipline** (`RA-SIM-CONFOUND-METHOD-001` rule (f)). For orientation-overlap rescue claims, bins used to define the tested signal must remain fixed across confound controls. If joint strata lack both low and high bins under that fixed definition, the signal is non-estimable rather than rescued by local re-binning.

## Scope

In scope: simulator-side v0.5.x .. v1.8.1 epistemic status; the orientation-overlap rescue chain; the certification-rescue / certificate-correlation positive line; the Lean v1.0/v1.2/v1.3/v1.4/concrete-graph qualitative bridges.

Out of scope: Lean kernel proofs (RA-KERNEL-* and RA_AmpLocality), Papers I-IV bibliography, RAKB schema; those have their own provenance.
