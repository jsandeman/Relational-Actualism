# RA Selector Closure Work Packet

This packet advances the Actualization Selector breakthrough into a concrete Lean v1 scaffold.

## Main file

```text
lean/RA_ActualizationSelector_v1.lean
```

It is intended as a non-root exploratory Lean file at first:

```text
src/RA_AQFT/RA_ActualizationSelector_v1.lean
```

## Recommended local check

```bash
cp lean/RA_ActualizationSelector_v1.lean /path/to/RA/src/RA_AQFT/
cd /path/to/RA/src/RA_AQFT
lake env lean RA_ActualizationSelector_v1.lean
```

## RAKB update

This v2 packet does not replace the selector issue update packet. Apply the selector issue update first if you have not already done so. Then use the v2 upserts to add this Lean artifact and the formalization report as source artifacts.

From `docs/RA_KB`:

```bash
cp <packet>/scripts/apply_selector_v2_upserts.py scripts/
python scripts/apply_selector_v2_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root <packet> \
  --dry-run
python scripts/apply_selector_v2_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root <packet>
python scripts/validate_rakb_v0_5.py
```

## Epistemic discipline

Do not mark the Selector Closure Theorem as proved. Mark this as:

```text
exploratory_formalization_scaffold
weak lemmas proved; hard selector closure open
```
