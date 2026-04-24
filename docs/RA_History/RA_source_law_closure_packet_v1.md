# RA Source-Law Closure Packet v1

Artifacts in this packet:

- `RA_suite_primary_weak_field_source_law_note_v2.md`
- `RA_source_law_dictionary_v1.csv`
- `RA_script_rethreading_memo_v1.md`
- `ra_source_law_reference.py`
- `RA_source_law_reference_output_v1.txt`
- `RA_Paper_III_source_law_patch_v4.zip`
- `RA_issue_register_v3.md`
- `RA_issue_register_v3.csv`
- `RA_benchmark_support_matrix_v4.md`

## Main new finding

There is a previously unlogged load-bearing ambiguity in the current rotation-curve formulation.

Paper III currently pairs:

- a correction term \(+c^2\nabla^2\ln\lambda\),
- with a halo profile \(\lambda(r)\propto r^{-2}\),
- and the claim that this correction is positive in the halo regime.

Under standard radial Laplacians this combination is not generically compatible:
the \(r^{-2}\) profile is positive only under a 1D second-derivative reading, zero in 2D cylindrical radial form, and negative in 3D spherical radial form.

So the right immediate move is not to promote the halo mechanism harder.
It is to canonicalize the source-law operator/sign/geometry first.

## Net effect on the programme

The dense-regime viability case is stronger after this pass.

The halo / cluster programme is also clearer after this pass, because the exact bottleneck is now mathematical rather than rhetorical.
