# Environmental BAO Splitting in DESI DR1: An Analysis Plan

### Testing a Prediction from Relational Actualism (RA)

**Author:** Joshua Sandeman (Salem, Oregon; independent researcher)
**Date:** April 19, 2026
**Draft status:** For discussion with DESI collaborators and void-cosmology specialists
**Associated paper:** RA Paper III §9.2 (Gravity, Cosmology, Complexity)

---

## 1. Executive summary

Relational Actualism (RA) is a discrete-substrate framework in which spacetime emerges from a growing causal DAG of actualization events, filtered by the Benincasa-Dowker-Glaser (BDG) causal-set action. The framework derives Λ = 0 structurally (the actualization projector P_act removes virtual/off-shell contributions from the stress-energy tensor), with consequences for late-time cosmology that differ in specific, testable ways from ΛCDM.

The prediction examined here is that **the observed BAO scale should differ between void and filament environments at fixed redshift** — a direct consequence of the fact that voids expand as Milne (q = 0) while matter-dominated regions expand as Einstein-de Sitter (q = +0.5) in a Λ = 0 cosmology. Homogeneous ΛCDM predicts zero environmental BAO splitting at fixed z. The RA prediction therefore provides a clean null test.

This document specifies the theoretical prediction, identifies the DESI DR1 data products required, outlines an analysis pipeline, estimates the statistical sensitivity, and flags the systematic considerations that would need to be controlled. It is intended as a concrete proposal to initiate a collaboration rather than as a final analysis.

**One directional note requires verification before proceeding.** Section 3 below works through the expected sign of the BAO splitting under the Milne/EdS mapping and arrives at a direction opposite to that stated in RA Paper III §9.2.5. This likely reflects a sign convention issue in the text; the underlying phenomenology — environmental BAO splitting at fixed z — is the core prediction and is not in dispute.

---

## 2. The RA prediction

### 2.1 The mechanism

RA derives three cosmological ingredients from its foundational commitments:

1. **Λ = 0 exactly**, because the actualization projector P_act removes virtual (off-shell) contributions from the metric source term. The QFT vacuum energy comes entirely from virtual processes (ΔS = 0); these are filtered out structurally.

2. **General relativity with Λ = 0 in the continuum limit**, via the Benincasa-Dowker 2010 theorem that the d = 4 BDG causal set action converges to the Einstein-Hilbert action under Poisson sprinkling into smooth Lorentzian manifolds.

3. **Two expansion regimes** as solutions of the Friedmann equation H² = (8πG/3)ρ with Λ = 0: empty regions (ρ → 0) give a(t) ∝ t (Milne, q = 0); matter-dominated regions give a(t) ∝ t^(2/3) (EdS, q = +0.5).

The real universe is inhomogeneous. Cosmic voids occupy ~60–70% of the volume at z = 0 (Pan et al. 2012; Cautun et al. 2014). In the RA picture, voids approach Milne behavior and filaments approach EdS behavior, producing environment-dependent expansion histories along different sightlines.

### 2.2 The BAO observable

The sound horizon r_s is set at recombination and is common to all sightlines (environmental differentiation occurs at late times only). Therefore the comoving BAO scale itself is environment-independent. What varies between environments is the *apparent* BAO scale when fiducial distances are computed from observed angles and redshifts, because the implied distance-redshift relation differs.

The standard Alcock-Paczynski decomposition parameterizes the measured BAO scale by:

- α_⊥ = [D_M(z)/r_s] / [D_M^fid(z)/r_s^fid]  (transverse)
- α_∥ = [H^fid(z) r_s^fid] / [H(z) r_s]        (radial)

where D_M = (1+z) D_A is the comoving angular diameter distance and "fid" denotes the fiducial cosmology used to compute separations from angles and redshifts (typically ΛCDM with Planck parameters).

In a two-phase RA universe (Milne voids, EdS filaments), the BAO scale measured in a void-dominated subsample differs from that in a filament-dominated subsample. ΛCDM predicts no such difference at fixed z: the BAO scale depends only on z and the global cosmology.

### 2.3 Predicted magnitude

Using H_0 = 67.4 km/s/Mpc as reference and z = 1 as a representative redshift:

