# RA Results Registry v0.3 Summary

Total results: 54

## By status

- ANC: 10
- DR: 10
- ONT: 9
- STATED: 6
- DR_CV: 4
- CV: 3
- DR_PI: 3
- CC: 3
- ARCH_CC: 2
- ONT_PI: 2
- PI: 2

## By domain

- kernel: 11
- complexity: 11
- matter: 10
- arithmetic: 8
- gravity: 8
- cosmology: 3
- framing: 3

## Results

### RA-ONT-001 — Finite causal graph ontology
- Status: STATED
- Domain: kernel
- Papers: I
- Statement: The realized universe-state contains a finite actualized causal DAG G_n=(V_n,≺_n).
- Sources: RA Paper I, Axiom 1, RA Paper I, Axiom 7
- Dependencies: none
- Nature targets: discrete event structure, causal order
- Caveats: Axiomatic foundation, not derived.

### RA-ONT-002 — Irreversible actualization
- Status: STATED
- Domain: kernel
- Papers: I
- Statement: Actualization writes an irreversible vertex into the realized graph.
- Sources: RA Paper I, Axiom 2
- Dependencies: RA-ONT-001
- Nature targets: event definiteness, irreversibility
- Caveats: Primitive RA commitment.

### RA-ONT-003 — Structured potentia / adjacent possible
- Status: STATED
- Domain: kernel
- Papers: I
- Statement: At stage n, the universe-state is U_n=(G_n,Π(G_n)), with Π(G_n) the structured set of admissible one-vertex extensions.
- Sources: RA Paper I, Axiom 3
- Dependencies: RA-ONT-001
- Nature targets: open future, possible event formation
- Caveats: Requires full measure formalization.

### RA-ONT-004 — Finitary Actuality
- Status: STATED
- Domain: kernel
- Papers: I
- Statement: Every physically realized graph and physically realized count is finite; infinities appear only as idealizations.
- Sources: RA Paper I, Axiom 7
- Dependencies: RA-ONT-001
- Nature targets: finite physical counts
- Caveats: Axiomatic.

### RA-LLC-001 — Local Ledger Condition
- Status: STATED
- Domain: kernel
- Papers: I, II, III, IV
- Statement: At every actualized vertex, incoming and outgoing conserved ledger quantities balance locally.
- Sources: RA Paper I, Axiom 6, RA_GraphCore.lean
- Dependencies: RA-ONT-002
- Nature targets: local conservation regularities
- Caveats: Formal content depends on ledger object definitions.

### RA-KERNEL-001 — Four-dimensional BDG acceptance kernel
- Status: ANC
- Domain: kernel
- Papers: I
- Statement: S=1−N1+9N2−16N3+8N4 and candidate extensions are admissible only when S>0.
- Sources: RA_O14_ArithmeticCore_v1.lean, RA Paper I §BDG
- Dependencies: RA-ONT-003
- Nature targets: event admissibility
- Caveats: The positivity criterion remains a foundational postulate/selection rule.

### RA-KERNEL-002 — Kernel locality
- Status: ANC
- Domain: kernel
- Papers: I
- Statement: BDG admissibility depends only on the realized past / local interval data of a candidate.
- Sources: RA_O01_KernelLocality_v2.lean
- Dependencies: RA-KERNEL-001, RA-ONT-001
- Nature targets: local causal dynamics
- Caveats: Covariant history measure remains open.

### RA-KERNEL-003 — Finite potentia
- Status: DR
- Domain: kernel
- Papers: I
- Statement: For finite G_n, the admissible adjacent possible Π(G_n) is finite.
- Sources: RA Paper I, finite potentia proposition
- Dependencies: RA-ONT-004, RA-ONT-003, RA-KERNEL-001
- Nature targets: finite event alternatives
- Caveats: Assumes finite candidate past-set construction.

