"""Check staleness eval inputs; hosted evals verify the skill's actual outputs."""

from datetime import datetime, timedelta
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[3]
EVAL_DIR = ROOT / "evals" / "triage-security"


def _case(case_id):
    """Load an existing runnable case without changing its fixture inputs."""
    cases = json.loads((EVAL_DIR / "evals.json").read_text())["evals"]
    return next(case for case in cases if case["id"] == case_id)


def _timestamp(value):
    """Parse the timezone-aware ISO timestamps supplied to the eval."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


@pytest.mark.parametrize("case_id, days_old", [(19, 72), (20, 14)])
def test_executor_and_grader_clock_agree_with_matrix_state(case_id, days_old):
    """Catch absent/divergent clocks and age claims that contradict fixture data."""
    # Given the existing fresh/stale case and its unchanged matrix fixture
    case = _case(case_id)
    matrix = next(path for path in case["files"] if "security-matrix" in path)
    updated = re.search(r"<!-- Last-Updated: (\S+) -->", (EVAL_DIR / matrix).read_text())

    # When reading the clock independently from executor and grader context
    clocks = [re.search(r"Evaluation clock: (\S+)", case[field])
              for field in ("prompt", "expected_output")]

    # Then both contexts describe the actual age under the same fixed clock
    assert all(clocks), "executor and grader need an explicit evaluation clock"
    assert clocks[0][1] == clocks[1][1] == "2026-07-12T10:00:00Z"
    assert _timestamp(clocks[0][1]) - _timestamp(updated[1]) == timedelta(days=days_old)
    assert f"{days_old} days old" in case["expected_output"]
