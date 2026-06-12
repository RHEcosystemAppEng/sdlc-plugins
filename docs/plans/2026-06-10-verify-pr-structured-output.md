# verify-pr Structured Output Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor verify-pr so the sandbox agent produces a structured JSON action plan instead of directly calling Jira/GitHub APIs, and a deterministic post_script on the runner executes all write operations.

**Architecture:** The verify-pr skill gains a "sandbox mode" that outputs a JSON file to `$FULLSEND_OUTPUT_DIR/agent-result.json` instead of calling APIs directly. The JSON contains an ordered array of actions (create sub-task, create link, post PR reply, post report) with cross-references resolved by the post_script at execution time. A JSON Schema validates the output before the post_script runs via fullsend's `validation_loop`. The post_script is a Python script that uses the existing `jira-client.py` for Jira operations and `gh` CLI for GitHub operations.

**Tech Stack:** Python 3 (stdlib only), JSON Schema (draft 2020-12), bash, `gh` CLI, existing `jira-client.py`

---

## File Structure

| File | Responsibility |
|---|---|
| `plugins/sdlc-workflow/schemas/verify-pr-input.schema.json` | JSON Schema for pre-fetched Jira data passed into sandbox |
| `plugins/sdlc-workflow/schemas/verify-pr-result.schema.json` | JSON Schema for verify-pr structured output |
| `plugins/sdlc-workflow/scripts/pre-verify-pr.sh` | Pre_script: validates inputs before sandbox creation |
| `plugins/sdlc-workflow/scripts/post-verify-pr.sh` | Post_script: reads JSON, executes all write operations |
| `plugins/sdlc-workflow/scripts/execute-actions.py` | Python action executor: processes the actions array, resolves refs, calls Jira/GitHub |
| `plugins/sdlc-workflow/scripts/test_execute_actions.py` | Unit tests for the action executor |
| `plugins/sdlc-workflow/skills/verify-pr/SKILL.md` | Modified: adds sandbox mode output path |
| `plugins/sdlc-workflow/harness/verify-pr.yaml` | Modified: adds `pre_script`, `validation_loop`, `post_script`, `runner_env` |
| `plugins/sdlc-workflow/policies/verify-pr.yaml` | Modified: removes Jira/GitHub write access from sandbox |
| `plugins/sdlc-workflow/agents/verify-pr.md` | Modified: instructs agent to use sandbox mode |

---

### Task 1: Define the JSON Schema for verify-pr output

**Files:**
- Create: `plugins/sdlc-workflow/schemas/verify-pr-result.schema.json`

- [ ] **Step 1: Create the schemas directory**

```bash
ls plugins/sdlc-workflow/
```

Verify the directory exists. The `schemas/` subdirectory does not exist yet.

- [ ] **Step 2: Write the JSON Schema**

Create `plugins/sdlc-workflow/schemas/verify-pr-result.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "verify-pr-result.schema.json",
  "title": "Verify PR Agent Result",
  "description": "Structured output from the verify-pr agent. Validated by fullsend's validation_loop before the post_script runs.",
  "type": "object",
  "additionalProperties": false,
  "required": ["report", "actions"],
  "properties": {
    "report": { "$ref": "#/$defs/report" },
    "actions": {
      "type": "array",
      "items": { "$ref": "#/$defs/action" }
    }
  },
  "$defs": {
    "report": {
      "type": "object",
      "required": ["jira_issue_id", "pr_repo", "pr_number", "commit_sha", "overall", "table_md", "report_md", "report_adf", "plugin_version"],
      "additionalProperties": false,
      "properties": {
        "jira_issue_id": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" },
        "pr_repo": { "type": "string", "pattern": "^[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+$" },
        "pr_number": { "type": "integer", "minimum": 1 },
        "commit_sha": { "type": "string", "pattern": "^[0-9a-f]{7,40}$" },
        "overall": { "type": "string", "enum": ["PASS", "WARN", "FAIL"] },
        "table_md": { "type": "string", "minLength": 1 },
        "report_md": { "type": "string", "minLength": 1 },
        "report_adf": { "type": "object" },
        "plugin_version": { "type": "string", "pattern": "^[0-9]+\\.[0-9]+\\.[0-9]+$" }
      }
    },
    "action": {
      "type": "object",
      "required": ["type"],
      "properties": {
        "type": { "type": "string", "enum": ["create_subtask", "create_link", "post_pr_reply", "create_root_cause_task", "post_comment", "post_report"] }
      },
      "allOf": [
        {
          "if": { "properties": { "type": { "const": "create_subtask" } } },
          "then": {
            "required": ["type", "ref", "parent", "summary", "labels", "description_adf"],
            "properties": {
              "type": {},
              "ref": { "type": "string", "pattern": "^[a-z0-9-]+$" },
              "parent": { "type": "string", "pattern": "^[A-Z]+-[0-9]+$" },
              "summary": { "type": "string", "minLength": 1, "maxLength": 255 },
              "labels": { "type": "array", "items": { "type": "string" } },
              "description_adf": { "type": "object" }
            },
            "additionalProperties": false
          }
        },
        {
          "if": { "properties": { "type": { "const": "create_link" } } },
          "then": {
            "required": ["type", "link_type", "inward", "outward"],
            "properties": {
              "type": {},
              "link_type": { "type": "string", "enum": ["Blocks", "Relates"] },
              "inward": { "type": "string", "minLength": 1 },
              "outward": { "type": "string", "minLength": 1 }
            },
            "additionalProperties": false
          }
        },
        {
          "if": { "properties": { "type": { "const": "post_pr_reply" } } },
          "then": {
            "required": ["type", "repo", "pr_number", "comment_id", "body"],
            "properties": {
              "type": {},
              "repo": { "type": "string" },
              "pr_number": { "type": "integer", "minimum": 1 },
              "comment_id": { "type": "integer", "minimum": 1 },
              "body": { "type": "string", "minLength": 1 }
            },
            "additionalProperties": false
          }
        },
        {
          "if": { "properties": { "type": { "const": "create_root_cause_task" } } },
          "then": {
            "required": ["type", "ref", "summary", "labels", "description_adf"],
            "properties": {
              "type": {},
              "ref": { "type": "string", "pattern": "^[a-z0-9-]+$" },
              "summary": { "type": "string", "minLength": 1, "maxLength": 255 },
              "labels": { "type": "array", "items": { "type": "string" } },
              "description_adf": { "type": "object" }
            },
            "additionalProperties": false
          }
        },
        {
          "if": { "properties": { "type": { "const": "post_comment" } } },
          "then": {
            "required": ["type", "issue", "body_adf"],
            "properties": {
              "type": {},
              "issue": { "type": "string", "minLength": 1 },
              "body_adf": { "type": "object" }
            },
            "additionalProperties": false
          }
        },
        {
          "if": { "properties": { "type": { "const": "post_report" } } },
          "then": {
            "required": ["type"],
            "properties": {
              "type": {}
            },
            "additionalProperties": false
          }
        }
      ]
    }
  }
}
```

