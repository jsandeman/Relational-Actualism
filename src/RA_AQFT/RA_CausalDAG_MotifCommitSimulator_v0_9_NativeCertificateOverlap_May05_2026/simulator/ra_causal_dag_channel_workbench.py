#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.6 channel-separation workbench.

v0.6 responds to the v0.5.2 ensemble-analysis finding that frontier dropout,
ledger failure, and orientation degradation were degenerate in the earlier
workbench: all three produced the same loss profile. This module keeps the
RA-native actualization ladder, but separates the severance channels explicitly:

  candidate motif -> finite Hasse-frontier support cut -> oriented support
  witness -> certified support -> causal reachability -> support availability
  -> strict / selected commitment -> severance-channel diagnostics.

The module also introduces a support-diverse growth generator, so ensembles can
contain support frontiers of width > 1. This is necessary before support-width
fragility claims can be tested meaningfully.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import statistics
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple

try:  # package import
    from .ra_causal_dag_simulator import (
        CausalDAG,
        MotifCandidate,
        SelectorPolicy,
        SupportCut,
        clone_motif,
        degraded_ledger_metadata,
        degraded_orientation_metadata,
        min_finality_depth,
        motif_site,
        protocol_for,
        readiness_recovery_length,
        remove_edges,
        rows_to_csv,
        selected_commit_bool,
        with_conflict_domain,
        _metadata_with_gates,
    )
except ImportError:  # script import from simulator/ directory
    from ra_causal_dag_simulator import (  # type: ignore
        CausalDAG,
        MotifCandidate,
        SelectorPolicy,
        SupportCut,
        clone_motif,
        degraded_ledger_metadata,
        degraded_orientation_metadata,
        min_finality_depth,
        motif_site,
        protocol_for,
        readiness_recovery_length,
        remove_edges,
        rows_to_csv,
        selected_commit_bool,
        with_conflict_domain,
        _metadata_with_gates,
    )


SEVERANCE_MODES: Tuple[str, ...] = (
    "edge_dropout",
    "frontier_dropout",
    "support_delay",
    "orientation_degradation",
    "ledger_failure",
    "selector_stress",
)


@dataclass(frozen=True)
class ChannelSeparatedRunConfig:
    """Parameters for the v0.6 channel-separation ensemble."""

    seeds: Tuple[int, ...] = tuple(range(17, 37))
    steps: int = 24
    max_parents: int = 4
    target_frontier_min: int = 5
    branch_probability: float = 0.42
    wide_join_probability: float = 0.72
    conflict_rate: float = 0.22
    defect_rate: float = 0.02
    orientation_defect_rate: float = 0.02
    conflict_witness_defect_rate: float = 0.08
    severance_seeds: Tuple[int, ...] = (101, 103)
    severities: Tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 1.0)
    modes: Tuple[str, ...] = SEVERANCE_MODES
    selector_mode: str = "greedy"
    selector_tie_policy: str = "lexicographic"
    include_alternatives: bool = False
    max_targets: Optional[int] = 18
    sample_limit: int = 2000

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "ChannelSeparatedRunConfig":
        seeds = tuple(range(args.seed_start, args.seed_stop)) if args.seed_list is None else tuple(int(x) for x in args.seed_list.split(",") if x.strip())
        severance_seeds = tuple(int(x) for x in args.severance_seeds.split(",") if x.strip())
        severities = tuple(float(x) for x in args.severities.split(",") if x.strip())
        modes = tuple(x.strip() for x in args.modes.split(",") if x.strip())
        max_targets = None if args.max_targets < 0 else args.max_targets
        return cls(
            seeds=seeds,
            steps=args.steps,
            max_parents=args.max_parents,
            target_frontier_min=args.target_frontier_min,
            branch_probability=args.branch_probability,
            wide_join_probability=args.wide_join_probability,
            conflict_rate=args.conflict_rate,
            defect_rate=args.defect_rate,
            orientation_defect_rate=args.orientation_defect_rate,
            conflict_witness_defect_rate=args.conflict_witness_defect_rate,
            severance_seeds=severance_seeds,
            severities=severities,
            modes=modes,
            selector_mode=args.selector_mode,
            selector_tie_policy=args.selector_tie_policy,
            include_alternatives=args.include_alternatives,
            max_targets=max_targets,
            sample_limit=args.sample_limit,
        )

    def expected_evaluations_upper_bound(self) -> int:
        target_factor = self.max_targets if self.max_targets is not None else self.steps
        alt_factor = 3 if self.include_alternatives else 1
        return len(self.seeds) * len(self.severance_seeds) * len(self.modes) * len(self.severities) * target_factor * alt_factor


@dataclass(frozen=True)
class ChannelIntervention:
    """RA-native severance intervention with explicit channel semantics."""

    mode: str
    severity: float
    seed: int = 0

    def __post_init__(self) -> None:
        if self.mode not in SEVERANCE_MODES:
            raise ValueError(f"unknown severance mode: {self.mode}")
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError("severity must lie in [0, 1]")


