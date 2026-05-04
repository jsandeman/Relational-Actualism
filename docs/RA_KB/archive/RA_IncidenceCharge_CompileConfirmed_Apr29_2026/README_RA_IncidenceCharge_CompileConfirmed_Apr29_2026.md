# RA Incidence Charge compile-confirmed packet — Apr 29 2026

This packet records local build success for `RA_IncidenceCharge_v1.lean`.

From `docs/RA_KB`:

```bash
cp /path/to/RA_IncidenceCharge_CompileConfirmed_Apr29_2026/scripts/apply_incidence_charge_v2_compile_upserts.py scripts/
python scripts/apply_incidence_charge_v2_compile_upserts.py --registry ./registry --reports ./reports --packet-root /path/to/RA_IncidenceCharge_CompileConfirmed_Apr29_2026 --dry-run
python scripts/apply_incidence_charge_v2_compile_upserts.py --registry ./registry --reports ./reports --packet-root /path/to/RA_IncidenceCharge_CompileConfirmed_Apr29_2026
python scripts/validate_rakb_v0_5.py
```
