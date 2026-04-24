# RA-Native Development Protocol v2

## 1. Binding rule
Every active RA derivation must run from **DAG + BDG + LLC + Nature-measurements**.
Anything else is either a deferred bridge or a non-native dependency.

## 2. Four-gate test for every new claim
1. **Mechanism gate** — Does the mechanism use only vertices, directed edges, BDG depths, the BDG score, actualization, acyclicity, severance, and LLC?
2. **Target gate** — Is the target a measurable Nature-quantity (mass, lifetime, cross-section, orbit, lensing map, biosignature, etc.) rather than a theory-object (gauge group, running coupling, Page curve, Landauer bound, etc.)?
3. **Input gate** — Are all inputs either RA primitives or direct Nature-measurements? If a script imports `alpha_s`, `Lambda_QCD`, `SU(3)`, `FLRW`, `B3LYP`, or similar, it fails.
4. **Category gate** — Are the labels internal to RA? If categories are inherited from PDG / QFT / GR and merely renamed, the claim is not yet native.

If a claim fails any gate, it must be tagged as one of:
- `mixed-rewrite`
- `deferred-bridge`
- `non-native`

## 3. Development order (mandatory)
### Ring 0 — ontology and graph primitives
- DAG acyclicity
- local finiteness
- actualization events
- links, chains, antichains
- LLC

### Ring 1 — closure mathematics on the graph
- BDG integers / O14 uniqueness
- acceptance kernel and saturation laws
- amplitude locality / causal invariance
- motif stability and confinement windows
- cut / severance theorems

### Ring 2 — native motif census
- topology classes
- winding-based conserved quantities
- extension enumeration
- exit/disruption accessibility
- assembly depth / recursive closure

### Ring 3 — Nature-facing observables
Derive only measured quantities directly from Rings 0–2:
- masses
- lifetimes
- decay branching patterns
- radii
- cosmological anomaly amplitudes
- biosignature thresholds
- lensing/orbit data

### Ring 4 — optional cartography (deferred)
Only after a native result is stable may one ask whether it resembles QFT/GR/SM summaries. This is archival cartography, not part of the derivation.

## 4. What a native Lean theorem should look like
A theorem belongs on the active path when:
- its statement is written in terms of RA-native objects;
- it does not assume continuum/QFT axioms;
- it closes without executable `sorry` or ad hoc axioms;
- its physical reading is a direct consequence, not the theorem statement itself.

Good pattern:
- theorem about a graph invariant, BDG score, winding, cut, or extension class
- then a separate prose note mapping that theorem to a measured quantity

Bad pattern:
- theorem stated directly in imported continuum or SM language
- theorem whose proof depends on `vacuum_lorentz_invariant`, external RG flow, or imported information-theory axioms

## 5. What a native Python script should look like
A script on the active path must have four explicit blocks:
1. **RA primitives** — BDG integers, depth rules, LLC, assembly rules.
2. **Nature inputs** — measured masses, lifetimes, orbital parameters, temperatures, etc.
3. **Native derivation** — no hidden theoretical imports.
4. **Nature comparison** — compare output only to measured data.

Forbidden on the active path:
- scheme-dependent couplings or scales
- gauge-group targets
- PDG quantum-number tables used as mechanism
- FLRW / QFT / GR equations as the real engine of the script

## 6. Writing discipline for the papers
Replace these patterns everywhere:
- “recover / reproduce SM or GR” → “predict the measured pattern / observable”
- “symmetry forbids” → “RA self-consistency blocks”
- “parameter” → “structure” whenever the quantity is internally derived
- “global unitarity is preserved” → “LLC is globally preserved; information is partitioned by severance”

## 7. Native milestone stack (current)
### Tier A — bedrock now
1. `RA_GraphCore.lean`
2. `RA_O14_Uniqueness.lean`
3. `RA_D1_Proofs.lean`
4. `RA_AmpLocality.lean`

### Tier B — quantitative native candidates
5. `RA_BaryonChirality.lean`
6. `RA_Alpha_EM_Proof.lean`
7. `RA_Koide.lean`
8. `rho_native.py` after removal of non-native inputs
9. topology/exit scripts after sigma-label provenance cleanup

### Tier C — complexity/life once Tier B is stable
10. `RA_Complexity_Proofs.lean`
11. `assembly_mapper.py` rewritten around RA-native assembly/depth measures
12. Paper IV internal categories only

### Tier D — deferred archive
- AQFT files
- Casimir / Unruh bridge material
- GR bridge material
- quantum-information bridge claims

## 8. Immediate next tasks
1. Freeze the bedrock theorem frontier and audit it line by line.
2. Quarantine scripts with explicit forbidden theory-object dependence.
3. Rewrite flagged paper sections before generating new public-facing prose.
4. Promote only those quantitative claims that survive the four-gate test.
5. For every mixed claim, restate the target as a Nature-quantity before doing any new derivation work.

## 9. Success criterion
A result counts as a success only when:
- the mechanism is RA-native,
- the target is Nature-facing,
- the inputs are primitive or measured,
- the output can be compared directly to data.

If RA succeeds this way, any later bridge to continuum physics is commentary, not validation.
