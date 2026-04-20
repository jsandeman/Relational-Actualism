# DESI T1 Forecast: Corrected Memo (v3)

### Replacing the earlier "ε_env ≈ 0.3" forecast with honest bracketing

**Author:** Joshua Sandeman
**Date:** April 19, 2026 (v3)
**Supersedes:** `Epsilon_Env_Forecast_Memo.md` (v1)
**Companion files:** `t1_forecast_deliverables.py` (computation script), `DESI_T1_Analysis_Plan_v2.md` (the analysis plan, still current)

**Why v3.** The v1 memo contained a subtle but real technical inconsistency: the two-phase light-cone model averages 1/H along the path to get the radial comoving coordinate χ, but my tabulation mixed flat treatment (D_M = χ) for intermediate f_v with curved treatment (D_M = sinh χ) at f_v = 1. This produced a falsely clean "slope ≈ 0.22" that blended two distinct models. The corrected presentation here treats the two models separately and shows that they bracket the plausible range. I have also walked back the "two estimates converge on ε_env ≈ 0.3" framing, which overstated the independence and confidence of the agreement.

---

## 1. What we know cleanly

The endpoint Milne-vs-EdS diagnostic is rigorous; it depends only on standard FRW arithmetic. Using flat ΛCDM with Ω_m = 0.3 as fiducial, the α values across DESI's redshift range (from the deliverables script):

| z | α_⊥^Milne | α_⊥^EdS | Δα_⊥^endpoint | α_∥^Milne | α_∥^EdS | Δα_∥^endpoint |
|---|---|---|---|---|---|---|
| 0.2 | 0.961 | 0.914 | 0.048 | 0.920 | 0.840 | 0.080 |
| 0.5 | — | — | 0.113 | — | — | 0.160 |
| 0.8 | 0.956 | 0.782 | 0.174 | 0.870 | 0.648 | 0.221 |
| 1.0 | 0.972 | 0.759 | **0.213** | 0.880 | 0.622 | **0.258** |
| 1.2 | 0.993 | 0.742 | 0.252 | 0.897 | 0.605 | 0.292 |
| 1.6 | 1.044 | 0.716 | 0.328 | 0.940 | 0.583 | 0.357 |

These are the theoretical upper bounds on the environmental AP splitting at each redshift. The Milne calculation uses the correct transverse distance D_M = sinh(χ) = sinh(ln(1+z)) including the Ω_k = 1 spatial curvature; the EdS calculation uses D_M = 2(1 − 1/√(1+z)) as a flat FRW result.

**The sign in the endpoint diagnostic is unambiguous:** α_⊥^void > α_⊥^filament because D_M^Milne > D_M^EdS at fixed z (Milne-like regions produce larger transverse comoving distances than EdS-like regions), and α_∥^void > α_∥^filament because H_Milne(z) < H_EdS(z) at fixed z > 0 (and α_∥ = H^fid/H^env is the reciprocal). Physically this corresponds to Milne regions having expanded over more of cosmic history at a rate that is faster than EdS at early times but slower than EdS at low z; the net effect at the observed redshift is that the BAO ruler in a void region ends up further away (larger D_M) and is observed with a smaller local H.

**The magnitude of the endpoint grows with redshift**, from Δα ~ 0.05 at z = 0.2 to Δα ~ 0.33 at z = 1.6. Higher-redshift DESI samples (ELG, QSO) in principle give larger signal if ε_env does not fall off with z.

---

## 2. What we do not know cleanly: the mapping from f_v to Δα

The environmental suppression factor ε_env is the ratio Δα^obs / Δα^endpoint. To forecast ε_env from a theoretical model, we need to know how the realized α depends on the void/filament mixture along BAO-relevant paths. I have not done this rigorously, and the RA framework does not yet contain the machinery to do so. What follows is two toy models that bracket the plausible range.

### 2.1 Model A: flat path-average

