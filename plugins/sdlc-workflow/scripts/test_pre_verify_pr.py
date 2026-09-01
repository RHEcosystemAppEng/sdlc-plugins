#!/usr/bin/env python3
"""Tests for pre_verify_pr.py — PR URL extraction, GitHub bundle, transform."""

import json
import os
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


# --- build_github_bundle ---

def test_build_github_bundle():
    bundle = pre_verify_pr.build_github_bundle(
        pr_repo="org/repo", pr_number="42", head_ref="feat/x",
        commit_sha="abc1234", diff="diff --git a b", stat=" 1 file changed",
        reviews=[{"id": 1}], review_comments=[{"id": 2}],
        issue_comments=[{"id": 3}], commits=[{"oid": "abc1234"}],
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
    assert gh["commits"] == [{"oid": "abc1234def"}]


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
