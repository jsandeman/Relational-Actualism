# Environmental BAO Splitting in DESI DR1: An Analysis Plan (v2)

### Testing a Prediction from Relational Actualism (RA)

**Author:** Joshua Sandeman (Salem, Oregon; independent researcher)
**Date:** April 19, 2026 (v2)
**Draft status:** For discussion with DESI collaborators and void-cosmology specialists
**Associated paper:** RA Paper III §9.2 (Gravity, Cosmology, Complexity)

**Changelog from v1:** Corrected Milne transverse distance (includes spatial curvature: D_M = sinh(χ), not χ). Corrected LCDM D_M(z=1). Reframed endpoint Milne/EdS numbers as diagnostic upper bounds, not DESI forecasts, and introduced an environmental suppression factor ε_env as the quantity to be constrained. Reformulated the ΛCDM null as calibration against matched mocks rather than mathematical zero. Added void-galaxy anisotropic AP as a companion observable better aligned with specialist methodology. Updated DESI release status (DR2 cosmology chains released October 2025; full DR2 LSS catalogs not yet public). Softened collaboration framing to a narrow methodological question.

---

## 1. Executive summary

Relational Actualism (RA) is a discrete-substrate framework in which spacetime emerges from a growing causal DAG of actualization events, filtered by the Benincasa-Dowker-Glaser (BDG) causal-set action. RA derives Λ = 0 structurally (the actualization projector P_act removes virtual/off-shell contributions from the stress-energy tensor), with consequences for late-time cosmology that differ in specific, testable ways from ΛCDM.

The prediction examined here is that **the observed BAO scale should differ between void-dominated and filament-dominated sightlines at fixed redshift**, a consequence of the fact that voids approach Milne expansion (q = 0) while matter-dominated regions approach Einstein–de Sitter expansion (q = +0.5) in a Λ = 0 cosmology. Homogeneous ΛCDM predicts no such environmental splitting at fixed z; matched ΛCDM mocks with the same galaxy-sample selection predict only small residual splitting from tracer bias, RSD, and selection effects. RA therefore predicts a detectable environment-dependent anisotropic dilation over and above the mock-calibrated ΛCDM null.

The prediction is cleanly formulated in Alcock-Paczynski parameters:

$$
\alpha_\perp(\text{void}) > \alpha_\perp(\text{filament}), \qquad \alpha_\parallel(\text{void}) > \alpha_\parallel(\text{filament})
$$

at fixed observed z, with the magnitude controlled by an environmental suppression factor ε_env(z) to be constrained by the measurement itself. The pure Milne/EdS endpoint provides an upper-limit diagnostic; realistic ε_env is expected to be smaller.

This document specifies the theoretical prediction, defines the observables, identifies required DESI data products, outlines an analysis pipeline, and flags key systematics. It is intended as a basis for discussion with void-cosmology specialists rather than as a complete analysis.

---

## 2. The RA prediction

### 2.1 Mechanism

RA derives three cosmological ingredients from its foundational commitments:

1. **Λ = 0 exactly**, because P_act removes virtual (off-shell) contributions from the metric source term. The QFT vacuum energy is entirely off-shell (ΔS = 0) and is filtered out structurally.

2. **General relativity with Λ = 0 in the continuum limit**, via the Benincasa–Dowker 2010 theorem that the d = 4 BDG causal set action converges to the Einstein–Hilbert action under Poisson sprinkling into smooth Lorentzian manifolds.

3. **Two expansion regimes** as solutions of H² = (8πG/3)ρ with Λ = 0: empty regions (ρ → 0) give a(t) ∝ t (Milne, q = 0); matter-dominated regions give a(t) ∝ t^(2/3) (EdS, q = +0.5).

The universe is inhomogeneous: voids occupy ~60–70% of the volume at z = 0 (Pan et al. 2012; Cautun et al. 2014). In RA, voids approach Milne behavior and filaments approach EdS, producing environment-dependent expansion histories along different sightlines. The observed BAO scale inherits this environmental dependence through the angular-diameter and Hubble distances that enter the Alcock-Paczynski parameterization.

