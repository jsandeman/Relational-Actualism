import RA_MotifCommitProtocol

/-!
# RA_MotifSupportFamilyBridge

Support-family bridge for RA motif actualization.

The motif-commit protocol uses a single support cut: all vertices in that cut
must reach the candidate actualization site.  The v0.6 channel-resolved
severance workbench showed that increasing the width of one conjunctive support
cut can increase exposure to edge/reachability loss.  This module introduces the
separate RA-native notion of a support-cut family: a candidate motif may be
certified by one of several sufficient cuts.

Thus:

* single support cut readiness is all-of-one-cut;
* family readiness is existence of a certified ready cut in a family;
* all-cut family readiness is a stronger diagnostic notion;
* singleton families recover the existing support-cut semantics.

This module is abstract.  It does not assert a physical redundancy law, and it
does not import external voting or inherited-theory apparatus.  Concrete support
families must still be justified downstream by BDG-LLC, frontier, orientation,
ledger, or native-closure evidence.
-/

namespace RA

/-! ## DAG support-cut families -/

section O01FamilyLayer

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- A family of candidate support cuts over a finite ActualizationDAG surface.

`cuts Q` means that `Q` is one of the alternative support cuts in the family.
A nonempty family is required so that `all`-style diagnostics are not vacuous. -/
structure DAGSupportCutFamily (V : Type*) [Fintype V] [DecidableEq V] where
  cuts : CausalSupportCut V → Prop
  nonempty_cuts : ∃ Q, cuts Q

/-- Singleton support-cut family.  This is the embedding of the existing
single-cut motif-commit semantics into the family layer. -/
def DAGSingletonSupportCutFamily
    (Q : CausalSupportCut V) : DAGSupportCutFamily V :=
  { cuts := fun Q' => Q' = Q
    nonempty_cuts := ⟨Q, rfl⟩ }

/-- Any-cut family readiness: some cut in the family is ready at the site. -/
def DAGFamilyReadyAt
    (G : _root_.ActualizationDAG V) (F : DAGSupportCutFamily V) (x : V) : Prop :=
  ∃ Q, F.cuts Q ∧ DAGReadyAt G Q x

/-- All-cut family readiness: every cut in the family is ready at the site.
This is a diagnostic strengthening, not the redundancy semantics. -/
def DAGFamilyAllReadyAt
    (G : _root_.ActualizationDAG V) (F : DAGSupportCutFamily V) (x : V) : Prop :=
  ∀ Q, F.cuts Q → DAGReadyAt G Q x

/-- Certified family readiness: some cut in the family is both context-certified
for the motif and causally ready at the site. -/
def DAGCertifiedFamilyReadyAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V) (x : V) : Prop :=
  ∃ Q, F.cuts Q ∧ Γ.supports M Q ∧ DAGReadyAt G Q x

/-- A ready cut in a family witnesses family readiness. -/
theorem DAGFamilyReadyAt.of_cut_ready
    {G : _root_.ActualizationDAG V} {F : DAGSupportCutFamily V} {x : V}
    {Q : CausalSupportCut V}
    (hcut : F.cuts Q) (hready : DAGReadyAt G Q x) :
    DAGFamilyReadyAt G F x :=
  ⟨Q, hcut, hready⟩

/-- All-cut readiness implies any-cut readiness for nonempty families. -/
theorem DAGFamilyAllReadyAt.to_family_ready
    {G : _root_.ActualizationDAG V} {F : DAGSupportCutFamily V} {x : V}
    (hall : DAGFamilyAllReadyAt G F x) :
    DAGFamilyReadyAt G F x := by
  rcases F.nonempty_cuts with ⟨Q, hcut⟩
  exact ⟨Q, hcut, hall Q hcut⟩

/-- Family readiness is monotone toward the causal future. -/
theorem DAGFamilyReadyAt.future_mono
    (G : _root_.ActualizationDAG V) (F : DAGSupportCutFamily V) {x z : V}
    (hready : DAGFamilyReadyAt G F x)
    (hxz : G.precedes x z) :
    DAGFamilyReadyAt G F z := by
  rcases hready with ⟨Q, hcut, hQ⟩
  exact ⟨Q, hcut, DAGReadyAt.future_mono G Q hQ hxz⟩

