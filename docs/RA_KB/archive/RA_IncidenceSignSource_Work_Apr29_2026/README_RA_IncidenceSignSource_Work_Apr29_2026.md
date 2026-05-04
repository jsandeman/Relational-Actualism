# RA Incidence Sign Source work packet — Apr 29 2026

Copy `lean/RA_IncidenceSignSource_v1.lean` into `src/RA_AQFT/`, add it as a Lake root after `RA_IncidenceCharge_v1`, then run:

```bash
cd src/RA_AQFT
lake env lean RA_IncidenceSignSource_v1.lean
lake build
```

This file is a conditional scaffold, not the hard theorem. It proves that a deterministic frontier orientation chart induces the incidence sign source and hence the seven-value signed N1 charge ledger. The next target is deriving the chart from graph-native frontier/orientation data.

To apply RAKB upserts from `docs/RA_KB`:

```bash
cp /path/to/RA_IncidenceSignSource_Work_Apr29_2026/scripts/apply_incidence_sign_source_v1_upserts.py scripts/
python scripts/apply_incidence_sign_source_v1_upserts.py --registry ./registry --reports ./reports --packet-root /path/to/RA_IncidenceSignSource_Work_Apr29_2026 --dry-run
python scripts/apply_incidence_sign_source_v1_upserts.py --registry ./registry --reports ./reports --packet-root /path/to/RA_IncidenceSignSource_Work_Apr29_2026
python scripts/validate_rakb_v0_5.py
```
