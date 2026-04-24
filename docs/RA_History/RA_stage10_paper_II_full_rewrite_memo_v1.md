# RA Stage 10 — Paper II Full Rewrite Memo

## What this rewrite does

This is a full doctrinal rewrite of Paper II, not a local patch. The revised paper is organized around four requirements:

1. **RA-native mechanism first.** The proof path now runs through DAG growth, the BDG kernel, the local ledger condition, the arithmetic $d=4$ spine, and the compiled D1-native chain.
2. **Causal set theory made explicit as lineage.** The paper now states clearly that RA is built in the immediate lineage of causal set theory and explains what RA adds to CST to make a matter programme possible: irreversible actualization, realized/potentia state structure, local ledger conservation, and finite motif renewal.
3. **Compare without borrowing.** The paper now compares RA throughout with the Standard Model’s empirical domain—masses, interaction hierarchy, charge quantization, and matter-sector excess—without using gauge groups, field content, or renormalization machinery as RA’s proof path.
4. **Open sectors stated plainly.** Each major section now contains an explicit open-target paragraph where closure is still missing.

## Major structural changes

- Replaced the old Standard-Model-centered architecture with a native matter programme framed around motif sectors, closure windows, renewal, and orientation.
- Added a dedicated section on **From Causal Set Theory to a Matter Programme**.
- Rebuilt the matter taxonomy as a finite stable census in the $d=4$ regime, with comparison to familiar particle-sector language kept secondary.
- Reframed the numerical programme so that the observed fine-structure constant is treated as a direct measured target, not a running-coupling object.
- Recast proton-mass and proton-radius discussion as a native cascade programme with an explicit unresolved step ($N_{\mathrm{eff}}$ closure).
- Rewrote the force-range section around **closure burden and renewal**, contrasting this with gauge-boson and mediator-mass explanations.
- Rewrote the charge and matter-sector asymmetry material around **orientation**, **ledger structure**, and **severance boundary data**, with explicit comparison to the Standard Model’s charge operator and baryogenesis framing.
- Replaced archival/overlay-heavy framing with a compact final section stating exactly what the paper explains now and what it does not yet explain.

## Active support surface used positively

- `RA_GraphCore.lean`
- `RA_O01_KernelLocality_v2.lean`
- `RA_O14_ArithmeticCore_v1.lean`
- `RA_D1_NativeKernel_v1.lean`
- `RA_D1_NativeConfinement_v1.lean`
- `RA_D1_NativeClosure_v1.lean`
- `RA_D1_NativeLedgerOrientation_v1.lean`

## What remains deliberately open in the text

- complete proton-scale closure without the current $N_{\mathrm{eff}}=L_q^3$ hypothesis;
- direct force-law, scattering, and decay predictions;
- full observational cartography from motif sectors to all measured particle species;
- quantitative matter-sector excess from severance boundary data.

## Output files

- `RA_Paper_II_Matter_Forces_and_Motifs_native_v4.tex`
- `RA_Paper_II_Matter_Forces_and_Motifs_native_v4.pdf`
- `RA_Paper_II_native_v4.diff`
