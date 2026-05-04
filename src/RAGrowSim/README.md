# RAGrowSim

Julia implementation of the RA growth dynamics with ledger and seeded
initial conditions.

## What changed (April 28 2026)

The original simulator (April 27) ran the BDG dynamics from an empty DAG with antichain-only parent enumeration. Two issues with that:

1. **Antichain-only is wrong.** The Lean enumeration tables (`RA_D1_Core_draft.lean` lines 453–487) enumerate *all subsets* of existing vertices as candidate parent sets. The BDG filter handles non-antichain subsets correctly via the cardinality structure.

2. **Empty DAG is the wrong initial condition.** Per RA, every DAG nucleates from a parent (vacuum nucleation or severance daughter), and the kernel saturation theorem (`kernel_saturation.py`) shows that nucleation occurs at saturation, not from emptiness. Empty-DAG growth under strict S>0 collapses to all-isolated vertices (we verified this).

The new architecture fixes both: candidates are all subsets (with a `max_parent_size` cap for tractability), and seeds are explicit (vacuum nucleation, severance daughter, or one of the canonical D1 motifs).

A third addition: **pluggable ledger rules** (`LedgerRule` strategies), per RA-MATTER-CHARGE-001 and RA-OPEN-CHARGE-SIGN-001. The edge-level sign-source for the signed N1 charge is an open formalization target, so we provide `Neutral` (zero ledger baseline), `EnumerateLLC` (conservative LLC-respecting enumeration with no claim about physical measure), and a placeholder for `OrientationRuleV0` (future graph-native sign rule).

## Layout

```
RAGrowSim/
├── Project.toml
├── README.md
├── src/
│   ├── RAGrowSim.jl        # top-level package
│   ├── BDGGrow.jl          # core: DAG, profile, bdgscore
│   ├── Ledger.jl           # EdgeLedger, VertexLedger, admissibility
│   ├── LedgerRules.jl      # Neutral, EnumerateLLC, OrientationRuleV0
│   ├── Antichains.jl       # antichain enumeration (kept; not used by Dynamics)
│   ├── Seeds.jl            # vacuum_nucleation, severance_daughter,
│   │                       # seed_chain, seed_sym_branch, seed_asym_branch
│   ├── Dynamics.jl         # the growth rule with ledger + seeds
│   └── Observables.jl      # statistics from a GrowthHistory
├── test/
│   ├── runtests.jl
│   ├── test_BDGGrow.jl
│   ├── test_Ledger.jl
│   ├── test_LedgerRules.jl
│   ├── test_Antichains.jl
│   ├── test_Seeds.jl
│   └── test_Dynamics.jl
└── scripts/
    ├── run_small.jl        # original empty-DAG runner (kept for diagnostics)
    └── run_seeded.jl       # new: seeded runs with ledger rule comparison
```

## Running tests

From the project root:

```bash
julia --project=. test/runtests.jl
```

## Running a seeded simulation

```bash
julia --project=. scripts/run_seeded.jl chain4 12 30
```

Arguments:
- `seed_kind`: one of `chain4`, `chain2`, `sym_branch`, `asym_branch`
- `target_extra_n`: number of vertices to grow beyond the seed (default 12)
- `n_seeds`: number of independent runs (default 30)

The script runs both `Neutral` and `EnumerateLLC` ledger rules so you can see the difference.

## Methodological notes

**Stochasticity is intrinsic.** Paper I §Sequential Growth makes vertex selection stochastic ("among admissible candidates, one is actualized stochastically"). Monte Carlo over independent runs measures expected behavior of an inherently random process — this is not an approximation.

**Antichain enumeration is gone from the dynamics path.** The new `Dynamics.jl` enumerates all subsets up to `max_parent_size`, not antichains. The `Antichains.jl` module is retained for completeness and for tests that exercise it directly.

**Per-vertex LLC at birth checks signature only.** Per ChatGPT's Apr-28 note, the per-vertex LLC (incoming = outgoing) is enforced over the eventual neighborhood, not at the instant of birth. At birth we only check that the incoming qN1 sum lies in the seven-value signature {-3..+3}. Future actualizations close the outgoing-port obligations.

**The sign-source is unresolved.** Per RA-OPEN-CHARGE-SIGN-001, the graph-native rule for assigning signs to individual N1 edges is not yet formalized. ChatGPT's Apr-28 deep analysis identifies the right target as **finite incidence / cochain incidence**: `s(e) = incidence(local oriented cell, e)` so that signs are induced by graph topology, not sampled. Until that rule is formalized, neither `Neutral` nor `EnumerateLLC` is a faithful implementation of the physical RA charge rule. Both are scaffolding:

  - `Neutral` is a no-charge baseline useful for isolating BDG dynamics.
  - `EnumerateLLC` is the conservative "no preferred orientation" enumeration. Its qN1 distribution emerges from uniform-pick over admissible sign assignments — this is *combinatorial* structure, not a physical prediction.

**Do not interpret the qN1 distribution from `EnumerateLLC` runs as RA's prediction for measured charge distributions.** It is the distribution the simulator sees under a uniform-measure assumption that RA does not actually make. The BDG profile statistics, by contrast, are measured from the topological side of the dynamics where Lean is fully verified and are physically meaningful.

**`max_parent_size = 4` by default.** This caps the candidate enumeration at C(n, ≤4), polynomial in n. All canonical D1 motifs use parent sets of size ≤ 3, so the cap does not exclude any known stable motif. Set `max_parent_size = typemax(Int)` for exact full enumeration (slow past n ≈ 20).

## Open formalization targets

- **`RA-OPEN-CHARGE-SIGN-001`**: graph-native edge-level sign-source for signed N1 ledger. Per ChatGPT's Apr-28 deep analysis, the right target is finite incidence / cochain incidence: `s(e) = incidence(local oriented cell, e)`, with the seven-value spectrum following from the at-most-three independent spatial directions in d=4. Two-stage formalization plan:
  - **Stage 1** (immediate): conditional Lean theorem — given a signed N1 frame with at most three directions, prove Q_N1 ∈ {-3..+3}.
  - **Stage 2** (deeper): construct the signed frame from graph topology. Likely route: oriented local cut → incidence signs on N1 links → signed N1 ledger → vertexwise LLC → discrete Stokes / cut conservation. Hardest sub-theorem: N2 winding boundary projects to N1 signature.
- N2 strong-sector channel enumeration (currently zero by default in `EnumerateLLC`). The unification hypothesis (N1 = boundary projection of N2) would make this redundant if proved; until proved, the two channels are tracked separately.
- Per-vertex LLC closure tracking (outgoing-port obligations); requires extending `DAG` to carry edge-ledger maps.
- A direct test that BDG profiles measured from grown DAGs converge to (or diverge from) Poisson(μ=1) at high local density. **Preliminary chain-4 seed result (Apr 28): the growing-DAG ⟨N_k⟩ does NOT match Poisson(μ=1) at this scale.** Worth confirming with multi-seed + μ-conditional analysis.
