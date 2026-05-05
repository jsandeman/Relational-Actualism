# RA v1.3 Native Orientation-Link Derivation Report

## Purpose

v1.1 found exact confounding among support/frontier/orientation overlap in the v0.9/v1.0 component layer. v1.2 demonstrated that orientation-specific diagnostics become identifiable when given a distinct orientation-link surface, but that surface was synthetic. v1.3 replaces the synthetic row-metadata surface with a native Lean theorem/sign-source catalog surface.

## Native catalog

The analysis extracts theorem/definition names from native RA Lean files and classifies them into role/tag surfaces. Examples include:

- `one_way_precedence`
- `forward_winding_stable`
- `reverse_winding_filtered`
- `orientation_one_way`
- `orientation_asymmetry`
- `depth2_ledger_preserved_symmetric`
- native closure extension classifications

The resulting manifest is recorded in `ra_native_orientation_theorem_manifest_v1_3.csv`.

## Local result

The included local run produced:

- distinct native orientation catalog surface: yes;
- matched support/frontier strata with native orientation variation: yes;
- orientation-specific diagnostic resolved: yes;
- selector guardrail passed: yes;
- old orientation component remains confounded, as expected.

The key residual audit:

```text
native_orientation_link_overlap residual after support/frontier control ≈ 0.174
legacy orientation_overlap residual after support/frontier control ≈ 3.7e-16
```

This verifies that v1.3 is not simply reusing the old support/frontier/orientation triplet.

## Lean bridge

`RA_MotifNativeOrientationLinkDerivation.lean` imports the v1.2 orientation-link surface and native orientation/ledger/closure modules. It defines a native-catalog evidence layer refining the abstract orientation-link surface and then the generic orientation component surface. It does not assert a numerical rescue law.

## Caveat

The native-catalog surface is not yet per-graph witness extraction. It is an RA-native declaration/theorem-role surface. A future step should extract orientation-link witnesses directly from graph incidence/sign-source structures in the native orientation stack.
