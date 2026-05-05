# Simulator-to-Lean Bridge — v0.8 Independent Certified Support Families

The simulator's `independent_member` regime corresponds to the abstract Lean notion:

```text
DAGFamilyCertificateContext.certifies Q
GraphFamilyCertificateContext.certifies Q
```

The Lean bridge does not formalize probability, correlation, or sampling. It records the structural relation:

```text
certified member cut + ReadyAt
  ⇒ independent certified-family readiness
  ⇒ ordinary certified-family readiness
  ⇒ ordinary support-family readiness
```

Simulator fields map as follows:

```text
family.cuts                         ↔ SupportCutFamily.cuts
certified family member             ↔ Ξ.certifies Q
family_after_ready                  ↔ IndependentCertifiedFamilyReadyAt
family_certification_resilience     ↔ existence of a certified-ready member after certificate-channel stress
certificate_correlation             ↔ simulator parameter only, not Lean formalized
```

The key methodological restriction is:

```text
Certification rescue is not route rescue.
```

A family can rescue ledger/orientation failure only if there is a member-distinct certificate or a native equivalent witness for an alternative family member.
