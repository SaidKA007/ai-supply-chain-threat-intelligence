#!/usr/bin/env python3
"""Run four local, benign model-deserialization teaching scenarios.

Python 3.10+, standard library only. There is deliberately no input-file,
command, target, or network option. Only fixtures built in this source are
passed to pickle.loads(). Never adapt this into a loader for unknown pickles.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import pickle
import pickletools
import platform
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lab_helpers import ACTIVE_CONTEXT, CallbackFixture, LabContext, toy_model_data

SCHEMA_VERSION = "1.0"
TELEMETRY_SOURCE = "week6_application_instrumentation"
SCENARIOS = {
    "S01": "baseline_pickle",
    "S02": "benign_callback_pickle",
    "S03": "callback_then_load_error",
    "S04": "reject_pickle_accept_json",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def csv_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    if not records:
        raise ValueError("Cannot export an empty table without a schema.")
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows({key: csv_value(value) for key, value in row.items()} for row in records)


def write_json(path: Path, value: Any) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


class EventRecorder:
    """Application statements recorded when the indicated code path executes.

    Not Sysmon, an EDR sensor, a packet capture, or independent OS auditing.
    """

    def __init__(self, run_id: str) -> None:
        self.run_id = run_id
        self.started_ns = time.monotonic_ns()
        self.events: list[dict[str, Any]] = []

    def emit(self, event_type: str, scenario_id: str = "RUN", **details: Any) -> dict[str, Any]:
        sequence = len(self.events) + 1
        event = {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "event_id": f"W6-E{sequence:05d}",
            "sequence": sequence,
            "timestamp_utc": utc_now(),
            "elapsed_ns": time.monotonic_ns() - self.started_ns,
            "scenario_id": scenario_id,
            "event_type": event_type,
            "pid": os.getpid(),
            "parent_pid": os.getppid(),
            "telemetry_source": TELEMETRY_SOURCE,
            "is_lab": True,
            "details": details,
        }
        self.events.append(event)
        return event


def make_fixtures() -> dict[str, bytes]:
    baseline = pickle.dumps(toy_model_data(), protocol=2)
    callback = pickle.dumps(CallbackFixture(), protocol=2)
    if callback[-1:] != b".":
        raise RuntimeError("Expected a final STOP opcode in the controlled fixture.")
    # Protocol 2 has no FRAME header. Removing only STOP allows the callback to
    # run before a real EOFError. This is an authored toy failure, not C01 replay.
    late_error = callback[:-1]
    return {
        "baseline_pickle": baseline,
        "callback_pickle": callback,
        "late_error_pickle": late_error,
        "data_only_json": json.dumps(toy_model_data(), sort_keys=True).encode("utf-8"),
    }


def load_known_pickle(data: bytes, recorder: EventRecorder, scenario_id: str) -> tuple[str, str]:
    recorder.emit("pickle_load_start", scenario_id, fixture_sha256=sha256(data))
    try:
        value = pickle.loads(data)  # Only in-memory fixtures made above are allowed here.
    except Exception as exc:
        recorder.emit("pickle_load_error", scenario_id, error_type=type(exc).__name__, message=str(exc))
        return "load_error", type(exc).__name__
    recorder.emit("pickle_load_success", scenario_id, returned_type=type(value).__name__)
    if value != toy_model_data():
        raise RuntimeError("The fixture returned an unexpected object.")
    return "loaded", ""


def json_only_policy(data: bytes, declared_format: str) -> dict[str, Any]:
    """A simple format policy, not an antivirus product or a safe pickle loader."""
    if declared_format != "json":
        raise ValueError("Policy allows JSON only; pickle is not deserialized.")
    if len(data) > 4096:
        raise ValueError("The toy metadata limit is 4096 bytes.")
    result = json.loads(data.decode("utf-8"))
    if result != toy_model_data():
        raise ValueError("The JSON does not match this toy metadata schema.")
    return result


def run_experiment(output_dir: Path, context_label: str = "local-user-run") -> dict[str, Any]:
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10 or newer is required.")
    # Refuse existing paths, including symlinks; never delete an earlier result.
    output_dir = Path(output_dir).absolute()
    if output_dir.exists() or output_dir.is_symlink():
        raise FileExistsError(f"Output already exists; choose a NEW folder: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "markers").mkdir()
    run_id = f"W6-{uuid.uuid4().hex[:12]}"
    recorder = EventRecorder(run_id)
    recorder.emit("run_start", context_label=context_label)
    fixtures = make_fixtures()
    recorder.emit("fixtures_built", fixture_count=len(fixtures), origin="fixed_local_source")
    results: list[dict[str, Any]] = []

    for scenario_id, name in SCENARIOS.items():
        start_index = len(recorder.events)
        recorder.emit("scenario_start", scenario_id, scenario_name=name)
        token = ACTIVE_CONTEXT.set(LabContext(output_dir, run_id, scenario_id, recorder.emit))
        error_type = ""
        policy_blocked = False
        json_loaded = False
        fixture_name = {
            "S01": "baseline_pickle", "S02": "callback_pickle",
            "S03": "late_error_pickle", "S04": "callback_pickle",
        }[scenario_id]
        candidate = fixtures[fixture_name]
        try:
            if scenario_id != "S04":
                outcome, error_type = load_known_pickle(candidate, recorder, scenario_id)
            else:
                # Exactly the same bytes as S02 are offered to this format gate.
                try:
                    json_only_policy(candidate, "pickle")
                except ValueError as exc:
                    policy_blocked = True
                    recorder.emit("policy_reject", scenario_id,
                                  fixture_sha256=sha256(candidate), reason=str(exc))
                recorder.emit("json_load_start", scenario_id,
                              fixture_sha256=sha256(fixtures["data_only_json"]))
                json_only_policy(fixtures["data_only_json"], "json")
                json_loaded = True
                recorder.emit("json_load_success", scenario_id, returned_type="dict")
                outcome = "pickle_blocked_json_loaded"
        finally:
            ACTIVE_CONTEXT.reset(token)

        scoped = recorder.events[start_index:]
        callback_count = sum(event["event_type"] == "python_callback" for event in scoped)
        marker_file = output_dir / "markers" / f"{scenario_id}.txt"
        marker_exists = marker_file.is_file()
        load_attempted = any(event["event_type"] == "pickle_load_start" for event in scoped)
        expected = {
            "S01": ("loaded", 0, False, False, False, ""),
            "S02": ("loaded", 1, True, False, False, ""),
            "S03": ("load_error", 1, True, False, False, "EOFError"),
            "S04": ("pickle_blocked_json_loaded", 0, False, True, True, ""),
        }[scenario_id]
        observed = (outcome, callback_count, marker_exists, policy_blocked, json_loaded, error_type)
        expectation_met = observed == expected
        recorder.emit("scenario_end", scenario_id, outcome=outcome, expectation_met=expectation_met)
        results.append({
            "scenario_id": scenario_id,
            "scenario_name": name,
            "candidate_fixture": fixture_name,
            "candidate_sha256": sha256(candidate),
            "outcome": outcome,
            "pickle_load_attempted": load_attempted,
            "callback_count": callback_count,
            "marker_exists": marker_exists,
            "marker_path": f"markers/{scenario_id}.txt" if marker_exists else "",
            "error_type": error_type,
            "policy_blocked": policy_blocked,
            "json_loaded": json_loaded,
            "expectation_met": expectation_met,
        })

    passed = sum(result["expectation_met"] for result in results)
    recorder.emit("run_complete", scenarios_passed=passed, scenario_count=len(results))
    source_dir = Path(__file__).resolve().parent
    summary = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "started_utc": recorder.events[0]["timestamp_utc"],
        "finished_utc": recorder.events[-1]["timestamp_utc"],
        "execution_context": context_label,
        "evidence_kind": "executed_benign_simulation",
        "telemetry_source": TELEMETRY_SOURCE,
        "environment": {"os_family": platform.system(), "python_version": platform.python_version(),
                        "python_implementation": platform.python_implementation()},
        "source_sha256": {f"simulation/{name}": sha256((source_dir / name).read_bytes())
                          for name in ("run_lab.py", "lab_helpers.py")},
        "event_count": len(recorder.events),
        "scenario_count": len(results),
        "scenarios_passed": passed,
        "marker_count": sum(row["marker_exists"] for row in results),
        "all_expectations_met": passed == len(results),
        "scenarios": results,
        "scope": {
            "fixture_type": "authored in-memory toy objects, not real AI models",
            "payload_behavior": "one fixed in-process Python callback creates a harmless marker",
            "network_operations_in_lab_source": False,
            "child_process_operations_in_lab_source": False,
            "independent_network_or_endpoint_capture": False,
            "production_detection_evaluation": False,
        },
    }
    with (output_dir / "events.jsonl").open("x", encoding="utf-8", newline="\n") as handle:
        for event in recorder.events:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")
    write_csv(output_dir / "events.csv", recorder.events)
    write_csv(output_dir / "results.csv", results)
    write_json(output_dir / "summary.json", summary)
    write_json(output_dir / "fixtures.json", {
        name: {"sha256": sha256(data), "size_bytes": len(data), "stored_as_binary": False}
        for name, data in fixtures.items()
    })
    disassembly = io.StringIO()
    pickletools.dis(fixtures["callback_pickle"], out=disassembly)
    (output_dir / "callback_disassembly.txt").write_text(disassembly.getvalue(), encoding="utf-8")
    console = [
        "Week 6 | ATT&CK T1059.006 | BENIGN LOCAL SIMULATION",
        f"Run: {run_id}", f"Context: {context_label}",
        f"Environment: {summary['environment']['os_family']} / Python {platform.python_version()}",
    ]
    for row in results:
        console.append(
            f"{row['scenario_id']} | {row['outcome']} | callbacks={row['callback_count']} "
            f"| marker={str(row['marker_exists']).lower()} "
            f"| check={'PASS' if row['expectation_met'] else 'FAIL'}"
        )
    console.extend([
        f"Checks: {passed}/{len(results)}; events: {len(recorder.events)}; markers: {summary['marker_count']}",
        "Evidence: application instrumentation and marker files; not victim telemetry.",
        "The lab source performs no network access and launches no child process.",
    ])
    (output_dir / "console.txt").write_text("\n".join(console) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="NEW output folder; existing folders are refused")
    parser.add_argument("--context", choices=["local-user-run", "assistant-verification-environment"],
                        default="local-user-run", help="Provenance label, not a security setting")
    args = parser.parse_args()
    suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:6]
    output = args.output or Path(__file__).resolve().parents[1] / "runs" / suffix
    try:
        summary = run_experiment(output, args.context)
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print((output / "console.txt").read_text(encoding="utf-8"), end="")
    print(f"Results saved to: {output.resolve()}")
    return 0 if summary["all_expectations_met"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
