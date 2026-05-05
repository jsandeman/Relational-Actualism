# RA v0.9.2 Native Overlap Calibration / Family-Semantics Audit Report

This packet audits the v0.9 native certificate-overlap workbench after the v0.9.1 robustness result.

## Scientific role

v0.9.2 asks whether the native-overlap rescue signature is carried uniformly across monotone support-family semantics, and whether native-overlap bins can be compared to the external certificate-correlation baseline from v0.8.1.

## Status

- Pure analysis layer.
- No Lean changes.
- No simulator semantic changes.
- Python tests included.
- Packet-local outputs are generated from the v0.9/v0.8.1 files available in this environment and should be replaced by canonical outputs after local run.

## Key expected canonical result

The expected outcome, based on the user's v0.9.1 review, is that `augmented_exact_k` remains the primary signal carrier, while `at_least_k` remains valuable as a monotone guardrail semantics but may collapse to zero rescue in `ledger_failure` slices under current metrics.
