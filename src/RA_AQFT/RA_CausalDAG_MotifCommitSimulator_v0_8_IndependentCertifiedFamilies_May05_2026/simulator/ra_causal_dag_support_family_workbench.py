#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.7 support-family redundancy workbench.

v0.6 showed a crucial distinction: widening a *single* strict support cut
increases the number of required support vertices. Under edge dropout this can
increase fragility. v0.7 introduces a distinct RA-native object:

    support-cut family

A support-cut family represents alternative sufficient cuts for the same motif.
The current simulator instantiation uses threshold subfamilies over the same
Hasse-frontier support roles: for an original support cut Q of width n, a
threshold family at k contains the k-subsets of Q. Family readiness holds when
some certified cut in that family is ready.

This is a disciplined simulator abstraction, not a new foundational law. The
formal bridge is `RA_MotifSupportFamilyBridge.lean`; concrete support families
must still be justified by BDG-LLC / frontier / orientation / ledger evidence.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple

try:
    from .ra_causal_dag_simulator import (
        CausalDAG,
        MotifCandidate,
        SupportCut,
        min_finality_depth,
        motif_site,
        readiness_recovery_length,
        remove_edges,
        rows_to_csv,
    )
    from .ra_causal_dag_channel_workbench import (
        SEVERANCE_MODES,
        ChannelSeparatedRunConfig,
        ChannelSeedState,
        build_channel_seed_state,
        causal_edges_inside_site_past,
        choose_fraction,
        target_motifs_for_channel_severance,
    )
except ImportError:
    from ra_causal_dag_simulator import (  # type: ignore
        CausalDAG,
        MotifCandidate,
        SupportCut,
        min_finality_depth,
        motif_site,
        readiness_recovery_length,
        remove_edges,
        rows_to_csv,
    )
    from ra_causal_dag_channel_workbench import (  # type: ignore
        SEVERANCE_MODES,
        ChannelSeparatedRunConfig,
        ChannelSeedState,
        build_channel_seed_state,
        causal_edges_inside_site_past,
        choose_fraction,
        target_motifs_for_channel_severance,
    )


@dataclass(frozen=True)
class SupportFamilyRunConfig:
    """Parameters for the v0.7 support-family ensemble."""

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
    threshold_fractions: Tuple[float, ...] = (1.0, 0.75, 0.50, 0.25)
    include_alternatives: bool = False
    max_targets: Optional[int] = 18
    sample_limit: int = 2000

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "SupportFamilyRunConfig":
        seeds = tuple(range(args.seed_start, args.seed_stop)) if args.seed_list is None else tuple(int(x) for x in args.seed_list.split(",") if x.strip())
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
            severance_seeds=tuple(int(x) for x in args.severance_seeds.split(",") if x.strip()),
            severities=tuple(float(x) for x in args.severities.split(",") if x.strip()),
            modes=tuple(x.strip() for x in args.modes.split(",") if x.strip()),
            threshold_fractions=tuple(float(x) for x in args.threshold_fractions.split(",") if x.strip()),
            include_alternatives=args.include_alternatives,
            max_targets=None if args.max_targets < 0 else args.max_targets,
            sample_limit=args.sample_limit,
        )

    def channel_config(self, seed: int) -> ChannelSeparatedRunConfig:
        return ChannelSeparatedRunConfig(
            seeds=(seed,),
            steps=self.steps,
            max_parents=self.max_parents,
            target_frontier_min=self.target_frontier_min,
            branch_probability=self.branch_probability,
            wide_join_probability=self.wide_join_probability,
            conflict_rate=self.conflict_rate,
            defect_rate=self.defect_rate,
            orientation_defect_rate=self.orientation_defect_rate,
            conflict_witness_defect_rate=self.conflict_witness_defect_rate,
            severance_seeds=self.severance_seeds,
            severities=self.severities,
            modes=self.modes,
            include_alternatives=self.include_alternatives,
            max_targets=self.max_targets,
            sample_limit=self.sample_limit,
        )


@dataclass(frozen=True)
class SupportCutFamily:
    """Alternative sufficient support cuts for one motif.

    `threshold_k` records the threshold subfamily semantics used to construct
    the family in this workbench. The family is ready at a site when at least one
    certified cut in `cuts` is ready at that site.
    """

    motif: str
    base_support_cut: SupportCut
    cuts: Tuple[SupportCut, ...]
    threshold_k: int
    threshold_fraction: float

    @property
    def support_width(self) -> int:
        return len(self.base_support_cut)

    @property
    def family_size(self) -> int:
        return len(self.cuts)


