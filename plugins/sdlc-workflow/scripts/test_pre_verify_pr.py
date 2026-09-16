#!/usr/bin/env python3
"""Tests for pre_verify_pr.py — PR URL extraction, GitHub bundle, transform."""

import json
import os
import re
import subprocess
import sys
import tempfile

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
import pre_verify_pr


# --- extract_pr_url ---

def test_extract_pr_url_adf_inline_card():
    issue = {"fields": {"customfield_10875": {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "inlineCard", "attrs": {"url": "https://github.com/org/repo/pull/42"}}
        ]}]
    }}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "https://github.com/org/repo/pull/42", f"Got: {result}"


def test_extract_pr_url_plain_string():
    issue = {"fields": {"customfield_10875": "https://github.com/org/repo/pull/7"}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "https://github.com/org/repo/pull/7", f"Got: {result}"


def test_extract_pr_url_missing_field():
    issue = {"fields": {}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "", f"Expected empty string, got: {result}"


def test_extract_pr_url_null_field():
    issue = {"fields": {"customfield_10875": None}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "", f"Expected empty string, got: {result}"


def test_extract_pr_url_adf_no_inline_card():
    issue = {"fields": {"customfield_10875": {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "text", "text": "no link here"}
        ]}]
    }}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "", f"Expected empty string, got: {result}"


def test_extract_pr_url_adf_text_link_mark():
    """ADF text node carrying a link mark (how a manually-typed link is stored)."""
    issue = {"fields": {"customfield_10875": {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "text", "text": "PR", "marks": [
                {"type": "link", "attrs": {
                    "href": "https://github.com/org/repo/pull/13"}}
            ]}
        ]}]
    }}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "https://github.com/org/repo/pull/13", f"Got: {result}"


def test_extract_pr_url_adf_plain_text_url():
    """ADF plain text that merely contains a bare URL (no mark, no card)."""
    issue = {"fields": {"customfield_10875": {
        "type": "doc", "version": 1,
        "content": [{"type": "paragraph", "content": [
            {"type": "text", "text": "see https://github.com/org/repo/pull/99 for details"}
        ]}]
    }}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "https://github.com/org/repo/pull/99", f"Got: {result}"


def test_extract_pr_url_string_with_surrounding_text():
    """Plain-string field whose value embeds a URL among other text."""
    issue = {"fields": {"customfield_10875": "PR: https://github.com/org/repo/pull/5."}}
    result = pre_verify_pr.extract_pr_url(issue)
    assert result == "https://github.com/org/repo/pull/5", f"Got: {result}"


# --- build_github_bundle ---

def test_build_github_bundle():
    bundle = pre_verify_pr.build_github_bundle(
        pr_repo="org/repo", pr_number="42", head_ref="feat/x",
        commit_sha="abc1234", diff="diff --git a b", stat=" 1 file changed",
        reviews=[{"id": 1}], review_comments=[{"id": 2}],
        issue_comments=[{"id": 3}], commits=[{"oid": "abc1234"}],
        check_runs=[{"name": "pytest", "status": "completed",
                     "conclusion": "success", "details_url": "https://ci/1"}],
    )
    assert bundle["pr_repo"] == "org/repo"
    assert bundle["pr_number"] == 42  # coerced to int
    assert bundle["headRefName"] == "feat/x"
    assert bundle["commit_sha"] == "abc1234"
    assert bundle["diff"] == "diff --git a b"
    assert bundle["stat"] == " 1 file changed"
    assert bundle["reviews"] == [{"id": 1}]
    assert bundle["review_comments"] == [{"id": 2}]
    assert bundle["issue_comments"] == [{"id": 3}]
    assert bundle["commits"] == [{"oid": "abc1234"}]
    assert bundle["check_runs"] == [{"name": "pytest", "status": "completed",
                                     "conclusion": "success",
                                     "details_url": "https://ci/1"}]


def test_build_github_bundle_check_runs_defaults_to_empty_list():
    """A PR head with no checks yields check_runs=[], never absent.

    The github object is additionalProperties:false with check_runs required, so
    the key must always be present for the prefetch to validate against
    verify-pr-input.schema.json.
    """
    # Given a bundle built without an explicit check_runs argument
    bundle = pre_verify_pr.build_github_bundle(
        "o/r", 5, "b", "deadbee", "d", "s", [], [], [], [],
    )

    # Then check_runs is present and defaults to an empty list
    assert bundle["check_runs"] == []


# --- transform_to_input ---

def test_transform_basic():
    issue = {"fields": {
        "summary": "Add feature X",
        "description": {"type": "doc", "content": []},
        "status": {"name": "In Progress"},
        "labels": ["backend", "api"],
        "issuelinks": [],
    }}
    result = pre_verify_pr.transform_to_input(issue, "TC-100", "https://github.com/o/r/pull/1")
    assert result["task_id"] == "TC-100"
    assert result["task"]["summary"] == "Add feature X"
    assert result["task"]["status"] == "In Progress"
    assert result["task"]["labels"] == ["backend", "api"]
    assert result["task"]["issue_links"] == []
    assert result["pr_url"] == "https://github.com/o/r/pull/1"
    assert result["source"]["tracker"] == "jira"
    assert result["source"]["raw"] is issue


def test_transform_without_github_omits_key():
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "")
    assert "github" not in result


def test_transform_with_github():
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    github = pre_verify_pr.build_github_bundle(
        "o/r", 5, "b", "deadbee", "d", "s", [], [], [], [],
    )
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "https://github.com/o/r/pull/5", github)
    assert result["github"]["pr_repo"] == "o/r"
    assert result["github"]["pr_number"] == 5
    assert result["github"]["commit_sha"] == "deadbee"


def test_transform_embeds_check_runs_under_github():
    """The CI check-run outcomes are embedded under the github bundle.

    Mirrors the reviews/comments bundle tests: correctness.md Check 1 reads
    github.check_runs in sandbox mode, so the transform must pass them through.
    """
    # Given an issue and a github bundle carrying head-SHA CI check-run outcomes
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    check_runs = [
        {"name": "pytest", "status": "completed", "conclusion": "success",
         "details_url": "https://ci/pytest"},
        {"name": "skillsaw", "status": "completed", "conclusion": "failure",
         "details_url": "https://ci/skillsaw"},
    ]
    github = pre_verify_pr.build_github_bundle(
        "o/r", 5, "b", "deadbee", "d", "s", [], [], [], [], check_runs,
    )

    # When transforming to the tracker-agnostic input
    result = pre_verify_pr.transform_to_input(
        issue, "TC-1", "https://github.com/o/r/pull/5", github)

    # Then the check-run outcomes are embedded verbatim under github.check_runs
    assert result["github"]["check_runs"] == check_runs