@dataclass(frozen=True)
class ChannelEvaluation:
    """Before/after diagnostics with separated support/readiness channels."""

    motif: str
    site: int
    mode: str
    severity: float
    seed: int
    support_width: int
    before_supported: bool
    before_causally_ready: bool
    before_operationally_ready: bool
    before_strict_commits: bool
    before_selected_commits: bool
    after_supported: bool
    after_causally_ready: bool
    after_support_available: bool
    after_operationally_ready: bool
    after_strict_commits: bool
    after_selected_commits: bool
    lost_support_certification: bool
    lost_causal_reachability: bool
    lost_support_availability: bool
    lost_operational_readiness: bool
    lost_strict_commit: bool
    lost_selected_commit: bool
    ledger_gate_loss: bool
    orientation_gate_loss: bool
    selector_stress_loss: bool
    finality_depth_before: Optional[int]
    finality_depth_after: Optional[int]
    finality_depth_shift: Optional[int]
    recovery_length: Optional[int]
    affected_support_vertices: Tuple[int, ...]
    affected_edge_count: int
    added_competitors: int
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
            "before_causally_ready": self.before_causally_ready,
            "before_operationally_ready": self.before_operationally_ready,
            "before_strict_commits": self.before_strict_commits,
            "before_selected_commits": self.before_selected_commits,
            "after_supported": self.after_supported,
            "after_causally_ready": self.after_causally_ready,
            "after_support_available": self.after_support_available,
            "after_operationally_ready": self.after_operationally_ready,
            "after_strict_commits": self.after_strict_commits,
            "after_selected_commits": self.after_selected_commits,
            "lost_support_certification": self.lost_support_certification,
            "lost_causal_reachability": self.lost_causal_reachability,
            "lost_support_availability": self.lost_support_availability,
            "lost_operational_readiness": self.lost_operational_readiness,
            "lost_strict_commit": self.lost_strict_commit,
            "lost_selected_commit": self.lost_selected_commit,
            "ledger_gate_loss": self.ledger_gate_loss,
            "orientation_gate_loss": self.orientation_gate_loss,
            "selector_stress_loss": self.selector_stress_loss,
            "finality_depth_before": self.finality_depth_before,
            "finality_depth_after": self.finality_depth_after,
            "finality_depth_shift": self.finality_depth_shift,
            "recovery_length": self.recovery_length,
            "affected_support_vertices": list(self.affected_support_vertices),
            "affected_edge_count": self.affected_edge_count,
            "added_competitors": self.added_competitors,
            "intervention_detail": self.intervention_detail,
        }


@dataclass
class ChannelSeedState:
    dag: CausalDAG
    motifs: List[MotifCandidate]
    support_widths: Tuple[int, ...]


def _frontier_sample(rng: random.Random, frontier: Sequence[int], *, k: int) -> Set[int]:
    if not frontier:
        return set()
    k = max(1, min(k, len(frontier)))
    return set(rng.sample(list(frontier), k=k))


