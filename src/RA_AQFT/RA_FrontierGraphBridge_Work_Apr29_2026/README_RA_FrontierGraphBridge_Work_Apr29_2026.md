# RA Frontier/Graph Bridge Work Packet — Apr 29 2026

This packet contains the next Selector Closure theorem-step scaffold:

```text
RA_FrontierGraphBridge_v1.lean
```

It bridges the compiled frontier/incidence vocabulary to the concrete graph-core structures in `RA_GraphCore.lean`.

## Install Lean file

From repo root:

```bash
cp RA_FrontierGraphBridge_Work_Apr29_2026/lean/RA_FrontierGraphBridge_v1.lean \
   src/RA_AQFT/
```

Add this root to `src/RA_AQFT/lakefile.lean` after the selector/frontier roots:

```lean
`RA_ActualizationSelector_v1,
`RA_FrontierIncidence_v1,
`RA_FrontierGraphBridge_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake env lean RA_FrontierGraphBridge_v1.lean
lake build
```

## Apply RAKB upserts

From `docs/RA_KB`:

```bash
cp /path/to/RA_FrontierGraphBridge_Work_Apr29_2026/scripts/apply_frontier_graph_v1_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_frontier_graph_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_FrontierGraphBridge_Work_Apr29_2026 \
  --dry-run
```

Apply:

```bash
python scripts/apply_frontier_graph_v1_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RA_FrontierGraphBridge_Work_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```

## Expected status

Before local Lean compile:

```text
static_no_sorry_no_admit_no_axiom_build_pending
```

After successful local compile / lake build:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
```

## Scope

This is still a bridge scaffold. It does not prove the hard Selector Closure theorem. It re-expresses graph-core LLC/cut conservation as frontier-boundary ledger conservation and prepares the next hard theorem: concrete reachability/Hasse-frontier construction.