| Quantity | ΛCDM (Ω_m = 0.3) | Milne (void) | EdS (filament) |
|---|---|---|---|
| D_M(z = 1) / (c/H_0) | 0.751 | 0.693 | 0.586 |
| H(z = 1) / H_0 | 1.76 | 2.00 | 2.83 |
| α_⊥ (fiducial = ΛCDM) | 1.00 | 0.923 | 0.781 |
| α_∥ (fiducial = ΛCDM) | 1.00 | 0.880 | 0.622 |

**Predicted void-vs-filament splitting at z = 1:**

- Transverse: α_⊥(void)/α_⊥(fil) = 0.923/0.781 = **1.18** (void BAO angular scale is 18% *larger* relative to filament)
- Radial: α_∥(void)/α_∥(fil) = 0.880/0.622 = **1.41** (void BAO radial scale is 41% *larger* relative to filament)
- Isotropic (D_V): α_V(void)/α_V(fil) ≈ **1.25**

These are the magnitudes of the signal the analysis is designed to detect. They are large; if the RA prediction is correct, the effect is not subtle.

**Caveat on magnitude:** The numbers above treat voids and filaments as fully Milne and fully EdS. Real voids have ρ > 0 and real filaments are not pure EdS. The realized environmental signal will be smaller than these pure-endpoint values by a factor depending on the actual density contrast and the volume fraction of each environment along representative sightlines. A realistic estimate would require modeling the density field and integrating the expansion history along ensembles of sightlines, which is part of the proposed analysis.

---

## 3. Directional verification (requires resolution)

The prediction magnitudes in Section 2.3 suggest that at fixed observed z, the BAO angular scale is **larger in voids** than in filaments, when both are measured against a ΛCDM fiducial. This arises from:

- D_M is smaller in EdS than in Milne at fixed z (0.586 vs 0.693 in c/H_0 units at z=1)
- α_⊥ = D_M^true / D_M^fid, so α_⊥ is smaller for filaments (D_M^EdS / D_M^LCDM < D_M^Milne / D_M^LCDM)
- Smaller α_⊥ means the measured transverse BAO scale is compressed more strongly in filaments than in voids

**This agrees with the RA Paper III §9.2.5 statement** that "at fixed redshift, the BAO standard ruler should appear larger inside cosmic voids."

**However, direct computation of the angular BAO scale gives the opposite result.** The observed angular BAO scale is Δθ_BAO = r_s / D_M. At z = 1:

- Δθ_Milne = 147 Mpc / (0.693 × 4448 Mpc) = 0.0477 rad
- Δθ_EdS = 147 Mpc / (0.586 × 4448 Mpc) = 0.0564 rad

This gives a *smaller* angular scale in voids and a *larger* angular scale in filaments — the opposite of the "ruler appears larger in voids" framing.

**Resolution.** Both statements are correct; they describe different quantities. The *measured angular separation* of BAO galaxy pairs is larger in filaments (they subtend a bigger angle on the sky at fixed observed z). The *inferred r_s* when one uses a common ΛCDM fiducial to convert angles to comoving separations is also larger in filaments (α_⊥ smaller → inferred scale in fiducial comoving units is larger). These go in the same direction.

The quantity that is larger in voids is α itself — the α-parameter. Since α < 1 in both environments and smaller α means more compression, voids show *less compression* than filaments, which is naturally described as "BAO scale closer to fiducial / less shifted from expectation" in voids. This is what the Paper III text appears to be gesturing at, but the phrasing "appears larger inside voids" is the opposite of what the measurement shows directly.

**Recommendation for the Paper III text:** Revise §9.2.5 T1 to:

> "At fixed redshift, the measured BAO scale should be systematically shifted from ΛCDM expectation, and the shift should be environment-dependent: filament-dominated sightlines show a larger shift (smaller α) than void-dominated sightlines. Specifically, α(void) > α(filament) for both transverse and radial BAO scales, producing a detectable environmental splitting. ΛCDM predicts α(void) = α(filament) = 1 at all redshifts."

This is the scientifically precise version and corresponds directly to measurable quantities in a DESI BAO analysis. The environmental splitting effect — which is what makes the prediction distinctive — is preserved.

---

## 4. DESI DR1 data requirements

DESI Data Release 1 (March 2025) is fully public and contains all data products required for this analysis. The specific data products are:

### 4.1 Galaxy clustering catalog