### RA-KERNEL-004 — Stochastic actualization kernel requirement
- Status: ONT
- Domain: kernel
- Papers: I
- Statement: RA requires a normalized local selection weight on admissible one-vertex extensions.
- Sources: RA Paper I, Axiom 5
- Dependencies: RA-ONT-003, RA-KERNEL-003
- Nature targets: event frequencies, repeated experiment statistics
- Caveats: Full local measure family not yet closed.

### RA-KERNEL-005 — Discrete covariance target
- Status: ONT
- Domain: kernel
- Papers: I
- Statement: The induced measure on completed histories should factor through unlabeled causal-set isomorphism classes.
- Sources: RA Paper I, CST/CSG covariance remark
- Dependencies: RA-KERNEL-004, RA-KERNEL-002
- Nature targets: label-independent physics
- Caveats: Not yet theorem-level.

### RA-ARITH-001 — BDG coefficient arithmetic spine
- Status: ANC
- Domain: arithmetic
- Papers: I
- Statement: The d=4 BDG action vector is (-1,9,-16,8) with birth term c0=1.
- Sources: RA_O14_ArithmeticCore_v1.lean
- Dependencies: RA-KERNEL-001
- Nature targets: four-dimensional event kernel
- Caveats: Geometric continuum identification remains comparative.

### RA-ARITH-002 — Second-order cancellation pattern
- Status: ANC
- Domain: arithmetic
- Papers: I
- Statement: The non-birth action sum vanishes: -1+9-16+8=0, while the full sum with c0 is 1.
- Sources: RA_O14_ArithmeticCore_v1.lean
- Dependencies: RA-ARITH-001
- Nature targets: stable kernel arithmetic
- Caveats: Interpretation as geometric closure is downstream.

### RA-D4-001 — D4U02 selectivity ceiling
- Status: CV
- Domain: arithmetic
- Papers: I, III
- Statement: The d=4 selectivity profile has first local maximum near μ*=1.019.
- Sources: d4u02_enumeration.py, D4U02_analytic_proof.md
- Dependencies: RA-KERNEL-001, RA-ARITH-001
- Nature targets: observed dimensionality, kernel scale selection
- Caveats: Analytic closure remains open.

### RA-D4-002 — D4U02 modular barrier
- Status: DR
- Domain: arithmetic
- Papers: I
- Statement: The d=4 kernel exhibits a modular barrier structure constraining self-sustained actualization.
- Sources: D4U02_analytic_proof.md
- Dependencies: RA-D4-001, RA-ARITH-002
- Nature targets: dimension selection
- Caveats: Needs final formalization.

### RA-ARITH-003 — Koide ratio identity
- Status: ANC
- Domain: arithmetic
- Papers: II
- Statement: The three-angle kval construction satisfies K=2/3 exactly.
- Sources: RA_KvalRatio.lean
- Dependencies: RA-ARITH-001
- Nature targets: charged lepton mass-ratio regularity
- Caveats: Physical embedding into rest masses remains open.

### RA-ARITH-004 — Dimensionless strong-interaction scale
- Status: DR_CV
- Domain: arithmetic
- Papers: II
- Statement: RA arithmetic gives α_RA,strong=1/sqrt(72)≈0.117851.
- Sources: d3_alpha_s_proof.py, vwyler_proof.py
- Dependencies: RA-ARITH-001
- Nature targets: dimensionless interaction-strength measurement
- Caveats: Comparison to QCD α_s is cartography, not mechanism.

### RA-ARITH-005 — Internal density scale from selectivity
- Status: DR_CV
- Domain: arithmetic
- Papers: II, III
- Statement: μ_int=exp(sqrt(4ΔS*))≈4.71 from BDG selectivity.
- Sources: mu_derivation.py, d4u02_enumeration.py
- Dependencies: RA-D4-001, RA-GRAV-001
- Nature targets: hadronic-scale regularities
- Caveats: Physical embedding remains partially interpretive.

