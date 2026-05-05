#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.5

RA-native simulator for motif support, causal readiness, selector closure,
orientation-gated support certification, and causal-severance fragility
diagnostics.

This is an RA-native actualization workbench. The operational vocabulary is:

  candidate motif -> causal support cut -> oriented support witness ->
  certified readiness -> selector closure -> selected commitment -> finality ->
  causal-severance intervention -> fragility / recovery diagnostics.

Lean-to-Python correspondence:

  GraphMotifCandidate                   ↔ MotifCandidate
  GraphSupportCut                       ↔ SupportCut = frozenset[node_id]
  supportCutOfFiniteHasseFrontier       ↔ CausalDAG.support_cut_of_finite_hasse_frontier
  GraphReadyAt                          ↔ CausalDAG.ready_at
  GraphOrientedMotifSupport.certified   ↔ GraphOrientationSupportCertifier.evaluate(...).supported
  GraphOrientationActualizationContext  ↔ OrientationActualizationContext
  GraphSelectedCommitsAt                ↔ MotifCommitProtocol.selected_decision(...).commits
"""
from __future__ import annotations

import argparse
import copy
import csv
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

NodeId = int
SupportCut = FrozenSet[NodeId]


@dataclass(frozen=True)
class MotifCandidate:
    """Finite motif candidate with RA-native support metadata."""

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
            "gate_details": [{"gate": g.gate, "passed": g.passed, "detail": g.detail} for g in self.gates],
        }


@dataclass(frozen=True)
class OrientationLink:
    """Incidence-sign datum used by an orientation-support witness."""

    src: NodeId
    dst: NodeId
    sign: int

    def valid(self, dag: "CausalDAG") -> bool:
        return self.src in dag.parents and self.dst in dag.parents and self.sign in {-1, 1}

    def to_row(self) -> Dict[str, object]:
        return {"src": self.src, "dst": self.dst, "sign": self.sign}


@dataclass(frozen=True)
class OrientationClosureCertificate:
    """Simulator surface of the graph-orientation closure certificate."""

    selector_compatible: bool = True
    no_extra_random_labels: bool = True
    no_particle_label_primitives: bool = True
    qN1_signature: int = 7
    local_conserved: bool = True
    sign_links: Tuple[OrientationLink, ...] = ()

    @staticmethod
    def from_mapping(raw: Mapping[str, object]) -> "OrientationClosureCertificate":
        links: List[OrientationLink] = []
        for item in raw.get("sign_links", ()):  # type: ignore[assignment]
            if isinstance(item, Mapping):
                links.append(OrientationLink(int(item["src"]), int(item["dst"]), int(item["sign"])))
            elif isinstance(item, (list, tuple)) and len(item) == 3:
                links.append(OrientationLink(int(item[0]), int(item[1]), int(item[2])))
            else:
                raise TypeError("sign_links entries must be mappings or triples")
        return OrientationClosureCertificate(
            selector_compatible=bool(raw.get("selector_compatible", True)),
            no_extra_random_labels=bool(raw.get("no_extra_random_labels", True)),
            no_particle_label_primitives=bool(raw.get("no_particle_label_primitives", True)),
            qN1_signature=int(raw.get("qN1_signature", 7)),
            local_conserved=bool(raw.get("local_conserved", True)),
            sign_links=tuple(links),
        )

    def to_row(self) -> Dict[str, object]:
        return {
            "selector_compatible": self.selector_compatible,
            "no_extra_random_labels": self.no_extra_random_labels,
            "no_particle_label_primitives": self.no_particle_label_primitives,
            "qN1_signature": self.qN1_signature,
            "local_conserved": self.local_conserved,
            "sign_links": [x.to_row() for x in self.sign_links],
        }


@dataclass(frozen=True)
class GraphOrientedMotifSupport:
    """Orientation support witness for a motif over a graph-native candidate past."""

    motif: str
    candidate_past: FrozenSet[NodeId]
    support_cut: SupportCut
    closure: OrientationClosureCertificate
    frontier_sufficient_for_motif: bool = True
    local_ledger_compatible: bool = True
    carrier_represented_by_frontier: bool = True

    @staticmethod
    def from_metadata(motif: MotifCandidate) -> Optional["GraphOrientedMotifSupport"]:
        raw = motif.metadata.get("orientation_support_witness")
        if raw is None:
            return None
        if not isinstance(raw, Mapping):
            raise TypeError("orientation_support_witness must be a mapping")
        closure_raw = raw.get("closure", raw)
        if not isinstance(closure_raw, Mapping):
            raise TypeError("orientation_support_witness.closure must be a mapping")
        return GraphOrientedMotifSupport(
            motif=str(raw.get("motif", motif.name)),
            candidate_past=frozenset(int(x) for x in raw.get("candidate_past", motif.metadata.get("candidate_past", ()))),  # type: ignore[arg-type]
            support_cut=frozenset(int(x) for x in raw.get("support_cut", motif.support_cut)),  # type: ignore[arg-type]
            closure=OrientationClosureCertificate.from_mapping(closure_raw),
            frontier_sufficient_for_motif=bool(raw.get("frontier_sufficient_for_motif", True)),
            local_ledger_compatible=bool(raw.get("local_ledger_compatible", True)),
            carrier_represented_by_frontier=bool(raw.get("carrier_represented_by_frontier", True)),
        )

    def to_row(self) -> Dict[str, object]:
        return {
            "motif": self.motif,
            "candidate_past": sorted(self.candidate_past),
            "support_cut": sorted(self.support_cut),
            "frontier_sufficient_for_motif": self.frontier_sufficient_for_motif,
            "local_ledger_compatible": self.local_ledger_compatible,
            "carrier_represented_by_frontier": self.carrier_represented_by_frontier,
            **self.closure.to_row(),
            "sign_link_count": len(self.closure.sign_links),
        }


@dataclass(frozen=True)
class OrientationConflictWitness:
    motif_a: str
    motif_b: str
    conflict_reason: str
    conflict_holds: bool = True

    def to_row(self) -> Dict[str, object]:
        return {
            "motif_a": self.motif_a,
            "motif_b": self.motif_b,
            "conflict_reason": self.conflict_reason,
            "conflict_holds": self.conflict_holds,
        }


@dataclass(frozen=True)
class CommitDecision:
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
    """Append-only finite DAG with edges oriented causal-past -> causal-future."""

    def __init__(self) -> None:
        self.parents: Dict[NodeId, Set[NodeId]] = {}
        self.children: Dict[NodeId, Set[NodeId]] = {}
        self.depth: Dict[NodeId, int] = {}
        self._ancestors_cache: Dict[Tuple[NodeId, bool], FrozenSet[NodeId]] = {}
        self._next_id = 0

    def add_node(self, parents: Iterable[NodeId] = ()) -> NodeId:
        ps = set(parents)
        unknown = ps.difference(self.parents)
        if unknown:
            raise ValueError(f"unknown parent node(s): {sorted(unknown)}")
        node = self._next_id
        self._next_id += 1
        self.parents[node] = set(ps)
        self.children[node] = set()
        for p in ps:
            self.children[p].add(node)
        self.depth[node] = 0 if not ps else 1 + max(self.depth[p] for p in ps)
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
        if key in self._ancestors_cache:
            return self._ancestors_cache[key]
        out: Set[NodeId] = {node} if include_self else set()
        stack = list(self.parents[node])
        while stack:
            p = stack.pop()
            if p not in out:
                out.add(p)
                stack.extend(self.parents[p])
        res = frozenset(out)
        self._ancestors_cache[key] = res
        return res

    def reachable(self, src: NodeId, dst: NodeId) -> bool:
        self._require_node(src)
        self._require_node(dst)
        return src == dst or src in self.ancestors(dst)

    def candidate_past_from_support(self, support: Iterable[NodeId]) -> FrozenSet[NodeId]:
        out: Set[NodeId] = set()
        for s in support:
            self._require_node(s)
            out.update(self.ancestors(s, include_self=True))
        return frozenset(out)

    def is_down_closed(self, past: Iterable[NodeId]) -> bool:
        pset = set(past)
        unknown = pset.difference(self.parents)
        if unknown:
            raise ValueError(f"unknown past node(s): {sorted(unknown)}")
        return all(self.ancestors(y).issubset(pset) for y in pset)

    def hasse_frontier(self, past: Iterable[NodeId]) -> SupportCut:
        pset = frozenset(past)
        unknown = set(pset).difference(self.parents)
        if unknown:
            raise ValueError(f"unknown past node(s): {sorted(unknown)}")
        if not self.is_down_closed(pset):
            raise ValueError("Hasse frontier requires a down-closed candidate past")
        return frozenset(v for v in pset if not any(v != w and self.reachable(v, w) for w in pset))

    def support_cut_of_finite_hasse_frontier(self, past: Iterable[NodeId]) -> SupportCut:
        return self.hasse_frontier(past)

    def ready_at(self, support_cut: SupportCut, site: NodeId) -> bool:
        self._require_node(site)
        for y in support_cut:
            self._require_node(y)
        return all(self.reachable(y, site) for y in support_cut)

    def finalized_at_depth(self, support_cut: SupportCut, min_depth: int) -> bool:
        return all(self.ready_at(support_cut, x) for x, d in self.depth.items() if d >= min_depth)

    def _require_node(self, node: NodeId) -> None:
        if node not in self.parents:
            raise ValueError(f"unknown node: {node}")


class GraphOrientationSupportCertifier:
    """Concrete orientation-gated implementation of Γ.supports."""

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
        require_orientation_witness: bool = True,
        require_qN1_seven: bool = True,
        require_sign_links_cover_support: bool = True,
    ) -> None:
        self.dag = dag
        self.require_hasse_frontier = require_hasse_frontier
        self.require_support_reaches_carrier = require_support_reaches_carrier
        self.max_support_width = max_support_width
        self.max_depth_span = max_depth_span
        self.allow_empty_support_for_kinds = tuple(allow_empty_support_for_kinds)
        self.require_bdg_gate = require_bdg_gate
        self.require_ledger_gate = require_ledger_gate
        self.require_orientation_witness = require_orientation_witness
        self.require_qN1_seven = require_qN1_seven
        self.require_sign_links_cover_support = require_sign_links_cover_support

    def supports(self, motif: MotifCandidate, support_cut: SupportCut) -> bool:
        return self.evaluate(motif, support_cut).supported

    def evaluate(self, motif: MotifCandidate, support_cut: SupportCut) -> SupportEvaluation:
        gates: List[SupportGateResult] = []

        def gate(name: str, passed: bool, detail: str = "") -> None:
            gates.append(SupportGateResult(name, bool(passed), detail))

        gate("motif_certified_flag", motif.certified, f"certified={motif.certified}")
        known_carrier = self._all_known(motif.carrier)
        known_support = self._all_known(support_cut)
        gate("known_carrier_vertices", known_carrier, f"carrier={sorted(motif.carrier)}")
        gate("known_support_vertices", known_support, f"support_cut={sorted(support_cut)}")
        gate("support_cut_matches_declared", motif.support_cut == support_cut, f"declared={sorted(motif.support_cut)} supplied={sorted(support_cut)}")
        gate("empty_support_allowed", bool(support_cut) or motif.kind in self.allow_empty_support_for_kinds, f"kind={motif.kind}")
        if self.max_support_width is not None:
            gate("support_width_bound", len(support_cut) <= self.max_support_width, f"width={len(support_cut)} max={self.max_support_width}")
        if self.max_depth_span is not None:
            if support_cut:
                span = max(self.dag.depth[y] for y in support_cut) - min(self.dag.depth[y] for y in support_cut)
                gate("support_depth_span_bound", span <= self.max_depth_span, f"span={span} max={self.max_depth_span}")
            else:
                gate("support_depth_span_bound", True, "empty support has span 0")

        candidate_past = self._candidate_past_from_metadata(motif)
        if self.require_hasse_frontier:
            gate("candidate_past_declared", candidate_past is not None, "metadata.candidate_past present" if candidate_past is not None else "missing metadata.candidate_past")
            if candidate_past is not None:
                known_past = self._all_known(candidate_past)
                gate("candidate_past_vertices_known", known_past, f"candidate_past={sorted(candidate_past)}")
                down = False
                if known_past:
                    try:
                        down = self.dag.is_down_closed(candidate_past)
                    except ValueError as exc:
                        gate("candidate_past_down_closed", False, str(exc))
                    else:
                        gate("candidate_past_down_closed", down, f"size={len(candidate_past)}")
                else:
                    gate("candidate_past_down_closed", False, "unknown candidate past vertex")
                if known_past and down:
                    frontier = self.dag.support_cut_of_finite_hasse_frontier(candidate_past)
                    gate("support_cut_is_hasse_frontier", frontier == support_cut, f"frontier={sorted(frontier)} supplied={sorted(support_cut)}")
                else:
                    gate("support_cut_is_hasse_frontier", False, "candidate past not available as down-closed past")

        if self.require_support_reaches_carrier:
            if known_carrier and known_support:
                bad = [(y, c) for y in support_cut for c in motif.carrier if not self.dag.reachable(y, c)]
                gate("support_reaches_carrier", not bad, f"bad_pairs={bad[:6]}")
            else:
                gate("support_reaches_carrier", False, "unknown carrier/support vertex")
        if self.require_bdg_gate:
            ok = bool(motif.metadata.get("bdg_local_ok", True))
            gate("bdg_local_gate", ok, f"bdg_local_ok={ok}")
        if self.require_ledger_gate:
            ok = bool(motif.metadata.get("ledger_local_ok", True))
            gate("ledger_local_gate", ok, f"ledger_local_ok={ok}")

        try:
            witness = GraphOrientedMotifSupport.from_metadata(motif)
        except (TypeError, ValueError) as exc:
            witness = None
            gate("orientation_witness_parseable", False, str(exc))
        else:
            gate("orientation_witness_parseable", True, "parsed" if witness is not None else "no witness")

        if witness is None:
            gate("orientation_witness_declared", not self.require_orientation_witness, "missing metadata.orientation_support_witness")
        else:
            self._evaluate_orientation_witness(motif, support_cut, witness, candidate_past, gate)

        supported = all(g.passed for g in gates)
        return SupportEvaluation(motif=motif.name, support_cut=tuple(sorted(support_cut)), supported=supported, gates=tuple(gates))

    def _evaluate_orientation_witness(
        self,
        motif: MotifCandidate,
        support_cut: SupportCut,
        witness: GraphOrientedMotifSupport,
        declared_past: Optional[FrozenSet[NodeId]],
        gate,
    ) -> None:
        gate("orientation_witness_declared", True, "metadata.orientation_support_witness present")
        gate("orientation_witness_names_motif", witness.motif == motif.name, f"witness.motif={witness.motif}")
        gate("orientation_candidate_past_matches_declared", witness.candidate_past == declared_past, f"witness={sorted(witness.candidate_past)} declared={sorted(declared_past or [])}")
        gate("orientation_support_cut_matches_supplied", witness.support_cut == support_cut, f"witness={sorted(witness.support_cut)} supplied={sorted(support_cut)}")
        try:
            frontier = self.dag.support_cut_of_finite_hasse_frontier(witness.candidate_past)
        except (TypeError, ValueError) as exc:
            gate("orientation_witness_hasse_frontier_defined", False, str(exc))
        else:
            gate("orientation_witness_hasse_frontier_defined", True, f"frontier={sorted(frontier)}")
            gate("orientation_support_cut_is_hasse_frontier", frontier == support_cut, f"frontier={sorted(frontier)} supplied={sorted(support_cut)}")

        # Operational proxy: support frontier represents the site-carrier when
        # it reaches every carrier vertex and the witness asserts representation.
        if self._all_known(motif.carrier) and self._all_known(support_cut):
            bad = [(y, c) for y in support_cut for c in motif.carrier if not self.dag.reachable(y, c)]
            carrier_reachable = not bad
        else:
            bad = []
            carrier_reachable = False
        gate("orientation_carrier_represented_by_frontier", witness.carrier_represented_by_frontier and carrier_reachable, f"witness={witness.carrier_represented_by_frontier} bad_pairs={bad[:6]}")
        gate("orientation_frontier_sufficient_for_motif", witness.frontier_sufficient_for_motif, f"frontier_sufficient_for_motif={witness.frontier_sufficient_for_motif}")
        gate("orientation_local_ledger_compatible", witness.local_ledger_compatible, f"local_ledger_compatible={witness.local_ledger_compatible}")
        gate("orientation_selector_compatible", witness.closure.selector_compatible, f"selector_compatible={witness.closure.selector_compatible}")
        gate("orientation_no_extra_random_labels", witness.closure.no_extra_random_labels, f"no_extra_random_labels={witness.closure.no_extra_random_labels}")
        gate("orientation_no_particle_label_primitives", witness.closure.no_particle_label_primitives, f"no_particle_label_primitives={witness.closure.no_particle_label_primitives}")
        gate("orientation_sign_links_valid", all(l.valid(self.dag) for l in witness.closure.sign_links), f"sign_links={len(witness.closure.sign_links)}")
        if self.require_sign_links_cover_support:
            srcs = {l.src for l in witness.closure.sign_links}
            covers = True if not support_cut else set(support_cut).issubset(srcs)
            detail = "empty support" if not support_cut else f"missing_support_sources={sorted(set(support_cut).difference(srcs))}"
            gate("orientation_sign_source_covers_support", covers, detail)
        if self.require_qN1_seven:
            gate("orientation_qN1_seven", witness.closure.qN1_signature == 7, f"qN1_signature={witness.closure.qN1_signature}")
        gate("orientation_local_conserved", witness.closure.local_conserved, f"local_conserved={witness.closure.local_conserved}")

    def orientation_witness_row(self, motif: MotifCandidate) -> Dict[str, object]:
        witness = GraphOrientedMotifSupport.from_metadata(motif)
        if witness is None:
            return {"motif": motif.name, "orientation_witness_declared": False, "support_cut": sorted(motif.support_cut)}
        row = witness.to_row()
        row["orientation_witness_declared"] = True
        return row

    def _all_known(self, vertices: Iterable[NodeId]) -> bool:
        return all(v in self.dag.parents for v in vertices)

    @staticmethod
    def _candidate_past_from_metadata(motif: MotifCandidate) -> Optional[FrozenSet[NodeId]]:
        raw = motif.metadata.get("candidate_past")
        if raw is None:
            return None
        if isinstance(raw, (list, tuple, set, frozenset)):
            return frozenset(int(x) for x in raw)
        raise TypeError("metadata.candidate_past must be a finite iterable of node IDs")


class OrientationActualizationContext:
    """Orientation-gated support and witnessed incompatibility context."""

    def __init__(self, certifier: GraphOrientationSupportCertifier, *, use_orientation_conflicts: bool = True) -> None:
        self.certifier = certifier
        self.use_orientation_conflicts = use_orientation_conflicts

    def supports(self, motif: MotifCandidate, support_cut: SupportCut) -> bool:
        return self.certifier.supports(motif, support_cut)

    def evaluate_support(self, motif: MotifCandidate, support_cut: SupportCut) -> SupportEvaluation:
        return self.certifier.evaluate(motif, support_cut)

    def conflict_witness(self, a: MotifCandidate, b: MotifCandidate) -> Optional[OrientationConflictWitness]:
        if a.name == b.name:
            return None
        domain_a = a.metadata.get("orientation_conflict_domain", a.exclusion_domain)
        domain_b = b.metadata.get("orientation_conflict_domain", b.exclusion_domain)
        if domain_a is None or domain_a != domain_b:
            return None
        holds_a = bool(a.metadata.get("orientation_conflict_ok", True))
        holds_b = bool(b.metadata.get("orientation_conflict_ok", True))
        return OrientationConflictWitness(a.name, b.name, f"shared_orientation_conflict_domain:{domain_a}", holds_a and holds_b)

    def incompatible(self, a: MotifCandidate, b: MotifCandidate) -> bool:
        if not self.use_orientation_conflicts:
            return a.name != b.name and a.exclusion_domain is not None and a.exclusion_domain == b.exclusion_domain
        w = self.conflict_witness(a, b)
        return w.conflict_holds if w is not None else False


class SelectorPolicy:
    """Downstream selector closure over certified-ready motifs."""

    def __init__(self, mode: str = "greedy", tie_policy: str = "lexicographic") -> None:
        if mode not in {"none", "greedy"}:
            raise ValueError("mode must be 'none' or 'greedy'")
        if tie_policy not in {"lexicographic", "stalemate"}:
            raise ValueError("tie_policy must be 'lexicographic' or 'stalemate'")
        self.mode = mode
        self.tie_policy = tie_policy

    def select(self, *, site: NodeId, candidates: Sequence[MotifCandidate], context: OrientationActualizationContext) -> SelectorClosureResult:
        eligible = tuple(sorted(candidates, key=lambda m: m.name))
        if self.mode == "none":
            comp = SelectorComponentTrace(0, tuple(m.name for m in eligible), tuple(m.name for m in eligible), (), False, "selector_disabled_all_eligible_selected")
            return SelectorClosureResult(site, self.mode, self.tie_policy, comp.candidates, comp.selected, (), (), (comp,) if eligible else ())

        components = self._conflict_components(eligible, context)
        selected: List[str] = []
        rejected: List[str] = []
        stalemates: List[str] = []
        traces: List[SelectorComponentTrace] = []
        for idx, comp in enumerate(components):
            comp_sorted = tuple(sorted(comp, key=lambda m: m.name))
            if len(comp_sorted) == 1:
                name = comp_sorted[0].name
                selected.append(name)
                traces.append(SelectorComponentTrace(idx, (name,), (name,), (), False, "singleton_component_selected"))
                continue
            if self.tie_policy == "stalemate":
                top = self._top_pre_name_rank_group(comp_sorted)
                if len(top) > 1 and self._contains_incompatible_pair(top, context):
                    names = tuple(m.name for m in comp_sorted)
                    rejected.extend(names)
                    stalemates.extend(names)
                    traces.append(SelectorComponentTrace(idx, names, (), names, True, "top_rank_tie_without_selector_break"))
                    continue
            local_sel: List[MotifCandidate] = []
            local_rej: List[MotifCandidate] = []
            for m in sorted(comp_sorted, key=self._total_order_key):
                if all(not self._incompatible_symmetric(m, chosen, context) for chosen in local_sel):
                    local_sel.append(m)
                else:
                    local_rej.append(m)
            selected.extend(m.name for m in local_sel)
            rejected.extend(m.name for m in local_rej)
            traces.append(SelectorComponentTrace(idx, tuple(m.name for m in comp_sorted), tuple(sorted(m.name for m in local_sel)), tuple(sorted(m.name for m in local_rej)), False, "greedy_compatible_subset_selected"))
        return SelectorClosureResult(site, self.mode, self.tie_policy, tuple(m.name for m in eligible), tuple(sorted(selected)), tuple(sorted(rejected)), tuple(sorted(stalemates)), tuple(traces))

    @staticmethod
    def _incompatible_symmetric(a: MotifCandidate, b: MotifCandidate, context: OrientationActualizationContext) -> bool:
        return context.incompatible(a, b) or context.incompatible(b, a)

    def _conflict_components(self, candidates: Sequence[MotifCandidate], context: OrientationActualizationContext) -> List[Tuple[MotifCandidate, ...]]:
        remaining = set(range(len(candidates)))
        comps: List[Tuple[MotifCandidate, ...]] = []
        while remaining:
            start = remaining.pop()
            stack = [start]
            indices = {start}
            while stack:
                i = stack.pop()
                for j in list(remaining):
                    if self._incompatible_symmetric(candidates[i], candidates[j], context):
                        remaining.remove(j)
                        indices.add(j)
                        stack.append(j)
            comps.append(tuple(candidates[i] for i in sorted(indices, key=lambda k: candidates[k].name)))
        return sorted(comps, key=lambda c: tuple(m.name for m in c))

    @staticmethod
    def _kind_rank(kind: str) -> int:
        return {"seed": 0, "renewal": 1, "alternative": 2, "generic": 3}.get(kind, 4)

    def _rank_without_name(self, motif: MotifCandidate) -> Tuple[int, int, int]:
        return (-motif.priority, len(motif.support_cut), self._kind_rank(motif.kind))

    def _total_order_key(self, motif: MotifCandidate) -> Tuple[int, int, int, str]:
        return (*self._rank_without_name(motif), motif.name)

    def _top_pre_name_rank_group(self, candidates: Sequence[MotifCandidate]) -> Tuple[MotifCandidate, ...]:
        ordered = sorted(candidates, key=self._rank_without_name)
        if not ordered:
            return ()
        best = self._rank_without_name(ordered[0])
        return tuple(m for m in ordered if self._rank_without_name(m) == best)

    def _contains_incompatible_pair(self, candidates: Sequence[MotifCandidate], context: OrientationActualizationContext) -> bool:
        for i, a in enumerate(candidates):
            for b in candidates[i + 1:]:
                if self._incompatible_symmetric(a, b, context):
                    return True
        return False


class MotifCommitProtocol:
    def __init__(self, dag: CausalDAG, motifs: Sequence[MotifCandidate], context: OrientationActualizationContext) -> None:
        self.dag = dag
        self.motifs = list(motifs)
        self.context = context
        self._support_eval_cache: Dict[str, SupportEvaluation] = {}

    def support_evaluation(self, motif: MotifCandidate) -> SupportEvaluation:
        if motif.name not in self._support_eval_cache:
            self._support_eval_cache[motif.name] = self.context.evaluate_support(motif, motif.support_cut)
        return self._support_eval_cache[motif.name]

    def supported(self, motif: MotifCandidate) -> bool:
        return self.support_evaluation(motif).supported

    def ready(self, motif: MotifCandidate, site: NodeId) -> bool:
        return self.dag.ready_at(motif.support_cut, site)

    def eligible_at(self, site: NodeId) -> Tuple[MotifCandidate, ...]:
        return tuple(m for m in self.motifs if self.supported(m) and self.ready(m, site))

    def blockers(self, motif: MotifCandidate, site: NodeId) -> Tuple[MotifCandidate, ...]:
        if not self.supported(motif) or not self.ready(motif, site):
            return ()
        out: List[MotifCandidate] = []
        for other in self.motifs:
            if other.name == motif.name:
                continue
            if self.supported(other) and self.ready(other, site) and self.context.incompatible(motif, other):
                out.append(other)
        return tuple(out)

    def decision(self, motif: MotifCandidate, site: NodeId) -> CommitDecision:
        ev = self.support_evaluation(motif)
        supported = ev.supported
        ready = self.ready(motif, site) if supported else False
        blocked = self.blockers(motif, site) if supported and ready else ()
        return CommitDecision(motif.name, site, supported, ready, supported and ready and not blocked, tuple(b.name for b in blocked), ev.failed_gates)

    def decisions_at(self, site: NodeId) -> Tuple[CommitDecision, ...]:
        return tuple(self.decision(m, site) for m in self.motifs)

    def selector_closure_at(self, site: NodeId, selector: Optional[SelectorPolicy] = None) -> SelectorClosureResult:
        return (selector or SelectorPolicy()).select(site=site, candidates=self.eligible_at(site), context=self.context)

    def selected_blockers(self, motif: MotifCandidate, site: NodeId, closure: SelectorClosureResult) -> Tuple[MotifCandidate, ...]:
        if motif.name not in closure.selected_set():
            return ()
        selected = closure.selected_set()
        return tuple(m for m in self.motifs if m.name in selected and m.name != motif.name and self.context.incompatible(motif, m))

    def selected_decision(self, motif: MotifCandidate, site: NodeId, selector: Optional[SelectorPolicy] = None, closure: Optional[SelectorClosureResult] = None) -> SelectedCommitDecision:
        strict = self.decision(motif, site)
        closure = closure or self.selector_closure_at(site, selector)
        selected = motif.name in closure.selected_set()
        selected_blocked = self.selected_blockers(motif, site, closure) if selected else ()
        if not strict.supported:
            reason = "not_supported"
        elif not strict.ready:
            reason = "not_ready"
        elif selected and not selected_blocked:
            reason = "selected"
        elif selected and selected_blocked:
            reason = "selected_but_blocked_by_selected_competitor"
        elif motif.name in closure.stalemate_set():
            reason = "selector_stalemate"
        elif motif.name in closure.rejected_set():
            reason = "rejected_by_selector"
        else:
            reason = "not_eligible"
        return SelectedCommitDecision(motif.name, site, strict.supported, strict.ready, selected, strict.supported and strict.ready and selected and not selected_blocked, reason, strict.blocked_by, tuple(b.name for b in selected_blocked), strict.support_failures)

    def selected_decisions_at(self, site: NodeId, selector: Optional[SelectorPolicy] = None) -> Tuple[SelectedCommitDecision, ...]:
        closure = self.selector_closure_at(site, selector)
        return tuple(self.selected_decision(m, site, selector, closure) for m in self.motifs)


def _orientation_witness_metadata(*, rng: random.Random, candidate_past: Iterable[NodeId], support_cut: Iterable[NodeId], site: NodeId, defect_rate: float) -> Dict[str, object]:
    support = sorted(set(support_cut))
    closure: Dict[str, object] = {
        "selector_compatible": True,
        "no_extra_random_labels": True,
        "no_particle_label_primitives": True,
        "qN1_signature": 7,
        "local_conserved": True,
        "sign_links": [[int(y), int(site), rng.choice([-1, 1])] for y in support],
    }
    witness: Dict[str, object] = {
        "candidate_past": sorted(set(candidate_past)),
        "support_cut": support,
        "frontier_sufficient_for_motif": True,
        "local_ledger_compatible": True,
        "carrier_represented_by_frontier": True,
        "closure": closure,
    }
    if defect_rate > 0 and rng.random() < defect_rate:
        tag = rng.choice(["frontier_sufficient_for_motif", "local_ledger_compatible", "carrier_represented_by_frontier", "selector_compatible", "no_extra_random_labels", "no_particle_label_primitives", "qN1_signature", "local_conserved", "sign_links"])
        if tag in {"frontier_sufficient_for_motif", "local_ledger_compatible", "carrier_represented_by_frontier"}:
            witness[tag] = False
        elif tag == "qN1_signature":
            closure["qN1_signature"] = rng.choice([0, 1, 3, 5])
        elif tag == "sign_links":
            closure["sign_links"] = [] if support else [[-1, -1, 0]]
        else:
            closure[tag] = False
        witness["orientation_defect_tag"] = tag
    return witness


def _metadata_with_gates(*, rng: random.Random, candidate_past: Iterable[NodeId], parents: Iterable[NodeId], support_cut: SupportCut, site: NodeId, defect_rate: float, orientation_defect_rate: float) -> Dict[str, object]:
    metadata: Dict[str, object] = {
        "candidate_past": sorted(set(candidate_past)),
        "parents": sorted(set(parents)),
        "past_size": len(set(candidate_past)),
        "bdg_local_ok": True,
        "ledger_local_ok": True,
        "orientation_support_witness": _orientation_witness_metadata(rng=rng, candidate_past=candidate_past, support_cut=support_cut, site=site, defect_rate=orientation_defect_rate),
        "defect_tags": [],
    }
    if defect_rate > 0 and rng.random() < defect_rate:
        tag = rng.choice(["bdg_local_ok", "ledger_local_ok"])
        metadata[tag] = False
        metadata["defect_tags"] = [tag]
    ow = metadata["orientation_support_witness"]
    if isinstance(ow, Mapping) and ow.get("orientation_defect_tag"):
        metadata["defect_tags"] = list(metadata.get("defect_tags", [])) + [f"orientation:{ow['orientation_defect_tag']}"]
    return metadata


def make_context(dag: CausalDAG, *, max_support_width: Optional[int] = None, max_depth_span: Optional[int] = None, use_orientation_conflicts: bool = True) -> OrientationActualizationContext:
    certifier = GraphOrientationSupportCertifier(dag, max_support_width=max_support_width, max_depth_span=max_depth_span)
    return OrientationActualizationContext(certifier, use_orientation_conflicts=use_orientation_conflicts)


def generate_growth_demo(
    *,
    steps: int = 24,
    seed: int = 17,
    max_parents: int = 3,
    conflict_rate: float = 0.30,
    defect_rate: float = 0.10,
    orientation_defect_rate: float = 0.12,
    conflict_witness_defect_rate: float = 0.10,
    max_support_width: Optional[int] = None,
    max_depth_span: Optional[int] = None,
    selector_mode: str = "greedy",
    selector_tie_policy: str = "lexicographic",
    use_orientation_conflicts: bool = True,
) -> Tuple[CausalDAG, List[MotifCandidate], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    rng = random.Random(seed)
    dag = CausalDAG()
    genesis = dag.add_node()
    motifs: List[MotifCandidate] = [MotifCandidate(
        name="genesis_seed",
        carrier=frozenset({genesis}),
        support_cut=frozenset(),
        kind="seed",
        priority=3,
        metadata={
            "candidate_past": [],
            "parents": [],
            "past_size": 0,
            "bdg_local_ok": True,
            "ledger_local_ok": True,
            "orientation_support_witness": {
                "candidate_past": [],
                "support_cut": [],
                "frontier_sufficient_for_motif": True,
                "local_ledger_compatible": True,
                "carrier_represented_by_frontier": True,
                "closure": {"selector_compatible": True, "no_extra_random_labels": True, "no_particle_label_primitives": True, "qN1_signature": 7, "local_conserved": True, "sign_links": []},
            },
            "defect_tags": [],
        },
    )]
    rows: List[Dict[str, object]] = []
    support_rows: List[Dict[str, object]] = []
    selector_rows: List[Dict[str, object]] = []
    orientation_rows: List[Dict[str, object]] = []
    conflict_rows: List[Dict[str, object]] = []
    selector = SelectorPolicy(selector_mode, selector_tie_policy)

    for _ in range(steps):
        existing = list(dag.nodes)
        frontier = list(dag.maximal_nodes()) or existing
        parent_pool = frontier if frontier else existing
        parents = set(rng.sample(parent_pool, k=rng.randint(1, min(max_parents, len(parent_pool)))))
        if len(existing) > 2 and rng.random() < 0.35:
            parents.add(rng.choice(existing))
        site = dag.add_node(parents)
        past = dag.candidate_past_from_support(parents)
        support_cut = dag.support_cut_of_finite_hasse_frontier(past)

        stable_meta = _metadata_with_gates(rng=rng, candidate_past=past, parents=parents, support_cut=support_cut, site=site, defect_rate=defect_rate * 0.35, orientation_defect_rate=orientation_defect_rate * 0.35)
        motifs.append(MotifCandidate(f"renewal_{site}", frozenset({site}), support_cut, "renewal", priority=2, metadata={**stable_meta, "support_width": len(support_cut)}))

        introduced_conflict = rng.random() < conflict_rate
        if introduced_conflict:
            domain = f"orientation_choice_at_{site}"
            for label in ("A", "B"):
                meta = _metadata_with_gates(rng=rng, candidate_past=past, parents=parents, support_cut=support_cut, site=site, defect_rate=defect_rate, orientation_defect_rate=orientation_defect_rate)
                meta["orientation_conflict_domain"] = domain
                meta["orientation_conflict_ok"] = not (conflict_witness_defect_rate > 0 and rng.random() < conflict_witness_defect_rate)
                motifs.append(MotifCandidate(f"choice_{label}_{site}", frozenset({site}), support_cut, "alternative", exclusion_domain=domain, priority=1, metadata={**meta, "support_width": len(support_cut)}))

        context = make_context(dag, max_support_width=max_support_width, max_depth_span=max_depth_span, use_orientation_conflicts=use_orientation_conflicts)
        protocol = MotifCommitProtocol(dag, motifs, context)
        strict = protocol.decisions_at(site)
        closure = protocol.selector_closure_at(site, selector)
        selected = tuple(protocol.selected_decision(m, site, selector, closure) for m in motifs)

        for motif in motifs:
            ev = protocol.support_evaluation(motif)
            r = ev.to_row(); r["site"] = site; support_rows.append(r)
            orow = context.certifier.orientation_witness_row(motif); orow["site"] = site; orientation_rows.append(orow)

        names = {m.name: m for m in motifs}
        for component in closure.components:
            cr = component.to_row(site); cr["selector_mode"] = selector.mode; cr["selector_tie_policy"] = selector.tie_policy; selector_rows.append(cr)
            cand_names = list(component.candidates)
            for i, a_name in enumerate(cand_names):
                for b_name in cand_names[i+1:]:
                    w = context.conflict_witness(names[a_name], names[b_name])
                    if w is not None:
                        rr = w.to_row(); rr["site"] = site; conflict_rows.append(rr)

        hist: Dict[str, int] = {}
        for d in strict:
            for f in d.support_failures:
                hist[f] = hist.get(f, 0) + 1
        strict_committed = [d.motif for d in strict if d.commits]
        strict_blocked = [d.motif for d in strict if d.ready and not d.commits and d.blocked_by]
        unsupported = [d.motif for d in strict if not d.supported]
        selected_committed = [d.motif for d in selected if d.commits]
        selector_rejected = [d.motif for d in selected if d.selector_reason == "rejected_by_selector"]
        selector_stalemates = [d.motif for d in selected if d.selector_reason == "selector_stalemate"]
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
            "use_orientation_conflicts": use_orientation_conflicts,
            "eligible_count": len(closure.eligible),
            "selected_count": len(closure.selected),
            "strict_ready_count": sum(1 for d in strict if d.ready),
            "strict_supported_count": sum(1 for d in strict if d.supported),
            "unsupported_count": len(unsupported),
            "strict_committed_count": len(strict_committed),
            "strict_blocked_count": len(strict_blocked),
            "selector_committed_count": len(selected_committed),
            "selector_rejected_count": len(selector_rejected),
            "selector_stalemate_count": len(selector_stalemates),
            "orientation_failure_count": sum(count for gate, count in hist.items() if gate.startswith("orientation_")),
            "strict_committed_motifs": strict_committed,
            "strict_blocked_ready_motifs": strict_blocked,
            "selector_committed_motifs": selected_committed,
            "selector_rejected_motifs": selector_rejected,
            "selector_stalemate_motifs": selector_stalemates,
            "unsupported_motifs": unsupported,
            "support_failure_histogram": hist,
        })
    return dag, motifs, rows, support_rows, selector_rows, orientation_rows, conflict_rows


def summarize_run(rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    if not rows:
        return {"sites": 0, "total_strict_committed": 0, "total_strict_blocked": 0, "total_selector_committed": 0, "total_selector_rejected": 0, "total_selector_stalemates": 0, "total_unsupported": 0, "total_orientation_failures": 0, "mean_support_width": 0.0}
    return {
        "sites": len(rows),
        "total_strict_committed": sum(int(r.get("strict_committed_count", 0)) for r in rows),
        "total_strict_blocked": sum(int(r.get("strict_blocked_count", 0)) for r in rows),
        "total_selector_committed": sum(int(r.get("selector_committed_count", 0)) for r in rows),
        "total_selector_rejected": sum(int(r.get("selector_rejected_count", 0)) for r in rows),
        "total_selector_stalemates": sum(int(r.get("selector_stalemate_count", 0)) for r in rows),
        "total_unsupported": sum(int(r.get("unsupported_count", 0)) for r in rows),
        "total_orientation_failures": sum(int(r.get("orientation_failure_count", 0)) for r in rows),
        "mean_support_width": round(sum(int(r.get("support_width", 0)) for r in rows) / len(rows), 4),
        "last_site": rows[-1].get("site"),
    }


def run_parameter_sweep(*, seeds: Sequence[int] = (11, 17), conflict_rates: Sequence[float] = (0.0, 0.30), defect_rates: Sequence[float] = (0.0, 0.10), orientation_defect_rates: Sequence[float] = (0.0, 0.12), conflict_witness_defect_rates: Sequence[float] = (0.0, 0.25), selector_modes: Sequence[str] = ("none", "greedy"), selector_tie_policies: Sequence[str] = ("lexicographic", "stalemate"), orientation_conflict_modes: Sequence[bool] = (True,), steps: int = 24, max_parents: int = 3, max_support_width: Optional[int] = None, max_depth_span: Optional[int] = None) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for use_orientation_conflicts in orientation_conflict_modes:
        for selector_mode in selector_modes:
            for selector_tie_policy in selector_tie_policies:
                for conflict_rate in conflict_rates:
                    for defect_rate in defect_rates:
                        for orientation_defect_rate in orientation_defect_rates:
                            for conflict_witness_defect_rate in conflict_witness_defect_rates:
                                for seed in seeds:
                                    dag, motifs, rows, *_ = generate_growth_demo(steps=steps, seed=seed, max_parents=max_parents, conflict_rate=conflict_rate, defect_rate=defect_rate, orientation_defect_rate=orientation_defect_rate, conflict_witness_defect_rate=conflict_witness_defect_rate, max_support_width=max_support_width, max_depth_span=max_depth_span, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy, use_orientation_conflicts=use_orientation_conflicts)
                                    out.append({"seed": seed, "steps": steps, "nodes": len(dag.nodes), "edges": len(dag.edges), "motifs": len(motifs), "conflict_rate": conflict_rate, "defect_rate": defect_rate, "orientation_defect_rate": orientation_defect_rate, "conflict_witness_defect_rate": conflict_witness_defect_rate, "use_orientation_conflicts": use_orientation_conflicts, "selector_mode": selector_mode, "selector_tie_policy": selector_tie_policy, "max_support_width": max_support_width, "max_depth_span": max_depth_span, **summarize_run(rows)})
    return out


def run_orientation_comparison(*, seed: int = 17, steps: int = 24, conflict_rate: float = 0.30, defect_rate: float = 0.10, orientation_defect_rate: float = 0.12, conflict_witness_defect_rate: float = 0.10) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for use_orientation_conflicts in (False, True):
        dag, motifs, rows, *_ = generate_growth_demo(steps=steps, seed=seed, conflict_rate=conflict_rate, defect_rate=defect_rate, orientation_defect_rate=orientation_defect_rate, conflict_witness_defect_rate=conflict_witness_defect_rate, use_orientation_conflicts=use_orientation_conflicts)
        out.append({"seed": seed, "steps": steps, "nodes": len(dag.nodes), "edges": len(dag.edges), "motifs": len(motifs), "use_orientation_conflicts": use_orientation_conflicts, **summarize_run(rows)})
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
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for k, v in list(out.items()):
                if isinstance(v, (list, tuple, dict, set, frozenset)):
                    out[k] = json.dumps(v, sort_keys=True)
            writer.writerow(out)


def dump_state_json(dag: CausalDAG, motifs: Sequence[MotifCandidate], rows: Sequence[Mapping[str, object]], support_rows: Sequence[Mapping[str, object]], selector_rows: Sequence[Mapping[str, object]], orientation_rows: Sequence[Mapping[str, object]], conflict_rows: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "0.4",
        "nodes": list(dag.nodes),
        "edges": [list(e) for e in dag.edges],
        "depth": {str(k): v for k, v in dag.depth.items()},
        "motifs": [{"name": m.name, "carrier": sorted(m.carrier), "support_cut": sorted(m.support_cut), "kind": m.kind, "exclusion_domain": m.exclusion_domain, "certified": m.certified, "priority": m.priority, "metadata": dict(m.metadata)} for m in motifs],
        "site_summaries": list(rows),
        "support_evaluations": list(support_rows),
        "selector_components": list(selector_rows),
        "orientation_witnesses": list(orientation_rows),
        "orientation_conflict_witnesses": list(conflict_rows),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")




# ---------------------------------------------------------------------------
# v0.5 causal-severance / actualization-fragility workbench
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CausalSeveranceIntervention:
    """Controlled RA-native perturbation of causal support availability."""

    mode: str
    severity: float
    seed: int = 0
    label: str = ""

    def __post_init__(self) -> None:
        allowed = {
            "edge_dropout",
            "frontier_dropout",
            "support_delay",
            "orientation_degradation",
            "ledger_failure",
            "selector_stress",
        }
        if self.mode not in allowed:
            raise ValueError(f"unknown severance mode: {self.mode}")
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError("severity must lie in [0, 1]")


@dataclass(frozen=True)
class SeveranceEvaluation:
    """Before/after actualization diagnostics for one motif at one site."""

    motif: str
    site: NodeId
    mode: str
    severity: float
    seed: int
    support_width: int
    before_supported: bool
    before_ready: bool
    before_strict_commits: bool
    before_selected_commits: bool
    after_supported: bool
    after_ready: bool
    after_strict_commits: bool
    after_selected_commits: bool
    lost_support: bool
    lost_readiness: bool
    lost_strict_commit: bool
    lost_selected_commit: bool
    finality_depth_before: Optional[int]
    finality_depth_after: Optional[int]
    finality_depth_shift: Optional[int]
    recovery_length: Optional[int]
    intervention_detail: str

    def to_row(self) -> Dict[str, object]:
        return {
            "motif": self.motif,
            "site": self.site,
            "mode": self.mode,
            "severity": self.severity,
            "seed": self.seed,
            "support_width": self.support_width,
            "before_supported": self.before_supported,
            "before_ready": self.before_ready,
            "before_strict_commits": self.before_strict_commits,
            "before_selected_commits": self.before_selected_commits,
            "after_supported": self.after_supported,
            "after_ready": self.after_ready,
            "after_strict_commits": self.after_strict_commits,
            "after_selected_commits": self.after_selected_commits,
            "lost_support": self.lost_support,
            "lost_readiness": self.lost_readiness,
            "lost_strict_commit": self.lost_strict_commit,
            "lost_selected_commit": self.lost_selected_commit,
            "finality_depth_before": self.finality_depth_before,
            "finality_depth_after": self.finality_depth_after,
            "finality_depth_shift": self.finality_depth_shift,
            "recovery_length": self.recovery_length,
            "intervention_detail": self.intervention_detail,
        }


def clone_dag(dag: CausalDAG) -> CausalDAG:
    out = CausalDAG()
    out.parents = {n: set(ps) for n, ps in dag.parents.items()}
    out.children = {n: set(cs) for n, cs in dag.children.items()}
    out.depth = dict(dag.depth)
    out._next_id = dag._next_id
    out._ancestors_cache.clear()
    return out


def recompute_depths(dag: CausalDAG) -> None:
    dag.depth = {}
    for n in sorted(dag.parents):
        ps = dag.parents[n]
        dag.depth[n] = 0 if not ps else 1 + max(dag.depth[p] for p in ps)
    dag._ancestors_cache.clear()


def remove_edges(dag: CausalDAG, edges: Iterable[Tuple[NodeId, NodeId]]) -> CausalDAG:
    out = clone_dag(dag)
    for p, c in edges:
        if c in out.parents and p in out.parents[c]:
            out.parents[c].remove(p)
        if p in out.children and c in out.children[p]:
            out.children[p].remove(c)
    recompute_depths(out)
    return out


def causal_edges_inside_site_past(dag: CausalDAG, site: NodeId) -> Tuple[Tuple[NodeId, NodeId], ...]:
    past = dag.ancestors(site, include_self=True)
    return tuple(sorted((p, c) for c in past for p in dag.parents[c] if p in past))


def choose_prefix_fraction(items: Sequence[object], severity: float, rng: random.Random) -> Tuple[object, ...]:
    if severity <= 0 or not items:
        return ()
    shuffled = list(items)
    rng.shuffle(shuffled)
    k = max(1, min(len(shuffled), int(round(severity * len(shuffled)))))
    return tuple(shuffled[:k])


def min_finality_depth(dag: CausalDAG, support_cut: SupportCut) -> Optional[int]:
    if not dag.depth:
        return None
    for d in sorted(set(dag.depth.values())):
        later = [x for x, depth in dag.depth.items() if depth >= d]
        if later and all(dag.ready_at(support_cut, x) for x in later):
            return d
    return None


def readiness_recovery_length(
    dag: CausalDAG,
    support_cut: SupportCut,
    site: NodeId,
    *,
    unavailable_support: FrozenSet[NodeId] = frozenset(),
    delay_depth: int = 0,
) -> Optional[int]:
    if unavailable_support.intersection(support_cut):
        return None
    target_depth = dag.depth[site] + max(0, delay_depth)
    for x in sorted(dag.nodes, key=lambda n: (dag.depth[n], n)):
        if dag.depth[x] < dag.depth[site] or dag.depth[x] < target_depth:
            continue
        if dag.ready_at(support_cut, x):
            return max(0, dag.depth[x] - dag.depth[site])
    return None


def metadata_deepcopy(metadata: Mapping[str, object]) -> Dict[str, object]:
    return json.loads(json.dumps(dict(metadata), sort_keys=True))


def clone_motif(motif: MotifCandidate, *, metadata: Optional[Mapping[str, object]] = None, name: Optional[str] = None, priority: Optional[int] = None, exclusion_domain: Optional[str] = None) -> MotifCandidate:
    return MotifCandidate(
        name=name or motif.name,
        carrier=motif.carrier,
        support_cut=motif.support_cut,
        kind=motif.kind,
        exclusion_domain=motif.exclusion_domain if exclusion_domain is None else exclusion_domain,
        certified=motif.certified,
        priority=motif.priority if priority is None else priority,
        metadata=metadata_deepcopy(metadata if metadata is not None else motif.metadata),
    )


def degraded_orientation_metadata(metadata: Mapping[str, object], severity: float) -> Dict[str, object]:
    out = metadata_deepcopy(metadata)
    witness = out.get("orientation_support_witness")
    if not isinstance(witness, dict) or severity <= 0:
        return out
    closure = witness.get("closure")
    if not isinstance(closure, dict):
        closure = {}
        witness["closure"] = closure
    steps = max(1, int(round(severity * 5)))
    if steps >= 1:
        closure["qN1_signature"] = 5
    if steps >= 2:
        closure["local_conserved"] = False
    if steps >= 3:
        closure["sign_links"] = []
    if steps >= 4:
        witness["frontier_sufficient_for_motif"] = False
    if steps >= 5:
        closure["selector_compatible"] = False
    out["severance_tags"] = list(out.get("severance_tags", [])) + [f"orientation_degradation:{severity}"]
    return out


def degraded_ledger_metadata(metadata: Mapping[str, object], severity: float) -> Dict[str, object]:
    out = metadata_deepcopy(metadata)
    if severity <= 0:
        return out
    out["ledger_local_ok"] = False
    witness = out.get("orientation_support_witness")
    if isinstance(witness, dict):
        witness["local_ledger_compatible"] = False
    out["severance_tags"] = list(out.get("severance_tags", [])) + [f"ledger_failure:{severity}"]
    return out


def with_conflict_domain(metadata: Mapping[str, object], domain: str) -> Dict[str, object]:
    out = metadata_deepcopy(metadata)
    out["orientation_conflict_domain"] = domain
    out["orientation_conflict_ok"] = True
    return out


def replace_motif(motifs: Sequence[MotifCandidate], target: MotifCandidate, replacement: MotifCandidate) -> List[MotifCandidate]:
    return [replacement if m.name == target.name else m for m in motifs]


def protocol_for(dag: CausalDAG, motifs: Sequence[MotifCandidate], *, selector_mode: str = "greedy", selector_tie_policy: str = "lexicographic", use_orientation_conflicts: bool = True) -> Tuple[MotifCommitProtocol, SelectorPolicy]:
    context = make_context(dag, use_orientation_conflicts=use_orientation_conflicts)
    return MotifCommitProtocol(dag, motifs, context), SelectorPolicy(selector_mode, selector_tie_policy)


def motif_site(motif: MotifCandidate) -> NodeId:
    return max(motif.carrier) if motif.carrier else -1


def selected_commit_bool(protocol: MotifCommitProtocol, motif: MotifCandidate, site: NodeId, selector: SelectorPolicy) -> bool:
    closure = protocol.selector_closure_at(site, selector)
    return protocol.selected_decision(motif, site, selector, closure).commits


def evaluate_severance(
    dag: CausalDAG,
    motifs: Sequence[MotifCandidate],
    motif: MotifCandidate,
    site: NodeId,
    intervention: CausalSeveranceIntervention,
    *,
    selector_mode: str = "greedy",
    selector_tie_policy: str = "lexicographic",
    use_orientation_conflicts: bool = True,
) -> SeveranceEvaluation:
    base_protocol, selector = protocol_for(dag, motifs, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy, use_orientation_conflicts=use_orientation_conflicts)
    before_decision = base_protocol.decision(motif, site)
    before_selected = selected_commit_bool(base_protocol, motif, site, selector)
    finality_before = min_finality_depth(dag, motif.support_cut)

    rng = random.Random(intervention.seed + 7919 * site + sum(ord(c) for c in motif.name) + int(intervention.severity * 1000))
    after_dag = dag
    after_motifs = list(motifs)
    after_motif = motif
    unavailable_support: FrozenSet[NodeId] = frozenset()
    delay_depth = 0
    detail = "no_change"

    if intervention.mode == "edge_dropout":
        chosen = choose_prefix_fraction(causal_edges_inside_site_past(dag, site), intervention.severity, rng)
        chosen_edges = tuple((int(a), int(b)) for a, b in chosen)  # type: ignore[misc]
        after_dag = remove_edges(dag, chosen_edges)
        detail = f"removed_edges={list(chosen_edges)}"
    elif intervention.mode == "frontier_dropout":
        dropped = choose_prefix_fraction(tuple(sorted(motif.support_cut)), intervention.severity, rng)
        unavailable_support = frozenset(int(x) for x in dropped)  # type: ignore[arg-type]
        detail = f"dropped_support_vertices={sorted(unavailable_support)}"
    elif intervention.mode == "support_delay":
        delay_depth = int(round(intervention.severity * 5))
        detail = f"delay_depth={delay_depth}"
    elif intervention.mode == "orientation_degradation":
        after_motif = clone_motif(motif, metadata=degraded_orientation_metadata(motif.metadata, intervention.severity))
        after_motifs = replace_motif(motifs, motif, after_motif)
        detail = f"orientation_degradation_severity={intervention.severity}"
    elif intervention.mode == "ledger_failure":
        after_motif = clone_motif(motif, metadata=degraded_ledger_metadata(motif.metadata, intervention.severity))
        after_motifs = replace_motif(motifs, motif, after_motif)
        detail = f"ledger_failure_severity={intervention.severity}"
    elif intervention.mode == "selector_stress":
        domain = f"severance_selector_stress:{motif.name}:{site}"
        after_motif = clone_motif(motif, metadata=with_conflict_domain(motif.metadata, domain), exclusion_domain=domain)
        after_motifs = replace_motif(motifs, motif, after_motif)
        competitor_count = int(round(intervention.severity * 3))
        for idx in range(competitor_count):
            comp = clone_motif(motif, name=f"stress_{idx}_{motif.name}", metadata=with_conflict_domain(motif.metadata, domain), priority=motif.priority, exclusion_domain=domain)
            after_motifs.append(comp)
        detail = f"added_incompatible_competitors={competitor_count} domain={domain}"

    after_protocol, after_selector = protocol_for(after_dag, after_motifs, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy, use_orientation_conflicts=use_orientation_conflicts)
    after_decision = after_protocol.decision(after_motif, site)
    after_selected = selected_commit_bool(after_protocol, after_motif, site, after_selector)

    after_supported = after_decision.supported
    after_ready = after_decision.ready
    after_strict = after_decision.commits
    if unavailable_support.intersection(motif.support_cut):
        after_supported = False
        after_ready = False
        after_strict = False
        after_selected = False
    if delay_depth > 0:
        after_ready = False
        after_strict = False
        after_selected = False

    finality_after = min_finality_depth(after_dag, motif.support_cut)
    if intervention.mode == "support_delay" and finality_after is not None:
        finality_after = finality_after + delay_depth
    if unavailable_support.intersection(motif.support_cut):
        finality_after = None
    shift = None if finality_before is None or finality_after is None else finality_after - finality_before
    recovery = readiness_recovery_length(after_dag, motif.support_cut, site, unavailable_support=unavailable_support, delay_depth=delay_depth)

    return SeveranceEvaluation(
        motif=motif.name,
        site=site,
        mode=intervention.mode,
        severity=intervention.severity,
        seed=intervention.seed,
        support_width=len(motif.support_cut),
        before_supported=before_decision.supported,
        before_ready=before_decision.ready,
        before_strict_commits=before_decision.commits,
        before_selected_commits=before_selected,
        after_supported=after_supported,
        after_ready=after_ready,
        after_strict_commits=after_strict,
        after_selected_commits=after_selected,
        lost_support=before_decision.supported and not after_supported,
        lost_readiness=before_decision.ready and not after_ready,
        lost_strict_commit=before_decision.commits and not after_strict,
        lost_selected_commit=before_selected and not after_selected,
        finality_depth_before=finality_before,
        finality_depth_after=finality_after,
        finality_depth_shift=shift,
        recovery_length=recovery,
        intervention_detail=detail,
    )


def target_motifs_for_severance(motifs: Sequence[MotifCandidate], *, include_alternatives: bool = False, max_targets: Optional[int] = 12) -> Tuple[MotifCandidate, ...]:
    kinds = {"renewal", "alternative"} if include_alternatives else {"renewal"}
    out = tuple(m for m in motifs if m.kind in kinds and m.carrier and m.support_cut)
    return out if max_targets is None else out[:max_targets]


def run_severance_workbench(
    *,
    steps: int = 8,
    seed: int = 17,
    max_parents: int = 3,
    conflict_rate: float = 0.30,
    defect_rate: float = 0.05,
    orientation_defect_rate: float = 0.05,
    conflict_witness_defect_rate: float = 0.10,
    severance_seeds: Sequence[int] = (101,),
    severities: Sequence[float] = (0.0, 0.50, 1.0),
    modes: Sequence[str] = ("edge_dropout", "frontier_dropout", "support_delay", "orientation_degradation", "ledger_failure", "selector_stress"),
    selector_mode: str = "greedy",
    selector_tie_policy: str = "lexicographic",
    include_alternatives: bool = False,
    max_targets: Optional[int] = 4,
) -> Tuple[CausalDAG, List[MotifCandidate], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    dag, motifs, base_rows, *_ = generate_growth_demo(
        steps=steps,
        seed=seed,
        max_parents=max_parents,
        conflict_rate=conflict_rate,
        defect_rate=defect_rate,
        orientation_defect_rate=orientation_defect_rate,
        conflict_witness_defect_rate=conflict_witness_defect_rate,
        selector_mode=selector_mode,
        selector_tie_policy=selector_tie_policy,
    )
    targets = target_motifs_for_severance(motifs, include_alternatives=include_alternatives, max_targets=max_targets)
    eval_rows: List[Dict[str, object]] = []
    for sev_seed in severance_seeds:
        for mode in modes:
            for severity in severities:
                intervention = CausalSeveranceIntervention(mode=mode, severity=float(severity), seed=int(sev_seed))
                for motif in targets:
                    site = motif_site(motif)
                    if site >= 0:
                        ev = evaluate_severance(dag, motifs, motif, site, intervention, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy)
                        eval_rows.append(ev.to_row())
    fragility_rows = summarize_fragility(eval_rows)
    finality_rows = [r for r in eval_rows if r.get("finality_depth_before") is not None or r.get("finality_depth_after") is not None]
    recovery_rows = [r for r in eval_rows if r.get("recovery_length") is not None or r.get("lost_readiness")]
    return dag, motifs, eval_rows, fragility_rows, finality_rows, recovery_rows


def summarize_fragility(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, float, int], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["mode"]), float(r["severity"]), int(r["support_width"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, severity, width), items in sorted(buckets.items()):
        n = len(items)
        shifts = [int(r["finality_depth_shift"]) for r in items if r.get("finality_depth_shift") is not None]
        recoveries = [int(r["recovery_length"]) for r in items if r.get("recovery_length") is not None]
        out.append({
            "mode": mode,
            "severity": severity,
            "support_width": width,
            "samples": n,
            "lost_support_rate": round(sum(1 for r in items if bool(r.get("lost_support"))) / n, 6),
            "lost_readiness_rate": round(sum(1 for r in items if bool(r.get("lost_readiness"))) / n, 6),
            "lost_strict_commit_rate": round(sum(1 for r in items if bool(r.get("lost_strict_commit"))) / n, 6),
            "lost_selected_commit_rate": round(sum(1 for r in items if bool(r.get("lost_selected_commit"))) / n, 6),
            "mean_recovery_length": round(sum(recoveries) / len(recoveries), 6) if recoveries else None,
            "mean_finality_depth_shift": round(sum(shifts) / len(shifts), 6) if shifts else None,
        })
    return out


def summarize_severance_sweep(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, float], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["mode"]), float(r["severity"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, severity), items in sorted(buckets.items()):
        n = len(items)
        out.append({
            "mode": mode,
            "severity": severity,
            "samples": n,
            "mean_support_width": round(sum(int(r["support_width"]) for r in items) / n, 6),
            "support_loss_rate": round(sum(1 for r in items if bool(r.get("lost_support"))) / n, 6),
            "readiness_loss_rate": round(sum(1 for r in items if bool(r.get("lost_readiness"))) / n, 6),
            "strict_commit_loss_rate": round(sum(1 for r in items if bool(r.get("lost_strict_commit"))) / n, 6),
            "selected_commit_loss_rate": round(sum(1 for r in items if bool(r.get("lost_selected_commit"))) / n, 6),
        })
    return out


def write_severance_predictions(rows: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sweep = summarize_severance_sweep(rows)
    strongest = sorted(sweep, key=lambda r: (float(r["strict_commit_loss_rate"]), float(r["readiness_loss_rate"])), reverse=True)[:5]
    widths = sorted(set(int(r["support_width"]) for r in rows)) if rows else []
    text = [
        "# RA Causal-Severance Prediction Note — Simulator v0.5",
        "",
        "This note states RA-native diagnostics only. It does not treat any inherited theory as the target.",
        "",
        "## Workbench predicates",
        "",
        "- support loss: orientation/ledger/support certification no longer holds after intervention.",
        "- readiness loss: the required support cut no longer reaches the tested site, or its availability is delayed beyond the tested site.",
        "- commitment loss: a motif that committed before the intervention no longer commits after it.",
        "- recovery length: the first later depth at which the same support cut is again ready, when such a depth exists in the finite run.",
        "",
        "## Observed support-width classes",
        "",
        f"Observed support widths in this run: {widths}.",
        "",
        "## Highest-loss intervention settings",
        "",
    ]
    for r in strongest:
        text.append(f"- mode={r['mode']}, severity={r['severity']}: strict_commit_loss_rate={r['strict_commit_loss_rate']}, readiness_loss_rate={r['readiness_loss_rate']}, support_loss_rate={r['support_loss_rate']}.")
    text += [
        "",
        "## RA-native prediction families to track",
        "",
        "1. Frontier-width fragility: narrower support cuts should show higher loss rates under frontier dropout when support redundancy is absent.",
        "2. Reachability/certification separation: edge and frontier interventions should primarily alter readiness, while orientation and ledger interventions should primarily alter support certification.",
        "3. Delay-induced finality shift: support delay should preserve recoverability when the support remains connected, but move readiness/finality deeper into the causal future.",
        "4. Selector-stress ambiguity: increasing certified incompatible alternatives should alter selected commitment without necessarily damaging support readiness.",
        "",
        "These are simulator diagnostics, not empirical claims. Their role is to sharpen RA-native prediction language before physical correspondence tests are proposed.",
    ]
    path.write_text("\n".join(text) + "\n", encoding="utf-8")


def dump_severance_state_json(dag: CausalDAG, motifs: Sequence[MotifCandidate], severance_rows: Sequence[Mapping[str, object]], fragility_rows: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "0.5",
        "nodes": list(dag.nodes),
        "edges": [list(e) for e in dag.edges],
        "depth": {str(k): v for k, v in dag.depth.items()},
        "motifs": [{"name": m.name, "carrier": sorted(m.carrier), "support_cut": sorted(m.support_cut), "kind": m.kind, "exclusion_domain": m.exclusion_domain, "certified": m.certified, "priority": m.priority, "metadata": dict(m.metadata)} for m in motifs],
        "severance_evaluations": list(severance_rows),
        "fragility_profiles": list(fragility_rows),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RA causal-DAG motif-commit simulator v0.5 with causal-severance diagnostics.")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--max-parents", type=int, default=3)
    parser.add_argument("--conflict-rate", type=float, default=0.30)
    parser.add_argument("--defect-rate", type=float, default=0.05)
    parser.add_argument("--orientation-defect-rate", type=float, default=0.05)
    parser.add_argument("--conflict-witness-defect-rate", type=float, default=0.10)
    parser.add_argument("--selector-mode", choices=["none", "greedy"], default="greedy")
    parser.add_argument("--selector-tie-policy", choices=["lexicographic", "stalemate"], default="lexicographic")
    parser.add_argument("--include-alternatives", action="store_true")
    parser.add_argument("--max-targets", type=int, default=4)
    parser.add_argument("--summary-csv", type=Path, default=Path("outputs/ra_causal_dag_severance_summary_v0_5.csv"))
    parser.add_argument("--severance-csv", type=Path, default=Path("outputs/ra_causal_dag_severance_evaluations_v0_5.csv"))
    parser.add_argument("--sweep-csv", type=Path, default=Path("outputs/ra_causal_dag_severance_sweep_v0_5.csv"))
    parser.add_argument("--fragility-csv", type=Path, default=Path("outputs/ra_causal_dag_fragility_profiles_v0_5.csv"))
    parser.add_argument("--finality-csv", type=Path, default=Path("outputs/ra_causal_dag_finality_depth_shift_v0_5.csv"))
    parser.add_argument("--recovery-csv", type=Path, default=Path("outputs/ra_causal_dag_recovery_lengths_v0_5.csv"))
    parser.add_argument("--prediction-md", type=Path, default=Path("outputs/ra_causal_dag_severance_predictions_v0_5.md"))
    parser.add_argument("--json", type=Path, default=Path("outputs/ra_causal_dag_severance_state_v0_5.json"))
    args = parser.parse_args()

    dag, motifs, severance_rows, fragility_rows, finality_rows, recovery_rows = run_severance_workbench(
        steps=args.steps,
        seed=args.seed,
        max_parents=args.max_parents,
        conflict_rate=args.conflict_rate,
        defect_rate=args.defect_rate,
        orientation_defect_rate=args.orientation_defect_rate,
        conflict_witness_defect_rate=args.conflict_witness_defect_rate,
        selector_mode=args.selector_mode,
        selector_tie_policy=args.selector_tie_policy,
        include_alternatives=args.include_alternatives,
        max_targets=args.max_targets,
    )
    sweep_rows = summarize_severance_sweep(severance_rows)
    summary = {
        "version": "0.5",
        "nodes": len(dag.nodes),
        "edges": len(dag.edges),
        "motifs": len(motifs),
        "severance_evaluations": len(severance_rows),
        "fragility_profiles": len(fragility_rows),
        "sweep_rows": len(sweep_rows),
        "total_lost_support": sum(1 for r in severance_rows if r.get("lost_support")),
        "total_lost_readiness": sum(1 for r in severance_rows if r.get("lost_readiness")),
        "total_lost_strict_commit": sum(1 for r in severance_rows if r.get("lost_strict_commit")),
        "total_lost_selected_commit": sum(1 for r in severance_rows if r.get("lost_selected_commit")),
    }
    rows_to_csv([summary], args.summary_csv)
    rows_to_csv(severance_rows, args.severance_csv)
    rows_to_csv(sweep_rows, args.sweep_csv)
    rows_to_csv(fragility_rows, args.fragility_csv)
    rows_to_csv(finality_rows, args.finality_csv)
    rows_to_csv(recovery_rows, args.recovery_csv)
    write_severance_predictions(severance_rows, args.prediction_md)
    dump_severance_state_json(dag, motifs, severance_rows, fragility_rows, args.json)
    print(f"nodes={len(dag.nodes)} edges={len(dag.edges)} motifs={len(motifs)}")
    print(f"summary={summary}")
    print(f"summary_csv={args.summary_csv}")
    print(f"severance_csv={args.severance_csv}")
    print(f"fragility_csv={args.fragility_csv}")
    print(f"prediction_md={args.prediction_md}")
    print(f"state_json={args.json}")


if __name__ == "__main__":
    main()