@dataclass(frozen=True)
class FamilyInterventionState:
    after_dag: CausalDAG
    unavailable_support: FrozenSet[int]
    uncertified_cuts: FrozenSet[SupportCut]
    delay_depth: int
    selector_stress: bool
    affected_edges: Tuple[Tuple[int, int], ...]
    detail: str


@dataclass(frozen=True)
class SupportFamilyEvaluation:
    motif: str
    site: int
    mode: str
    severity: float
    seed: int
    support_width: int
    threshold_k: int
    threshold_fraction: float
    family_size: int
    strict_before_ready: bool
    family_before_ready: bool
    strict_after_ready: bool
    family_after_ready: bool
    strict_lost_readiness: bool
    family_lost_readiness: bool
    strict_survives: bool
    family_survives: bool
    family_rescues_strict_loss: bool
    strict_finality_depth_before: Optional[int]
    strict_finality_depth_after: Optional[int]
    family_recovery_length: Optional[int]
    strict_recovery_length: Optional[int]
    unavailable_support_count: int
    uncertified_cut_count: int
    affected_edge_count: int
    intervention_detail: str

    def to_row(self) -> Dict[str, object]:
        return {
            "motif": self.motif,
            "site": self.site,
            "mode": self.mode,
            "severity": self.severity,
            "seed": self.seed,
            "support_width": self.support_width,
            "threshold_k": self.threshold_k,
            "threshold_fraction": self.threshold_fraction,
            "family_size": self.family_size,
            "strict_before_ready": self.strict_before_ready,
            "family_before_ready": self.family_before_ready,
            "strict_after_ready": self.strict_after_ready,
            "family_after_ready": self.family_after_ready,
            "strict_lost_readiness": self.strict_lost_readiness,
            "family_lost_readiness": self.family_lost_readiness,
            "strict_survives": self.strict_survives,
            "family_survives": self.family_survives,
            "family_rescues_strict_loss": self.family_rescues_strict_loss,
            "strict_finality_depth_before": self.strict_finality_depth_before,
            "strict_finality_depth_after": self.strict_finality_depth_after,
            "family_recovery_length": self.family_recovery_length,
            "strict_recovery_length": self.strict_recovery_length,
            "unavailable_support_count": self.unavailable_support_count,
            "uncertified_cut_count": self.uncertified_cut_count,
            "affected_edge_count": self.affected_edge_count,
            "intervention_detail": self.intervention_detail,
        }


def threshold_k(width: int, fraction: float) -> int:
    if width <= 0:
        return 0
    return max(1, min(width, int(math.ceil(width * fraction))))


def threshold_support_family(motif: MotifCandidate, fraction: float) -> SupportCutFamily:
    base = tuple(sorted(motif.support_cut))
    k = threshold_k(len(base), fraction)
    if not base:
        cuts: Tuple[SupportCut, ...] = (frozenset(),)
    else:
        cuts = tuple(frozenset(c) for c in itertools.combinations(base, k))
    return SupportCutFamily(motif=motif.name, base_support_cut=motif.support_cut, cuts=cuts, threshold_k=k, threshold_fraction=float(fraction))


def family_ready_at(dag: CausalDAG, family: SupportCutFamily, site: int, *, unavailable: FrozenSet[int] = frozenset(), uncertified: FrozenSet[SupportCut] = frozenset(), delay_depth: int = 0) -> bool:
    if delay_depth > 0:
        return False
    for cut in family.cuts:
        if cut in uncertified:
            continue
        if unavailable.intersection(cut):
            continue
        if dag.ready_at(cut, site):
            return True
    return False


def strict_ready_at(dag: CausalDAG, support_cut: SupportCut, site: int, *, unavailable: FrozenSet[int] = frozenset(), uncertified: bool = False, delay_depth: int = 0) -> bool:
    if delay_depth > 0 or uncertified:
        return False
    if unavailable.intersection(support_cut):
        return False
    return dag.ready_at(support_cut, site)


def _rng_for(motif: MotifCandidate, site: int, mode: str, severity: float, seed: int, salt: int) -> random.Random:
    return random.Random(seed + 7919 * site + 104729 * len(motif.support_cut) + 15485863 * salt + sum(ord(c) for c in motif.name + mode) + int(severity * 10000))


