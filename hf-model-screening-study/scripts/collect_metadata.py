#!/usr/bin/env python3
"""Public Hugging Face metadata inventory. Does not download or load model weights.

This is a plumbing pilot, NOT a vulnerability or backdoor detector.
Run from the repository root: python scripts/collect_metadata.py --limit 10
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from importlib.metadata import version
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import sys
import time
from typing import Any

# No implicit account credentials or telemetry for this public metadata pilot.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_DISABLE_IMPLICIT_TOKEN", "1")

SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def serializable(obj: Any) -> Any:
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, datetime):
        return obj.isoformat()
    if is_dataclass(obj):
        return serializable(asdict(obj))
    if isinstance(obj, dict):
        return {str(k): serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [serializable(v) for v in obj]
    return str(obj)


def summarize_files(siblings: Any) -> dict[str, Any]:
    """Filename observations only; an extension is not a verified serialization type."""
    if siblings is None:
        return {"file_listing_available": False, "files": None,
                "extension_counts": None, "has_python": None,
                "has_safetensors": None, "has_pickle_like_extension": None}
    names = sorted({str(s.rfilename) for s in siblings})
    counts: dict[str, int] = {}
    for name in names:
        ext = PurePosixPath(name).suffix.lower() or "[none]"
        counts[ext] = counts.get(ext, 0) + 1
    return {
        "file_listing_available": True,
        "files": names,
        "extension_counts": counts,
        "has_python": ".py" in counts,
        "has_safetensors": ".safetensors" in counts,
        "has_pickle_like_extension": any(ext in counts for ext in (".pkl", ".pickle", ".bin", ".pt", ".pth")),
    }


def collect_one(api: Any, repo_id: str, rank: int, selected_at: str) -> dict[str, Any]:
    head = api.model_info(repo_id, timeout=30, token=False)
    if getattr(head, "private", False):
        raise ValueError("Refusing to inventory a private repository")
    sha = getattr(head, "sha", None)
    if not isinstance(sha, str) or not SHA_PATTERN.fullmatch(sha):
        raise ValueError("No full immutable Git commit SHA returned; record cannot be pinned")
    # Resolve once, then re-read the file list at that exact commit.
    pinned = api.model_info(repo_id, revision=sha, files_metadata=True, timeout=30, token=False)
    if getattr(pinned, "sha", None) != sha:
        raise ValueError("Returned revision differs from requested commit SHA")
    result = {
        "schema_version": 1,
        "model_id": repo_id,
        "selection_rank": rank,
        "selection_observed_at_utc": selected_at,
        "metadata_observed_at_utc": now_utc(),
        "revision_sha": sha,
        "downloads_last_30_days": getattr(head, "downloads", None),
        "likes": getattr(head, "likes", None),
        "pipeline_tag": getattr(head, "pipeline_tag", None),
        "library_name": getattr(head, "library_name", None),
        "last_modified": serializable(getattr(head, "last_modified", None)),
        "tags": serializable(getattr(head, "tags", None)),
        "file_metadata": [serializable(s) for s in pinned.siblings] if pinned.siblings is not None else None,
        "scan_status": "not_run",
        "behavior_test_status": "not_run",
        "backdoor_label": "unknown",
        "remote_code_requirement": "not_assessed",
    }
    result.update(summarize_files(getattr(pinned, "siblings", None)))
    return result


def save_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10, help="Pilot size (1–100); not a representative sample")
    parser.add_argument("--out", type=Path, default=Path("data"))
    parser.add_argument("--repo-id", action="append", help="Optional explicit public repository; repeat this option")
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("Install dependencies: python -m pip install -r requirements.txt", file=sys.stderr)
        return 2

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    out = args.out / f"metadata_{stamp}"
    out.mkdir(parents=True, exist_ok=False)
    api = HfApi(token=False)
    selected_at = now_utc()
    errors: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    selected_ids: list[str] = []
    selection = "explicit_public_ids" if args.repo_id else "top_downloads_public_ungated_text_classification"
    try:
        if args.repo_id:
            selected_ids = list(dict.fromkeys(args.repo_id))[:args.limit]
        else:
            selected_ids = [m.id for m in api.list_models(
                pipeline_tag="text-classification", sort="downloads", gated=False,
                limit=args.limit, full=True, token=False)]
    except Exception as exc:
        errors.append({"stage": "selection", "error_type": type(exc).__name__, "message": str(exc)})

    save_json(out / "selection.json", {"method": selection, "observed_at_utc": selected_at,
                                     "limit": args.limit, "model_ids": selected_ids})
    for rank, repo_id in enumerate(selected_ids, 1):
        try:
            record = collect_one(api, repo_id, rank, selected_at)
            records.append(record)
            print(f"[{rank}/{len(selected_ids)}] inventoried: {repo_id}")
        except Exception as exc:
            errors.append({"stage": "model_info", "model_id": repo_id,
                           "error_type": type(exc).__name__, "message": str(exc)})
            print(f"[{rank}/{len(selected_ids)}] unavailable: {repo_id}", file=sys.stderr)
        time.sleep(0.4)
    with (out / "metadata.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    save_json(out / "errors.json", errors)
    save_json(out / "run.json", {
        "started_at_utc": selected_at, "finished_at_utc": now_utc(),
        "selection_method": selection, "requested": args.limit,
        "selected": len(selected_ids), "collected": len(records), "errors": len(errors),
        "python": platform.python_version(), "huggingface_hub": version("huggingface_hub"),
        "weights_downloaded": False, "models_executed": False,
        "security_scanning_performed": False, "behavioral_testing_performed": False,
        "sample_is_representative": False,
    })
    report = (
        "# Metadata pilot\n\n"
        f"Selection: `{selection}`.\n\n"
        f"Selected repositories: {len(selected_ids)}; metadata records: {len(records)}; errors: {len(errors)}.\n\n"
        "Only public API metadata and filenames were collected. No model weights or repository code "
        "were downloaded or executed. No scanning or behavioral evaluation was performed. "
        "Every repository has `backdoor_label=unknown`.\n\n"
        "This convenience inventory tests data collection, not model safety, backdoor prevalence, "
        "scanner accuracy, or the number of users who did not verify downloads. "
        "File extensions are unverified format hints. Presence of Python files does not establish "
        "whether custom code is required. Missing metadata is not absence of a risk.\n"
    )
    (out / "pilot.md").write_text(report, encoding="utf-8")
    print(f"Saved inventory and status report to: {out}")
    return 0 if records and not errors else (1 if records else 2)


if __name__ == "__main__":
    raise SystemExit(main())
