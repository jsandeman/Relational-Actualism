# RA Native Bedrock Audit v1

## Scope

This pass audits the Lean bedrock under the native-first framing discipline, focusing on:

- `RA_GraphCore.lean`
- `RA_AmpLocality.lean`
- `RA_O14_Uniqueness.lean`
- `RA_D1_Proofs.lean`

## Counts by file and status

| file                   |   deferred_bridge |   mixed_rewrite |   native_candidate_rewrite |   native_core |   non_native |
|:-----------------------|------------------:|----------------:|---------------------------:|--------------:|-------------:|
| RA_AmpLocality.lean    |                 0 |               0 |                          2 |            11 |            0 |
| RA_D1_Proofs.lean      |                 8 |               2 |                         53 |            11 |           12 |
| RA_GraphCore.lean      |                 0 |               1 |                          2 |            23 |            0 |
| RA_O14_Uniqueness.lean |                 0 |               0 |                          0 |            48 |            4 |

Status vocabulary:

- `native_core`: already aligned with DAG + BDG + LLC primitives
- `native_candidate_rewrite`: mathematical content is native, but naming/commentary or surrounding framing still leaks legacy theory language
- `mixed_rewrite`: theorem is mostly native but packaged as a translation alias
- `deferred_bridge`: explicitly bridge-facing; not on the current active path
- `non_native`: imports forbidden theory objects or uses them as mechanisms / targets

## Main conclusions

### 1. `RA_GraphCore.lean` is the cleanest structural bedrock

The file is overwhelmingly native-core: vertex, edge, actualization graph, LLC, causal cuts, flux decomposition, and the graph-cut theorem all live directly in the allowed primitive vocabulary.

Two caveats:

- `horizon_partition` is just a translation alias for `RA_graph_cut_theorem`. It should not live in the native root.
- `MarkovBlanket` / `MarkovBlanket.boundary` encode a promising native shielding structure, but the terminology is imported and the file does not yet prove a blanket theorem. This should be recast as a causal shield / boundary structure before promotion.

### 2. `RA_AmpLocality.lean` is native, with one terminology leak

The core of the file is strongly native: causal DAGs, causal past, causal intervals, BDG increments, and locality of the BDG amplitude.

The strongest part is `bdg_amplitude_locality`. Under the framing discipline, amplitude locality is explicitly admitted as genuinely RA-native.

The only place I would pause is `quantum_measure` / `bdg_causal_invariance`. The underlying result is still useful and likely native in substance, but the labels package it in legacy quantum-measure language. This looks like a rewrite problem, not a theorem problem.

### 3. `RA_O14_Uniqueness.lean` contains an excellent native arithmetic core plus a clear leak

Sections deriving the Yeats moments, binomial coefficients, BDG coefficient vector, second-order identity, and hockey-stick checks are clean native-core mathematics.

The leak is narrow and obvious:

- `alpha_inv_137`
- `twelve_squared`
- `screening_seven`
- `alpha_s_weight`

Under the current framing discipline these do not belong in the active native root, because they target coupling-constant objects rather than direct Nature-target quantities or internal RA structural invariants.

The `yeats_eq_choose_k*` theorems themselves are fine as arithmetic identities. What must be handled carefully is the *file-level claim*: the Lean proves the arithmetic side; the Lorentzian geometric identification remains external.

### 4. `RA_D1_Proofs.lean` is the key file that must be split

This is the biggest result of the pass.

`RA_D1_Proofs.lean` is **not** a uniform module. It contains:

- a substantial native BDG motif / extension / closure core (Sections 0–14)
- a clearly non-native translation layer (Section 15)
- a deferred bridge layer (Section 16)
- alias packaging that still carries SM-facing language (Section 17)

#### Safe native core inside D1
The following are the strongest native pieces:

- `bdgScore`
- `chainScore`
- `D1a_fixed_point`
- `D1a_positive_iff`
- boundary/filter threshold theorems in Section 12

These are already close to native-root quality.

#### Native mathematics that still needs language cleanup
Most of Sections 2–14 are mathematically RA-native but still named through translation labels:

- `D1b_sym_yjoin`, `D1b_asym_yjoin`
- `D1c_gluon_*`, `D1c_quark_*`
- `D1d_gluon_convergence`, `D1d_quark_convergence`
- `gluon_confinement_length`, `quark_confinement_length`
- `D1f_*` baryon-language theorems
- `D1g_*` chirality-language theorems

These should be preserved but renamed into motif / N-vector / winding / DAG-irreversibility language.

#### Non-native section to remove from active frontier
Section 15 is not on the active native path. It imports coherent-state, SU(2), hypercharge, and Gell-Mann–Nishijima language as explanatory machinery.

All `D1h_*` declarations should be moved out of the native root.

#### Deferred bridge section to archive
Section 16 is explicitly bridge-facing:

- `relative_entropy_self_zero`
- `vacuum_stress_energy_zero`
- `P_act_conservation`
- `RA_field_equation_unique`

These are not wrong to keep in the repository, but they are no longer native-frontier theorems.

### 5. The current `lakefile.lean` root is too broad for a native-first build target

At present the default roots include AQFT, Koide, spin-2, and the unsplit D1 file. That is acceptable for a full-project build, but not for a native-first proof frontier.

The native root should be narrowed.

## Recommended split plan

### `RA_GraphCore.lean`
Keep as native root after:
- moving `horizon_partition` to a translation layer
- renaming `MarkovBlanket` to a native shield/boundary term
- adding an actual theorem about shielding if Paper IV is to rely on it

### `RA_AmpLocality.lean`
Keep as native root after:
- optionally renaming `quantum_measure` to something less imported
- optionally renaming `bdg_causal_invariance` to extension-order invariance / foliation-order invariance

### `RA_O14_Uniqueness.lean`
Split into:
- `RA_O14_Uniqueness_Core.lean` — arithmetic core only
- `RA_O14_Translations.lean` — alpha/coupling overlays, if retained at all

### `RA_D1_Proofs.lean`
Split into:
- `RA_D1_Core.lean` — Sections 0–14
- `RA_D1_Translations.lean` — Section 15 + Section 17 aliases
- `RA_D1_Bridge.lean` — Section 16

## Immediate next theorem targets

1. Promote `RA_graph_cut_theorem` as the canonical native statement and remove horizon aliasing from the root.
2. Recast `MarkovBlanket` as a native shield/boundary object and prove at least one nontrivial shielding theorem.
3. Split `RA_O14_Uniqueness.lean` so the BDG coefficient derivation stands alone without alpha-language contamination.
4. Split `RA_D1_Proofs.lean` at Section 15 and rename the Section 0–14 theorem vocabulary into motif / N-vector language.
5. After that, audit `RA_BaryonChirality.lean` using the same declaration-level method.

## Proposed temporary native root

Before any theorem changes, the cleanest temporary native root is:

- `RA_GraphCore`
- `RA_AmpLocality`
- `RA_O14_Uniqueness` (with Sections 8–9 treated as quarantined)
- `RA_D1_Core` (not the current full `RA_D1_Proofs`)

## Bottom line

The native programme is viable. The strongest current Lean bedrock is real. The main obstacle is no longer missing proof in these four files; it is **semantic hygiene and module boundaries**.

The most valuable next move is not proving more bridge theorems. It is splitting the bedrock so the genuinely native core can stand on its own, cleanly.
