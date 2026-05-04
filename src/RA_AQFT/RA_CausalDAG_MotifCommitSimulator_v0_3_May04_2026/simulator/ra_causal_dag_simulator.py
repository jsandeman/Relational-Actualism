#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.3

This simulator mirrors the vocabulary of RA_MotifCommitProtocol.lean and adds
an explicit selector-closure layer downstream of strict commit semantics.

Lean-to-Python correspondence:

  MotifCandidate / GraphMotifCandidate
    ↔ MotifCandidate

  CausalSupportCut / GraphSupportCut
    ↔ SupportCut = frozenset[node_id]

  supportCutOfFiniteHasseFrontier
    ↔ CausalDAG.support_cut_of_finite_hasse_frontier

  ReadyAt
    ↔ CausalDAG.ready_at

  CommitContext.supports
    ↔ GraphSupportCertifier.supports, wrapped by CommitContext

  CommitContext.incompatible
    ↔ CommitContext.incompatible

  Strict CommitsAt
    ↔ MotifCommitProtocol.decision(...).commits

  Selector-closed commit
    ↔ MotifCommitProtocol.selected_decision(...).commits

  FinalizedAtDepth
    ↔ CausalDAG.finalized_at_depth

This is intentionally not a blockchain/consensus simulator. There are no agents,
votes, leaders, or message rounds. The central RA-native question is:

  Which motif candidates have certified support cuts whose support vertices lie
  in the causal past of a site, which are excluded by certified-ready
  incompatible competitors under strict CommitsAt, and how can a downstream
  selector closure narrow mutually incompatible alternatives before commit?

Important boundary:

  The strict decision path is the direct simulator counterpart of the compiled
  RA_MotifCommitProtocol interface. The selector-closed path is a downstream
  experimental extension meant to model how RA_ActualizationSelector-style
  closure could narrow the eligible frontier before strict incompatibility
  exclusion is evaluated.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


NodeId = int
SupportCut = FrozenSet[NodeId]


@dataclass(frozen=True)
class MotifCandidate:
    """Finite motif candidate with carrier, support cut, and optional metadata.

    `exclusion_domain` is a simulator convenience for defining incompatibility:
    two candidates with the same non-null exclusion domain and distinct names are
    treated as incompatible by the default context.

    Metadata keys used by the support certifier:
      - candidate_past: list[int] or set[int]
      - bdg_local_ok: bool, default True
      - ledger_local_ok: bool, default True
      - orientation_closure_ok: bool, default True

    The three *_ok flags are explicit experimental gates. They are not claimed
    to derive BDG locality, ledger closure, or orientation closure; they simply
    make those future attachment points operational in the simulator.
    """

    name: str
    carrier: FrozenSet[NodeId]
    support_cut: SupportCut
    kind: str = "generic"
    exclusion_domain: Optional[str] = None
    certified: bool = True
    priority: int = 0
    metadata: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class SupportGateResult:
    gate: str
    passed: bool
    detail: str = ""


@dataclass(frozen=True)
class SupportEvaluation:
    motif: str
    support_cut: Tuple[NodeId, ...]
    supported: bool
    gates: Tuple[SupportGateResult, ...]

    @property
    def failed_gates(self) -> Tuple[str, ...]:
        return tuple(g.gate for g in self.gates if not g.passed)

    @property
    def passed_gates(self) -> Tuple[str, ...]:
        return tuple(g.gate for g in self.gates if g.passed)

    def to_row(self) -> Dict[str, object]:
        return {
            "motif": self.motif,
            "support_cut": list(self.support_cut),
            "supported": self.supported,
            "passed_gates": list(self.passed_gates),
            "failed_gates": list(self.failed_gates),
            "gate_details": [
                {"gate": g.gate, "passed": g.passed, "detail": g.detail}
                for g in self.gates
            ],
        }


@dataclass(frozen=True)
class CommitDecision:
    """Strict Lean-style motif-commit decision."""

    motif: str
    site: NodeId
    supported: bool
    ready: bool
    commits: bool
    blocked_by: Tuple[str, ...] = ()
    support_failures: Tuple[str, ...] = ()


@dataclass(frozen=True)
class SelectorComponentTrace:
    component_id: int
    candidates: Tuple[str, ...]
    selected: Tuple[str, ...]
    rejected: Tuple[str, ...]
    stalemate: bool
    reason: str

    def to_row(self, site: NodeId) -> Dict[str, object]:
        return {
            "site": site,
            "component_id": self.component_id,
            "candidates": list(self.candidates),
            "selected": list(self.selected),
            "rejected": list(self.rejected),
            "stalemate": self.stalemate,
            "reason": self.reason,
        }


@dataclass(frozen=True)
class SelectorClosureResult:
    """Result of narrowing certified-ready motifs at a site."""

    site: NodeId
    mode: str
    tie_policy: str
    eligible: Tuple[str, ...]
    selected: Tuple[str, ...]
    rejected: Tuple[str, ...]
    stalemates: Tuple[str, ...]
    components: Tuple[SelectorComponentTrace, ...]

    def selected_set(self) -> Set[str]:
        return set(self.selected)

    def rejected_set(self) -> Set[str]:
        return set(self.rejected)

    def stalemate_set(self) -> Set[str]:
        return set(self.stalemates)

    def component_rows(self) -> List[Dict[str, object]]:
        return [c.to_row(self.site) for c in self.components]


@dataclass(frozen=True)
class SelectedCommitDecision:
    """Commit decision after selector closure has narrowed eligible motifs."""

    motif: str
    site: NodeId
    supported: bool
    ready: bool
    selected: bool
    commits: bool
    selector_reason: str
    strict_blocked_by: Tuple[str, ...] = ()
    selected_blocked_by: Tuple[str, ...] = ()
    support_failures: Tuple[str, ...] = ()


