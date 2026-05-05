import csv
import tempfile
import unittest
from pathlib import Path

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from analysis.ra_causal_dag_ensemble_analysis import analyze, read_csv_rows, summarize_modes


def write_csv(path, fieldnames, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


class EnsembleAnalysisV052Tests(unittest.TestCase):
    def test_threshold_saturating_loss_classification(self):
        rows = []
        for sev in [0.0, 0.25, 0.5, 0.75, 1.0]:
            loss = 0.0 if sev == 0.0 else 0.97
            rows.append({
                'mode': 'frontier_dropout', 'severity': sev, 'samples': 100,
                'support_loss_rate': loss, 'readiness_loss_rate': loss,
                'strict_commit_loss_rate': loss, 'selected_commit_loss_rate': loss,
                'mean_finality_depth_shift': '', 'mean_recovery_length': '',
            })
        summary = summarize_modes(rows)
        self.assertEqual(summary[0]['response_class'], 'threshold_saturating_support_loss')
        self.assertEqual(summary[0]['primary_failure_channel'], 'support_certification_or_frontier_loss')
        self.assertAlmostEqual(summary[0]['loss_saturation_score'], 1.0)

    def test_support_delay_classification(self):
        rows = []
        shifts = {0.0: 0, 0.25: 1, 0.5: 2, 0.75: 4, 1.0: 5}
        for sev, shift in shifts.items():
            rows.append({
                'mode': 'support_delay', 'severity': sev, 'samples': 100,
                'support_loss_rate': 0.0,
                'readiness_loss_rate': 0.0 if sev == 0.0 else 0.97,
                'strict_commit_loss_rate': 0.0 if sev == 0.0 else 0.97,
                'selected_commit_loss_rate': 0.0 if sev == 0.0 else 0.97,
                'mean_finality_depth_shift': shift,
                'mean_recovery_length': shift,
            })
        summary = summarize_modes(rows)
        self.assertEqual(summary[0]['primary_failure_channel'], 'readiness_delay_without_support_loss')
        self.assertGreaterEqual(summary[0]['finality_shift_monotone_score'], 0.75)
        self.assertEqual(summary[0]['response_class'], 'graded_delay_without_support_loss')

    def test_selector_stress_classification(self):
        rows = []
        for sev in [0.0, 0.25, 0.5, 0.75, 1.0]:
            strict = 0.0 if sev == 0.0 else 0.97
            rows.append({
                'mode': 'selector_stress', 'severity': sev, 'samples': 100,
                'support_loss_rate': 0.0, 'readiness_loss_rate': 0.0,
                'strict_commit_loss_rate': strict, 'selected_commit_loss_rate': 0.0,
                'mean_finality_depth_shift': 0.0, 'mean_recovery_length': 0.0,
            })
        summary = summarize_modes(rows)
        self.assertEqual(summary[0]['primary_failure_channel'], 'strict_commit_incompatibility_channel')
        self.assertEqual(summary[0]['response_class'], 'strict_channel_threshold_saturation')

    def test_end_to_end_outputs_written(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            inp = base / 'inputs'
            out = base / 'outputs'
            inp.mkdir()
            aggregate_fields = [
                'mode','severity','samples','mean_support_width','support_loss_rate','readiness_loss_rate',
                'strict_commit_loss_rate','selected_commit_loss_rate','mean_finality_depth_shift','mean_recovery_length'
            ]
            aggregate_rows = []
            for mode in ['frontier_dropout', 'support_delay', 'selector_stress']:
                for sev in [0.0, 0.5, 1.0]:
                    if mode == 'support_delay':
                        support, ready, strict, selected, shift, rec = (0, 0 if sev == 0 else .9, 0 if sev == 0 else .9, 0 if sev == 0 else .9, sev * 5, sev * 5)
                    elif mode == 'selector_stress':
                        support, ready, strict, selected, shift, rec = (0, 0, 0 if sev == 0 else .9, 0, 0, 0)
                    else:
                        loss = 0 if sev == 0 else .9
                        support, ready, strict, selected, shift, rec = (loss, loss, loss, loss, '', '')
                    aggregate_rows.append({
                        'mode': mode, 'severity': sev, 'samples': 10, 'mean_support_width': 1,
                        'support_loss_rate': support, 'readiness_loss_rate': ready,
                        'strict_commit_loss_rate': strict, 'selected_commit_loss_rate': selected,
                        'mean_finality_depth_shift': shift, 'mean_recovery_length': rec,
                    })
            write_csv(inp / 'ra_causal_dag_ensemble_aggregate_v0_5_1.csv', aggregate_fields, aggregate_rows)
            frag_fields = ['mode','severity','support_width','samples','lost_support_rate','lost_readiness_rate','lost_strict_commit_rate','lost_selected_commit_rate','mean_recovery_length','mean_finality_depth_shift']
            write_csv(inp / 'ra_causal_dag_ensemble_fragility_v0_5_1.csv', frag_fields, [
                {'mode':'frontier_dropout','severity':0.5,'support_width':1,'samples':10,'lost_support_rate':.9,'lost_readiness_rate':.9,'lost_strict_commit_rate':.9,'lost_selected_commit_rate':.9,'mean_recovery_length':'','mean_finality_depth_shift':''}
            ])
            summary_fields = ['version','run_count','steps','workers','actual_evaluations','sampled_evaluations','elapsed_seconds','evaluations_per_second']
            write_csv(inp / 'ra_causal_dag_ensemble_summary_v0_5_1.csv', summary_fields, [
                {'version':'0.5.1','run_count':3,'steps':2,'workers':1,'actual_evaluations':90,'sampled_evaluations':90,'elapsed_seconds':1.0,'evaluations_per_second':90}
            ])
            state = analyze(inp, out)
            self.assertEqual(state['mode_count'], 3)
            for name in state['outputs']:
                self.assertTrue((out / name).exists(), name)
            signatures = read_csv_rows(out / 'ra_severance_mode_signatures_v0_5_2.csv')
            channels = {r['mode']: r['primary_failure_channel'] for r in signatures}
            self.assertEqual(channels['support_delay'], 'readiness_delay_without_support_loss')
            self.assertEqual(channels['selector_stress'], 'strict_commit_incompatibility_channel')


if __name__ == '__main__':
    unittest.main()
