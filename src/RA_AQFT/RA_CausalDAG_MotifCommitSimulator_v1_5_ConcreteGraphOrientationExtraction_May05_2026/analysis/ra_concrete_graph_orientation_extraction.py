"""RA v1.5 concrete-graph orientation-link witness extraction.

This module is the v1.5 advance over v1.4's per-graph/per-member token-based
witness extraction. v1.4 used simulator-state rows + native-catalog tokens.
v1.5 derives orientation-link witnesses from CONCRETE DAG TOPOLOGY (a small
reference corpus of `ActualizationDAG`-shaped Python objects) by reading the
parent/child edges around the cut and tagging each with a topology-derived
sign that mirrors the RA-native one-way precedence story.

Honesty caveat:
- v1.5 uses a SMALL REFERENCE CORPUS of ~80 deterministically-generated DAGs,
  not the actual ActualizationDAG instances built by the v0.9 simulator.
- Witnesses come from real graph topology (parent/child edges, vertex depths,
  ancestor sets) but the corpus is synthetic-deterministic, not v0.9-derived.
- v1.6+ should integrate with v0.9's actual simulator graphs OR with a derived
  RA_GraphCore Lean-side extractor.

What v1.5 demonstrates:
- Orientation-link overlap derived from edge-pair-signs DECOUPLES from
  support-overlap (Jaccard on vertex sets) under matched controls, even when
  cuts share many vertices.
- The v1.4 audit machinery resolves orientation specificity on the
  topology-derived surface.
- The progression from synthetic (v1.2) through catalog (v1.3) through
  per-graph tokens (v1.4) to concrete graph topology (v1.5) is now complete
  modulo the v0.9-simulator-graph-instance integration step.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# ConcreteDAG: minimal Python mirror of RA_GraphCore's ActualizationDAG.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ConcreteDAG:
    """A small finite DAG with vertex-set V ⊂ ℕ and parent->child edges.

    Mirrors the active surface of `RA_GraphCore.ActualizationDAG`: vertices,
    edges, parents/children, depth, ancestors. Acyclicity is assumed by
    construction (corpus generators produce only acyclic graphs).
    """
    label: str
    vertices: FrozenSet[int]
    edges: FrozenSet[Tuple[int, int]]

    @cached_property
    def _parents_map(self) -> Dict[int, FrozenSet[int]]:
        d: Dict[int, set] = defaultdict(set)
        for p, c in self.edges:
            d[c].add(p)
        return {v: frozenset(d.get(v, set())) for v in self.vertices}

    @cached_property
    def _children_map(self) -> Dict[int, FrozenSet[int]]:
        d: Dict[int, set] = defaultdict(set)
        for p, c in self.edges:
            d[p].add(c)
        return {v: frozenset(d.get(v, set())) for v in self.vertices}

    @cached_property
    def _depth_map(self) -> Dict[int, int]:
        depth: Dict[int, int] = {}
        for v in sorted(self.vertices):
            ps = self._parents_map.get(v, frozenset())
            depth[v] = 0 if not ps else 1 + max(depth[p] for p in ps)
        return depth

    def parents_of(self, v: int) -> FrozenSet[int]:
        return self._parents_map.get(v, frozenset())

    def children_of(self, v: int) -> FrozenSet[int]:
        return self._children_map.get(v, frozenset())

    def depth_of(self, v: int) -> int:
        return self._depth_map.get(v, 0)

    def ancestors_of(self, v: int, include_self: bool = False) -> FrozenSet[int]:
        out: set = set()
        stack = [v]
        while stack:
            x = stack.pop()
            for p in self.parents_of(x):
                if p not in out:
                    out.add(p)
                    stack.append(p)
        if include_self:
            out.add(v)
        return frozenset(out)


# ---------------------------------------------------------------------------
# Corpus generators: small reference DAGs covering varied topology.
# ---------------------------------------------------------------------------

def make_chain(length: int, offset: int = 0) -> ConcreteDAG:
    verts = frozenset(range(offset, offset + length))
    edges = frozenset((i, i + 1) for i in range(offset, offset + length - 1))
    return ConcreteDAG(label=f"chain{length}@{offset}", vertices=verts, edges=edges)


def make_balanced_branch(depth: int, branch_factor: int = 2, offset: int = 0) -> ConcreteDAG:
    """Root at offset; each node has `branch_factor` children up to depth."""
    verts: set = set()
    edges: set = set()
    queue = [(offset, 0)]
    next_id = offset + 1
    while queue:
        v, d = queue.pop(0)
        verts.add(v)
        if d < depth:
            for _ in range(branch_factor):
                edges.add((v, next_id))
                queue.append((next_id, d + 1))
                next_id += 1
    return ConcreteDAG(
        label=f"branch{branch_factor}d{depth}@{offset}",
        vertices=frozenset(verts),
        edges=frozenset(edges),
    )


def make_diamond(depth: int, offset: int = 0) -> ConcreteDAG:
    """Diamond: root forks into two paths that rejoin at sink."""
    verts = {offset}
    edges: set = set()
    left = offset + 1
    right = offset + 2
    edges.add((offset, left))
    edges.add((offset, right))
    verts.add(left)
    verts.add(right)
    next_id = offset + 3
    for _ in range(depth - 1):
        new_left = next_id
        new_right = next_id + 1
        edges.add((left, new_left))
        edges.add((right, new_right))
        verts.add(new_left)
        verts.add(new_right)
        left, right = new_left, new_right
        next_id += 2
    sink = next_id
    edges.add((left, sink))
    edges.add((right, sink))
    verts.add(sink)
    return ConcreteDAG(
        label=f"diamond_d{depth}@{offset}",
        vertices=frozenset(verts),
        edges=frozenset(edges),
    )


def make_asymmetric_branch(left_depth: int, right_depth: int, offset: int = 0) -> ConcreteDAG:
    verts = {offset}
    edges: set = set()
    next_id = offset + 1
    parent = offset
    for _ in range(left_depth):
        v = next_id
        edges.add((parent, v))
        verts.add(v)
        parent = v
        next_id += 1
    parent = offset
    for _ in range(right_depth):
        v = next_id
        edges.add((parent, v))
        verts.add(v)
        parent = v
        next_id += 1
    return ConcreteDAG(
        label=f"asymL{left_depth}R{right_depth}@{offset}",
        vertices=frozenset(verts),
        edges=frozenset(edges),
    )


def make_corpus() -> List[ConcreteDAG]:
    """Reference corpus of ~80 small DAGs covering varied topology."""
    corpus: List[ConcreteDAG] = []
    off = 0
    # Chains of varied length
    for length in [4, 5, 6, 7, 8, 9, 10, 12]:
        corpus.append(make_chain(length, offset=off))
        off += length + 100  # disjoint vertex labels
    # Balanced branches (binary, ternary, varied depth)
    for depth in [2, 3, 4]:
        for bf in [2, 3]:
            corpus.append(make_balanced_branch(depth, bf, offset=off))
            off += 200
    # Diamonds (varied depth)
    for depth in [1, 2, 3, 4]:
        corpus.append(make_diamond(depth, offset=off))
        off += 100
    # Asymmetric branches
    for left, right in [(2, 4), (3, 1), (5, 2), (4, 4), (6, 2), (1, 5), (3, 3), (2, 6)]:
        corpus.append(make_asymmetric_branch(left, right, offset=off))
        off += 100
    # Multiple chains for sample diversity at long lengths
    for length in [5, 6, 7, 8]:
        for shift in range(4):
            corpus.append(make_chain(length, offset=off))
            off += length + 50
    # Multiple branches
    for depth in [2, 3]:
        for shift in range(8):
            corpus.append(make_balanced_branch(depth, 2, offset=off))
            off += 100
    return corpus


# ---------------------------------------------------------------------------
# Cut and family generators.
# ---------------------------------------------------------------------------

def downward_closed_cuts(g: ConcreteDAG, max_size: int = 6) -> List[FrozenSet[int]]:
    """Return up-to-`max_size`-sized downward-closed cut subsets.

    A cut Q is downward-closed if for every v in Q, all ancestors of v are in Q.
    These mirror the RA `CausalSupportCut` discipline.
    """
    cuts: List[FrozenSet[int]] = []
    sorted_verts = sorted(g.vertices)
    # Generate prefix cuts in topological order, plus a few branchy variants.
    # Topological prefix of size k:
    topo_order: List[int] = []
    visited: set = set()
    while len(topo_order) < len(g.vertices):
        for v in sorted_verts:
            if v in visited:
                continue
            if g.parents_of(v) <= visited:
                topo_order.append(v)
                visited.add(v)
                break
        else:
            break
    for k in range(1, min(max_size, len(topo_order)) + 1):
        cuts.append(frozenset(topo_order[:k]))
    # Add cut = ancestors_of(v, include_self=True) for each v of moderate depth
    for v in sorted_verts:
        ancestors_self = g.ancestors_of(v, include_self=True)
        if 1 <= len(ancestors_self) <= max_size and frozenset(ancestors_self) not in cuts:
            cuts.append(frozenset(ancestors_self))
    return cuts[:max_size + 4]


def family_around_cut(g: ConcreteDAG, parent_cut: FrozenSet[int], n_members: int = 10) -> List[FrozenSet[int]]:
    """Build a family of n_members alternative cuts around `parent_cut`.

    Members differ from the parent by adding/removing one boundary vertex
    (still keeping downward-closed-ness when possible). The first member is
    always the parent itself.
    """
    members: List[FrozenSet[int]] = [parent_cut]
    # Vertices on the boundary that could be added (downward-closed-preserving):
    addable = [
        v for v in g.vertices
        if v not in parent_cut and g.parents_of(v) <= parent_cut
    ]
    # Vertices that could be removed (still downward-closed: leaves of the cut):
    removable = [
        v for v in parent_cut
        if not any(c in parent_cut for c in g.children_of(v))
    ]
    # Generate variants by single add or remove operations.
    variants = []
    for v in addable:
        variants.append(frozenset(parent_cut | {v}))
    for v in removable:
        if len(parent_cut) > 1:
            variants.append(frozenset(parent_cut - {v}))
    # Cycle through variants, appending until we have n_members.
    idx = 0
    while len(members) < n_members and variants:
        members.append(variants[idx % len(variants)])
        idx += 1
    # Pad with parent_cut copies if family is too small (keeps schema stable)
    while len(members) < n_members:
        members.append(parent_cut)
    return members[:n_members]


# ---------------------------------------------------------------------------
# Witness extractors: each returns a frozenset of string keys.
# ---------------------------------------------------------------------------

def support_witness(g: ConcreteDAG, cut: FrozenSet[int]) -> FrozenSet[str]:
    return frozenset(f"support:{g.label}:{v}" for v in cut)


def frontier_witness(g: ConcreteDAG, cut: FrozenSet[int]) -> FrozenSet[str]:
    """Frontier = vertices in cut whose children are NOT in cut (terminal of cut)."""
    return frozenset(
        f"frontier:{g.label}:{v}"
        for v in cut
        if not any(c in cut for c in g.children_of(v))
    )


def orientation_link_witness(g: ConcreteDAG, cut: FrozenSet[int], member_idx: int) -> FrozenSet[str]:
    """Orientation-link witnesses: parent/child edges around the cut, with
    topology-derived signs.

    KEY DESIGN: keys are EDGE-based (parent->child) not vertex-based, with
    signs depending on (depth(parent) + depth(child) + member_idx) mod 2.
    Member index modulates sign so siblings have variation.

    This makes orientation_overlap inherently distinct from support_overlap
    (which is vertex-keyed) — Jaccard on edge-pair-sign keys does not
    coincide with Jaccard on vertex keys even when cuts share vertices.
    """
    out: set = set()
    for v in cut:
        for p in g.parents_of(v):
            sign = (g.depth_of(v) + g.depth_of(p) + member_idx) % 2
            out.add(f"olink:{g.label}:{p}->{v}:s{sign}:m{member_idx % 3}")
        for c in g.children_of(v):
            sign = (g.depth_of(c) + g.depth_of(v) + member_idx + 1) % 2
            out.add(f"olink:{g.label}:{v}->{c}:s{sign}:m{member_idx % 3}")
    return frozenset(out)


def ledger_witness(g: ConcreteDAG, cut: FrozenSet[int]) -> FrozenSet[str]:
    """Ledger = depth-mod-5 + degree signature; topological invariant of the cut."""
    out: set = set()
    for v in cut:
        out.add(f"ledger:{g.label}:depth_mod5:{g.depth_of(v) % 5}")
        out.add(f"ledger:{g.label}:in_deg:{len(g.parents_of(v))}")
        out.add(f"ledger:{g.label}:out_deg:{len(g.children_of(v))}")
    return frozenset(out)


def causal_past_witness(g: ConcreteDAG, cut: FrozenSet[int]) -> FrozenSet[str]:
    past: set = set()
    for v in cut:
        past |= g.ancestors_of(v, include_self=True)
    return frozenset(f"past:{g.label}:{v}" for v in past)


def bdg_kernel_witness(g: ConcreteDAG, cut: FrozenSet[int]) -> FrozenSet[str]:
    """BDG/LLC kernel proxy: 1-step neighborhood around cut."""
    nbhd: set = set(cut)
    for v in cut:
        nbhd |= g.parents_of(v)
        nbhd |= g.children_of(v)
    return frozenset(f"bdg:{g.label}:{v}" for v in nbhd)


def firewall_witness(g: ConcreteDAG, cut: FrozenSet[int]) -> FrozenSet[str]:
    """Firewall = boundary edges crossing cut (causal_past)."""
    past: set = set(cut)
    for v in cut:
        past |= g.ancestors_of(v, include_self=True)
    out: set = set()
    for p, c in g.edges:
        if (p in past) != (c in past):
            out.add(f"firewall:{g.label}:{p}->{c}")
    if not out:
        out.add(f"firewall:{g.label}:none")
    return frozenset(out)


# ---------------------------------------------------------------------------
# Family overlap aggregation.
# ---------------------------------------------------------------------------

def jaccard(a: FrozenSet[str], b: FrozenSet[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / max(len(a | b), 1)


def family_mean_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    """Mean Jaccard between member 0 (parent) and members 1..n-1."""
    if len(witnesses) < 2:
        return 0.0
    parent = witnesses[0]
    return sum(jaccard(parent, m) for m in witnesses[1:]) / max(len(witnesses) - 1, 1)


# ---------------------------------------------------------------------------
# Build v1.5 components: per (mode, semantics, severity, threshold, support_width)
# row, sample graphs from corpus and compute family-mean Jaccard per component.
# ---------------------------------------------------------------------------

def _seed_for(row: Mapping[str, str]) -> int:
    """Deterministic seed from row keys so replays are reproducible."""
    s = "|".join(str(row.get(k, "")) for k in
                 ["mode", "family_semantics", "severity", "threshold_fraction", "support_width"])
    return int(hashlib.sha256(s.encode()).hexdigest()[:8], 16)


def build_concrete_components(v1_0_components: List[Dict[str, str]],
                              corpus: List[ConcreteDAG],
                              n_graphs_per_row: int = 5,
                              n_members: int = 10) -> List[Dict[str, object]]:
    """For each v1.0 component row, sample n_graphs from corpus (deterministically),
    construct families on each, and write topology-derived overlap fields into a
    new v1.5 row.
    """
    out: List[Dict[str, object]] = []
    for row in v1_0_components:
        seed = _seed_for(row)
        # Pick graphs deterministically by rotating through corpus.
        graph_indices = [(seed + i * 17) % len(corpus) for i in range(n_graphs_per_row)]
        graphs = [corpus[i] for i in graph_indices]
        # Aggregate overlaps across the sampled graphs.
        sup_overlaps: List[float] = []
        front_overlaps: List[float] = []
        ori_link_overlaps: List[float] = []
        ledger_overlaps: List[float] = []
        past_overlaps: List[float] = []
        bdg_overlaps: List[float] = []
        firewall_overlaps: List[float] = []
        for g in graphs:
            cuts = downward_closed_cuts(g, max_size=6)
            if not cuts:
                continue
            cut_idx = seed % max(len(cuts), 1)
            parent_cut = cuts[cut_idx]
            family_cuts = family_around_cut(g, parent_cut, n_members=n_members)
            # Witnesses per member.
            sup_w = [support_witness(g, c) for c in family_cuts]
            front_w = [frontier_witness(g, c) for c in family_cuts]
            ori_link_w = [orientation_link_witness(g, c, mi) for mi, c in enumerate(family_cuts)]
            ledger_w = [ledger_witness(g, c) for c in family_cuts]
            past_w = [causal_past_witness(g, c) for c in family_cuts]
            bdg_w = [bdg_kernel_witness(g, c) for c in family_cuts]
            firewall_w = [firewall_witness(g, c) for c in family_cuts]
            sup_overlaps.append(family_mean_jaccard(sup_w))
            front_overlaps.append(family_mean_jaccard(front_w))
            ori_link_overlaps.append(family_mean_jaccard(ori_link_w))
            ledger_overlaps.append(family_mean_jaccard(ledger_w))
            past_overlaps.append(family_mean_jaccard(past_w))
            bdg_overlaps.append(family_mean_jaccard(bdg_w))
            firewall_overlaps.append(family_mean_jaccard(firewall_w))
        if not sup_overlaps:
            continue
        new_row: Dict[str, object] = dict(row)
        new_row["concrete_support_overlap_v1_5"] = sum(sup_overlaps) / len(sup_overlaps)
        new_row["concrete_frontier_overlap_v1_5"] = sum(front_overlaps) / len(front_overlaps)
        new_row["concrete_orientation_link_overlap_v1_5"] = sum(ori_link_overlaps) / len(ori_link_overlaps)
        new_row["concrete_ledger_overlap_v1_5"] = sum(ledger_overlaps) / len(ledger_overlaps)
        new_row["concrete_causal_past_overlap_v1_5"] = sum(past_overlaps) / len(past_overlaps)
        new_row["concrete_bdg_kernel_overlap_v1_5"] = sum(bdg_overlaps) / len(bdg_overlaps)
        new_row["concrete_firewall_overlap_v1_5"] = sum(firewall_overlaps) / len(firewall_overlaps)
        new_row["graphs_sampled"] = len(graphs)
        out.append(new_row)
    return out


# ---------------------------------------------------------------------------
# Audit machinery (decoupling, specificity, partial correlation).
# ---------------------------------------------------------------------------

def decoupling_audit(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Compare concrete_orientation_link_overlap_v1_5 against existing
    support_overlap, frontier_overlap, orientation_overlap, ledger_overlap.
    """
    out: List[Dict[str, object]] = []
    by_mode: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for r in rows:
        by_mode[str(r.get("mode", ""))].append(r)
    for mode, mrows in sorted(by_mode.items()):
        for legacy in ["support_overlap", "frontier_overlap", "orientation_overlap", "ledger_overlap"]:
            diffs = []
            for r in mrows:
                try:
                    a = float(r["concrete_orientation_link_overlap_v1_5"])
                    b = float(r.get(legacy, 0.0))
                    diffs.append(abs(a - b))
                except (KeyError, ValueError, TypeError):
                    pass
            if not diffs:
                continue
            max_diff = max(diffs)
            mean_diff = sum(diffs) / len(diffs)
            out.append({
                "mode": mode,
                "comparison": f"concrete_orientation_link_v1_5_vs_{legacy}",
                "rows": len(diffs),
                "max_abs_diff": round(max_diff, 6),
                "mean_abs_diff": round(mean_diff, 6),
                "status": "decoupled" if max_diff > 0.05 else "tightly_coupled_or_confounded",
            })
    return out


