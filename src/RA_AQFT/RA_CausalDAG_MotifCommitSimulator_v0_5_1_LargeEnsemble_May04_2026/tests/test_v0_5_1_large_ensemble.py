import unittest

from simulator.ra_causal_dag_simulator import generate_growth_demo
from simulator.ra_causal_dag_ensemble import (
    EnsembleRunConfig,
    StreamingBuckets,
    generate_growth_state_fast,
    run_large_ensemble,
    benchmark_fast_vs_audited,
)


class LargeEnsembleV051Tests(unittest.TestCase):
    def test_fast_growth_matches_audited_final_state_for_fixed_seed(self):
        dag_fast, motifs_fast = generate_growth_state_fast(steps=10, seed=29, max_parents=3)
        dag_audited, motifs_audited, *_ = generate_growth_demo(
            steps=10,
            seed=29,
            max_parents=3,
            conflict_rate=0.30,
            defect_rate=0.05,
            orientation_defect_rate=0.05,
            conflict_witness_defect_rate=0.10,
        )
        self.assertEqual(dag_fast.edges, dag_audited.edges)
        self.assertEqual([m.name for m in motifs_fast], [m.name for m in motifs_audited])
        self.assertEqual([sorted(m.support_cut) for m in motifs_fast], [sorted(m.support_cut) for m in motifs_audited])
        self.assertEqual([m.metadata.get("defect_tags") for m in motifs_fast], [m.metadata.get("defect_tags") for m in motifs_audited])

    def test_streaming_buckets_samples_and_aggregates(self):
        bucket = StreamingBuckets(sample_limit=2)
        for i in range(5):
            bucket.observe({
                "run_seed": 10 + i,
                "mode": "frontier_dropout",
                "severity": 0.5,
                "support_width": 1,
                "lost_support": i % 2 == 0,
                "lost_readiness": True,
                "lost_strict_commit": False,
                "lost_selected_commit": False,
                "nodes": 5,
                "edges": 4,
                "motifs": 6,
                "target_count": 2,
            })
        self.assertEqual(bucket.count, 5)
        self.assertEqual(len(bucket.samples), 2)
        aggregate = bucket.aggregate_rows()[0]
        self.assertEqual(aggregate["samples"], 5)
        self.assertEqual(aggregate["readiness_loss_rate"], 1.0)

    def test_large_ensemble_outputs_expected_tables(self):
        config = EnsembleRunConfig(
            seeds=(17, 19),
            steps=6,
            severance_seeds=(101,),
            severities=(0.0, 0.5),
            modes=("frontier_dropout", "support_delay"),
            max_targets=3,
            sample_limit=10,
            workers=1,
        )
        summary, run_rows, aggregate_rows, fragility_rows, sample_rows = run_large_ensemble(config)
        self.assertEqual(summary["version"], "0.5.1")
        self.assertEqual(summary["run_count"], 2)
        self.assertGreater(summary["actual_evaluations"], 0)
        self.assertEqual(len(run_rows), 2)
        self.assertEqual(len(aggregate_rows), 4)
        self.assertGreater(len(fragility_rows), 0)
        self.assertLessEqual(len(sample_rows), 10)

    def test_benchmark_reports_speedup_row(self):
        rows = benchmark_fast_vs_audited(seed=17, steps=4, repeats=1)
        self.assertEqual(rows[-1]["mode"], "speedup_fast_vs_audited")
        self.assertIsNotNone(rows[-1]["mean_seconds"])


if __name__ == "__main__":
    unittest.main()
