# Prediction Source Linkage Candidate Report

This report inspects targeted string-search matches for `RA-PRED-001`, `RA-PRED-002`, and `RA-PRED-003`. It ranks files by match count and source-likelihood, but does not treat string matches as proof.

## RA-PRED-001 fine-structure
### Ranked candidate files
- `d3_alpha_s_BDG.py` — matches 5, score 18; terms: alpha_EM×2, alpha_em×2, 137.036×1
- `bdg_multicoupling.py` — matches 11, score 16; terms: alpha_EM×5, alpha_em×5, 137.036×1
- `D1_BDG_MCMC_simulation.py` — matches 7, score 12; terms: alpha_EM×3, alpha_em×3, 137.036×1
- `RA_Framing_Discipline.md` — matches 3, score 7; terms: 137.036×3
- `ra_calibration.py` — matches 2, score 7; terms: alpha_EM×1, alpha_em×1
- `RA_RASM_Verification.py` — matches 2, score 7; terms: alpha_EM×1, alpha_em×1
- `RA_Paper_II_Matter_Forces_and_Motifs_native_v5(1).tex` — matches 4, score 4; terms: 137.036×2, 941×1, proton×1
- `RA_Paper_II_Matter_Forces_and_Motifs_native_v5.tex` — matches 4, score 4; terms: 137.036×2, 941×1, proton×1
- `RA_Paper_II_Emergent_Matter_Interaction_Discrete_Motif_Structure_v8_tiered_restored_Apr2026.tex` — matches 4, score 4; terms: 137.036×2, 941×1, proton×1

### Top snippets

#### `d3_alpha_s_BDG.py`
```

```
```

```
```

```

#### `bdg_multicoupling.py`
```

```
```

```
```

```

#### `D1_BDG_MCMC_simulation.py`
```

```
```

```
```

```

#### `RA_Framing_Discipline.md`
```
23: - QFT quantum numbers used as labels, categories, or conservation rules: G-parity, isospin, strangeness, charm, bottomness, topness, baryon number, lepton number, weak hypercharge, weak isospin. These are SM's organization of empirical regularities. RA must derive its own categories from DAG + BDG primitives. Where RA's categories happen to agree numerically with SM labels on specific phenomena, that's downstream agreement, not validation and not a substitute for derivation.
24: - Lagrangians, path integrals, Feynman diagrams, Green's functions, Wilson coefficients, operator product expansions. None of these exist in RA.
25: - Coupling constants α_s, α_EM, α_w as theoretical objects. The fine-structure constant is a measurable number from Nature (≈ 1/137.036). RA must predict this number from primitives. SM's theoretical definition (the running coupling at some scheme-dependent scale) is not RA's problem and not RA's target.
26: - Λ_QCD (scheme-dependent theoretical parameter of QCD). RA does not input Λ_QCD and does not target it. If RA predicts a confinement scale directly from primitives, that is an RA prediction — separately whether it agrees with SM's Λ_QCD is a side question.
27: - Spontaneously broken symmetries, Goldstone theorem, Higgs mechanism, anomalies (chiral, scale, U(1)_A), instantons, theta vacuum. These are SM explanations for Nature-phenomena. RA must explain the Nature-phenomena directly; SM's explanations are not RA's business.
```
```
62: - Measured cross-sections
63: - Measured cosmological parameters (H₀, Ω_b, Ω_m, σ₈)
64: - Measured fine-structure constant (≈1/137.036)
65: - Planck units (ℏ, c, G — these are Nature-measurable, not SM-theoretical)
66: - Observed dimensionality of space (3+1, for the regime we observe)
```
```
84: **Things that need reframing (not rejection — these are still questions RA must answer, but in their Nature-facing form):**
85: 
86: - "Derive α_EM = 1/137 from BDG integers" → "Predict the measured fine-structure constant (≈1/137.036) from DAG + BDG + LLC. Comparison to SM running α(μ) is irrelevant."
87: - "Recover QCD confinement" → "Predict that certain composite motifs (what Nature shows us as hadrons) exist bound over timescales exceeding Compton times, with specific measurable masses and lifetimes."
88: - "Match SM gauge structure" → "Predict the measured pattern of interaction strengths and particle spectra." SM gauge structure is SM's summary of similar data; RA's prediction stands or falls on Nature, not on SM.
```