class CausalDAG:
    """Append-only finite DAG with edges oriented from causal past to future."""

    def __init__(self) -> None:
        self.parents: Dict[NodeId, Set[NodeId]] = {}
        self.children: Dict[NodeId, Set[NodeId]] = {}
        self.depth: Dict[NodeId, int] = {}
        self._ancestors_cache: Dict[Tuple[NodeId, bool], FrozenSet[NodeId]] = {}
        self._next_id: int = 0

    def add_node(self, parents: Iterable[NodeId] = ()) -> NodeId:
        parent_set = set(parents)
        unknown = parent_set.difference(self.parents)
        if unknown:
            raise ValueError(f"unknown parent node(s): {sorted(unknown)}")
        node = self._next_id
        self._next_id += 1
        self.parents[node] = set(parent_set)
        self.children[node] = set()
        for p in parent_set:
            self.children[p].add(node)
        self.depth[node] = 0 if not parent_set else 1 + max(self.depth[p] for p in parent_set)
        self._ancestors_cache.clear()
        return node

    @property
    def nodes(self) -> Tuple[NodeId, ...]:
        return tuple(sorted(self.parents))

    @property
    def edges(self) -> Tuple[Tuple[NodeId, NodeId], ...]:
        return tuple(sorted((p, c) for c, ps in self.parents.items() for p in ps))

    def maximal_nodes(self) -> Tuple[NodeId, ...]:
        return tuple(n for n in self.nodes if not self.children[n])

    def ancestors(self, node: NodeId, include_self: bool = False) -> FrozenSet[NodeId]:
        self._require_node(node)
        key = (node, include_self)
        cached = self._ancestors_cache.get(key)
        if cached is not None:
            return cached
        out: Set[NodeId] = {node} if include_self else set()
        stack = list(self.parents[node])
        while stack:
            p = stack.pop()
            if p not in out:
                out.add(p)
                stack.extend(self.parents[p])
        result = frozenset(out)
        self._ancestors_cache[key] = result
        return result

    def descendants(self, node: NodeId, include_self: bool = False) -> FrozenSet[NodeId]:
        self._require_node(node)
        out: Set[NodeId] = {node} if include_self else set()
        stack = list(self.children[node])
        while stack:
            c = stack.pop()
            if c not in out:
                out.add(c)
                stack.extend(self.children[c])
        return frozenset(out)

    def reachable(self, src: NodeId, dst: NodeId) -> bool:
        """Reflexive/transitive reachability: src lies in the causal past of dst."""
        self._require_node(src)
        self._require_node(dst)
        return src == dst or src in self.ancestors(dst)

    def candidate_past_from_support(self, support: Iterable[NodeId]) -> FrozenSet[NodeId]:
        """Smallest down-closed past generated by a proposed support set."""
        past: Set[NodeId] = set()
        for s in support:
            self._require_node(s)
            past.update(self.ancestors(s, include_self=True))
        return frozenset(past)

    def is_down_closed(self, past: Iterable[NodeId]) -> bool:
        pset = set(past)
        unknown = pset.difference(self.parents)
        if unknown:
            raise ValueError(f"unknown past node(s): {sorted(unknown)}")
        for y in list(pset):
            if not self.ancestors(y).issubset(pset):
                return False
        return True

    def hasse_frontier(self, past: Iterable[NodeId]) -> SupportCut:
        """Maximal vertices of a downset under reflexive reachability."""
        pset = frozenset(past)
        unknown = set(pset).difference(self.parents)
        if unknown:
            raise ValueError(f"unknown past node(s): {sorted(unknown)}")
        if not self.is_down_closed(pset):
            raise ValueError("Hasse frontier requires a down-closed candidate past")
        frontier = {
            v for v in pset
            if not any(v != w and self.reachable(v, w) for w in pset)
        }
        return frozenset(frontier)

    def support_cut_of_finite_hasse_frontier(self, past: Iterable[NodeId]) -> SupportCut:
        """Python counterpart of `supportCutOfFiniteHasseFrontier`."""
        return self.hasse_frontier(past)

    def ready_at(self, support_cut: SupportCut, site: NodeId) -> bool:
        """Python counterpart of `GraphReadyAt`."""
        self._require_node(site)
        for y in support_cut:
            self._require_node(y)
        return all(self.reachable(y, site) for y in support_cut)

    def finalized_at_depth(self, support_cut: SupportCut, min_depth: int) -> bool:
        """Depth-indexed finality: all sites at depth >= min_depth are ready."""
        return all(
            self.ready_at(support_cut, x)
            for x, d in self.depth.items()
            if d >= min_depth
        )

    def _require_node(self, node: NodeId) -> None:
        if node not in self.parents:
            raise ValueError(f"unknown node: {node}")


