#!/usr/bin/env python3
"""Execute verify-pr structured output actions.

Reads agent-result.json, processes actions sequentially, resolves
{{ref.key}} and {{ref.url}} placeholders as entities are created.

Uses jira-client.py for Jira operations and gh CLI for GitHub operations.
Runs on the fullsend runner (trusted side), not inside the sandbox.

Not idempotent: if an action fails mid-execution, previously completed
actions (e.g., created Jira sub-tasks) are not rolled back. Manual
cleanup may be needed after partial failures.

Usage:
    execute-actions.py <result-json>

Required env vars:
    JIRA_SERVER_URL, JIRA_EMAIL, JIRA_API_TOKEN — Jira credentials
    GH_TOKEN — GitHub token
    JIRA_PROJECT_KEY — Jira project key (for root-cause task creation)
"""

import json
import os
import re
import subprocess
import sys
from typing import Any


REF_PATTERN = re.compile(r"\{\{([a-z0-9-]+)\.(key|url)\}\}")
JIRA_CLIENT_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jira-client.py")


def resolve_refs(text: str, registry: dict[str, dict[str, str]]) -> str:
    """Replace {{ref.key}} and {{ref.url}} placeholders with resolved values."""
    def replacer(match):
        ref_name, field = match.group(1), match.group(2)
        if ref_name not in registry:
            raise KeyError(f"Unknown ref: {ref_name}")
        return registry[ref_name][field]
    return REF_PATTERN.sub(replacer, text)


def resolve_refs_in_obj(obj: Any, registry: dict[str, dict[str, str]]) -> Any:
    """Recursively resolve refs in a JSON-like object (dicts, lists, strings)."""
    if isinstance(obj, str):
        return resolve_refs(obj, registry)
    if isinstance(obj, list):
        return [resolve_refs_in_obj(item, registry) for item in obj]
    if isinstance(obj, dict):
        return {k: resolve_refs_in_obj(v, registry) for k, v in obj.items()}
    return obj


def jira_client(*args: str) -> dict:
    """Call jira-client.py and return parsed JSON output."""
    cmd = ["python3", JIRA_CLIENT_SCRIPT]
    cmd.extend(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"jira-client.py {args[0]} failed:", file=sys.stderr)
        if result.stdout.strip():
            print(result.stdout, file=sys.stderr)
        if result.stderr.strip():
            print(result.stderr, file=sys.stderr)
        sys.exit(1)
    if result.stdout.strip():
        return json.loads(result.stdout)
    return {}


def gh_api(*args: str) -> str:
    """Call gh api and return raw output."""
    result = subprocess.run(
        ["gh", "api", *args],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"gh api failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def build_issue_url(key: str) -> str:
    """Build Jira issue browse URL from key."""
    server = os.environ.get("JIRA_SERVER_URL", "").rstrip("/")
    if not server:
        print("JIRA_SERVER_URL is required for issue URL construction", file=sys.stderr)
        sys.exit(1)
    return f"{server}/browse/{key}"


def execute_create_subtask(action: dict, registry: dict) -> None:
    ref = action["ref"]
    parent = resolve_refs(action["parent"], registry)
    summary = resolve_refs(action["summary"], registry)
    labels = action["labels"]
    description_adf = resolve_refs_in_obj(action["description_adf"], registry)

    result = jira_client(
        "create_issue",
        "--project", parent.split("-")[0],
        "--summary", summary,
        "--issue-type", "Sub-task",
        "--parent", parent,
        "--description-adf", json.dumps(description_adf),
        "--labels", ",".join(labels),
    )
    key = result.get("key", "")
    url = build_issue_url(key)
    registry[ref] = {"key": key, "url": url}
    print(f"  Created sub-task: {key} (ref: {ref})")


def execute_create_link(action: dict, registry: dict) -> None:
    link_type = action["link_type"]
    inward = resolve_refs(action["inward"], registry)
    outward = resolve_refs(action["outward"], registry)

    jira_client(
        "create_link",
        "--link-type", link_type,
        "--inward", inward,
        "--outward", outward,
    )
    print(f"  Created link: {inward} {link_type} {outward}")


def execute_post_pr_reply(action: dict, registry: dict) -> None:
    repo = action["repo"]
    pr_number = action["pr_number"]
    comment_id = action["comment_id"]
    body = resolve_refs(action["body"], registry)

    gh_api(
        f"repos/{repo}/pulls/{pr_number}/comments/{comment_id}/replies",
        "-f", f"body={body}",
    )
    print(f"  Posted PR reply on comment {comment_id}")


def execute_create_root_cause_task(action: dict, registry: dict) -> None:
    ref = action["ref"]
    summary = resolve_refs(action["summary"], registry)
    labels = action["labels"]
    description_adf = resolve_refs_in_obj(action["description_adf"], registry)

    project_key = os.environ.get("JIRA_PROJECT_KEY", "")
    if not project_key:
        print("JIRA_PROJECT_KEY is required for root-cause task creation", file=sys.stderr)
        sys.exit(1)

    result = jira_client(
        "create_issue",
        "--project", project_key,
        "--summary", summary,
        "--issue-type", "Task",
        "--description-adf", json.dumps(description_adf),
        "--labels", ",".join(labels),
    )
    key = result.get("key", "")
    url = build_issue_url(key)
    registry[ref] = {"key": key, "url": url}
    print(f"  Created root-cause task: {key} (ref: {ref})")


def execute_post_comment(action: dict, registry: dict) -> None:
    issue = resolve_refs(action["issue"], registry)
    body_adf = resolve_refs_in_obj(action["body_adf"], registry)

    jira_client(
        "add_comment",
        issue,
        "--comment-adf", json.dumps(body_adf),
    )
    print(f"  Posted comment on {issue}")


def execute_post_report(action: dict, registry: dict, report: dict) -> None:
    repo = report["pr_repo"]
    pr_number = report["pr_number"]
    jira_issue_id = report["jira_issue_id"]
    report_md = resolve_refs(report["report_md"], registry)
    report_adf = resolve_refs_in_obj(report["report_adf"], registry)

    result = subprocess.run(
        ["gh", "pr", "comment", str(pr_number), "--body", report_md, "-R", repo],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"Failed to post GitHub PR comment: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"  Posted report to PR #{pr_number}")

    jira_client(
        "add_comment",
        jira_issue_id,
        "--comment-adf", json.dumps(report_adf),
    )
    print(f"  Posted report to Jira {jira_issue_id}")


EXECUTORS = {
    "create_subtask": execute_create_subtask,
    "create_link": execute_create_link,
    "post_pr_reply": execute_post_pr_reply,
    "create_root_cause_task": execute_create_root_cause_task,
    "post_comment": execute_post_comment,
}


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <result-json>", file=sys.stderr)
        sys.exit(1)

    result_path = sys.argv[1]
    with open(result_path) as f:
        data = json.load(f)

    report = data["report"]
    actions = data["actions"]
    registry: dict[str, dict[str, str]] = {}

    print(f"Executing {len(actions)} actions for {report['jira_issue_id']}...")

    for i, action in enumerate(actions):
        action_type = action["type"]
        print(f"[{i + 1}/{len(actions)}] {action_type}")

        if action_type == "post_report":
            execute_post_report(action, registry, report)
        elif action_type in EXECUTORS:
            EXECUTORS[action_type](action, registry)
        else:
            print(f"  Unknown action type: {action_type}", file=sys.stderr)
            sys.exit(1)

    print(f"Done. {len(actions)} actions executed successfully.")


if __name__ == "__main__":
    main()
