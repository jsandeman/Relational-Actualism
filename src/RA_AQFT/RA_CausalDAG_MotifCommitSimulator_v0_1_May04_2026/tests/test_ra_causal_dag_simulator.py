import unittest

from simulator.ra_causal_dag_simulator import (
    CausalDAG,
    CommitContext,
    MotifCandidate,
    MotifCommitProtocol,
)


class TestRACausalDAGSimulator(unittest.TestCase):
    def diamond(self):
        dag = CausalDAG()
        n0 = dag.add_node()
        n1 = dag.add_node([n0])
        n2 = dag.add_node([n0])
        n3 = dag.add_node([n1, n2])
        return dag, n0, n1, n2, n3

    def test_hasse_frontier_of_downset(self):
        dag, n0, n1, n2, _n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        self.assertEqual(dag.hasse_frontier(past), frozenset({n1, n2}))

    def test_ready_at_and_future_monotonicity(self):
        dag, n0, n1, _n2, n3 = self.diamond()
        cut = frozenset({n0})
        self.assertTrue(dag.ready_at(cut, n1))
        self.assertTrue(dag.reachable(n1, n3))
        self.assertTrue(dag.ready_at(cut, n3))

    def test_incompatible_ready_motifs_block_each_other(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = MotifCandidate("A", frozenset({n3}), cut, exclusion_domain="choice")
        b = MotifCandidate("B", frozenset({n3}), cut, exclusion_domain="choice")
        protocol = MotifCommitProtocol(dag, [a, b], CommitContext())
        da = protocol.decision(a, n3)
        db = protocol.decision(b, n3)
        self.assertTrue(da.ready)
        self.assertTrue(db.ready)
        self.assertFalse(da.commits)
        self.assertFalse(db.commits)
        self.assertEqual(da.blocked_by, ("B",))
        self.assertEqual(db.blocked_by, ("A",))

    def test_unique_ready_motif_commits(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        m = MotifCandidate("M", frozenset({n3}), cut)
        protocol = MotifCommitProtocol(dag, [m])
        decision = protocol.decision(m, n3)
        self.assertTrue(decision.supported)
        self.assertTrue(decision.ready)
        self.assertTrue(decision.commits)

    def test_depth_finality(self):
        dag, n0, n1, n2, n3 = self.diamond()
        self.assertTrue(dag.finalized_at_depth(frozenset({n0}), 1))
        self.assertTrue(dag.finalized_at_depth(frozenset({n1, n2}), dag.depth[n3]))


if __name__ == "__main__":
    unittest.main()
