import RA_ActualizationSelector

/-!
# RA Frontier / Incidence Normal Form v1

Second exploratory Lean scaffold for the Selector Closure programme.

This file advances the theorem ladder from the abstract selector layer to a
first abstract frontier/incidence layer.  It still does **not** prove the hard
Selector Closure Theorem.  Instead it names the structures needed for T6/T7:

* causal order over a finite RA universe-state;
* candidate past/downset;
* Hasse-style frontier as maximal boundary of a candidate past;
* finite incidence signs in {-1, 0, +1};
* seven-value signed `N1` charge signature;
* boundary ledger as a frontier-level object;
* frontier normal form for candidate descriptions;
* no-hidden-multiplicity as invariance under frontier-normal-form equality;
* a weak bridge from frontier-constraint closure to the existing selector
  closure scaffold.

Suggested RAKB status:

```text
exploratory_formalization_scaffold_not_active_root
proof_status: scaffold / weak lemmas only
```

The intended next step is to replace the abstract `CausalOrder`,
`CandidatePast`, and `Frontier` placeholders with the concrete RA graph/Hasse
frontier structures, then connect the boundary ledger to the existing LLC graph
cut theorem.
-/

namespace RA

/-- Abstract causal order over an RA universe-state.

Later versions should bind this to the concrete graph order already used in the
RA graph-core files. -/
structure CausalOrder (U : UniverseState) where
  le : U.Vertex → U.Vertex → Prop
  refl : ∀ v : U.Vertex, le v v
  trans : ∀ {a b c : U.Vertex}, le a b → le b c → le a c
  antisymm : ∀ {a b : U.Vertex}, le a b → le b a → a = b

/-- A candidate past is a downset in the causal order.

If `y` is in the candidate past and `x ≤ y`, then `x` is also in the candidate
past.  This is the first formal move from arbitrary parent listings toward a
closure/frontier normal form. -/
structure CandidatePast (U : UniverseState) (O : CausalOrder U) where
  contains : U.Vertex → Prop
  down_closed : ∀ {x y : U.Vertex}, O.le x y → contains y → contains x

/-- A frontier for a candidate past.

The frontier is abstractly represented as the set of maximal elements of the
candidate past, plus a covering condition saying every past element lies below
some frontier element.  This is a Hasse-frontier placeholder; later versions
should define it constructively from the concrete finite graph. -/
structure Frontier (U : UniverseState) (O : CausalOrder U)
    (P : CandidatePast U O) where
  isFrontier : U.Vertex → Prop
  frontier_in_past : ∀ {v : U.Vertex}, isFrontier v → P.contains v
  maximal : ∀ {v w : U.Vertex}, isFrontier v → P.contains w → O.le v w → w = v
  every_past_below_frontier :
    ∀ {x : U.Vertex}, P.contains x → ∃ f : U.Vertex, isFrontier f ∧ O.le x f

/-- Three-valued signed incidence coefficient for a frontier link. -/
inductive IncidenceSign where
  | neg
  | zero
  | pos
  deriving DecidableEq, Repr

/-- Integer interpretation of an incidence sign. -/
def IncidenceSign.toInt : IncidenceSign → Int
  | IncidenceSign.neg => (-1 : Int)
  | IncidenceSign.zero => (0 : Int)
  | IncidenceSign.pos => (1 : Int)

/-- Seven-value signed N1 charge signature.

This is the formal range statement used by the electric translation layer:
`Q_N1 ∈ {-3,-2,-1,0,+1,+2,+3}`.  The edge-level sign-source is still open; this
predicate only records the range. -/
def SevenCharge (q : Int) : Prop :=
  q = (-3 : Int) ∨ q = (-2 : Int) ∨ q = (-1 : Int) ∨ q = (0 : Int) ∨
  q = (1 : Int) ∨ q = (2 : Int) ∨ q = (3 : Int)

/-- Boundary ledger data carried by a frontier.

The field `qN1` records the net signed N1 boundary readout.  The field
`local_conserved` is deliberately abstract: in the full theory it should become
LLC / divergence-free conservation on the local incidence boundary. -/
structure BoundaryLedger {U : UniverseState} {O : CausalOrder U}
    (P : CandidatePast U O) (F : Frontier U O P) where
  qN1 : Int
  qN1_seven : SevenCharge qN1
  local_conserved : Prop

/-- The N1 boundary charge of any boundary ledger lies in the seven-value
signature by construction. -/
theorem boundaryLedger_qN1_seven
    {U : UniverseState} {O : CausalOrder U}
    {P : CandidatePast U O} {F : Frontier U O P}
    (L : BoundaryLedger P F) :
    SevenCharge L.qN1 :=
  L.qN1_seven

/-- Candidate boundary data: a downset, its frontier, and a boundary ledger. -/
structure CandidateBoundaryData (U : UniverseState) (O : CausalOrder U) where
  past : CandidatePast U O
  frontier : Frontier U O past
  ledger : BoundaryLedger past frontier

/-- Frontier normal form for candidate descriptions.

This is the concrete analogue of `CandidateNormalForm`, but the normal data is
specifically a candidate past, Hasse-style frontier, and boundary ledger.  The
package does not assert that different histories are ontologically identical; it
asserts only that a proposed physical-equivalence relation is represented by
frontier-boundary data equality. -/
structure FrontierNormalForm {U : UniverseState}
    (Pot : Potentia U) (O : CausalOrder U) where
  dataOf : Pot.Candidate → CandidateBoundaryData U O
  physically_equiv : Pot.Candidate → Pot.Candidate → Prop
  equiv_iff_same_data : ∀ c d : Pot.Candidate,
    physically_equiv c d ↔ dataOf c = dataOf d

