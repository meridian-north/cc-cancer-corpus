import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mechanism_topics import match_topic, TOPICS
from query_index import load
from verify_release import expected_manifest, verify, MANIFEST, INVENTORY


class TopicTests(unittest.TestCase):
    def test_circadian_or_melatonin_with_timing(self):
        self.assertIsNotNone(match_topic({'title': 'Circadian regulation in cancer'}, 'circadian_timing'))
        self.assertIsNotNone(match_topic({'title': 'Melatonin trial', 'abstract': 'Evening administration'}, 'circadian_timing'))
        self.assertIsNone(match_topic({'title': 'Melatonin trial'}, 'circadian_timing'))

    def test_ambiguous_acronyms_need_context(self):
        self.assertIsNone(match_topic({'title': 'PDK1 in a signaling cascade'}, 'warburg_pdh_pdk'))
        self.assertIsNotNone(match_topic({'title': 'PDK1 controls glycolysis'}, 'warburg_pdh_pdk'))
        self.assertIsNotNone(match_topic({'title': 'PDH and HIF–1α'}, 'warburg_pdh_pdk'))
        self.assertIsNone(match_topic({'title': 'PDK10 and glycolysis'}, 'warburg_pdh_pdk'))

    def test_no_cross_field_phrase_creation(self):
        self.assertIsNone(match_topic({'title': 'Pyruvate', 'abstract': 'dehydrogenase'}, 'warburg_pdh_pdk'))

    def test_interaction_topics_require_both_sides(self):
        self.assertIsNone(match_topic({'title': 'Antioxidants in healthy volunteers'}, 'antioxidant_chemo_interaction'))
        self.assertIsNotNone(match_topic({'title': 'Antioxidants with carboplatin'}, 'antioxidant_chemo_interaction'))
        self.assertIsNone(match_topic({'title': 'Garlic cultivation'}, 'antiplatelet_bleeding_risk'))
        self.assertIsNotNone(match_topic({'title': 'Garlic and platelet aggregation'}, 'antiplatelet_bleeding_risk'))

    def test_negative_results_are_retrievable_not_positive_claims(self):
        row = {'title': 'No effect of melatonin', 'abstract': 'Evening melatonin did not protect blood counts.',
               'source_class': 'rct', 'verified': 'True', 'mechanism_nodes': 'old_node'}
        original = dict(row)
        match = match_topic(row, 'circadian_timing')
        self.assertEqual(match['status'], 'candidate_keyword_match')
        self.assertEqual(row, original)
        self.assertEqual(match['text_scope'], 'title_and_abstract')
        self.assertIn({'phrase': 'evening', 'field': 'abstract'}, match['rules'][0]['hits'])


class QueryTests(unittest.TestCase):
    def run_query(self, *args):
        return subprocess.run([sys.executable, str(ROOT/'query_index.py'), *args], capture_output=True, text=True)

    def test_title_only_explicit_csv_and_json_limits(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'sample.csv'
            with path.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=['id', 'title', 'source_class', 'mechanism_nodes', 'cohorts', 'year', 'link'])
                writer.writeheader()
                writer.writerows([
                    {'id':'1','title':'Warburg metabolism','source_class':'retracted','mechanism_nodes':'legacy','year':'2020'},
                    {'id':'2','title':'Aerobic glycolysis','source_class':'preclinical','mechanism_nodes':'legacy','year':'2021'}])
            result = self.run_query('--csv', str(path), '--topic', 'warburg_pdh_pdk', '--limit','1','--json')
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual((data['match_count'], data['returned_count']), (2, 1))
            self.assertEqual(data['rows'][0]['source_class'], 'retracted')
            self.assertEqual(data['rows'][0]['topic_match']['text_scope'], 'title_only')
            self.assertEqual(data['source_classes'], {'preclinical':1,'retracted':1})
            self.assertNotIn('abstract', data['rows'][0])

    def test_invalid_options_fail(self):
        for args in [('--topic','nonexistent'),('--node','nonexistent'),('--limit','-1'),
                     ('--year-min','2025','--year-max','2020'),('--summary','--topic','circadian_timing')]:
            with self.subTest(args=args):
                self.assertNotEqual(self.run_query(*args).returncode, 0)

    def test_case_report_class_discrepancy_is_flagged_without_regrading(self):
        result = self.run_query('--topic','warburg_pdh_pdk','--grep','Case Report: Sodium dichloroacetate','--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['source_class_status'], 'inherited_not_reassessed')
        self.assertEqual(data['match_count'], 1)
        self.assertEqual(data['rows'][0]['source_class'], 'clinical_trial')
        self.assertIn('case report', data['rows'][0]['source_class_review'])

    def test_existing_node_query_works(self):
        result = self.run_query('--node','immune_checkpoint','--class','rct','--limit','1','--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreater(json.loads(result.stdout)['match_count'], 0)

    def test_topic_summary_reproduces_committed_coverage(self):
        result = self.run_query('--topic-summary','--json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, (ROOT/'TOPIC_COVERAGE.json').read_text())

    def test_public_sources_agree_on_ids_and_classes(self):
        csv_rows = load(ROOT/'data/cancer_index.csv')
        json_rows = load(ROOT/'data/cancer_index.jsonl.gz')
        fields = ('id','source_class','mechanism_nodes','cohorts')
        self.assertEqual([[r.get(k) for k in fields] for r in csv_rows], [[r.get(k) for k in fields] for r in json_rows])
        self.assertEqual(len(csv_rows), json.loads((ROOT/'data/index_summary.json').read_text())['papers_total'])


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'public.txt').write_text('public fixture')
        (self.root/INVENTORY).write_text('public.txt\n')
        (self.root/MANIFEST).write_text(expected_manifest(self.root))

    def test_match_and_tamper(self):
        self.assertEqual(verify(self.root), 1)
        (self.root/'public.txt').write_text('changed')
        with self.assertRaises(ValueError): verify(self.root)

    def test_missing_file(self):
        (self.root/'public.txt').unlink()
        with self.assertRaises(ValueError): verify(self.root)

    def test_manifest_path_set_must_equal_inventory(self):
        for content in ['', '0'*64+'  extra.txt\n', (self.root/MANIFEST).read_text()*2]:
            (self.root/MANIFEST).write_text(content)
            with self.assertRaises(ValueError): verify(self.root)

    def test_private_unlisted_file_is_not_discovered(self):
        (self.root/'private.txt').write_text('synthetic private fixture')
        self.assertEqual(verify(self.root), 1)
        self.assertNotIn('private.txt', expected_manifest(self.root))

    def test_traversal_and_symlinks_rejected(self):
        for name in ['../outside.txt','/tmp/outside.txt','./public.txt','sub//name','public.txt\npublic.txt']:
            (self.root/INVENTORY).write_text(name+'\n')
            with self.assertRaises(ValueError): expected_manifest(self.root)
        (self.root/'alias').symlink_to(self.root/'public.txt')
        (self.root/INVENTORY).write_text('alias\n')
        with self.assertRaises(ValueError): expected_manifest(self.root)

    def test_manifest_symlink_rejected(self):
        (self.root/MANIFEST).unlink()
        (self.root/MANIFEST).symlink_to(self.root/'public.txt')
        with self.assertRaises(ValueError): verify(self.root)


if __name__ == '__main__':
    unittest.main()
