# RA Hasse Frontier FiniteMaxExist Work Packet — Apr 29 2026

This packet adds the next Lean scaffold in the Selector Closure theorem programme:

```text
RA_HasseFrontier_FiniteMaxExist_v1.lean
```

## Install

From the RA repo root:

```bash
cp RA_HasseFrontier_FiniteMaxExist_Work_Apr29_2026/lean/RA_HasseFrontier_FiniteMaxExist_v1.lean    src/RA_AQFT/
```

Add the Lake root after `RA_HasseFrontier_FiniteMax_v1`:

```lean
`RA_HasseFrontier_FiniteMax_v1,
`RA_HasseFrontier_FiniteMaxExist_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake env lean RA_HasseFrontier_FiniteMaxExist_v1.lean
lake build
```

## RAKB update

From `docs/RA_KB`:

```bash
cp /path/to/RA_HasseFrontier_FiniteMaxExist_Work_Apr29_2026/scripts/apply_hasse_finite_max_exist_v1_upserts.py scripts/
```

Dry run:

```bash
python scripts/apply_hasse_finite_max_exist_v1_upserts.py   --registry ./registry   --reports ./reports   --packet-root /path/to/RA_HasseFrontier_FiniteMaxExist_Work_Apr29_2026   --dry-run
```

Apply:

```bash
python scripts/apply_hasse_finite_max_exist_v1_upserts.py   --registry ./registry   --reports ./reports   --packet-root /path/to/RA_HasseFrontier_FiniteMaxExist_Work_Apr29_2026
```

Validate:

```bash
python scripts/validate_rakb_v0_5.py
```
