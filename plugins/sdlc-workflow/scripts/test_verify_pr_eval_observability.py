"""Check verify-pr evidence requests and fixtures; hosted evals grade actual outputs."""

import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[3]
EVAL_DIR = ROOT / "evals" / "verify-pr"


def _case():
    """Load the existing review-feedback case without changing its inputs."""
    cases = json.loads((EVAL_DIR / "evals.json").read_text())["evals"]
    return next(case for case in cases if case["id"] == 3)


@pytest.mark.parametrize("evidence", [
    r"author check against github-actions\[bot\]",
    r"body marker check for ## Eval Results",
    r"body footer check for sdlc-workflow/run-evals",
    r"number of reviews matching all three checks",
    r"resulting Eval Quality verdict and its effect on the Test Quality combination",
])
def test_case3_requests_detection_evidence_in_report(evidence):
    """Catch detection facts mentioned as inputs but never requested in the report."""
    # Given the actual review-feedback case prompt
    prompt = _case()["prompt"]

    # When isolating requests to record evidence in the grader-visible report
    requests = re.findall(r"Record (.+?) in outputs/report\.md", prompt)

    # Then every detection fact and its verdict impact is requested for actual reviews
    assert any("each actual review" in request and re.search(evidence, request)
               for request in requests), evidence


def test_case3_requests_fixture_based_detection_and_conditional_na():
    """Catch invented review evidence, inline/body confusion, and unconditional N/A."""
    # Given the actual prompt, rather than its declarative expected output
    prompt = _case()["prompt"]

    # When inspecting the detection source and no-match reporting instructions
    source = re.search(r"Inspect only (.+?) for Eval Quality detection", prompt)
    no_match = re.search(r"When no review matches all three checks, (.+?)\.", prompt)

    # Then the report must derive evidence from the supplied Reviews list only
    assert source, "the detection request must identify the supplied review inventory"
    assert "supplied Reviews JSON list in pr-review-comments.md" in source[1]
    assert no_match, "N/A reporting must be conditional on the actual match result"
    assert "Eval Quality is N/A" in no_match[1]
    assert "does not affect the Test Quality combination" in no_match[1]
    assert "do not invent reviews, treat inline comments as review bodies, or call live GitHub/Jira" in prompt


def test_case3_fixture_supplies_review_inputs_with_no_qualifying_eval_review():
    """Verify the fixture's actual review author/body values imply no eval match."""
    # Given the review fixture mounted by the existing case
    case = _case()
    assert "files/pr-review-comments.md" in case["files"]
    fixture = (EVAL_DIR / "files/pr-review-comments.md").read_text()

    # When reading the Reviews JSON, excluding the separate inline comments list
    reviews_section = fixture.split("## Reviews (", 1)[1].split("\n## Review Comments (", 1)[0]
    reviews = json.loads(re.search(r"```json\n(.+?)\n```", reviews_section, re.S)[1])
    inputs = [(review["id"], review["user"]["login"], review["body"]) for review in reviews]
    checks = [(review_id, author == "github-actions[bot]", "## Eval Results" in body,
               "sdlc-workflow/run-evals" in body) for review_id, author, body in inputs]

    # Then the supplied human review fails all three checks and yields no matches
    assert inputs == [(20001, "reviewer-a",
                       "Good approach overall. A few things to address before we can merge.")]
    assert checks == [(20001, False, False, False)]
    assert [review_id for review_id, author, marker, footer in checks
            if author and marker and footer] == []


@pytest.mark.parametrize("criterion", [
    "github-actions[bot]", "## Eval Results", "sdlc-workflow/run-evals",
])
def test_case3_assertion_agrees_with_production_detection_criteria(criterion):
    """Catch criterion drift between the unchanged assertion and production contract."""
    # Given the existing case 3 detection assertion and production skill
    assertion = _case()["assertions"][13]
    skill = (ROOT / "plugins/sdlc-workflow/skills/verify-pr/SKILL.md").read_text()

    # When isolating the production three-condition detection contract
    detection = skill.split("### Step 4a.1 – Detect Eval Result Reviews", 1)[1].split("### Step 4b", 1)[0]

    # Then both contracts retain each independently declared detection criterion
    assert criterion in assertion
    assert criterion in detection


def test_case6_human_classification_allows_an_explicit_non_eval_explanation():
    """Reject lexical bans that penalize correctly distinguishing human feedback."""
    # Given the retained human-comment classification assertion
    cases = json.loads((EVAL_DIR / "evals.json").read_text())["evals"]
    case = next(case for case in cases if case["id"] == 6)
    assertion = case["assertions"][2]

    # Then the contract tests classification grounds rather than forbidden words
    assert "its classification does not reference eval detection or eval metrics" not in assertion
    assert "classification is grounded in the human reviewer's substantive feedback" in assertion
    assert "Explicitly explaining that the comment is not an eval result is allowed" in assertion
    assert "treated as an automated eval result or classified using eval metrics" in assertion
    assert len(cases) == 6 and sum(len(item["assertions"]) for item in cases) == 68