# --- commit_references_task (Commit Traceability determinism) ---

def test_commit_references_task_in_body_trailer():
    # The canonical failure mode: the ID lives only in the body trailer, far
    # past where a subject-only or truncated read would look.
    commit = {
        "messageHeadline": "feat(verify-pr): re-sync sandbox dual-mode onto SKILL.md",
        "messageBody": "Long body paragraph ...\n\nImplements TC-5812\n\nAssisted-by: x",
    }
    assert pre_verify_pr.commit_references_task(commit, "TC-5812") is True


def test_commit_references_task_in_headline():
    commit = {"messageHeadline": "TC-5812: fix scope", "messageBody": ""}
    assert pre_verify_pr.commit_references_task(commit, "TC-5812") is True


def test_commit_references_task_absent():
    commit = {"messageHeadline": "fix: thing", "messageBody": "no id here"}
    assert pre_verify_pr.commit_references_task(commit, "TC-5812") is False


def test_commit_references_task_word_boundary():
    # A superstring ID must not match, nor a different task in the same family.
    assert pre_verify_pr.commit_references_task(
        {"messageHeadline": "x", "messageBody": "see TC-58120"}, "TC-5812") is False
    assert pre_verify_pr.commit_references_task(
        {"messageHeadline": "x", "messageBody": "the TC-5982 fix"}, "TC-5812") is False


def test_commit_references_task_missing_body_key():
    assert pre_verify_pr.commit_references_task(
        {"messageHeadline": "TC-5812: x"}, "TC-5812") is True


def test_transform_annotates_commit_references_task_id():
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    commits = [
        {"oid": "aaa", "messageHeadline": "feat: x", "messageBody": "Implements TC-5812"},
        {"oid": "bbb", "messageHeadline": "fix: y", "messageBody": "TC-6033 unrelated"},
    ]
    github = pre_verify_pr.build_github_bundle(
        "o/r", 5, "b", "aaa", "d", "s", [], [], [], commits,
    )
    result = pre_verify_pr.transform_to_input(issue, "TC-5812", "", github)
    annotated = result["github"]["commits"]
    assert annotated[0]["references_task_id"] is True
    assert annotated[1]["references_task_id"] is False


def test_transform_issue_links():
    issue = {"fields": {
        "summary": "S", "description": {}, "status": {"name": "Open"},
        "labels": [], "issuelinks": [
            {"type": {"name": "Blocks"}, "outwardIssue": {"key": "TC-200"}},
            {"type": {"name": "Related"}, "inwardIssue": {"key": "TC-300"}},
        ],
    }}
    links = pre_verify_pr.transform_to_input(issue, "TC-100", "")["task"]["issue_links"]
    assert len(links) == 2
    assert links[0] == {"type": "Blocks", "direction": "outward", "key": "TC-200"}
    assert links[1] == {"type": "Related", "direction": "inward", "key": "TC-300"}


def test_transform_custom_fields():
    issue = {"fields": {
        "summary": "S", "description": {}, "status": None, "labels": [],
        "issuelinks": [],
        "customfield_10875": "https://github.com/o/r/pull/5",
        "customfield_99999": {"value": "something"},
        "priority": {"name": "High"},
    }}
    cf = pre_verify_pr.transform_to_input(issue, "TC-1", "")["task"]["custom_fields"]
    assert "customfield_10875" in cf
    assert "customfield_99999" in cf
    assert "priority" not in cf


def test_transform_empty_fields():
    issue = {"fields": {}}
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "")
    assert result["task"]["summary"] == ""
    assert result["task"]["status"] == ""
    assert result["task"]["labels"] == []
    assert result["task"]["issue_links"] == []


def test_transform_null_status():
    issue = {"fields": {"summary": "S", "status": None, "labels": [], "issuelinks": []}}
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "")
    assert result["task"]["status"] == ""


def test_transform_null_description_coerced_to_object():
    """An explicit null description becomes {} so task.description stays an object.

    Regression for Sourcery id 3896899434: `fields.get("description", {})` only
    defaults on an absent key, so an explicit JSON null (an issue with no
    description) yielded task.description = null, violating the input schema.
    """
    # Given a Jira issue whose description field is an explicit null
    issue = {"fields": {"summary": "S", "description": None, "status": {"name": "Open"},
                        "labels": [], "issuelinks": []}}

    # When transforming it to the tracker-agnostic input
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "")

    # Then the null is coerced to an empty object, not left as null
    assert result["task"]["description"] == {}, \
        f"expected {{}}, got: {result['task']['description']!r}"
    assert isinstance(result["task"]["description"], dict)


def test_null_description_input_validates_against_schema():
    """A produced input with a null-source description validates against the schema.

    Drives the full transform (task + github bundle) for an issue with a null
    description and asserts the result satisfies verify-pr-input.schema.json —
    the acceptance criterion for TC-5886. Without the null coercion the instance
    would carry task.description = null and fail (description must be an object).
    """
    from jsonschema import validate

    # Given an issue with a null description and the prefetched github bundle a
    # real run embeds (the schema requires `github`, so a bare task won't do)
    issue = {"fields": {"summary": "S", "description": None, "status": {"name": "Open"},
                        "labels": [], "issuelinks": []}}
    github = pre_verify_pr.build_github_bundle(
        "o/r", 5, "feat/x", "deadbee", "diff", "stat", [], [], [], [],
    )

    # When producing the input and loading the input schema
    result = pre_verify_pr.transform_to_input(
        issue, "TC-1", "https://github.com/o/r/pull/5", github)
    schema_path = os.path.join(
        script_dir, "..", "schemas", "verify-pr-input.schema.json")
    with open(schema_path) as f:
        schema = json.load(f)

    # Then it validates cleanly (validate raises ValidationError on failure)
    assert result["task"]["description"] == {}
    validate(instance=result, schema=schema)


