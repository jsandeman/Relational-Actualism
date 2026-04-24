# RA Native Root Proposal v1

## Goal

Define a Lean root set that can be presented, audited, and extended without relying on bridge modules or legacy theory-language overlays.

## Proposed native root (target state)

- `RA_GraphCore`
- `RA_AmpLocality`
- `RA_O14_Uniqueness_Core`
- `RA_D1_Core`

## Why this root

These modules stay closest to the framing primitives:

- DAG / causal precedence
- BDG integers and BDG score
- actualization filter structure
- LLC / graph cuts
- amplitude locality
- arithmetic uniqueness of the d=4 BDG coefficients
- motif closure / confinement / winding / irreversibility in N-vector language

## Modules to exclude from the native root

- `RA_AQFT_Proofs_v10`
- `RA_Koide`
- `RA_Spin2_Macro`
- full unsplit `RA_D1_Proofs`
- coupling/alpha overlays in `RA_O14_Uniqueness`

## Transitional compromise

Until file splits are made, maintain two roots:

### `RelationalActualism`
full project root for archival / bridge work

### `RelationalActualismNative`
temporary native root for active development and public theorem claims
