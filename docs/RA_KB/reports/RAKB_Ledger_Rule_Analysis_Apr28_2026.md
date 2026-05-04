# RAKB Ledger Rule Analysis — Charge Sign-Source and Topological Route

Date: 2026-04-28  
Scope: RA charge assignment during actualization / graph growth  
Registry action: refine `RA-MOTIF-006`; add `RA-OPEN-CHARGE-SIGN-001`

## 1. Governance decision

The RAKB already contains:

```text
RA-MOTIF-006 — Signed three-direction charge spectrum
```

Therefore the correct registry action is **not** to add a duplicate active claim `RA-MATTER-CHARGE-001`. Instead:

1. Refine `RA-MOTIF-006` to state the clean seven-value signed-N1/electric translation rule.
2. Add `RA-MATTER-CHARGE-001` only as an alias/cross-reference.
3. Add a new issue:

```text
RA-OPEN-CHARGE-SIGN-001 — Edge-level sign-source for signed N1 charge
```

The distinction is:

```text
RA-MOTIF-006:
  source-backed seven-value charge signature

RA-OPEN-CHARGE-SIGN-001:
  unresolved derivation of s(edge, local_context) -> {-1,0,+1}
```

## 2. Settled source-backed content

The current source layer supports three claims.

### 2.1 Vertexwise LLC

The Local Ledger Condition is vertexwise. It is not merely a horizon-level conservation statement. Cut/horizon conservation is downstream of local vertex conservation.

Operational implication:

```text
Every actualization event must be represented as a local ledger-balanced interaction.
```

For sequential simulation, this does **not** mean all newly born vertices must have zero charge at birth. A vertex should be represented as an interaction with incoming ledger and outgoing ledger ports/obligations. Future actualizations consume/close those ports.

### 2.2 Seven-value electric translation

In the d=4 / 3+1D sector, the electric translation uses a signed N1 ledger value:

```text
Q_N1 ∈ {-3,-2,-1,0,+1,+2,+3}
Q_e  = (e/3) Q_N1
```

This is the RA-native discrete seven-value signature. Mapping those values to SM particle labels is translation/cartography, not mechanism.

### 2.3 N1/N2 normalization

The current source layer uses two related but distinct notions:

```text
N1 signed ledger:
  electric-charge translation channel

N2 spatial winding / branching:
  strong, baryonic, color-like ledger channel
```

The papers sometimes describe charge quantization as N2 winding but write the electric translation as signed N1 charge. The normalized RAKB reading should preserve both:

```text
N2 = spatial winding/branching channel
N1 = electric translation / immediate-predecessor signed ledger projection
```

## 3. The unresolved piece

The missing formal object is:

```text
s : edge × local_graph_context -> {-1,0,+1}
```

or, more generally:

```text
ledger_increment : edge × local_graph_context -> LedgerVector
```

Current Lean files support depth-2 ledger preservation, orientation asymmetry, and one-way causal orientation, but they do not yet construct a canonical edge-level sign-source from graph topology alone.

## 4. Could the ledger rule be topological?

Yes — and the most RA-native route is that it should be **topological in the finite graph sense**, not topological in the continuum-manifold sense.

The promising formulation is:

```text
charge = signed incidence / cohomological flux on a finite oriented DAG complex
```

### 4.1 Chain-complex / incidence formulation

Construct a finite combinatorial complex from the local causal graph:

```text
C0 = vertices
C1 = oriented links / immediate-predecessor edges
C2 = branching/depth-2 cells
C3 = local spatial cut volumes
```

Then define incidence/boundary maps:

```text
∂1 : C1 -> C0
∂2 : C2 -> C1
∂3 : C3 -> C2
```

A signed edge contribution is then not an extra random variable. It is an **incidence coefficient**:

```text
s(e) = incidence(local oriented cell, e) ∈ {-1,0,+1}
```

The electric signed-N1 ledger is:

```text
Q_N1(v) = Σ_{e incoming to v} s(e)
```

The LLC becomes a discrete divergence-free condition:

```text
δJ(v) = 0
```

and graph-cut conservation follows by discrete Stokes:

```text
sum over boundary = sum of local divergences = 0
```

This is conceptually ideal because it makes conservation a boundary-of-boundary principle rather than a separately imposed bookkeeping rule.

### 4.2 Oriented-matroid formulation

The immediate-predecessor antichain of a vertex behaves like a finite spatial frame. In d=4, a local spatial cut has rank at most 3. An oriented matroid gives signs to ordered bases of such a finite configuration by a chirotope:

```text
χ(parent_i, parent_j, parent_k) ∈ {-1,0,+1}
```

Then an edge sign can be induced by whether its parent branch agrees or disagrees with the propagated local orientation of the cut.

This has the right properties:

```text
- finite / graph-native
- no continuum manifold required
- signs are determined up to global orientation flip
- global flip corresponds to charge conjugation
- individual sign convention is gauge-like; conservation and spectra are physical
```

### 4.3 N2-to-N1 boundary projection

