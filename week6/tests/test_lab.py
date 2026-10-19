"""Regression checks for the teaching code; not detection-accuracy measurements."""
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

WEEK6 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WEEK6 / "simulation"))

from lab_helpers import ACTIVE_CONTEXT, toy_model_data, write_marker
from run_lab import TELEMETRY_SOURCE, csv_value, json_only_policy, make_fixtures, run_experiment


class LabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="week6_test_")
        cls.output = Path(cls.temp.name) / "fresh_run"
        cls.summary = run_experiment(cls.output, "automated-local-test")
        cls.rows = {row["scenario_id"]: row for row in cls.summary["scenarios"]}
        cls.events = [json.loads(line) for line in (cls.output / "events.jsonl").read_text().splitlines()]

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def types(self, scenario_id: str) -> list[str]:
        return [event["event_type"] for event in self.events if event["scenario_id"] == scenario_id]

    def test_baseline_has_no_callback(self) -> None:
        self.assertEqual(self.rows["S01"]["outcome"], "loaded")
        self.assertEqual(self.rows["S01"]["callback_count"], 0)
        self.assertFalse(self.rows["S01"]["marker_exists"])

    def test_callback_is_between_load_start_and_success(self) -> None:
        self.assertEqual(self.types("S02"), [
            "scenario_start", "pickle_load_start", "python_callback",
            "marker_created", "pickle_load_success", "scenario_end",
        ])
        self.assertEqual(self.rows["S02"]["callback_count"], 1)

    def test_callback_precedes_real_load_error(self) -> None:
        self.assertEqual(self.types("S03"), [
            "scenario_start", "pickle_load_start", "python_callback",
            "marker_created", "pickle_load_error", "scenario_end",
        ])
        self.assertEqual(self.rows["S03"]["error_type"], "EOFError")
        self.assertTrue(self.rows["S03"]["marker_exists"])

    def test_policy_uses_identical_candidate_bytes(self) -> None:
        self.assertEqual(self.rows["S02"]["candidate_sha256"], self.rows["S04"]["candidate_sha256"])
        self.assertTrue(self.rows["S04"]["policy_blocked"])
        self.assertNotIn("pickle_load_start", self.types("S04"))
        self.assertNotIn("python_callback", self.types("S04"))

    def test_policy_accepts_data_only_json(self) -> None:
        self.assertTrue(self.rows["S04"]["json_loaded"])
        result = json_only_policy(make_fixtures()["data_only_json"], "json")
        self.assertEqual(result, toy_model_data())

    def test_mislabeled_pickle_is_not_a_json_fallback(self) -> None:
        with self.assertRaises((ValueError, UnicodeDecodeError)):
            json_only_policy(make_fixtures()["callback_pickle"], "json")
        self.assertEqual(len(list((self.output / "markers").glob("*.txt"))), 2)

    def test_json_size_and_schema_limits(self) -> None:
        with self.assertRaises(ValueError):
            json_only_policy(b"{}", "json")
        with self.assertRaises(ValueError):
            json_only_policy(b" " * 4097, "json")

    def test_fixture_construction_does_not_execute_callback(self) -> None:
        self.assertIsNone(ACTIVE_CONTEXT.get())
        fixtures = make_fixtures()
        self.assertEqual(fixtures["late_error_pickle"], fixtures["callback_pickle"][:-1])
        self.assertEqual(fixtures["callback_pickle"][-1:], b".")

    def test_callback_refuses_missing_context(self) -> None:
        with self.assertRaises(RuntimeError):
            write_marker()

    def test_existing_output_is_never_overwritten(self) -> None:
        before = (self.output / "summary.json").read_bytes()
        with self.assertRaises(FileExistsError):
            run_experiment(self.output)
        self.assertEqual(before, (self.output / "summary.json").read_bytes())

    def test_jsonl_and_csv_are_identical_representations(self) -> None:
        with (self.output / "events.csv").open(encoding="utf-8", newline="") as handle:
            csv_rows = list(csv.DictReader(handle))
        expected = [{key: csv_value(value) for key, value in row.items()} for row in self.events]
        self.assertEqual(csv_rows, expected)

    def test_summary_matches_result_csv(self) -> None:
        with (self.output / "results.csv").open(encoding="utf-8", newline="") as handle:
            actual = list(csv.DictReader(handle))
        expected = [{key: csv_value(value) for key, value in row.items()}
                    for row in self.summary["scenarios"]]
        self.assertEqual(actual, expected)
        self.assertEqual(self.summary["scenarios_passed"], 4)
        self.assertTrue(self.summary["all_expectations_met"])

    def test_events_are_ordered_unique_and_one_process(self) -> None:
        self.assertEqual([event["sequence"] for event in self.events], list(range(1, len(self.events) + 1)))
        self.assertEqual(len({event["event_id"] for event in self.events}), len(self.events))
        self.assertEqual({event["run_id"] for event in self.events}, {self.summary["run_id"]})
        elapsed = [event["elapsed_ns"] for event in self.events]
        self.assertEqual(elapsed, sorted(elapsed))
        self.assertEqual(len({event["pid"] for event in self.events}), 1)
        self.assertTrue(all(event["is_lab"] and event["telemetry_source"] == TELEMETRY_SOURCE
                            for event in self.events))

    def test_exactly_two_real_marker_files(self) -> None:
        self.assertEqual({path.name for path in (self.output / "markers").iterdir()}, {"S02.txt", "S03.txt"})
        for scenario_id in ("S02", "S03"):
            text = (self.output / "markers" / f"{scenario_id}.txt").read_text()
            self.assertIn("WEEK6_BENIGN_EXECUTION_MARKER", text)
            self.assertIn(f"run_id={self.summary['run_id']}", text)
            self.assertIn(f"scenario_id={scenario_id}", text)
        self.assertEqual(self.summary["marker_count"], 2)

    def test_fixture_manifest_and_non_executing_disassembly(self) -> None:
        fixtures = json.loads((self.output / "fixtures.json").read_text())
        self.assertEqual(len(fixtures), 4)
        self.assertFalse(any(item["stored_as_binary"] for item in fixtures.values()))
        disassembly = (self.output / "callback_disassembly.txt").read_text()
        self.assertIn("lab_helpers write_marker", disassembly)
        self.assertIn("REDUCE", disassembly)
        self.assertEqual(list(self.output.rglob("*.pkl")), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