### RA-ARITH-006 — BDG path-weight ratio
- Status: CV
- Domain: arithmetic
- Papers: II
- Statement: W_other/W_baryon≈17.32 from finite path-weight enumeration.
- Sources: f0_enumeration.py
- Dependencies: RA-ARITH-001, RA-MOTIF-002
- Nature targets: lifetime hierarchy / matter-sector weight regularity
- Caveats: Downstream uses require care.

### RA-MOTIF-001 — Native motif sector definition
- Status: STATED
- Domain: matter
- Papers: II
- Statement: Motif sectors are local realized-growth patterns classified by BDG depth counts, closure, renewal, and ledger behavior.
- Sources: RA Paper II
- Dependencies: RA-KERNEL-001, RA-LLC-001
- Nature targets: particle-like classes
- Caveats: Mapping to all observed species remains open.

### RA-MOTIF-002 — Stable motif census
- Status: ANC
- Domain: matter
- Papers: II
- Statement: The d=4 regime yields a finite census of topologically distinct stability classes under admissible extension.
- Sources: RA_D1_NativeKernel_v1.lean, RA_D1_NativeClosure_v1.lean
- Dependencies: RA-MOTIF-001, RA-D4-001
- Nature targets: number/type of particle-like motifs
- Caveats: Exact observational cartography remains open.

### RA-MOTIF-003 — Minimal closure windows
- Status: ANC
- Domain: matter
- Papers: II
- Statement: The two minimal branching motifs have finite closure lengths Lg=3 and Lq=4.
- Sources: RA_D1_NativeConfinement_v1.lean
- Dependencies: RA-MOTIF-002
- Nature targets: finite interaction ranges, confinement-like behavior
- Caveats: Terminology Lg/Lq should remain native or clearly cartographic.

### RA-MOTIF-004 — Extension census
- Status: ANC
- Domain: matter
- Papers: II
- Statement: Admissible extension classes for symmetric/asymmetric and transition-state motifs are exhaustively classified in finite cases.
- Sources: RA_D1_NativeClosure_v1.lean
- Dependencies: RA-MOTIF-003
- Nature targets: motif transition structure
- Caveats: Full spectrum mapping remains open.

### RA-MOTIF-005 — Depth-2 ledger/orientation structure
- Status: ANC
- Domain: matter
- Papers: II
- Statement: Depth-2 ledger preservation and orientation asymmetry constrain admissible motif transitions.
- Sources: RA_D1_NativeLedgerOrientation_v1.lean
- Dependencies: RA-LLC-001, RA-MOTIF-002
- Nature targets: charge/orientation regularities, matter-sector asymmetry
- Caveats: Baryon chirality interpretation requires careful cartography.

### RA-MOTIF-006 — Signed three-direction charge spectrum
- Status: DR
- Domain: matter
- Papers: II
- Statement: Three signed spatial orientations yield Q∈{−e,−2e/3,−e/3,0,e/3,2e/3,e}.
- Sources: RA_D1_NativeLedgerOrientation_v1.lean, RA Paper II
- Dependencies: RA-MOTIF-005
- Nature targets: electric charge quantization pattern
- Caveats: Complete species assignment remains open.

### RA-MOTIF-007 — Confinement as finite renewal
- Status: DR
- Domain: matter
- Papers: II
- Statement: Some bound motifs do not admit indefinitely isolated free terminal extension and persist only through finite renewal.
- Sources: RA_D1_NativeConfinement_v1.lean, RA Paper II
- Dependencies: RA-MOTIF-003, RA-MOTIF-004
- Nature targets: bound-state persistence, confinement-like observations
- Caveats: No direct scattering/hadronization predictions yet.

### RA-OPEN-001 — Full motif-to-spectrum cartography
- Status: ONT
- Domain: matter
- Papers: II
- Statement: Derive the complete observed particle/motif spectrum from RA-native motif taxonomy and closure dynamics.
- Sources: RA Paper II
- Dependencies: RA-MOTIF-002, RA-MOTIF-003, RA-MOTIF-005
- Nature targets: particle multiplicity, masses, lifetimes
- Caveats: Major open programme.

