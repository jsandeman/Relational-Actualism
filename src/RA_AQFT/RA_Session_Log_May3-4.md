# RA Session Log — May 3-4, 2026
## BMV Tier-1→4 + Lean Cleanup + Python/Julia Cleanup + Lit Review v1→v2 Self-Correction

---

## I. BMV Pipeline Build-Out (12 commits, May 3)

Build-out of `RA-PRED-008` (BMV gravity-mediated entanglement null
target) from comparator stub to research-grade analysis.

### Tier 1 — Three-model comparator

`bmv_comparator.py`: side-by-side prediction under quantized
gravity (Bose 2017), semiclassical (averaged source), and RA
(common-mode phase from Step-5 metric). Computes negativity,
Wootters concurrence, spin correlators across the time sweep.
At Bose 2017 nominal (m=1e-14 kg, dX=250 μm, T=2.5 s, parallel
geometry): quantized gives C ≈ 0.156; both semiclassical and RA
give machine zero. The pure-state identity C = 2N is satisfied
exactly.

**Files**: `bmv_comparator.py`, `test_bmv_comparator.py` (9/9),
`bmv_comparator_results.csv`. RAKB: `RA-PRED-008` created with
3 attached artifacts + edges; sources include the Apr 2026 BMV
note (previously unattached).

### Tier 2 — Lindblad decoherence + entanglement sudden death

Closed-form Lindblad evolution because [H_grav, σ_z^X] = 0 — each
off-diagonal element is multiplied by `exp(-Γ_eff·t)` where
Γ_eff counts how many indices flip. No numerical ODE integration
needed.

**Headline finding**: γ_ESD ≈ 0.06 /s — above this, concurrence is
*exactly* zero (Wootters formula sharp transition; state truly
separable, not weakly entangled). Required coherence time τ_coh ≥
17 s for C ≥ 0.01 detection; 49 s for C ≥ 0.1.

**Files**: `bmv_comparator.py` extended, `bmv_coherence_budget.csv`.
17/17 tests passing.

### Tier 2 (geometry comparison)

Parallel vs perpendicular geometry. Perpendicular (Bose 2017's
actual geometry, d=200 μm < dX=250 μm) gives ~2× larger Δφ and
~2× larger budget. Even so, required τ_coh ≈ 9 s — still much
longer than the ~2.5 s often cited.

### Tier 3 (environment bridge)

`gas_collision_rate(env, p)` and `blackbody_decoherence_rate(env, p)`
formulas. Bridge interpretation: λ_pos = Γ_decoh.

**Headline finding**: at idealized cryo UHV (1e-12 Pa, 0.1 K),
λ_pos ≈ 1.2e6 /s — about 10⁷ times larger than γ_ESD. The
branch-coherent regime is unreachable for the original Bose 2017
mass scale under any realistic conditions.

### Tier 3b — BDG-kernel actualization rate (Python)

`bdg_actualization.py`: λ_pos = Γ_cand · P_acc(μ) using
`bdg_acceptance_probability` from the existing `kernel_saturation.py`
infrastructure. Identifies three regimes:
- Saturated (μ > ~8): P_acc → 1; bridge interpretation holds
- Selective (μ ~ 3-5): P_acc ~ 0.4; ~2.5x suppression vs bridge
- Strongly-selective minimum at μ ≈ 4

11/11 tests passing.

### Tier 3c — Lean formalization (algebraic content)

`RA_BDG_ActualizationRate.lean` (Tier-A bedrock): formalizes the
arithmetic / algebraic content of the actualization-rate construction.
**17 theorems** including bridge limit, monotonicity in P_acc and
Γ_cand, bilinearity, upper bound (filter can only suppress, never
amplify), worked accept/reject examples at depths 1-4. Uses the
shared `c_BDG = (1, -1, 9, -16, 8)` from `RA_O14_ArithmeticCore`.

P_acc treated as an abstract real parameter in [0, 1]; probability
theory left as Tier 3d. Lake build clean: 0 sorry / admit / axiom /
warnings.

### Tier 3d — measure-theoretic interface (Lean)