def _uncertified_cuts_for_family(family: SupportCutFamily, severity: float, rng: random.Random) -> FrozenSet[SupportCut]:
    if severity <= 0 or not family.cuts:
        return frozenset()
    # Cut-level certification failure: the family survives if at least one
    # certified alternative cut remains ready.
    chosen = choose_fraction(list(family.cuts), severity, rng)
    return frozenset(chosen)


def _intervention_state(state: ChannelSeedState, motif: MotifCandidate, site: int, family: SupportCutFamily, *, mode: str, severity: float, seed: int) -> FamilyInterventionState:
    dag = state.dag
    rng = _rng_for(motif, site, mode, severity, seed, salt=17)
    unavailable: FrozenSet[int] = frozenset()
    uncertified: FrozenSet[SupportCut] = frozenset()
    delay_depth = 0
    selector_stress = False
    affected_edges: Tuple[Tuple[int, int], ...] = ()
    after_dag = dag
    detail = "no_change"

    if mode == "edge_dropout":
        affected_edges = tuple((int(a), int(b)) for a, b in choose_fraction(causal_edges_inside_site_past(dag, site), severity, rng))
        if affected_edges:
            after_dag = remove_edges(dag, affected_edges)
        detail = f"removed_edges={list(affected_edges)}"
    elif mode == "frontier_dropout":
        unavailable = frozenset(int(x) for x in choose_fraction(tuple(sorted(motif.support_cut)), severity, rng))
        detail = f"unavailable_support_vertices={sorted(unavailable)}"
    elif mode == "support_delay":
        # Support-family delay is role-local: only a severity-selected subset is
        # delayed. This lets alternative cuts survive if they avoid delayed roles.
        delayed = frozenset(int(x) for x in choose_fraction(tuple(sorted(motif.support_cut)), severity, rng))
        unavailable = delayed
        delay_depth = int(round(severity * 5)) if delayed else 0
        detail = f"delayed_support_vertices={sorted(delayed)} delay_depth={delay_depth}"
    elif mode == "ledger_failure":
        uncertified = _uncertified_cuts_for_family(family, severity, rng)
        detail = f"uncertified_family_cuts={len(uncertified)} channel=ledger"
    elif mode == "orientation_degradation":
        uncertified = _uncertified_cuts_for_family(family, severity, rng)
        detail = f"uncertified_family_cuts={len(uncertified)} channel=orientation"
    elif mode == "selector_stress":
        selector_stress = severity > 0
        detail = f"selector_stress={selector_stress}"
    else:
        raise ValueError(f"unknown severance mode: {mode}")

    return FamilyInterventionState(
        after_dag=after_dag,
        unavailable_support=unavailable,
        uncertified_cuts=uncertified,
        delay_depth=delay_depth,
        selector_stress=selector_stress,
        affected_edges=affected_edges,
        detail=detail,
    )


def _family_recovery_length(dag: CausalDAG, family: SupportCutFamily, site: int, *, unavailable: FrozenSet[int], uncertified: FrozenSet[SupportCut], delay_depth: int) -> Optional[int]:
    if family_ready_at(dag, family, site, unavailable=unavailable, uncertified=uncertified, delay_depth=0):
        return delay_depth
    lengths: List[int] = []
    for cut in family.cuts:
        if cut in uncertified or unavailable.intersection(cut):
            continue
        length = readiness_recovery_length(dag, cut, site, unavailable_support=frozenset(), delay_depth=0)
        if length is not None:
            lengths.append(length + delay_depth)
    return min(lengths) if lengths else None