#### `ra_calibration.py`
```

```
```

```

## RA-PRED-002 proton mass
### Ranked candidate files
- `n_eff_mc_test.py` — matches 2, score 15; terms: proton×2
- `n_eff_alternative.py` — matches 1, score 14; terms: proton×1
- `RA_Paper_II_Matter_Forces_and_Motifs_native_v5(1).tex` — matches 10, score 10; terms: proton×9, Higgs×1
- `RA_Paper_II_Matter_Forces_and_Motifs_native_v5.tex` — matches 10, score 10; terms: proton×9, Higgs×1
- `RA_Paper_II_Emergent_Matter_Interaction_Discrete_Motif_Structure_v8_tiered_restored_Apr2026.tex` — matches 10, score 10; terms: proton×9, Higgs×1
- `ra_calibration.py` — matches 1, score 6; terms: proton×1
- `bdg_multicoupling.py` — matches 1, score 6; terms: proton×1
- `RA_Suite_Final_Preprint_Readiness_Audit_Apr23_2026.md` — matches 1, score 5; terms: proton×1
- `RA_suite_active_support_surface_master_v2.csv` — matches 1, score 2; terms: proton×1

### Top snippets

#### `n_eff_mc_test.py`
```

```
```

```

#### `n_eff_alternative.py`
```

```

#### `RA_Paper_II_Matter_Forces_and_Motifs_native_v5(1).tex`
```
100: 
101: \begin{abstract}
102: This paper develops the matter-and-interaction programme of Relational Actualism (RA) in explicit continuity with causal set theory, but not as a mere causal-set restatement. Causal set theory already supplies the locally finite causal order, sequential growth background, and discrete-action setting in which RA is formulated \cite{Bombelli1987,Sorkin1997,Rideout2000,Benincasa2010,Dowker2013}. RA adds four ingredients that are essential for turning that background into a matter programme: primitive irreversible actualization, the local ledger condition at every vertex, a realized/potentia state structure, and the use of the $d=4$ Benincasa--Dowker score as a local acceptance kernel. On that basis this paper argues that observed matter classes, interaction hierarchy, charge regularities, and matter-sector asymmetry can be approached through a finite census of renewal motifs and closure windows rather than through continuum fields, gauge representations, or symmetry breaking as primitive inputs. The paper therefore compares RA throughout with the empirical domains ordinarily organized by the Standard Model while keeping the proof path native. Its strongest present claims are structural and compiled: a finite motif census in the stable $d=4$ regime, finite closure lengths for the two minimal branching motifs, a depth-2 ledger / orientation theorem family, and the arithmetic coefficient spine used for direct Nature-facing numerical targets. Where RA reaches familiar observables by a different route --- for example, closure burden instead of boson mass as the source of finite range, or severance boundary data instead of dynamical baryogenesis as the source of matter-sector excess --- that difference is stated directly. Where RA does not yet have theorem-level closure --- most importantly in proton-mass completion, direct scattering and decay predictions, and full observational cartography from motifs to measured particle data --- the gap i
```
```
241: \paragraph{Open target.} The arithmetic result is strong, but its physical embedding into the full matter architecture is not complete until the force-range and scattering programme is closed natively.
242: 
243: \subsection{Proton-scale cascade as a native numerical programme}
244: 
245: The most ambitious numerical construction in the present paper remains the proton-scale cascade. The native idea is that a stable bound motif sustained by the minimal branching mediator should generate a multiplicative suppression from the Planck scale through repeated finite closure. In the current programme, that enters through the schematic relation
```
```
243: \subsection{Proton-scale cascade as a native numerical programme}
244: 
245: The most ambitious numerical construction in the present paper remains the proton-scale cascade. The native idea is that a stable bound motif sustained by the minimal branching mediator should generate a multiplicative suppression from the Planck scale through repeated finite closure. In the current programme, that enters through the schematic relation
246: \begin{equation}
247: \frac{m_p}{m_P} \sim \frac{\mu_p^5}{c_4},
```