`RA_BDG_PAccMeasure.lean` (Tier-A bedrock): lifts P_acc from
abstract real to a measure-theoretic quantity `(Measure BDGProfile
→ ℝ)` using Mathlib's MeasureTheory. **8 theorems** including the
trivial saturation point (Dirac at empty profile gives P_acc = 1),
bounds for any IsProbabilityMeasure, and the composition theorem
linking Tier 3c's `actualization_rate` at the saturation point.

Discrete σ-algebra (top) on BDGProfile with auto-derived
DiscreteMeasurableSpace + MeasurableSingletonClass. Joint
Poisson-CSG measure construction (`bdgProfileMeasure : ℝ≥0 →
Measure BDGProfile`) deferred to Tier 3e.

### Tier 4 — discriminator regime sweep

`bmv_discrimination_sweep.py`: 2D (m, T) grid sweep at fixed
(dX, d, env). Computes "realistic peak concurrence" (under
quantized gravity with Tier-3a decoherence applied).

**Verdict**: ALL three canonical reference points (Bose 2017,
Advanced near-term, Carney nominal) FAIL to discriminate under
both Bose-ideal and frozen-lab environments. Discriminating
frontier:
- (dX=1μm, d=2μm) Bose-ideal env: m ≥ 3e-14 kg
- (dX=1μm, d=2μm) frozen-lab env: m ≥ 1e-15 kg
- (dX=10nm, d=20nm) frozen-lab env: m ≥ 3e-18 kg

The Carney 1e-19 kg target is one decade below even the
nanoscale-frozen-lab frontier. 6/6 tests passing.

### Tier 3b mass-emergence — μ-dictionary catalog

`bmv_mu_dictionary.py`: 5 candidate identifications of μ for the
BMV apparatus, each with explicit provenance and assumption.
Only Dictionary D (μ = d = 4 universally) deviates from the bridge
limit, predicting ~2.5× universal positional-decoherence
suppression — a NEW testable signal independent of BMV.

New issue `RA-OPEN-BMV-MU-DICTIONARY-001` created, depending on
existing `RA-OPEN-MU-ESTIMATOR-001`, `RA-OPEN-ACTUALIZATION-
SELECTOR-001`, etc.

### Decoherence-landscape sweep + lit-review v1

`bdg_decoherence_predictions.py`: sweeps the universal-2.5x
prediction across 5 representative experimental classes. Initial
verdict: mature interferometry already ~10-20% precision, well
below the predicted 2.5x discrepancy → Dict D constrained.

`bdg_decoherence_channels.py`: refines via channel decomposition
(gas, blackbody, recoil, vibration, trap photons) and 4 candidate
filter masks (D_uniform, D_multi_vertex_only, D_gas_only,
D_BMV_specific). Initial verdict: even the most restricted
variant (D_gas_only) is constrained.

Wrote a self-contained lit-review prompt
(`lit_review_prompt_decoherence_budgets_May3_2026.md`) for a fresh
Claude chat to do a primary-source pass.

**v1 lit-review response** integrated; key correction: nominal vs
engineered conditions matter — the Hornberger 2003 / Hackermüller
2004 measurements engineered specific channels to dominate. Under
nominal C60 conditions gas+BB are only ~15% of the budget, not 80%.
Verdict reversed: D_multi_vertex_only and D_gas_only became
"CONSISTENT with measured mature data".

### v2 lit-review — SELF-CORRECTION

A second Claude reviewed the v1 lit review and identified two
**critical methodological issues**:

1. **Lindblad additivity is NOT universally valid**. Atom-IF
   vibration is ensemble phase variance (not Lindblad position
   decoherence). Trapped-lattice atom-IF is dominated by
   collective dephasing from anharmonic trap (not Lindblad).
   Heavy-mol nominal residual is instrumental (not Lindblad).
   Diamond-NV CoM is graphitization (not in any decoherence
   schema). BMV is missing magnetic-gradient + charge-multipole
   channels Bose 2017 explicitly identifies.