### 2.2 Observables

The sound horizon r_s is set at recombination and is environment-independent. What varies between environments is the inferred BAO scale when fiducial distances are computed from observed angles and redshifts, because the environment-conditioned distance-redshift relation differs.

The standard AP parameters are:

$$
\alpha_\perp = \frac{D_M(z) / r_s}{D_M^{\text{fid}}(z) / r_s^{\text{fid}}}, \qquad \alpha_\parallel = \frac{H^{\text{fid}}(z) r_s^{\text{fid}}}{H(z) r_s}
$$

where D_M = (1+z) D_A is the transverse comoving distance. In a two-phase RA universe, these parameters differ between void-dominated and filament-dominated sightlines. ΛCDM predicts identical α across environments at the background level; matched-mock calibration quantifies the residual environmental signal from galaxy-sample effects alone.

### 2.3 Endpoint diagnostic (not a DESI prediction)

To establish the maximum possible signal, compute α in the pure endpoints. Using flat ΛCDM with Ω_m = 0.3 as fiducial and z = 1 as a representative redshift:

| Quantity | ΛCDM (Ω_m = 0.3) | Milne (Ω_k = 1) | EdS (Ω_m = 1) |
|---|---|---|---|
| χ(z = 1) / (c/H₀)  | — (not used) | ln 2 = 0.6931 | — (not used) |
| D_M(z = 1) / (c/H₀) | 0.7714 | sinh(ln 2) = 0.7500 | 2(1 − 1/√2) = 0.5858 |
| H(z = 1) / H₀ | √(0.3·2³ + 0.7) = 1.7607 | 2.0000 | 2^(3/2) = 2.8284 |
| α_⊥ (vs LCDM fid) | 1.0000 | 0.9722 | 0.7594 |
| α_∥ (vs LCDM fid) | 1.0000 | 0.8803 | 0.6225 |

**Corrected endpoint splitting at z = 1:**

- Transverse: Δα_⊥^endpoint = α_⊥(Milne) − α_⊥(EdS) ≈ **0.213**
- Radial: Δα_∥^endpoint = α_∥(Milne) − α_∥(EdS) ≈ **0.258**
- Ratios: α_⊥(void)/α_⊥(fil) ≈ 1.28, α_∥(void)/α_∥(fil) ≈ 1.41

**Critical note on Milne geometry.** Milne cosmology has negative spatial curvature (Ω_k = 1, not Ω_k = 0). The transverse comoving distance includes the curvature factor: D_M(z) = sinh(χ(z)) in units of c/H₀, where χ(z) = ln(1+z) is the line-of-sight comoving coordinate. A common shortcut that sets D_M = χ (valid only for flat cosmologies) would give D_M^Milne = 0.693 and systematically underestimate α_⊥^void by ~5% at z = 1.

**These endpoint numbers are diagnostic upper bounds, not DESI forecasts.** Real voids have ρ > 0 and real filaments are not pure EdS; more importantly, BAO measurements average over ~100–150 Mpc pair separations along light cones that pass through both environments. A galaxy classified as "in a void" does not define a pure-Milne light cone to the observer.

### 2.4 Forecast in environmental suppression factor

Define an environmental suppression factor ε_env(z) ∈ [0, 1] such that the observed splitting is

$$
\Delta \alpha_i^{\text{obs}}(z) = \epsilon_{\text{env}}(z) \, \Delta \alpha_i^{\text{endpoint}}(z), \qquad i \in \{\perp, \parallel\}
$$

Then the testable RA prediction becomes:

$$
\boxed{\epsilon_{\text{env}}(z) > 0 \text{ at statistical significance above matched-mock calibration}}
$$

and the numerical DESI observable is ε_env itself. ΛCDM predicts ε_env consistent with the mock-calibrated null (nominally zero, but modulated by tracer/selection effects). RA predicts ε_env > 0 with a magnitude that requires inhomogeneous light-cone modeling to forecast.