class GraphSupportCertifier:
    """Concrete instantiation of `CommitContext.supports`.

    A support cut is certified for a motif when the finite cut is graph-native,
    matches the motif's declared cut, is the Hasse frontier of the motif's
    declared candidate past, reaches every carrier vertex, and passes explicit
    metadata gates for future BDG/local-ledger/orientation attachments.

    This class is a simulator-level operationalization, not a Lean theorem.
    """

    def __init__(
        self,
        dag: CausalDAG,
        *,
        require_hasse_frontier: bool = True,
        require_support_reaches_carrier: bool = True,
        max_support_width: Optional[int] = None,
        max_depth_span: Optional[int] = None,
        allow_empty_support_for_kinds: Sequence[str] = ("seed",),
        require_bdg_gate: bool = True,
        require_ledger_gate: bool = True,
        require_orientation_gate: bool = True,
    ) -> None:
        self.dag = dag
        self.require_hasse_frontier = require_hasse_frontier
        self.require_support_reaches_carrier = require_support_reaches_carrier
        self.max_support_width = max_support_width
        self.max_depth_span = max_depth_span
        self.allow_empty_support_for_kinds = tuple(allow_empty_support_for_kinds)
        self.require_bdg_gate = require_bdg_gate
        self.require_ledger_gate = require_ledger_gate
        self.require_orientation_gate = require_orientation_gate

    def supports(self, motif: MotifCandidate, support_cut: SupportCut) -> bool:
        return self.evaluate(motif, support_cut).supported

    def evaluate(self, motif: MotifCandidate, support_cut: SupportCut) -> SupportEvaluation:
        gates: List[SupportGateResult] = []

        def gate(name: str, passed: bool, detail: str = "") -> None:
            gates.append(SupportGateResult(name, bool(passed), detail))

        gate("motif_certified_flag", motif.certified, f"certified={motif.certified}")

        known_carrier = self._all_known(motif.carrier)
        gate("known_carrier_vertices", known_carrier, f"carrier={sorted(motif.carrier)}")

        known_support = self._all_known(support_cut)
        gate("known_support_vertices", known_support, f"support_cut={sorted(support_cut)}")

        declared_cut_ok = motif.support_cut == support_cut
        gate(
            "support_cut_matches_declared",
            declared_cut_ok,
            f"declared={sorted(motif.support_cut)} supplied={sorted(support_cut)}",
        )

        empty_ok = bool(support_cut) or motif.kind in self.allow_empty_support_for_kinds
        gate("empty_support_allowed", empty_ok, f"kind={motif.kind}")

        if self.max_support_width is not None:
            width_ok = len(support_cut) <= self.max_support_width
            gate("support_width_bound", width_ok, f"width={len(support_cut)} max={self.max_support_width}")

        if self.max_depth_span is not None and support_cut:
            span = max(self.dag.depth[y] for y in support_cut) - min(self.dag.depth[y] for y in support_cut)
            span_ok = span <= self.max_depth_span
            gate("support_depth_span_bound", span_ok, f"span={span} max={self.max_depth_span}")
        elif self.max_depth_span is not None:
            gate("support_depth_span_bound", True, "empty support has span 0")

        candidate_past = self._candidate_past_from_metadata(motif)
        if self.require_hasse_frontier:
            has_past = candidate_past is not None
            gate("candidate_past_declared", has_past, "metadata.candidate_past present" if has_past else "missing metadata.candidate_past")
            if candidate_past is not None:
                known_past = self._all_known(candidate_past)
                gate("candidate_past_vertices_known", known_past, f"candidate_past={sorted(candidate_past)}")
                if known_past:
                    try:
                        down_closed = self.dag.is_down_closed(candidate_past)
                    except ValueError as exc:
                        down_closed = False
                        detail = str(exc)
                    else:
                        detail = f"size={len(candidate_past)}"
                    gate("candidate_past_down_closed", down_closed, detail)
                    if down_closed:
                        frontier = self.dag.support_cut_of_finite_hasse_frontier(candidate_past)
                        frontier_ok = frontier == support_cut
                        gate(
                            "support_cut_is_hasse_frontier",
                            frontier_ok,
                            f"frontier={sorted(frontier)} supplied={sorted(support_cut)}",
                        )
                    else:
                        gate("support_cut_is_hasse_frontier", False, "candidate past not down-closed")
                else:
                    gate("candidate_past_down_closed", False, "candidate past has unknown vertices")
                    gate("support_cut_is_hasse_frontier", False, "candidate past has unknown vertices")

        if self.require_support_reaches_carrier:
            if known_carrier and known_support:
                bad_pairs = [
                    (y, c)
                    for y in support_cut
                    for c in motif.carrier
                    if not self.dag.reachable(y, c)
                ]
                gate("support_reaches_carrier", not bad_pairs, f"bad_pairs={bad_pairs[:6]}")
            else:
                gate("support_reaches_carrier", False, "unknown carrier/support vertex")

        if self.require_bdg_gate:
            ok = bool(motif.metadata.get("bdg_local_ok", True))
            gate("bdg_local_gate", ok, f"bdg_local_ok={ok}")

        if self.require_ledger_gate:
            ok = bool(motif.metadata.get("ledger_local_ok", True))
            gate("ledger_local_gate", ok, f"ledger_local_ok={ok}")

        if self.require_orientation_gate:
            ok = bool(motif.metadata.get("orientation_closure_ok", True))
            gate("orientation_closure_gate", ok, f"orientation_closure_ok={ok}")

        supported = all(g.passed for g in gates)
        return SupportEvaluation(
            motif=motif.name,
            support_cut=tuple(sorted(support_cut)),
            supported=supported,
            gates=tuple(gates),
        )

    def _all_known(self, vertices: Iterable[NodeId]) -> bool:
        return all(v in self.dag.parents for v in vertices)

    @staticmethod
    def _candidate_past_from_metadata(motif: MotifCandidate) -> Optional[FrozenSet[NodeId]]:
        raw = motif.metadata.get("candidate_past")
        if raw is None:
            return None
        if isinstance(raw, (list, tuple, set, frozenset)):
            return frozenset(int(x) for x in raw)
        raise TypeError("metadata.candidate_past must be list/tuple/set/frozenset of node IDs")