A strong candidate for resolving the N1/N2 ambiguity is:

```text
N2 winding is the spatial branching/surface ledger.
N1 signed charge is the boundary projection of that winding onto immediate links.
```

In chain-complex language:

```text
N2 channel: 2-chain / 2-cochain on branching cells
N1 channel: boundary / coboundary readout on links
```

Then electric charge is not independent of spatial winding. It is the link-level boundary readout of deeper branching topology.

This would explain why Paper II can speak of N2 winding while writing the electric translation as signed N1 charge: the N1 signature is the immediate-edge projection of an N2 winding structure.

## 5. Why signs should not be sampled as physical variables

A simulator may temporarily enumerate sign assignments subject to LLC, but it should not treat them as independent physical random variables unless RA explicitly adopts that as an axiom.

The RA-native preference ordering should be:

```text
Best:       signs are induced by finite graph topology / incidence / propagated local orientation
Acceptable: signs are finite gauge choices constrained by topology and LLC
Temporary: enumerate signs as candidate ledger states, clearly marked as simulator scaffolding
Avoid:      uniform random signs treated as physical mechanism
```

## 6. Worked example: asymmetric branch

Graph:

```text
0 -> 1 -> 3
2 -> 3
```

Assuming `0` and `2` are incomparable, vertex `3` has:

```text
N1 = 2   immediate predecessors: 1, 2
N2 = 1   depth-2 ancestor: 0
N3 = 0
N4 = 0
```

BDG score:

```text
S = 1 - N1 + 9N2 - 16N3 + 8N4
  = 1 - 2 + 9
  = 8
```

This fixes the motif class and BDG admissibility. It does **not** by itself fix electric charge. The charge is:

```text
Q_N1(3) = s(1 -> 3) + s(2 -> 3)
```

The open rule is the sign-source `s`. If both incoming edges are nonzero ±1 edges, possible values are:

```text
{-2, 0, +2}
```

If zero-valued ledger edges are allowed, possible values are:

```text
{-2,-1,0,+1,+2}
```

A topological incidence rule should select the signs from the local oriented branching context, not from an external random label.

## 7. Boundary conditions

### Vacuum nucleation

For true vacuum/empty-graph nucleation:

```text
initial ledger = 0
Q_N1 = 0
```

There is no inherited boundary orientation/charge state.

### Severance daughter

For a daughter graph produced by severance:

```text
initial ledger = inherited from the parent cut
```

The first effective boundary state is therefore not necessarily neutral. It carries whatever finite ledger data is preserved across the severance boundary.

## 8. Simulator recommendation

Implement ledger rules as a pluggable component.

```python
@dataclass(frozen=True)
class LedgerVector:
    qN1: int = 0                 # electric translation channel
    qN2: tuple[int,int,int] = (0,0,0)  # spatial winding / color-like channel
    qN3: int = 0
    qN4: int = 0
```

```python
@dataclass(frozen=True)
class CandidateExtension:
    parent_set: tuple[int, ...]
    edge_ledger: dict[tuple[int,int], LedgerVector]
    outgoing_ports: tuple[LedgerVector, ...]
```

Then isolate the unresolved physics in one function:

```python
def enumerate_ledger_assignments(G, parent_set, mode="enumerate_llc"):
    """
    mode="neutral": baseline, all local electric ledgers zero.
    mode="enumerate_llc": enumerate signed assignments satisfying LLC and seven-value range.
    mode="orientation_rule_v0": experimental graph-orientation/incidence rule.
    """
```

The simulator should record the mode used in every output file.

## 9. Lean formalization route

A useful intermediate Lean target is conditional, not ontologically final:

```text
Given a finite local signed ledger frame with:
  - at most three independent signed N1 directions
  - each sign in {-1,0,+1}
prove:
  Q_N1 ∈ {-3,-2,-1,0,+1,+2,+3}
```

This would make the seven-value spectrum theorem precise while leaving the construction of the sign frame as the open issue.

A later stronger theorem should construct the signed frame from graph topology:

```text
oriented_local_cut -> edge incidence signs -> signed N1 ledger -> LLC-conserved current
```

Proposed file:

```text
src/RA_AQFT/RA_D1_ChargeLedger_v1.lean
```

Suggested theorem stack:

```text
signed_sum_range_rank_le_three
qN1_seven_value_spectrum
orientation_flip_charge_conjugation
vertex_llc_signed_current
cut_conservation_from_vertex_llc_signed_current
n2_winding_boundary_projects_to_n1_signature   # later / harder
```

## 10. Bottom-line hypothesis

The ledger rule should probably be topological, but not as continuum homotopy. It should be topological as **finite incidence/cohomology of the actualized DAG**:

```text
local oriented graph complex
  -> incidence signs on N1 links
  -> N1 electric readout
  -> N2 winding as branching/surface ledger
  -> LLC as divergence-free current
  -> cut conservation by discrete Stokes
```

This is the cleanest way to make charge assignment an emergent property of RA primitives rather than an extra sampled label.