def test_transform_large_payload():
    """Regression test: large payloads must work via stdin, not argv."""
    issue = {"fields": {
        "summary": "Large issue",
        "description": "x" * 500_000,
        "status": {"name": "Open"},
        "labels": [],
        "issuelinks": [],
    }}
    payload = json.dumps(issue)
    assert len(payload) > 500_000

    result = subprocess.run(
        [sys.executable, os.path.join(script_dir, "pre_verify_pr.py"),
         "transform", "TC-BIG", "https://example.com/pr/1"],
        input=payload, capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    output = json.loads(result.stdout)
    assert output["task_id"] == "TC-BIG"
    assert output["task"]["summary"] == "Large issue"
    assert "github" not in output


def test_cli_transform_github_dir():
    """CLI transform reads the raw GitHub files and embeds the bundle."""
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "pr.diff"), "w") as f:
            f.write("diff --git a b\n")
        with open(os.path.join(d, "pr.stat"), "w") as f:
            f.write(" 1 file changed\n")
        for name, payload in [
            ("reviews.json", [{"id": 1, "state": "APPROVED"}]),
            ("review-comments.json", [{"id": 2}]),
            ("issue-comments.json", [{"id": 3}]),
            ("commits.json", [{"oid": "abc1234def"}]),
            ("check-runs.json", [{"name": "pytest", "status": "completed",
                                  "conclusion": "success",
                                  "details_url": "https://ci/1"}]),
        ]:
            with open(os.path.join(d, name), "w") as f:
                json.dump(payload, f)

        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, "pre_verify_pr.py"),
             "transform", "TC-9", "https://github.com/o/r/pull/9",
             "--github-dir", d, "--pr-repo", "o/r", "--pr-number", "9",
             "--head-ref", "feat/x", "--commit-sha", "abc1234def"],
            input=json.dumps(issue), capture_output=True, text=True,
        )
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    output = json.loads(result.stdout)
    gh = output["github"]
    assert gh["pr_repo"] == "o/r"
    assert gh["pr_number"] == 9
    assert gh["headRefName"] == "feat/x"
    assert gh["commit_sha"] == "abc1234def"
    assert gh["diff"] == "diff --git a b\n"
    assert gh["stat"] == " 1 file changed\n"
    assert gh["reviews"] == [{"id": 1, "state": "APPROVED"}]
    assert gh["review_comments"] == [{"id": 2}]
    assert gh["issue_comments"] == [{"id": 3}]
    # transform annotates each commit with the deterministic traceability fact.
    assert gh["commits"] == [{"oid": "abc1234def", "references_task_id": False}]
    assert gh["check_runs"] == [{"name": "pytest", "status": "completed",
                                 "conclusion": "success",
                                 "details_url": "https://ci/1"}]


# --- idempotency prefetch (related_keys, build_idempotency_bundle, transform) ---

def test_related_keys_from_subtasks_and_links():
    """related_keys collects sub-task keys and linked-issue keys, deduped/sorted."""
    issue = {"fields": {
        "subtasks": [{"key": "TC-201"}, {"key": "TC-202"}],
        "issuelinks": [
            {"type": {"name": "Blocks"}, "inwardIssue": {"key": "TC-202"}},
            {"type": {"name": "Related"}, "outwardIssue": {"key": "TC-300"}},
        ],
    }}
    # TC-202 appears as both a sub-task and a link — deduped; result is sorted
    assert pre_verify_pr.related_keys(issue) == ["TC-201", "TC-202", "TC-300"]


def test_related_keys_empty_when_no_relations():
    issue = {"fields": {"summary": "S"}}
    assert pre_verify_pr.related_keys(issue) == []


def test_build_idempotency_bundle_extracts_fields_and_comments():
    """The bundle carries the fields the dedup checks inspect, incl. comment bodies."""
    ri = {
        "key": "TC-500",
        "fields": {
            "summary": "Fix eval-3 assertion failures",
            "labels": ["ai-generated-jira", "eval-failure"],
            "description": {"type": "doc", "content": []},
            "issuetype": {"name": "Sub-task"},
            "comment": {"comments": [
                {"body": {"type": "doc", "content": [{"type": "text"}]}},
                {"body": {"type": "doc"}},
            ]},
        },
    }
    bundle = pre_verify_pr.build_idempotency_bundle([ri])
    entry = bundle["related_issues"][0]
    assert entry["key"] == "TC-500"
    assert entry["summary"] == "Fix eval-3 assertion failures"
    assert entry["labels"] == ["ai-generated-jira", "eval-failure"]
    assert entry["description"] == {"type": "doc", "content": []}
    assert entry["issuetype"] == "Sub-task"
    assert len(entry["comments"]) == 2
    assert entry["comments"][0] == {"type": "doc", "content": [{"type": "text"}]}


def test_build_idempotency_bundle_handles_missing_fields():
    """A related issue lacking comments/description yields empty defaults, not errors."""
    bundle = pre_verify_pr.build_idempotency_bundle([{"key": "TC-9", "fields": {}}])
    entry = bundle["related_issues"][0]
    assert entry["summary"] == ""
    assert entry["labels"] == []
    assert entry["description"] == {}  # null/absent coerced to object
    assert entry["issuetype"] == ""
    assert entry["comments"] == []


def test_build_idempotency_bundle_empty():
    assert pre_verify_pr.build_idempotency_bundle([]) == {"related_issues": []}


def test_transform_with_idempotency_attaches_key():
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    idem = pre_verify_pr.build_idempotency_bundle([{"key": "TC-1", "fields": {}}])
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "", None, idem)
    assert result["idempotency"]["related_issues"][0]["key"] == "TC-1"


def test_transform_without_idempotency_defaults_to_empty():
    """With no idempotency supplied, transform still emits an empty bundle.

    Option 1 of TC-6026: the key is always present so the tokenless sandbox
    always has a data source for the Steps 6d/6f/7c dedup checks — a missing
    argument degrades to "no known duplicates", never an omitted key.
    """
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    result = pre_verify_pr.transform_to_input(issue, "TC-1", "")
    assert result["idempotency"] == {"related_issues": []}


def test_cli_transform_idempotency_dir():
    """CLI transform globs the related-issue JSONs and embeds the idempotency bundle."""
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "TC-501.json"), "w") as f:
            json.dump({"key": "TC-501", "fields": {
                "summary": "Existing sub-task", "labels": ["review-feedback"],
                "description": {"type": "doc"}, "issuetype": {"name": "Sub-task"},
                "comment": {"comments": [{"body": {"type": "doc"}}]},
            }}, f)
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, "pre_verify_pr.py"),
             "transform", "TC-1", "https://github.com/o/r/pull/1",
             "--idempotency-dir", d],
            input=json.dumps(issue), capture_output=True, text=True,
        )
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    output = json.loads(result.stdout)
    related = output["idempotency"]["related_issues"]
    assert len(related) == 1
    assert related[0]["key"] == "TC-501"
    assert related[0]["labels"] == ["review-feedback"]
    assert related[0]["comments"] == [{"type": "doc"}]


def test_cli_transform_empty_idempotency_dir():
    """An empty related-issues dir yields an empty related_issues list, not an error."""
    issue = {"fields": {"summary": "S", "status": {"name": "Open"}, "labels": [], "issuelinks": []}}
    with tempfile.TemporaryDirectory() as d:
        result = subprocess.run(
            [sys.executable, os.path.join(script_dir, "pre_verify_pr.py"),
             "transform", "TC-1", "https://github.com/o/r/pull/1",
             "--idempotency-dir", d],
            input=json.dumps(issue), capture_output=True, text=True,
        )
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    assert json.loads(result.stdout)["idempotency"] == {"related_issues": []}