**An honest forecast for ε_env.** A rough estimate treating voids as ~70% Milne-like along the light cone and filaments as ~80% EdS-like along the light cone gives ε_env ~ 0.2–0.4, and corresponding observable splittings Δα_⊥ ~ 0.04–0.09 and Δα_∥ ~ 0.05–0.10 at z = 1. These numbers are rough and should not be treated as derived predictions pending proper inhomogeneous modeling. They are plausible-magnitude estimates against which DR1 statistical sensitivity can be compared.

---

## 3. The sign: what is larger in which environment

To avoid ambiguity, it is worth being explicit about what is larger in which environment, because the answer depends on which quantity is being reported.

**The observed angular BAO separation** Δθ_BAO = r_s / D_M is larger in filaments (smaller D_M) than in voids (larger D_M). Numerically at z = 1 with r_s = 147 Mpc and H₀ = 67.4 km/s/Mpc:

- Δθ_Milne = 0.0441 rad
- Δθ_EdS = 0.0564 rad

**The observed radial BAO redshift separation** Δz_BAO = H(z) r_s / c is likewise larger in filaments (higher H) than in voids (lower H):

- (Δz/r_s)_Milne ∝ 2.00
- (Δz/r_s)_EdS ∝ 2.83

**The fitted Alcock-Paczynski parameters** α_⊥, α_∥ are larger in voids than in filaments, because both α's are smaller when the true D_M is smaller (filament) or the true H is larger (filament):

- α_⊥(void) > α_⊥(filament)
- α_∥(void) > α_∥(filament)

**The invariant, unambiguous RA prediction** is the last one: environment-dependent splitting of the fitted AP parameters, with voids giving larger α than filaments. This is the correct phrasing for specialist discussion.

**Recommended revision to RA Paper III §9.2.5 T1:**

> At fixed redshift, RA predicts an environment-dependent AP dilation: sightlines dominated by voids should yield larger fitted α_⊥ and α_∥ than sightlines dominated by filaments, after calibration against matched ΛCDM mocks. The endpoint Milne/EdS diagnostic gives Δα_⊥^endpoint ≈ 0.21 and Δα_∥^endpoint ≈ 0.26 at z = 1; the realized observable signal is Δα_i^obs = ε_env Δα_i^endpoint with ε_env < 1 and determined by the effective environmental contrast along DESI sightlines. ΛCDM predicts ε_env = 0 at the background level.

---

## 4. DESI data status (updated)

DESI Data Release 1 (March 2025) is fully public and contains all LSS catalogs required for this analysis:

- **DR1 LSS clustering catalogs:** `https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/` (Ross et al. 2025 documents the construction)
- **DR1 mocks** (AbacusSummit and EZmocks for covariance estimation): `https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/mocks`
- **Tracers:** LRG (z = 0.4–1.1), ELG (z = 0.6–1.6), QSO (z = 0.8–2.1), BGS (z < 0.4)
- **European mirror** at PIC; also accessible via NERSC and NOIRLab Astro Data Lab

**DESI DR2 status (as of April 2026):**

- DR2 BAO cosmological results released March 19, 2025
- DR2 cosmology MCMC chains and posterior products released October 2025: `https://www.desi.lbl.gov/2025/10/06/`
- **Full DR2 LSS catalogs / void-ready products are not equivalently public yet.** The DESI data release page states that DR2 cosmology chains are a standalone early release; the full DR2 spectra and LSS catalogs follow later.

**Implication:** DR1 is the right starting point for an external preliminary analysis. DR2 BAO results should be referenced for context, and the DR2 cosmology chains can be used for mock comparisons, but the LSS-level void-splitting analysis proposed here must use DR1.

