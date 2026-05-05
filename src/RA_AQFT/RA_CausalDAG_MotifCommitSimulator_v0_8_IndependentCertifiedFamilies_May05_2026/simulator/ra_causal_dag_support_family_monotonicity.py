#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.7.1 support-family monotonicity audit.

v0.7 introduced support-cut families and showed that threshold subfamilies can
rescue reachability/availability-channel loss.  It also revealed a subtle but
important issue: an *exact-k* threshold family can be worse than the original
strict support cut under some certification-channel interventions, because the
family replaces the original cut rather than augmenting it.

v0.7.1 distinguishes three support-family semantics:

  exact_k
      all k-subsets of the base support cut.  This is the v0.7 semantics.
      It need not include the original full support cut when k < n.

  at_least_k
      all subsets of size >= k.  This includes the full support cut and is
      monotone as k decreases.

  augmented_exact_k
      the exact-k family plus the original full support cut.  This is the
      minimal additive redundancy variant of exact-k.

The module also compares two certification regimes:

  cut_level
      each family member cut can fail certification independently.

  parent_shared
      one parent support certificate gates the whole family.  This is useful for
      distinguishing support-route redundancy from certification redundancy.

This is a simulator audit layer, not a new RA law.  The formal bridge is
`RA_MotifSupportFamilyMonotonicity.lean`, which proves the abstract monotonicity
condition: if one family includes another, any-cut readiness propagates upward.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, FrozenSet, Iterator, List, Mapping, Optional, Sequence, Tuple

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
    from .ra_causal_dag_support_family_workbench import (
        FamilyInterventionState,
        SupportCutFamily,
        _family_recovery_length,
        _intervention_state,
        _rng_for,
        family_ready_at,
        strict_ready_at,
        threshold_k,
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
    from ra_causal_dag_support_family_workbench import (  # type: ignore
        FamilyInterventionState,
        SupportCutFamily,
        _family_recovery_length,
        _intervention_state,
        _rng_for,
        family_ready_at,
        strict_ready_at,
        threshold_k,
    )


FAMILY_SEMANTICS: Tuple[str, ...] = ("exact_k", "at_least_k", "augmented_exact_k")
CERTIFICATION_REGIMES: Tuple[str, ...] = ("cut_level", "parent_shared")
CERTIFICATION_MODES: FrozenSet[str] = frozenset({"ledger_failure", "orientation_degradation"})


@dataclass(frozen=True)
class SupportFamilyMonotonicityConfig:
    """Parameters for the v0.7.1 monotonicity audit."""

    seeds: Tuple[int, ...] = tuple(range(17, 21))
    steps: int = 16
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
    family_semantics: Tuple[str, ...] = FAMILY_SEMANTICS
    certification_regimes: Tuple[str, ...] = CERTIFICATION_REGIMES
    include_alternatives: bool = False
    max_targets: Optional[int] = 8
    sample_limit: int = 1000

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "SupportFamilyMonotonicityConfig":
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
            family_semantics=tuple(x.strip() for x in args.family_semantics.split(",") if x.strip()),
            certification_regimes=tuple(x.strip() for x in args.certification_regimes.split(",") if x.strip()),
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


def _combination_cuts(base: Tuple[int, ...], sizes: Sequence[int]) -> Tuple[SupportCut, ...]:
    seen: Dict[Tuple[int, ...], SupportCut] = {}
    for size in sizes:
        if size < 0 or size > len(base):
            continue
        for c in itertools.combinations(base, size):
            seen.setdefault(tuple(sorted(c)), frozenset(c))
    return tuple(seen[k] for k in sorted(seen))


def support_family_by_semantics(motif: MotifCandidate, fraction: float, semantics: str) -> SupportCutFamily:
    """Build a support-cut family under one v0.7.1 semantics."""
    base = tuple(sorted(motif.support_cut))
    k = threshold_k(len(base), fraction)
    if not base:
        cuts = (frozenset(),)
    elif semantics == "exact_k":
        cuts = _combination_cuts(base, [k])
    elif semantics == "at_least_k":
        cuts = _combination_cuts(base, range(k, len(base) + 1))
    elif semantics == "augmented_exact_k":
        cuts = _combination_cuts(base, [k, len(base)])
    else:
        raise ValueError(f"unknown support-family semantics: {semantics}")
    return SupportCutFamily(
        motif=motif.name,
        base_support_cut=motif.support_cut,
        cuts=cuts,
        threshold_k=k,
        threshold_fraction=float(fraction),
    )


def family_includes_strict_cut(family: SupportCutFamily) -> bool:
    return family.base_support_cut in family.cuts


def _parent_shared_intervention_state(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    family: SupportCutFamily,
    *,
    mode: str,
    severity: float,
    seed: int,
) -> Tuple[FamilyInterventionState, bool]:
    """Intervention state plus strict-parent certification failure flag.

    For non-certification modes this delegates to the v0.7 intervention.  For
    ledger/orientation modes under parent-shared certification, one parent
    certificate gates the strict cut and the whole family.
    """
    if mode not in CERTIFICATION_MODES:
        intervention = _intervention_state(state, motif, site, family, mode=mode, severity=severity, seed=seed)
        return intervention, motif.support_cut in intervention.uncertified_cuts

    rng = _rng_for(motif, site, mode, severity, seed, salt=71)
    parent_failed = bool(severity > 0 and rng.random() < severity)
    uncertified = frozenset(family.cuts) if parent_failed else frozenset()
    intervention = FamilyInterventionState(
        after_dag=state.dag,
        unavailable_support=frozenset(),
        uncertified_cuts=uncertified,
        delay_depth=0,
        selector_stress=False,
        affected_edges=(),
        detail=f"parent_shared_certificate_failed={parent_failed} channel={mode}",
    )
    return intervention, parent_failed


def _intervention_with_regime(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    family: SupportCutFamily,
    *,
    mode: str,
    severity: float,
    seed: int,
    certification_regime: str,
) -> Tuple[FamilyInterventionState, bool]:
    if certification_regime == "cut_level":
        intervention = _intervention_state(state, motif, site, family, mode=mode, severity=severity, seed=seed)
        return intervention, motif.support_cut in intervention.uncertified_cuts
    if certification_regime == "parent_shared":
        return _parent_shared_intervention_state(state, motif, site, family, mode=mode, severity=severity, seed=seed)
    raise ValueError(f"unknown certification regime: {certification_regime}")


def evaluate_support_family_monotonicity(
    state: ChannelSeedState,
    motif: MotifCandidate,
    site: int,
    *,
    threshold_fraction: float,
    family_semantics: str,
    certification_regime: str,
    mode: str,
    severity: float,
    seed: int,
) -> Dict[str, object]:
    family = support_family_by_semantics(motif, threshold_fraction, family_semantics)
    before_strict = strict_ready_at(state.dag, motif.support_cut, site)
    before_family = family_ready_at(state.dag, family, site)
    intervention, strict_uncertified = _intervention_with_regime(
        state, motif, site, family, mode=mode, severity=severity, seed=seed, certification_regime=certification_regime
    )
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
    family_rescues = before_strict and (not after_strict_ready) and after_family_ready
    no_worse_violation = after_strict_ready and (not after_family_ready)
    strict_loss = before_strict and not after_strict_ready
    family_loss = before_family and not after_family_ready
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
    return {
        "motif": motif.name,
        "site": site,
        "seed": seed,
        "mode": mode,
        "severity": float(severity),
        "support_width": len(motif.support_cut),
        "threshold_fraction": float(threshold_fraction),
        "threshold_k": family.threshold_k,
        "family_semantics": family_semantics,
        "certification_regime": certification_regime,
        "family_size": family.family_size,
        "family_includes_strict_cut": family_includes_strict_cut(family),
        "strict_before_ready": before_strict,
        "family_before_ready": before_family,
        "strict_after_ready": after_strict_ready,
        "family_after_ready": after_family_ready,
        "strict_lost_readiness": strict_loss,
        "family_lost_readiness": family_loss,
        "family_rescues_strict_loss": family_rescues,
        "no_worse_violation": no_worse_violation,
        "loss_reduction_vs_strict": int(strict_loss) - int(family_loss),
        "strict_finality_depth_before": finality_before,
        "strict_finality_depth_after": finality_after,
        "strict_recovery_length": strict_recovery,
        "family_recovery_length": family_recovery,
        "unavailable_support_count": len(intervention.unavailable_support),
        "uncertified_cut_count": len(intervention.uncertified_cuts),
        "affected_edge_count": len(intervention.affected_edges),
        "intervention_detail": intervention.detail,
    }


def iter_monotonicity_rows_for_seed(config: SupportFamilyMonotonicityConfig, seed: int) -> Iterator[Dict[str, object]]:
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
                        for semantics in config.family_semantics:
                            for regime in config.certification_regimes:
                                row = evaluate_support_family_monotonicity(
                                    state,
                                    motif,
                                    site,
                                    threshold_fraction=fraction,
                                    family_semantics=semantics,
                                    certification_regime=regime,
                                    mode=mode,
                                    severity=float(severity),
                                    seed=int(severance_seed),
                                )
                                row["run_seed"] = seed
                                yield row


def _rate(rows: Sequence[Mapping[str, object]], key: str) -> float:
    return round(sum(1 for r in rows if bool(r.get(key))) / len(rows), 6) if rows else 0.0


def _mean(values: Sequence[float]) -> Optional[float]:
    return round(sum(values) / len(values), 6) if values else None


def _num(rows: Sequence[Mapping[str, object]], key: str) -> List[float]:
    out: List[float] = []
    for r in rows:
        v = r.get(key)
        if v not in (None, ""):
            out.append(float(v))
    return out


def aggregate_monotonicity_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, float, float], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["family_semantics"]), str(r["certification_regime"]), str(r["mode"]), float(r["severity"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (semantics, regime, mode, severity, threshold), items in sorted(buckets.items()):
        out.append({
            "family_semantics": semantics,
            "certification_regime": regime,
            "mode": mode,
            "severity": severity,
            "threshold_fraction": threshold,
            "samples": len(items),
            "support_width_count": len({int(r.get("support_width", 0)) for r in items}),
            "mean_support_width": _mean([float(r.get("support_width", 0)) for r in items]),
            "mean_family_size": _mean([float(r.get("family_size", 0)) for r in items]),
            "strict_loss_rate": _rate(items, "strict_lost_readiness"),
            "family_loss_rate": _rate(items, "family_lost_readiness"),
            "family_rescue_rate": _rate(items, "family_rescues_strict_loss"),
            "no_worse_violation_rate": _rate(items, "no_worse_violation"),
            "mean_loss_reduction_vs_strict": _mean([float(r.get("loss_reduction_vs_strict", 0)) for r in items]),
            "strict_cut_inclusion_rate": _rate(items, "family_includes_strict_cut"),
            "mean_uncertified_cut_count": _mean([float(r.get("uncertified_cut_count", 0)) for r in items]),
            "mean_unavailable_support_count": _mean([float(r.get("unavailable_support_count", 0)) for r in items]),
            "mean_family_recovery_length": _mean(_num(items, "family_recovery_length")),
        })
    return out


def no_worse_audit_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, float], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["family_semantics"]), str(r["certification_regime"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (semantics, regime, threshold), items in sorted(buckets.items()):
        violations = [r for r in items if bool(r.get("no_worse_violation"))]
        out.append({
            "family_semantics": semantics,
            "certification_regime": regime,
            "threshold_fraction": threshold,
            "samples": len(items),
            "strict_cut_inclusion_rate": _rate(items, "family_includes_strict_cut"),
            "no_worse_violations": len(violations),
            "no_worse_violation_rate": round(len(violations) / len(items), 6) if items else 0.0,
            "readiness_monotone_by_construction": semantics in {"at_least_k", "augmented_exact_k"},
        })
    return out


def certification_regime_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    filtered = [r for r in rows if str(r.get("mode")) in CERTIFICATION_MODES and float(r.get("severity", 0.0)) > 0]
    buckets: Dict[Tuple[str, str, str, float], List[Mapping[str, object]]] = {}
    for r in filtered:
        buckets.setdefault((str(r["mode"]), str(r["family_semantics"]), str(r["certification_regime"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, regime, threshold), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "family_semantics": semantics,
            "certification_regime": regime,
            "threshold_fraction": threshold,
            "samples": len(items),
            "strict_loss_rate": _rate(items, "strict_lost_readiness"),
            "family_loss_rate": _rate(items, "family_lost_readiness"),
            "family_rescue_rate": _rate(items, "family_rescues_strict_loss"),
            "no_worse_violation_rate": _rate(items, "no_worse_violation"),
            "mean_uncertified_cut_count": _mean([float(r.get("uncertified_cut_count", 0)) for r in items]),
        })
    return out


def width_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, float, float, int], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["family_semantics"]), str(r["certification_regime"]), str(r["mode"]), float(r["severity"]), float(r["threshold_fraction"]), int(r["support_width"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (semantics, regime, mode, severity, threshold, width), items in sorted(buckets.items()):
        out.append({
            "family_semantics": semantics,
            "certification_regime": regime,
            "mode": mode,
            "severity": severity,
            "threshold_fraction": threshold,
            "support_width": width,
            "samples": len(items),
            "strict_loss_rate": _rate(items, "strict_lost_readiness"),
            "family_loss_rate": _rate(items, "family_lost_readiness"),
            "family_rescue_rate": _rate(items, "family_rescues_strict_loss"),
            "no_worse_violation_rate": _rate(items, "no_worse_violation"),
            "mean_family_size": _mean([float(r.get("family_size", 0)) for r in items]),
        })
    return out


def run_support_family_monotonicity(config: SupportFamilyMonotonicityConfig) -> Tuple[Dict[str, object], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    started = time.perf_counter()
    all_rows: List[Dict[str, object]] = []
    run_rows: List[Dict[str, object]] = []
    for seed in config.seeds:
        seed_rows = list(iter_monotonicity_rows_for_seed(config, seed))
        all_rows.extend(seed_rows)
        run_rows.append({
            "run_seed": seed,
            "evaluations": len(seed_rows),
            "support_width_classes": sorted({int(r.get("support_width", 0)) for r in seed_rows}),
            "family_semantics": sorted({str(r.get("family_semantics")) for r in seed_rows}),
            "certification_regimes": sorted({str(r.get("certification_regime")) for r in seed_rows}),
            "no_worse_violation_rate": _rate(seed_rows, "no_worse_violation"),
            "family_rescue_rate": _rate(seed_rows, "family_rescues_strict_loss"),
        })
    elapsed = time.perf_counter() - started
    aggregate = aggregate_monotonicity_rows(all_rows)
    audit = no_worse_audit_rows(all_rows)
    cert_rows = certification_regime_rows(all_rows)
    by_width = width_rows(all_rows)
    summary = {
        "version": "0.7.1",
        "run_count": len(config.seeds),
        "steps": config.steps,
        "actual_evaluations": len(all_rows),
        "elapsed_seconds": round(elapsed, 6),
        "evaluations_per_second": round(len(all_rows) / elapsed, 6) if elapsed > 0 else None,
        "support_width_classes": sorted({int(r.get("support_width", 0)) for r in all_rows}),
        "support_width_count": len({int(r.get("support_width", 0)) for r in all_rows}),
        "family_semantics": sorted({str(r.get("family_semantics")) for r in all_rows}),
        "certification_regimes": sorted({str(r.get("certification_regime")) for r in all_rows}),
        "threshold_fractions": sorted({float(r.get("threshold_fraction", 0.0)) for r in all_rows}),
        "total_strict_losses": sum(1 for r in all_rows if bool(r.get("strict_lost_readiness"))),
        "total_family_losses": sum(1 for r in all_rows if bool(r.get("family_lost_readiness"))),
        "total_family_rescues": sum(1 for r in all_rows if bool(r.get("family_rescues_strict_loss"))),
        "total_no_worse_violations": sum(1 for r in all_rows if bool(r.get("no_worse_violation"))),
        "monotone_semantics_no_worse_violations": sum(1 for r in all_rows if str(r.get("family_semantics")) in {"at_least_k", "augmented_exact_k"} and bool(r.get("no_worse_violation"))),
    }
    return summary, run_rows, aggregate, audit, cert_rows, by_width, all_rows[: config.sample_limit]


def write_predictions(summary: Mapping[str, object], aggregate: Sequence[Mapping[str, object]], audit: Sequence[Mapping[str, object]], cert_rows: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    worsening = [r for r in aggregate if float(r.get("no_worse_violation_rate") or 0.0) > 0]
    best_rescue = sorted([r for r in aggregate if float(r.get("severity", 0.0)) > 0 and float(r.get("threshold_fraction", 1.0)) < 1.0], key=lambda r: float(r.get("family_rescue_rate") or 0.0), reverse=True)[:8]
    lines = [
        "# RA Support-Family Monotonicity Audit — v0.7.1",
        "",
        "This note is RA-native.  It distinguishes exact-threshold family replacement from monotone family augmentation.",
        "",
        "## Scale",
        "",
        f"- run_count: {summary.get('run_count')}",
        f"- steps: {summary.get('steps')}",
        f"- actual_evaluations: {summary.get('actual_evaluations')}",
        f"- support_width_classes: {summary.get('support_width_classes')}",
        f"- family_semantics: {summary.get('family_semantics')}",
        f"- certification_regimes: {summary.get('certification_regimes')}",
        "",
        "## Monotonicity reading",
        "",
        "Exact-k support families may remove the original strict support cut.  At-least-k and augmented-exact-k families include the strict cut and therefore implement additive support-family augmentation at the readiness level.",
        "",
        f"- total_no_worse_violations: {summary.get('total_no_worse_violations')}",
        f"- monotone_semantics_no_worse_violations: {summary.get('monotone_semantics_no_worse_violations')}",
        "",
        "## Highest rescue regimes",
        "",
    ]
    if not best_rescue:
        lines.append("- No rescue regimes observed in this run.")
    for r in best_rescue:
        lines.append(
            f"- semantics={r['family_semantics']} regime={r['certification_regime']} mode={r['mode']} "
            f"severity={r['severity']} threshold={r['threshold_fraction']}: "
            f"rescue={r['family_rescue_rate']} strict_loss={r['strict_loss_rate']} family_loss={r['family_loss_rate']} "
            f"no_worse={r['no_worse_violation_rate']}."
        )
    lines += ["", "## Non-monotone regimes", ""]
    if not worsening:
        lines.append("- No no-worse violations observed.")
    for r in sorted(worsening, key=lambda x: float(x.get("no_worse_violation_rate") or 0.0), reverse=True)[:8]:
        lines.append(
            f"- semantics={r['family_semantics']} regime={r['certification_regime']} mode={r['mode']} "
            f"severity={r['severity']} threshold={r['threshold_fraction']}: "
            f"no_worse_violation_rate={r['no_worse_violation_rate']} family_loss={r['family_loss_rate']} strict_loss={r['strict_loss_rate']}."
        )
    lines += [
        "",
        "## Methodological caution",
        "",
        "The simulator comparison is diagnostic.  The formal monotonicity theorem applies to family inclusion; concrete support-family certification still has to be justified by BDG-LLC / frontier / orientation / ledger evidence.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_state(summary: Mapping[str, object], run_rows: Sequence[Mapping[str, object]], aggregate: Sequence[Mapping[str, object]], audit: Sequence[Mapping[str, object]], cert_rows: Sequence[Mapping[str, object]], width: Sequence[Mapping[str, object]], sample: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "version": "0.7.1",
        "summary": dict(summary),
        "runs": list(run_rows),
        "aggregate": list(aggregate),
        "no_worse_audit": list(audit),
        "certification_regimes": list(cert_rows),
        "width_rows": list(width),
        "sample": list(sample),
    }, indent=2, sort_keys=True), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run RA causal-DAG v0.7.1 support-family monotonicity audit.")
    p.add_argument("--seed-start", type=int, default=17)
    p.add_argument("--seed-stop", type=int, default=21)
    p.add_argument("--seed-list", type=str, default=None)
    p.add_argument("--steps", type=int, default=16)
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
    p.add_argument("--family-semantics", type=str, default=",".join(FAMILY_SEMANTICS))
    p.add_argument("--certification-regimes", type=str, default=",".join(CERTIFICATION_REGIMES))
    p.add_argument("--include-alternatives", action="store_true")
    p.add_argument("--max-targets", type=int, default=8)
    p.add_argument("--sample-limit", type=int, default=1000)
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return p


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_arg_parser().parse_args(argv)
    config = SupportFamilyMonotonicityConfig.from_args(args)
    summary, run_rows, aggregate, audit, cert_rows, width, sample = run_support_family_monotonicity(config)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    rows_to_csv([summary], out / "ra_support_family_monotonicity_summary_v0_7_1.csv")
    rows_to_csv(run_rows, out / "ra_support_family_monotonicity_runs_v0_7_1.csv")
    rows_to_csv(aggregate, out / "ra_support_family_semantics_comparison_v0_7_1.csv")
    rows_to_csv(audit, out / "ra_support_family_no_worse_audit_v0_7_1.csv")
    rows_to_csv(cert_rows, out / "ra_support_family_certification_regimes_v0_7_1.csv")
    rows_to_csv(width, out / "ra_support_family_monotonicity_by_width_v0_7_1.csv")
    rows_to_csv(sample, out / "ra_support_family_monotonicity_sample_v0_7_1.csv")
    write_predictions(summary, aggregate, audit, cert_rows, out / "ra_support_family_monotonicity_predictions_v0_7_1.md")
    write_state(summary, run_rows, aggregate, audit, cert_rows, width, sample, out / "ra_support_family_monotonicity_state_v0_7_1.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