class CommitContext:
    """Certified support and incompatibility context for motif commit."""

    def __init__(
        self,
        supports: Optional[Callable[[MotifCandidate, SupportCut], bool]] = None,
        incompatible: Optional[Callable[[MotifCandidate, MotifCandidate], bool]] = None,
        support_certifier: Optional[GraphSupportCertifier] = None,
    ) -> None:
        if supports is not None and support_certifier is not None:
            raise ValueError("provide either supports callable or support_certifier, not both")
        self.support_certifier = support_certifier
        self._supports = supports or (support_certifier.supports if support_certifier is not None else self.default_supports)
        self.incompatible = incompatible or self.default_incompatible

    def supports(self, motif: MotifCandidate, support_cut: SupportCut) -> bool:
        return self._supports(motif, support_cut)

    def evaluate_support(self, motif: MotifCandidate, support_cut: SupportCut) -> SupportEvaluation:
        if self.support_certifier is not None:
            return self.support_certifier.evaluate(motif, support_cut)
        supported = self.supports(motif, support_cut)
        return SupportEvaluation(
            motif=motif.name,
            support_cut=tuple(sorted(support_cut)),
            supported=supported,
            gates=(SupportGateResult("default_supports", supported, "motif.certified and declared cut equality"),),
        )

    @staticmethod
    def default_supports(motif: MotifCandidate, support_cut: SupportCut) -> bool:
        return motif.certified and motif.support_cut == support_cut

    @staticmethod
    def default_incompatible(a: MotifCandidate, b: MotifCandidate) -> bool:
        return (
            a.name != b.name
            and a.exclusion_domain is not None
            and a.exclusion_domain == b.exclusion_domain
        )


class SelectorPolicy:
    """Downstream selector closure over certified-ready motif candidates.

    Modes:
      - none: select every eligible motif; this reproduces strict blocking when
        incompatible eligible candidates remain selected.
      - greedy: build a deterministic compatible subset of eligible motifs.

    Tie policies for greedy mode:
      - lexicographic: use priority, support width, kind rank, and name as a
        deterministic total order.
      - stalemate: if the top-ranked alternatives in a connected incompatibility
        component are tied before name-breaking and mutually incompatible, select
        none from that component and record a stalemate.

    The selector is an experimental downstream layer. It is not part of the
    compiled RA_MotifCommitProtocol interface; it is meant to explore how
    RA_ActualizationSelector-style closure could feed that interface.
    """

    def __init__(self, mode: str = "greedy", tie_policy: str = "lexicographic") -> None:
        if mode not in {"none", "greedy"}:
            raise ValueError("mode must be 'none' or 'greedy'")
        if tie_policy not in {"lexicographic", "stalemate"}:
            raise ValueError("tie_policy must be 'lexicographic' or 'stalemate'")
        self.mode = mode
        self.tie_policy = tie_policy

    def select(
        self,
        *,
        site: NodeId,
        candidates: Sequence[MotifCandidate],
        context: CommitContext,
    ) -> SelectorClosureResult:
        eligible = tuple(sorted(candidates, key=lambda m: m.name))
        if self.mode == "none":
            component = SelectorComponentTrace(
                component_id=0,
                candidates=tuple(m.name for m in eligible),
                selected=tuple(m.name for m in eligible),
                rejected=(),
                stalemate=False,
                reason="selector_disabled_all_eligible_selected",
            )
            return SelectorClosureResult(
                site=site,
                mode=self.mode,
                tie_policy=self.tie_policy,
                eligible=tuple(m.name for m in eligible),
                selected=tuple(m.name for m in eligible),
                rejected=(),
                stalemates=(),
                components=(component,) if eligible else (),
            )

        components = self._conflict_components(eligible, context)
        selected_names: List[str] = []
        rejected_names: List[str] = []
        stalemate_names: List[str] = []
        traces: List[SelectorComponentTrace] = []

        for idx, comp in enumerate(components):
            comp_sorted = tuple(sorted(comp, key=lambda m: m.name))
            if len(comp_sorted) == 1:
                m = comp_sorted[0]
                selected_names.append(m.name)
                traces.append(SelectorComponentTrace(
                    component_id=idx,
                    candidates=(m.name,),
                    selected=(m.name,),
                    rejected=(),
                    stalemate=False,
                    reason="singleton_component_selected",
                ))
                continue

            if self.tie_policy == "stalemate":
                top = self._top_pre_name_rank_group(comp_sorted)
                if len(top) > 1 and self._contains_incompatible_pair(top, context):
                    names = tuple(m.name for m in sorted(comp_sorted, key=lambda m: m.name))
                    rejected_names.extend(names)
                    stalemate_names.extend(names)
                    traces.append(SelectorComponentTrace(
                        component_id=idx,
                        candidates=names,
                        selected=(),
                        rejected=names,
                        stalemate=True,
                        reason="top_rank_tie_without_selector_break",
                    ))
                    continue

            local_selected: List[MotifCandidate] = []
            local_rejected: List[MotifCandidate] = []
            for motif in sorted(comp_sorted, key=self._total_order_key):
                if all(not self._incompatible_symmetric(motif, chosen, context) for chosen in local_selected):
                    local_selected.append(motif)
                else:
                    local_rejected.append(motif)

            selected_names.extend(m.name for m in local_selected)
            rejected_names.extend(m.name for m in local_rejected)
            traces.append(SelectorComponentTrace(
                component_id=idx,
                candidates=tuple(m.name for m in comp_sorted),
                selected=tuple(m.name for m in sorted(local_selected, key=lambda m: m.name)),
                rejected=tuple(m.name for m in sorted(local_rejected, key=lambda m: m.name)),
                stalemate=False,
                reason="greedy_compatible_subset_selected",
            ))

        return SelectorClosureResult(
            site=site,
            mode=self.mode,
            tie_policy=self.tie_policy,
            eligible=tuple(m.name for m in eligible),
            selected=tuple(sorted(selected_names)),
            rejected=tuple(sorted(rejected_names)),
            stalemates=tuple(sorted(stalemate_names)),
            components=tuple(traces),
        )

    @staticmethod
    def _incompatible_symmetric(a: MotifCandidate, b: MotifCandidate, context: CommitContext) -> bool:
        return context.incompatible(a, b) or context.incompatible(b, a)

    def _conflict_components(
        self,
        candidates: Sequence[MotifCandidate],
        context: CommitContext,
    ) -> List[Tuple[MotifCandidate, ...]]:
        remaining = set(range(len(candidates)))
        components: List[Tuple[MotifCandidate, ...]] = []
        while remaining:
            start = remaining.pop()
            stack = [start]
            comp_indices = {start}
            while stack:
                i = stack.pop()
                for j in list(remaining):
                    if self._incompatible_symmetric(candidates[i], candidates[j], context):
                        remaining.remove(j)
                        comp_indices.add(j)
                        stack.append(j)
            components.append(tuple(candidates[i] for i in sorted(comp_indices, key=lambda k: candidates[k].name)))
        return sorted(components, key=lambda comp: tuple(m.name for m in comp))

    @staticmethod
    def _kind_rank(kind: str) -> int:
        # Lower is preferred after priority and support width.
        return {
            "seed": 0,
            "renewal": 1,
            "alternative": 2,
            "generic": 3,
        }.get(kind, 4)

    def _rank_without_name(self, motif: MotifCandidate) -> Tuple[int, int, int]:
        # Higher priority is better; smaller support width is treated as a more
        # parsimonious support boundary; kind rank gives stable domain ordering.
        return (-motif.priority, len(motif.support_cut), self._kind_rank(motif.kind))

    def _total_order_key(self, motif: MotifCandidate) -> Tuple[int, int, int, str]:
        return (*self._rank_without_name(motif), motif.name)

    def _top_pre_name_rank_group(self, candidates: Sequence[MotifCandidate]) -> Tuple[MotifCandidate, ...]:
        ordered = sorted(candidates, key=self._rank_without_name)
        if not ordered:
            return ()
        best_key = self._rank_without_name(ordered[0])
        return tuple(m for m in ordered if self._rank_without_name(m) == best_key)

    def _contains_incompatible_pair(self, candidates: Sequence[MotifCandidate], context: CommitContext) -> bool:
        for i, a in enumerate(candidates):
            for b in candidates[i + 1:]:
                if self._incompatible_symmetric(a, b, context):
                    return True
        return False