def generate_support_diverse_growth_state(
    *,
    steps: int = 24,
    seed: int = 17,
    max_parents: int = 4,
    target_frontier_min: int = 5,
    branch_probability: float = 0.42,
    wide_join_probability: float = 0.72,
    conflict_rate: float = 0.22,
    defect_rate: float = 0.02,
    orientation_defect_rate: float = 0.02,
    conflict_witness_defect_rate: float = 0.08,
) -> Tuple[CausalDAG, List[MotifCandidate]]:
    """Generate a DAG with support-frontier width diversity.

    Earlier growth used the current maximal frontier too aggressively, often
    collapsing the active frontier to width 1. Here we intentionally maintain
    multiple active strands and occasionally join incomparable frontier vertices.
    This gives the Hasse-frontier support cut genuine width variation.
    """

    rng = random.Random(seed)
    dag = CausalDAG()
    genesis = dag.add_node()
    motifs: List[MotifCandidate] = [
        MotifCandidate(
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
                    "closure": {
                        "selector_compatible": True,
                        "no_extra_random_labels": True,
                        "no_particle_label_primitives": True,
                        "qN1_signature": 7,
                        "local_conserved": True,
                        "sign_links": [],
                    },
                },
                "defect_tags": [],
                "support_width": 0,
            },
        )
    ]

    for step in range(steps):
        existing = list(dag.nodes)
        frontier = [n for n in dag.maximal_nodes() if n != genesis] or list(dag.maximal_nodes())
        spawn_new_strand = len(frontier) < target_frontier_min or rng.random() < branch_probability

        if spawn_new_strand:
            # Attach to a shallow/base vertex to create a new active strand while
            # preserving the existing frontier. This avoids immediate reduction
            # back to a single maximal node.
            shallow = [n for n in existing if dag.depth[n] <= 1] or [genesis]
            parents = {rng.choice(shallow)}
            event_kind = "branch_spawn"
        else:
            max_k = min(max_parents, len(frontier))
            if max_k >= 2 and rng.random() < wide_join_probability:
                k = rng.randint(2, max_k)
                event_kind = "wide_frontier_join"
            else:
                k = 1
                event_kind = "single_frontier_extension"
            parents = _frontier_sample(rng, frontier, k=k)

        site = dag.add_node(parents)
        past = dag.candidate_past_from_support(parents)
        support_cut = dag.support_cut_of_finite_hasse_frontier(past)
        meta = _metadata_with_gates(
            rng=rng,
            candidate_past=past,
            parents=parents,
            support_cut=support_cut,
            site=site,
            defect_rate=defect_rate,
            orientation_defect_rate=orientation_defect_rate,
        )
        meta["support_width"] = len(support_cut)
        meta["growth_event_kind"] = event_kind
        motifs.append(MotifCandidate(f"renewal_{site}", frozenset({site}), support_cut, "renewal", priority=2, metadata=meta))

        if rng.random() < conflict_rate:
            domain = f"orientation_choice_at_{site}"
            for label in ("A", "B"):
                cmeta = _metadata_with_gates(
                    rng=rng,
                    candidate_past=past,
                    parents=parents,
                    support_cut=support_cut,
                    site=site,
                    defect_rate=defect_rate,
                    orientation_defect_rate=orientation_defect_rate,
                )
                cmeta["support_width"] = len(support_cut)
                cmeta["growth_event_kind"] = event_kind
                cmeta["orientation_conflict_domain"] = domain
                cmeta["orientation_conflict_ok"] = not (conflict_witness_defect_rate > 0 and rng.random() < conflict_witness_defect_rate)
                motifs.append(MotifCandidate(f"choice_{label}_{site}", frozenset({site}), support_cut, "alternative", exclusion_domain=domain, priority=1, metadata=cmeta))
    return dag, motifs


def build_channel_seed_state(config: ChannelSeparatedRunConfig, seed: int) -> ChannelSeedState:
    dag, motifs = generate_support_diverse_growth_state(
        steps=config.steps,
        seed=seed,
        max_parents=config.max_parents,
        target_frontier_min=config.target_frontier_min,
        branch_probability=config.branch_probability,
        wide_join_probability=config.wide_join_probability,
        conflict_rate=config.conflict_rate,
        defect_rate=config.defect_rate,
        orientation_defect_rate=config.orientation_defect_rate,
        conflict_witness_defect_rate=config.conflict_witness_defect_rate,
    )
    widths = tuple(sorted({len(m.support_cut) for m in motifs if m.support_cut}))
    return ChannelSeedState(dag=dag, motifs=list(motifs), support_widths=widths)


def target_motifs_for_channel_severance(motifs: Sequence[MotifCandidate], *, include_alternatives: bool = False, max_targets: Optional[int] = 18) -> Tuple[MotifCandidate, ...]:
    kinds = {"renewal", "alternative"} if include_alternatives else {"renewal"}
    candidates = [m for m in motifs if m.kind in kinds and m.carrier and m.support_cut]
    # Prefer a width-diverse prefix rather than simply earliest motifs.
    by_width: Dict[int, List[MotifCandidate]] = {}
    for m in candidates:
        by_width.setdefault(len(m.support_cut), []).append(m)
    ordered: List[MotifCandidate] = []
    while any(by_width.values()):
        for width in sorted(by_width):
            if by_width[width]:
                ordered.append(by_width[width].pop(0))
                if max_targets is not None and len(ordered) >= max_targets:
                    return tuple(ordered)
    return tuple(ordered)


def causal_edges_inside_site_past(dag: CausalDAG, site: int) -> Tuple[Tuple[int, int], ...]:
    past = dag.ancestors(site, include_self=True)
    return tuple(sorted((p, c) for c in past for p in dag.parents[c] if p in past))


def choose_fraction(items: Sequence[Any], severity: float, rng: random.Random) -> Tuple[Any, ...]:
    if severity <= 0 or not items:
        return ()
    shuffled = list(items)
    rng.shuffle(shuffled)
    k = max(1, min(len(shuffled), int(math.ceil(severity * len(shuffled)))))
    return tuple(shuffled[:k])


def _stochastic_gate(severity: float, rng: random.Random) -> bool:
    return severity > 0 and rng.random() < severity


def _support_available(support_cut: SupportCut, unavailable: FrozenSet[int]) -> bool:
    return not bool(unavailable.intersection(support_cut))