- **Primary file:** DR1 LSS catalogs
  - `https://data.desi.lbl.gov/public/dr1/survey/catalogs/dr1/LSS/iron/LSScats/v1.5/`
  - Files with `clustering` in the name are optimized for clustering analysis
  - Tracers needed: LRG (luminous red galaxies, z = 0.4–1.1), ELG (emission-line galaxies, z = 0.6–1.6), QSO (quasars, z = 0.8–2.1)

### 4.2 Randoms catalog

- Randoms cover the angular and redshift selection function
- Same directory as above, files named `{tracer}_{region}_clustering.ran.fits`

### 4.3 Void catalog

- DESI does not publish an official void catalog with DR1. Voids must be constructed from the galaxy catalog.
- Standard codes: VIDE (Sutter et al. 2015) or ZOBOV (Neyrinck 2008) based on Voronoi tessellation
- Nadathur has constructed void catalogs for previous BOSS/eBOSS data using REVOLVER; he may have or be willing to share a DR1 version

### 4.4 BAO measurement infrastructure

- Standard DESI BAO pipeline: Cullan Howlett's `Barry` code or the internal DESI BAO fitting pipeline
- Reference: DESI BAO analysis papers (DESI Collaboration 2025, DR1 BAO results)

### 4.5 Supporting data

- Survey mask (angular and redshift selection) from DR1 release
- Imaging-derived galaxy properties from the Legacy Surveys (DR9 and later)
- Reconstructed density field (optional, for void classification)

**Total data volume:** ~50–200 GB depending on which tracers and reconstruction products are pulled. Accessible from NERSC, the European mirror at PIC, or NOIRLab's Astro Data Lab.

---

## 5. Analysis pipeline

### Step 1: Void identification and classification

Input: DR1 galaxy clustering catalog (LRG primary; ELG and QSO as cross-checks)
Output: Catalog of voids with centers, effective radii, and member galaxies

- Apply Voronoi tessellation via VIDE or ZOBOV to the galaxy distribution
- Identify local density minima; grow voids using the watershed algorithm
- Compute void effective radius R_v from the volume of the Voronoi cells
- Classify galaxies as void (interior), void boundary, or filament (outside any void) based on position relative to identified voids

Split the galaxy sample into environment-defined subsamples:
- **Void subsample:** galaxies with local density δ < δ_v (typically δ_v ≈ −0.5; threshold to be tuned for signal/noise)
- **Filament subsample:** galaxies with local density δ > δ_f (typically δ_f > +1)
- **Transition subsample:** everything in between (excluded from the primary test or used for robustness checks)

### Step 2: Correlation function measurement

Input: Environment-split galaxy catalog + matched randoms
Output: ξ_void(s), ξ_fil(s) at several redshift bins

- Use Landy-Szalay estimator ξ(s) = (DD − 2DR + RR) / RR
- Compute ξ(s, μ) and decompose into Legendre multipoles ξ_0, ξ_2
- Repeat separately for void and filament subsamples
- Apply density-weighting to preserve BAO sensitivity in sparse subsamples

Redshift bins:
- Low-z: 0.4 < z < 0.6 (LRG)
- Mid-z: 0.6 < z < 1.0 (LRG + ELG)
- High-z: 1.0 < z < 1.6 (ELG + QSO)

### Step 3: BAO template fitting

Input: ξ_0, ξ_2 in each subsample and redshift bin
Output: α_⊥, α_∥ in each subsample and redshift bin

- Fit standard BAO template (linear power spectrum with damped BAO feature + smooth broadband)
- Free parameters: α_⊥, α_∥, and broadband nuisance terms
- Use Gaussian likelihood with covariance from jackknife or mock catalogs

### Step 4: Environmental splitting test

Input: {α_⊥, α_∥} in void and filament subsamples
Output: Δα_⊥ = α_⊥(void) − α_⊥(fil), Δα_∥ = α_∥(void) − α_∥(fil), with error bars

- Compute Δα and its covariance (accounting for the fact that void and filament subsamples are statistically independent but share survey systematics)
- Compare measured Δα to three hypotheses:
  - H0 (ΛCDM): Δα_⊥ = Δα_∥ = 0
  - H1 (RA with full Milne/EdS endpoints): Δα_⊥ ≈ 0.14, Δα_∥ ≈ 0.26 (at z = 1)
  - H2 (RA with realistic density contrast): Δα between 0 and the H1 values, with magnitude dependent on the effective density contrast achieved in the subsamples