### RA-OPEN-002 — Scattering and decay predictions
- Status: ONT
- Domain: matter
- Papers: II
- Statement: Derive observable scattering cross-sections and decay/lifetime patterns from motif renewal and ledger dynamics.
- Sources: RA Paper II
- Dependencies: RA-MOTIF-007, RA-KERNEL-004
- Nature targets: cross-sections, decay rates, lifetimes
- Caveats: Requires native statistical dynamics.

### RA-ARCH-001 — Sigma-filter PDG classification
- Status: ARCH_CC
- Domain: matter
- Papers: II
- Statement: Prior sigma-filter classification used PDG/SM labels and is not active native support.
- Sources: sigma_analysis.py, sigma_table.py
- Dependencies: RA-OPEN-002
- Nature targets: lifetime classification
- Caveats: Can be restored only after RA-derived labels replace imported quantum numbers.

### RA-GRAV-001 — Kernel–Poisson divergence identity
- Status: DR_CV
- Domain: gravity
- Papers: I, III
- Statement: For the truncated BDG acceptance kernel, D_KL=-log P_acc=ΔS* and TV=1-P_acc.
- Sources: kernel_saturation.py, RA Paper I/III
- Dependencies: RA-KERNEL-001
- Nature targets: kernel selectivity, high-density behavior
- Caveats: Poisson-CSG approximation.

### RA-GRAV-002 — Asymptotic kernel saturation
- Status: DR_CV
- Domain: gravity
- Papers: I, III
- Statement: For d=4 BDG coefficients, P_acc(μ)→1 at high density with O(μ^-4) bound structure.
- Sources: kernel_saturation.py
- Dependencies: RA-GRAV-001, RA-D4-001
- Nature targets: collapse/high-density regimes
- Caveats: Physical severance onset requires further dynamics.

### RA-GRAV-003 — Causal severance
- Status: DR_PI
- Domain: gravity
- Papers: III
- Statement: A finite graph partition terminates causal contact when kernel saturation removes discriminatory event formation.
- Sources: RA Paper III, kernel_saturation.py
- Dependencies: RA-GRAV-002, RA-ONT-004
- Nature targets: black hole interiors, singular limits, causal disconnection
- Caveats: Local onset dynamics still open.

### RA-GRAV-004 — Severed-link entropy observable
- Status: DR
- Domain: gravity
- Papers: III
- Statement: RA-native severance entropy is S_RA(Σ)=|L_Σ|, the count of blocked irreducible causal links.
- Sources: RA Paper III
- Dependencies: RA-GRAV-003, RA-ONT-004
- Nature targets: black-hole entropy, horizon thermodynamics
- Caveats: Metric prefactor translation open.

### RA-GRAV-005 — Discrete boundary law
- Status: DR
- Domain: gravity
- Papers: III
- Statement: If severed out-degree is asymptotically local/stable, severance entropy scales with boundary vertex count.
- Sources: RA Paper III
- Dependencies: RA-GRAV-004
- Nature targets: area-law behavior
- Caveats: Coefficient 1/4 not derived natively.

### RA-GRAV-006 — Joint BDG/LLC macro-kernel dimension
- Status: ANC
- Domain: gravity
- Papers: III
- Statement: The joint trace/BDG/LLC macro-kernel on Fin 5 → ℝ has dimension 2.
- Sources: RA_BDG_LLC_Kernel.lean
- Dependencies: RA-LLC-001, RA-KERNEL-001
- Nature targets: macroscopic response degrees of freedom
- Caveats: Do not identify with spin-2/gravitons except as cartography.

### RA-GRAV-007 — Antichain drift local statistic
- Status: CV
- Domain: cosmology
- Papers: I, III
- Statement: BDG-filtered Poisson-CSG growth gives positive accepted antichain drift near μ=1, about +0.34.
- Sources: antichain_drift.py
- Dependencies: RA-KERNEL-001, RA-GRAV-001
- Nature targets: expansion-like graph behavior
- Caveats: Not a complete cosmological expansion law.

