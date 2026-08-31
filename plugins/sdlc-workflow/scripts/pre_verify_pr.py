#!/usr/bin/env python3
"""Pre-verify-pr data extraction functions.

Extracts PR URL from Jira custom fields, assembles the GitHub tier-1 read
bundle prefetched on the runner, and transforms Jira issue JSON into the
tracker-agnostic input schema used by the sandbox.

CLI usage (called by pre-verify-pr.sh):
    echo "$ISSUE_JSON" | python3 pre_verify_pr.py extract-pr-url
    echo "$ISSUE_JSON" | python3 pre_verify_pr.py transform TASK_ID PR_URL \\
        [--github-dir DIR --pr-repo REPO --pr-number N \\
         --head-ref REF --commit-sha SHA]

When the --github-* options are supplied, `transform` reads the raw GitHub
reads from DIR (pr.diff, pr.stat, reviews.json, review-comments.json,
issue-comments.json, commits.json) and embeds them under a `github` key.
"""

import argparse
import json
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


def transform_to_input(issue, task_id, pr_url, github=None):
    """Transform Jira issue JSON to tracker-agnostic input schema."""
    fields = issue.get("fields", {})
    result = {
        "task_id": task_id,
        "task": {
            "summary": fields.get("summary", ""),
            "description": fields.get("description", {}),
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


def main(argv):
    parser = argparse.ArgumentParser(prog="pre_verify_pr.py")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("extract-pr-url")

    t = sub.add_parser("transform")
    t.add_argument("task_id")
    t.add_argument("pr_url")
    t.add_argument("--github-dir")
    t.add_argument("--pr-repo")
    t.add_argument("--pr-number", type=int)
    t.add_argument("--head-ref")
    t.add_argument("--commit-sha")

    args = parser.parse_args(argv)
    issue = json.load(sys.stdin)

    if args.command == "extract-pr-url":
        print(extract_pr_url(issue))
    elif args.command == "transform":
        github = _github_from_dir(args) if args.github_dir else None
        result = transform_to_input(issue, args.task_id, args.pr_url, github)
        json.dump(result, sys.stdout, indent=2)


if __name__ == "__main__":
    main(sys.argv[1:])