def evaluate_support_family(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    *,
    threshold_fraction: float,
    mode: str,
    severity: float,
    seed: int,
) -> SupportFamilyEvaluation:
    family = threshold_support_family(motif, threshold_fraction)
    before_strict = strict_ready_at(state.dag, motif.support_cut, site)
    before_family = family_ready_at(state.dag, family, site)
    intervention = _intervention_state(state, motif, site, family, mode=mode, severity=severity, seed=seed)

    strict_uncertified = motif.support_cut in intervention.uncertified_cuts
    after_strict_ready = strict_ready_at(
        intervention.after_dag,
        motif.support_cut,
        site,
        unavailable=intervention.unavailable_support,
        uncertified=strict_uncertified,
        delay_depth=intervention.delay_depth,
    )
    after_family_ready = family_ready_at(
        intervention.after_dag,
        family,
        site,
        unavailable=intervention.unavailable_support,
        uncertified=intervention.uncertified_cuts,
        delay_depth=intervention.delay_depth,
    )

    # Selector stress acts on strict commitment / exclusion rather than support
    # readiness. It does not change family readiness in this bridge.
    strict_survives = after_strict_ready and not intervention.selector_stress
    family_survives = after_family_ready and not intervention.selector_stress
    if mode == "selector_stress":
        family_survives = after_family_ready

    finality_before = min_finality_depth(state.dag, motif.support_cut)
    finality_after = min_finality_depth(intervention.after_dag, motif.support_cut)
    if intervention.delay_depth and finality_after is not None:
        finality_after += intervention.delay_depth
    strict_recovery = readiness_recovery_length(
        intervention.after_dag,
        motif.support_cut,
        site,
        unavailable_support=intervention.unavailable_support,
        delay_depth=intervention.delay_depth,
    )
    family_recovery = _family_recovery_length(
        intervention.after_dag,
        family,
        site,
        unavailable=intervention.unavailable_support,
        uncertified=intervention.uncertified_cuts,
        delay_depth=intervention.delay_depth,
    )
    return SupportFamilyEvaluation(
        motif=motif.name,
        site=site,
        mode=mode,
        severity=severity,
        seed=seed,
        support_width=len(motif.support_cut),
        threshold_k=family.threshold_k,
        threshold_fraction=family.threshold_fraction,
        family_size=family.family_size,
        strict_before_ready=before_strict,
        family_before_ready=before_family,
        strict_after_ready=after_strict_ready,
        family_after_ready=after_family_ready,
        strict_lost_readiness=before_strict and not after_strict_ready,
        family_lost_readiness=before_family and not after_family_ready,
        strict_survives=strict_survives,
        family_survives=family_survives,
        family_rescues_strict_loss=(before_strict and not after_strict_ready and after_family_ready),
        strict_finality_depth_before=finality_before,
        strict_finality_depth_after=finality_after,
        family_recovery_length=family_recovery,
        strict_recovery_length=strict_recovery,
        unavailable_support_count=len(intervention.unavailable_support),
        uncertified_cut_count=len(intervention.uncertified_cuts),
        affected_edge_count=len(intervention.affected_edges),
        intervention_detail=intervention.detail,
    )


def iter_family_rows_for_seed(config: SupportFamilyRunConfig, seed: int) -> Iterator[Dict[str, object]]:
    state = build_channel_seed_state(config.channel_config(seed), seed)
    targets = target_motifs_for_channel_severance(state.motifs, include_alternatives=config.include_alternatives, max_targets=config.max_targets)
    for severance_seed in config.severance_seeds:
        for mode in config.modes:
            for severity in config.severities:
                for motif in targets:
                    site = motif_site(motif)
                    if site < 0 or not motif.support_cut:
                        continue
                    for fraction in config.threshold_fractions:
                        ev = evaluate_support_family(state, motif, site, threshold_fraction=fraction, mode=mode, severity=float(severity), seed=int(severance_seed))
                        row = ev.to_row()
                        row["run_seed"] = seed
                        row["nodes"] = len(state.dag.nodes)
                        row["edges"] = len(state.dag.edges)
                        row["motifs"] = len(state.motifs)
                        row["target_count"] = len(targets)
                        row["support_width_classes_in_seed"] = list(state.support_widths)
                        yield row


def _rate(rows: Sequence[Mapping[str, object]], key: str) -> float:
    return round(sum(1 for r in rows if bool(r.get(key))) / len(rows), 6) if rows else 0.0


def _mean(values: Sequence[float]) -> Optional[float]:
    return round(sum(values) / len(values), 6) if values else None


def _non_null_numeric(rows: Sequence[Mapping[str, object]], key: str) -> List[float]:
    out: List[float] = []
    for r in rows:
        v = r.get(key)
        if v is not None and v != "":
            out.append(float(v))
    return out


def aggregate_family_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, float, float], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["mode"]), float(r["severity"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, severity, fraction), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "severity": severity,
            "threshold_fraction": fraction,
            "samples": len(items),
            "mean_support_width": _mean([float(r.get("support_width", 0)) for r in items]),
            "support_width_count": len({int(r.get("support_width", 0)) for r in items}),
            "mean_family_size": _mean([float(r.get("family_size", 0)) for r in items]),
            "strict_readiness_loss_rate": _rate(items, "strict_lost_readiness"),
            "family_readiness_loss_rate": _rate(items, "family_lost_readiness"),
            "strict_survival_rate": _rate(items, "strict_survives"),
            "family_survival_rate": _rate(items, "family_survives"),
            "family_rescue_rate": _rate(items, "family_rescues_strict_loss"),
            "mean_family_recovery_length": _mean(_non_null_numeric(items, "family_recovery_length")),
            "mean_strict_recovery_length": _mean(_non_null_numeric(items, "strict_recovery_length")),
            "mean_uncertified_cut_count": _mean([float(r.get("uncertified_cut_count", 0)) for r in items]),
            "mean_unavailable_support_count": _mean([float(r.get("unavailable_support_count", 0)) for r in items]),
        })
    return out