class MotifCommitProtocol:
    """Strict and selector-closed RA motif-commit semantics over a CausalDAG."""

    def __init__(self, dag: CausalDAG, motifs: Sequence[MotifCandidate], context: Optional[CommitContext] = None) -> None:
        self.dag = dag
        self.motifs = list(motifs)
        self.context = context or CommitContext()
        self._support_eval_cache: Dict[str, SupportEvaluation] = {}

    def support_evaluation(self, motif: MotifCandidate) -> SupportEvaluation:
        cached = self._support_eval_cache.get(motif.name)
        if cached is not None:
            return cached
        evaluation = self.context.evaluate_support(motif, motif.support_cut)
        self._support_eval_cache[motif.name] = evaluation
        return evaluation

    def supported(self, motif: MotifCandidate) -> bool:
        return self.support_evaluation(motif).supported

    def ready(self, motif: MotifCandidate, site: NodeId) -> bool:
        return self.dag.ready_at(motif.support_cut, site)

    def eligible_at(self, site: NodeId) -> Tuple[MotifCandidate, ...]:
        """Certified-ready motifs at a site."""
        return tuple(m for m in self.motifs if self.supported(m) and self.ready(m, site))

    def blockers(self, motif: MotifCandidate, site: NodeId) -> Tuple[MotifCandidate, ...]:
        if not self.supported(motif) or not self.ready(motif, site):
            return ()
        blocked_by: List[MotifCandidate] = []
        for other in self.motifs:
            if other.name == motif.name:
                continue
            if not self.supported(other):
                continue
            if not self.ready(other, site):
                continue
            if self.context.incompatible(motif, other):
                blocked_by.append(other)
        return tuple(blocked_by)

    def decision(self, motif: MotifCandidate, site: NodeId) -> CommitDecision:
        """Strict counterpart of `GraphCommitsAt`."""
        evaluation = self.support_evaluation(motif)
        supported = evaluation.supported
        ready = self.ready(motif, site) if supported else False
        blocked = self.blockers(motif, site) if supported and ready else ()
        return CommitDecision(
            motif=motif.name,
            site=site,
            supported=supported,
            ready=ready,
            commits=supported and ready and not blocked,
            blocked_by=tuple(b.name for b in blocked),
            support_failures=evaluation.failed_gates,
        )

    def decisions_at(self, site: NodeId) -> Tuple[CommitDecision, ...]:
        return tuple(self.decision(m, site) for m in self.motifs)

    def committed_at(self, site: NodeId) -> Tuple[MotifCandidate, ...]:
        return tuple(m for m in self.motifs if self.decision(m, site).commits)

    def selector_closure_at(self, site: NodeId, selector: Optional[SelectorPolicy] = None) -> SelectorClosureResult:
        selector = selector or SelectorPolicy()
        return selector.select(site=site, candidates=self.eligible_at(site), context=self.context)

    def selected_blockers(
        self,
        motif: MotifCandidate,
        site: NodeId,
        closure: SelectorClosureResult,
    ) -> Tuple[MotifCandidate, ...]:
        if motif.name not in closure.selected_set():
            return ()
        selected_names = closure.selected_set()
        selected_motifs = [m for m in self.motifs if m.name in selected_names and m.name != motif.name]
        return tuple(m for m in selected_motifs if self.context.incompatible(motif, m))

    def selected_decision(
        self,
        motif: MotifCandidate,
        site: NodeId,
        selector: Optional[SelectorPolicy] = None,
        closure: Optional[SelectorClosureResult] = None,
    ) -> SelectedCommitDecision:
        strict = self.decision(motif, site)
        closure = closure or self.selector_closure_at(site, selector)
        selected = motif.name in closure.selected_set()
        selected_blocked = self.selected_blockers(motif, site, closure) if selected else ()

        if not strict.supported:
            selector_reason = "not_supported"
        elif not strict.ready:
            selector_reason = "not_ready"
        elif selected and not selected_blocked:
            selector_reason = "selected"
        elif selected and selected_blocked:
            selector_reason = "selected_but_blocked_by_selected_competitor"
        elif motif.name in closure.stalemate_set():
            selector_reason = "selector_stalemate"
        elif motif.name in closure.rejected_set():
            selector_reason = "rejected_by_selector"
        else:
            selector_reason = "not_eligible"

        return SelectedCommitDecision(
            motif=motif.name,
            site=site,
            supported=strict.supported,
            ready=strict.ready,
            selected=selected,
            commits=strict.supported and strict.ready and selected and not selected_blocked,
            selector_reason=selector_reason,
            strict_blocked_by=strict.blocked_by,
            selected_blocked_by=tuple(b.name for b in selected_blocked),
            support_failures=strict.support_failures,
        )

    def selected_decisions_at(self, site: NodeId, selector: Optional[SelectorPolicy] = None) -> Tuple[SelectedCommitDecision, ...]:
        closure = self.selector_closure_at(site, selector)
        return tuple(self.selected_decision(m, site, selector, closure) for m in self.motifs)

    def selected_committed_at(self, site: NodeId, selector: Optional[SelectorPolicy] = None) -> Tuple[MotifCandidate, ...]:
        decisions = self.selected_decisions_at(site, selector)
        committed_names = {d.motif for d in decisions if d.commits}
        return tuple(m for m in self.motifs if m.name in committed_names)


