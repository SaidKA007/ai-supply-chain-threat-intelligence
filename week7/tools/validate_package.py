"""Validate report files only. Does NOT execute the simulation or a VQL query.

Run: python week7/tools/validate_package.py
Requires Python 3.9+ and the standard library. Safe to run on non-Windows hosts.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def rows(rel: str) -> list[dict[str, str]]:
    with (ROOT / rel).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def patterns(rel: str) -> tuple[str, str]:
    source = text(rel)
    child = re.search(r'WHERE Name =~ ("[^"\n]+")', source)
    parent = re.search(r'AND Parent\.Name =~ ("[^"\n]+")', source)
    if child is None or parent is None:
        raise ValueError(f"Missing expected filter in {rel}")
    # These recorded VQL literals use JSON-compatible double-quoted escapes.
    return json.loads(child.group(1)), json.loads(parent.group(1))


class PackageChecks(unittest.TestCase):
    def test_01_required_files(self) -> None:
        required = (
            "README.md", "simulation/ai_model_loader.py",
            "simulation/negative_control.txt", "docs/mitre_mapping.md",
            "docs/reproduce.md", "docs/sources.md", "evidence/environment.json",
            "evidence/README.md", "evidence/validation_report.txt",
        )
        for rel in required:
            with self.subTest(file=rel):
                self.assertTrue((ROOT / rel).is_file(), rel)

    def test_02_image_integrity_and_png_headers(self) -> None:
        manifest = rows("evidence/screenshots_manifest.csv")
        self.assertEqual(len(manifest), 11)
        self.assertEqual(len({r["evidence_id"] for r in manifest}), 11)
        for entry in manifest:
            path = ROOT / entry["package_file"]
            data = path.read_bytes()
            with self.subTest(image=path.name):
                self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
                w, h = struct.unpack(">II", data[16:24])
                self.assertGreater(w, 100)
                self.assertGreater(h, 80)
                self.assertEqual(hashlib.sha256(data).hexdigest(), entry["packaged_sha256"])

    def test_03_local_markdown_links(self) -> None:
        for path in ROOT.rglob("*.md"):
            content = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
            for dest in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", content):
                if re.match(r"(?:https?://|mailto:)", dest):
                    continue
                dest, _, anchor = dest.partition("#")
                if path.name == "root_readme_snippet.md":
                    target = (ROOT.parent / dest).resolve()
                else:
                    target = (path.parent / unquote(dest)).resolve() if dest else path
                with self.subTest(source=str(path.relative_to(ROOT)), destination=dest):
                    self.assertTrue(target.exists(), str(target))
                    if anchor and target.suffix.lower() == ".md":
                        headings = re.findall(r"^#{1,6}\s+(.+)$", target.read_text(encoding="utf-8"), re.M)
                        slugs = [re.sub(r"[^\w\- ]", "", h.lower()).replace(" ", "-") for h in headings]
                        self.assertIn(anchor, slugs)

    def test_04_python_source_syntax_and_fixed_command(self) -> None:
        tree = ast.parse(text("simulation/ai_model_loader.py"))
        imports = {alias.name for n in ast.walk(tree) if isinstance(n, ast.Import) for alias in n.names}
        self.assertEqual(imports, {"os", "subprocess"})
        runs = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                and isinstance(n.func, ast.Attribute)
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "subprocess" and n.func.attr == "run"]
        self.assertEqual(len(runs), 1)
        self.assertEqual(ast.literal_eval(runs[0].args[0]),
                         ["cmd.exe", "/c", "echo WEEK7_CAR_TEST && timeout /t 120 /nobreak"])

    def test_05_recorded_predicates_match(self) -> None:
        positive = patterns("queries/04_python_cmd_detection.vql")
        negative = patterns("queries/05_negative_test_detection.vql")
        self.assertEqual(positive, negative)
        self.assertEqual(positive, (r"(?i)^cmd\.exe$", r"(?i)^python(\.exe|w\.exe)?$"))
        for pattern in positive:
            re.compile(pattern)
        # Check that the test marker was not silently added to the rule.
        self.assertNotIn("WEEK7_CAR_TEST", text("queries/04_python_cmd_detection.vql"))

    def test_06_transcribed_positive_record(self) -> None:
        records = rows("data/process_rows_transcribed.csv")
        positive = [r for r in records if r["snapshot_id"] == "positive"]
        self.assertEqual(len(positive), 1)
        row = positive[0]
        self.assertEqual((row["Pid"], row["Ppid"], row["ParentName"]),
                         ("8600", "3148", "python.exe"))
        child, parent = patterns("queries/04_python_cmd_detection.vql")
        self.assertIsNotNone(re.search(child, row["Name"]))
        self.assertIsNotNone(re.search(parent, row["ParentName"]))

    def test_07_transcribed_negative_control(self) -> None:
        negative = [r for r in rows("data/process_rows_transcribed.csv") if r["snapshot_id"] == "negative_context"]
        self.assertEqual(len(negative), 2)
        control = next(r for r in negative if "WEEK7_BENIGN_CONTROL" in r["CommandLine"])
        self.assertEqual((control["Pid"], control["Ppid"], control["ParentName"]),
                         ("15836", "2972", "cmd.exe"))
        child, parent = patterns("queries/05_negative_test_detection.vql")
        matches = [r for r in negative if re.search(child, r["Name"]) and re.search(parent, r["ParentName"])]
        self.assertEqual(matches, [])

    def test_08_result_provenance(self) -> None:
        results = rows("data/observed_results.csv")
        by_id = {r["test_id"]: r for r in results}
        self.assertEqual(by_id["B01"]["reported_rows"], "254")
        self.assertEqual(by_id["P01"]["reported_rows"], "1")
        self.assertEqual(by_id["N02"]["reported_rows"], "")
        self.assertEqual(by_id["N02"]["observed_output"], "Table contains no data")
        for r in results:
            self.assertIn("screenshot transcription", r["basis"])

    def test_09_mapping_and_environment(self) -> None:
        mappings = rows("data/mitre_mapping.csv")
        self.assertEqual({r["id"] for r in mappings},
                         {"CAR-2013-02-003", "T1059.003", "T1059.006"})
        env = json.loads(text("evidence/environment.json"))
        self.assertEqual(env["velociraptor_reported"], "0.77.3")
        self.assertFalse(env["siem_execution_observed"])
        self.assertFalse(env["event_stream_configured_in_this_run"])
        self.assertFalse(env["raw_process_export_provided"])

    def test_10_private_text_not_in_public_text_files(self) -> None:
        # Does not perform OCR or certify the complete absence of sensitive data.
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".csv", ".json", ".txt", ".vql"}:
                data = path.read_text(encoding="utf-8").lower()
                with self.subTest(file=str(path.relative_to(ROOT))):
                    self.assertNotRegex(data, r'c:\\users\\(?!redacted|\[redacted\]|<redacted>)[^\\\s"<>]+')
                    self.assertNotIn("begin private key", data)
                    self.assertNotIn("begin rsa private key", data)

    def test_11_checksum_manifest(self) -> None:
        manifest = ROOT / "evidence/SHA256SUMS.txt"
        if not manifest.exists():
            self.skipTest("Checksum manifest not yet generated")
        for line in manifest.read_text(encoding="utf-8").splitlines():
            digest, rel = line.split("  ", 1)
            with self.subTest(file=rel):
                self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    print("Week 7: local package checks only; no Windows process or VQL execution.", flush=True)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PackageChecks)
    result = unittest.TextTestRunner(verbosity=2, stream=sys.stdout).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
