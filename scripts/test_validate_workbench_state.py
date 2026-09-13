"""Regression checks for missing or mismatched extension verification records."""
import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_workbench_state as validator

ROOT = Path(__file__).resolve().parent.parent
RECEIPT = ROOT / 'certificates/lean_extended_receipt.json'


class ExtensionReceiptTests(unittest.TestCase):
    def rejects(self, mutate, message):
        receipt = copy.deepcopy(validator.load_json(RECEIPT))
        mutate(receipt)
        original = validator.parsed_value

        def substituted(parsed, path):
            return receipt if path == RECEIPT else original(parsed, path)

        with patch.object(validator, 'parsed_value', side_effect=substituted):
            with self.assertRaisesRegex(validator.ValidationFailure, message):
                validator.validate(ROOT)

    def test_current_records_pass(self):
        self.assertEqual(validator.validate(ROOT)['status'], 'PASS')

    def test_failed_run_rejected(self):
        self.rejects(lambda r: r['runs'][1].update(exit_code=1), 'Unsuccessful Lean run')

    def test_missing_run_rejected(self):
        self.rejects(lambda r: r['runs'].pop(), 'all four serial checks')

    def test_missing_input_rejected(self):
        self.rejects(lambda r: r['source_sha256'].pop('formal/lean/Main.lean'), 'input inventory')

    def test_wrong_source_hash_rejected(self):
        self.rejects(lambda r: r['source_sha256'].update({'formal/lean/ErdosProblem817/Extended.lean': '0'*64}), 'hash mismatch')

    def test_wrong_run_source_rejected(self):
        self.rejects(lambda r: r['runs'][1].update(source_sha256='0'*64), 'run source')

    def test_overlap_rejected(self):
        self.rejects(lambda r: r['runs'][1].update(started_utc=r['runs'][0]['started_utc']), 'duration|overlap')

    def test_no_preflight_rejected(self):
        self.rejects(lambda r: r['runs'][1].update(overlap_preflight='unknown'), 'preflight')

    def test_resource_excess_rejected(self):
        self.rejects(lambda r: r['runs'][1].update(peak_working_set_bytes=5000000001), 'memory scope')

    def test_false_theorem_inventory_rejected(self):
        def alter(receipt):
            receipt['axiom_report']['NotATheorem'] = receipt['axiom_report'].pop('ErdosProblem817.card_generators')
        self.rejects(alter, 'theorem inventory')

    def test_unreported_axiom_rejected(self):
        self.rejects(lambda r: r['axiom_report']['ErdosProblem817.erdos_problem_817_upper_bound'].append('sorryAx'), 'full Lean output|Unexpected axiom')

    def test_changed_output_rejected(self):
        self.rejects(lambda r: r.update(axiom_log_sha256='0'*64), 'output hash')

    def test_cache_is_pruned(self):
        with tempfile.TemporaryDirectory(prefix='ep817-validator-') as folder:
            root = Path(folder)
            (root / '.lake').mkdir()
            (root / '.lake/invalid.json').write_text('not JSON')
            (root / 'valid.json').write_text('{}')
            self.assertEqual(validator.public_structured_files(root), [root / 'valid.json'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