def _metadata_with_gates(
    *,
    rng: random.Random,
    candidate_past: Iterable[NodeId],
    parents: Iterable[NodeId],
    defect_rate: float,
    past_size: Optional[int] = None,
) -> Dict[str, object]:
    metadata: Dict[str, object] = {
        "candidate_past": sorted(candidate_past),
        "parents": sorted(parents),
        "past_size": past_size if past_size is not None else len(set(candidate_past)),
        "bdg_local_ok": True,
        "ledger_local_ok": True,
        "orientation_closure_ok": True,
        "defect_tags": [],
    }
    if defect_rate > 0 and rng.random() < defect_rate:
        tag = rng.choice(["bdg_local_ok", "ledger_local_ok", "orientation_closure_ok"])
        metadata[tag] = False
        metadata["defect_tags"] = [tag]
    return metadata


def make_context(
    dag: CausalDAG,
    *,
    max_support_width: Optional[int] = None,
    max_depth_span: Optional[int] = None,
) -> CommitContext:
    certifier = GraphSupportCertifier(
        dag,
        require_hasse_frontier=True,
        require_support_reaches_carrier=True,
        max_support_width=max_support_width,
        max_depth_span=max_depth_span,
        require_bdg_gate=True,
        require_ledger_gate=True,
        require_orientation_gate=True,
    )
    return CommitContext(support_certifier=certifier)