def evaluate_channel_severance(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    intervention: ChannelIntervention,
    *,
    selector_mode: str = "greedy",
    selector_tie_policy: str = "lexicographic",
) -> ChannelEvaluation:
    """Evaluate one motif under separated severance-channel semantics."""

    dag = state.dag
    motifs = state.motifs
    base_protocol, selector = protocol_for(dag, motifs, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy, use_orientation_conflicts=True)
    before_decision = base_protocol.decision(motif, site)
    before_supported = before_decision.supported
    before_causal_ready = dag.ready_at(motif.support_cut, site)
    before_operational_ready = before_supported and before_causal_ready
    before_strict = before_decision.commits
    before_selected = selected_commit_bool(base_protocol, motif, site, selector)
    finality_before = min_finality_depth(dag, motif.support_cut)

    rng = random.Random(intervention.seed + 7919 * site + 104729 * len(motif.support_cut) + sum(ord(c) for c in motif.name) + int(intervention.severity * 10000))
    after_dag = dag
    after_motifs = list(motifs)
    after_motif = motif
    after_supported = before_supported
    after_causal_ready = before_causal_ready
    after_support_available = True
    after_strict = before_strict
    after_selected = before_selected
    unavailable_support: FrozenSet[int] = frozenset()
    delay_depth = 0
    affected_edges: Tuple[Tuple[int, int], ...] = ()
    added_competitors = 0
    ledger_gate_loss = False
    orientation_gate_loss = False
    selector_stress_loss = False
    detail = "no_change"

    if intervention.mode == "edge_dropout":
        affected_edges = tuple((int(a), int(b)) for a, b in choose_fraction(causal_edges_inside_site_past(dag, site), intervention.severity, rng))
        if affected_edges:
            after_dag = remove_edges(dag, affected_edges)
            after_causal_ready = after_dag.ready_at(motif.support_cut, site)
            # Certification remains the same channel here; edge dropout tests
            # whether the certified support still reaches the site.
            after_strict = before_strict and after_supported and after_causal_ready
            after_selected = before_selected and after_supported and after_causal_ready
        detail = f"removed_edges={list(affected_edges)}"

    elif intervention.mode == "frontier_dropout":
        unavailable_support = frozenset(int(x) for x in choose_fraction(tuple(sorted(motif.support_cut)), intervention.severity, rng))
        after_support_available = _support_available(motif.support_cut, unavailable_support)
        after_causal_ready = before_causal_ready and after_support_available
        # Dropout is availability loss, not certificate loss.
        after_supported = before_supported
        after_strict = before_strict and after_supported and after_causal_ready
        after_selected = before_selected and after_supported and after_causal_ready
        detail = f"unavailable_support_vertices={sorted(unavailable_support)}"

    elif intervention.mode == "support_delay":
        delay_depth = int(round(intervention.severity * 5))
        if delay_depth > 0:
            after_causal_ready = False
            after_strict = False
            after_selected = False
        detail = f"delay_depth={delay_depth}"

    elif intervention.mode == "orientation_degradation":
        orientation_gate_loss = _stochastic_gate(intervention.severity, rng)
        if orientation_gate_loss:
            after_motif = clone_motif(motif, metadata=degraded_orientation_metadata(motif.metadata, 1.0))
            after_motifs = [after_motif if m.name == motif.name else m for m in motifs]
        after_protocol, after_selector = protocol_for(after_dag, after_motifs, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy, use_orientation_conflicts=True)
        after_decision = after_protocol.decision(after_motif, site)
        after_supported = after_decision.supported
        after_causal_ready = before_causal_ready
        after_strict = after_decision.commits
        after_selected = selected_commit_bool(after_protocol, after_motif, site, after_selector)
        detail = f"orientation_gate_loss={orientation_gate_loss} probability={intervention.severity}"

    elif intervention.mode == "ledger_failure":
        ledger_gate_loss = _stochastic_gate(intervention.severity, rng)
        if ledger_gate_loss:
            after_motif = clone_motif(motif, metadata=degraded_ledger_metadata(motif.metadata, 1.0))
            after_motifs = [after_motif if m.name == motif.name else m for m in motifs]
        after_protocol, after_selector = protocol_for(after_dag, after_motifs, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy, use_orientation_conflicts=True)
        after_decision = after_protocol.decision(after_motif, site)
        after_supported = after_decision.supported
        after_causal_ready = before_causal_ready
        after_strict = after_decision.commits
        after_selected = selected_commit_bool(after_protocol, after_motif, site, after_selector)
        detail = f"ledger_gate_loss={ledger_gate_loss} probability={intervention.severity}"

    elif intervention.mode == "selector_stress":
        domain = f"channel_selector_stress:{motif.name}:{site}"
        after_motif = clone_motif(motif, metadata=with_conflict_domain(motif.metadata, domain), exclusion_domain=domain)
        after_motifs = [after_motif if m.name == motif.name else m for m in motifs]
        added_competitors = int(round(intervention.severity * 3))
        for idx in range(added_competitors):
            comp = clone_motif(
                motif,
                name=f"stress_{idx}_{motif.name}",
                metadata=with_conflict_domain(motif.metadata, domain),
                priority=motif.priority,
                exclusion_domain=domain,
            )
            after_motifs.append(comp)
        after_protocol, after_selector = protocol_for(after_dag, after_motifs, selector_mode=selector_mode, selector_tie_policy=selector_tie_policy, use_orientation_conflicts=True)
        after_decision = after_protocol.decision(after_motif, site)
        after_supported = after_decision.supported
        after_causal_ready = before_causal_ready
        after_strict = after_decision.commits
        after_selected = selected_commit_bool(after_protocol, after_motif, site, after_selector)
        selector_stress_loss = before_strict and not after_strict and after_supported and after_causal_ready
        detail = f"added_incompatible_competitors={added_competitors} domain={domain}"

    finality_after = min_finality_depth(after_dag, motif.support_cut)
    if intervention.mode == "support_delay" and finality_after is not None:
        finality_after += delay_depth
    if not after_support_available:
        finality_after = None
    shift = None if finality_before is None or finality_after is None else finality_after - finality_before
    recovery = readiness_recovery_length(after_dag, motif.support_cut, site, unavailable_support=unavailable_support, delay_depth=delay_depth)

    after_operational_ready = after_supported and after_causal_ready and after_support_available
    return ChannelEvaluation(
        motif=motif.name,
        site=site,
        mode=intervention.mode,
        severity=intervention.severity,
        seed=intervention.seed,
        support_width=len(motif.support_cut),
        before_supported=before_supported,
        before_causally_ready=before_causal_ready,
        before_operationally_ready=before_operational_ready,
        before_strict_commits=before_strict,
        before_selected_commits=before_selected,
        after_supported=after_supported,
        after_causally_ready=after_causal_ready,
        after_support_available=after_support_available,
        after_operationally_ready=after_operational_ready,
        after_strict_commits=after_strict,
        after_selected_commits=after_selected,
        lost_support_certification=before_supported and not after_supported,
        lost_causal_reachability=before_causal_ready and not after_causal_ready,
        lost_support_availability=not after_support_available,
        lost_operational_readiness=before_operational_ready and not after_operational_ready,
        lost_strict_commit=before_strict and not after_strict,
        lost_selected_commit=before_selected and not after_selected,
        ledger_gate_loss=ledger_gate_loss,
        orientation_gate_loss=orientation_gate_loss,
        selector_stress_loss=selector_stress_loss,
        finality_depth_before=finality_before,
        finality_depth_after=finality_after,
        finality_depth_shift=shift,
        recovery_length=recovery,
        affected_support_vertices=tuple(sorted(unavailable_support)),
        affected_edge_count=len(affected_edges),
        added_competitors=added_competitors,
        intervention_detail=detail,
    )