- Report significance of Δα ≠ 0 (primary test) and Δα consistency with H1 or H2 (secondary test)

### Step 5: Robustness tests

- Vary the density thresholds δ_v, δ_f to confirm the signal is robust to subsample definition
- Cross-check across tracers (LRG-only vs ELG-only analyses)
- Test for residual systematics: imaging systematics, redshift-dependent completeness, fiber-assignment effects
- Compare with mock catalogs generated from ΛCDM and from an inhomogeneous Λ = 0 model (if available)

### Step 6: Interpretation

- If Δα is consistent with zero at high precision, the RA environmental-BAO prediction is ruled out at the tested effective density contrast
- If Δα is detected with a magnitude between 0 and the H1 endpoint, this constitutes positive evidence for environmental expansion-history dependence, and the magnitude constrains the effective density contrast
- If Δα exceeds the H1 magnitude, a more complex model is required

---

## 6. Statistical sensitivity

The DESI DR1 sample contains ~13.1M galaxies with high-confidence redshifts. The forecast precision on α_⊥ and α_∥ from the full DR1 sample is σ(α) ≈ 0.01–0.02 at z = 0.5–1.5 (DESI Collaboration 2025, DR1 BAO paper).

Subdividing into void and filament subsamples reduces the effective sample size. If roughly 60% of galaxies can be classified into either subsample with a meaningful density contrast, and the two subsamples are roughly equal in size, each subsample has ~3.9M galaxies, and σ(α) degrades to approximately σ(α_subsample) ≈ σ(α_full) × √(3) ≈ 0.02–0.04.

**The predicted signal magnitude (Δα_⊥ ≈ 0.14 for full Milne/EdS, or Δα_⊥ ≈ 0.05–0.10 for realistic density contrasts) is comparable to or larger than the per-subsample uncertainty.** This means DR1 has enough statistical power to detect the effect if it exists at the predicted level — provided systematics are controlled at the relevant level.

**Realistic signal magnitude.** The full Milne-vs-EdS calculation assumes complete expansion-history differentiation, which real voids do not achieve. A more realistic estimate treats each environment as a weighted combination of Milne and EdS contributions. If voids are 70% Milne and filaments are 80% EdS (rough estimate pending more careful modeling), the effective Δα reduces to ≈ 0.04–0.08 — still potentially detectable, but closer to the noise floor. A careful forecast using mock catalogs would sharpen this estimate.

DR2 (2026, expected) will approximately double the sample size, pushing σ(α_subsample) down to ~0.014–0.03. If the effect is marginal in DR1, DR2 should resolve it.

---

## 7. Systematics

Environmental BAO splitting is a cross-correlation between galaxy BAO and environmental density. Several systematics could produce spurious environmental splitting or mask a real one:

**Imaging systematics.** Depth, seeing, and stellar contamination vary across the DESI footprint. If void and filament samples are distributed differently across footprint regions, residual imaging systematics could fake a Δα signal. Mitigation: use weights from the DR1 LSS imaging-systematics procedure; test stability by restricting to the most uniform footprint regions.

**Redshift distribution differences.** Voids and filaments may have different effective n(z) distributions if galaxy types segregate with environment. This could produce BAO scale differences unrelated to expansion history. Mitigation: match n(z) between subsamples by weighting, or use narrow redshift bins to minimize the effect.

**Non-linear bias and redshift-space distortions.** Galaxies in voids and filaments have different large-scale biases and velocity statistics. At BAO scales (~150 Mpc) the effect is small but not zero. Mitigation: standard reconstruction procedures (Padmanabhan & White 2008; Burden et al. 2014) reduce non-linear BAO shifts to sub-percent; apply reconstruction independently in each subsample.

**Fiber assignment effects.** DESI fiber assignment produces small-scale incompleteness patterns that can leak into clustering statistics. Mitigation: use PIP (pairwise inverse probability) weights or the BAOtracer framework.

**Edge effects.** Void identification near survey edges is unreliable. Mitigation: restrict void catalog to voids fully contained in the observed volume.

**Void/filament definition.** Δα depends on what density threshold separates the subsamples. Mitigation: report Δα as a function of threshold; test robustness.

---

## 8. Collaboration pathway

The proposed analysis sits at the intersection of three specializations: (i) DESI BAO measurement; (ii) void identification and cosmology; (iii) the specific theoretical prediction.

