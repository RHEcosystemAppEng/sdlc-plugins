#!/usr/bin/env python3
"""Pre-verify-pr data extraction functions.

Extracts PR URL from Jira custom fields, assembles the GitHub tier-1 read
bundle prefetched on the runner, and transforms Jira issue JSON into the
tracker-agnostic input schema used by the sandbox.

CLI usage (called by pre-verify-pr.sh):
    echo "$ISSUE_JSON" | python3 pre_verify_pr.py extract-pr-url
    echo "$ISSUE_JSON" | python3 pre_verify_pr.py related-keys
    echo "$ISSUE_JSON" | python3 pre_verify_pr.py transform TASK_ID PR_URL \\
        [--github-dir DIR --pr-repo REPO --pr-number N \\
         --head-ref REF --commit-sha SHA --idempotency-dir DIR]

When the --github-* options are supplied, `transform` reads the raw GitHub
reads from DIR (pr.diff, pr.stat, reviews.json, review-comments.json,
issue-comments.json, commits.json) and embeds them under a `github` key.

`related-keys` prints the task's sub-task and linked-issue keys (one per line)
so the shell can prefetch each on the runner. When --idempotency-dir is given,
`transform` reads those prefetched issue JSONs and embeds their summary/labels/
description/comments under an `idempotency` key, giving the sandbox a tokenless
data source for the Steps 6d/6f/7c idempotency checks.
"""

import argparse
import glob
import json
import os
import re
import sys


def commit_references_task(commit, task_id):
    """True if the commit references ``task_id`` in its headline OR body.

    The Jira task ID conventionally sits in a trailer or body line (e.g.
    ``Implements TC-5812``), not only the subject, so BOTH ``messageHeadline``
    and ``messageBody`` are scanned. Word boundaries keep ``TC-5812`` from
    matching ``TC-58120`` or another ID like ``TC-5982``. This computes the
    Commit Traceability fact deterministically on the runner so the tokenless
    sandbox agent never has to re-derive it from ``git log`` (which, with
    ``--oneline``/``%s``, would see subjects only and miss the trailer).
    """
    if not task_id:
        return False
    text = "{}\n{}".format(
        commit.get("messageHeadline", "") or "",
        commit.get("messageBody", "") or "",
    )
    return re.search(r"\b{}\b".format(re.escape(task_id)), text) is not None


_URL_RE = re.compile(r"https?://\S+")


def _first_url_in_adf(node):
    """Return the first URL found in an ADF node, depth-first in document order.

    Covers every shape Jira uses to populate a URL/textarea custom field:
    an ``inlineCard`` (smart link), a ``text`` node carrying a ``link`` mark,
    or plain text that merely contains a bare URL. Returns "" when none is found.
    """
    if isinstance(node, dict):
        if node.get("type") == "inlineCard":
            url = node.get("attrs", {}).get("url", "")
            if url:
                return url
        if node.get("type") == "text":
            for mark in node.get("marks", []):
                if mark.get("type") == "link":
                    href = mark.get("attrs", {}).get("href", "")
                    if href:
                        return href
            match = _URL_RE.search(node.get("text", "") or "")
            if match:
                return match.group(0).rstrip(".,);]")
        for child in node.get("content", []):
            url = _first_url_in_adf(child)
            if url:
                return url
    elif isinstance(node, list):
        for child in node:
            url = _first_url_in_adf(child)
            if url:
                return url
    return ""


def extract_pr_url(issue):
    """Extract the PR URL from the Jira Git Pull Request custom field.

    The field is format-agnostic: it may be a plain string, an ADF
    ``inlineCard`` smart link, an ADF ``text`` node with a ``link`` mark, or
    plain ADF text holding a bare URL. All are handled so a linked PR is never
    missed because of how the field happened to be populated. Returns "" when
    the field is absent or contains no URL.
    """
    field = issue.get("fields", {}).get("customfield_10875")
    if not field:
        return ""
    if isinstance(field, str):
        match = _URL_RE.search(field)
        return match.group(0).rstrip(".,);]") if match else field.strip()
    if isinstance(field, dict):
        return _first_url_in_adf(field)
    return ""


