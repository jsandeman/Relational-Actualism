# RA Bridge Support Supplement v1

## Scope

This supplement focuses on the specific files that now control the weak-field and lensing audit.

The important shift from the previous pass is that I inspected the *substance* of the bridge-support declarations, not only their names and file locations.

## Main finding

The present bridge support is **layered but uneven**:

1. The papers give a clear semantic bridge from BDG to the Einstein–Hilbert sector.
2. The current Lean files contain *named* conservation and bridge theorems.
3. But the specific bridge-support theorems I inspected are still at **scaffold / placeholder** level rather than being a typed end-to-end formal closure.

That does **not** collapse the programme. It does change how the bridge should be described:

- safe wording: **derived / translation-level / conditional on the published BDG-to-EH limit plus explicit bridge assumptions**
- unsafe wording: **Lean-verified end-to-end gravitational closure**

## Direct inspection highlights

### 1. `RA_D1_Proofs.lean` (default root)

This file contains bridge-named declarations including `P_act_conservation` and `RA_field_equation_unique`.

However, the displayed theorem currently has the form:

```lean
theorem P_act_conservation :
    (0 : ℤ) * 0 + 0 * 0 = 0 := by simp
```

That is a placeholder arithmetic witness, not a typed proof of stress-tensor conservation.

### 2. `RA_PACT_conservation_lean.lean` (nonroot)

This file is a clearer attempt at the intended bridge theorem chain, but it is still explicitly provisional.

Key points from direct inspection:

- `vacuum_T_zero` is an **axiom**
- `LLC_implies_T_conservation` is proved as `True := trivial`
- `P_act_T_conserved` is proved as `True := by trivial`
- `RA_field_equation_unique` is proved as `True := trivial`

So this file is best read as a **proof scaffold / formal roadmap**, not as completed formal closure.

### 3. `RA_AQFT_Proofs_v10.lean` (default root)

This remains the main AQFT adapter file for frame-independence language.

Static pass summary:

- 4 theorems
- 5 lemmas
- 2 axioms
- 5 `sorry`s

That is enough for a disciplined conditional bridge, but not enough to market the AQFT layer as closed.

### 4. Script layer already separates “good benchmark” from “hard wall”

The strongest part of the current Python layer is its honesty:

- `ra_flat_rotation_curve.py` is a calibration / explanatory script because it sets the flat-curve scale from a target velocity.
- `bullet_cluster.py` ends with an explicit statement that the framework is consistent in outline but that the lensing-source relation remains a hard wall.

That script-level honesty should be mirrored in the papers.

## Recommended use in the suite

### Safe claims now

- Paper III can continue to present the BDG→Einstein–Hilbert bridge as a **translation-level derivation chain**.
- Solar weak-field observables can be presented as **benchmark consequences conditional on the recovered Einstein sector**.
- Bullet Cluster and covariant cluster-lensing claims should remain **open computational targets**.

### Claims to avoid for now

- “The gravitational source-law bridge is Lean-verified.”
- “P_act-modified stress-tensor conservation has already been formally closed.”
- “Cluster lensing has been derived rather than sketched.”

## File summary

| artifact | kind | default root | theorem count | axiom count | sorry count | audit reading |
|---|---|---:|---:|---:|---:|---|
| RA_D1_Proofs.lean | Lean | yes | 67 | 0 | 0 | Contains bridge-named declarations, but direct inspection shows the displayed P_act-conservation theorem is a placeholder arithmetic statement `(0 : ℤ) * 0 + 0 * 0 = 0 := by simp`, not a typed stress-tensor conservation proof. |
| RA_PACT_conservation_lean.lean | Lean | no | 6 | 1 | 1 | Dedicated bridge file, but current theorem chain remains a scaffold: `vacuum_T_zero` is an axiom, `LLC_implies_T_conservation` is `True := trivial`, and `P_act_T_conserved` / `RA_field_equation_unique` are also proved only as `True`. |
| RA_AQFT_Proofs_v10.lean | Lean | yes | 4 | 2 | 5 | AQFT adapter layer still carries explicit axioms and sorrys; appropriate for conditional bridge support, not end-to-end formal closure. |
| RA_Proofs_Lean4.lean | Lean | no | 9 | 3 | 7 | Important nonroot support file for Paper IV and bridge rhetoric, but its current proof status is exploratory rather than canonical. |
| ra_flat_rotation_curve.py | Python | n/a |  |  |  | Useful calibration script. It sets the flat-curve scale by input target velocity, so it should be presented as an illustrative model, not a first-principles derivation. |
| bullet_cluster.py | Python | n/a |  |  |  | Strongly self-critical benchmark analysis. It concludes that the framework is consistent in outline but that the exact lensing source relation remains an open hard wall. |

## Bottom line

The weak-field/lensing bridge is now better characterized as:

**paper-semantic bridge + partial formal scaffolding + honest benchmark scripts + one remaining canonical source-law gap.**

That is already enough to support a disciplined programme. It is not yet enough to claim formal closure of the bridge itself.
