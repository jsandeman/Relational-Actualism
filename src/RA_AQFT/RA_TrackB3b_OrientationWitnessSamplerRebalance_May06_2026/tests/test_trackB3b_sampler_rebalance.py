import unittest
from analysis.ra_trackB3b_sampler_rebalance import (
    absolute_overlap_bin, all_pairs_mean_jaccard, parent_anchored_jaccard,
    fixed_bin_coverage, joint_strata, coverage_by_config, recommendations,
)
import pandas as pd

class TrackB3bSamplerRebalanceTests(unittest.TestCase):
    def test_overlap_bins(self):
        self.assertEqual(absolute_overlap_bin(0.0), 'low')
        self.assertEqual(absolute_overlap_bin(0.5), 'medium')
        self.assertEqual(absolute_overlap_bin(0.8), 'high')

    def test_all_pairs_vs_parent(self):
        w = [frozenset({'a','b'}), frozenset({'a','c'}), frozenset({'d'})]
        self.assertNotEqual(all_pairs_mean_jaccard(w), parent_anchored_jaccard(w))

    def test_coverage_sufficiency_excludes_by_construction(self):
        rows=[]
        # One config/keying with a single joint stratum containing low and high
        for b in ['low']*30 + ['high']*30 + ['medium']*10:
            rows.append({'config_id':'c','keying':'edge_direction_only','family_semantics':'augmented_exact_k','threshold_fraction':0.5,'support_width':2,'family_size':3,'orientation_bin':b})
        df=pd.DataFrame(rows)
        cov=coverage_by_config(df, min_rows_per_stratum=25)
        self.assertTrue(bool(cov['coverage_sufficient_legitimate'].iloc[0]))
        rec=recommendations(cov)
        self.assertEqual(rec['recommendation'].iloc[0], 'coverage_sufficient_legitimate_keying')

    def test_non_estimable_without_high(self):
        df=pd.DataFrame([
            {'config_id':'c','keying':'edge_direction_only','family_semantics':'augmented_exact_k','threshold_fraction':0.5,'support_width':2,'family_size':3,'orientation_bin':'low'} for _ in range(10)
        ])
        cov=coverage_by_config(df, min_rows_per_stratum=5)
        self.assertFalse(bool(cov['coverage_sufficient_legitimate'].iloc[0]))
        rec=recommendations(cov)
        self.assertEqual(rec['recommendation'].iloc[0], 'increase_high_overlap_coverage')

if __name__ == '__main__':
    unittest.main()