**Void catalog.** DESI does not publish an official void catalog with DR1. Voids must be constructed from the galaxy catalog using VIDE (Sutter et al. 2015), ZOBOV (Neyrinck 2008), or REVOLVER (Nadathur). Nadathur and collaborators have constructed DR1 void catalogs for their own work; informal sharing or cross-validation may be possible.

---

## 5. Two observables

A specialist audience will expect not one but two environment-conditioned BAO observables. Both should be part of the analysis plan.

### 5.1 Primary observable: environment-split galaxy-galaxy BAO

- Split the DR1 galaxy sample into void-dominated and filament-dominated subsamples based on local density
- Measure ξ(s, μ) via Landy-Szalay in each subsample; decompose into multipoles ξ₀, ξ₂
- Fit standard BAO template to extract α_⊥^sub, α_∥^sub
- Report Δα_⊥ = α_⊥(void) − α_⊥(fil), Δα_∥ = α_∥(void) − α_∥(fil), with error bars from jackknife or mocks
- Calibrate the ΛCDM null against matched ΛCDM mocks run through the same environment-split pipeline
- Quote ε_env as the ratio (Δα^obs − Δα^mock) / Δα^endpoint

This is the direct RA-T1 observable.

### 5.2 Companion observable: void-galaxy anisotropic cross-correlation

- Compute ξ(s_⊥, s_∥) between void centers and galaxies
- Extract the AP parameter F_AP(z) = D_A(z) H(z) / c from the anisotropy of the void-galaxy correlation (standard method; Hamaus et al. 2016, Nadathur et al. 2020)
- In ΛCDM, F_AP(z) traces the background cosmology. In RA, F_AP measured around void centers should differ from F_AP measured around filaments or from the global value
- This observable is the natural target for void-cosmology specialists and complements the galaxy-galaxy BAO approach

Nadathur's group has used void-galaxy AP to constrain D_A H / c from eBOSS at the 1% level at z = 0.57. A similar analysis on DR1, split by void vs filament environments of the void centers, would probe the same RA prediction through a different statistical channel.

### 5.3 Joint analysis

The two observables probe the same underlying environment-conditioned geometry with different galaxy-selection and reconstruction dependencies. Consistency between them strengthens any detection; disagreement diagnoses systematics.

---

## 6. Statistical sensitivity

DR1 contains 18.7M unique redshifts. Forecast precision on α from the full DR1 sample is σ(α) ≈ 0.01–0.02 at z = 0.5–1.5 (DESI DR1 BAO paper).

Environment-splitting reduces effective sample size. If 60% of galaxies can be classified with meaningful density contrast and the void/filament subsamples are comparable in size, σ(α_sub) degrades to ~0.02–0.04 per subsample. The covariance between void and filament α measurements is reduced but nonzero (shared systematics).

**Detection threshold.** For a 3σ detection of the RA prediction, we need Δα^obs / σ(Δα) > 3. With σ(Δα) ~ 0.04 (√2 combination of two subsample errors), the required observable splitting is Δα^obs > 0.12. This is at the edge of the rough ε_env estimate (Δα ~ 0.04–0.09), suggesting that DR1 alone will likely produce either a marginal detection, a tight upper limit on ε_env, or a null result, but not a high-significance detection unless the actual ε_env sits at the top of the plausible range.

DR2 doubles the sample size; DR3+ will be larger. If DR1 gives a marginal or null result, DR2 LSS (once released) should sharpen the answer substantially.

---

## 7. Systematics

Environmental BAO splitting is a cross-correlation between galaxy BAO and environmental density. The following systematics can produce or mask signals:

- **Imaging systematics.** Depth, seeing, stellar contamination vary across the footprint. Mitigation: use the DR1 LSS imaging-systematics weights; test stability across footprint regions.
- **Redshift distribution n(z) differences.** Voids and filaments may have different effective n(z) if galaxy types segregate with environment. Mitigation: match n(z) by weighting, or use narrow redshift bins.
- **Tracer bias and redshift-space distortions.** Different for void and filament galaxies. Mitigation: apply reconstruction independently in each subsample (Padmanabhan & White 2008; Burden et al. 2014).
- **Fiber assignment.** DESI fiber assignment produces small-scale incompleteness patterns. Mitigation: PIP weights (Lasker et al. 2025) or BAOtracer.
- **Edge effects in void identification.** Restrict to voids fully contained in the observed volume.
- **Threshold dependence.** Δα depends on the density threshold separating subsamples. Mitigation: report Δα as a function of threshold.
- **Residual ΛCDM signal in matched mocks.** The calibrated null requires that mocks reproduce DESI selection, RSD, and reconstruction faithfully. Use the AbacusSummit mocks released with DR1.

The ΛCDM null is not "Δα = 0" but "Δα consistent with matched-mock expectation." This is the correct statistical test.

---

## 8. Collaboration pathway

A concrete analysis, even a preliminary one, is a much stronger opening than a theoretical claim. However, the most efficient first step is a narrow methodological question rather than a full collaboration request.

**Suggested approach:**

1. **Draft a short (2-page) observable-definition memo** based on §2–3 of this document, with emphasis on the invariant AP-parameter formulation and the ε_env parameterization
2. **Conduct a small-scale pilot** using public DR1 LSS catalogs — possibly even restricted to a single tracer (LRG) at a single redshift bin — to establish the pipeline and produce an initial Δα estimate
3. **Approach a specialist with a narrow question** rather than a theoretical pitch. A framing such as: *"I am testing a prediction that produces environment-conditioned AP splitting. Before investing in a full analysis pipeline, I would value feedback on whether my environment split and BAO estimator would survive standard void-catalog and mock-catalog scrutiny."*

This is lower-friction than asking a specialist to evaluate a new theoretical framework; methodology feedback is something they give often and comfortably. The theoretical context can come later.

**Candidate specialists:**

- **Seshadri Nadathur (University of Portsmouth)** — author of REVOLVER; lead on eBOSS void-galaxy BAO and AP analyses
- **Nico Hamaus (LMU Munich)** — void statistics; author of VIDE
- **Nelson Padilla (IATE Córdoba)** — void environment classification
- **Ashley Ross (Ohio State / CCAPP)** — DESI DR1 LSS catalog lead; right contact for catalog-level methodology
- **Slađana Radinović** and **Paula Souza Cruz** (both associated with DESI void-galaxy work) — potentially appropriate for specific data-access questions

---

## 9. References

Benincasa, D. M. T., & Dowker, F. (2010). *PRL* **104**, 181301.

Burden, A., et al. (2014). *MNRAS* **445**, 3152.

Cautun, M., et al. (2014). *MNRAS* **441**, 2923.

DESI Collaboration (2025). "Data Release 1 of the Dark Energy Spectroscopic Instrument." arXiv:2503.14745.

DESI Collaboration (2025). "DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints."

Hamaus, N., et al. (2016). *PRL* **117**, 091302. (Anisotropic void-galaxy correlation for AP.)

Lasker, J., et al. (2025). "AltMTL: Producing PIP weights for DESI DR1." (DESI technical paper.)

Nadathur, S., et al. (2020). *MNRAS* **499**, 4140. (Void-galaxy BAO/RSD from eBOSS DR16.)

Neyrinck, M. C. (2008). *MNRAS* **386**, 2101.

Padmanabhan, N., & White, M. (2008). *PRD* **80**, 063508.

Pan, D. C., et al. (2012). *MNRAS* **421**, 926.

Ross, A. J., et al. (2025). "Construction of the DESI DR1 LSS catalogs."

Sandeman, J. (2026). "Relational Actualism III: Gravity, Cosmology, Complexity." Draft; §9.2.5 specifies the T1 environmental BAO splitting prediction.

Sutter, P. M., et al. (2015). *Astronomy and Computing* **9**, 1.

---

**Contact:** Joshua Sandeman, Salem, Oregon. Independent researcher. Framework: Relational Actualism (4-paper canonical suite, April 2026).