2. **The cumulative-Γ analysis was the WRONG analytical framing**.
   The right move is **per-channel constraint from engineered-
   condition measurements**: Hornberger 2003 directly bounds
   Γ_gas at <10% precision. Dict D's predicted 60% per-channel
   suppression is 6σ away from that — not "marginally constrained"
   by cumulative-Γ in nominal scenarios.

**Verdict reversed AGAIN**, much more sharply:
- D_uniform: FALSIFIED at 6.0σ (gas) + 4.0σ (BB) + 4.3σ (trap_photon)
- D_multi_vertex_only: FALSIFIED at 6.0σ + 4.0σ
- D_gas_only: FALSIFIED at 6.0σ (Hornberger 2003 alone)
- D_BMV_specific: FALSIFIED at 6.0σ + 4.3σ

The kernel-structural conjecture μ=d=4 universally is broadly
**closed by direct per-channel measurement**. Surviving escape
routes: non-universal μ-dictionary, filter touching only spontaneous
emission / laser phase noise (which aren't multi-vertex events
anyway), or Dict-D-as-universal is wrong.

Refactored `bdg_decoherence_channels.py` to v2 schema: 10 channels,
13 protocol-variant-split scenarios, `channel_additivity_valid`
flag, `unknown_fraction` field, `per_channel_constraints` function
as the headline analysis.

---

## II. Lean Corpus Cleanup (1 commit, May 4)

Naming convention: stripped `_v1`, `_v2`, `_draft` suffixes from 20
Lean filenames. Metadata about file age/version moved to file
comments.

**Judgment call** (user-confirmed): kept `_Core` and `_Native`
suffixes — these distinguish files that coexist by design
(`RA_GraphCore` vs `RA_GraphCore_Native`, `RA_AmpLocality` vs
`RA_AmpLocality_Native`).

**16 files archived** to `archive_lean_deprecated_May4_2026.zip`:
- `RA_AQFT_Proofs` (3 versions; IC46 framing violation per old lakefile docstring)
- `RA_AQFT_CFC_Patch`, `RA_CFC_Port`, `RA_BaryonChirality` (retired)
- `RA_AmpLocality_v2`, `RA_GraphCore_v2` (sorry-closure attempts)
- `RA_O14_Uniqueness`, `RA_O14_Uniqueness_Core_draft` (superseded by `ArithmeticCore`)
- `RA_BDG_Coefficient_Arithmetic_v2` (content moved into canonical name)
- `RA_D1_Proofs` (older D1 proofs)
- `RA_Alpha_EM_Proof`, `RA_PACT_conservation_lean`, `RA_Proofs_Lean4` (exploratory)
- `lakefile_v1.lean`

**2 new modules added to active roots**:
- `RA_O01_KernelLocality` (Tier A bedrock — kernel-locality lemma)
- `RA_MotifCommitProtocol` (Tier B native — consensus-inspired
  motif-commit semantics; finite-Hasse-frontier ↔ causal-support-cut
  bridge for motif readiness)

**Stale-import fix**: `RA_BDG_Coefficient_Arithmetic.lean` was
importing the obsolete `RA_O14_Uniqueness_Core_draft`; replaced
with the v2 content that imports the correct `RA_O14_ArithmeticCore`.

**4 new RAKB claim nodes**:
- `RA-MOTIF-COMMIT-001` — Hasse-frontier as causal support cut
  (formal_anchor: `supportCutOfFiniteHasseFrontier`; bridge theorem:
  `GraphReadyAt_supportCutOfFiniteHasseFrontier_iff`)
- `RA-MOTIF-COMMIT-002` — readiness is support-cut containment in
  realized causal past (`DAGReadyAt_iff_support_subset_realized_past`)
- `RA-MOTIF-COMMIT-003` — readiness is monotone toward causal future
- `RA-MOTIF-COMMIT-004` — committed motif excludes ready
  incompatible motifs at same site

All 4 tagged `lean_verified_or_compiled_native` with explicit
formal_anchor fields. **Lake build clean: 8299 jobs / 0 errors / 0
warnings**. File count: `src/RA_AQFT/*.lean` 54 → 38.

---

