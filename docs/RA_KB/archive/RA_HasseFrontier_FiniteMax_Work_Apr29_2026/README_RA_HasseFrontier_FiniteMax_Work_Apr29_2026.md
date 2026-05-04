# RA Hasse Frontier FiniteMax Work Packet

Copy `lean/RA_HasseFrontier_FiniteMax_v1.lean` into `src/RA_AQFT/`, add it to the Lake roots after `RA_HasseFrontier_Maximal_v1`, then run:

```bash
cd src/RA_AQFT
lake env lean RA_HasseFrontier_FiniteMax_v1.lean
lake build
```

The file is a finite-enumeration scaffold. It does not yet prove finite maximum existence; it packages the data needed for the next proof step.

RAKB upserts can be applied from `docs/RA_KB` with:

```bash
python scripts/apply_hasse_finite_max_v1_upserts.py   --registry ./registry   --reports ./reports   --packet-root /path/to/RA_HasseFrontier_FiniteMax_Work_Apr29_2026   --dry-run
```
