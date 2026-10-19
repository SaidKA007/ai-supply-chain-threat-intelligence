"""Fixed, benign callback for the Week 6 teaching experiment.

No shell, network, credentials, model download, or arbitrary input is used.
The callback needs a context created by run_lab.py and writes one new marker
inside that run's output directory. This is NOT a general-purpose sandbox.
"""
from __future__ import annotations

from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class LabContext:
    output_dir: Path
    run_id: str
    scenario_id: str
    emit: Callable[..., dict[str, Any]]


ACTIVE_CONTEXT: ContextVar[LabContext | None] = ContextVar("week6_context", default=None)


def toy_model_data() -> dict[str, Any]:
    """A small dictionary, not a trained model or real inference pipeline."""
    return {
        "model_name": "week6-toy-model",
        "weights": [0.25, 0.50, 0.75],
        "purpose": "teaching-only",
    }


def write_marker() -> dict[str, Any]:
    """Executed by the unpickler's REDUCE opcode, never directly by the runner."""
    context = ACTIVE_CONTEXT.get()
    if context is None or context.scenario_id not in {"S01", "S02", "S03", "S04"}:
        raise RuntimeError("The fixed callback requires an active Week 6 lab context.")
    context.emit("python_callback", context.scenario_id, callback="lab_helpers.write_marker")
    relative = Path("markers") / f"{context.scenario_id}.txt"
    marker = context.output_dir / relative
    # Exclusive creation: a run cannot silently replace an earlier marker.
    with marker.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(
            "WEEK6_BENIGN_EXECUTION_MARKER\n"
            f"run_id={context.run_id}\n"
            f"scenario_id={context.scenario_id}\n"
            "This file is a harmless lab marker, not a malware indicator.\n"
        )
    context.emit("marker_created", context.scenario_id, relative_path=relative.as_posix())
    return toy_model_data()


class CallbackFixture:
    """Serializes a reference to the single fixed callback with no arguments."""

    def __reduce__(self) -> tuple[Callable[[], dict[str, Any]], tuple[()]]:
        # __reduce__ runs while constructing the fixture. The callable it returns
        # runs later, DURING unpickling. These are different moments.
        return write_marker, ()