## III. Working-Tree Sync (1 commit, May 4)

`.gitignore` was root-anchored (`/.lake/`, `/build/`,
`/lake-packages/`); switched to unanchored. Added `~$*` (Office
lockfiles) and `relational-actualism-web/` (its own GitHub Pages
repo).

`git rm --cached -r src/RA_AQFT/.lake` removed 181 accidentally-
tracked Lean build cache files.

**547 previously-untracked files added**: top-level packets,
`docs/RA_Canonical_Papers/` paper bundle, `docs/RA_KB/` content
(README_RAKB_v0_5.md, archive/, scripts/, reports/, ~40 registry
.bak_* snapshots), `src/RAGrowSim/` (entire Julia package), several
`RA_*_Work_Apr29_2026/` directories.

**~14 pending deletions staged**: legacy `src/RA_KB/` Python tooling,
old `rakb.yaml`, etc.

---

## IV. Python + Julia Cleanup (2 commits, May 4)

Companion to the Lean cleanup. Python is more diverse (66 files
in `src/RA_AQFT/`, mixed conventions); Julia archived in full per
user directive.

**Python renames** (RA-prefixed CamelCase → snake_case):
- `RA_BDG_Simulation.py` → `bdg_simulation.py`
- `RA_D1_Proof.py` → `d1_proof.py`
- `RA_RASM_Verification.py` → `rasm_verification.py`

**Promotion**: `t1_forecast_deliverables_v2.py` → canonical name
(replacing v1; v1 archived).

**Python archived** (26 files in `archive_python_deprecated_May4_2026.zip`):
- 17 `apply_*_upserts.py` one-shot RAKB migration scripts (per
  CLAUDE.md "historical, not part of a CI loop")
- 1 superseded `t1_forecast_deliverables` v1
- 1 forecast variant
- 7 intermediate `berry_*.py` iterative-work scripts (per user
  decision after reviewing held-back items): berry_bridge,
  berry_computation, berry_decomposition, berry_derive_f,
  berry_gauge, berry_thinning, berry_transfer

**Berry-phase keepers in tree**: `berry_final.py`, `berry_theorems.py`
(the breakthrough modules from the Apr 12 8-iteration session).

**Held-in-tree per user decision**:
- `mu_int_derive.py` (RAKB status: `blocked_repair_required`)
- `actualization_thermo.py` (RAKB status:
  `blocked_missing_dependency_pending_reproduction`)

**Julia archived** (entire `src/RAGrowSim/` subtree, 56 files,
2.3 MB, plus standalone `src/RAGrowSim.tar.gz`) → `archive_julia_ragrowsim_May4_2026.zip`.

**RAKB updates**: 6 RAGrowSim rows + 9 berry rows + 1 O14 row
marked archived; 17+16 Python rename substitutions; 3 new archive
artifacts registered. After orphan-fix pass: 0 broken `repo_relative_path`
entries (was 7 — 1 from this session's archival, 6 pre-existing data-quality issues
in selector/frontier rows that were missing `docs/RA_KB/` prefix).

---

## V. End-of-session state

**Branch**: `main`, fully synced with `origin/main`.

**Build status**: lake build 8299 jobs / 0 errors / 0 warnings;
all 6 Python test suites in `src/RA_AQFT` pass (49 tests across
6 modules: test_bmv_comparator, test_bmv_discrimination_sweep,
test_bmv_mu_dictionary, test_bdg_actualization,
test_bdg_decoherence_predictions, test_bdg_decoherence_channels).

**RAKB validator**: PASSES.
- claims=43 (+4 RA-MOTIF-COMMIT-*)
- issues=25 (+2 RA-OPEN-BMV-MU-DICTIONARY-001 +
                  RA-OPEN-BDG-DECOHERENCE-CONSTRAINTS-001)
- targets=8 (+1 RA-PRED-008)
- artifacts=261
- claim_artifact_edges=381
- claim_edges=65 (+5)
- all_dependency_edges=178 (+7)
- 0 orphan repo_relative_path entries