The researcher best suited to the analysis proper is one with experience in void-galaxy cross-correlations in spectroscopic BAO surveys. The names most directly relevant:

- **Seshadri Nadathur (University of Portsmouth)** — author of REVOLVER void-finding code; has worked directly with DESI and eBOSS data on void-BAO cross-correlations and void-galaxy cross-correlation cosmology. Lead author on the void-galaxy BAO analysis of eBOSS DR16.

- **Nico Hamaus (LMU Munich)** — long-standing expertise in void statistics and void-matter connection; author of VIDE; has worked on void BAO with BOSS and SDSS data.

- **Nelson Padilla (Instituto de Astronomía Teórica y Experimental, Córdoba)** — void environment classification and void-galaxy physics.

- **Ashley Ross (Ohio State / CCAPP)** — DESI DR1 LSS catalog lead; natural contact for data-product methodology questions. Not a void specialist but the right person for catalog-level questions.

An efficient approach would be:

1. Complete a preliminary version of the analysis using DR1 public data, establishing methodology and reporting initial Δα bounds
2. Share the preliminary results with Nadathur or Hamaus, framing the work as a specific theoretical prediction being tested rather than as a request for data access
3. If the preliminary analysis shows either a detection or a meaningful upper limit, pursue formal collaboration for a full analysis including reconstruction, mocks, and systematics

The framing "I have a theoretical prediction that produces this specific environmental signal; here is my preliminary test against DR1 public data; I would value your feedback" is substantially stronger than a theoretical prediction alone, and likely to receive serious attention from researchers whose own work addresses exactly this question.

---

## 9. Deliverables and timeline

**Phase 1: Preliminary analysis (4–8 weeks).** Download DR1 data; implement void identification pipeline using VIDE or REVOLVER; measure correlation function in void/filament subsamples; fit BAO templates; produce Δα measurement with preliminary error bars; compile results into a short technical note.

**Phase 2: External review (2 weeks).** Share technical note with Nadathur, Hamaus, or other relevant specialists; incorporate feedback on methodology.

**Phase 3: Publication-quality analysis (8–16 weeks, collaborative).** Full analysis with reconstruction, mock covariances, systematics tests, and robustness checks; write up for submission.

**Phase 4: Publication.** Submit to PRD, JCAP, or MNRAS.

Total timeline from data access to submission: approximately 4–8 months, depending on whether the collaboration is pursued and how tightly the science is scoped.

---

## 10. References

Benincasa, D. M. T., & Dowker, F. (2010). "The scalar curvature of a causal set." *Physical Review Letters* **104**, 181301.

Burden, A., et al. (2014). "Efficient reconstruction of linear baryon acoustic oscillations in galaxy surveys." *MNRAS* **445**, 3152.

Cautun, M., et al. (2014). "Evolution of the cosmic web." *MNRAS* **441**, 2923.

DESI Collaboration (2025). "Data Release 1 of the Dark Energy Spectroscopic Instrument." arXiv:2503.14745.

DESI Collaboration (2025). "DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints."

Nadathur, S., et al. (2020). "The completed SDSS-IV extended Baryon Oscillation Spectroscopic Survey: BAO and RSD measurements from the anisotropic power spectrum of the quasar sample." *MNRAS* **498**, 2354.

Neyrinck, M. C. (2008). "ZOBOV: a parameter-free void-finding algorithm." *MNRAS* **386**, 2101.

Padmanabhan, N., & White, M. (2008). "Calibrating the baryon oscillation ruler for matter and haloes." *Physical Review D* **80**, 063508.

Pan, D. C., et al. (2012). "Cosmic voids in Sloan Digital Sky Survey Data Release 7." *MNRAS* **421**, 926.

Sandeman, J. (2026). "Relational Actualism III: Gravity, Cosmology, Complexity." Draft; §9.2.5 describes the T1 BAO-splitting prediction.

Sutter, P. M., et al. (2015). "VIDE: The Void IDentification and Examination toolkit." *Astronomy and Computing* **9**, 1.

---

**Contact:** Joshua Sandeman, Salem, Oregon. Independent researcher. Framework: Relational Actualism (4-paper suite, April 2026; archival legacy series RAQM/RAGC/RACL/etc.). Github: [to be added]. Zenodo DOIs: see RA suite for individual paper DOIs.