def iter_channel_rows_for_seed(config: ChannelSeparatedRunConfig, seed: int) -> Iterator[Dict[str, object]]:
    state = build_channel_seed_state(config, seed)
    targets = target_motifs_for_channel_severance(state.motifs, include_alternatives=config.include_alternatives, max_targets=config.max_targets)
    for severance_seed in config.severance_seeds:
        for mode in config.modes:
            for severity in config.severities:
                intervention = ChannelIntervention(mode=mode, severity=float(severity), seed=int(severance_seed))
                for motif in targets:
                    site = motif_site(motif)
                    if site < 0:
                        continue
                    ev = evaluate_channel_severance(state, motif, site, intervention, selector_mode=config.selector_mode, selector_tie_policy=config.selector_tie_policy)
                    row = ev.to_row()
                    row["run_seed"] = seed
                    row["nodes"] = len(state.dag.nodes)
                    row["edges"] = len(state.dag.edges)
                    row["motifs"] = len(state.motifs)
                    row["target_count"] = len(targets)
                    row["support_width_classes_in_seed"] = list(state.support_widths)
                    yield row


def _rate(items: Sequence[Mapping[str, object]], key: str) -> float:
    return round(sum(1 for r in items if bool(r.get(key))) / len(items), 6) if items else 0.0


def _mean(values: Sequence[float]) -> Optional[float]:
    return round(sum(values) / len(values), 6) if values else None


def _non_null_numeric(items: Sequence[Mapping[str, object]], key: str) -> List[float]:
    out: List[float] = []
    for r in items:
        v = r.get(key)
        if v is not None and v != "":
            out.append(float(v))
    return out


def summarize_channel_aggregate(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, float], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["mode"]), float(r["severity"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, severity), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "severity": severity,
            "samples": len(items),
            "mean_support_width": _mean([float(r.get("support_width", 0)) for r in items]),
            "support_width_count": len({int(r.get("support_width", 0)) for r in items}),
            "support_certification_loss_rate": _rate(items, "lost_support_certification"),
            "causal_reachability_loss_rate": _rate(items, "lost_causal_reachability"),
            "support_availability_loss_rate": _rate(items, "lost_support_availability"),
            "operational_readiness_loss_rate": _rate(items, "lost_operational_readiness"),
            "strict_commit_loss_rate": _rate(items, "lost_strict_commit"),
            "selected_commit_loss_rate": _rate(items, "lost_selected_commit"),
            "ledger_gate_loss_rate": _rate(items, "ledger_gate_loss"),
            "orientation_gate_loss_rate": _rate(items, "orientation_gate_loss"),
            "selector_stress_loss_rate": _rate(items, "selector_stress_loss"),
            "mean_finality_depth_shift": _mean(_non_null_numeric(items, "finality_depth_shift")),
            "mean_recovery_length": _mean(_non_null_numeric(items, "recovery_length")),
        })
    return out