Key design decisions:
- `ref` fields use simple slugs (`subtask-1`, `rc-1`) for cross-referencing between actions.
- `inward`/`outward` in `create_link` and `issue` in `post_comment` accept both literal Jira keys (`TC-4740`) and ref placeholders (`{{subtask-1.key}}`). The executor resolves placeholders at runtime.
- `body` in `post_pr_reply` may contain `{{ref.key}}` and `{{ref.url}}` placeholders resolved by the executor.
- `post_report` has no extra fields — it reads from the top-level `report` object.
- `report_adf` is a pre-rendered ADF document for the Jira comment. `report_md` is the GitHub PR comment body.

- [ ] **Step 3: Validate the schema is parseable**

Run:
```bash
python3 -c "import json; json.load(open('plugins/sdlc-workflow/schemas/verify-pr-result.schema.json'))" && echo "Valid JSON"
```
Expected: `Valid JSON`

- [ ] **Step 4: Commit**

```bash
git add plugins/sdlc-workflow/schemas/verify-pr-result.schema.json
git commit --trailer="Assisted-by: Claude Code" -m "feat(fullsend): add JSON Schema for verify-pr structured output

Define the output schema for verify-pr sandbox mode. The agent writes
actions (create sub-task, post reply, post report) as a JSON array with
cross-references resolved by the post_script at execution time.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Implement the action executor

The action executor is a Python script that reads the structured JSON output and executes all write operations. It resolves `{{ref.key}}` and `{{ref.url}}` placeholders as actions create entities.

**Files:**
- Create: `plugins/sdlc-workflow/scripts/execute-actions.py`
- Create: `plugins/sdlc-workflow/scripts/test_execute_actions.py`

- [ ] **Step 1: Write the failing test for ref resolution**

Create `plugins/sdlc-workflow/scripts/test_execute_actions.py`:

```python
#!/usr/bin/env python3
"""Tests for execute-actions.py ref resolution and action processing."""

import sys
import os
import json
import importlib.util

script_dir = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "execute_actions",
    os.path.join(script_dir, "execute-actions.py"),
)
execute_actions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(execute_actions)

resolve_refs = execute_actions.resolve_refs


def test_resolve_refs_replaces_key():
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "Sub-task [{{subtask-1.key}}]({{subtask-1.url}}) created."
    result = resolve_refs(text, registry)
    assert result == "Sub-task [TC-100](https://jira.example.com/browse/TC-100) created.", f"Got: {result}"


def test_resolve_refs_no_placeholders():
    registry = {}
    text = "No placeholders here."
    result = resolve_refs(text, registry)
    assert result == "No placeholders here."


def test_resolve_refs_unknown_ref_raises():
    registry = {}
    text = "{{unknown-ref.key}}"
    try:
        resolve_refs(text, registry)
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_resolve_refs_in_adf():
    registry = {"rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"}}
    adf = {
        "type": "doc",
        "content": [
            {"type": "text", "text": "Task {{rc-1.key}} created"}
        ]
    }
    result = execute_actions.resolve_refs_in_obj(adf, registry)
    assert result["content"][0]["text"] == "Task TC-200 created"


if __name__ == "__main__":
    test_resolve_refs_replaces_key()
    test_resolve_refs_no_placeholders()
    test_resolve_refs_unknown_ref_raises()
    test_resolve_refs_in_adf()
    print("All tests passed.")
