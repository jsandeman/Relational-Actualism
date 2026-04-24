import RA_GraphCore

/-!
# RA_GraphCore_Native

Native wrapper for the active graph bedrock.

This file does **not** change the mathematical content of `RA_GraphCore`.
It changes the active vocabulary of the theorem frontier so that the root of
the project speaks in RA's own terms:

- local ledger condition
- causal cut / ledger flux
- causal shielding

Retired from the active native root:
- `horizon_partition` (alias only; not canonical)
- `MarkovBlanket` as the public-facing name
-/

open BigOperators

abbrev LedgerGraph := ActualizationGraph
abbrev LedgerCut := CausalCut

/-- RA-native active name for the Local Ledger Condition at a vertex. -/
def llc_at (G : LedgerGraph) (v : Vertex) : Prop :=
  satisfies_local_ledger G v

/-- Edges wholly internal to the left side of a ledger cut. -/
def cut_internal_edges (G : LedgerGraph) (C : LedgerCut G) : Finset Edge :=
  internal_edges G C.V_L

/-- The net ledger-bearing edge set across the cut. -/
def cut_flux (G : LedgerGraph) (C : LedgerCut G) : Finset Edge :=
  boundary_flux G C

/-- The active native form of the graph-cut theorem. -/
theorem ledger_flux_zero_across_cut
    (G : LedgerGraph) (C : LedgerCut G)
    (h_llc : ∀ v ∈ C.V_L, llc_at G v) :
    ∑ e ∈ cut_flux G C, e.charge = 0 := by
  exact RA_graph_cut_theorem G C h_llc

/-- Native replacement for the old public-facing `MarkovBlanket` vocabulary. -/
structure CausalShield (G : LedgerGraph) where
  Interior      : Finset Vertex
  Exterior      : Finset Vertex
  SensoryShell  : Finset Vertex
  ActiveShell   : Finset Vertex
  is_complete   : Interior ∪ Exterior ∪ SensoryShell ∪ ActiveShell = G.V
  shield_interior :
      ∀ e ∈ G.E, e.dst ∈ Interior → e.src ∈ SensoryShell ∪ Interior
  shield_exterior :
      ∀ e ∈ G.E, e.dst ∈ Exterior → e.src ∈ ActiveShell ∪ Exterior

namespace CausalShield

def boundary (G : LedgerGraph) (S : CausalShield G) : Finset Vertex :=
  S.SensoryShell ∪ S.ActiveShell

end CausalShield

/-- A native bridge from the archival structure name to the new active one. -/
def causalShield_of_markovBlanket (G : LedgerGraph) (M : MarkovBlanket G) :
    CausalShield G where
  Interior := M.Internal
  Exterior := M.External
  SensoryShell := M.Sensory
  ActiveShell := M.Active
  is_complete := by simpa [Finset.union_assoc, Finset.union_left_comm] using M.is_complete
  shield_interior := M.shield_internal
  shield_exterior := M.shield_external

/-- The canonical boundary extracted from the archival structure. -/
theorem causalShield_boundary_agrees
    (G : LedgerGraph) (M : MarkovBlanket G) :
    (causalShield_of_markovBlanket G M).boundary G = M.boundary G := by
  rfl

/-!
Native root note:

The active theorem frontier should cite:
- `llc_at`
- `ledger_flux_zero_across_cut`
- `CausalShield`
- `CausalShield.boundary`

and should not cite `horizon_partition` or use `MarkovBlanket` as the
canonical public-facing vocabulary.
-/