def summarize_width_fragility(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, float, int], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["mode"]), float(r["severity"]), int(r.get("support_width", 0))), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, severity, width), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "severity": severity,
            "support_width": width,
            "samples": len(items),
            "support_certification_loss_rate": _rate(items, "lost_support_certification"),
            "causal_reachability_loss_rate": _rate(items, "lost_causal_reachability"),
            "support_availability_loss_rate": _rate(items, "lost_support_availability"),
            "strict_commit_loss_rate": _rate(items, "lost_strict_commit"),
            "selected_commit_loss_rate": _rate(items, "lost_selected_commit"),
            "mean_finality_depth_shift": _mean(_non_null_numeric(items, "finality_depth_shift")),
            "mean_recovery_length": _mean(_non_null_numeric(items, "recovery_length")),
        })
    return out


def _signature_vector(row: Mapping[str, object]) -> Tuple[float, ...]:
    return (
        float(row.get("support_certification_loss_rate") or 0.0),
        float(row.get("causal_reachability_loss_rate") or 0.0),
        float(row.get("support_availability_loss_rate") or 0.0),
        float(row.get("strict_commit_loss_rate") or 0.0),
        float(row.get("selected_commit_loss_rate") or 0.0),
        float(row.get("ledger_gate_loss_rate") or 0.0),
        float(row.get("orientation_gate_loss_rate") or 0.0),
        float(row.get("selector_stress_loss_rate") or 0.0),
        (float(row.get("mean_finality_depth_shift") or 0.0) / 5.0),
        (float(row.get("mean_recovery_length") or 0.0) / 5.0),
    )


