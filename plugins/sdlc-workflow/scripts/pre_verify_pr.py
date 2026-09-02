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
import sys


def extract_pr_url(issue):
    """Extract PR URL from Jira custom field (ADF or string).

    Returns empty string if the field is missing or has no URL.
    """
    field = issue.get("fields", {}).get("customfield_10875")
    if not field:
        return ""
    if isinstance(field, str):
        return field
    if isinstance(field, dict):
        for block in field.get("content", []):
            for inline in block.get("content", []):
                if inline.get("type") == "inlineCard":
                    return inline.get("attrs", {}).get("url", "")
    return ""


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
    """Transform Jira issue JSON to tracker-agnostic input schema."""
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
        result["github"] = github
    if idempotency is not None:
        result["idempotency"] = idempotency
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