def test_cli_related_keys():
    """The related-keys subcommand prints sub-task and linked-issue keys."""
    issue = {"fields": {
        "subtasks": [{"key": "TC-201"}],
        "issuelinks": [{"type": {"name": "Related"}, "outwardIssue": {"key": "TC-300"}}],
    }}
    result = subprocess.run(
        [sys.executable, os.path.join(script_dir, "pre_verify_pr.py"), "related-keys"],
        input=json.dumps(issue), capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    assert result.stdout.split() == ["TC-201", "TC-300"]


def test_idempotency_input_validates_against_schema():
    """A produced input carrying the idempotency bundle validates against the schema."""
    from jsonschema import validate

    issue = {"fields": {"summary": "S", "description": {}, "status": {"name": "Open"},
                        "labels": [], "issuelinks": []}}
    github = pre_verify_pr.build_github_bundle(
        "o/r", 5, "feat/x", "deadbee", "diff", "stat", [], [], [], [])
    idem = pre_verify_pr.build_idempotency_bundle([{"key": "TC-9", "fields": {
        "summary": "Existing", "labels": ["review-feedback"],
        "description": {"type": "doc"}, "issuetype": {"name": "Sub-task"},
        "comment": {"comments": [{"body": {"type": "doc"}}]},
    }}])
    result = pre_verify_pr.transform_to_input(
        issue, "TC-1", "https://github.com/o/r/pull/5", github, idem)
    schema_path = os.path.join(
        script_dir, "..", "schemas", "verify-pr-input.schema.json")
    with open(schema_path) as f:
        schema = json.load(f)
    validate(instance=result, schema=schema)  # raises on failure


def test_prefetch_omitting_idempotency_fails_schema_validation():
    """A prefetch lacking the idempotency bundle is rejected by the schema.

    Option 1 of TC-6026: idempotency is a top-level required key, so Step 0.7
    validation rejects a bundle that omits it *before* any consuming step runs —
    the fail-fast contract from TC-5980/TC-5981. This closes the gap that let a
    schema-valid prefetch skip the tokenless dedup checks silently.
    """
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError

    # Given an otherwise-valid input (task + github) with no idempotency key
    issue = {"fields": {"summary": "S", "description": {}, "status": {"name": "Open"},
                        "labels": [], "issuelinks": []}}
    github = pre_verify_pr.build_github_bundle(
        "o/r", 5, "feat/x", "deadbee", "diff", "stat", [], [], [], [])
    instance = pre_verify_pr.transform_to_input(
        issue, "TC-1", "https://github.com/o/r/pull/5", github)
    del instance["idempotency"]  # simulate an older/hand-supplied bundle

    schema_path = os.path.join(
        script_dir, "..", "schemas", "verify-pr-input.schema.json")
    with open(schema_path) as f:
        schema = json.load(f)

    # When validating it against the input schema, Then it is rejected
    try:
        validate(instance=instance, schema=schema)
        assert False, "schema accepted a prefetch missing idempotency"
    except ValidationError as e:
        assert "idempotency" in str(e), f"unexpected error: {e}"


def test_incomplete_related_issue_fails_schema_validation():
    """A related-issue entry missing a per-item field is rejected by the schema.

    TC-6032: idempotency.related_issues.items requires the fields the dedup
    checks consume (Steps 6d/6f/7c). Without a per-item `required` list, a
    structurally incomplete entry passed Step 0.7 and dedup silently treated it
    as non-matching — the item-level analogue of the TC-6026 array-level gap.
    """
    from jsonschema import validate
    from jsonschema.exceptions import ValidationError

    # Given an otherwise-valid input whose sole related issue omits `comments`
    issue = {"fields": {"summary": "S", "description": {}, "status": {"name": "Open"},
                        "labels": [], "issuelinks": []}}
    github = pre_verify_pr.build_github_bundle(
        "o/r", 5, "feat/x", "deadbee", "diff", "stat", [], [], [], [])
    instance = pre_verify_pr.transform_to_input(
        issue, "TC-1", "https://github.com/o/r/pull/5", github)
    instance["idempotency"] = {"related_issues": [{
        "key": "TC-9", "summary": "Existing", "labels": [],
        "description": {}, "issuetype": "Sub-task",
        # `comments` intentionally omitted
    }]}

    schema_path = os.path.join(
        script_dir, "..", "schemas", "verify-pr-input.schema.json")
    with open(schema_path) as f:
        schema = json.load(f)

    # When validating it against the input schema, Then it is rejected
    try:
        validate(instance=instance, schema=schema)
        assert False, "schema accepted a related issue missing a required field"
    except ValidationError as e:
        assert "comments" in str(e), f"unexpected error: {e}"


# --- stat production (pre-verify-pr.sh) ---

pre_verify_sh = os.path.join(script_dir, "pre-verify-pr.sh")


def test_stat_produced_by_git_apply_stat():
    """The stat mechanism (git apply --stat) yields a diffstat matching the
    downstream github.stat contract: a per-file line plus a summary line.

    Exercises the real command pre-verify-pr.sh runs, not a gh stub that
    silently accepts the unsupported --stat flag.
    """
    # Given a unified diff like the one gh pr diff writes to pr.diff
    patch = (
        "diff --git a/foo.txt b/foo.txt\n"
        "index 1111111..2222222 100644\n"
        "--- a/foo.txt\n"
        "+++ b/foo.txt\n"
        "@@ -1,3 +1,3 @@\n"
        " line1\n"
        "-line2\n"
        "+CHANGED\n"
        " line3\n"
    )
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "pr.diff"), "w") as f:
            f.write(patch)

        # When producing the stat with the exact command pre-verify-pr.sh uses.
        # Run it from the (non-repo) temp dir: `git apply --stat` is CWD-sensitive
        # — inside a repo subdirectory it scopes the patch to that subtree and
        # reports "0 files changed", so cwd=d keeps this a pure textual diffstat
        # independent of where the test runner is launched.
        result = subprocess.run(
            ["git", "apply", "--stat", "pr.diff"],
            cwd=d, capture_output=True, text=True,
        )

    # Then it succeeds and emits a git diffstat downstream can consume
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    assert "foo.txt" in result.stdout, f"Got: {result.stdout!r}"
    assert "1 file changed" in result.stdout, f"Got: {result.stdout!r}"