/-- Same frontier-boundary data implies physical equivalence under the chosen
frontier normal-form package. -/
theorem frontier_physically_equiv_of_same_data
    {U : UniverseState} {Pot : Potentia U} {O : CausalOrder U}
    (FNF : FrontierNormalForm Pot O)
    {c d : Pot.Candidate}
    (h : FNF.dataOf c = FNF.dataOf d) :
    FNF.physically_equiv c d :=
  (FNF.equiv_iff_same_data c d).2 h

/-- Physical equivalence under a frontier normal-form package implies equality
of frontier-boundary data. -/
theorem same_data_of_frontier_physically_equiv
    {U : UniverseState} {Pot : Potentia U} {O : CausalOrder U}
    (FNF : FrontierNormalForm Pot O)
    {c d : Pot.Candidate}
    (h : FNF.physically_equiv c d) :
    FNF.dataOf c = FNF.dataOf d :=
  (FNF.equiv_iff_same_data c d).1 h

/-- A candidate weight function, used only to state no-hidden-multiplicity
invariance abstractly.  This is not a probability measure. -/
structure CandidateWeight {U : UniverseState} (Pot : Potentia U) where
  weight : Pot.Candidate → Nat

/-- No-hidden-multiplicity discipline for a frontier normal form.

If two candidate descriptions are physically equivalent because they have the
same frontier-boundary normal form, then any physical weight/selector-shadow
assigned to them must agree.  This prevents representational redundancy from
becoming hidden physical multiplicity. -/
structure NormalFormInvariantWeight
    {U : UniverseState} {Pot : Potentia U} {O : CausalOrder U}
    (FNF : FrontierNormalForm Pot O) where
  W : CandidateWeight Pot
  invariant : ∀ {c d : Pot.Candidate}, FNF.physically_equiv c d → W.weight c = W.weight d

/-- Equal frontier-boundary data gives equal physical weight under a
normal-form-invariant weight package. -/
theorem same_weight_of_same_frontier_data
    {U : UniverseState} {Pot : Potentia U} {O : CausalOrder U}
    {FNF : FrontierNormalForm Pot O}
    (I : NormalFormInvariantWeight FNF)
    {c d : Pot.Candidate}
    (h : FNF.dataOf c = FNF.dataOf d) :
    I.W.weight c = I.W.weight d :=
  I.invariant (frontier_physically_equiv_of_same_data FNF h)

/-- Frontier-constraint closure data.

This is the T6/T7 refinement of `SelectorClosureData`: the hard graph-native
constraints are assumed to determine a unique valid candidate, and the candidate
space is equipped with frontier-boundary normal-form data.  The future hard
work is to derive this package from concrete DAG + BDG + LLC + incidence data. -/
structure FrontierConstraintClosureData
    {U : UniverseState} (Pot : Potentia U) (O : CausalOrder U) where
  normal_form : FrontierNormalForm Pot O
  constraints : CandidateConstraints Pot
  below_saturation : ¬ Pot.saturated
  unique_valid : ∃! c : Pot.Candidate, constraints.valid c

/-- Forget frontier-normal-form information and recover the abstract closure-data
package from `RA_ActualizationSelector_v1`. -/
def selectorClosureDataOfFrontierData
    {U : UniverseState} {Pot : Potentia U} {O : CausalOrder U}
    (H : FrontierConstraintClosureData Pot O) : SelectorClosureData Pot :=
  { constraints := H.constraints
    below_saturation := H.below_saturation
    unique_valid := H.unique_valid }

noncomputable section

/-- Frontier closure data induces an actualization selector via the existing
abstract selector scaffold. -/
def selectorFromFrontierClosureData
    {U : UniverseState} {Pot : Potentia U} {O : CausalOrder U}
    (H : FrontierConstraintClosureData Pot O) : ActualizationSelector U Pot :=
  selectorFromClosureData (selectorClosureDataOfFrontierData H)

/-- Weak Frontier Selector Closure theorem.

If frontier/incidence constraints determine a unique valid candidate below
saturation, then the induced selector selects a unique admissible candidate.
This is still conditional; it does not yet prove that RA's concrete constraints
always determine such a unique valid candidate. -/
theorem weak_frontier_selector_closure
    {U : UniverseState} {Pot : Potentia U} {O : CausalOrder U}
    (H : FrontierConstraintClosureData Pot O) :
    ∃! c : Admissible Pot, c = (selectorFromFrontierClosureData H).choose := by
  exact selected_candidate_unique (selectorFromFrontierClosureData H)

end

/-!
## Next hard targets

1. Replace `CausalOrder` with the concrete finite DAG order.
2. Construct `CandidatePast` as the causal closure/downset of a candidate.
3. Construct `Frontier` as the Hasse frontier of that downset.
4. Replace `BoundaryLedger.local_conserved` with concrete LLC/divergence-free
   incidence conservation.
5. Prove the edge-level sign-source theorem for signed N1 charge, or prove a
   conditional theorem that signed N1 follows from a supplied oriented frontier.
6. Derive `FrontierConstraintClosureData` from RA graph + BDG + LLC constraints,
   rather than assuming it.
-/

end RA