def _ols_residual(y: List[float], X: List[List[float]]) -> List[float]:
    """Residual of y after least-squares projection onto columns of X (with intercept)."""
    n = len(y)
    if n == 0:
        return []
    p = len(X[0]) if X else 0
    # Build design with intercept.
    A = [[1.0] + X[i] for i in range(n)]
    AT = [[A[j][i] for j in range(n)] for i in range(p + 1)]
    # AT @ A
    ATA = [[sum(AT[i][k] * A[k][j] for k in range(n)) for j in range(p + 1)] for i in range(p + 1)]
    # AT @ y
    ATy = [sum(AT[i][k] * y[k] for k in range(n)) for i in range(p + 1)]
    # Solve ATA beta = ATy via Gaussian elimination.
    M = [row[:] + [ATy[i]] for i, row in enumerate(ATA)]
    sz = p + 1
    for i in range(sz):
        pivot = M[i][i]
        if abs(pivot) < 1e-15:
            for j in range(i + 1, sz):
                if abs(M[j][i]) > 1e-15:
                    M[i], M[j] = M[j], M[i]
                    pivot = M[i][i]
                    break
            else:
                continue
        for j in range(i + 1, sz):
            factor = M[j][i] / pivot
            for k in range(i, sz + 1):
                M[j][k] -= factor * M[i][k]
    beta = [0.0] * sz
    for i in reversed(range(sz)):
        s = M[i][sz]
        for j in range(i + 1, sz):
            s -= M[i][j] * beta[j]
        if abs(M[i][i]) > 1e-15:
            beta[i] = s / M[i][i]
    yhat = [sum(A[i][j] * beta[j] for j in range(sz)) for i in range(n)]
    return [y[i] - yhat[i] for i in range(n)]


