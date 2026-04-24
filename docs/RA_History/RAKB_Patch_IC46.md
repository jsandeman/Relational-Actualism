# RAKB Patch — IC46: AQFT Axiom/Admit Inventory Correction
## April 17, 2026 · Produced after direct inspection of RA_AQFT_Proofs_v10.lean

This patch corrects an under-reported scope caveat on Lean-verified (LV)
claims L04 and L05, and flags an inconsistency between the RAKB Apr 16
"O11 DISSOLVED" status and the actual Lean dependency graph.

Apply this as a patch to `rakb.yaml`.

---

## NEW INTEGRITY CHECK

```yaml
IC46:
  date: 2026-04-17
  severity: HIGH
  category: framing_discipline_violation
  note: >
    L04 (frame_independence) and L05 (rindler_stationarity) in
    RA_AQFT_Proofs_v10.lean depend on three items the RAKB and
    website had not been tracking explicitly:

    (a) Matrix.cfc_conj_unitary (line 287, sorry):
        General CFC-unitary-conjugation lemma. Pure mathematical
        gap. Closable in ~1 line by copying the proof from
        Lean-QuantumInfo Isometry.lean (Meiburg et al. 2025,
        arXiv:2510.08672). No physics implications.

    (b) vacuum_lorentz_invariant (line 344, axiom):
        States unitaryConj U vacuumState = vacuumState for any
        unitary U. This is a Wightman-axiom import from QFT.
        *** VIOLATES THE RA FRAMING DISCIPLINE ***
        Under the April 17, 2026 framing discipline (see
        RA_Framing_Discipline.md), RA claims must trace to
        vertices + edges + BDG filter + LLC.  Axiomatizing
        Lorentz invariance of the Minkowski vacuum imports a
        continuum QFT result that the RA-native programme is
        supposed to DERIVE, not assume.

    (c) petz_monotonicity (line 436, axiom):
        Data processing inequality for quantum relative entropy
        under CPTP maps. Mathematical axiom (not QFT-specific).
        Closable by importing Lean-QuantumInfo and writing a
        ~50-line adapter between DensityMatrix (local defn) and
        MState (LQI defn). NOT load-bearing for L04 or L05.

  dependency_graph: >
    frame_independence (L04) invokes:
      ├─ vacuum_lorentz_invariant     [AXIOM-QFT]   ← item (b)
      └─ relEnt_unitary_invariant     [proved]
          └─ log_unitary_conj         [proved, 1 line]
              └─ Matrix.cfc_conj_unitary [SORRY]    ← item (a)

    rindler_stationarity (L05) = frame_independence applied to
    rindlerThermal. Inherits both (a) and (b) dependencies.

    petz_monotonicity (c) is stated but NOT invoked by L04 or L05.

  status_correction: >
    L04 and L05 should be labeled "LV-conditional" (conditional
    on items (a) and (b)) rather than unconditional LV, until
    either:
      • Item (a) is discharged by copying the LQI proof (trivial);
      • Item (b) is replaced by a BDG-native derivation of
        Lorentz invariance of the vacuum state, OR the L04/L05
        claim is restated so it does not require this axiom.

  inconsistency_with_apr16_update: >
    The RAKB Apr 16 update listed O11 (LORENTZ_DISSOLUTION) as
    DISSOLVED via D11, with the rationale:
      "Lorentz invariance IS causal invariance of the quantum
       measure (Lean-verified) read through the Benincasa-Dowker
       sprinkling limit."

    This dissolution claim is INCONSISTENT with the continued
    presence of vacuum_lorentz_invariant as a QFT-imported axiom
    in the Lean core. A genuine dissolution would derive the
    vacuum-invariance property from L07 (causal invariance) plus
    the BDG sprinkling limit, eliminating the need for the
    axiom.

    Three options for resolution:
      1. Actually prove vacuum_lorentz_invariant from L07 + BDG
         sprinkling (upgrades dissolution from claim to theorem;
         removes the axiom).
      2. Downgrade O11 from DISSOLVED back to OP, with the note
         that the dissolution requires closing this specific gap.
      3. Reformulate L04/L05 so they don't depend on vacuum
         invariance as a separate axiom (e.g., state them for
         any U-invariant reference state σ₀ and let the physics
         map to Minkowski vacuum separately).

  target: >
    Either discharge vacuum_lorentz_invariant as a theorem of
    BDG + causal invariance (preferred), or revise O11 status
    and L04/L05 labels to accurately reflect the dependency.

  detection_source: >
    Direct inspection of RA_AQFT_Proofs_v10.lean on April 17, 2026.
    The file's own status table (lines 448-468) and "one axiom
    that is NOT a Lean gap" note (lines 479-486) correctly
    flagged these items. The RAKB and website narration had
    compressed these caveats out, and the Apr 16 "O11 DISSOLVED"
    claim was made without reconciling with the continued
    presence of the axiom in the Lean core.
```

