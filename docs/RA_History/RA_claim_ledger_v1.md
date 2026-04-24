# RA Claim Ledger v1

Snapshot basis:
- Canonical papers: `RA_Paper_I_Kernel_and_Engine.tex`, `RA_Paper_II_Matter_Forces_and_Motifs.tex`, `RA_Paper_III_Gravity_Cosmology_Complexity.tex`, `RA_Paper_IV_Complexity_Life_Causal_Firewall.tex`
- Supporting audit inputs: `RA_Suite_Editorial_Catalog.md`, `RA_Framing_Discipline.md`, `RA_dir_tree.txt`
- This ledger is seeded from the papers' own epistemic-status tables, then tagged for audit strategy.

## Counts by paper
- P1: 24 status-table claims; 15 theorem-like environments
- P2: 37 status-table claims; 22 theorem-like environments
- P3: 45 status-table claims; 22 theorem-like environments
- P4: 32 status-table claims; 10 theorem-like environments

## Coarse status totals
| paper   |   AR |   CN |   CV |   DR |   LV |   Mixed |   Open |   PI |   Prediction |   Stated |
|:--------|-----:|-----:|-----:|-----:|-----:|--------:|-------:|-----:|-------------:|---------:|
| P1      |    1 |    0 |    4 |   14 |    2 |       0 |      1 |    0 |            0 |        2 |
| P2      |    0 |    3 |    6 |   13 |    6 |       0 |      0 |    9 |            0 |        0 |
| P3      |    2 |    1 |   12 |   16 |    7 |       0 |      0 |    3 |            4 |        0 |
| P4      |    1 |    3 |    8 |   16 |    0 |       1 |      0 |    1 |            2 |        0 |

## Strategic tracks added for the audit
1. `QFT-domain-recovery`
   - Claims that RA yields the phenomena usually organized by QM/QFT/SM language within their domains of applicability.
   - Core claim clusters: Paper I kinematic/measurement bridge; Paper II topology/couplings/force ranges/gauge structure.

2. `GR-domain-recovery`
   - Claims that RA yields the gravitational and cosmological phenomena usually organized by GR.
   - Core claim clusters: Paper III field equation, \Lambda=0, Lorentz/Bianchi translations, dark-matter-as-topology, severance/entropy.

3. `benchmark-observable`
   - Claims that should be tested against concrete observables or benchmark calculations.
   - Current suite/examples already named in the papers: BMV, WIMP exclusion, Hubble gradient, rotation curves, Bullet Cluster, DESI/CMB anomalies, KCB, biosignatures.

4. `calculation-utility`
   - Claims already expressed in a finite/discrete calculational form and therefore relevant to your "useful tool" criterion.
   - These are mostly LV/CV/DR rows with explicit numerical or combinatorial workflows.

5. `complexity-life` and `consciousness-exploratory`
   - Paper IV only; separated because they should not carry the burden of suite viability.

## Immediate audit priorities
- High: Paper III GR-derivation rows, because they bear the "RA yields GR in-domain" burden.
- High: Paper II gauge/mass-cascade rows, because they bear much of the "RA yields QFT/SM structure in-domain" burden.
- High: Paper IV Causal Firewall / assembly / quantum-information rows, because the current text still has legacy-supplement and primacy problems.
- Medium: Paper I bridge rows (Schrödinger limit, Rindler/Unruh, KCB/t*), because they set suite-wide expectations for the later papers.

## Benchmark-program note
Your added success criteria imply a second-pass benchmark docket beyond the paper-only claim ledger:
- Mercury perihelion / weak-field orbital precession
- gravitational lensing
- Casimir
- rotation curves / cluster lensing
- quantum-information ceilings and decoherence thresholds
- tractability vs continuum methods

In the currently uploaded core bundle, I did **not** find a Mercury-specific artifact. The full directory tree, however, advertises broader benchmark scripts in `src/RA_AQFT`, including `bullet_cluster.py`, `casimir_benchmark.py`, and related observables. That should become a dedicated benchmark track after the core claim audit.
