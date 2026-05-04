
# Relational Actualism Knowledge Base (RAKB)

This repository organizes the Relational Actualism (RA) theory as a **structured knowledge base** rather than a set of standalone papers.

## Core Principle

All development follows:

**Source → Registry → Analysis → Papers**

- Sources: Lean, Python, MD, CSV
- Registry: `RA_results_master.yaml` (ground truth)
- Analysis: dependency graph, metrics
- Papers: projections of the registry

## Workflow

### 1. Add/modify source files
- Lean proofs
- Python computations
- MD derivations

### 2. Scan into registry
Use the assistant prompt:

```
Scan the following files and update the RAKB...
```

### 3. Run integrity check
Ensures:
- no orphan results
- no orphan files
- correct status labels

### 4. Analyze dependencies
Identify:
- bottlenecks
- high-leverage targets
- weak claims

### 5. Update papers
Only after registry is correct.

## Status Labels

- ANC: Active Native Compiled (Lean)
- DR: Derived Native
- CV: Computational Verification
- PI: Provisional Interpretation
- CC: Comparative Cartography
- ONT: Open Native Target
- ARCH: Archived

## Rules

1. No result exists unless it is in the registry.
2. No paper claim exists without a registry ID.
3. Every source file must be referenced.
4. Every result must have a Nature-facing target.
5. Papers are projections, not sources of truth.

## Directory Structure

```
/registry/
  RA_results_master.yaml
/analysis/
  dependency_graph.dot
  metrics.csv
/papers/
  paper_I.tex
  paper_II.tex
  ...
/scripts/
  *.py
/lean/
  *.lean
```

## Goal

Maintain a **coherent, scalable theory graph** that supports:

- continuous research
- reproducibility
- controlled publication