def test_pre_verify_sh_uses_supported_stat_command():
    """Regression guard: the prefetch derives the stat with git apply --stat and
    never passes the unsupported --stat flag to gh pr diff (Sourcery id 3896899424).
    """
    # Given the current pre-verify-pr.sh source
    with open(pre_verify_sh) as f:
        script = f.read()

    # Then no gh pr diff invocation uses --stat, and git apply --stat is present
    for line in script.splitlines():
        if line.lstrip().startswith("#"):
            continue  # skip comments (which may mention the removed flag)
        if "gh pr diff" in line:
            assert "--stat" not in line, f"unsupported gh flag reintroduced: {line!r}"
    assert "git apply --stat" in script, "expected git apply --stat stat mechanism"


# --- idempotency prefetch (pre-verify-pr.sh) ---

def test_pre_verify_sh_prefetches_related_issues():
    """Regression guard: pre-verify-pr.sh fetches related-issue metadata for the
    sandbox idempotency checks (TC-5982) — it lists related keys, fetches each
    issue including its comments, and passes --idempotency-dir to transform.
    """
    with open(pre_verify_sh) as f:
        script = f.read()

    # It enumerates the task's related keys via pre_verify_pr.py related-keys
    assert "related-keys" in script, "expected related-keys enumeration"
    # It fetches each related issue including the comment field (for Step 7c)
    non_comment = [
        line for line in script.splitlines()
        if 'get_issue "${key}"' in line and not line.lstrip().startswith("#")
    ]
    assert non_comment, "expected a per-key get_issue fetch"
    # The fields list feeding that fetch must include comment, description, labels
    assert "summary,labels,description,issuetype,comment" in script, \
        "related-issue fetch must request comment/description/labels"
    # And it wires the prefetched dir into transform
    assert "--idempotency-dir" in script, "transform must receive --idempotency-dir"


# --- PR-URL-derived Jira gating (pre-verify-pr.sh) ---

def test_pre_verify_sh_derives_and_gates_from_pr_url():
    """Regression guard (TC-6190): pre-verify-pr.sh takes the PR URL as its entry
    point, derives the Jira key by JQL on the Git Pull Request field, and maps a
    gate failure to the ADR-0072 skip signal — it never requires JIRA_ISSUE_ID.
    """
    # Given the current pre-verify-pr.sh source
    with open(pre_verify_sh) as f:
        script = f.read()

    non_comment = [
        line for line in script.splitlines() if not line.lstrip().startswith("#")
    ]
    body = "\n".join(non_comment)

    # The triggering PR URL is the required input (from fullsend harness-run)
    assert "FULLSEND_WORK_ITEM_URL" in body, "PR URL entry point must be required"
    # It never validates or requires a supplied JIRA_ISSUE_ID as an input
    assert "JIRA_ISSUE_ID:?" not in body, "JIRA_ISSUE_ID must not be a required input"
    # The key is derived by JQL on the custom field then gated in Python
    assert "build-pr-jql" in body, "must build the PR JQL"
    assert "search_jql" in body, "must search Jira by JQL"
    assert "resolve-gated-issue" in body, "must resolve + gate the issue"
    # A gate failure (exit 3) is mapped to the ADR-0072 skip signal
    assert "-eq 3" in body and "request_skip" in body, \
        "gate failure (exit 3) must trigger request_skip"


# --- paginated fetch aggregation (pre-verify-pr.sh) ---

def test_paginated_pages_aggregate_into_flat_array():
    """Multi-page fetches merge into one complete array, not truncated at page 1.

    Exercises the exact merge pre-verify-pr.sh runs on the `gh api --paginate
    --slurp` output — a per-page array-of-arrays piped through `jq 'add'` — and
    asserts every page's items survive in order with their object shape intact.
    """
    # Given the array-of-pages that `gh api --paginate --slurp` emits: three
    # pages, so page-2 and page-3 items only appear if pagination is honored.
    slurped_pages = [
        [{"id": 1}, {"id": 2}],
        [{"id": 3}, {"id": 4}],
        [{"id": 5}],
    ]

    # When merged with the same standalone `jq 'add'` the script pipes through
    result = subprocess.run(
        ["jq", "add"],
        input=json.dumps(slurped_pages), capture_output=True, text=True,
    )

    # Then the pages flatten into one array carrying items beyond the first page
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    merged = json.loads(result.stdout)
    assert merged == [{"id": 1}, {"id": 2}, {"id": 3}, {"id": 4}, {"id": 5}], \
        f"expected flat concatenation, got: {merged!r}"
    assert [o["id"] for o in merged] == [1, 2, 3, 4, 5]  # order preserved
    assert {"id": 5} in merged  # last page (beyond first) not truncated


def test_pre_verify_sh_paginates_review_comment_fetches():
    """Regression guard: all three gh api review/comment fetches request every
    page and merge with `jq 'add'` (Sourcery id 3896899429), keeping the stored
    value a flat array for pre_verify_pr.py.
    """
    # Given the current pre-verify-pr.sh source
    with open(pre_verify_sh) as f:
        script = f.read()

    # Then each of the three paginated endpoints is fetched with --paginate
    # --slurp and merged via jq add on a non-comment line.
    endpoints = [
        "/pulls/${PR_NUM}/reviews",
        "/pulls/${PR_NUM}/comments",
        "/issues/${PR_NUM}/comments",
    ]
    for endpoint in endpoints:
        matches = [
            line for line in script.splitlines()
            if endpoint in line and not line.lstrip().startswith("#")
        ]
        assert matches, f"no fetch line found for {endpoint}"
        for line in matches:
            if "gh api" not in line:
                continue
            assert "--paginate" in line, f"missing --paginate: {line!r}"
            assert "--slurp" in line, f"missing --slurp: {line!r}"
            assert "jq 'add'" in line, f"missing jq 'add' merge: {line!r}"


# --- PR-URL parsing regex (pre-verify-pr.sh) ---

def _github_pr_url_regex():
    """Extract the github.com PR-URL match regex from pre-verify-pr.sh.

    The tests below run the *actual* regex the script ships (not a re-typed
    copy), so an accidental loss of the end anchor is caught behaviorally.
    """
    with open(pre_verify_sh) as f:
        for line in f:
            if "=~" in line and "github" in line and "/pull/" in line:
                m = re.search(r"=~\s+(\S.*?)\s+\]\]", line)
                if m:
                    return m.group(1)
    raise AssertionError("github.com PR-URL regex not found in pre-verify-pr.sh")