Treat the mixed void/filament path as if it were flat (ignore Milne's curvature because most of the path is not in a pure Milne region anyway):

$$D_M^{\text{mix, A}}(z; f_v) = f_v \cdot \chi_{\text{Milne}}(z) + (1 - f_v) \cdot D_M^{\text{EdS}}(z)$$

where χ_Milne(z) = ln(1+z) is the line-of-sight comoving coordinate (not the curved transverse distance). This model gives smaller endpoint splittings:

- Δα_⊥^A(z=1) = 0.139
- Δα_⊥^A(z=1.6) = 0.185

### 2.2 Model B: curved interpolation

Linearly interpolate between the curved Milne D_M and the flat EdS D_M:

$$D_M^{\text{mix, B}}(z; f_v) = f_v \cdot \sinh(\chi_{\text{Milne}}(z)) + (1 - f_v) \cdot D_M^{\text{EdS}}(z)$$

This model gives the larger endpoint splittings matching §1:

- Δα_⊥^B(z=1) = 0.213
- Δα_⊥^B(z=1.6) = 0.328

### 2.3 Which is right?

Neither. Both are toys. They bracket two simple curvature treatments; the true DESI statistic must be determined by mock-calibrated light-cone or inhomogeneous-distance modeling, which is not guaranteed to lie between the two bracketing values — curvature, lensing, shear, environment selection, void compensation walls, and reconstruction effects can push an inferred statistic outside the naive interpolation bracket. Model A tends to understate the signal because it ignores the curvature contribution in genuinely void-dominated portions of the path; Model B tends to overstate it because it treats every mixed path as if both curvatures are fully present. The rigorous answer requires the Wiltshire/timescape machinery, N-body ray tracing, or direct inhomogeneous-GR calculation.

**For an order-of-magnitude sensitivity target, take the range Δα_⊥^endpoint ∈ [0.14, 0.21] at z = 1.** The radial endpoint Δα_∥ is less curvature-convention-dependent because it depends only on H at the measurement redshift, not on path-integrated curvature; its endpoint value is 0.258 at z = 1 regardless of toy model. However, the observed radial BAO/AP statistic still requires mock calibration — redshift-space distortions, reconstruction, pair selection, and environment-conditioned velocities all enter the inferred α_∥.

### 2.4 The actual suppression factor

In both toy models, Δα is approximately linear in Δf_v over the [0, 1] range. To leading order:

- Δα_⊥^obs ≈ slope × Δf_v, with slope = 0.14 (Model A) to 0.21 (Model B) at z = 1
- Δα_∥^obs ≈ 0.26 × Δf_v at z = 1 (curvature-independent)

Δf_v is the difference in path-averaged void volume fraction between void-selected and filament-selected DESI sightlines. This is an empirically specifiable quantity, but what value it takes for DESI environment cuts at the BAO scale is not theoretically known. Rough estimates from the galaxy-density-contrast literature suggest Δf_v in the range 0.1–0.5 for reasonable void/filament classifications, but I am not putting a specific number on it — this is the quantity the pilot analysis would constrain.

**Revised honest forecast.** Rather than quoting a specific ε_env prediction, I state:

$$\text{Exploratory sensitivity range: } 0.1 \lesssim \varepsilon_{\text{env}} \lesssim 0.5$$

This is the range scanned for sensitivity studies, not a derived RA prediction range. The purpose of the scan is to determine whether DESI DR1/DR2 could constrain the effect across the range of theoretically conceivable values. ε_env is the parameter to be measured, not forecast.

---

## 3. Sensitivity matrix

Using Model B (curved interpolation) endpoint values as the less conservative bracket, and treating Model A values as giving ~65% of these:

### 3.1 Transverse (α_⊥)

Signal-to-noise S/N = Δα^obs / σ at assumed ε_env values:

| ε_env | z=0.5 Δα_⊥^obs | σ=0.04 S/N | σ=0.06 S/N | z=1.0 Δα_⊥^obs | σ=0.04 S/N | σ=0.06 S/N | z=1.5 Δα_⊥^obs | σ=0.04 S/N | σ=0.06 S/N |
|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.011 | 0.3 | 0.2 | 0.021 | 0.5 | 0.4 | 0.031 | 0.8 | 0.5 |
| 0.2 | 0.023 | 0.6 | 0.4 | 0.043 | 1.1 | 0.7 | 0.062 | 1.5 | 1.0 |
| 0.3 | 0.034 | 0.8 | 0.6 | 0.064 | 1.6 | 1.1 | 0.093 | 2.3 | 1.5 |
| 0.5 | 0.056 | 1.4 | 0.9 | 0.106 | 2.7 | 1.8 | 0.155 | 3.9 | 2.6 |
| 1.0 | 0.113 | 2.8 | 1.9 | 0.213 | 5.3 | 3.5 | 0.309 | 7.7 | 5.2 |

### 3.2 Radial (α_∥)

| ε_env | z=0.5 Δα_∥^obs | σ=0.04 S/N | σ=0.06 S/N | z=1.0 Δα_∥^obs | σ=0.04 S/N | σ=0.06 S/N | z=1.5 Δα_∥^obs | σ=0.04 S/N | σ=0.06 S/N |
|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.016 | 0.4 | 0.3 | 0.026 | 0.6 | 0.4 | 0.034 | 0.9 | 0.6 |
| 0.2 | 0.032 | 0.8 | 0.5 | 0.052 | 1.3 | 0.9 | 0.068 | 1.7 | 1.1 |
| 0.3 | 0.048 | 1.2 | 0.8 | 0.077 | 1.9 | 1.3 | 0.102 | 2.6 | 1.7 |
| 0.5 | 0.080 | 2.0 | 1.3 | 0.129 | 3.2 | 2.1 | 0.171 | 4.3 | 2.8 |
| 1.0 | 0.160 | 4.0 | 2.7 | 0.258 | 6.4 | 4.3 | 0.341 | 8.5 | 5.7 |

### 3.3 What this says about DR1

Assume σ(Δα) ≈ 0.04 per subsample (optimistic; ChatGPT correctly notes that environment-splitting introduces extra covariances that may inflate this to 0.06 or higher).

**At the low end of the plausible ε_env range (ε_env = 0.1)**, Δα^obs is below 0.03 at all redshifts and in both directions. S/N per subsample per observable is < 1. Combined transverse + radial across three redshift bins could push this to ~2, but that's below reliable detection.

**At the baseline guess (ε_env = 0.3)**, Δα^obs is in the range 0.03–0.10 across redshifts. Per-subsample S/N is in the range 0.5–2.5. Combined S/N across transverse + radial at the best redshift (z ≈ 1.0) is ~2–3.

**At the high end (ε_env = 0.5)**, Δα^obs is 0.06–0.17. Per-subsample S/N reaches 2–4. Combined S/N could reach 4–5, which would be a real detection.

**Honest expectation for DR1:**

- If ε_env is at the low end: DR1 produces an upper limit consistent with both ΛCDM and the lower end of the RA range. Scientifically useful but not decisive.
- If ε_env is at the middle: DR1 produces a marginal detection (1-3σ). Suggestive but requires DR2 confirmation.
- If ε_env is at the high end: DR1 produces a clean detection (3-5σ). The result would warrant immediate follow-up.

**DR1 is a pilot-scale instrument for this test, not a definitive one.** The analysis should be designed to produce a defensible upper limit or marginal detection, and DR2 (when fully released) should be the definitive stage.

---

## 4. What ChatGPT got right that I walked back

ChatGPT's audit identified four overstatements in the v1 memo that I want to flag explicitly so the revised framing is clear:

1. **"Two independent estimates converge on ε_env ≈ 0.3"** was wrong. The two-phase model and the linear-theory density-contrast estimate used related physical intuitions with different arithmetic; their rough agreement is not independent evidence. The revised framing treats ε_env as a measurable parameter with plausible range 0.1–0.5, not as a specific forecast.

2. **"Combined detection significance at DR1 is ~2.5σ"** was too optimistic. The figure assumed optimal combination across observables and an idealized σ(Δα), neither of which automatically holds for a novel environment-split statistic. The revised sensitivity matrix shows the honest range of outcomes as a function of ε_env.

3. **"RA is mechanically similar to timescape"** was too strong. Timescape has a specific quasilocal gravitational-energy structure that RA does not share. The correct framing is that both motivate Λ = 0 inhomogeneous interpretations of apparent acceleration, and the methodological overlap is in computing environment-conditioned observables without FLRW assumptions. Wiltshire is the right person to approach, but with a precise question rather than a claim of framework identity.

4. **"AP is the best observable"** may not be true. ChatGPT points out that recent local-void BAO analyses have found that the volume-averaged distance D_V is sometimes more discriminative than the AP splitting. This is a real concern; the analysis plan should allow D_V as an additional or alternative observable and not commit exclusively to α_⊥, α_∥.

---

## 5. The scientifically honest statement for collaborators

> In the limiting Milne-vs-EdS endpoint diagnostic, RA predicts a positive environment-conditioned AP splitting: α_⊥^void > α_⊥^filament and α_∥^void > α_∥^filament. At z = 1, relative to a flat Ω_m = 0.3 ΛCDM fiducial, the curved-endpoint diagnostic gives Δα_⊥ ≈ 0.213 and Δα_∥ ≈ 0.258. A flat path-average transverse toy gives Δα_⊥ ≈ 0.139, illustrating the dependence on curvature treatment. These are not direct DESI predictions. The observed signal should be written Δα_i^obs = ε_env Δα_i^endpoint, with ε_env to be constrained by environment-split DESI measurements and matched ΛCDM mocks.
>
> The RA contribution to the broader Λ = 0 inhomogeneous-cosmology program is the structural derivation of Λ = 0 from actualization physics (P_act vacuum suppression), which shifts the explanatory question from "why Λ is so small" to "what is the precise observational signature of inhomogeneous backreaction in a universe whose Λ vanishes by construction." The rigorous calculation of ε_env requires inhomogeneous-GR distance machinery not yet developed within RA; toy estimates make values in the range 0.1–0.5 conceivable for sensitivity-study purposes, but no specific value is predicted. DR1 is suitable for a pilot analysis and mock-calibrated upper limit; DR2 or the void-galaxy anisotropic cross-correlation statistic (Nadathur-style) may be required for decisive tests.

This is the framing I would take to Wiltshire, Nadathur, Hamaus, or any other specialist. It is precise, honest about what is and isn't known, and makes a falsifiable prediction without overpromising the magnitude.

---

## 6. Revised next steps

1. **Accept the corrected sensitivity framing.** ε_env is the parameter to be measured; the scan range 0.1–0.5 is an exploratory sensitivity target, not a theoretical window.

2. **Contact Wiltshire with a narrow methodological question.** Suggested phrasing:

> Professor Wiltshire — I am working on testing a Λ = 0 inhomogeneous-cosmology prediction of environment-dependent BAO AP splitting against DESI DR1 public data. The prediction is conceptually distinct from timescape at the foundational level (it comes from a discrete causal-graph substrate rather than from quasilocal gravitational energy), but both frameworks motivate Λ = 0 inhomogeneous interpretations of apparent acceleration and the observational question is methodologically similar. Before I commit to a full analysis pipeline, I would like to ask whether (a) your existing timescape BAO calculation machinery could be adapted to produce environment-conditioned forecasts for alternative Λ = 0 inhomogeneous models, and (b) whether you would be interested in a brief discussion of how the timescape BAO predictions compare to the endpoint Milne-vs-EdS diagnostic at the DESI redshifts.

3. **Contact Nadathur with a narrow methodological question about the void-galaxy AP observable.** Suggested phrasing:

> Dr. Nadathur — I am planning to test a theoretical prediction of environment-conditioned BAO dilation against DESI DR1. The prediction is that void-selected and filament-selected sightlines should show α(void) > α(filament) with a magnitude suppressed from the pure Milne-vs-EdS endpoint by an environmental factor ε_env to be determined empirically. Your REVOLVER + eBOSS work on void-galaxy anisotropic correlations suggests that the void-galaxy AP observable F_AP(z) might be a more sensitive channel than galaxy-galaxy BAO in environment-split subsamples. Would you be open to a brief discussion of which observable is most appropriate for a first pilot analysis at DR1 sensitivity?

These are the two highest-leverage contacts, asking narrow methodological questions that don't require the collaborator to engage with RA as a framework.

4. **Do the pilot analysis.** With corrected sensitivity expectations in hand, the DR1 analysis is still worth doing; it produces either a marginal detection or a useful upper limit, and it establishes the pipeline for DR2.

---

## 7. Files

- `DESI_T1_Analysis_Plan_v2.md` — the analysis plan itself, still current
- `t1_forecast_deliverables_v2.py` — Python script that produces `endpoint_ap_table.csv`, `toy_model_bracket_table.csv`, `sensitivity_matrix.csv`, and `endpoint_splitting_plot.png`. Uses NumPy only (no SciPy dependency). Runs `verify_numerics()` at the top to confirm closed-form agreement before producing outputs.
- `Epsilon_Env_Forecast_Memo.md` (v1) — **superseded by this document**; retained for record
- `t1_forecast_deliverables.py` — superseded by v2

The honest computational state: Deliverable 1 (endpoint calculator) is clean, verified against closed forms, and written to `endpoint_ap_table.csv`. Deliverable 2 (two competing toy models) is a bracketing diagnostic, not a derivation, and is written to `toy_model_bracket_table.csv`. Deliverable 3 (sensitivity matrix) shows what DR1 can and can't do across the exploratory ε_env range and is written to `sensitivity_matrix.csv`. The plot `endpoint_splitting_plot.png` visualizes the Δα endpoint values with the toy-model bracket and reference sensitivity lines. The rigorous forecast remains a specific open problem, best addressed through the Wiltshire contact or N-body ray tracing.