### RA-OPEN-003 — Coefficient-level orbital/lensing source law
- Status: ONT
- Domain: gravity
- Papers: III
- Statement: Derive exact source coefficients for orbital response and gravitational lensing from finite graph quantities.
- Sources: RA Paper III
- Dependencies: RA-GRAV-006, RA-GRAV-007
- Nature targets: rotation curves, lensing maps
- Caveats: Major open target.

### RA-OPEN-004 — Environment-sensitive expansion law
- Status: ONT
- Domain: cosmology
- Papers: III
- Statement: Derive H(z), BAO shifts, and supernova residual correlations from finite inhomogeneous graph structure.
- Sources: ra_dark_energy.py, ra_desi_verify.py, RA Paper III
- Dependencies: RA-GRAV-007
- Nature targets: redshift-distance relations, BAO, supernova residuals
- Caveats: Current scripts are exploratory phenomenology.

### RA-OPEN-005 — Low-l CMB / Axis-of-Evil severance inheritance
- Status: ONT_PI
- Domain: cosmology
- Papers: III
- Statement: Explain large-angle CMB alignments from finite inherited boundary data of a daughter graph.
- Sources: daughter_universe.py, RA Paper III
- Dependencies: RA-GRAV-003
- Nature targets: Axis of Evil, low-l CMB anomalies
- Caveats: Exploratory.

### RA-ARCH-002 — BMV null prediction
- Status: ARCH_CC
- Domain: gravity
- Papers: III
- Statement: Prior BMV-style null prediction remains comparative/provisional until reformulated in RA-native observables.
- Sources: bmv-related scripts if present
- Dependencies: RA-KERNEL-004
- Nature targets: gravity-mediated entanglement experiments
- Caveats: May be theory-artifact entanglement framing.

### RA-COMP-001 — Tier hierarchy
- Status: DR
- Domain: complexity
- Papers: IV
- Statement: Organized systems can be described by coarse-grained tiers from event-level actualization to recursively self-maintaining organizations.
- Sources: RA Paper IV
- Dependencies: RA-ONT-001, RA-LLC-001
- Nature targets: multi-scale organization
- Caveats: Faithful coarse-graining theorem open.

### RA-COMP-002 — Recursive closure
- Status: DR
- Domain: complexity
- Papers: IV
- Statement: A subsystem exhibits recursive closure when its future admissible extensions depend on boundary conditions re-inscribed by its own history.
- Sources: RA Paper IV
- Dependencies: RA-COMP-001, RA-KERNEL-002
- Nature targets: self-maintaining organization
- Caveats: Quantitative threshold open.

### RA-COMP-003 — Causal Firewall conditions
- Status: DR
- Domain: complexity
- Papers: IV
- Statement: Stable recursive organization requires redundant boundary inscription and bounded boundary turnover.
- Sources: RA Paper IV
- Dependencies: RA-COMP-002
- Nature targets: life-like persistence, agency conditions
- Caveats: Full shield theorem open.

### RA-COMP-004 — RA assembly depth
- Status: DR
- Domain: complexity
- Papers: IV
- Statement: RA assembly depth is the minimum number of causally irreducible organizational layers needed to produce a stable structure.
- Sources: RA Paper IV
- Dependencies: RA-COMP-001
- Nature targets: biological organization, assembly complexity
- Caveats: Operational estimates need computational formalization.

### RA-COMP-005 — Glycolysis assembly depth estimate
- Status: PI
- Domain: complexity
- Papers: IV
- Statement: A conservative causal coarse-graining gives A_RA(glycolysis)=3.
- Sources: RA Paper IV
- Dependencies: RA-COMP-004
- Nature targets: metabolic pathway organization
- Caveats: Illustrative; needs native computational implementation.

### RA-COMP-006 — E. coli assembly depth estimate
- Status: PI
- Domain: complexity
- Papers: IV
- Statement: Whole-cell E. coli metabolic organization estimates to A_RA≈4–6 after coarse-graining.
- Sources: RA Paper IV
- Dependencies: RA-COMP-004
- Nature targets: cellular organization
- Caveats: Partition-dependent estimate.