**File counts**:
- `src/RA_AQFT/*.lean`: 38 (was 54)
- `src/RA_AQFT/*.py`: 33 (was 66)
- `src/RAGrowSim/`: removed (archived)

**Three archive zips at repo root** (all git-tracked):
- `archive_lean_deprecated_May4_2026.zip` (16 files, 209 KB)
- `archive_python_deprecated_May4_2026.zip` (26 files, ~118 KB)
- `archive_julia_ragrowsim_May4_2026.zip` (56 files + tar.gz, 442 KB)

---

## VI. Headline scientific findings (consolidated)

1. **BMV at the original Bose 2017 mass scale is decoherence-
   limited and cannot discriminate RA from quantized gravity** even
   in principle. RA's null prediction is intact but vacuously
   consistent with the (zero) experimental signal achievable at
   that scale.

2. **The "new prediction" angle (Dict D μ=d=4 ⇒ ~2.5× universal
   positional-decoherence suppression) is broadly closed by direct
   per-channel measurement.** Hornberger 2003 (gas), Hackermüller
   2004 (BB), Delić 2020 (trap photon) all directly bound the
   per-channel suppression factor at <10-15% precision; Dict-D's
   predicted 60% suppression is 4-6σ away. All four enumerated
   variants (D_uniform, D_multi_vertex_only, D_gas_only,
   D_BMV_specific) are FALSIFIED.

3. **Surviving escape routes are narrow**: (a) non-universal
   μ-dictionary that lands in saturation for measured scenarios
   (open `RA-OPEN-MU-ESTIMATOR-001`), (b) filter touching only
   spontaneous emission / laser phase noise (which aren't
   multi-vertex actualization candidates by any natural reading),
   or (c) Dict-D-as-universal is wrong, requiring a fundamentally
   different mass-emergence story.

4. **Discriminating BMV regime exists but requires nanoscale
   geometry + frozen-lab environment** (m ≈ 10⁻¹⁵ to 10⁻¹⁸ kg with
   nm-scale dX); the Carney 10⁻¹⁹ kg target is one decade below
   even the most aggressive currently-modeled frontier.

5. **Real methodological lesson** (the v1→v2 self-correction):
   Lindblad additivity is not universally valid; cumulative-Γ
   across mixed-channel nominal scenarios is the wrong analytical
   framing for constraining flat per-channel suppression.

---

## Commits in chronological order (oldest first)

```
c85cabc  RA Session May 3, 2026: BMV Tier-1 comparator + RAKB target RA-PRED-008
75326ee  RA Session May 3, 2026: BMV Tier-2 (Lindblad decoherence + ESD detection)
af443ed  RA Session May 3, 2026: BMV Tier-2 geometry comparison + Tier-3 environment
32038e7  RA Session May 3, 2026: BMV Tier-3b (BDG-kernel actualization rate)
c6d898a  RA Session May 3, 2026: BMV Tier-4 (discriminator regime sweep)
b9baa9c  RA Session May 3, 2026: BMV Tier-3c (Lean formalization of actualization rate)
07d7e1d  RA Session May 3, 2026: BMV Tier-3d (interface) — measure-theoretic P_acc
d2db406  RA Session May 3, 2026: BMV Tier-3b mass-emergence (mu-dictionary catalog)
22497ce  RA Session May 3, 2026: BDG decoherence-landscape sweep + empirical constraints
e80acee  RA Session May 3, 2026: channel-resolved BDG suppression analysis
4880081  Add lit-review prompt for decoherence-budget primary-source pass
f6a91c0  Integrate primary-literature-cited channel-budget breakdowns
4b30f95  v2 lit-review integration: per-channel constraints falsify all Dict-D variants
b42b902  Lean corpus cleanup pass — drop version suffixes, archive deprecated, integrate motif-commit
2c42da0  Sync working-tree to repo: track untracked work + fix .gitignore
19a9b14  Session summary doc for May 3-4 2026 work
a284e29  Python + Julia cleanup pass — rename, archive deprecated, archive Julia entirely
11cb740  Berry-phase iterative-work archival follow-up
(this commit) RAKB completeness pass: orphan-path fixes + session log
```
