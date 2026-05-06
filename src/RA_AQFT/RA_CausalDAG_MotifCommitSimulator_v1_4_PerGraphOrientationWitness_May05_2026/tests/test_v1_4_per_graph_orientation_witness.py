import tempfile
from pathlib import Path
import unittest
import pandas as pd

from analysis.ra_per_graph_orientation_witness import run, build_member_witnesses, fallback_manifest, load_rows, compute_row_overlap

_PKT_PARENT = Path(__file__).resolve().parents[2]
INPUT = _PKT_PARENT / 'RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026' / 'outputs'
MANIFEST = _PKT_PARENT / 'RA_CausalDAG_MotifCommitSimulator_v1_3_NativeOrientationLinkDerivation_May05_2026' / 'outputs'

class TestPerGraphOrientationWitnessV14(unittest.TestCase):
    def test_member_witnesses_are_extracted(self):
        rows=load_rows(INPUT).head(5)
        w=build_member_witnesses(rows, fallback_manifest())
        self.assertGreater(len(w), 0)
        self.assertIn('orientation_link_tokens', w.columns)
        self.assertTrue((w['graph_local_token_count'] > 0).all())

    def test_overlap_decouples_from_support_when_possible(self):
        rows=load_rows(INPUT).head(80)
        w=build_member_witnesses(rows, fallback_manifest())
        o=compute_row_overlap(w, rows)
        diff=(o['per_graph_orientation_link_overlap']-o['support_overlap']).abs().max()
        self.assertGreater(diff, 1e-9)

    def test_orientation_specificity_summary(self):
        with tempfile.TemporaryDirectory() as td:
            s=run(INPUT, MANIFEST, None, Path(td), sample_limit=200)
            self.assertTrue(s['per_graph_orientation_surface_decoupled'])
            self.assertTrue(s['matched_orientation_variation_available'])
            self.assertTrue(s['selector_guardrail_passed'])

    def test_outputs_written(self):
        with tempfile.TemporaryDirectory() as td:
            run(INPUT, MANIFEST, None, Path(td), sample_limit=100)
            expected=['ra_per_graph_orientation_witness_members_v1_4.csv','ra_per_graph_orientation_link_overlap_v1_4.csv','ra_per_graph_orientation_witness_summary_v1_4.md']
            for f in expected:
                self.assertTrue((Path(td)/f).exists())

if __name__ == '__main__':
    unittest.main()
