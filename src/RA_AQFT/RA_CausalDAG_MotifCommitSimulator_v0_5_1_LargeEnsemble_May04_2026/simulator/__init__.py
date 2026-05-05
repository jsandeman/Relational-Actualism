from .ra_causal_dag_simulator import (
    CausalDAG, MotifCandidate, MotifCommitProtocol, GraphOrientationSupportCertifier,
    OrientationActualizationContext, SelectorPolicy, CausalSeveranceIntervention,
    SeveranceEvaluation, run_severance_workbench, evaluate_severance, summarize_fragility,
)

_ENSEMBLE_EXPORTS = {
    "EnsembleRunConfig", "StreamingBuckets", "generate_growth_state_fast", "run_large_ensemble",
    "benchmark_fast_vs_audited",
}

__all__ = [
    "CausalDAG", "MotifCandidate", "MotifCommitProtocol", "GraphOrientationSupportCertifier",
    "OrientationActualizationContext", "SelectorPolicy", "CausalSeveranceIntervention",
    "SeveranceEvaluation", "run_severance_workbench", "evaluate_severance", "summarize_fragility",
    *_ENSEMBLE_EXPORTS,
]


def __getattr__(name):
    if name in _ENSEMBLE_EXPORTS:
        from . import ra_causal_dag_ensemble as ensemble
        return getattr(ensemble, name)
    raise AttributeError(name)
