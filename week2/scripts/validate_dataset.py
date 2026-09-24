#!/usr/bin/env python3
"""Check the Week 2 package locally. No network access or third-party packages.

This checks file structure, values, and cross-references. It does not verify the
truth of an originating report, assess live indicators, or scan any AI model.
Run from any directory: python path/to/week2/scripts/validate_dataset.py
"""
from __future__ import annotations

import csv
import ipaddress
import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def csv_rows(relative: str) -> list[dict[str, str]]:
    with (ROOT / relative).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def json_data(relative: str):
    with (ROOT / relative).open(encoding="utf-8") as handle:
        return json.load(handle)


def unique(rows: list[dict], key: str) -> set[str]:
    values = [row[key] for row in rows]
    require(all(values), f"Empty identifier: {key}")
    require(len(values) == len(set(values)), f"Duplicate identifier: {key}")
    return set(values)


def check() -> None:
    sources = csv_rows("data/sources.csv")
    cases = csv_rows("data/cases.csv")
    mappings = csv_rows("data/atlas_mappings.csv")
    obs = csv_rows("data/observables.csv")
    metrics = csv_rows("data/published_metrics.csv")
    media = json_data("images/manifest.json")
    metadata = json_data("evidence/build_metadata.json")
    expected = metadata["counts"]
    counts = {
        "technical_source_resources": len(sources), "cases": len(cases),
        "selected_atlas_mappings": len(mappings), "observable_records": len(obs),
        "published_metric_rows": len(metrics), "original_source_figures": len(media),
    }
    require(counts == expected, f"Count mismatch: {counts} != {expected}")
    source_ids = unique(sources, "source_id")
    case_ids = unique(cases, "case_id")
    unique(mappings, "mapping_id")
    unique(obs, "observable_id")
    unique(metrics, "metric_row_id")
    unique(media, "media_id")
    print("PASS: 7 source resources; 4 cases; 14 mappings; 12 observations; 8 measurement rows; 5 figures.")

    for row in sources:
        require(urlsplit(row["url"]).scheme == "https", "Non-HTTPS source URL")
        require(bool(row["locator"]), "Missing source locator")
    for row in cases:
        require(row["atlas_type"] in {"Incident", "Exercise"}, "Unknown case type")
        require(set(row["source_ids"].split(";")) <= source_ids, "Unknown case source")
        require(row["atlas_date_granularity"] in {"Year", "Month", "Day"}, "Unknown date granularity")
    for table in (mappings, obs, metrics):
        for row in table:
            require(row["case_id"] in case_ids, "Unknown case reference")
            require(row["source_id"] in source_ids, "Unknown source reference")
            require(urlsplit(row["source_url"]).scheme == "https", "Invalid source link")
    require(Counter(row["atlas_type"] for row in cases) == {"Incident": 2, "Exercise": 2}, "Case-type counts changed")
    require(len({row["technique_id"] for row in mappings}) == 8, "Expected 8 distinct mapped techniques")
    for row in mappings:
        require(re.fullmatch(r"AML\.T\d{4}(?:\.\d{3})?", row["technique_id"]) is not None, "Invalid technique ID")
        if row["tactic_id"] == "AML.TA0001":
            require(row["tactic_name"] == "AI Attack Adaptation", "Tactic name does not match pinned release")
    print("PASS: Source/case references, 2 Incident + 2 Exercise labels, and selected ATLAS identifiers.")

    cases_json = json_data("data/cases.json")
    require(cases == cases_json, "Case CSV and JSON differ")
    obs_json = json_data("data/observables.json")
    as_csv = [{k: str(v) if isinstance(v, bool) else v for k, v in row.items()} for row in obs_json]
    require(obs == as_csv, "Observable CSV and JSON differ")
    for row in obs:
        value = row["value_as_reported"]
        if row["type"] == "sha1":
            require(re.fullmatch(r"[0-9a-f]{40}", value) is not None, "Invalid SHA-1 length or alphabet")
        elif row["type"] == "sha256":
            require(re.fullmatch(r"[0-9a-f]{64}", value) is not None, "Invalid SHA-256 length or alphabet")
        elif row["type"] == "ipv4":
            ipaddress.IPv4Address(value)
            require("[.]" in row["display_value"], "IPv4 display is not defanged")
        elif row["type"] == "domain_pattern":
            require(value.startswith("*.") and "[.]" in value, "Wildcard/source defanging was lost")
        require(row["to_ids"].lower() == "false", "Unexpected detection approval")
        require(row["current_status"] == "not assessed", "Unexpected current-status claim")
        require(row["first_seen"] == "not established", "Unexpected first-seen claim")
        require(bool(row["source_locator"]) and bool(row["context"]), "Observation lacks provenance/context")
    require(sum(row["assessment_scope"] == "historical_ioc_candidate" for row in obs) == 8, "Candidate count mismatch")
    print("PASS: CSV/JSON agree; hash and IPv4 syntax; wildcard preservation; 8 candidates + 4 context records.")
    print("PASS: Every observation retains unknown first_seen, unassessed current status, and to_ids=false.")

    for row in metrics:
        for col in ("clean_accuracy_C00", "benign_deviation_magnitude", "triggered_accuracy_C11"):
            require(0 <= float(row[col]) <= 1, "Measurement outside proportion range")
        require("not this project" in row["measurement_owner"], "Measurement ownership missing")
        require("NOT attack success rate" in row["metric"], "Metric distinction missing")
    require(metrics[-1]["model_family"] == "Average", "Source-reported Average row missing")
    print("PASS: Published metric units and ownership retained; reported Average not recomputed.")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    image_targets = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", readme)
    require(len(image_targets) == 5, "Expected five embedded figures")
    for row in media:
        require(urlsplit(row["url"]).hostname in {"arxiv.org", "unit42.paloaltonetworks.com"}, "Unexpected image host")
        local = "images/" + row["local_filename"]
        require(row["url"] in image_targets or local in image_targets, "Figure missing from README")
        if local in image_targets:
            require((ROOT / local).is_file(), f"Localized image missing: {local}")
    for document in ROOT.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        # Parse direct Markdown links, including relative image links.
        for target in re.findall(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            require((document.parent / unquote(parsed.path)).exists(), f"Broken relative link in {document.name}: {target}")
    source_map = (ROOT / "docs/source_map.mmd").read_text(encoding="utf-8").strip()
    require(source_map in readme, "README/source Mermaid mismatch")
    print("PASS: Five original figure references, internal Markdown links, and source-map consistency.")
    print("RESULT: Structural validation passed. No network requests, threat scans, or experimental replication performed.")


def main() -> int:
    print("Week 2 — local dataset validation")
    try:
        check()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
