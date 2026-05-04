# RA Hasse Frontier Maximal fix packet — Apr 29 2026

This packet fixes the Lean error in `RA_HasseFrontier_Maximal_v1.lean` where a declaration returning structure data was incorrectly marked as a `theorem`.

## Install

From the repo root:

```bash
cp RA_HasseFrontier_Maximal_Fix_Apr29_2026/lean/RA_HasseFrontier_Maximal_v1.lean \
   src/RA_AQFT/RA_HasseFrontier_Maximal_v1.lean

cd src/RA_AQFT
lake env lean RA_HasseFrontier_Maximal_v1.lean
lake build
```

## Patch-only option

```bash
git apply RA_HasseFrontier_Maximal_Fix_Apr29_2026/patches/patch_RA_HasseFrontier_Maximal_v1_theorem_to_def.diff
```
