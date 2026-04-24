# RA Theorem Inventory v1

Method:
- Static source parse of uploaded Lean files (`theorem`, `lemma`, `axiom` declarations).
- No build execution was performed in this environment because the Lean toolchain (`lean`, `lake`) was not installed here.
- Therefore this is a declaration-level inventory, not yet a compile-validated proof-status report.

## Default root set from `lakefile.lean`
1. `RA_GraphCore`
2. `RA_D1_Proofs`
3. `RA_Koide`
4. `RA_AQFT_Proofs_v10`
5. `RA_AmpLocality`
6. `RA_Spin2_Macro`
7. `RA_O14_Uniqueness`
8. `RA_BaryonChirality`

## Counts by file
| file                           | root_layer           |   axiom |   lemma |   theorem |
|:-------------------------------|:---------------------|--------:|--------:|----------:|
| RA_Complexity_Proofs.lean      | complexity_straggler |       2 |       3 |         7 |
| RA_AQFT_Proofs_v10.lean        | default_root         |       2 |       5 |         4 |
| RA_AmpLocality.lean            | default_root         |       0 |       3 |         2 |
| RA_BaryonChirality.lean        | default_root         |       0 |       1 |        12 |
| RA_D1_Proofs.lean              | default_root         |       0 |       9 |        67 |
| RA_GraphCore.lean              | default_root         |       0 |      11 |         2 |
| RA_Koide.lean                  | default_root         |       0 |       5 |         7 |
| RA_O14_Uniqueness.lean         | default_root         |       0 |       0 |        50 |
| RA_Spin2_Macro.lean            | default_root         |       0 |       1 |         1 |
| RA_AQFT_CFC_Patch.lean         | nonroot              |       0 |       1 |         0 |
| RA_AQFT_Proofs.lean            | nonroot              |       3 |       3 |         4 |
| RA_AQFT_Proofs_v2.lean         | nonroot              |       0 |      10 |        10 |
| RA_Alpha_EM_Proof.lean         | nonroot              |       0 |       6 |        14 |
| RA_CFC_Port.lean               | nonroot              |       0 |       1 |         5 |
| RA_PACT_conservation_lean.lean | nonroot              |       1 |       0 |         6 |
| RA_Proofs_Lean4.lean           | nonroot              |       3 |       8 |         9 |

## High-value audit observations
- `RA_AQFT_Proofs_v10.lean` is the only default-root file with live gap exposure in the current snapshot: one live `sorry` (`Matrix.cfc_conj_unitary`) and two axioms (`vacuum_lorentz_invariant`, `petz_monotonicity`).
- `RA_GraphCore.lean` contains the graph-cut theorem and a `MarkovBlanket` structure, but not the theorem `markov_blanket_shielding`.
- `markov_blanket_shielding` appears in `RA_Proofs_Lean4.lean` and in the uploaded `RA_Complexity_Proofs.lean`, both outside the default root set.
- `RA_Complexity_Proofs.lean` is therefore a Paper-IV-relevant straggler, not part of the current default formal bedrock.
- `RA_D1_Proofs.lean` and `RA_O14_Uniqueness.lean` carry much of the theorem volume for Papers II and III.

## Consequence for the audit
The formal audit should be split into:
1. default-root bedrock;
2. nonroot bridge/legacy files still cited by the papers;
3. Paper-IV complexity stragglers.

That split matters because some paper claims currently read as if they rest on the default Lean core, when in fact they are only formalized in nonroot files.