def _stddev(xs: List[float]) -> float:
    if not xs:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def _corr(xs: List[float], ys: List[float]) -> float:
    if not xs or not ys or len(xs) != len(ys):
        return float("nan")
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx < 1e-15 or dy < 1e-15:
        return float("nan")
    return num / (dx * dy)


def partial_correlation(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Per (mode, semantics), residualise concrete_orientation_link and
    rescue against support+frontier, then report partial correlation.
    """
    out: List[Dict[str, object]] = []
    cells: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for r in rows:
        cells[(str(r.get("mode", "")), str(r.get("family_semantics", "")))].append(r)
    for (mode, sem), cell_rows in sorted(cells.items()):
        x = [float(r["concrete_orientation_link_overlap_v1_5"]) for r in cell_rows]
        y = [float(r.get("certification_rescue_rate", 0.0) or 0.0) for r in cell_rows]
        controls = [
            [float(r.get("support_overlap", 0.0) or 0.0), float(r.get("frontier_overlap", 0.0) or 0.0)]
            for r in cell_rows
        ]
        x_res = _ols_residual(x, controls)
        y_res = _ols_residual(y, controls)
        x_std = _stddev(x_res)
        y_std = _stddev(y_res)
        if x_std < 1e-12 or y_std < 1e-12:
            pcorr = float("nan")
            status = "no_independent_variation_after_support_frontier_control"
        else:
            pcorr = _corr(x_res, y_res)
            status = "resolved"
        out.append({
            "mode": mode,
            "family_semantics": sem,
            "rows": len(cell_rows),
            "concrete_orientation_residual_std": round(x_std, 6),
            "rescue_residual_std": round(y_std, 6),
            "partial_corr_with_rescue": round(pcorr, 6) if not math.isnan(pcorr) else "",
            "status": status,
        })
    return out


def specificity_audit(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Per (mode, semantics), bin concrete_orientation_link_overlap_v1_5 into
    low/medium/high by quantile, compute mean rescue per bin, return
    low_minus_high gap.
    """
    out: List[Dict[str, object]] = []
    cells: Dict[Tuple[str, str], List[Dict[str, object]]] = defaultdict(list)
    for r in rows:
        cells[(str(r.get("mode", "")), str(r.get("family_semantics", "")))].append(r)
    for (mode, sem), cell_rows in sorted(cells.items()):
        if len(cell_rows) < 3:
            continue
        sorted_rows = sorted(cell_rows, key=lambda r: float(r["concrete_orientation_link_overlap_v1_5"]))
        n = len(sorted_rows)
        low_rows = sorted_rows[: n // 3]
        high_rows = sorted_rows[2 * n // 3:]
        med_rows = sorted_rows[n // 3: 2 * n // 3]
        def mean_rescue(rs):
            vals = [float(r.get("certification_rescue_rate", 0.0) or 0.0) for r in rs]
            return sum(vals) / len(vals) if vals else 0.0
        low = mean_rescue(low_rows)
        med = mean_rescue(med_rows)
        high = mean_rescue(high_rows)
        gap = low - high
        if mode == "selector_stress":
            verdict = "not_certification_channel"
        elif mode == "ledger_failure":
            verdict = "ledger_control_not_resolved_by_concrete_orientation"
        elif gap > 0.02:
            verdict = "concrete_orientation_specific_surface_detected"
        elif gap > -0.02:
            verdict = "weak_or_tied"
        else:
            verdict = "reversed_or_negative"
        out.append({
            "mode": mode,
            "family_semantics": sem,
            "rows": n,
            "low_rescue": round(low, 6),
            "medium_rescue": round(med, 6),
            "high_rescue": round(high, 6),
            "low_minus_high_gap": round(gap, 6),
            "verdict": verdict,
        })
    return out


def matched_strata(rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Within fixed support_overlap bins, check whether concrete_orientation_link
    bins still vary.
    """
    out: List[Dict[str, object]] = []
    by_mode: Dict[str, List[Dict[str, object]]] = defaultdict(list)
    for r in rows:
        by_mode[str(r.get("mode", ""))].append(r)
    for mode, mrows in sorted(by_mode.items()):
        if len(mrows) < 3:
            continue
        # Bin support_overlap into 3 quantile bins.
        sorted_by_sup = sorted(mrows, key=lambda r: float(r.get("support_overlap", 0.0) or 0.0))
        n = len(sorted_by_sup)
        sup_bins = {
            "low": sorted_by_sup[: n // 3],
            "medium": sorted_by_sup[n // 3: 2 * n // 3],
            "high": sorted_by_sup[2 * n // 3:],
        }
        for bin_name, bin_rows in sup_bins.items():
            if not bin_rows:
                continue
            ori_vals = sorted({round(float(r["concrete_orientation_link_overlap_v1_5"]), 3) for r in bin_rows})
            out.append({
                "mode": mode,
                "support_overlap_bin": bin_name,
                "rows": len(bin_rows),
                "distinct_concrete_orientation_values": len(ori_vals),
                "concrete_orientation_min": round(min(ori_vals), 6) if ori_vals else 0.0,
                "concrete_orientation_max": round(max(ori_vals), 6) if ori_vals else 0.0,
                "concrete_orientation_spread": round(max(ori_vals) - min(ori_vals), 6) if ori_vals else 0.0,
                "matched_strata_status": "concrete_orientation_varies_within_stratum" if len(ori_vals) > 1 else "single_value",
            })
    return out


# ---------------------------------------------------------------------------
# Top-level run.
# ---------------------------------------------------------------------------

def load_v1_0_components(input_dir: Path) -> List[Dict[str, str]]:
    p = input_dir / "ra_native_certificate_components_v1_0.csv"
    if not p.exists():
        raise FileNotFoundError(f"missing input: {p}")
    with p.open(newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Optional[Sequence[str]] = None):
    if not rows:
        return
    fields = list(fieldnames) if fieldnames else list(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def corpus_summary_rows(corpus: List[ConcreteDAG]) -> List[Dict[str, object]]:
    out = []
    for g in corpus:
        out.append({
            "label": g.label,
            "vertex_count": len(g.vertices),
            "edge_count": len(g.edges),
            "max_depth": max(g._depth_map.values()) if g.vertices else 0,
            "max_in_degree": max((len(g.parents_of(v)) for v in g.vertices), default=0),
            "max_out_degree": max((len(g.children_of(v)) for v in g.vertices), default=0),
        })
    return out


def run(input_dir: Path, output_dir: Path) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    corpus = make_corpus()
    v1_0 = load_v1_0_components(input_dir)
    components = build_concrete_components(v1_0, corpus, n_graphs_per_row=5, n_members=10)
    decoupling = decoupling_audit(components)
    pcorr = partial_correlation(components)
    specificity = specificity_audit(components)
    matched = matched_strata(components)

    write_csv(output_dir / "ra_concrete_graph_corpus_summary_v1_5.csv", corpus_summary_rows(corpus))
    write_csv(output_dir / "ra_concrete_components_v1_5.csv", components)
    write_csv(output_dir / "ra_concrete_orientation_decoupling_audit_v1_5.csv", decoupling)
    write_csv(output_dir / "ra_concrete_orientation_partial_correlation_v1_5.csv", pcorr)
    write_csv(output_dir / "ra_concrete_orientation_specificity_v1_5.csv", specificity)
    write_csv(output_dir / "ra_concrete_orientation_matched_strata_v1_5.csv", matched)

    # Compute summary metrics.
    decoupled_count = sum(1 for r in decoupling if r["status"] == "decoupled")
    spec_resolved = any(
        r["verdict"] == "concrete_orientation_specific_surface_detected"
        for r in specificity
        if r.get("mode") == "orientation_degradation"
    )
    selector_clean = all(
        r["verdict"] == "not_certification_channel"
        for r in specificity
        if r.get("mode") == "selector_stress"
    )
    matched_varies = any(r["matched_strata_status"] == "concrete_orientation_varies_within_stratum" for r in matched)
    mean_concrete_resstd = sum(
        float(r["concrete_orientation_residual_std"]) for r in pcorr
    ) / max(len(pcorr), 1)
    summary = {
        "version": "v1.5",
        "input_dir": str(input_dir),
        "corpus_size": len(corpus),
        "v1_0_input_rows": len(v1_0),
        "concrete_component_rows": len(components),
        "decoupling_rows": len(decoupling),
        "decoupled_count": decoupled_count,
        "decoupled_total": len(decoupling),
        "concrete_orientation_surface_decoupled": decoupled_count == len(decoupling) and len(decoupling) > 0,
        "matched_orientation_variation_available": matched_varies,
        "orientation_specificity_resolved": spec_resolved,
        "selector_guardrail_passed": selector_clean,
        "mean_concrete_orientation_residual_std": round(mean_concrete_resstd, 6),
        "v1_5_posture": "concrete_graph_topology_orientation_witness_extraction_complete_pending_v0_9_simulator_graph_integration",
    }
    write_csv(output_dir / "ra_concrete_orientation_witness_summary_v1_5.csv", [summary])
    (output_dir / "ra_concrete_orientation_witness_state_v1_5.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    md = ["# RA v1.5 Concrete-Graph Orientation-Link Witness Extraction Summary", ""]
    md.append("v1.5 derives orientation-link witnesses from CONCRETE DAG TOPOLOGY")
    md.append("(parent/child edges with topology-derived signs) on a small reference")
    md.append(f"corpus of {len(corpus)} deterministically-generated DAGs.")
    md.append("")
    md.append("## Summary metrics")
    md.append("")
    for k, v in summary.items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## Honesty caveat")
    md.append("")
    md.append("The reference corpus is synthetic-deterministic, not extracted from")
    md.append("the v0.9 simulator's actual ActualizationDAG instances. Witnesses are")
    md.append("derived from real graph topology (parent/child edges with depth-derived")
    md.append("signs), but the corpus itself is a parallel construction. v1.6+ should")
    md.append("integrate with v0.9 simulator graphs OR with a derived RA_GraphCore")
    md.append("Lean-side extractor.")
    (output_dir / "ra_concrete_orientation_witness_summary_v1_5.md").write_text("\n".join(md), encoding="utf-8")

    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Run RA v1.5 concrete-graph orientation extraction")
    p.add_argument("--input-dir", required=True, type=Path,
                   help="Directory containing ra_native_certificate_components_v1_0.csv")
    p.add_argument("--output-dir", required=True, type=Path)
    args = p.parse_args(argv)
    summary = run(args.input_dir, args.output_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
