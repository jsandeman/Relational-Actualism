# RA Incidence Charge Work Packet — Apr 29 2026

This packet introduces `RA_IncidenceCharge_v1.lean`, the first conditional topological charge-sign scaffold after the compile-confirmed Hasse-frontier finite-existence layer.

Install:

```bash
cp RA_IncidenceCharge_Work_Apr29_2026/lean/RA_IncidenceCharge_v1.lean src/RA_AQFT/
```

Add to Lake roots after `RA_HasseFrontier_FiniteMaxExist_v1`:

```lean
`RA_HasseFrontier_FiniteMaxExist_v1,
`RA_IncidenceCharge_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake env lean RA_IncidenceCharge_v1.lean
lake build
```

RAKB upsert from `docs/RA_KB`:

```bash
cp /path/to/RA_IncidenceCharge_Work_Apr29_2026/scripts/apply_incidence_charge_v1_upserts.py scripts/
python scripts/apply_incidence_charge_v1_upserts.py --registry ./registry --reports ./reports --packet-root /path/to/RA_IncidenceCharge_Work_Apr29_2026 --dry-run
python scripts/apply_incidence_charge_v1_upserts.py --registry ./registry --reports ./reports --packet-root /path/to/RA_IncidenceCharge_Work_Apr29_2026
python scripts/validate_rakb_v0_5.py
```
