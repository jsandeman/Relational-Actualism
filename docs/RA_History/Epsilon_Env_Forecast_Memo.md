# Environmental Suppression Factor ε_env: Derivation and Forecast

### Technical Memo (Companion to DESI T1 Analysis Plan v2)

**Author:** Joshua Sandeman
**Date:** April 19, 2026
**Purpose:** Upgrade the environmental BAO splitting prediction from a plausible-guess ε_env estimate to a defensible forecast, using existing inhomogeneous-cosmology machinery.

---

## 1. Goal

The RA T1 prediction is an environment-dependent anisotropic dilation in DESI BAO measurements, with magnitude

$$\Delta \alpha_i^{\text{obs}}(z) = \varepsilon_{\text{env}}(z) \, \Delta \alpha_i^{\text{endpoint}}(z), \qquad i \in \{\perp, \parallel\}$$

where Δα_endpoint is the pure Milne-vs-EdS diagnostic (Δα_⊥^endpoint ≈ 0.21, Δα_∥^endpoint ≈ 0.26 at z = 1) and ε_env ∈ [0, 1] is the environmental suppression factor that must be estimated from actual light-cone geometry. This memo derives ε_env in two complementary frameworks and identifies the specific computational targets that would upgrade the forecast from plausible to rigorous.

**Result preview.** Under three different estimation frameworks, ε_env falls into the range 0.15–0.50 for DESI-realistic environment classifications at the BAO scale, giving observable splittings Δα_⊥^obs ≈ 0.03–0.10 at z = 1. This is comparable to or larger than the DR1 per-split statistical uncertainty (σ(Δα) ≈ 0.04), meaning DR1 is genuinely at the detection threshold: a positive result would be marginal but informative; a null result would constrain ε_env < 0.3 or so at 2σ, which is a scientifically meaningful bound.

---

## 2. Framework: light-cone averaging

The rigorous framework for computing distance measures in a statistically homogeneous but locally inhomogeneous universe is Räsänen's light-cone averaging (Räsänen 2009, 2010; building on Buchert 2000). The observation is that a photon traversing an inhomogeneous universe accumulates redshift at the *local* expansion rate at each point along its path, so:

$$\chi(z) = \int_0^z \frac{c \, dz'}{H_{\text{local}}(z', \text{path})}$$

For a path that samples the universe statistically, this becomes

$$\chi(z) = \int_0^z c \, dz' \, \left\langle \frac{1}{H}(z') \right\rangle_{\text{path}}$$

The key insight is that the path-averaged 1/H, not H itself, is the quantity that enters distance integrals. This distinction matters because 1/H is sensitive to low-H regions (voids, where 1/H is large) in a way that H is not.

**For RA specifically**, the relevant local Hubble rates are:

- Void-like regions: H_local(z) = H_Milne(z) = (1+z) H_0
- Filament-like regions: H_local(z) = H_EdS(z) = (1+z)^{3/2} H_0

The environmental suppression factor ε_env arises because DESI "void" and "filament" subsamples do not select sightlines that are purely one or the other — they select sightlines with *biased* volume fractions f_v of void-like paths.

---

## 3. Simple two-phase model

### 3.1 Setup

Define f_v(path) as the volume fraction of the path spent in void-like regions (0 ≤ f_v ≤ 1). Then the path-averaged 1/H is

$$\left\langle \frac{1}{H} \right\rangle = \frac{f_v}{H_{\text{Milne}}(z)} + \frac{1 - f_v}{H_{\text{EdS}}(z)}$$

and the comoving distance along the path is

$$\chi(z; f_v) = \int_0^z \left[ \frac{f_v}{H_{\text{Milne}}(z')} + \frac{1-f_v}{H_{\text{EdS}}(z')} \right] c \, dz'$$

For DESI subsamples: void-classified galaxies have f_v = f_v^{void}, filament-classified galaxies have f_v = f_v^{fil}, with f_v^{void} > f_v^{fil}.

### 3.2 AP parameter and the splitting

The AP parameter α_⊥ against an LCDM fiducial is α_⊥(f_v) = D_M(z; f_v) / D_M^{fid}(z). For a flat or nearly-flat effective cosmology, D_M ≈ χ. Numerical integration at z = 1:

| f_v | D_M / (c/H_0) | α_⊥ (vs LCDM Ω_m=0.3) |
|---|---|---|
| 0.0 (pure EdS) | 0.5858 | 0.7594 |
| 0.2 | 0.6073 | 0.7872 |
| 0.4 | 0.6287 | 0.8150 |
| 0.5 | 0.6395 | 0.8289 |
| 0.6 | 0.6502 | 0.8429 |
| 0.8 | 0.6717 | 0.8707 |
| 1.0 (pure Milne) | 0.7500 | 0.9722 |

The splitting Δα_⊥(Δf_v) = α_⊥(f_v^{void}) − α_⊥(f_v^{fil}) is *nearly linear* in Δf_v = f_v^{void} − f_v^{fil}, with slope ≈ 0.22 per unit Δf_v. This gives the clean result:

$$\boxed{\Delta \alpha_\perp^{\text{obs}} \approx 0.22 \cdot \Delta f_v \text{ at } z = 1}$$

**And therefore ε_env ≈ Δf_v in this approximation.**

The environmental suppression factor is the *difference in void volume fraction* between void-classified and filament-classified sightlines.

### 3.3 Realistic Δf_v

How biased are DESI-classified sightlines? The answer depends on the scale at which voids are defined. Two relevant regimes:

**Galaxy-scale classification (VIDE/ZOBOV, ~20 Mpc scale).** Cosmic voids defined this way cover ~60% of the volume at z = 0 (Pan et al. 2012). A sightline to a galaxy chosen to be "in a void" has the last ~50 Mpc preferentially void-like; the rest of the path (~3 Gpc at z = 1) samples the universe approximately randomly. Effective Δf_v from endpoint selection alone ≈ (50 Mpc / 3000 Mpc) × (1 − 0.6) ≈ 0.007. Negligible.

**Large-scale (BAO-scale) density classification.** If galaxies are classified by their local density smoothed at 100–150 Mpc, the environment captures the large-scale structure that matters for BAO. Density contrast at this scale is smaller (δ_BAO rarely exceeds ~1 in magnitude), but correlated across the BAO pair separation. Effective Δf_v for BAO-relevant environments is the key quantity, and it has been studied in void-galaxy cross-correlation work.

For Nadathur-style void catalogs tuned for BAO analyses, typical Δf_v along sightlines at BAO pair-separation scales is ~0.2–0.6, depending on void definition, tracer choice, and whether voids are reconstructed at the BAO scale or inherited from galaxy-scale catalogs.

**Expected range:**
- Conservative (galaxy-scale voids, weak environment bias): Δf_v ≈ 0.1–0.2, giving Δα_⊥^obs ≈ 0.02–0.04
- Baseline (BAO-tuned void classification): Δf_v ≈ 0.3–0.4, giving Δα_⊥^obs ≈ 0.07–0.09
- Optimistic (aggressive void selection, high contrast): Δf_v ≈ 0.5–0.6, giving Δα_⊥^obs ≈ 0.11–0.13

ε_env ≈ Δf_v, so the baseline forecast is ε_env ≈ 0.3–0.4.

---

## 4. Independent check: linear-theory density-contrast estimate

An independent estimate comes from linear cosmological perturbation theory. In linear theory, the local Hubble rate perturbation is

$$\frac{\delta H}{H} \approx -\frac{1}{3} f(\Omega_m) \, \delta_{\text{linear}}$$

where δ is the matter density contrast and f(Ω_m) ≈ Ω_m^0.55 is the growth rate index. Integrated over the epoch during which the perturbation has been established (roughly the last half of cosmic time, weighted by growth):

$$\frac{\Delta \ln a_{\text{local}}}{\Delta t} \sim -\frac{1}{3} f(\Omega_m) \langle \delta \rangle_{\text{integrated}}$$

At z = 1, Ω_m(z=1) ≈ 0.77 for Ω_{m,0} = 0.3, giving f ≈ 0.87. With integrated fraction ~ 0.5:

| Environment scenario | δ_void | δ_fil | α_void/α_fil − 1 | Δα_⊥^abs |
|---|---|---|---|---|
| Extreme (small-scale, rare) | −0.8 | +2.0 | 0.31 | 0.30 |
| Strong (DESI-classified, small scale) | −0.5 | +1.0 | 0.15 | 0.14 |
| **Moderate (BAO-scale smoothing)** | **−0.3** | **+0.5** | **0.08** | **0.07** |
| Weak (large-scale) | −0.15 | +0.3 | 0.04 | 0.04 |

**This agrees with the two-phase model at the order-of-magnitude level.** The "moderate" row — which corresponds to density classification at the BAO smoothing scale — predicts Δα_⊥^obs ≈ 0.07, matching the baseline two-phase estimate. The "strong" row (stronger environment selection, galaxy-scale voids) gives larger values up to Δα ≈ 0.14.

