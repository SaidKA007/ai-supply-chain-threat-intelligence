"""Offline tests use constructed API responses, not observations from the Hub."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import unittest

PATH = Path(__file__).resolve().parents[1] / 'scripts' / 'collect_metadata.py'
spec = importlib.util.spec_from_file_location('collector', PATH)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
SHA = 'a' * 40

class FakeApi:
    def __init__(self):
        self.calls = []
    def model_info(self, repo_id, **kwargs):
        self.calls.append((repo_id, kwargs))
        return SimpleNamespace(sha=SHA, private=False, downloads=12, likes=1,
             siblings=[SimpleNamespace(rfilename='weights.bin'), SimpleNamespace(rfilename='helper.py')])

class MetadataTests(unittest.TestCase):
    def test_missing_listing_is_unknown(self):
        result = collector.summarize_files(None)
        self.assertIsNone(result['has_python'])
        self.assertIsNone(result['has_safetensors'])
    def test_empty_listing_is_distinct(self):
        self.assertIs(collector.summarize_files([])['has_python'], False)
    def test_extensions_not_backdoor_labels(self):
        api = FakeApi()
        row = collector.collect_one(api, 'example/test', 1, '2026-11-13T00:00:00+00:00')
        self.assertTrue(row['has_pickle_like_extension'])
        self.assertTrue(row['has_python'])
        self.assertEqual(row['backdoor_label'], 'unknown')
        self.assertEqual(row['scan_status'], 'not_run')
        self.assertEqual(row['remote_code_requirement'], 'not_assessed')
    def test_second_call_is_pinned(self):
        api = FakeApi()
        collector.collect_one(api, 'example/test', 1, 'time')
        self.assertEqual(api.calls[1][1]['revision'], SHA)
        self.assertTrue(api.calls[1][1]['files_metadata'])
        self.assertIs(api.calls[0][1]['token'], False)
        self.assertIs(api.calls[1][1]['token'], False)
    def test_no_sha_does_not_silently_use_main(self):
        class Missing(FakeApi):
            def model_info(self, repo_id, **kwargs):
                return SimpleNamespace(sha=None, private=False)
        with self.assertRaises(ValueError):
            collector.collect_one(Missing(), 'example/test', 1, 'time')
    def test_case_and_duplicate_names(self):
        rows = [SimpleNamespace(rfilename='A.PY'), SimpleNamespace(rfilename='A.PY'),
                SimpleNamespace(rfilename='model.safetensors')]
        summary = collector.summarize_files(rows)
        self.assertEqual(summary['extension_counts']['.py'], 1)
        self.assertTrue(summary['has_safetensors'])
    def test_unknown_binary_extension_is_not_proven_pickle(self):
        summary = collector.summarize_files([SimpleNamespace(rfilename='weights.bin')])
        self.assertNotIn('confirmed_pickle', summary)
    def test_revision_mismatch_fails(self):
        class Mismatch(FakeApi):
            def model_info(self, repo_id, **kwargs):
                r = super().model_info(repo_id, **kwargs)
                if kwargs.get('revision'):
                    r.sha = 'b' * 40
                return r
        with self.assertRaises(ValueError):
            collector.collect_one(Mismatch(), 'example/test', 1, 'time')

if __name__ == '__main__':
    unittest.main()
