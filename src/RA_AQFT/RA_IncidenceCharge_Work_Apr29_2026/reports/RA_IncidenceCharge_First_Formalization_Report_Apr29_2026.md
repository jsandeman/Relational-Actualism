# RA Incidence Charge First Formalization Report — Apr 29 2026

`RA_IncidenceCharge_v1.lean` was generated as the next theorem step after the compile-confirmed finite Hasse-frontier existence layer.

Static scan:

```text
sorry: 0
admit: 0
axiom: 0
```

Lean source SHA-256:

```text
b26a38234037419b6ec66f6e23d7534bf4af5bb71f523b5ff3c5cca532325d1e
```

Main formal objects:

```text
OrientedFrontierLink
IncidenceSignSource
SignedFrontierLink
SignedN1ThreeFrame
ThreeDirectionalIncidenceBoundary
```

Main lemmas:

```text
signSource_deterministic
sevenCharge_of_three_incidence_signs
signedN1ThreeFrame_qN1_seven
signedThreeFrameOfSource_qN1_seven
ledgerOfThreeDirectionalBoundary_qN1_seven
```

The file is intentionally conditional: it does not derive `IncidenceSignSource`.  It isolates the next hard theorem: finite Hasse frontier plus oriented boundary/incidence structure should produce the sign-source function.