def generate_growth_demo(
    steps: int = 24,
    seed: int = 17,
    max_parents: int = 3,
    conflict_rate: float = 0.30,
    defect_rate: float = 0.12,
    max_support_width: Optional[int] = None,
    max_depth_span: Optional[int] = None,
    selector_mode: str = "greedy",
    selector_tie_policy: str = "lexicographic",
) -> Tuple[CausalDAG, List[MotifCandidate], List[dict[str, object]], List[dict[str, object]], List[dict[str, object]]]:
    """Generate a small append-only RA causal-DAG and motif-candidate stream.

    The demo includes three separate behaviors:
      1. certified-ready incompatible alternatives block each other under the
         strict Lean-style `CommitsAt` predicate;
      2. support-certification defects fail before readiness/commit is evaluated;
      3. selector closure can narrow certified-ready alternatives before commit.
    """
    rng = random.Random(seed)
    dag = CausalDAG()
    genesis = dag.add_node()
    motifs: List[MotifCandidate] = []
    rows: List[dict[str, object]] = []
    support_rows: List[dict[str, object]] = []
    selector_rows: List[dict[str, object]] = []
    selector = SelectorPolicy(mode=selector_mode, tie_policy=selector_tie_policy)

    motifs.append(MotifCandidate(
        name="genesis_seed",
        carrier=frozenset({genesis}),
        support_cut=frozenset(),
        kind="seed",
        exclusion_domain=None,
        metadata={
            "candidate_past": [],
            "parents": [],
            "past_size": 0,
            "bdg_local_ok": True,
            "ledger_local_ok": True,
            "orientation_closure_ok": True,
            "defect_tags": [],
        },
    ))

    for _ in range(steps):
        existing = list(dag.nodes)
        frontier = list(dag.maximal_nodes()) or existing
        parent_pool = frontier if len(frontier) >= 1 else existing
        k = rng.randint(1, min(max_parents, len(parent_pool)))
        parents = set(rng.sample(parent_pool, k=k))

        if len(existing) > 2 and rng.random() < 0.35:
            parents.add(rng.choice(existing))

        site = dag.add_node(parents)
        past = dag.candidate_past_from_support(parents)
        support_cut = dag.support_cut_of_finite_hasse_frontier(past)

        stable_metadata = _metadata_with_gates(
            rng=rng,
            candidate_past=past,
            parents=parents,
            defect_rate=defect_rate * 0.35,
            past_size=len(past),
        )
        stable = MotifCandidate(
            name=f"renewal_{site}",
            carrier=frozenset({site}),
            support_cut=support_cut,
            kind="renewal",
            exclusion_domain=None,
            priority=2,
            metadata={**stable_metadata, "support_width": len(support_cut)},
        )
        motifs.append(stable)

        introduced_conflict = rng.random() < conflict_rate
        if introduced_conflict:
            domain = f"choice_at_{site}"
            a_metadata = _metadata_with_gates(
                rng=rng,
                candidate_past=past,
                parents=parents,
                defect_rate=defect_rate,
                past_size=len(past),
            )
            b_metadata = _metadata_with_gates(
                rng=rng,
                candidate_past=past,
                parents=parents,
                defect_rate=defect_rate,
                past_size=len(past),
            )
            # Usually equal priority, so lexicographic selector breaks symmetry;
            # a future stochastic/physical selector could replace this.
            motifs.append(MotifCandidate(
                name=f"choice_A_{site}",
                carrier=frozenset({site}),
                support_cut=support_cut,
                kind="alternative",
                exclusion_domain=domain,
                priority=1,
                metadata={**a_metadata, "support_width": len(support_cut)},
            ))
            motifs.append(MotifCandidate(
                name=f"choice_B_{site}",
                carrier=frozenset({site}),
                support_cut=support_cut,
                kind="alternative",
                exclusion_domain=domain,
                priority=1,
                metadata={**b_metadata, "support_width": len(support_cut)},
            ))

        context = make_context(dag, max_support_width=max_support_width, max_depth_span=max_depth_span)
        protocol = MotifCommitProtocol(dag, motifs, context)
        strict_decisions = protocol.decisions_at(site)
        closure = protocol.selector_closure_at(site, selector)
        selected_decisions = tuple(protocol.selected_decision(m, site, selector, closure) for m in motifs)

        strict_committed = [d.motif for d in strict_decisions if d.commits]
        strict_blocked = [d.motif for d in strict_decisions if d.ready and not d.commits and d.blocked_by]
        unsupported = [d.motif for d in strict_decisions if not d.supported]
        selected_committed = [d.motif for d in selected_decisions if d.commits]
        selector_rejected = [d.motif for d in selected_decisions if d.selector_reason == "rejected_by_selector"]
        selector_stalemates = [d.motif for d in selected_decisions if d.selector_reason == "selector_stalemate"]
        selected_blocked = [d.motif for d in selected_decisions if d.selected_blocked_by]

        for motif in motifs:
            evaluation = protocol.support_evaluation(motif)
            row = evaluation.to_row()
            row["site"] = site
            support_rows.append(row)

        for component_row in closure.component_rows():
            component_row["selector_mode"] = selector.mode
            component_row["selector_tie_policy"] = selector.tie_policy
            selector_rows.append(component_row)

        failure_histogram: Dict[str, int] = {}
        for d in strict_decisions:
            for failure in d.support_failures:
                failure_histogram[failure] = failure_histogram.get(failure, 0) + 1

        rows.append({
            "site": site,
            "depth": dag.depth[site],
            "parents": sorted(parents),
            "candidate_past_size": len(past),
            "hasse_frontier_support_cut": sorted(support_cut),
            "support_width": len(support_cut),
            "introduced_conflict": introduced_conflict,
            "selector_mode": selector.mode,
            "selector_tie_policy": selector.tie_policy,
            "eligible_count": len(closure.eligible),
            "selected_count": len(closure.selected),
            "strict_ready_count": sum(1 for d in strict_decisions if d.ready),
            "strict_supported_count": sum(1 for d in strict_decisions if d.supported),
            "unsupported_count": len(unsupported),
            "strict_committed_count": len(strict_committed),
            "strict_blocked_count": len(strict_blocked),
            "selector_committed_count": len(selected_committed),
            "selector_rejected_count": len(selector_rejected),
            "selector_stalemate_count": len(selector_stalemates),
            "selector_selected_blocked_count": len(selected_blocked),
            "strict_committed_motifs": strict_committed,
            "strict_blocked_ready_motifs": strict_blocked,
            "selector_committed_motifs": selected_committed,
            "selector_rejected_motifs": selector_rejected,
            "selector_stalemate_motifs": selector_stalemates,
            "unsupported_motifs": unsupported,
            "support_failure_histogram": failure_histogram,
        })

    return dag, motifs, rows, support_rows, selector_rows


