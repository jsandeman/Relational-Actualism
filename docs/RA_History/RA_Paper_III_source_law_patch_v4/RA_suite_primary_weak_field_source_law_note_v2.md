# RA Suite-Primary Weak-Field Source-Law Note v2

## Purpose

This note supplies the missing suite-primary dictionary linking the covariant gravity bridge of Paper III to the benchmark scripts and to the weak-field / lensing ladder.

The goal is **not** to overstate closure. It is to make one thing canonical:

> what the current suite is justified in saying about the weak-field source law, right now.

## The canonical chain

Paper III already fixes the covariant bridge:

\[
G_{\mu\nu}=8\pi G\,P_{\mathrm{act}}[T_{\mu\nu}],\qquad \Lambda=0.
\]

That is the top-level continuum translation claim.

The weak-field programme should then be organized into **three regimes**.

### Regime A — dense equilibrium

In dense baryonic environments, the safest quasi-static reading is:

\[
\rho_A := \frac{P_{\mathrm{act}}[T_{00}]}{c^2},
\qquad
\rho_A \approx \rho_m
\]

up to a small tracking error controlled by local equilibration.

In this regime the correction term is suppressed and the standard Poisson law is recovered:

\[
\nabla^2\Phi \approx 4\pi G\,\rho_A \approx 4\pi G\,\rho_m.
\]

This is the regime supporting:
- Solar light deflection
- Mercury perihelion
- dense-regime thin-lens formulas

These are therefore **benchmark consequences of the recovered Einstein sector**.

### Regime B — sparse / boundary correction regime

Paper III currently writes the effective weak-field equation as

\[
\nabla^2\Phi = 4\pi G\,\rho_m + c^2\nabla^2(\ln\lambda).
\]

The script layer often rewrites the second term as an effective source contribution.

The safest canonical notation is therefore:

\[
\nabla^2\Phi = 4\pi G\,\rho_A + \mathcal{D}_\lambda[\lambda],
\]

where:
- \(\rho_A\) is the dense-equilibrium actualized source,
- \(\mathcal{D}_\lambda[\lambda]\) is the **current effective actualization-gradient correction operator**.

At the current suite stage, the paper-level ansatz is
\(\mathcal{D}_\lambda[\lambda] = c^2\nabla^2\ln\lambda\),
but the coefficient-level and operator-level closure is **not yet canonicalized**.

This regime is the current location of the rotation-curve mechanism.

### Regime C — historical / mixed-regime lensing

The Bullet Cluster discussion introduces a different object:

\[
A_{\mathrm{RA}}(x)
\]

or accumulated causal depth / historical source.

This is not yet canonically identified with either:
- the dense source \(\rho_A\), or
- the local correction operator \(\mathcal{D}_\lambda[\lambda]\).

So the safe current reading is:

> dense-regime lensing is already supported by the recovered Einstein sector, but mixed-regime cluster lensing remains downstream of an open covariant source-law closure.

## The source-law dictionary

| Symbol / phrase | Safe canonical reading now | Status |
| --- | --- | --- |
| \(P_{\mathrm{act}}[T_{\mu\nu}]\) | covariant actualized stress source | DR bridge claim |
| \(\rho_A\) | quasi-static effective density read from \(P_{\mathrm{act}}[T_{00}]\) | bridge-level definition |
| \(\rho_m\) | ordinary matter density in the continuum description | standard continuum variable |
| \(\lambda(x)\) | local actualization density (smoothed \(\mu\)) | paper-level variable |
| \(\mathcal{D}_\lambda[\lambda]\) | effective correction from actualization-density gradients | AR / not fully canonicalized |
| \(A_{\mathrm{RA}}(x)\) | accumulated causal depth / historical source used in lensing discussion | AR / covariant map still open |

## The new hard-wall check: operator / sign ambiguity

Paper III presently combines two statements:

1. the quasi-static correction term is \(+\,c^2\nabla^2(\ln\lambda)\),
2. a halo with \(\lambda(r)\propto r^{-2}\) yields the desired extra attraction.

Those two statements are **not automatically compatible**.

For a standard radial Laplacian in spatial dimension \(d\), if

\[
\lambda(r)\propto r^{-p},
\qquad
\ln\lambda(r)=\text{const}-p\ln r,
\]

then

\[
\nabla_d^2 \ln\lambda
=
p(2-d)\,r^{-2}.
\]

So for the profile \(p=2\):

- in \(d=1\): \(+2/r^2\)
- in \(d=2\): \(0\)
- in \(d=3\): \(-2/r^2\)

This means the current paper-level statement
“\(\lambda(r)\propto r^{-2}\) and \(\nabla^2\ln\lambda>0\)”
is only compatible with a one-dimensional second-derivative reading, not with the ordinary 2D cylindrical or 3D spherical radial Laplacians.

## Audit consequence

This is a real load-bearing issue, but it is also very fixable.

The correct immediate move is:

- do **not** insist on the specific \(\lambda(r)\propto r^{-2}\) profile yet,
- present the rotation-curve mechanism as an **effective-source statement**,
- leave the exact operator/sign/geometry closure as open.

That preserves the conceptual claim while avoiding a likely sign mistake.

## Canonical regime ladder for the suite

### Safe to present now
- \(G_{\mu\nu}=8\pi G\,P_{\mathrm{act}}[T_{\mu\nu}]\), \(\Lambda=0\)
- dense-regime recovery of ordinary weak-field GR
- Solar deflection
- Mercury perihelion
- ordinary thin-lens translation benchmarks

### Present as effective ansatz, not closure
- halo-source correction term
- rotation-curve phenomenology from actualization gradients

### Keep explicitly open
- coefficient-level halo closure
- covariant relation between \(P_{\mathrm{act}}[T_{\mu\nu}]\), \(\rho_A\), \(\lambda\), and \(A_{\mathrm{RA}}\)
- cluster lensing
- Bullet Cluster quantitative closure

## Recommended paper-level wording

### Replace
“the gravitational potential satisfies ... where \(\lambda(r)\propto r^{-2}\) at large radii”

### With
“the weak-field quasi-static regime is modeled by an effective source split into a dense-equilibrium term and an actualization-gradient correction term; the exact operator-level closure for the halo regime remains open.”

## Bottom line

The current suite can already say something strong and clean:

> RA recovers the dense weak-field Einstein sector and already supports standard Solar-system and thin-lens benchmarks there.

What it should **not** yet say is that the halo/cluster source law is coefficient-level closed.

That is the next real derivation target.
