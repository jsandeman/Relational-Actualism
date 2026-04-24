# RA Domain-Recovery and Benchmark Program v1

## Strategic aim

You stated two related goals:

1. show that RA yields the successful effective descriptions of QFT and GR inside their domains of applicability, and
2. show that RA is a practical calculational framework for concrete observables.

For the audit, these should be separated but linked.

- **Domain-recovery track:** show that RA reproduces the relevant effective equations / observables where the continuum theories are known to work.
- **Benchmark track:** compute named observables from RA primitives with explicit assumptions and numerical outputs.
- **Tractability track:** show that the RA computation is finite, modular, and in some cases simpler than the continuum machinery it replaces.

## Working principle

The public-facing success criterion should be:

> RA starts from DAG + BDG + actualization primitives, derives a finite or discrete prediction, and then matches measured phenomena. Agreement with GR/QFT inside their validated regimes is a demanding downstream benchmark.

This preserves RA primacy while still meeting the scientific bar you want.

## Priority benchmark ladder

### 1. Casimir effect

**Why first:**
- already has a runnable witness,
- compact calculation,
- directly supports the vacuum-source story,
- strongest immediate case for “RA is a useful calculational tool.”

**Deliverable:** short benchmark note + polished script.

### 2. Weak-field light deflection

**Why next:**
- the cleanest solar-system / lensing bridge,
- conceptually simpler than Bullet Cluster,
- directly tests whether the RA sourcing law yields the right deflection angle.

**Deliverable:** derive the RA weak-field metric or effective deflection law, then compute Solar deflection at the limb.

### 3. Mercury perihelion precession

**Why third:**
- iconic GR-domain benchmark,
- strong evidence that RA is not merely qualitatively gravitational,
- high rhetorical value for reviewers.

**Deliverable:** derive the post-Newtonian correction from the RA weak-field law and compute arcseconds/century.

### 4. Rotation curves

**Why fourth:**
- already present in Paper III and script form,
- but current script is calibrated rather than first-principles.

**Deliverable:** replace the calibration parameter by a sourced RA quantity.

### 5. Weak/strong lensing at cluster scale

**Why after Mercury and solar deflection:**
- observationally powerful,
- but derivationally harder,
- depends on the same sourcing law used in the simpler solar benchmark.

**Deliverable:** only after the weak-field source law is canonicalized.

### 6. Bullet Cluster

**Why later:**
- still open even in the current script package,
- should not be flagship until the source mapping is fully derived.

## Benchmark specification template

Every benchmark note should have the same six-part structure.

### A. Observable
What measurable quantity is being computed?

### B. RA input data
What comes from RA primitives, and what comes from measurement?

### C. Derivation chain
Exact symbolic chain from RA assumptions to the benchmark formula.

### D. Numerical evaluation
A script that reproduces the reported number or plot.

### E. Comparison
Observed value, residual, and epistemic tier.

### F. Open scope
Exactly what remains unproved, conditional, or imported.

## What counts as tractability evidence

To support the stronger thesis that RA may be more tractable than continuum physics, each benchmark should explicitly display:

- finite combinatorial inputs,
- small number of primitive assumptions,
- compact symbolic derivation,
- minimal parameter count,
- direct numerical evaluation without heavy perturbative machinery where possible.

The comparison is not “RA replaces all continuum methods today.”
The comparison is “RA yields a compact derivation of the same measured quantity from a smaller primitive base.”

## Immediate deliverables to build next

### Benchmark Note 1
**Casimir effect from actualization-projected stress-energy**

### Benchmark Note 2
**Weak-field light deflection from the RA sourcing law**

### Benchmark Note 3
**Mercury perihelion precession from the same weak-field correction**

## Formal dependencies to close in parallel

### For the QFT-domain side
- AQFT modular-flow closure for the Unruh / stationarity layer,
- explicit status separation between benchmark-level success and full theorem closure.

### For the GR-domain side
- canonical weak-field source law,
- canonical derivation chain from RA discrete source to effective metric / deflection law,
- one benchmark note for solar deflection and one for Mercury before moving to cluster-scale lensing.

## Recommended public sequencing

1. Paper patches for primacy and coherence,
2. Casimir benchmark note,
3. weak-field lensing note,
4. Mercury note,
5. update Paper III with benchmark cross-references,
6. only then elevate Bullet Cluster / large-scale lensing.

## Bottom line

The clean path is now:

**patch coherence first, then benchmark visibly, then broaden.**

That order best supports your stated aim of showing both viability and calculational usefulness.
