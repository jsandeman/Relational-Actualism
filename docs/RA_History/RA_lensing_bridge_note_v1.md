# RA Lensing Bridge Note v1

## Purpose

This note separates three different things that are easy to conflate:

1. **Solar weak-field light deflection** in the dense recovered Einstein sector;
2. **generic thin-lens consequences** of that recovered sector;
3. **cluster lensing / Bullet Cluster** claims that require the still-open RA source-law closure.

## Safe lensing ladder

### L1. Solar-limb light deflection
Already benchmarked from the recovered Schwarzschild weak-field sector:

- solar-limb deflection = **1.751243 arcsec**

This is the cleanest lensing-type benchmark presently available.

### L2. Generic thin-lens formulas in the dense-equilibrium regime
If the recovered Einstein sector is accepted in ordinary dense weak-field environments, then the standard thin-lens formulas follow as translation-level consequences:

\[
\hat\alpha(b)=\frac{4GM}{bc^2},
\qquad
\beta = \theta - \frac{D_{ls}}{D_s}\hat\alpha(\theta),
\qquad
\theta_E = \sqrt{\frac{4GM}{c^2}\frac{D_{ls}}{D_l D_s}}.
\]

These are not yet direct discrete derivations, but they are legitimate **benchmark consequences** of the Paper III bridge.

### L3. Mixed-regime / accumulated-history lensing
Once the source depends on accumulated actualization depth rather than only instantaneous matter density, the cluster-lensing problem becomes harder.

That is where the open source-law gap appears.

## Illustrative strong-lensing benchmark

For a **generic point-mass lens** with

- \(M = 10^{11} M_\odot\),
- \(D_l = 1\,\mathrm{Gpc}\),
- \(D_s = 2\,\mathrm{Gpc}\),

the standard dense-regime thin-lens translation gives:

- Einstein angle: **0.638126 arcsec**
- Einstein radius in the lens plane: **3.093723 kpc**

For a source offset \(\beta = 0.5\,\theta_E\), the image positions are:

- \(\theta_+ = 1.280776\,\theta_E\)
- \(\theta_- = -0.780776\,\theta_E\)

with total magnification

- \(\mu_{\mathrm{tot}} = 2.182821\)

This is a useful calculational witness because it shows the recovered sector is not only qualitative; it immediately yields standard lensing observables.

## Where the open hard wall begins

The Bullet Cluster argument is not controlled by the same safe ladder.

Why not?

Because the current RA explanation requires a stronger claim:

- the metric source relevant for lensing follows **accumulated causal depth** (or a canonically related \(\rho_A\)),
- not merely current matter placement or current local \(\lambda\).

That is exactly the step the current `bullet_cluster.py` script itself labels as the hard wall.

## Recommended suite language

### Safe now
> In dense-equilibrium weak-field environments, RA inherits the standard null-geodesic and thin-lens benchmarks through the recovered Einstein sector. Solar light deflection and ordinary point-lens formulas are therefore benchmark consequences of the bridge.

### Keep open
> Cluster lensing in mixed sparse/historical-source regimes requires a canonical derivation of the RA weak-field source law and remains an open computational target.

## Bottom line

The lensing programme is now best organized as:

1. solar deflection,
2. generic thin-lens translation benchmark,
3. canonical source-law closure,
4. cluster lensing,
5. Bullet Cluster.

That ordering is both honest and strategically efficient.
