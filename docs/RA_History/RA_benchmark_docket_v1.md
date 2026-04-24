# RA Benchmark Docket v1

Purpose:
Translate your added desiderata into an audit-ready benchmark sequence.

Your stated target is not only "RA is conceptually viable," but:
1. RA yields QFT/GR within their applicable regimes;
2. RA makes concrete predictions for standard benchmark observables;
3. RA is a workable calculational framework, possibly more tractable than continuum methods.

## A. Domain-recovery track

### QFT-domain recovery
Primary source papers:
- Paper I: measurement / Schrödinger low-density bridge / Rindler stationarity
- Paper II: topology classes, couplings, force ranges, gauge-structure identifications

Target question:
- Does RA recover the observed finite set of QFT-organized regularities without smuggling the continuum mechanism back in?

### GR-domain recovery
Primary source paper:
- Paper III

Target question:
- Does RA account for the gravitational and cosmological phenomena usually organized by GR, and does it do so with a stable discrete-native source law?

## B. Observable benchmark track

### Already explicit in the current papers
- BMV null result
- Hubble gradient / DESI-family cosmology
- rotation curves
- Bullet Cluster
- Kinematic Coherence Bound
- spin-bath collapse timescale
- biosignature / SETI criteria

### Present in the full directory tree, but not in the uploaded core-proof bundle
- `bullet_cluster.py`
- `casimir_benchmark.py`
- broader AQFT/bridge scripts under `src/RA_AQFT`

### Not found in the currently uploaded core snapshot
- Mercury perihelion / post-Newtonian orbital benchmark
- a clear weak-field solar-system lensing benchmark
- a suite-primary, self-contained Casimir benchmark in the uploaded core files

## C. Recommended benchmark order

### 1. Casimir
Why first:
- finite geometry,
- quantum benchmark with a clean standard answer,
- good test of whether RA can be a practical calculational tool.

Deliverable:
- one canonical RA calculation,
- one benchmark against the standard Casimir result,
- one statement of what is genuinely RA-native versus translated.

### 2. Light deflection / weak-field lensing
Why second:
- direct GR-domain applicability test,
- easier to communicate than full cosmology,
- connects naturally to cluster/lensing scripts already present in the full tree.

Deliverable:
- point-mass lensing derivation,
- stated approximation regime,
- comparison with standard weak-field GR result.

### 3. Mercury perihelion
Why third:
- classic post-Newtonian benchmark,
- high rhetorical value,
- good tractability test.

Deliverable:
- one clean orbit-precession computation from the RA weak-field limit,
- explicit identification of which RA-native quantity plays the role of the effective correction term.

### 4. Rotation curves / Bullet Cluster
Why fourth:
- these are already central to Paper III,
- but they depend on the weak-field sourcing story being stable first.

### 5. QEC / KCB / spin-bath
Why fifth:
- interesting and distinctive,
- but KCB formula consistency must be repaired before it can function as a flagship benchmark.

## D. Tractability criterion

For each benchmark, the audit should ask:
- Is the calculation finite/combinatorial rather than continuum-variational?
- Are there fewer hidden regularity assumptions than in the continuum treatment?
- Can the pipeline be automated?
- Does the RA route produce the number with fewer ad hoc steps?

That is the right way to cash out your "more tractable than continuum mathematics" criterion.

## E. Immediate next benchmark recommendation

Best next benchmark to develop into suite-primary form:
1. Casimir
2. weak-field light deflection
3. Mercury perihelion

That sequence gives you:
- one quantum benchmark,
- one gravitational optics benchmark,
- one orbital mechanics benchmark,

which is a much stronger demonstration of practical usefulness than more abstract "bridge" prose alone.
