#!/usr/bin/env python3
"""Pre-verify-pr data extraction functions.

Extracts PR URL from Jira custom fields and transforms Jira issue
JSON into the tracker-agnostic input schema used by the sandbox.

CLI usage (called by pre-verify-pr.sh):
    echo "$ISSUE_JSON" | python3 pre_verify_pr.py extract-pr-url
    echo "$ISSUE_JSON" | python3 pre_verify_pr.py transform TASK_ID PR_URL
"""

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


def transform_to_input(issue, task_id, pr_url):
    """Transform Jira issue JSON to tracker-agnostic input schema."""
    fields = issue.get("fields", {})
    return {
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


def main(args):
    if len(args) < 1:
        print("Usage: pre_verify_pr.py <extract-pr-url|transform> [args...]", file=sys.stderr)
        sys.exit(1)

    issue = json.load(sys.stdin)
    command = args[0]

    if command == "extract-pr-url":
        print(extract_pr_url(issue))
    elif command == "transform":
        if len(args) < 3:
            print("Usage: pre_verify_pr.py transform TASK_ID PR_URL", file=sys.stderr)
            sys.exit(1)
        result = transform_to_input(issue, args[1], args[2])
        json.dump(result, sys.stdout, indent=2)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