def summarize_mode_signatures(aggregate_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    by_mode: Dict[str, List[Mapping[str, object]]] = {}
    for r in aggregate_rows:
        if float(r.get("severity", 0.0)) <= 0:
            continue
        by_mode.setdefault(str(r["mode"]), []).append(r)
    out: List[Dict[str, object]] = []
    for mode, items in sorted(by_mode.items()):
        vectors = [_signature_vector(r) for r in items]
        if not vectors:
            continue
        means = tuple(sum(v[i] for v in vectors) / len(vectors) for i in range(len(vectors[0])))
        if mode == "frontier_dropout":
            classification = "frontier_availability_channel"
        elif mode == "edge_dropout":
            classification = "causal_reachability_channel"
        elif mode == "ledger_failure":
            classification = "ledger_certification_channel"
        elif mode == "orientation_degradation":
            classification = "orientation_witness_certification_channel"
        elif mode == "support_delay":
            classification = "delay_recovery_channel"
        elif mode == "selector_stress":
            classification = "selector_exclusion_channel"
        else:
            classification = "unclassified"
        out.append({
            "mode": mode,
            "classification": classification,
            "mean_support_certification_loss_rate": round(means[0], 6),
            "mean_causal_reachability_loss_rate": round(means[1], 6),
            "mean_support_availability_loss_rate": round(means[2], 6),
            "mean_strict_commit_loss_rate": round(means[3], 6),
            "mean_selected_commit_loss_rate": round(means[4], 6),
            "mean_ledger_gate_loss_rate": round(means[5], 6),
            "mean_orientation_gate_loss_rate": round(means[6], 6),
            "mean_selector_stress_loss_rate": round(means[7], 6),
            "mean_finality_shift_scaled": round(means[8], 6),
            "mean_recovery_length_scaled": round(means[9], 6),
        })
    return out


def mode_separability(aggregate_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    signatures = summarize_mode_signatures(aggregate_rows)
    vectors = {str(r["mode"]): (
        float(r["mean_support_certification_loss_rate"]),
        float(r["mean_causal_reachability_loss_rate"]),
        float(r["mean_support_availability_loss_rate"]),
        float(r["mean_strict_commit_loss_rate"]),
        float(r["mean_selected_commit_loss_rate"]),
        float(r["mean_ledger_gate_loss_rate"]),
        float(r["mean_orientation_gate_loss_rate"]),
        float(r["mean_selector_stress_loss_rate"]),
        float(r["mean_finality_shift_scaled"]),
        float(r["mean_recovery_length_scaled"]),
    ) for r in signatures}
    modes = sorted(vectors)
    out: List[Dict[str, object]] = []
    for i, a in enumerate(modes):
        for b in modes[i + 1:]:
            va, vb = vectors[a], vectors[b]
            dist = math.sqrt(sum((x - y) ** 2 for x, y in zip(va, vb)))
            na = math.sqrt(sum(x * x for x in va))
            nb = math.sqrt(sum(x * x for x in vb))
            cosine = sum(x * y for x, y in zip(va, vb)) / (na * nb) if na and nb else 0.0
            out.append({"mode_a": a, "mode_b": b, "euclidean_distance": round(dist, 6), "cosine_similarity": round(cosine, 6)})
    return out


def reservoir_sample(rows: Iterable[Dict[str, object]], limit: int) -> Tuple[List[Dict[str, object]], int]:
    out: List[Dict[str, object]] = []
    count = 0
    for row in rows:
        count += 1
        if limit <= 0:
            continue
        if len(out) < limit:
            out.append(dict(row))
        else:
            slot = (count * 1103515245 + 12345) % count
            if slot < limit:
                out[int(slot)] = dict(row)
    return out, count


def run_channel_ensemble(config: ChannelSeparatedRunConfig) -> Tuple[Dict[str, object], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    started = time.perf_counter()
    all_rows: List[Dict[str, object]] = []
    run_rows: List[Dict[str, object]] = []
    width_classes: Set[int] = set()
    for seed in config.seeds:
        seed_rows = list(iter_channel_rows_for_seed(config, seed))
        all_rows.extend(seed_rows)
        width_classes.update(int(r.get("support_width", 0)) for r in seed_rows)
        run_rows.append({
            "run_seed": seed,
            "evaluations": len(seed_rows),
            "support_width_classes": sorted({int(r.get("support_width", 0)) for r in seed_rows}),
            "support_certification_loss_rate": _rate(seed_rows, "lost_support_certification"),
            "causal_reachability_loss_rate": _rate(seed_rows, "lost_causal_reachability"),
            "support_availability_loss_rate": _rate(seed_rows, "lost_support_availability"),
            "strict_commit_loss_rate": _rate(seed_rows, "lost_strict_commit"),
            "selected_commit_loss_rate": _rate(seed_rows, "lost_selected_commit"),
        })
    elapsed = time.perf_counter() - started
    aggregate_rows = summarize_channel_aggregate(all_rows)
    width_rows = summarize_width_fragility(all_rows)
    signatures = summarize_mode_signatures(aggregate_rows)
    separability = mode_separability(aggregate_rows)
    sample_rows, _ = reservoir_sample(iter(all_rows), config.sample_limit)
    summary = {
        "version": "0.6",
        "run_count": len(config.seeds),
        "steps": config.steps,
        "actual_evaluations": len(all_rows),
        "sampled_evaluations": len(sample_rows),
        "elapsed_seconds": round(elapsed, 6),
        "evaluations_per_second": round(len(all_rows) / elapsed, 6) if elapsed > 0 else None,
        "support_width_classes": sorted(width_classes),
        "support_width_count": len(width_classes),
        "total_lost_support_certification": sum(1 for r in all_rows if bool(r.get("lost_support_certification"))),
        "total_lost_causal_reachability": sum(1 for r in all_rows if bool(r.get("lost_causal_reachability"))),
        "total_lost_support_availability": sum(1 for r in all_rows if bool(r.get("lost_support_availability"))),
        "total_lost_operational_readiness": sum(1 for r in all_rows if bool(r.get("lost_operational_readiness"))),
        "total_lost_strict_commit": sum(1 for r in all_rows if bool(r.get("lost_strict_commit"))),
        "total_lost_selected_commit": sum(1 for r in all_rows if bool(r.get("lost_selected_commit"))),
    }
    return summary, run_rows, aggregate_rows, width_rows, signatures, separability, sample_rows


def write_channel_predictions(summary: Mapping[str, object], signatures: Sequence[Mapping[str, object]], separability: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    zero_pairs = [r for r in separability if float(r.get("euclidean_distance", 0.0)) == 0.0]
    closest = sorted(separability, key=lambda r: float(r.get("euclidean_distance", 0.0)))[:5]
    text = [
        "# RA Channel-Separated Severance Signature Note — v0.6",
        "",
        "This note is RA-native. It reports simulator signatures for separated actualization-fragility channels.",
        "",
        "## Scale",
        "",
        f"- run_count: {summary.get('run_count')}",
        f"- steps: {summary.get('steps')}",
        f"- actual_evaluations: {summary.get('actual_evaluations')}",
        f"- support_width_classes: {summary.get('support_width_classes')}",
        "",
        "## Mode classifications",
        "",
    ]
    for r in signatures:
        text.append(
            f"- {r['mode']}: {r['classification']} "
            f"(support_cert={r['mean_support_certification_loss_rate']}, "
            f"causal_reach={r['mean_causal_reachability_loss_rate']}, "
            f"availability={r['mean_support_availability_loss_rate']}, "
            f"ledger={r['mean_ledger_gate_loss_rate']}, "
            f"orientation={r['mean_orientation_gate_loss_rate']}, "
            f"selector={r['mean_selector_stress_loss_rate']})."
        )
    text += [
        "",
        "## Separability check",
        "",
        f"- zero-distance mode pairs: {len(zero_pairs)}.",
        "- nearest pairs:",
    ]
    for r in closest:
        text.append(f"  - {r['mode_a']} vs {r['mode_b']}: distance={r['euclidean_distance']}, cosine={r['cosine_similarity']}.")
    text += [
        "",
        "## Interpretation",
        "",
        "v0.6 separates support certification, causal reachability, support availability, and selector exclusion. Therefore a high commitment-loss rate no longer compresses distinct severance modes into a single undiagnosed failure channel.",
        "",
        "The support-diverse generator also exposes frontier widths greater than one, enabling support-width fragility analysis that was blocked in the v0.5.1/v0.5.2 ensembles.",
    ]
    path.write_text("\n".join(text) + "\n", encoding="utf-8")


def write_json_state(summary: Mapping[str, object], run_rows: Sequence[Mapping[str, object]], aggregate_rows: Sequence[Mapping[str, object]], width_rows: Sequence[Mapping[str, object]], signatures: Sequence[Mapping[str, object]], separability: Sequence[Mapping[str, object]], sample_rows: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "0.6",
        "summary": dict(summary),
        "runs": list(run_rows),
        "aggregate": list(aggregate_rows),
        "width_fragility": list(width_rows),
        "signatures": list(signatures),
        "separability": list(separability),
        "sample_evaluations": list(sample_rows),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run RA causal-DAG v0.6 channel-separated severance ensemble.")
    p.add_argument("--seed-start", type=int, default=17)
    p.add_argument("--seed-stop", type=int, default=37)
    p.add_argument("--seed-list", type=str, default=None)
    p.add_argument("--steps", type=int, default=24)
    p.add_argument("--max-parents", type=int, default=4)
    p.add_argument("--target-frontier-min", type=int, default=5)
    p.add_argument("--branch-probability", type=float, default=0.42)
    p.add_argument("--wide-join-probability", type=float, default=0.72)
    p.add_argument("--conflict-rate", type=float, default=0.22)
    p.add_argument("--defect-rate", type=float, default=0.02)
    p.add_argument("--orientation-defect-rate", type=float, default=0.02)
    p.add_argument("--conflict-witness-defect-rate", type=float, default=0.08)
    p.add_argument("--severance-seeds", type=str, default="101,103")
    p.add_argument("--severities", type=str, default="0.0,0.25,0.50,0.75,1.0")
    p.add_argument("--modes", type=str, default=",".join(SEVERANCE_MODES))
    p.add_argument("--selector-mode", type=str, default="greedy")
    p.add_argument("--selector-tie-policy", type=str, default="lexicographic")
    p.add_argument("--include-alternatives", action="store_true")
    p.add_argument("--max-targets", type=int, default=18)
    p.add_argument("--sample-limit", type=int, default=2000)
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return p


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_arg_parser().parse_args(argv)
    config = ChannelSeparatedRunConfig.from_args(args)
    summary, run_rows, aggregate_rows, width_rows, signatures, separability, sample_rows = run_channel_ensemble(config)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    rows_to_csv([summary], out / "ra_channel_separation_summary_v0_6.csv")
    rows_to_csv(run_rows, out / "ra_channel_separation_runs_v0_6.csv")
    rows_to_csv(aggregate_rows, out / "ra_channel_separation_aggregate_v0_6.csv")
    rows_to_csv(aggregate_rows, out / "ra_channel_resolved_fragility_v0_6.csv")
    rows_to_csv(aggregate_rows, out / "ra_gate_failure_decomposition_v0_6.csv")
    rows_to_csv(width_rows, out / "ra_support_width_fragility_v0_6.csv")
    rows_to_csv(width_rows, out / "ra_support_width_fragility_curve_v0_6.csv")
    rows_to_csv(width_rows, out / "ra_redundancy_survival_profiles_v0_6.csv")
    rows_to_csv(signatures, out / "ra_channel_mode_signatures_v0_6.csv")
    rows_to_csv(signatures, out / "ra_threshold_vs_graded_classification_v0_6.csv")
    rows_to_csv(separability, out / "ra_channel_mode_separability_v0_6.csv")
    rows_to_csv(separability, out / "ra_mode_separability_channel_resolved_v0_6.csv")
    rows_to_csv(sample_rows, out / "ra_channel_evaluations_sample_v0_6.csv")
    write_channel_predictions(summary, signatures, separability, out / "ra_channel_separation_predictions_v0_6.md")
    write_json_state(summary, run_rows, aggregate_rows, width_rows, signatures, separability, sample_rows, out / "ra_channel_separation_state_v0_6.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