# Gates the verification: the JQL-resolved issue must be in this status AND
# carry this label, mirroring the interactive verify-pr entry conditions. Kept
# as module constants so the skip reasons and the tests reference one source.
GATE_STATUS = "Review"
GATE_LABEL = "ai-generated-jira"


def build_pr_jql(pr_url):
    """JQL recalling issues whose Git Pull Request field references ``pr_url``.

    Uses the ``~`` (contains) operator on the custom field by id (``cf[10875]``):
    an exact ``=`` match is unreliable for Jira URL/text fields, which tokenize
    their stored value. Recall is intentionally broad — ``resolve_gated_issue``
    re-confirms the *exact* PR URL in Python, so a fuzzy ``~`` hit on a different
    PR can never be accepted. The value is wrapped in a quoted JQL string literal
    with backslashes and quotes escaped so a crafted URL cannot break out of it.
    """
    escaped = pr_url.replace("\\", "\\\\").replace('"', '\\"')
    return 'cf[10875] ~ "{}"'.format(escaped)


def resolve_gated_issue(search_result, pr_url):
    """Resolve the single Jira issue that gates verification of ``pr_url``.

    Returns ``(key, None)`` when exactly one issue's Git Pull Request field
    *exactly* equals ``pr_url`` AND that issue is in status ``Review`` AND
    carries the ``ai-generated-jira`` label. Returns ``(None, reason)`` when any
    gate fails, with a human-readable ``reason`` for the ADR-0072 skip signal:

    - no issue references ``pr_url`` (the broad ``~`` recall matched nothing exact)
    - more than one issue references ``pr_url`` (ambiguous — refuse to guess)
    - the matched issue is not in status ``Review``
    - the matched issue lacks the ``ai-generated-jira`` label

    The exact-URL re-match (``extract_pr_url`` per candidate) is the trust
    anchor: the JQL ``~`` operator over-matches, so acceptance is decided here,
    never by JQL alone.
    """
    issues = search_result.get("issues", []) if isinstance(search_result, dict) else []
    matches = [issue for issue in issues if extract_pr_url(issue) == pr_url]
    if not matches:
        return None, (
            "no Jira issue links PR {} in its Git Pull Request field".format(pr_url)
        )
    if len(matches) > 1:
        keys = ", ".join(sorted(issue.get("key", "?") for issue in matches))
        return None, (
            "multiple Jira issues link PR {} ({}) — refusing to guess".format(
                pr_url, keys)
        )
    issue = matches[0]
    key = issue.get("key", "")
    fields = issue.get("fields", {})
    status = (fields.get("status") or {}).get("name", "")
    if status != GATE_STATUS:
        return None, "{} is in status '{}', not '{}'".format(
            key, status, GATE_STATUS)
    labels = fields.get("labels", []) or []
    if GATE_LABEL not in labels:
        return None, "{} is missing the '{}' label".format(key, GATE_LABEL)
    return key, None


def build_github_bundle(pr_repo, pr_number, head_ref, commit_sha,
                        diff, stat, reviews, review_comments,
                        issue_comments, commits):
    """Assemble the GitHub tier-1 read bundle embedded in the input.

    diff/stat are raw text; the four *_comments/reviews/commits arguments
    are already-parsed JSON (lists). Keys mirror the reads the verify-pr
    skill performs so the sandbox needs no api.github.com egress.
    """
    return {
        "pr_repo": pr_repo,
        "pr_number": int(pr_number),
        "headRefName": head_ref,
        "commit_sha": commit_sha,
        "diff": diff,
        "stat": stat,
        "reviews": reviews,
        "review_comments": review_comments,
        "issue_comments": issue_comments,
        "commits": commits,
    }


