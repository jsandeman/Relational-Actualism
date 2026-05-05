# Simulator-to-Lean Bridge: v0.9 Native Certificate Overlap

Lean module: `RA_MotifNativeCertificateOverlapBridge.lean`

Simulator object mapping:

```text
NativeCertificateWitness
  ↔ Type-valued witness Q in DAG/GraphNativeCertificateOverlapContext

native overlap relation / components
  ↔ overlaps Q Q' abstract relation

native-overlap-induced readiness
  ↔ DAG/GraphNativeOverlapCertifiedFamilyReadyAt
```

The Lean bridge does not fix numerical overlap or probability. It only asserts
that native witness data can refine the v0.8 independent certified-family
readiness predicate.
