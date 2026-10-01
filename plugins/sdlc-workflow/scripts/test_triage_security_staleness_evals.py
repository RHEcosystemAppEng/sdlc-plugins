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


@pytest.mark.parametrize("context", ["prompt", "expected_output"])
@pytest.mark.parametrize("day_offset, days_old, stale", [(-1, 13, False), (0, 14, False), (1, 15, True)])
def test_fresh_fixture_clock_straddles_strict_production_boundary(context, day_offset, days_old, stale):
    """Catch threshold or fixture drift around the existing fresh case's clock."""
    # Given the actual fresh case, fixture and production threshold contract
    case = _case(20)
    matrix = next(path for path in case["files"] if "security-matrix" in path)
    updated = re.search(r"<!-- Last-Updated: (\S+) -->", (EVAL_DIR / matrix).read_text())
    skill = (ROOT / "plugins/sdlc-workflow/skills/triage-security/SKILL.md").read_text()
    step = skill.split("## Step 0.3 – Matrix Staleness Check", 1)[1].split("## Step 0.5", 1)[0]
    threshold = re.search(r"older than \*\*(\d+) days\*\*", step)
    assert threshold, "production contract must retain a strict older-than threshold"

    # When inspecting either side of the recorded clock without running a skill
    clock = re.search(r"Evaluation clock: (\S+)", case[context])
    age = _timestamp(clock[1]) + timedelta(days=day_offset) - _timestamp(updated[1])

    # Then the actual inputs imply fresh below/at equality and stale above it
    assert age == timedelta(days=days_old)
    assert (age > timedelta(days=int(threshold[1]))) is stale