def related_keys(issue):
    """Keys of the task's sub-tasks and linked issues (idempotency targets).

    Steps 6d/6f/7c dedupe against the parent task's existing sub-tasks and its
    linked (e.g., root-cause) issues. The pre_script fetches each of these keys
    on the trusted runner so the sandbox can run those idempotency checks
    without a Jira token. Returns a sorted, de-duplicated list.
    """
    fields = issue.get("fields", {})
    keys = set()
    for sub in fields.get("subtasks") or []:
        key = sub.get("key")
        if key:
            keys.add(key)
    for link in fields.get("issuelinks") or []:
        related = link.get("inwardIssue") or link.get("outwardIssue") or {}
        key = related.get("key")
        if key:
            keys.add(key)
    return sorted(keys)


def build_idempotency_bundle(related_issue_jsons):
    """Bundle related-issue metadata for the sandbox idempotency checks.

    Each item is a full issue JSON the runner fetched with fields summary,
    labels, description, issuetype, and comment. The sandbox reads this instead
    of calling Jira to dedupe sub-tasks (Steps 6d/6f) and root-cause tasks
    (Step 7c). Descriptions and comment bodies are kept in the tracker's native
    format (ADF for Jira) — the sandbox agent inspects them directly.
    """
    related = []
    for ri in related_issue_jsons:
        fields = ri.get("fields", {})
        comments = [
            c.get("body") or {}
            for c in (fields.get("comment") or {}).get("comments", [])
        ]
        related.append({
            "key": ri.get("key", ""),
            "summary": fields.get("summary", ""),
            "labels": fields.get("labels", []),
            # Coerce an explicit null description to {} so the value stays an
            # object per verify-pr-input.schema.json (see transform_to_input).
            "description": fields.get("description") or {},
            "issuetype": (fields.get("issuetype") or {}).get("name", ""),
            "comments": comments,
        })
    return {"related_issues": related}


def transform_to_input(issue, task_id, pr_url, github=None, idempotency=None):
    """Transform Jira issue JSON to tracker-agnostic input schema.

    The ``idempotency`` bundle is always emitted (defaulting to an empty
    ``related_issues`` list when none is supplied) so the tokenless sandbox
    always has a data source for the Steps 6d/6f/7c dedup checks. This matches
    verify-pr-input.schema.json, which requires ``idempotency.related_issues``:
    a schema-valid prefetch can never omit the bundle and silently skip dedup.
    """
    fields = issue.get("fields", {})
    result = {
        "task_id": task_id,
        "task": {
            "summary": fields.get("summary", ""),
            # Jira may return an explicit null description; `.get(key, {})` only
            # defaults on an ABSENT key, so `or {}` also coerces null → {} to
            # keep task.description an object per verify-pr-input.schema.json.
            "description": fields.get("description") or {},
            "status": (fields.get("status") or {}).get("name", ""),
            "labels": fields.get("labels", []),
            "issue_links": [
                {
                    "type": (link.get("type") or {}).get("name", ""),
                    "direction": "inward" if "inwardIssue" in link else "outward",
                    "key": (
                        link.get("inwardIssue") or link.get("outwardIssue") or {}
                    ).get("key", ""),
                }
                for link in fields.get("issuelinks", [])
            ],
            "custom_fields": {
                k: v
                for k, v in fields.items()
                if k.startswith("customfield_")
            },
        },
        "pr_url": pr_url,
        "source": {
            "tracker": "jira",
            "raw": issue,
        },
    }
    if github is not None:
        # Annotate each commit with the deterministic Commit Traceability fact
        # (Check 3). commits.items is unconstrained in the input schema, so the
        # extra key is schema-valid; the sandbox agent reads references_task_id
        # instead of running its own subjects-only git log.
        commits = github.get("commits")
        if isinstance(commits, list):
            for commit in commits:
                if isinstance(commit, dict):
                    commit["references_task_id"] = commit_references_task(
                        commit, task_id)
        result["github"] = github
    result["idempotency"] = (
        idempotency if idempotency is not None else {"related_issues": []}
    )
    return result