#### `RA_Paper_II_Matter_Forces_and_Motifs_native_v5.tex`
```
100: 
101: \begin{abstract}
102: This paper develops the matter-and-interaction programme of Relational Actualism (RA) in explicit continuity with causal set theory, but not as a mere causal-set restatement. Causal set theory already supplies the locally finite causal order, sequential growth background, and discrete-action setting in which RA is formulated \cite{Bombelli1987,Sorkin1997,Rideout2000,Benincasa2010,Dowker2013}. RA adds four ingredients that are essential for turning that background into a matter programme: primitive irreversible actualization, the local ledger condition at every vertex, a realized/potentia state structure, and the use of the $d=4$ Benincasa--Dowker score as a local acceptance kernel. On that basis this paper argues that observed matter classes, interaction hierarchy, charge regularities, and matter-sector asymmetry can be approached through a finite census of renewal motifs and closure windows rather than through continuum fields, gauge representations, or symmetry breaking as primitive inputs. The paper therefore compares RA throughout with the empirical domains ordinarily organized by the Standard Model while keeping the proof path native. Its strongest present claims are structural and compiled: a finite motif census in the stable $d=4$ regime, finite closure lengths for the two minimal branching motifs, a depth-2 ledger / orientation theorem family, and the arithmetic coefficient spine used for direct Nature-facing numerical targets. Where RA reaches familiar observables by a different route --- for example, closure burden instead of boson mass as the source of finite range, or severance boundary data instead of dynamical baryogenesis as the source of matter-sector excess --- that difference is stated directly. Where RA does not yet have theorem-level closure --- most importantly in proton-mass completion, direct scattering and decay predictions, and full observational cartography from motifs to measured particle data --- the gap i
```
```
241: \paragraph{Open target.} The arithmetic result is strong, but its physical embedding into the full matter architecture is not complete until the force-range and scattering programme is closed natively.
242: 
243: \subsection{Proton-scale cascade as a native numerical programme}
244: 
245: The most ambitious numerical construction in the present paper remains the proton-scale cascade. The native idea is that a stable bound motif sustained by the minimal branching mediator should generate a multiplicative suppression from the Planck scale through repeated finite closure. In the current programme, that enters through the schematic relation
```
```
243: \subsection{Proton-scale cascade as a native numerical programme}
244: 
245: The most ambitious numerical construction in the present paper remains the proton-scale cascade. The native idea is that a stable bound motif sustained by the minimal branching mediator should generate a multiplicative suppression from the Planck scale through repeated finite closure. In the current programme, that enters through the schematic relation
246: \begin{equation}
247: \frac{m_p}{m_P} \sim \frac{\mu_p^5}{c_4},
```