### RA-COMP-007 — Origin-of-life sandwich bound
- Status: DR_PI
- Domain: complexity
- Papers: IV
- Statement: Viable prebiotic organization requires minimum feedback-bearing assembly depth and environmental overwrite below persistence capacity.
- Sources: RA Paper IV
- Dependencies: RA-COMP-003, RA-COMP-004
- Nature targets: origin-of-life constraints
- Caveats: Quantitative persistence formula open.

### RA-COMP-008 — Substrate-independent biosignature criteria
- Status: DR_PI
- Domain: complexity
- Papers: IV
- Statement: Biosignature criteria include redundant boundary inscription, bounded boundary turnover, and closure-supporting density.
- Sources: RA Paper IV
- Dependencies: RA-COMP-003
- Nature targets: astrobiology, SETI, artificial life
- Caveats: Needs empirical operationalization.

### RA-OPEN-006 — Causal shield theorem
- Status: ONT
- Domain: complexity
- Papers: IV
- Statement: Prove stable recursive organization requires mediated boundary interfaces across faithful coarse-graining levels.
- Sources: RA Paper IV
- Dependencies: RA-COMP-003
- Nature targets: persistent biological organization
- Caveats: Major open theorem.

### RA-OPEN-007 — Persistence-window formula
- Status: ONT
- Domain: complexity
- Papers: IV
- Statement: Derive a closed native formula for boundary overwrite/re-inscription viability windows.
- Sources: RA Paper IV
- Dependencies: RA-COMP-003, RA-COMP-007
- Nature targets: life-like persistence under environmental forcing
- Caveats: High-priority computational/theoretical target.

### RA-OPEN-008 — Consciousness threshold problem
- Status: ONT_PI
- Domain: complexity
- Papers: IV
- Statement: Determine necessary and possibly sufficient RA conditions for phenomenal consciousness beyond recursive closure.
- Sources: RA Paper IV
- Dependencies: RA-COMP-002, RA-COMP-003, RA-COMP-004
- Nature targets: cognition, agency, consciousness
- Caveats: Exploratory; no sufficient theory claimed.

### RA-NONTARGET-001 — Born rule as non-target
- Status: CC
- Domain: framing
- Papers: I, IV
- Statement: The Born rule is not Nature itself; observed frequency regularities are the Nature-facing target.
- Sources: RA_Framing_Discipline_v3
- Dependencies: RA-KERNEL-004
- Nature targets: repeated experimental frequencies
- Caveats: Need RA-native frequency law.

### RA-OPEN-009 — RA-native frequency law
- Status: ONT
- Domain: kernel
- Papers: I
- Statement: Derive repeated-actualization frequency regularities from the stochastic actualization kernel without importing Hilbert-space Born-rule ontology.
- Sources: RA Paper I, RA_Framing_Discipline_v3
- Dependencies: RA-KERNEL-004, RA-KERNEL-005
- Nature targets: experimental outcome frequencies
- Caveats: Major foundational open target.

### RA-NONTARGET-002 — QCD running as non-mechanism
- Status: CC
- Domain: framing
- Papers: II
- Statement: QCD running couplings are comparative cartography; RA targets measured interaction-strength patterns through RA-native observables.
- Sources: RA_Framing_Discipline_v3, qcd_running_proof.py
- Dependencies: RA-ARITH-004
- Nature targets: interaction strength measurements
- Caveats: Do not use as active native proof.

### RA-NONTARGET-003 — Metric field as non-primitive
- Status: CC
- Domain: framing
- Papers: I, III
- Statement: Metric geometry is not RA's primitive substrate; RA targets observed gravitational phenomena via finite graph structure.
- Sources: RA_Framing_Discipline_v3, RA Paper III
- Dependencies: RA-ONT-001, RA-GRAV-006
- Nature targets: orbital response, lensing, horizon phenomena
- Caveats: Effective metric translations may be downstream.
