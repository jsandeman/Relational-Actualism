# Track B.1 — Native Graph/Cut Orientation Witness Extraction

This packet starts Track B after the Track A formal chain.  It does **not** add a
new rescue claim.  It defines and tests a graph/cut-local orientation witness
surface that is derived from DAG incidence around support-family member cuts.

## Scope

- No probability law.
- No orientation-specific rescue claim.
- No re-opening of v1.5.
- No member-index labels in the witness surface.

The central aim is to replace arbitrary row/member keying with a graph/cut-local
witness interface that can later be tied to RA's native orientation, ledger,
closure, and graph-cut modules.

## Lean bridge

`RA_MotifNativeGraphCutWitnessExtraction.lean` imports:

```lean
import RA_MotifComparisonDomainValidity
import RA_GraphOrientationClosure
```

It defines `GraphCutOrientationWitness`, which packages:

- a `GraphSupportCut`,
- a `GraphOrientationClosureCertificate`,
- an `OrientedN1ThreeFrame`,
- a predicate selecting oriented frontier links for the member witness,
- graph/cut-locality and no-member-index methodological fields.

Theorems prove only refinement/accessor facts: induced sign-source evaluation,
seven-value N1 ledger inheritance, graph-cut-derived accessor, no-member-index
accessor, and overlap-profile guardrails.

## Python extractor

The Python extractor builds witness tokens from graph incidence around the cut:

- incoming edges into cut vertices,
- outgoing edges from cut vertices,
- through links parent → cut vertex → child,
- depth/local parity signatures.

A bad member-indexed control is included only to verify that the Track B surface
is independent of family-member ordering.

## Correct interpretation

This is a witness-extraction surface.  It prepares future matched-graph analyses
but does not itself validate orientation-specific certification rescue.
