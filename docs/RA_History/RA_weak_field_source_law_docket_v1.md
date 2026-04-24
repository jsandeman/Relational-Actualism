# RA Weak-Field Source-Law Docket v1

## Purpose

This note upgrades the weak-field audit from “benchmark consequences” to the more important question:

> **What is the canonical RA weak-field source law, exactly?**

At the moment, the current core snapshot contains **three nearby but non-identical source-law presentations**.

## The three current source-law layers

### Layer A — Paper III continuum bridge

Paper III gives the suite-level bridge:

\[
G_{\mu\nu} = 8\pi G\,P_{\mathrm{act}}[T_{\mu\nu}],\qquad \Lambda = 0.
\]

This is the most canonical high-level statement in the current suite.

### Layer B — Paper III quasi-static effective equation

Paper III then writes the weak-field quasi-static limit as

\[
\nabla^2\Phi = 4\pi G\,\rho_m + c^2\,\nabla^2(\ln\lambda),
\]

with \(\lambda(x)\) the local actualization density.

This is useful phenomenologically, but the present paper text does **not** yet give an end-to-end derivation from Layer A to Layer B.

### Layer C — script-level source split

The current scripts use a more explicit split:

- `ra_flat_rotation_curve.py`: \(G_{00} = 8\pi G\,[T_{00}^{(A)} + \Theta_{00}^{(\lambda)}]\)
- `bullet_cluster.py`: proposed unified quasi-static form \(\nabla^2\Phi = 4\pi G[\rho_A + \rho_\lambda]\)

This is physically suggestive and may well be the right intermediate language.
But it is **not yet canonicalized** in the papers.

## Audit verdict

The current suite has a **semantic bridge** and a **phenomenological weak-field equation**, but it does not yet have a single canonical derivation tying together

\[
P_{\mathrm{act}}[T_{\mu\nu}] \quad \longrightarrow \quad \rho_A,\ \rho_m,\ \lambda,\ \Theta_{00}^{(\lambda)},\ \rho_\lambda.
\]

That is the main technical reason the benchmark ladder currently splits neatly into:

- **safe, dense-regime Solar-system benchmarks**, and
- **open, mixed-regime halo / cluster lensing claims**.

## Minimal canonical statement that is safe now

The safest suite-primary source-law wording is:

> In the dense equilibration regime, the weak-field limit reduces to the standard Poisson law and hence to the ordinary Schwarzschild / PPN(β=γ=1) benchmarks. In sparse or nonequilibrated regimes, RA predicts an additional actualization-density correction. The exact covariant mapping from \(P_{\mathrm{act}}[T_{\mu\nu}]\) to the quasi-static source split used in rotation-curve and cluster-lensing analyses remains an open closure target.

This wording is strong enough to support the existing weak-field benchmarks and cautious enough to keep the open source-law problem visible.

## What must be derived to close the gap

### W1. Define the dense-regime source variable canonically
Decide whether the canonical weak-field density is:

- \(\rho_m\) (ordinary matter density),
- \(\rho_A\) (accumulated actualization depth density),
- or an explicit projector image of the 00-component of \(P_{\mathrm{act}}[T_{\mu\nu}]\).

### W2. Derive the quasi-static correction term from the covariant equation
Show explicitly how the sparse-regime correction is obtained:

- either as \(c^2\nabla^2\ln\lambda\),
- or as \(4\pi G\rho_\lambda\),
- or by proving these are the same object under a stated dictionary.

### W3. Prove the dense-regime reduction
Recover standard Poisson sourcing in the limit of local equilibration / constant actualization density.

### W4. Derive the coefficient, not only the shape
At present the halo-scale scripts still rely on calibrated or illustrative normalizations.
The next milestone is a coefficient-level derivation.

### W5. Derive the null-geodesic / Weyl-curvature reading from the same source law
This is the bridge from solar weak-field benchmarks to cluster lensing and Bullet Cluster claims.

## Implications for the benchmark programme

### Already safe
- Solar limb deflection
- Mercury perihelion
- generic thin-lens formulas in dense-equilibrium regime

### Still open
- rotation-curve normalization from first principles
- covariant cluster lensing
- Bullet Cluster quantitative closure

## Recommended wording change for Paper III §3.2

Replace the current opening sentence of the modified-Poisson discussion with a caveated source-law sentence such as:

> The weak-field quasi-static regime is expected to admit an effective source split into a dense-equilibrium matter term and an actualization-density correction term. The equation below should be read as the current effective RA ansatz for that regime; an end-to-end derivation from the covariant source \(P_{\mathrm{act}}[T_{\mu\nu}]\) remains an open closure target.

## Bottom line

The next technical target is now completely clear:

> **Canonicalize the weak-field source law before promoting halo and cluster lensing claims.**

That one move would connect the already-good Solar benchmarks to the harder astrophysical benchmarks and would materially strengthen the suite’s tractability claim.