/-- All-cut family readiness is monotone toward the causal future. -/
theorem DAGFamilyAllReadyAt.future_mono
    (G : _root_.ActualizationDAG V) (F : DAGSupportCutFamily V) {x z : V}
    (hall : DAGFamilyAllReadyAt G F x)
    (hxz : G.precedes x z) :
    DAGFamilyAllReadyAt G F z := by
  intro Q hcut
  exact DAGReadyAt.future_mono G Q (hall Q hcut) hxz

/-- A singleton family is ready exactly when its underlying support cut is ready. -/
theorem DAGFamilyReadyAt_singleton_iff
    (G : _root_.ActualizationDAG V) (Q : CausalSupportCut V) (x : V) :
    DAGFamilyReadyAt G (DAGSingletonSupportCutFamily Q) x ↔ DAGReadyAt G Q x := by
  constructor
  · intro h
    rcases h with ⟨Q', hQ', hready⟩
    simpa [hQ'] using hready
  · intro h
    exact ⟨Q, rfl, h⟩

/-- Family commitment: the motif commits via some certified ready support cut in
its support family.  Strict exclusion is still delegated to `DAGCommitsAt`. -/
def DAGFamilyCommitsAt
    (G : _root_.ActualizationDAG V) (Γ : DAGCommitContext G)
    (M : MotifCandidate V) (F : DAGSupportCutFamily V) (x : V) : Prop :=
  ∃ Q, F.cuts Q ∧ DAGCommitsAt G Γ M Q x

/-- Family commitment implies certified family readiness. -/
theorem DAGFamilyCommitsAt.certified_family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V} {x : V}
    (h : DAGFamilyCommitsAt G Γ M F x) :
    DAGCertifiedFamilyReadyAt G Γ M F x := by
  rcases h with ⟨Q, hcut, hcommit⟩
  exact ⟨Q, hcut, DAGCommitsAt.supports G Γ M Q x hcommit,
    DAGCommitsAt.ready G Γ M Q x hcommit⟩

/-- Family commitment implies any-cut family readiness. -/
theorem DAGFamilyCommitsAt.family_ready
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F : DAGSupportCutFamily V} {x : V}
    (h : DAGFamilyCommitsAt G Γ M F x) :
    DAGFamilyReadyAt G F x := by
  rcases h with ⟨Q, hcut, hcommit⟩
  exact ⟨Q, hcut, DAGCommitsAt.ready G Γ M Q x hcommit⟩

end O01FamilyLayer

/-! ## Concrete graph support-cut families -/

section GraphFamilyLayer

/-- A family of concrete graph support cuts. -/
structure GraphSupportCutFamily (G : _root_.ActualizationGraph) where
  cuts : GraphSupportCut G → Prop
  nonempty_cuts : ∃ Q, cuts Q

/-- Singleton concrete graph support-cut family. -/
def GraphSingletonSupportCutFamily
    {G : _root_.ActualizationGraph} (Q : GraphSupportCut G) :
    GraphSupportCutFamily G :=
  { cuts := fun Q' => Q' = Q
    nonempty_cuts := ⟨Q, rfl⟩ }

/-- Any-cut family readiness on the concrete graph surface. -/
def GraphFamilyReadyAt
    (G : _root_.ActualizationGraph) (F : GraphSupportCutFamily G)
    (x : GraphVertex G) : Prop :=
  ∃ Q, F.cuts Q ∧ GraphReadyAt G Q x

/-- All-cut family readiness on the concrete graph surface. -/
def GraphFamilyAllReadyAt
    (G : _root_.ActualizationGraph) (F : GraphSupportCutFamily G)
    (x : GraphVertex G) : Prop :=
  ∀ Q, F.cuts Q → GraphReadyAt G Q x

/-- Certified family readiness on the concrete graph surface. -/
def GraphCertifiedFamilyReadyAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (x : GraphVertex G) : Prop :=
  ∃ Q, F.cuts Q ∧ Γ.supports M Q ∧ GraphReadyAt G Q x

