import csv
import tempfile
import unittest
from pathlib import Path

from analysis.ra_native_certificate_anchoring import run_analysis

class NativeCertificateAnchoringV10Tests(unittest.TestCase):
    def write_csv(self, path, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        keys=[]
        for r in rows:
            for k in r:
                if k not in keys: keys.append(k)
        with path.open('w', newline='', encoding='utf-8') as f:
            w=csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)

    def test_end_to_end_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            inp=root/'inputs'; out=root/'outputs'; cal=root/'calibration'
            comp=[]
            for mode in ['ledger_failure','orientation_degradation']:
                for sem in ['at_least_k','augmented_exact_k']:
                    for i,(sev,thr) in enumerate([(0.5,0.25),(0.75,0.25)]):
                        comp.append({
                            'mode':mode,'family_semantics':sem,'severity':sev,'threshold_fraction':thr,
                            'support_width':2+i,'samples':10,'mean_weighted_native_overlap':0.2+i*0.4,
                            'mean_induced_certificate_correlation':0.2+i*0.4,'certification_rescue_rate':0.2-i*0.1,
                            'mean_support_overlap':0.1+i*0.2,'mean_frontier_overlap':0.1+i*0.2,
                            'mean_orientation_overlap':0.2+i*0.2,'mean_ledger_overlap':0.3+i*0.1,
                            'mean_causal_past_overlap':0.4,'mean_bdg_kernel_overlap':0.5,'mean_firewall_overlap':0.6,
                        })
            rescue=[]
            for mode in ['ledger_failure','orientation_degradation']:
                rescue += [
                    {'mode':mode,'family_semantics':'augmented_exact_k','native_overlap_bin':'low','samples':10,'mean_induced_certificate_correlation':0.2,'certification_rescue_rate':0.2,'family_certification_resilience_rate':0.4,'family_internal_loss_rate':0.6},
                    {'mode':mode,'family_semantics':'augmented_exact_k','native_overlap_bin':'high','samples':10,'mean_induced_certificate_correlation':0.9,'certification_rescue_rate':0.0,'family_certification_resilience_rate':0.1,'family_internal_loss_rate':0.9},
                    {'mode':mode,'family_semantics':'at_least_k','native_overlap_bin':'medium','samples':10,'mean_induced_certificate_correlation':0.5,'certification_rescue_rate':0.1,'family_certification_resilience_rate':0.3,'family_internal_loss_rate':0.7},
                    {'mode':mode,'family_semantics':'at_least_k','native_overlap_bin':'high','samples':10,'mean_induced_certificate_correlation':0.9,'certification_rescue_rate':0.0,'family_certification_resilience_rate':0.1,'family_internal_loss_rate':0.9},
                ]
            self.write_csv(inp/'ra_witness_overlap_components_v0_9.csv', comp)
            self.write_csv(inp/'ra_cert_rescue_by_native_overlap_v0_9.csv', rescue)
            self.write_csv(inp/'ra_native_certificate_overlap_selector_guardrail_v0_9.csv', [{'mode':'selector_stress','selector_guardrail_passed':'True'}])
            self.write_csv(cal/'ra_native_vs_external_correlation_mapping_v0_9_2.csv', [{'mode':'ledger_failure','alignment':'qualitative'}])
            summary=run_analysis(inp,out,cal)
            self.assertEqual(summary['primary_family_semantics'],'augmented_exact_k')
            self.assertEqual(summary['guardrail_family_semantics'],'at_least_k')
            self.assertTrue(summary['selector_guardrail_passed'])
            for fn in ['ra_native_certificate_components_v1_0.csv','ra_component_attribution_by_mode_v1_0.csv','ra_native_certificate_anchoring_summary_v1_0.md']:
                self.assertTrue((out/fn).exists(), fn)

    def test_missing_required_files_raises(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(FileNotFoundError):
                run_analysis(Path(td), Path(td)/'out')

    def test_primary_and_guardrail_roles(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); inp=root/'inputs'; out=root/'outputs'
            rows=[{'mode':'ledger_failure','family_semantics':'augmented_exact_k','severity':0.5,'threshold_fraction':0.25,'support_width':2,'samples':1,
                   'mean_weighted_native_overlap':0.1,'mean_induced_certificate_correlation':0.1,'certification_rescue_rate':0.2,
                   'mean_support_overlap':0,'mean_frontier_overlap':0,'mean_orientation_overlap':0,'mean_ledger_overlap':0,'mean_causal_past_overlap':0,'mean_bdg_kernel_overlap':0,'mean_firewall_overlap':0}]
            rescue=[{'mode':'ledger_failure','family_semantics':'augmented_exact_k','native_overlap_bin':'low','samples':1,'mean_induced_certificate_correlation':0.1,'certification_rescue_rate':0.2,'family_certification_resilience_rate':0.2,'family_internal_loss_rate':0.8}]
            self.write_csv(inp/'ra_witness_overlap_components_v0_9.csv', rows)
            self.write_csv(inp/'ra_cert_rescue_by_native_overlap_v0_9.csv', rescue)
            run_analysis(inp,out)
            with (out/'ra_native_overlap_profile_v1_0.csv').open(newline='', encoding='utf-8') as f:
                outrows=list(csv.DictReader(f))
            self.assertEqual(outrows[0]['semantics_role'],'primary_signal_carrier')

if __name__ == '__main__':
    unittest.main()