def _match_pr_url(url):
    """Run pre-verify-pr.sh's exact `[[ =~ ]]` test against url.

    Returns (matched, repo, number) using the same BASH_REMATCH groups the
    script consumes downstream, so a truncating match surfaces as a wrong
    `number` rather than a silent pass.
    """
    regex = _github_pr_url_regex()
    snippet = (
        'r="$1"; u="$2"\n'
        'if [[ "$u" =~ $r ]]; then\n'
        '  printf "MATCH\\t%s\\t%s" "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"\n'
        'else\n'
        '  printf "NOMATCH"\n'
        'fi\n'
    )
    result = subprocess.run(
        ["bash", "-c", snippet, "bash", regex, url],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"bash error: {result.stderr}"
    parts = result.stdout.split("\t")
    if parts[0] == "MATCH":
        return True, parts[1], parts[2]
    return False, None, None


def test_pr_url_wellformed_accepted():
    """A canonical github.com PR URL parses to its owner/repo and PR number."""
    # Given a well-formed PR URL like a Jira inlineCard stores
    # When matched by the script's regex
    matched, repo, number = _match_pr_url("https://github.com/org/repo/pull/42")

    # Then it matches and captures the exact repo and number
    assert matched, "well-formed URL should match"
    assert repo == "org/repo", f"Got repo: {repo!r}"
    assert number == "42", f"Got number: {number!r}"


def test_pr_url_trailing_slash_accepted():
    """A well-formed PR URL with a trailing slash still parses correctly."""
    # Given a PR URL with a trailing slash
    # When matched by the script's regex
    matched, repo, number = _match_pr_url("https://github.com/org/repo/pull/42/")

    # Then it matches with the same repo and number (the slash is tolerated)
    assert matched, "trailing-slash URL should match"
    assert repo == "org/repo", f"Got repo: {repo!r}"
    assert number == "42", f"Got number: {number!r}"


def test_pr_url_nonnumeric_suffix_rejected():
    """A pull number with a trailing non-numeric suffix is rejected, not truncated.

    Regression for Sourcery id 3902059934: the un-anchored regex accepted
    `.../pull/42abc` and truncated the number to 42, so the pre-script fetched
    the wrong PR. The end-anchored regex must reject it outright.
    """
    # Given a malformed URL with a non-numeric suffix on the pull number
    # When matched by the script's regex
    matched, _repo, number = _match_pr_url("https://github.com/org/repo/pull/42abc")

    # Then it does not match (rather than truncating to 42)
    assert not matched, f"expected rejection, but matched with number={number!r}"


def test_pr_url_extra_path_segment_rejected():
    """An extra path segment after the pull number is rejected, not truncated.

    Regression for Sourcery id 3902059934: `.../pull/42/invalid` previously
    matched and truncated to PR 42. The end anchor must reject it.
    """
    # Given a malformed URL with an extra path segment after the number
    # When matched by the script's regex
    matched, _repo, number = _match_pr_url(
        "https://github.com/org/repo/pull/42/invalid")

    # Then it does not match (rather than truncating to 42)
    assert not matched, f"expected rejection, but matched with number={number!r}"


# --- COMMIT_SHA derivation (pre-verify-pr.sh) ---

def _commit_sha_command():
    """Extract the COMMIT_SHA assignment command from pre-verify-pr.sh.

    The behavioral test below runs the *actual* command the script ships (not a
    re-typed copy), so a regression back to the bounded commits connection is
    caught by execution, not just by source inspection.
    """
    with open(pre_verify_sh) as f:
        for line in f:
            if line.lstrip().startswith("COMMIT_SHA="):
                return line.strip()
    raise AssertionError("COMMIT_SHA assignment not found in pre-verify-pr.sh")


def test_commit_sha_derived_from_head_ref_oid():
    """The prefetched COMMIT_SHA is the PR head ref tip OID, not the last commit
    of gh's bounded commits connection.

    Runs the exact COMMIT_SHA command pre-verify-pr.sh ships against a gh stub
    whose headRefOid and commits[-1].oid disagree (simulating a large PR whose
    commits connection is truncated below the head). Regression for Sourcery id
    3902563589: the old `.commits[-1].oid` read returns the truncated oid.
    """
    # Given a gh stub where the head ref OID and the (truncated) commits
    # connection's last oid disagree
    head_oid = "a" * 40
    truncated_oid = "b" * 40
    with tempfile.TemporaryDirectory() as d:
        gh_stub = os.path.join(d, "gh")
        with open(gh_stub, "w") as f:
            f.write(
                "#!/usr/bin/env bash\n"
                "for arg in \"$@\"; do\n"
                f'  if [[ "$arg" == headRefOid ]]; then echo {head_oid}; exit 0; fi\n'
                f'  if [[ "$arg" == commits ]]; then echo {truncated_oid}; exit 0; fi\n'
                "done\n"
                "echo UNEXPECTED >&2; exit 1\n"
            )
        os.chmod(gh_stub, 0o755)

        # When running the exact COMMIT_SHA assignment the script ships, with the
        # stub gh ahead on PATH and PR_NUM/PR_REPO supplied
        command = _commit_sha_command()
        env = {**os.environ, "PATH": d + os.pathsep + os.environ["PATH"],
               "PR_NUM": "275", "PR_REPO": "o/r"}
        result = subprocess.run(
            ["bash", "-c", command + "\nprintf '%s' \"$COMMIT_SHA\""],
            capture_output=True, text=True, env=env,
        )

    # Then the emitted commit SHA is the head ref OID, not the truncated last commit
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    assert result.stdout == head_oid, f"Got: {result.stdout!r} (stderr: {result.stderr!r})"
    assert result.stdout != truncated_oid


def test_pre_verify_sh_derives_commit_sha_from_head_ref_oid():
    """Regression guard: COMMIT_SHA reads headRefOid and never the truncatable
    commits connection (.commits[-1].oid) (Sourcery id 3902563589).
    """
    # Given the current pre-verify-pr.sh source
    with open(pre_verify_sh) as f:
        script = f.read()

    # Then every COMMIT_SHA assignment reads headRefOid and none falls back to
    # gh's bounded commits connection
    commit_sha_lines = [
        line for line in script.splitlines()
        if line.lstrip().startswith("COMMIT_SHA=")
    ]
    assert commit_sha_lines, "no COMMIT_SHA assignment found in pre-verify-pr.sh"
    for line in commit_sha_lines:
        assert "headRefOid" in line, f"COMMIT_SHA not derived from headRefOid: {line!r}"
        assert ".commits[-1]" not in line, \
            f"COMMIT_SHA reintroduced the bounded commits read: {line!r}"


# --- build_pr_jql (PR-URL → JQL) ---

PR_URL = "https://github.com/org/repo/pull/42"


def test_build_pr_jql_targets_custom_field_and_url():
    """The JQL queries the Git Pull Request custom field by id for the PR URL."""
    # Given a PR URL, when the JQL is built
    jql = pre_verify_pr.build_pr_jql(PR_URL)

    # Then it matches the custom field (by id) against the URL with ~ recall
    assert jql == 'cf[10875] ~ "https://github.com/org/repo/pull/42"', f"Got: {jql}"


def test_build_pr_jql_escapes_quotes():
    """A URL containing a double quote cannot break out of the JQL string literal."""
    # Given a hostile URL embedding a quote
    jql = pre_verify_pr.build_pr_jql('https://x/"; DROP')

    # Then the quote is backslash-escaped inside the quoted literal
    assert jql == 'cf[10875] ~ "https://x/\\"; DROP"', f"Got: {jql}"


# --- resolve_gated_issue (JQL result → gated key / skip reason) ---

def _search_issue(key, pr_url, status="Review", labels=("ai-generated-jira",)):
    """A single Jira search-result issue with the given gate-relevant fields."""
    return {
        "key": key,
        "fields": {
            "status": {"name": status},
            "labels": list(labels),
            "customfield_10875": pr_url,
        },
    }


def test_resolve_gated_issue_all_gates_pass():
    """One issue matching the PR URL, in Review, with the label → resolves the key."""
    # Given a search result with exactly one qualifying issue
    result = {"issues": [_search_issue("TC-6190", PR_URL)]}

    # When resolving against the PR URL
    key, reason = pre_verify_pr.resolve_gated_issue(result, PR_URL)

    # Then the key resolves and there is no skip reason
    assert key == "TC-6190", f"Got: {key}"
    assert reason is None, f"Got: {reason}"


def test_resolve_gated_issue_no_pr_match_skips():
    """No issue's custom field exactly equals the PR URL → skip (PR-match gate)."""
    # Given a search that recalled a different PR (broad ~ over-match)
    result = {"issues": [_search_issue("TC-1", "https://github.com/org/repo/pull/99")]}

    # When resolving against the target PR URL
    key, reason = pre_verify_pr.resolve_gated_issue(result, PR_URL)

    # Then no key resolves and the reason names the missing link
    assert key is None, f"Got: {key}"
    assert "no Jira issue links" in reason, f"Got: {reason}"


def test_resolve_gated_issue_multiple_matches_skips():
    """More than one issue links the same PR URL → skip (ambiguous, no guess)."""
    # Given two issues both exactly linking the PR URL
    result = {"issues": [_search_issue("TC-1", PR_URL), _search_issue("TC-2", PR_URL)]}

    # When resolving
    key, reason = pre_verify_pr.resolve_gated_issue(result, PR_URL)

    # Then it refuses to guess and names both keys
    assert key is None, f"Got: {key}"
    assert "multiple Jira issues" in reason, f"Got: {reason}"
    assert "TC-1" in reason and "TC-2" in reason, f"Got: {reason}"


def test_resolve_gated_issue_wrong_status_skips():
    """The matched issue is not in Review → skip (status gate)."""
    # Given the sole match in the wrong status
    result = {"issues": [_search_issue("TC-6190", PR_URL, status="In Progress")]}

    # When resolving
    key, reason = pre_verify_pr.resolve_gated_issue(result, PR_URL)

    # Then it skips and the reason names the status gate
    assert key is None, f"Got: {key}"
    assert "In Progress" in reason and "Review" in reason, f"Got: {reason}"


def test_resolve_gated_issue_missing_label_skips():
    """The matched issue lacks the ai-generated-jira label → skip (label gate)."""
    # Given the sole match in Review but without the gating label
    result = {"issues": [_search_issue("TC-6190", PR_URL, labels=("other",))]}

    # When resolving
    key, reason = pre_verify_pr.resolve_gated_issue(result, PR_URL)

    # Then it skips and the reason names the missing label
    assert key is None, f"Got: {key}"
    assert "ai-generated-jira" in reason, f"Got: {reason}"


def test_resolve_gated_issue_matches_adf_custom_field():
    """The PR-URL match works when the custom field is an ADF smart link, not a
    plain string — extract_pr_url normalizes both before the equality check."""
    # Given an issue whose Git Pull Request field is an ADF inlineCard
    issue = {
        "key": "TC-6190",
        "fields": {
            "status": {"name": "Review"},
            "labels": ["ai-generated-jira"],
            "customfield_10875": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [
                    {"type": "inlineCard", "attrs": {"url": PR_URL}}
                ]}],
            },
        },
    }

    # When resolving against the plain PR URL
    key, reason = pre_verify_pr.resolve_gated_issue({"issues": [issue]}, PR_URL)

    # Then the ADF-stored link still matches and the key resolves
    assert key == "TC-6190", f"Got: {key} (reason: {reason})"
    assert reason is None