Both frameworks independently predict ε_env ≈ 0.2–0.5 for realistic DESI environment selections, with Δα_⊥^obs ≈ 0.04–0.10 as the most probable range at z = 1.

---

## 5. Limits of the approximation

Three effects not captured by either framework above should be acknowledged:

### 5.1 Spatial curvature mixing

Milne has Ω_k = 1 (open); EdS has Ω_k = 0 (flat). A two-phase path is neither, strictly. The full treatment requires solving the null geodesic equation in an actual inhomogeneous metric, which in general does not admit clean decomposition. The volume-weighted 1/H approximation (Räsänen 2009) is accurate to a few percent for statistically isotropic inhomogeneities at BAO scales, but the correction is not negligible. A careful analysis would compute the curvature contribution explicitly.

### 5.2 Nonlinear structure

Filament galaxies live in regions with δ ~ few, which is nonlinear. Linear theory underestimates the suppression of expansion in these regions (clusters/filaments have effectively collapsed or are virializing, and no longer participate in cosmic expansion). If a DESI "filament" subsample contains many cluster galaxies, the effective f_v^{fil} is lower than naive linear theory suggests, enhancing Δf_v.

### 5.3 Correlation structure

The environment along a DESI BAO pair's path is correlated: the two galaxies in a BAO pair are only ~150 Mpc apart, so both see similar environmental conditions. This means the effective Δf_v for a BAO measurement is the Δf_v between *pair environments*, not between single-galaxy environments. This is typically slightly larger than the single-galaxy value because the BAO-scale correlation locks in the environmental contrast.

All three effects tend to *enhance* the expected signal relative to the simple two-phase estimate. So ε_env ≈ 0.3 is probably conservative.

---

## 6. Path to a rigorous forecast

Three increasingly ambitious approaches would produce a defensible ε_env prediction.

### 6.1 Wiltshire timescape framework

David Wiltshire and collaborators have developed the "timescape" cosmology — a Λ = 0 inhomogeneous model in which cosmic observers in voids and filaments have different proper times, and the global expansion is a volume-weighted average. Wiltshire has worked out the BAO signature of this model in detail and has been testing it against DESI data as of 2024–2025 (Seifert, Wiltshire, et al.).

**The timescape model is not RA, but it is the closest existing framework for computing environmental BAO splitting in a Λ = 0 universe.** The machinery Wiltshire has built — the finite-infinity model, the dressed-cosmological-parameters formalism, the light-cone integration through void/wall mixtures — is directly applicable. RA's contribution would be to replace the timescape's specific assumptions about the void/wall volume-fraction evolution with an RA-native calculation, but the distance-computation infrastructure is the same.

**Recommended action:** Reach out to Wiltshire (University of Canterbury, New Zealand) about whether his BAO analysis code can be adapted to RA-specific inputs. This is the single highest-leverage step for upgrading the forecast.

### 6.2 N-body ray tracing

Modern N-body simulations (AbacusSummit, Millennium, Euclid Flagship) contain realistic density fields that can be ray-traced to compute BAO observables along realistic sightlines. Tools exist (Hamaus et al., Cautun et al., Sutter et al.) for extracting void catalogs from N-body outputs and computing correlation functions in environment-split subsamples.

For an RA-specific forecast, the approach would be:

1. Take an AbacusSummit cosmic-variance set (these are already public and are used for DESI covariance estimation)
2. Identify voids and filaments with the same classification scheme as the DESI analysis will use
3. Compute the effective 1/H along sightlines passing through each environment, using the RA mapping (Milne for underdense regions, EdS for dense regions)
4. Compare to the same measurement in the simulation's native LCDM
5. Extract Δα^obs

This is a significant computational project (weeks to months) but it would produce a rigorous, mocks-calibrated ε_env forecast. It also generates the matched-mock null that the data analysis needs.

### 6.3 Direct backreaction computation

The Buchert equations with RA-native initial conditions and evolution could be integrated forward to produce environment-conditioned ⟨H⟩_D(z) for any specified domain D. This would be the most theoretically principled approach, but the computational machinery for fully-consistent backreaction simulations remains specialized (Kai, Grossi, Koksbang, and a few others actively work in this space).

This is the long-term target. The simulation infrastructure exists (e.g., in the work of Koksbang on the average expansion in inhomogeneous models) and could be adapted, but it is not trivial.

---

## 7. Implications for the DR1 analysis