def _read_text(path):
    with open(path) as f:
        return f.read()


def _read_json(path):
    with open(path) as f:
        return json.load(f)


def _github_from_dir(args):
    """Assemble the github bundle from raw read files written by the shell."""
    d = args.github_dir.rstrip("/")
    return build_github_bundle(
        pr_repo=args.pr_repo,
        pr_number=args.pr_number,
        head_ref=args.head_ref,
        commit_sha=args.commit_sha,
        diff=_read_text(f"{d}/pr.diff"),
        stat=_read_text(f"{d}/pr.stat"),
        reviews=_read_json(f"{d}/reviews.json"),
        review_comments=_read_json(f"{d}/review-comments.json"),
        issue_comments=_read_json(f"{d}/issue-comments.json"),
        commits=_read_json(f"{d}/commits.json"),
    )


def _idempotency_from_dir(path):
    """Read every related-issue JSON the shell wrote and build the bundle.

    Globs ``<path>/*.json`` (one file per related key, written by
    pre-verify-pr.sh). An empty directory yields an empty related_issues list.
    """
    files = sorted(glob.glob(os.path.join(path, "*.json")))
    return build_idempotency_bundle([_read_json(f) for f in files])


def main(argv):
    parser = argparse.ArgumentParser(prog="pre_verify_pr.py")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("extract-pr-url")
    sub.add_parser("related-keys")

    jql = sub.add_parser("build-pr-jql")
    jql.add_argument("pr_url")

    gate = sub.add_parser("resolve-gated-issue")
    gate.add_argument("pr_url")

    t = sub.add_parser("transform")
    t.add_argument("task_id")
    t.add_argument("pr_url")
    t.add_argument("--github-dir")
    t.add_argument("--pr-repo")
    t.add_argument("--pr-number", type=int)
    t.add_argument("--head-ref")
    t.add_argument("--commit-sha")
    t.add_argument("--idempotency-dir")

    args = parser.parse_args(argv)

    # build-pr-jql takes only an argument — it reads no stdin, so resolve it
    # before the stdin-consuming commands.
    if args.command == "build-pr-jql":
        print(build_pr_jql(args.pr_url))
        return

    if args.command == "resolve-gated-issue":
        # Exit 3 is the gate-failure contract the shell maps to an ADR-0072
        # skip; exit 1 (argparse/JSON errors) stays a hard failure.
        search_result = json.load(sys.stdin)
        key, reason = resolve_gated_issue(search_result, args.pr_url)
        if reason is not None:
            # Diagnostic to stderr (runner log only — stdout stays the clean
            # skip reason). Reveals what the JQL search actually returned so a
            # gate failure can be told apart from an empty/visibility-limited
            # search. Only non-secret shape is logged: issue count, keys, and
            # the PR URL extracted from each candidate's Git Pull Request field.
            issues = (
                search_result.get("issues", [])
                if isinstance(search_result, dict) else []
            )
            summary = ", ".join(
                "{}=>{!r}".format(i.get("key", "?"), extract_pr_url(i))
                for i in issues
            ) or "(none)"
            print(
                "resolve-gated-issue: search returned {} issue(s): {}".format(
                    len(issues), summary),
                file=sys.stderr,
            )
            print(reason)
            sys.exit(3)
        print(key)
        return

    issue = json.load(sys.stdin)

    if args.command == "extract-pr-url":
        print(extract_pr_url(issue))
    elif args.command == "related-keys":
        for key in related_keys(issue):
            print(key)
    elif args.command == "transform":
        github = _github_from_dir(args) if args.github_dir else None
        idempotency = (
            _idempotency_from_dir(args.idempotency_dir)
            if args.idempotency_dir else None
        )
        result = transform_to_input(
            issue, args.task_id, args.pr_url, github, idempotency)
        json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