def test_resolve_gated_issue_finds_exact_match_beyond_first_page():
    """TC-6233: a >50-result broad ~ recall where the exact PR match is not on the
    first page still resolves — given the full page-aggregated result that
    jira-client's `search_jql --all` produces (no false ADR-0072 skip).
    """
    # Given 60 recalled issues (page 1 = 50, page 2 = 10, as search_jql_all would
    # aggregate) where only the one at index 55 (beyond the first page) exactly
    # links the target PR; the rest are broad ~ over-matches on other PRs.
    # A distinct repo path so no generated recall URL can collide with PR_URL.
    other = "https://github.com/org/other-repo/pull/{}"
    issues = [_search_issue(f"TC-{i}", other.format(i)) for i in range(60)]
    issues[55] = _search_issue("TC-6190", PR_URL)
    result = {"issues": issues, "isLast": True}

    # When resolving against the target PR URL
    key, reason = pre_verify_pr.resolve_gated_issue(result, PR_URL)

    # Then the beyond-first-page issue resolves with no skip
    assert key == "TC-6190", f"Got: {key} (reason: {reason})"
    assert reason is None


def test_pre_verify_sh_paginates_jql_search_with_all():
    """Regression guard (TC-6233): pre-verify-pr.sh runs the gating JQL search
    with --all so a match beyond the first 50 recall results is never dropped.
    """
    # Given the current pre-verify-pr.sh source
    with open(pre_verify_sh) as f:
        script = f.read()

    # Then the search_jql invocation passes --all on a non-comment line
    search_lines = [
        line for line in script.splitlines()
        if "search_jql" in line and not line.lstrip().startswith("#")
    ]
    assert search_lines, "no search_jql invocation found"
    # The flag may sit on a continuation line of the same command; assert it is
    # present in the search_jql command block (the --fields line carries it).
    assert any("--all" in line for line in script.splitlines()
               if "--fields" in line and not line.lstrip().startswith("#")), \
        "gating JQL search must use --all to paginate"