---

## MODIFIED CLAIMS (status corrections)

```yaml
# L04: downgrade from unconditional LV to LV-conditional
L04:
  status: LV-conditional
  conditions: [IC46.a, IC46.b]
  gap: >
    Depends on Matrix.cfc_conj_unitary sorry (trivially closable
    from LQI) AND vacuum_lorentz_invariant axiom (QFT import,
    framing-discipline violation).
  previous_status: LV
  correction_date: 2026-04-17
  correction_source: direct Lean inspection

# L05: same correction as L04 (L05 is a one-line corollary)
L05:
  status: LV-conditional
  conditions: [IC46.a, IC46.b]
  gap: Inherited from frame_independence (L04).
  previous_status: LV
  correction_date: 2026-04-17

# O11: reopen or requalify the "DISSOLVED" claim
O11:
  status: DISSOLVED-pending-reconciliation
  note: >
    The dissolution claim from Apr 16 (Lorentz invariance IS
    causal invariance via BDG sprinkling) is not yet reflected
    in the Lean core, which still imports vacuum_lorentz_invariant
    as a QFT axiom. Until the axiom is replaced by a theorem,
    or L04/L05 are restated to not require it, the dissolution
    is provisional rather than actualized.
  target: >
    Derive vacuum_lorentz_invariant from L07 (causal_invariance)
    + BDG sprinkling limit, closing the axiom. If successful,
    O11 can be upgraded to fully DISSOLVED.
  previous_status: DISSOLVED (Apr 16)
  correction_date: 2026-04-17
```

---

## RAKB STATUS CHANGE

```yaml
# Before correction (Apr 16 state)
pre_correction:
  LV: 18
  CV: 33
  DR: 110
  AR: 26
  OP: 1
  Conjecture: 4
  DISSOLVED: 2
  total: 194

# After correction (Apr 17 state)
post_correction:
  LV: 16           # -2 (L04, L05 move to LV-conditional)
  LV_conditional: 2  # NEW (L04, L05)
  CV: 33
  DR: 110
  AR: 26
  OP: 1
  Conjecture: 4
  DISSOLVED: 1     # -1 (O11 → pending-reconciliation)
  DISSOLVED_pending: 1  # NEW (O11)
  total: 194
  notes: >
    Total claim count unchanged; only status labels refined.
    The two LV-conditional items can be promoted to LV by
    closing the Matrix.cfc_conj_unitary sorry (trivial) and
    either proving or removing vacuum_lorentz_invariant.
```

---

## ACKNOWLEDGMENT

This correction was surfaced because Joshua Sandeman directly inspected
the Lean source file (RA_AQFT_Proofs_v10.lean) and caught that the
programme-state narration (session logs, RAKB summaries, website) had
compressed out these caveats. The file's own in-source documentation
was honest about the gaps; the narration layer had not been faithful
to the source.

This is an example of the "narration vs primary materials" problem
that motivated the Stage A audit plan. More corrections of this kind
are likely when the other Lean files are inspected systematically.

---

*Patch produced April 17, 2026.*
*Joshua F. Sandeman · Claude (Opus 4.7)*