/-- A ready graph cut in a family witnesses graph family readiness. -/
theorem GraphFamilyReadyAt.of_cut_ready
    {G : _root_.ActualizationGraph} {F : GraphSupportCutFamily G}
    {x : GraphVertex G} {Q : GraphSupportCut G}
    (hcut : F.cuts Q) (hready : GraphReadyAt G Q x) :
    GraphFamilyReadyAt G F x :=
  ⟨Q, hcut, hready⟩

/-- All-cut graph readiness implies any-cut graph readiness for nonempty
families. -/
theorem GraphFamilyAllReadyAt.to_family_ready
    {G : _root_.ActualizationGraph} {F : GraphSupportCutFamily G}
    {x : GraphVertex G}
    (hall : GraphFamilyAllReadyAt G F x) :
    GraphFamilyReadyAt G F x := by
  rcases F.nonempty_cuts with ⟨Q, hcut⟩
  exact ⟨Q, hcut, hall Q hcut⟩

/-- Graph family readiness is monotone along concrete reachability. -/
theorem GraphFamilyReadyAt.future_mono
    (G : _root_.ActualizationGraph) (F : GraphSupportCutFamily G)
    {x z : GraphVertex G}
    (hready : GraphFamilyReadyAt G F x)
    (hxz : Reachable G x z) :
    GraphFamilyReadyAt G F z := by
  rcases hready with ⟨Q, hcut, hQ⟩
  exact ⟨Q, hcut, GraphReadyAt.future_mono G Q hQ hxz⟩

/-- All-cut graph family readiness is monotone along concrete reachability. -/
theorem GraphFamilyAllReadyAt.future_mono
    (G : _root_.ActualizationGraph) (F : GraphSupportCutFamily G)
    {x z : GraphVertex G}
    (hall : GraphFamilyAllReadyAt G F x)
    (hxz : Reachable G x z) :
    GraphFamilyAllReadyAt G F z := by
  intro Q hcut
  exact GraphReadyAt.future_mono G Q (hall Q hcut) hxz

/-- A singleton graph family is ready exactly when its underlying support cut is
ready. -/
theorem GraphFamilyReadyAt_singleton_iff
    (G : _root_.ActualizationGraph) (Q : GraphSupportCut G)
    (x : GraphVertex G) :
    GraphFamilyReadyAt G (GraphSingletonSupportCutFamily Q) x ↔ GraphReadyAt G Q x := by
  constructor
  · intro h
    rcases h with ⟨Q', hQ', hready⟩
    simpa [hQ'] using hready
  · intro h
    exact ⟨Q, rfl, h⟩

/-- Family commitment on the concrete graph surface. -/
def GraphFamilyCommitsAt
    (G : _root_.ActualizationGraph) (Γ : GraphCommitContext G)
    (M : GraphMotifCandidate G) (F : GraphSupportCutFamily G)
    (x : GraphVertex G) : Prop :=
  ∃ Q, F.cuts Q ∧ GraphCommitsAt G Γ M Q x

/-- Graph family commitment implies certified graph family readiness. -/
theorem GraphFamilyCommitsAt.certified_family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {x : GraphVertex G}
    (h : GraphFamilyCommitsAt G Γ M F x) :
    GraphCertifiedFamilyReadyAt G Γ M F x := by
  rcases h with ⟨Q, hcut, hcommit⟩
  exact ⟨Q, hcut, GraphCommitsAt.supports G Γ M Q x hcommit,
    GraphCommitsAt.ready G Γ M Q x hcommit⟩

/-- Graph family commitment implies graph family readiness. -/
theorem GraphFamilyCommitsAt.family_ready
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F : GraphSupportCutFamily G}
    {x : GraphVertex G}
    (h : GraphFamilyCommitsAt G Γ M F x) :
    GraphFamilyReadyAt G F x := by
  rcases h with ⟨Q, hcut, hcommit⟩
  exact ⟨Q, hcut, GraphCommitsAt.ready G Γ M Q x hcommit⟩

end GraphFamilyLayer

end RA