def summarize_run(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    if not rows:
        return {
            "sites": 0,
            "total_strict_committed": 0,
            "total_strict_blocked": 0,
            "total_selector_committed": 0,
            "total_selector_rejected": 0,
            "total_selector_stalemates": 0,
            "total_unsupported": 0,
            "mean_support_width": 0.0,
        }
    total_strict_committed = sum(int(r.get("strict_committed_count", 0)) for r in rows)
    total_strict_blocked = sum(int(r.get("strict_blocked_count", 0)) for r in rows)
    total_selector_committed = sum(int(r.get("selector_committed_count", 0)) for r in rows)
    total_selector_rejected = sum(int(r.get("selector_rejected_count", 0)) for r in rows)
    total_selector_stalemates = sum(int(r.get("selector_stalemate_count", 0)) for r in rows)
    total_unsupported = sum(int(r.get("unsupported_count", 0)) for r in rows)
    mean_width = sum(int(r.get("support_width", 0)) for r in rows) / len(rows)
    return {
        "sites": len(rows),
        "total_strict_committed": total_strict_committed,
        "total_strict_blocked": total_strict_blocked,
        "total_selector_committed": total_selector_committed,
        "total_selector_rejected": total_selector_rejected,
        "total_selector_stalemates": total_selector_stalemates,
        "total_unsupported": total_unsupported,
        "mean_support_width": round(mean_width, 4),
        "last_site": rows[-1].get("site"),
    }


def run_parameter_sweep(
    *,
    seeds: Sequence[int] = (11, 17),
    conflict_rates: Sequence[float] = (0.0, 0.30),
    defect_rates: Sequence[float] = (0.0, 0.10),
    selector_modes: Sequence[str] = ("none", "greedy"),
    selector_tie_policies: Sequence[str] = ("lexicographic", "stalemate"),
    steps: int = 24,
    max_parents: int = 3,
    max_support_width: Optional[int] = None,
    max_depth_span: Optional[int] = None,
) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for selector_mode in selector_modes:
        for selector_tie_policy in selector_tie_policies:
            for conflict_rate in conflict_rates:
                for defect_rate in defect_rates:
                    for seed in seeds:
                        dag, motifs, rows, _support_rows, _selector_rows = generate_growth_demo(
                            steps=steps,
                            seed=seed,
                            max_parents=max_parents,
                            conflict_rate=conflict_rate,
                            defect_rate=defect_rate,
                            max_support_width=max_support_width,
                            max_depth_span=max_depth_span,
                            selector_mode=selector_mode,
                            selector_tie_policy=selector_tie_policy,
                        )
                        summary = summarize_run(rows)
                        out.append({
                            "seed": seed,
                            "steps": steps,
                            "nodes": len(dag.nodes),
                            "edges": len(dag.edges),
                            "motifs": len(motifs),
                            "conflict_rate": conflict_rate,
                            "defect_rate": defect_rate,
                            "selector_mode": selector_mode,
                            "selector_tie_policy": selector_tie_policy,
                            "max_support_width": max_support_width,
                            "max_depth_span": max_depth_span,
                            **summary,
                        })
    return out


def rows_to_csv(rows: Sequence[Mapping[str, object]], path: Path, fieldnames: Optional[Sequence[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: List[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for key, value in list(out.items()):
                if isinstance(value, (list, tuple, dict, set, frozenset)):
                    out[key] = json.dumps(value, sort_keys=True)
            writer.writerow(out)


def dump_state_json(
    dag: CausalDAG,
    motifs: Sequence[MotifCandidate],
    rows: Sequence[Mapping[str, object]],
    support_rows: Sequence[Mapping[str, object]],
    selector_rows: Sequence[Mapping[str, object]],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "0.3",
        "nodes": list(dag.nodes),
        "edges": [list(e) for e in dag.edges],
        "depth": {str(k): v for k, v in dag.depth.items()},
        "motifs": [
            {
                "name": m.name,
                "carrier": sorted(m.carrier),
                "support_cut": sorted(m.support_cut),
                "kind": m.kind,
                "exclusion_domain": m.exclusion_domain,
                "certified": m.certified,
                "priority": m.priority,
                "metadata": dict(m.metadata),
            }
            for m in motifs
        ],
        "site_summaries": list(rows),
        "support_evaluations": list(support_rows),
        "selector_components": list(selector_rows),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the RA causal-DAG motif-commit simulator demo.")
    parser.add_argument('--steps', type=int, default=24)
    parser.add_argument('--seed', type=int, default=17)
    parser.add_argument('--max-parents', type=int, default=3)
    parser.add_argument('--conflict-rate', type=float, default=0.30)
    parser.add_argument('--defect-rate', type=float, default=0.12)
    parser.add_argument('--max-support-width', type=int, default=None)
    parser.add_argument('--max-depth-span', type=int, default=None)
    parser.add_argument('--selector-mode', choices=['none', 'greedy'], default='greedy')
    parser.add_argument('--selector-tie-policy', choices=['lexicographic', 'stalemate'], default='lexicographic')
    parser.add_argument('--csv', type=Path, default=Path('outputs/ra_causal_dag_demo_summary_v0_3.csv'))
    parser.add_argument('--support-csv', type=Path, default=Path('outputs/ra_causal_dag_support_evaluations_v0_3.csv'))
    parser.add_argument('--selector-csv', type=Path, default=Path('outputs/ra_causal_dag_selector_components_v0_3.csv'))
    parser.add_argument('--json', type=Path, default=Path('outputs/ra_causal_dag_demo_state_v0_3.json'))
    parser.add_argument('--sweep-csv', type=Path, default=Path('outputs/ra_causal_dag_parameter_sweep_v0_3.csv'))
    parser.add_argument('--run-sweep', action='store_true')
    args = parser.parse_args()

    dag, motifs, rows, support_rows, selector_rows = generate_growth_demo(
        steps=args.steps,
        seed=args.seed,
        max_parents=args.max_parents,
        conflict_rate=args.conflict_rate,
        defect_rate=args.defect_rate,
        max_support_width=args.max_support_width,
        max_depth_span=args.max_depth_span,
        selector_mode=args.selector_mode,
        selector_tie_policy=args.selector_tie_policy,
    )
    rows_to_csv(rows, args.csv)
    rows_to_csv(support_rows, args.support_csv)
    rows_to_csv(selector_rows, args.selector_csv)
    dump_state_json(dag, motifs, rows, support_rows, selector_rows, args.json)
    print(f"nodes={len(dag.nodes)} edges={len(dag.edges)} motifs={len(motifs)}")
    print(f"summary={summarize_run(rows)}")
    print(f"summary_csv={args.csv}")
    print(f"support_csv={args.support_csv}")
    print(f"selector_csv={args.selector_csv}")
    print(f"state_json={args.json}")
    if rows:
        print("last_site_summary=" + json.dumps(rows[-1], sort_keys=True))

    if args.run_sweep:
        sweep_rows = run_parameter_sweep(
            steps=args.steps,
            max_parents=args.max_parents,
            max_support_width=args.max_support_width,
            max_depth_span=args.max_depth_span,
        )
        rows_to_csv(sweep_rows, args.sweep_csv)
        print(f"sweep_rows={len(sweep_rows)} sweep_csv={args.sweep_csv}")


if __name__ == '__main__':
    main()
