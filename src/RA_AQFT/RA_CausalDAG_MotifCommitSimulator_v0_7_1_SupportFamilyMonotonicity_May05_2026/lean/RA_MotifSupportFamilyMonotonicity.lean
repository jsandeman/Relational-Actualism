import RA_MotifSupportFamilyBridge

/-!
# RA_MotifSupportFamilyMonotonicity

Monotonicity bridge for RA support-cut families.

`RA_MotifSupportFamilyBridge` introduced family readiness: a motif support
family is ready at a site when some member support cut is ready.  The v0.7
support-family simulator showed that exact-threshold subfamilies can behave
unlike true additive redundancy: replacing one family by another may remove the
original strict support cut and can therefore make some channels worse.

This module isolates the formal condition under which redundancy is monotone:
family inclusion.  If a family `F'` contains every cut of `F`, then any-cut
readiness, certified family readiness, and family commitment propagate from `F`
to `F'`.  The theorem is intentionally abstract; concrete support-family
construction is left to downstream BDG-LLC / frontier / orientation / ledger
certification layers.
-/

namespace RA

/-! ## DAG family inclusion and augmentation -/

section O01FamilyMonotonicity

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- Family inclusion for DAG support-cut families.  `DAGFamilyIncluded F F'`
means every support cut accepted by `F` is also accepted by `F'`. -/
def DAGFamilyIncluded
    (F F' : DAGSupportCutFamily V) : Prop :=
  ∀ Q, F.cuts Q → F'.cuts Q

/-- A family augmentation is just inclusion into a larger family. -/
def DAGFamilyAugments
    (Faug F : DAGSupportCutFamily V) : Prop :=
  DAGFamilyIncluded F Faug

/-- Union of two DAG support-cut families. -/
def DAGFamilyUnion
    (F₁ F₂ : DAGSupportCutFamily V) : DAGSupportCutFamily V :=
  { cuts := fun Q => F₁.cuts Q ∨ F₂.cuts Q
    nonempty_cuts := by
      rcases F₁.nonempty_cuts with ⟨Q, hQ⟩
      exact ⟨Q, Or.inl hQ⟩ }

/-- Family inclusion is reflexive. -/
theorem DAGFamilyIncluded.refl
    (F : DAGSupportCutFamily V) : DAGFamilyIncluded F F := by
  intro Q hQ
  exact hQ

/-- Family inclusion is transitive. -/
theorem DAGFamilyIncluded.trans
    {F₁ F₂ F₃ : DAGSupportCutFamily V}
    (h12 : DAGFamilyIncluded F₁ F₂)
    (h23 : DAGFamilyIncluded F₂ F₃) :
    DAGFamilyIncluded F₁ F₃ := by
  intro Q hQ
  exact h23 Q (h12 Q hQ)

/-- The left family is included in its union. -/
theorem DAGFamilyIncluded.left_union
    (F₁ F₂ : DAGSupportCutFamily V) :
    DAGFamilyIncluded F₁ (DAGFamilyUnion F₁ F₂) := by
  intro Q hQ
  exact Or.inl hQ

/-- The right family is included in its union. -/
theorem DAGFamilyIncluded.right_union
    (F₁ F₂ : DAGSupportCutFamily V) :
    DAGFamilyIncluded F₂ (DAGFamilyUnion F₁ F₂) := by
  intro Q hQ
  exact Or.inr hQ

/-- Any-cut readiness is monotone under family inclusion. -/
theorem DAGFamilyReadyAt.mono_family
    {G : _root_.ActualizationDAG V}
    {F F' : DAGSupportCutFamily V} {x : V}
    (hinc : DAGFamilyIncluded F F')
    (hready : DAGFamilyReadyAt G F x) :
    DAGFamilyReadyAt G F' x := by
  rcases hready with ⟨Q, hcut, hQ⟩
  exact ⟨Q, hinc Q hcut, hQ⟩

/-- Certified family readiness is monotone under family inclusion. -/
theorem DAGCertifiedFamilyReadyAt.mono_family
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F F' : DAGSupportCutFamily V} {x : V}
    (hinc : DAGFamilyIncluded F F')
    (hready : DAGCertifiedFamilyReadyAt G Γ M F x) :
    DAGCertifiedFamilyReadyAt G Γ M F' x := by
  rcases hready with ⟨Q, hcut, hsupports, hQ⟩
  exact ⟨Q, hinc Q hcut, hsupports, hQ⟩

/-- Family commitment is monotone under family inclusion. -/
theorem DAGFamilyCommitsAt.mono_family
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F F' : DAGSupportCutFamily V} {x : V}
    (hinc : DAGFamilyIncluded F F')
    (hcommit : DAGFamilyCommitsAt G Γ M F x) :
    DAGFamilyCommitsAt G Γ M F' x := by
  rcases hcommit with ⟨Q, hcut, hQ⟩
  exact ⟨Q, hinc Q hcut, hQ⟩

/-- All-cut readiness is contravariantly monotone: if every cut in a larger
family is ready, then every cut in a subfamily is ready. -/
theorem DAGFamilyAllReadyAt.mono_subfamily
    {G : _root_.ActualizationDAG V}
    {Fsub F : DAGSupportCutFamily V} {x : V}
    (hinc : DAGFamilyIncluded Fsub F)
    (hall : DAGFamilyAllReadyAt G F x) :
    DAGFamilyAllReadyAt G Fsub x := by
  intro Q hQ
  exact hall Q (hinc Q hQ)

/-- Readiness of a family survives left-union augmentation. -/
theorem DAGFamilyReadyAt.left_union
    {G : _root_.ActualizationDAG V}
    {F₁ F₂ : DAGSupportCutFamily V} {x : V}
    (hready : DAGFamilyReadyAt G F₁ x) :
    DAGFamilyReadyAt G (DAGFamilyUnion F₁ F₂) x :=
  DAGFamilyReadyAt.mono_family (DAGFamilyIncluded.left_union F₁ F₂) hready

/-- Certified readiness of a family survives left-union augmentation. -/
theorem DAGCertifiedFamilyReadyAt.left_union
    {G : _root_.ActualizationDAG V} {Γ : DAGCommitContext G}
    {M : MotifCandidate V} {F₁ F₂ : DAGSupportCutFamily V} {x : V}
    (hready : DAGCertifiedFamilyReadyAt G Γ M F₁ x) :
    DAGCertifiedFamilyReadyAt G Γ M (DAGFamilyUnion F₁ F₂) x :=
  DAGCertifiedFamilyReadyAt.mono_family (DAGFamilyIncluded.left_union F₁ F₂) hready

end O01FamilyMonotonicity

/-! ## Graph family inclusion and augmentation -/

section GraphFamilyMonotonicity

/-- Family inclusion for concrete graph support-cut families. -/
def GraphFamilyIncluded
    {G : _root_.ActualizationGraph}
    (F F' : GraphSupportCutFamily G) : Prop :=
  ∀ Q, F.cuts Q → F'.cuts Q

/-- A graph-family augmentation is inclusion into a larger graph family. -/
def GraphFamilyAugments
    {G : _root_.ActualizationGraph}
    (Faug F : GraphSupportCutFamily G) : Prop :=
  GraphFamilyIncluded F Faug

/-- Union of two graph support-cut families. -/
def GraphFamilyUnion
    {G : _root_.ActualizationGraph}
    (F₁ F₂ : GraphSupportCutFamily G) : GraphSupportCutFamily G :=
  { cuts := fun Q => F₁.cuts Q ∨ F₂.cuts Q
    nonempty_cuts := by
      rcases F₁.nonempty_cuts with ⟨Q, hQ⟩
      exact ⟨Q, Or.inl hQ⟩ }

/-- Graph-family inclusion is reflexive. -/
theorem GraphFamilyIncluded.refl
    {G : _root_.ActualizationGraph}
    (F : GraphSupportCutFamily G) : GraphFamilyIncluded F F := by
  intro Q hQ
  exact hQ

/-- Graph-family inclusion is transitive. -/
theorem GraphFamilyIncluded.trans
    {G : _root_.ActualizationGraph}
    {F₁ F₂ F₃ : GraphSupportCutFamily G}
    (h12 : GraphFamilyIncluded F₁ F₂)
    (h23 : GraphFamilyIncluded F₂ F₃) :
    GraphFamilyIncluded F₁ F₃ := by
  intro Q hQ
  exact h23 Q (h12 Q hQ)

/-- The left graph family is included in its union. -/
theorem GraphFamilyIncluded.left_union
    {G : _root_.ActualizationGraph}
    (F₁ F₂ : GraphSupportCutFamily G) :
    GraphFamilyIncluded F₁ (GraphFamilyUnion F₁ F₂) := by
  intro Q hQ
  exact Or.inl hQ

/-- The right graph family is included in its union. -/
theorem GraphFamilyIncluded.right_union
    {G : _root_.ActualizationGraph}
    (F₁ F₂ : GraphSupportCutFamily G) :
    GraphFamilyIncluded F₂ (GraphFamilyUnion F₁ F₂) := by
  intro Q hQ
  exact Or.inr hQ

/-- Concrete graph any-cut readiness is monotone under family inclusion. -/
theorem GraphFamilyReadyAt.mono_family
    {G : _root_.ActualizationGraph}
    {F F' : GraphSupportCutFamily G} {x : GraphVertex G}
    (hinc : GraphFamilyIncluded F F')
    (hready : GraphFamilyReadyAt G F x) :
    GraphFamilyReadyAt G F' x := by
  rcases hready with ⟨Q, hcut, hQ⟩
  exact ⟨Q, hinc Q hcut, hQ⟩

/-- Concrete graph certified family readiness is monotone under family inclusion. -/
theorem GraphCertifiedFamilyReadyAt.mono_family
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F F' : GraphSupportCutFamily G}
    {x : GraphVertex G}
    (hinc : GraphFamilyIncluded F F')
    (hready : GraphCertifiedFamilyReadyAt G Γ M F x) :
    GraphCertifiedFamilyReadyAt G Γ M F' x := by
  rcases hready with ⟨Q, hcut, hsupports, hQ⟩
  exact ⟨Q, hinc Q hcut, hsupports, hQ⟩

/-- Concrete graph family commitment is monotone under family inclusion. -/
theorem GraphFamilyCommitsAt.mono_family
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F F' : GraphSupportCutFamily G}
    {x : GraphVertex G}
    (hinc : GraphFamilyIncluded F F')
    (hcommit : GraphFamilyCommitsAt G Γ M F x) :
    GraphFamilyCommitsAt G Γ M F' x := by
  rcases hcommit with ⟨Q, hcut, hQ⟩
  exact ⟨Q, hinc Q hcut, hQ⟩

/-- Concrete graph all-cut readiness is contravariantly monotone. -/
theorem GraphFamilyAllReadyAt.mono_subfamily
    {G : _root_.ActualizationGraph}
    {Fsub F : GraphSupportCutFamily G} {x : GraphVertex G}
    (hinc : GraphFamilyIncluded Fsub F)
    (hall : GraphFamilyAllReadyAt G F x) :
    GraphFamilyAllReadyAt G Fsub x := by
  intro Q hQ
  exact hall Q (hinc Q hQ)

/-- Concrete graph readiness survives left-union augmentation. -/
theorem GraphFamilyReadyAt.left_union
    {G : _root_.ActualizationGraph}
    {F₁ F₂ : GraphSupportCutFamily G} {x : GraphVertex G}
    (hready : GraphFamilyReadyAt G F₁ x) :
    GraphFamilyReadyAt G (GraphFamilyUnion F₁ F₂) x :=
  GraphFamilyReadyAt.mono_family (GraphFamilyIncluded.left_union F₁ F₂) hready

/-- Concrete graph certified readiness survives left-union augmentation. -/
theorem GraphCertifiedFamilyReadyAt.left_union
    {G : _root_.ActualizationGraph} {Γ : GraphCommitContext G}
    {M : GraphMotifCandidate G} {F₁ F₂ : GraphSupportCutFamily G}
    {x : GraphVertex G}
    (hready : GraphCertifiedFamilyReadyAt G Γ M F₁ x) :
    GraphCertifiedFamilyReadyAt G Γ M (GraphFamilyUnion F₁ F₂) x :=
  GraphCertifiedFamilyReadyAt.mono_family (GraphFamilyIncluded.left_union F₁ F₂) hready

end GraphFamilyMonotonicity

end RA
