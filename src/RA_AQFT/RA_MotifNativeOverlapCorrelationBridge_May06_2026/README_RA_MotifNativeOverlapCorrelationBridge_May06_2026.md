# RA_MotifNativeOverlapCorrelationBridge — May 06 2026

This packet adds a narrow Track A Lean bridge connecting qualitative native certificate-overlap evidence to the certificate-fate / certificate-correlation vocabulary introduced by `RA_MotifCertificateCorrelationBridge`.

## Contents

```text
lean/RA_MotifNativeOverlapCorrelationBridge.lean
docs/RA_MotifNativeOverlapCorrelationBridge_May06_2026.md
bridge/native_overlap_to_certificate_correlation_bridge.md
patches/patch_lakefile_add_RA_MotifNativeOverlapCorrelationBridge.diff
reports/source_audit_RA_MotifNativeOverlapCorrelationBridge_May06_2026.log
registry_proposals/*
```

## Local compile

```bash
lake env lean RA_MotifNativeOverlapCorrelationBridge.lean
lake build RA_MotifNativeOverlapCorrelationBridge
```

## Status

Source-level pending local compile in this environment. Source audit contains no `sorry`, `admit`, or `axiom` declarations.

## Scope discipline

This bridge does not assert probability, monotone decay, external-correlation calibration, or orientation-specific rescue. It only records qualitative refinement structure.
