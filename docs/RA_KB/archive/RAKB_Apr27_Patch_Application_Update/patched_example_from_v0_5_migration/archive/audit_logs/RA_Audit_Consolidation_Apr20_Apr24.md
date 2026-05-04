
# RAKB Audit Consolidation: April 20–April 24, 2026

## Purpose

This document consolidates the distributed Relational Actualism Knowledge Base (RAKB) audit work performed between April 20 and April 24, 2026.

The audit was spread across chat sessions, Lean files, Python scripts, Markdown derivations, paper drafts, generated registries, dependency graphs, artifact inventories, and review feedback. This file is intended to become the working index of that audit so the project does not repeatedly rediscover decisions that have already been made.

## Governing conclusion

> **RAKB is now the authoritative project-state storage for Relational Actualism. Papers are public-facing projections; chats and session logs are provenance; the registry is the working map of the theory.**

## Authoritative audit window

The authoritative audit window for this consolidation is:

> **April 20, 2026 through April 24, 2026**

Older programme-state files remain useful legacy context, but they are not the baseline for the current registry. The decisive audit work was done after April 20.

## Major phases

### 1. Corpus recognition

The project was recognized as larger than a paper suite. It contains Lean theorem files, Python derivation and numerical scripts, Markdown derivation notes, paper drafts, generated metadata, and evolving support-surface summaries.

The diagnosis was that RA had outgrown document-based organization. A canonical knowledge base became necessary because paper drafts and chat logs were no longer reliable as the sole memory of the theory.

### 2. Paper-suite audit and overcorrection diagnosis

The four-paper suite was reviewed under a native-first framing discipline. A later correction clarified that the discipline had been over-applied: non-native bridge language should be removed, but RA-native numerical results should not be stripped merely because they address familiar empirical domains.

The corrected doctrine became:

> **RA targets Nature, derives through RA primitives, and compares with existing theories without borrowing their ontology, mechanisms, or formal artifacts as goals.**

### 3. Tiered restoration of native results

A tiered restoration pass reintroduced valid RA-native results into Papers II and III with explicit support status: Lean-backed motif and orientation results, the \(K=2/3\) identity, dimensionless interaction-scale arithmetic, \(\mu_{\mathrm{int}}\), the BDG path-weight ratio, kernel saturation identities, antichain drift, and D4U02 selectivity.

### 4. RAKB registry and theory graph

An initial registry was created and expanded into a dependency graph. The key realization was that RA is not linear; it is a dependency graph:

\[
\text{axioms} \to \text{kernel} \to \text{motifs/arithmetic} \to \text{observables} \to \text{phenomenology}.
\]

### 5. Schema correction

RAKB v0.4 split overloaded `status` into `proof_status` and `support_status`, and separated links into proof, framing, restoration, and later paper projection metadata. This made statements like “derived natively but compared through legacy cartography” expressible without overclaiming.

### 6. Prediction nodes

First-class `RA-PRED-*` nodes were introduced for empirical targets, including fine-structure inverse, proton mass scale, scalar/Higgs-scale target, \(f_0\) path-weight comparison, local Hubble/environment target, rotation/lensing, and Axis-of-Evil / low-\(\ell\) alignment.

### 7. Artifact inventory and source accountability

Source files were moved into a separate artifact inventory. This fixed the category error of treating source files as result nodes. Later patches filtered macOS metadata, duplicate browser-download files, and non-source garbage.

### 8. Lean source reconciliation

The D1-native family was identified as canonical motif support. `RA_MotifDynamics_Core.lean` was classified as a superseded wrapper over older draft imports, not active support. `RA_GraphCore_Native.lean` was accepted as the canonical uploaded/user-verified GraphCore source in the audit set. `RA_MotifDynamics_Core.lean` does not resolve the Type IV exact-zero question.

### 9. Validation cleanup

RAKB v0.4.5 fixed source-status enum mismatch, artifact inventory garbage, GraphCore source ambiguity, and added a prose-only DR audit.

## Current canonical state

- **Current authoritative registry:** RAKB v0.4.5, pending v0.5 reconstruction.
- **Tools:** RAKB tools are `v0.3-scaffold`; no automated extraction or proof validation yet.
- **Papers:** Zenodo papers are stable public snapshots, not the active development substrate.
- **Sources:** Lean support is relatively well organized; Python/MD support is visible but still incompletely linked.

## Resolved decisions

- RA targets Nature, not legacy formalisms.
- Existing theories are comparison maps, not mechanisms.
- `RA_MotifDynamics_Core.lean` is a superseded wrapper.
- The D1-native Lean family is canonical motif support.
- `RA_GraphCore_Native.lean` is canonical uploaded GraphCore support in this audit.
- Source files belong in artifact inventory, not as result nodes.
- Exact paper-section anchoring is deferred to a projection file.

## Still-open issues

### Missing prediction-source links

Three headline targets are under-linked:

- `RA-PRED-001`: \(\alpha_{\rm EM}^{-1} \approx 137.036\)
- `RA-PRED-002`: proton mass scale / \(2^{28}\) cascade
- `RA-PRED-003`: scalar/Higgs-scale \(\sim 125\) GeV target

These are not necessarily missing derivations. They are missing registry linkage to artifacts.

### Type IV exact-zero

`RA-MOTIF-009` remains unresolved. `RA_MotifDynamics_Core.lean` does not supply this support.

### Exploratory scripts

Several Python scripts are source-accounted but remain exploratory or comparative.

### Prose-only DR claims

Several derived-native claims are backed by paper prose rather than Lean/Python/MD artifacts. This is now visible and should be prioritized by downstream leverage.

## Immediate next tasks

1. Search the available source tree for missing prediction artifacts.
2. Update `RA-PRED-001`, `RA-PRED-002`, and `RA-PRED-003` if source artifacts are found.
3. If artifacts are not found, create compact MD/Python derivation artifacts.
4. Locate or archive Type IV exact-zero.
5. Move toward RAKB v0.5 as the first complete canonical reconstruction.