```

- [ ] **Step 2: Run the test to verify it fails**

Run:
```bash
python3 plugins/sdlc-workflow/scripts/test_execute_actions.py
```
Expected: `ModuleNotFoundError` or `AttributeError` — `execute-actions.py` doesn't exist yet.

- [ ] **Step 3: Write the action executor**

Create `plugins/sdlc-workflow/scripts/execute-actions.py`:

```python
#!/usr/bin/env python3
"""Execute verify-pr structured output actions.

Reads agent-result.json, processes actions sequentially, resolves
{{ref.key}} and {{ref.url}} placeholders as entities are created.

Uses jira-client.py for Jira operations and gh CLI for GitHub operations.
Runs on the fullsend runner (trusted side), not inside the sandbox.

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
    script = os.path.join(os.path.dirname(__file__), "jira-client.py")
    result = subprocess.run(
        ["python3", script, *args],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"jira-client.py {args[0]} failed: {result.stderr}", file=sys.stderr)
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
    return f"{server}/browse/{key}"


def execute_create_subtask(action: dict, registry: dict) -> None:
    ref = action["ref"]
    parent = resolve_refs(action["parent"], registry)
    summary = resolve_refs(action["summary"], registry)
    labels = action["labels"]
    description_adf = resolve_refs_in_obj(action["description_adf"], registry)

    label_args = []
    for label in labels:
        label_args.extend(["--labels", label])

    result = jira_client(
        "create_issue",
        "--project", parent.split("-")[0],
        "--summary", summary,
        "--issue-type", "Sub-task",
        "--parent", parent,
        "--description-adf", json.dumps(description_adf),
        *label_args,
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
        print("WARNING: JIRA_PROJECT_KEY not set", file=sys.stderr)

    label_args = []
    for label in labels:
        label_args.extend(["--labels", label])

    result = jira_client(
        "create_issue",
        "--project", project_key,
        "--summary", summary,
        "--issue-type", "Task",
        "--description-adf", json.dumps(description_adf),
        *label_args,
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
```

- [ ] **Step 4: Run the tests to verify they pass**

Run:
```bash
python3 plugins/sdlc-workflow/scripts/test_execute_actions.py
```
Expected: `All tests passed.`

- [ ] **Step 5: Commit**

```bash
git add plugins/sdlc-workflow/scripts/execute-actions.py plugins/sdlc-workflow/scripts/test_execute_actions.py
git commit --trailer="Assisted-by: Claude Code" -m "feat(fullsend): add action executor for verify-pr structured output

Python script that reads agent-result.json, processes actions
sequentially, and resolves {{ref.key}}/{{ref.url}} placeholders
as Jira entities are created. Uses existing jira-client.py for
Jira REST API and gh CLI for GitHub operations.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Extend jira-client.py to accept ADF directly

The action executor passes pre-rendered ADF objects. The existing `jira-client.py` only accepts `--description-md` (markdown converted to ADF internally). We need `--description-adf` and `--comment-adf` flags that accept raw ADF JSON.

**Files:**
- Modify: `plugins/sdlc-workflow/scripts/jira-client.py:605-700`
- Modify: `plugins/sdlc-workflow/scripts/test_jira_client.py`

- [ ] **Step 1: Add --description-adf flag to create_issue subparser**

In `plugins/sdlc-workflow/scripts/jira-client.py`, find line 605 where subparsers are defined. Find the `create_issue_parser` block and add after the existing `--description-md` argument:

```python
    create_issue_parser.add_argument('--description-adf', help='Issue description as raw ADF JSON (overrides --description-md)')
```

- [ ] **Step 2: Add --comment-adf flag to add_comment subparser**

Find the `add_comment_parser` block (around line 619) and add:

```python
    add_comment_parser.add_argument('--comment-adf', help='Comment body as raw ADF JSON (overrides --comment-md)')
```

- [ ] **Step 3: Update create_issue handler to use ADF when provided**

In the `create_issue` command handler (around line 660), update the description handling to prefer `--description-adf` over `--description-md`:

```python
    if hasattr(args, 'description_adf') and args.description_adf:
        fields['description'] = json.loads(args.description_adf)
    elif hasattr(args, 'description_md') and args.description_md:
        fields['description'] = markdown_to_adf(args.description_md)
```

- [ ] **Step 4: Update add_comment handler to use ADF when provided**

In the `add_comment` command handler (around line 682), update similarly:

```python
    if hasattr(args, 'comment_adf') and args.comment_adf:
        body = json.loads(args.comment_adf)
    elif hasattr(args, 'comment_md') and args.comment_md:
        body = markdown_to_adf(args.comment_md)
```

- [ ] **Step 5: Run existing tests to verify no regressions**

Run:
```bash
python3 plugins/sdlc-workflow/scripts/test_jira_client.py
```
Expected: All existing tests pass.

- [ ] **Step 6: Commit**

```bash
git add plugins/sdlc-workflow/scripts/jira-client.py plugins/sdlc-workflow/scripts/test_jira_client.py
git commit --trailer="Assisted-by: Claude Code" -m "feat(jira-client): add --description-adf and --comment-adf flags

Accept pre-rendered ADF JSON directly, bypassing markdown-to-ADF
conversion. Used by the post_script action executor which receives
ADF from the agent's structured output.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Create the post_script shell wrapper

The post_script is a bash shell script that fullsend invokes on the runner. It finds the result JSON and calls `execute-actions.py`. This follows the same pattern as fullsend's `post-triage.sh`.

**Files:**
- Create: `plugins/sdlc-workflow/scripts/post-verify-pr.sh`

- [ ] **Step 1: Write the post_script**

Create `plugins/sdlc-workflow/scripts/post-verify-pr.sh`:

```bash
#!/usr/bin/env bash
# post-verify-pr.sh — Execute verify-pr structured output actions.
#
# Runs on the fullsend runner AFTER the sandbox is destroyed.
# Working directory is the fullsend run output directory.
#
# Required env vars:
#   JIRA_SERVER_URL   — Jira instance URL
#   JIRA_EMAIL        — Jira user email
#   JIRA_API_TOKEN    — Jira API token
#   JIRA_PROJECT_KEY  — Jira project key (for root-cause task creation)
#   GH_TOKEN          — GitHub token
#
# The agent writes its output to output/agent-result.json (relative to
# the iteration directory). This script finds the most recent iteration's
# output and delegates to execute-actions.py.

set -euo pipefail

RESULT_FILE=""
for dir in iteration-*/output; do
  if [[ -f "${dir}/agent-result.json" ]]; then
    RESULT_FILE="${dir}/agent-result.json"
  fi
done

if [[ -z "${RESULT_FILE}" ]]; then
  echo "ERROR: agent-result.json not found in any iteration output directory"
  exit 1
fi

echo "Reading verify-pr result from: ${RESULT_FILE}"

if ! jq empty "${RESULT_FILE}" 2>/dev/null; then
  echo "ERROR: ${RESULT_FILE} is not valid JSON"
  exit 1
fi

OVERALL=$(jq -r '.report.overall' "${RESULT_FILE}")
ACTION_COUNT=$(jq '.actions | length' "${RESULT_FILE}")
echo "Overall: ${OVERALL}"
echo "Actions: ${ACTION_COUNT}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/execute-actions.py" "${RESULT_FILE}"
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x plugins/sdlc-workflow/scripts/post-verify-pr.sh
```

- [ ] **Step 3: Commit**

```bash
git add plugins/sdlc-workflow/scripts/post-verify-pr.sh
git commit --trailer="Assisted-by: Claude Code" -m "feat(fullsend): add post_script for verify-pr

Shell wrapper that finds agent-result.json from the latest iteration
and delegates to execute-actions.py for action processing. Follows
fullsend's post-triage.sh pattern.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Update the harness to use validation_loop and post_script

**Files:**
- Modify: `plugins/sdlc-workflow/harness/verify-pr.yaml`

- [ ] **Step 1: Update the harness YAML**

Replace the contents of `plugins/sdlc-workflow/harness/verify-pr.yaml` with:

```yaml
agent: agents/verify-pr.md
model: opus
image: ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest
policy: policies/verify-pr.yaml

security:
  enabled: true

host_files:
  - src: env/gcp-vertex.env
    dest: /tmp/workspace/.env.d/gcp-vertex.env
    expand: true
  - src: env/jira.env
    dest: /tmp/workspace/.env.d/jira.env
    expand: true
  - src: env/github.env
    dest: /tmp/workspace/.env.d/github.env
    expand: true
  - src: ${GOOGLE_APPLICATION_CREDENTIALS}
    dest: /tmp/gcp-creds.json
  - src: ${GCP_OIDC_TOKEN_FILE}
    dest: /tmp/gcp-oidc-token
    optional: true

validation_loop:
  script: scripts/validate-output-schema.sh
  max_iterations: 2

post_script: scripts/post-verify-pr.sh

runner_env:
  JIRA_SERVER_URL: "${JIRA_SERVER_URL}"
  JIRA_EMAIL: "${JIRA_EMAIL}"
  JIRA_API_TOKEN: "${JIRA_API_TOKEN}"
  JIRA_PROJECT_KEY: "${JIRA_PROJECT_KEY}"
  GH_TOKEN: "${GH_TOKEN}"
  FULLSEND_OUTPUT_SCHEMA: "schemas/verify-pr-result.schema.json"
  FULLSEND_OUTPUT_FILE: "agent-result.json"

timeout_minutes: 30
```

Key changes from the previous version:
- Added `validation_loop` — uses fullsend's standard `validate-output-schema.sh` to validate agent output against the JSON schema before the post_script runs. Up to 2 iterations if the first output fails validation.
- Added `post_script` — runs `post-verify-pr.sh` on the runner after successful validation.
- Added `runner_env` — Jira and GitHub credentials are available to the post_script on the runner side. These are expanded from `--env-file` values at runtime.

- [ ] **Step 2: Copy fullsend's validate-output-schema.sh**

The validation script is generic — it validates any JSON against a schema. Copy it from fullsend's scaffold:

```bash
cp /Users/mrizzi/git/cloned/fullsend/internal/scaffold/fullsend-repo/scripts/validate-output-schema.sh \
   plugins/sdlc-workflow/scripts/validate-output-schema.sh
chmod +x plugins/sdlc-workflow/scripts/validate-output-schema.sh
```

- [ ] **Step 3: Commit**

```bash
git add plugins/sdlc-workflow/harness/verify-pr.yaml plugins/sdlc-workflow/scripts/validate-output-schema.sh
git commit --trailer="Assisted-by: Claude Code" -m "feat(fullsend): add validation_loop and post_script to verify-pr harness

Harness now validates agent output against JSON schema before running
post_script. Jira/GitHub credentials move to runner_env (trusted side).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Update the sandbox policy to reflect read-only intent

With all write operations moved to the post_script, the sandbox policy entries are renamed to reflect their read-only intent.

**Files:**
- Modify: `plugins/sdlc-workflow/policies/verify-pr.yaml`

- [ ] **Step 1: Update the policy**

Replace the `network_policies` section in `plugins/sdlc-workflow/policies/verify-pr.yaml`:

```yaml
network_policies:
  claude_code:
    name: claude-code
    endpoints:
      - { host: api.anthropic.com, port: 443 }
      - { host: "*.googleapis.com", port: 443 }
      - { host: "*.amazonaws.com", port: 443 }
      - { host: statsig.anthropic.com, port: 443 }
      - { host: sentry.io, port: 443 }
      - { host: raw.githubusercontent.com, port: 443 }
      - { host: platform.claude.com, port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/node" }
  jira_read:
    name: jira-read
    endpoints:
      - { host: "*.atlassian.net", port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/python3" }
  github_read:
    name: github-read
    endpoints:
      - { host: api.github.com, port: 443 }
    binaries:
      - { path: "**/claude" }
      - { path: "**/gh" }
```

Note: OpenShell cannot distinguish GET from POST at the network level. The naming change (`jira` → `jira_read`, `github_api` → `github_read`) is documentation-as-code: it signals that the sandbox should only read. The post_script on the runner is the enforcement layer for write operations. Jira credentials remain in the sandbox env for authenticated read access.

- [ ] **Step 2: Commit**

```bash
git add plugins/sdlc-workflow/policies/verify-pr.yaml
git commit --trailer="Assisted-by: Claude Code" -m "refactor(fullsend): rename policy entries to reflect read-only sandbox

Rename jira → jira_read and github_api → github_read to signal that
the sandbox should only read from these APIs. Write operations are
handled by the post_script on the runner.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: Update the verify-pr skill to support sandbox mode

This is the core change. The skill detects whether it's running in sandbox mode (via `FULLSEND_OUTPUT_DIR` env var) and switches its output path: instead of calling Jira/GitHub APIs directly, it writes structured JSON to the output directory.

**Files:**
- Modify: `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`

- [ ] **Step 1: Add sandbox mode detection after Step 0.5**

Add a new section after "## Step 0.5 – JIRA Access Initialization" in `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`:

```markdown
## Step 0.6 – Sandbox Mode Detection

Check whether the `FULLSEND_OUTPUT_DIR` environment variable is set:

```bash
echo ${FULLSEND_OUTPUT_DIR:-not-set}
```

If set, this skill is running inside a fullsend sandbox. Switch to **sandbox mode**:
- Do NOT call Jira write APIs (create_issue, add_comment, create_link, transition_issue) directly
- Do NOT post GitHub PR comments or replies directly
- Instead, accumulate all write operations as actions in a JSON structure
- At the end of execution, write the complete result to `$FULLSEND_OUTPUT_DIR/agent-result.json`

If not set, execute in **interactive mode** (current behavior — call APIs directly).

Throughout the remaining steps, when you encounter a write operation:
- **Interactive mode:** execute it directly (existing behavior)
- **Sandbox mode:** add it to the actions array instead

Initialize the actions accumulator as an in-memory JSON structure:

```json
{
  "report": {},
  "actions": []
}
```
```

- [ ] **Step 2: Update Step 6d (Create Sub-Tasks) for sandbox mode**

In the "Step 6d – Create Sub-Tasks" section, after each `jira.create_issue` instruction, add the sandbox mode alternative:

```markdown
**Sandbox mode:** Instead of calling `jira.create_issue`, add an action to the accumulator:

```json
{
  "type": "create_subtask",
  "ref": "subtask-N",
  "parent": "<parent-task-id>",
  "summary": "<summary>",
  "labels": ["ai-generated-jira", "review-feedback"],
  "description_adf": <pre-rendered ADF object>
}
```

Then add a `create_link` action:

```json
{
  "type": "create_link",
  "link_type": "Blocks",
  "inward": "{{subtask-N.key}}",
  "outward": "<parent-task-id>"
}
```

Use incrementing refs: `subtask-1`, `subtask-2`, etc. The `{{subtask-N.key}}` placeholder is resolved by the post_script when the sub-task is actually created.
```

- [ ] **Step 3: Update Step 6e (Reply to Review Comments) for sandbox mode**

In the "Step 6e – Reply to Review Comments" section, add:

```markdown
**Sandbox mode:** Instead of calling `gh api`, add an action:

```json
{
  "type": "post_pr_reply",
  "repo": "<owner/repo>",
  "pr_number": <pr-number>,
  "comment_id": <comment-id>,
  "body": "[sdlc-workflow/verify-pr] Classified as **code change request** — sub-task [{{subtask-N.key}}]({{subtask-N.url}}) created."
}
```
```

- [ ] **Step 4: Update Step 7b (Create Root-Cause Tasks) for sandbox mode**

In the "Step 7b – Create Root-Cause Tasks" section, add:

```markdown
**Sandbox mode:** Instead of calling `jira.create_issue`, add actions:

```json
{
  "type": "create_root_cause_task",
  "ref": "rc-N",
  "summary": "Root-cause: <description>",
  "labels": ["ai-generated-jira", "root-cause"],
  "description_adf": <pre-rendered ADF object>
}
```

```json
{
  "type": "create_link",
  "link_type": "Relates",
  "inward": "{{rc-N.key}}",
  "outward": "<parent-task-id>"
}
```

```json
{
  "type": "post_comment",
  "issue": "{{rc-N.key}}",
  "body_adf": <pre-rendered ADF object with root-cause analysis and Comment Footnote>
}
```
```

- [ ] **Step 5: Update Step 9 (Post Report) for sandbox mode**

In the "Step 9 – Post Report" section, add:

```markdown
**Sandbox mode:** Instead of posting directly, populate the `report` object and add a `post_report` action:

Populate the report:

```json
{
  "jira_issue_id": "<issue-id>",
  "pr_repo": "<owner/repo>",
  "pr_number": <pr-number>,
  "commit_sha": "<short-sha>",
  "overall": "PASS|WARN|FAIL",
  "table_md": "<markdown verification table>",
  "report_md": "<full GitHub PR comment body with markdown footnote>",
  "report_adf": <full Jira comment ADF with Comment Footnote>,
  "plugin_version": "<version from plugin.json>"
}
```

Add the final action:

```json
{ "type": "post_report" }
```

Write the complete accumulated JSON to the output file:

```bash
cat > $FULLSEND_OUTPUT_DIR/agent-result.json << 'RESULT_EOF'
<the complete JSON with report and all actions>
RESULT_EOF
```

Verify the file was written:

```bash
python3 -m json.tool $FULLSEND_OUTPUT_DIR/agent-result.json > /dev/null && echo "Output validated"
```
```

- [ ] **Step 6: Commit**

```bash
git add plugins/sdlc-workflow/skills/verify-pr/SKILL.md
git commit --trailer="Assisted-by: Claude Code" -m "feat(verify-pr): add sandbox mode for structured JSON output

When FULLSEND_OUTPUT_DIR is set, the skill accumulates write operations
as JSON actions instead of calling APIs directly. The result is written
to agent-result.json for the post_script to process.

Interactive mode (no FULLSEND_OUTPUT_DIR) is unchanged — APIs are
called directly as before.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: Update the agent prompt for sandbox mode

**Files:**
- Modify: `plugins/sdlc-workflow/agents/verify-pr.md`

- [ ] **Step 1: Update the agent prompt**

Replace the contents of `plugins/sdlc-workflow/agents/verify-pr.md` with:

```markdown
---
name: verify-pr
description: >-
  Verify a PR against its Jira task acceptance criteria using the
  sdlc-workflow verify-pr skill inside an OpenShell sandbox.
model: opus
---

# Verify PR Agent

You are a PR verification agent running inside an OpenShell sandbox with the
sdlc-workflow plugin pre-installed.

## Startup procedure

1. Read the `JIRA_ISSUE_ID` environment variable:
   ```bash
   echo $JIRA_ISSUE_ID
   ```

2. Invoke the verify-pr skill with that issue ID. The skill is available as
   `/sdlc-workflow:verify-pr`. Example:
   ```
   /sdlc-workflow:verify-pr TC-4715
   ```

3. The skill handles everything: fetching the Jira task, identifying the PR,
   dispatching sub-agents for analysis, and producing the output.

4. After the skill completes, verify the output file exists:
   ```bash
   ls -la $FULLSEND_OUTPUT_DIR/agent-result.json
   ```

## Constraints

- Do not modify code. This agent only verifies.
- Do not push branches or create PRs.
- Do not call Jira write APIs directly — the skill writes structured JSON output.
- Do not post GitHub comments directly — the post_script handles this.
- Follow the skill's output — do not improvise verification steps.
```

- [ ] **Step 2: Commit**

```bash
git add plugins/sdlc-workflow/agents/verify-pr.md
git commit --trailer="Assisted-by: Claude Code" -m "refactor(fullsend): update verify-pr agent prompt for sandbox mode

Agent now verifies output file exists after skill completion.
Constraints updated to reflect that write operations are handled
by the post_script, not the agent.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: Update fullsend.md documentation

**Files:**
- Modify: `fullsend.md`

- [ ] **Step 1: Update the Quick start section**

In `fullsend.md`, remove `--no-post-script` from the local mode Quick start command and its explanation. The command becomes:

```bash
fullsend run verify-pr \
  --fullsend-dir plugins/sdlc-workflow \
  --target-repo /tmp/my-repo-clone \
  --env-file secrets.env
```

Replace the `--no-post-script` explanation with:

```markdown
The post_script handles all Jira/GitHub write operations (sub-task creation,
PR comment replies, verification report posting) after the sandbox agent
completes and output validation passes.
```

- [ ] **Step 2: Update the comparison table**

Update the "Pre/post scripts" row in the comparison table to:

```markdown
| Pre/post scripts | `pre_script` + `post_script` for split-trust | `post_script` executes structured JSON actions from sandbox output | ✓ | **Converged**: sandbox produces `agent-result.json` with ordered actions. `post_script` resolves `{{ref.key}}` placeholders and executes writes (Jira sub-tasks, PR replies, report posting). `validation_loop` validates output against JSON schema before post_script runs. | [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md), [security-threat-model.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/problems/security-threat-model.md) |
```

Update the "Validation loop" row to:

```markdown
| Validation loop | `validation_loop:` with script + `max_iterations` | `validation_loop` validates `agent-result.json` against `verify-pr-result.schema.json` | ✓ | **Converged**: uses fullsend's standard `validate-output-schema.sh` with the verify-pr JSON schema. Up to 2 iterations if first output fails validation. | [customizing-agents.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/guides/user/customizing-agents.md), [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md) |
```

Update the "Output schemas" row to:

```markdown
| Output schemas | `schemas/` directory for JSON validation | `schemas/verify-pr-result.schema.json` | ✓ | **Converged**: JSON Schema defines action types, cross-reference format, and report structure. Validated by `validation_loop` before post_script runs. | [architecture.md](https://github.com/fullsend-ai/fullsend/blob/58cc443/docs/architecture.md) |
```

- [ ] **Step 3: Update the file inventory table**

Add new rows to the file inventory table:

```markdown
| `schemas/verify-pr-result.schema.json` | JSON Schema for verify-pr structured output | Defines the action types, cross-reference format, and report structure. Validated by fullsend's `validation_loop` before the post_script runs. |
| `scripts/post-verify-pr.sh` | Post_script for verify-pr | Shell wrapper that finds `agent-result.json` and delegates to `execute-actions.py`. Runs on the trusted runner after sandbox is destroyed. |
| `scripts/execute-actions.py` | Action executor | Processes the ordered actions array, resolves `{{ref.key}}` placeholders as Jira entities are created, calls `jira-client.py` and `gh` CLI for all write operations. |
| `scripts/validate-output-schema.sh` | Output schema validator | Generic script from fullsend that validates JSON against a schema using Python's `jsonschema`. Used by `validation_loop`. |
```

- [ ] **Step 4: Commit**

```bash
git add fullsend.md
git commit --trailer="Assisted-by: Claude Code" -m "docs(fullsend): update for structured output convergence

Remove --no-post-script from quick start. Update comparison table
to reflect converged pre/post scripts, validation loop, and output
schemas. Add new files to inventory.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 10: Add pre_script for input validation (Phase 3 — deferred)

The pre_script runs on the trusted runner BEFORE sandbox creation. It validates
inputs and fails fast on invalid configuration, avoiding wasted sandbox compute
time (~$2-5 per failed run). This converges with fullsend's canonical pattern
where `pre_script` guards against invalid inputs.

**Files:**
- Create: `plugins/sdlc-workflow/scripts/pre-verify-pr.sh`
- Modify: `plugins/sdlc-workflow/harness/verify-pr.yaml`

- [ ] **Step 1: Write the pre_script**

Create `plugins/sdlc-workflow/scripts/pre-verify-pr.sh`:

```bash
#!/usr/bin/env bash
# pre-verify-pr.sh — Validate inputs before sandbox creation.
#
# Runs on the fullsend runner BEFORE the sandbox is created.
# Fails fast on invalid inputs to avoid wasting sandbox compute time.
#
# Required env vars:
#   JIRA_ISSUE_ID     — Jira issue key (e.g., TC-4741)
#   JIRA_SERVER_URL   — Jira instance URL
#   JIRA_EMAIL        — Jira user email
#   JIRA_API_TOKEN    — Jira API token
#   GH_TOKEN          — GitHub token

set -euo pipefail

# 1. Validate required env vars are set
: "${JIRA_ISSUE_ID:?JIRA_ISSUE_ID is required}"
: "${JIRA_SERVER_URL:?JIRA_SERVER_URL is required}"
: "${JIRA_EMAIL:?JIRA_EMAIL is required}"
: "${JIRA_API_TOKEN:?JIRA_API_TOKEN is required}"
: "${GH_TOKEN:?GH_TOKEN is required}"

# 2. Validate JIRA_ISSUE_ID format
if [[ ! "${JIRA_ISSUE_ID}" =~ ^[A-Z]+-[0-9]+$ ]]; then
  echo "ERROR: JIRA_ISSUE_ID '${JIRA_ISSUE_ID}' does not match expected format (e.g., TC-4741)"
  exit 1
fi

echo "Issue: ${JIRA_ISSUE_ID}"

# 3. Verify the Jira issue exists
AUTH=$(echo -n "${JIRA_EMAIL}:${JIRA_API_TOKEN}" | base64)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Basic ${AUTH}" \
  -H "Accept: application/json" \
  "${JIRA_SERVER_URL}/rest/api/3/issue/${JIRA_ISSUE_ID}?fields=summary")

if [[ "${HTTP_CODE}" == "404" ]]; then
  echo "ERROR: Jira issue ${JIRA_ISSUE_ID} not found"
  exit 1
elif [[ "${HTTP_CODE}" != "200" ]]; then
  echo "ERROR: Jira API returned HTTP ${HTTP_CODE} for ${JIRA_ISSUE_ID}"
  exit 1
fi

echo "Jira issue verified: ${JIRA_ISSUE_ID}"

# 4. Check if the issue has a linked PR (best-effort — don't fail if field is missing)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PR_FIELD=$(python3 "${SCRIPT_DIR}/jira-client.py" get_issue "${JIRA_ISSUE_ID}" \
  --fields "customfield_10875" 2>/dev/null | \
  python3 -c "import json,sys; d=json.load(sys.stdin); f=d.get('fields',{}).get('customfield_10875',''); print(f if f else '')" 2>/dev/null || echo "")

if [[ -n "${PR_FIELD}" ]]; then
  echo "PR linked: ${PR_FIELD}"
else
  echo "WARNING: No PR linked in Jira custom field — the skill will ask for the PR URL"
fi

echo "Input validation passed"
```

- [ ] **Step 2: Make it executable**

```bash
chmod +x plugins/sdlc-workflow/scripts/pre-verify-pr.sh
```

- [ ] **Step 3: Add pre_script to the harness**

In `plugins/sdlc-workflow/harness/verify-pr.yaml`, add the `pre_script` field
before the `post_script` line:

```yaml
pre_script: scripts/pre-verify-pr.sh
post_script: scripts/post-verify-pr.sh
```

- [ ] **Step 4: Test locally**

```bash
export JIRA_ISSUE_ID=TC-4741
source /tmp/sdlc-workflow-secrets.env
bash plugins/sdlc-workflow/scripts/pre-verify-pr.sh
```

Expected: "Input validation passed"

Test with bad input:

```bash
JIRA_ISSUE_ID=INVALID bash plugins/sdlc-workflow/scripts/pre-verify-pr.sh
```

Expected: Error about format

- [ ] **Step 5: Rebuild image and run fullsend end-to-end**

```bash
podman build -f plugins/sdlc-workflow/sandboxes/base/Dockerfile \
  -t ghcr.io/mrizzi/sdlc-plugins/sdlc-base:latest .
```

Then run fullsend with a disposable clone and verify the pre_script runs
before sandbox creation.

- [ ] **Step 6: Commit**

```bash
git add plugins/sdlc-workflow/scripts/pre-verify-pr.sh plugins/sdlc-workflow/harness/verify-pr.yaml
git commit --trailer="Assisted-by: Claude Code" -m "feat(fullsend): add pre_script for verify-pr input validation

Validate JIRA_ISSUE_ID format and existence, check required env vars,
and verify PR linkage before creating the sandbox. Fails fast on
invalid inputs to avoid wasting sandbox compute time.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```

---

### Task 11: Pre_script data passing — fetch Jira issue into sandbox (Phase 4)

The pre_script already validates that the Jira issue exists (Task 10). This task
extends it to fetch the full issue details, write them to a JSON file, and mount
that file into the sandbox via `host_files`. The skill reads the pre-fetched data
instead of calling the Jira API from inside the sandbox.

Once all Jira reads are handled by the pre_script, the `jira_read` network
policy entry and Jira credentials (`JIRA_EMAIL`, `JIRA_API_TOKEN`) can be
removed from the sandbox entirely. The sandbox would only need `claude_code`
and `github_read` network access.

**Files:**
- Create: `plugins/sdlc-workflow/schemas/verify-pr-input.schema.json`
- Modify: `plugins/sdlc-workflow/scripts/pre-verify-pr.sh`
- Modify: `plugins/sdlc-workflow/harness/verify-pr.yaml`
- Modify: `plugins/sdlc-workflow/policies/verify-pr.yaml` — remove `jira_read`
- Modify: `plugins/sdlc-workflow/env/jira.env` — remove `JIRA_EMAIL`, `JIRA_API_TOKEN`
- Modify: `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`

- [ ] **Step 1: Define the input JSON Schema**

Create `plugins/sdlc-workflow/schemas/verify-pr-input.schema.json` that defines
the structure of the pre-fetched Jira data passed into the sandbox:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "verify-pr-input.schema.json",
  "title": "Verify PR Pre-Script Input",
  "description": "Pre-fetched Jira issue data written by the pre_script and mounted into the sandbox.",
  "type": "object",
  "required": ["jira_issue_id", "jira_issue", "pr_url"],
  "additionalProperties": false,
  "properties": {
    "jira_issue_id": {
      "type": "string",
      "pattern": "^[A-Z]+-[0-9]+$"
    },
    "jira_issue": {
      "type": "object",
      "description": "Full Jira issue response from GET /rest/api/3/issue/{key}"
    },
    "pr_url": {
      "type": "string",
      "description": "PR URL extracted from the Jira custom field, or empty if not linked"
    }
  }
}
```

- [ ] **Step 2: Update pre_script to write pre-fetched data**

In `plugins/sdlc-workflow/scripts/pre-verify-pr.sh`, after the existing
validation steps, add:

```bash
# 5. Fetch full issue details and write to workspace for sandbox consumption
ISSUE_JSON=$(python3 "${SCRIPT_DIR}/jira-client.py" get_issue "${JIRA_ISSUE_ID}" --fields "*all" 2>/dev/null)
if [[ -z "${ISSUE_JSON}" ]]; then
  echo "WARNING: Could not fetch full issue details — sandbox will re-fetch"
else
  PRE_OUTPUT_DIR="/tmp/workspace/pre-script-output"
  mkdir -p "${PRE_OUTPUT_DIR}"
  python3 -c "
import json, sys
issue = json.loads(sys.argv[1])
pr_url = sys.argv[2]
output = {
    'jira_issue_id': sys.argv[3],
    'jira_issue': issue,
    'pr_url': pr_url
}
json.dump(output, sys.stdout, indent=2)
" "${ISSUE_JSON}" "${PR_FIELD}" "${JIRA_ISSUE_ID}" > "${PRE_OUTPUT_DIR}/verify-pr-input.json"
  echo "Pre-fetched issue data written to ${PRE_OUTPUT_DIR}/verify-pr-input.json"
fi
```

- [ ] **Step 3: Add host_files entry for pre-fetched data**

In `plugins/sdlc-workflow/harness/verify-pr.yaml`, add a `host_files` entry
that mounts the pre-script output into the sandbox:

```yaml
host_files:
  # ... existing entries ...
  - src: /tmp/workspace/pre-script-output/verify-pr-input.json
    dest: /tmp/workspace/.pre-script/verify-pr-input.json
    optional: true
```

The `optional: true` ensures the sandbox still starts if the pre-script
couldn't fetch the data (the skill falls back to fetching from the API).

- [ ] **Step 4: Update the skill to read pre-fetched data**

In `plugins/sdlc-workflow/skills/verify-pr/SKILL.md`, add a new step after
Step 0.6 (Sandbox Mode Detection):

```markdown
## Step 0.7 – Load Pre-Fetched Data

Check if pre-fetched Jira issue data exists:

```bash
cat /tmp/workspace/.pre-script/verify-pr-input.json 2>/dev/null | python3 -m json.tool > /dev/null 2>&1 && echo "Pre-fetched data available" || echo "No pre-fetched data"
```

If the file exists and contains valid JSON:
- Read the `jira_issue` field — this is the full Jira issue response
- Read the `pr_url` field — this is the PR URL from the custom field
- Skip Steps 1 (Fetch Jira Task) and 2 (Identify PR) — use the pre-fetched
  data instead

If the file does not exist or is invalid:
- Proceed with Steps 1 and 2 as normal (fetch from Jira API directly)
```

This step applies in both interactive and sandbox mode. In interactive mode,
the file won't exist (no pre_script ran), so the skill proceeds normally.

- [ ] **Step 5: Remove jira_read from sandbox policy**

In `plugins/sdlc-workflow/policies/verify-pr.yaml`, remove the `jira_read`
network policy entry entirely. The sandbox no longer needs Jira API access —
all Jira data comes from the pre-fetched input file.

In `plugins/sdlc-workflow/env/jira.env`, remove `JIRA_EMAIL` and
`JIRA_API_TOKEN` exports. Keep `JIRA_SERVER_URL` (used by the skill for
constructing browse URLs in the structured output) and `JIRA_ISSUE_ID`
(read by the agent prompt).

- [ ] **Step 6: Test with fullsend end-to-end**

Rebuild the image and run fullsend. Verify:
- Pre_script fetches issue data and writes `verify-pr-input.json`
- Sandbox starts without Jira network access
- Skill reads pre-fetched data from the mounted file
- No Jira API calls from inside the sandbox
- Post_script executes actions normally

- [ ] **Step 7: Commit**

```bash
git add plugins/sdlc-workflow/schemas/verify-pr-input.schema.json \
  plugins/sdlc-workflow/scripts/pre-verify-pr.sh \
  plugins/sdlc-workflow/harness/verify-pr.yaml \
  plugins/sdlc-workflow/policies/verify-pr.yaml \
  plugins/sdlc-workflow/env/jira.env \
  plugins/sdlc-workflow/skills/verify-pr/SKILL.md
git commit --trailer="Assisted-by: Claude Code" -m "feat(fullsend): pre_script passes Jira data into sandbox

The pre_script fetches the full Jira issue and writes it to a JSON
file that host_files mounts into the sandbox. The skill reads
pre-fetched data instead of calling the Jira API directly.

Removes jira_read from the sandbox network policy and Jira
credentials from the sandbox environment — the sandbox no longer
has any Jira API access.

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
```