# --- CLI: build-pr-jql / resolve-gated-issue exit-code contract ---

def _run_cli(args, stdin=None):
    return subprocess.run(
        [sys.executable, os.path.join(script_dir, "pre_verify_pr.py"), *args],
        input=stdin, capture_output=True, text=True,
    )


def test_cli_build_pr_jql():
    """build-pr-jql takes the URL as an argument and reads no stdin."""
    # When invoked with only the PR URL
    result = _run_cli(["build-pr-jql", PR_URL])

    # Then it prints the JQL and exits 0
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    assert result.stdout.strip() == 'cf[10875] ~ "%s"' % PR_URL


def test_cli_resolve_gated_issue_success_exit_0():
    """On a passing gate the CLI prints the key and exits 0."""
    # Given a qualifying search result on stdin
    payload = json.dumps({"issues": [_search_issue("TC-6190", PR_URL)]})

    # When resolving via the CLI
    result = _run_cli(["resolve-gated-issue", PR_URL], stdin=payload)

    # Then it exits 0 with the resolved key
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    assert result.stdout.strip() == "TC-6190"


def test_cli_resolve_gated_issue_gate_fail_exit_3():
    """On a failing gate the CLI exits 3 (the shell's ADR-0072 skip signal)."""
    # Given a search result whose sole match is in the wrong status
    payload = json.dumps(
        {"issues": [_search_issue("TC-6190", PR_URL, status="Closed")]})

    # When resolving via the CLI
    result = _run_cli(["resolve-gated-issue", PR_URL], stdin=payload)

    # Then it exits 3 and prints the skip reason
    assert result.returncode == 3, f"Exit {result.returncode}: {result.stdout}"
    assert "Closed" in result.stdout and "Review" in result.stdout


# --- revalidate_gate (TOCTOU re-check on the full issue before write) ---

def test_revalidate_gate_passes_when_full_issue_still_qualifies():
    """The full issue still links the PR, in Review, with the label → key, no skip."""
    # Given the full issue fetched after resolution still satisfies the gate
    issue = _search_issue("TC-6190", PR_URL)

    # When re-validating immediately before writing the input
    key, reason = pre_verify_pr.revalidate_gate(issue, PR_URL)

    # Then it resolves the key with no skip reason
    assert key == "TC-6190", f"Got: {key}"
    assert reason is None, f"Got: {reason}"


def test_revalidate_gate_skips_when_status_changed_after_search():
    """Issue left Review between the search gate and the full fetch → skip."""
    # Given the full issue is no longer in Review (the TOCTOU window)
    issue = _search_issue("TC-6190", PR_URL, status="Closed")

    # When re-validating the full issue
    key, reason = pre_verify_pr.revalidate_gate(issue, PR_URL)

    # Then no key resolves and the skip names the status change
    assert key is None, f"Got: {key}"
    assert "Closed" in reason and "Review" in reason, f"Got: {reason}"


def test_revalidate_gate_skips_when_label_removed_after_search():
    """Issue lost the ai-generated-jira label after the search → skip."""
    # Given the full issue no longer carries the gate label
    issue = _search_issue("TC-6190", PR_URL, labels=())

    # When re-validating the full issue
    key, reason = pre_verify_pr.revalidate_gate(issue, PR_URL)

    # Then no key resolves and the skip names the missing label
    assert key is None, f"Got: {key}"
    assert "ai-generated-jira" in reason, f"Got: {reason}"


def test_revalidate_gate_skips_when_pr_field_changed_after_search():
    """The Git Pull Request field was re-pointed after the search → skip."""
    # Given the full issue now links a different PR
    issue = _search_issue("TC-6190", "https://github.com/org/repo/pull/99")

    # When re-validating against the originally-resolved PR URL
    key, reason = pre_verify_pr.revalidate_gate(issue, PR_URL)

    # Then no key resolves and the skip names the broken PR link
    assert key is None, f"Got: {key}"
    assert "no Jira issue links" in reason, f"Got: {reason}"


def test_cli_revalidate_gate_success_exit_0():
    """On a still-qualifying full issue the CLI prints the key and exits 0."""
    # Given a qualifying full issue on stdin
    payload = json.dumps(_search_issue("TC-6190", PR_URL))

    # When re-validating via the CLI
    result = _run_cli(["revalidate-gate", PR_URL], stdin=payload)

    # Then it exits 0 with the resolved key
    assert result.returncode == 0, f"Exit {result.returncode}: {result.stderr}"
    assert result.stdout.strip() == "TC-6190"


def test_cli_revalidate_gate_gate_fail_exit_3():
    """A status change detected at re-validation exits 3 (ADR-0072 skip signal)."""
    # Given a full issue that has left Review since the search
    payload = json.dumps(_search_issue("TC-6190", PR_URL, status="Closed"))

    # When re-validating via the CLI
    result = _run_cli(["revalidate-gate", PR_URL], stdin=payload)

    # Then it exits 3 and prints the skip reason
    assert result.returncode == 3, f"Exit {result.returncode}: {result.stdout}"
    assert "Closed" in result.stdout and "Review" in result.stdout


def test_pre_verify_sh_revalidates_gate_before_writing_input():
    """The shell re-gates the full issue via revalidate-gate before the transform."""
    # Given the pre-verify-pr.sh source
    with open(pre_verify_sh) as f:
        script = f.read()

    # Then it invokes revalidate-gate, maps a gate failure to request_skip, and
    # does so BEFORE writing verify-pr-input.json (the transform step).
    assert "revalidate-gate" in script, "re-validation step missing"
    reval_idx = script.index("revalidate-gate")
    transform_idx = script.index("pre_verify_pr.py\" transform")
    assert reval_idx < transform_idx, \
        "revalidate-gate must run before the transform that writes the input"
    # The re-validation feeds the FULL issue (ISSUE_JSON), not the search result.
    reval_line = next(
        ln for ln in script.splitlines() if "revalidate-gate" in ln)
    assert "ISSUE_JSON" in reval_line, \
        f"revalidate-gate must re-check the full issue: {reval_line!r}"
    # A gate failure at re-validation emits the ADR-0072 skip, like Step 3.
    assert "request_skip \"${REVAL_OUT}\"" in script, \
        "a failed re-validation must map to request_skip"


# --- runner ---

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = []
    for t in tests:
        try:
            t()
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            print(f"  ✗ {t.__name__}: {e}")
            failed.append(t.__name__)
    print(f"{'=' * 60}")
    if failed:
        print(f"FAILED: {len(failed)}/{len(tests)} test(s) failed")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(tests)} tests passed")
        sys.exit(0)