def width_family_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, float, float, int], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["mode"]), float(r["severity"]), float(r["threshold_fraction"]), int(r["support_width"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, severity, fraction, width), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "severity": severity,
            "threshold_fraction": fraction,
            "support_width": width,
            "samples": len(items),
            "strict_readiness_loss_rate": _rate(items, "strict_lost_readiness"),
            "family_readiness_loss_rate": _rate(items, "family_lost_readiness"),
            "family_rescue_rate": _rate(items, "family_rescues_strict_loss"),
            "mean_family_size": _mean([float(r.get("family_size", 0)) for r in items]),
            "mean_family_recovery_length": _mean(_non_null_numeric(items, "family_recovery_length")),
        })
    return out


def threshold_curve_rows(aggregate: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for r in aggregate:
        strict_loss = float(r.get("strict_readiness_loss_rate") or 0.0)
        family_loss = float(r.get("family_readiness_loss_rate") or 0.0)
        out.append({
            "mode": r["mode"],
            "severity": r["severity"],
            "threshold_fraction": r["threshold_fraction"],
            "strict_readiness_loss_rate": strict_loss,
            "family_readiness_loss_rate": family_loss,
            "loss_reduction_vs_strict": round(strict_loss - family_loss, 6),
            "family_rescue_rate": r.get("family_rescue_rate"),
            "mean_family_size": r.get("mean_family_size"),
        })
    return out


def mode_signature_rows(aggregate: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    # Signature at each threshold fraction, using nonzero severities only.
    buckets: Dict[Tuple[str, float], List[Mapping[str, object]]] = {}
    for r in aggregate:
        if float(r.get("severity", 0.0)) <= 0:
            continue
        buckets.setdefault((str(r["mode"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, fraction), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "threshold_fraction": fraction,
            "mean_strict_loss": _mean([float(r.get("strict_readiness_loss_rate") or 0.0) for r in items]),
            "mean_family_loss": _mean([float(r.get("family_readiness_loss_rate") or 0.0) for r in items]),
            "mean_rescue": _mean([float(r.get("family_rescue_rate") or 0.0) for r in items]),
            "mean_family_size": _mean([float(r.get("mean_family_size") or 0.0) for r in items]),
        })
    return out


def run_support_family_ensemble(config: SupportFamilyRunConfig) -> Tuple[Dict[str, object], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    started = time.perf_counter()
    all_rows: List[Dict[str, object]] = []
    run_rows: List[Dict[str, object]] = []
    for seed in config.seeds:
        rows = list(iter_family_rows_for_seed(config, seed))
        all_rows.extend(rows)
        run_rows.append({
            "run_seed": seed,
            "evaluations": len(rows),
            "support_width_classes": sorted({int(r.get("support_width", 0)) for r in rows}),
            "threshold_fractions": sorted({float(r.get("threshold_fraction", 0.0)) for r in rows}),
            "family_rescue_rate": _rate(rows, "family_rescues_strict_loss"),
            "strict_readiness_loss_rate": _rate(rows, "strict_lost_readiness"),
            "family_readiness_loss_rate": _rate(rows, "family_lost_readiness"),
        })
    elapsed = time.perf_counter() - started
    aggregate = aggregate_family_rows(all_rows)
    width_rows = width_family_rows(all_rows)
    curve_rows = threshold_curve_rows(aggregate)
    signatures = mode_signature_rows(aggregate)
    summary = {
        "version": "0.7",
        "run_count": len(config.seeds),
        "steps": config.steps,
        "actual_evaluations": len(all_rows),
        "elapsed_seconds": round(elapsed, 6),
        "evaluations_per_second": round(len(all_rows) / elapsed, 6) if elapsed > 0 else None,
        "support_width_classes": sorted({int(r.get("support_width", 0)) for r in all_rows}),
        "support_width_count": len({int(r.get("support_width", 0)) for r in all_rows}),
        "threshold_fractions": sorted({float(r.get("threshold_fraction", 0.0)) for r in all_rows}),
        "total_strict_readiness_losses": sum(1 for r in all_rows if bool(r.get("strict_lost_readiness"))),
        "total_family_readiness_losses": sum(1 for r in all_rows if bool(r.get("family_lost_readiness"))),
        "total_family_rescues": sum(1 for r in all_rows if bool(r.get("family_rescues_strict_loss"))),
    }
    return summary, run_rows, aggregate, width_rows, curve_rows, signatures


def write_support_family_predictions(summary: Mapping[str, object], aggregate: Sequence[Mapping[str, object]], signatures: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notable = [r for r in aggregate if float(r.get("severity", 0.0)) > 0 and float(r.get("threshold_fraction", 1.0)) < 1.0]
    best = sorted(notable, key=lambda r: float(r.get("family_rescue_rate") or 0.0), reverse=True)[:8]
    text = [
        "# RA Support-Family Redundancy Signature Note — v0.7",
        "",
        "This note is RA-native. It compares strict single-cut readiness with support-family readiness.",
        "",
        "## Scale",
        "",
        f"- run_count: {summary.get('run_count')}",
        f"- steps: {summary.get('steps')}",
        f"- actual_evaluations: {summary.get('actual_evaluations')}",
        f"- support_width_classes: {summary.get('support_width_classes')}",
        f"- threshold_fractions: {summary.get('threshold_fractions')}",
        "",
        "## Interpretation",
        "",
        "A wider single support cut is an all-of-n obligation. A support-cut family is a set of alternative sufficient cuts. v0.7 therefore tests when support breadth becomes resilience rather than exposure.",
        "",
        "## Highest observed rescue regimes",
        "",
    ]
    if not best:
        text.append("- No nonzero family-rescue regimes in this run.")
    for r in best:
        text.append(
            f"- mode={r['mode']} severity={r['severity']} threshold={r['threshold_fraction']}: "
            f"family_rescue_rate={r['family_rescue_rate']}, "
            f"strict_loss={r['strict_readiness_loss_rate']}, family_loss={r['family_readiness_loss_rate']}."
        )
    text += [
        "",
        "## Methodological caution",
        "",
        "The threshold-subfamily construction is a simulator instantiation of the formal support-family bridge. It is not yet a derived physical law. Canonical runs should test whether the structural distinction between single-cut exposure and support-family resilience is robust under alternative family-generation rules.",
    ]
    path.write_text("\n".join(text) + "\n", encoding="utf-8")


def write_state(summary: Mapping[str, object], run_rows: Sequence[Mapping[str, object]], aggregate: Sequence[Mapping[str, object]], width_rows: Sequence[Mapping[str, object]], curve_rows: Sequence[Mapping[str, object]], signatures: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": "0.7",
        "summary": dict(summary),
        "runs": list(run_rows),
        "aggregate": list(aggregate),
        "width_rows": list(width_rows),
        "threshold_curves": list(curve_rows),
        "signatures": list(signatures),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run RA causal-DAG v0.7 support-family redundancy ensemble.")
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
    p.add_argument("--threshold-fractions", type=str, default="1.0,0.75,0.5,0.25")
    p.add_argument("--include-alternatives", action="store_true")
    p.add_argument("--max-targets", type=int, default=18)
    p.add_argument("--sample-limit", type=int, default=2000)
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return p


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_arg_parser().parse_args(argv)
    config = SupportFamilyRunConfig.from_args(args)
    summary, run_rows, aggregate, width_rows, curve_rows, signatures = run_support_family_ensemble(config)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    rows_to_csv([summary], out / "ra_support_family_summary_v0_7.csv")
    rows_to_csv(run_rows, out / "ra_support_family_runs_v0_7.csv")
    rows_to_csv(aggregate, out / "ra_support_family_comparison_v0_7.csv")
    rows_to_csv(curve_rows, out / "ra_support_family_threshold_curves_v0_7.csv")
    rows_to_csv(width_rows, out / "ra_support_family_resilience_by_width_v0_7.csv")
    rows_to_csv(signatures, out / "ra_support_family_mode_signatures_v0_7.csv")
    write_support_family_predictions(summary, aggregate, signatures, out / "ra_support_family_predictions_v0_7.md")
    write_state(summary, run_rows, aggregate, width_rows, curve_rows, signatures, out / "ra_support_family_state_v0_7.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
