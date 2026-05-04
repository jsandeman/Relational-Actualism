# RA Frontier / Incidence Normal Form — First Formalization Report

## Summary

This packet advances the Selector Closure theorem ladder from abstract selector vocabulary to a first frontier/incidence vocabulary.

The generated Lean file is:

```text
RA_FrontierIncidence_v1.lean
```

It imports:

```lean
import RA_ActualizationSelector_v1
```

so it should be copied into the same Lean source directory as the already-compiled selector scaffold.

## What it formalizes

The file defines:

```text
CausalOrder
CandidatePast
Frontier
IncidenceSign
SevenCharge
BoundaryLedger
CandidateBoundaryData
FrontierNormalForm
CandidateWeight
NormalFormInvariantWeight
FrontierConstraintClosureData
```

It proves:

```text
boundaryLedger_qN1_seven
frontier_physically_equiv_of_same_data
same_data_of_frontier_physically_equiv
same_weight_of_same_frontier_data
selectorClosureDataOfFrontierData
selectorFromFrontierClosureData
weak_frontier_selector_closure
```

## Interpretation

This file does not assert that candidate histories are quotientable. It says that if a frontier-normal-form package is supplied, then equality of frontier-boundary data can encode a specified physical-equivalence relation. This keeps Joshua's no-actual-history-quotient principle intact.

## Compile status

This file is generated as a conservative Lean scaffold, but it has not been locally compiled in this environment because Lean/Lake is unavailable here.

Recommended local check:

```bash
cp RA_FrontierIncidence_v1.lean src/RA_AQFT/
cd src/RA_AQFT
lake env lean RA_FrontierIncidence_v1.lean
```

Recommended registry status before local compile:

```text
static_no_sorry_no_admit_no_axiom_build_pending
```

After successful local compile:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
```