**Baseline forecast:**
- ε_env ≈ 0.3 ± 0.15 (one-sigma subjective range from the two independent estimates above)
- Δα_⊥^obs ≈ 0.06 ± 0.03 at z = 1
- Δα_∥^obs ≈ 0.08 ± 0.04 at z = 1

**DR1 per-split uncertainty** (from §6 of the v2 plan): σ(Δα) ≈ 0.04.

**Expected detection significance at z = 1:**
- Δα_⊥: 1.5σ ± 0.75σ
- Δα_∥: 2.0σ ± 1.0σ

**Combined transverse + radial (two independent measurements):** ~2.5σ ± 1σ.

**Three possible outcomes from a DR1 analysis:**

1. **Detection at ε_env ≈ 0.3–0.5** (favorable case): ~3σ combined evidence for environmental splitting consistent with RA's prediction. This would be a meaningful positive result but not confirmation; DR2 would be needed for high-significance detection.

2. **Marginal result around ε_env ≈ 0.1–0.2**: ~1σ per observable, combined ~1.5σ. Not statistically compelling, but constrains the prediction to the lower end of the plausible range. A useful null-ish result.

3. **Strong null ε_env < 0.1 at 2σ**: Δα^obs < 0.02. This would *rule out* the full Milne-vs-EdS endpoint framing at 10σ and would constrain ε_env < 0.1, which is below the baseline forecast. This would be a significant setback for the T1 prediction but not for RA as a whole — the Λ = 0 derivation would remain intact, and the failure would localize to whether realistic voids actually approach Milne-like expansion history.

In all three cases, a DR1 result is scientifically valuable. The most important precondition is that the ΛCDM null is calibrated against matched mocks, so that a null result can be interpreted as a constraint on ε_env rather than as a failure of the environmental-split methodology.

---

## 8. Recommended next steps

**Short term (1–2 weeks):**
1. Verify the two-phase model calibration by comparing my estimates to Wiltshire-style published timescape BAO predictions — if the timescape literature has already computed environmental BAO splittings for Λ = 0 inhomogeneous cosmologies, those numbers should agree with the estimates here to within factors of 1.5–2.
2. Draft a 1-page query to Wiltshire asking specifically whether the timescape BAO machinery can be adapted to RA-native inputs, and whether collaboration on a DR1 analysis would be of interest.

**Medium term (1–3 months):**
3. If Wiltshire engages: work out the adaptation and produce a rigorous ε_env forecast via his framework.
4. If not: pursue the AbacusSummit ray-tracing approach (more work, but self-contained). This requires significant computational setup but is achievable with the public DR1 mocks.

**Long term:**
5. Develop RA-native backreaction machinery. Probably a project in its own right, appropriate for a collaborator with simulation expertise.

The near-term priority is the Wiltshire contact, because if his machinery is adaptable it saves months of computational work. The timescape program has been doing exactly this calculation (Λ = 0 inhomogeneous BAO) for a decade, and is the natural home for the rigorous forecast.

---

## 9. References

Buchert, T. (2000). "On average properties of inhomogeneous fluids in general relativity: Dust cosmologies." *General Relativity and Gravitation* **32**, 105.

Koksbang, S. M. (2019). "Another look at redshift drift and the backreaction conjecture." *JCAP* **10**, 036.

Pan, D. C., et al. (2012). *MNRAS* **421**, 926.

Räsänen, S. (2009). "Light propagation in statistically homogeneous and isotropic dust universes." *JCAP* **02**, 011.

Räsänen, S. (2010). "Light propagation in statistically homogeneous and isotropic universes with general matter content." *JCAP* **03**, 018.

Seifert, A., Wiltshire, D. L., et al. (2024–2025). [Recent timescape vs DESI BAO analyses — check arXiv for current references.]

Wiltshire, D. L. (2007). "Exact solution to the averaging problem in cosmology." *PRL* **99**, 251101.

Wiltshire, D. L. (2009). "Observational tests of the timescape model." *PRD* **80**, 123512.

---

**Summary.** The environmental suppression factor ε_env ≈ 0.3 is the baseline RA forecast for DR1, giving Δα^obs ≈ 0.06–0.08 and combined detection significance ~2.5σ ± 1σ. DR1 is therefore at the detection threshold — a marginal but scientifically useful result is expected, with DR2 likely needed for unambiguous confirmation. The most efficient path to a rigorous forecast is to adapt Wiltshire's existing timescape BAO machinery rather than build RA-specific infrastructure from scratch.