#### `RA_Paper_II_Emergent_Matter_Interaction_Discrete_Motif_Structure_v8_tiered_restored_Apr2026.tex`
```
104: The paper addresses the same observational domain as particle physics---masses, lifetimes, interaction ranges, charge regularities, and matter-sector asymmetries---while proposing a distinct underlying mechanism based on discrete causal structure rather than continuum field dynamics. It compares RA throughout with the empirical domains ordinarily organized by the Standard Model while keeping the proof path native. Its strongest present claims are structural and compiled: a finite motif census in the stable $d=4$ regime, finite closure lengths for the two minimal branching motifs, a depth-2 ledger / orientation theorem family, and the arithmetic coefficient spine used for direct Nature-facing numerical targets. Where RA reaches familiar observables by a different route---for example, closure burden instead of boson mass as the source of finite range, or severance boundary data instead of dynamical baryogenesis as the source of matter-sector excess---that difference is stated directly.
105: 
106: Where quantitative closure is not yet achieved---including proton-mass completion, scattering predictions, decay predictions, and full mapping to observed particle spectra---the paper states explicit native routes forward within the motif-based framework.
107: \end{abstract}
108: 
```
```
306: \paragraph{Status.} Derived native / computation-verified support: \texttt{f0\_enumeration.py}. Later use of this ratio in comparison with cosmological abundance summaries is comparative cartography unless and until the full RA source law is derived natively.
307: 
308: \subsection{Proton-scale cascade as a native numerical programme}
309: 
310: The most ambitious numerical construction in the present paper remains the proton-scale cascade. The native idea is that a stable bound motif sustained by the minimal branching mediator should generate a multiplicative suppression from the Planck scale through repeated finite closure. In the current programme, that enters through the schematic relation
```
```
308: \subsection{Proton-scale cascade as a native numerical programme}
309: 
310: The most ambitious numerical construction in the present paper remains the proton-scale cascade. The native idea is that a stable bound motif sustained by the minimal branching mediator should generate a multiplicative suppression from the Planck scale through repeated finite closure. In the current programme, that enters through the schematic relation
311: \begin{equation}
312: \frac{m_p}{m_P} \sim \frac{\mu_p^5}{c_4},
```

## RA-PRED-003 scalar/Higgs
### Ranked candidate files
- `RA_Berry_Phase_Derived.md` — matches 7, score 19; terms: scalar×7
- `mu_int_derive.py` — matches 1, score 14; terms: scalar×1
- `rindler_relative_entropy.py` — matches 5, score 10; terms: scalar×5
- `bdg_multicoupling.py` — matches 4, score 9; terms: Higgs×4
- `ra_verify_heraclitus.py` — matches 3, score 8; terms: scalar×3
- `ra_desi_verify.py` — matches 3, score 8; terms: scalar×3
- `ra_structure_formation.py` — matches 2, score 7; terms: scalar×2
- `sigma_table.py` — matches 2, score 7; terms: Higgs×1, scalar×1
- `casimir_benchmark.py` — matches 2, score 7; terms: scalar×2
- `cross_dimensional_exclusion.py` — matches 1, score 6; terms: Higgs×1
- `o14_incidence_algebra.py` — matches 1, score 6; terms: scalar×1
- `D1_BDG_MCMC_simulation.py` — matches 1, score 6; terms: Higgs×1
- `RA_BDG_Simulation.py` — matches 1, score 6; terms: Higgs×1
- `RA_Framing_Discipline.md` — matches 1, score 5; terms: Higgs×1
- `RA_Paper_II_Matter_Forces_and_Motifs_native_v5(1).tex` — matches 3, score 3; terms: scalar×3

### Top snippets

#### `RA_Berry_Phase_Derived.md`
```

```
```

```
```

```

#### `mu_int_derive.py`
```

```

#### `rindler_relative_entropy.py`
```

```
```

```
```

```

#### `bdg_multicoupling.py`
```

```
```

```
```

```

#### `ra_verify_heraclitus.py`
```

```
```

```
```

```

## Provisional registry-linkage recommendations

### RA-PRED-001
Link only files that explicitly compute or derive the fine-structure inverse target. If no top candidate contains a complete IC30/Dyson derivation, keep `proof_status: ONT`, `support_status: PI`, and add candidate artifacts as unvalidated candidates rather than active support.

### RA-PRED-002
Link `n_eff_*` files if they support the `N_eff=64` or `2^28` subchain. Keep the full proton-mass prediction provisional until a complete proton-cascade artifact is identified or created.

### RA-PRED-003
Link only a file that explicitly derives the scalar/Higgs-scale target from RA-native quantities. Files merely mentioning `Higgs` or `125 GeV` should remain comparative/provisional, not active support.

## Next step
Create RAKB v0.4.6 only after manually confirming the top candidate files.
