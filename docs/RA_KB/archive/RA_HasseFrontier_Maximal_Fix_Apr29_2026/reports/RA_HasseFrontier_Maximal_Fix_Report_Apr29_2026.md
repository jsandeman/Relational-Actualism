# RA_HasseFrontier_Maximal_v1 Lean fix report — Apr 29 2026

## Problem

Lean rejected:

```lean
theorem maximalReachableAboveOfTopoMax ... : MaximalReachableAbove P x := ...
```

because `MaximalReachableAbove P x` is a structure/data type, not a proposition. In Lean, `theorem` declarations are for propositions; constructions returning data should be `def`.

The rejected declaration also caused the downstream unknown-constant error at `maximalCertificateOfTopoMax`.

## Fix

Changed:

```lean
theorem maximalReachableAboveOfTopoMax
```

to:

```lean
def maximalReachableAboveOfTopoMax
```

and adjusted the comment to make clear that this is a data-construction lemma/certificate constructor.

## Conceptual impact

No mathematical content changed. The declaration still constructs a `MaximalReachableAbove` certificate from a `TopoMaxCertificate`; it is simply declared with the correct Lean declaration kind.

## Recommended status

Before local compile:

```text
static_no_sorry_no_admit_no_axiom_build_pending
```

After successful local compile and full Lake build:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
```

No RAKB conceptual update is needed until the corrected file compiles.
