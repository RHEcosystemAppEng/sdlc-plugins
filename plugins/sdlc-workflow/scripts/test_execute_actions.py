#!/usr/bin/env python3
"""Tests for execute-actions.py ref resolution and native Jira comment posting."""

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
    """A single {{ref.key}}/{{ref.url}} pair resolves to registered values."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "Sub-task [{{subtask-1.key}}]({{subtask-1.url}}) created."
    result = resolve_refs(text, registry)
    assert result == "Sub-task [TC-100](https://jira.example.com/browse/TC-100) created.", f"Got: {result}"


def test_resolve_refs_no_placeholders():
    """Text without placeholders is returned unchanged."""
    registry = {}
    text = "No placeholders here."
    result = resolve_refs(text, registry)
    assert result == "No placeholders here."


def test_resolve_refs_unknown_ref_raises():
    """An unregistered ref raises KeyError."""
    registry = {}
    text = "{{unknown-ref.key}}"
    try:
        resolve_refs(text, registry)
        assert False, "Should have raised KeyError"
    except KeyError:
        pass


def test_resolve_refs_in_adf():
    """resolve_refs_in_obj resolves placeholders nested inside an ADF doc."""
    registry = {"rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"}}
    adf = {
        "type": "doc",
        "content": [
            {"type": "text", "text": "Task {{rc-1.key}} created"}
        ]
    }
    result = execute_actions.resolve_refs_in_obj(adf, registry)
    assert result["content"][0]["text"] == "Task TC-200 created"


def test_resolve_refs_multiple_different_refs():
    """Multiple distinct refs in one string each resolve independently."""
    registry = {
        "subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"},
        "rc-1": {"key": "TC-200", "url": "https://jira.example.com/browse/TC-200"},
    }
    text = "Sub-task {{subtask-1.key}} and root-cause {{rc-1.key}} ({{rc-1.url}})."
    result = resolve_refs(text, registry)
    assert result == "Sub-task TC-100 and root-cause TC-200 (https://jira.example.com/browse/TC-200).", f"Got: {result}"


def test_resolve_refs_repeated_placeholder():
    """A placeholder repeated in one string resolves at every occurrence."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "{{subtask-1.key}} depends on {{subtask-1.key}}."
    result = resolve_refs(text, registry)
    assert result == "TC-100 depends on TC-100.", f"Got: {result}"


def test_resolve_refs_mixed_key_url_same_ref():
    """The .key and .url fields of one ref resolve to their respective values."""
    registry = {"subtask-1": {"key": "TC-100", "url": "https://jira.example.com/browse/TC-100"}}
    text = "See {{subtask-1.key}} at {{subtask-1.url}}; {{subtask-1.key}} must be done first."
    result = resolve_refs(text, registry)
    assert result == "See TC-100 at https://jira.example.com/browse/TC-100; TC-100 must be done first.", f"Got: {result}"


class _FakeCompleted:
    """Stand-in for subprocess.CompletedProcess."""

    def __init__(self, returncode=0, stderr=""):
        self.returncode = returncode
        self.stderr = stderr


class _RunRecorder:
    """Captures the argv/input/env of a single subprocess.run call."""

    def __init__(self, returncode=0, stderr=""):
        self.returncode = returncode
        self.stderr = stderr
        self.cmd = None
        self.input = None
        self.env = None

    def __call__(self, cmd, input=None, text=None, capture_output=None, env=None):
        self.cmd = cmd
        self.input = input
        self.env = env
        return _FakeCompleted(self.returncode, self.stderr)


_JIRA_ENV = {
    "JIRA_SERVER_URL": "https://jira.example.com",
    "JIRA_EMAIL": "bot@example.com",
    "JIRA_API_TOKEN": "s3cr3t",
}


def _with_jira_env_and_recorder(recorder):
    """Install a fake subprocess.run + Jira env; return a restore callback."""
    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = recorder
    os.environ.update(_JIRA_ENV)

    def restore():
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    return restore


def test_post_jira_comment_native_builds_argv():
    """post_jira_comment_native calls the native CLI with marker, project, and number."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-321", "hello **world**")
    finally:
        restore()

    assert recorder.cmd[:4] == ["fullsend", "issues", "post-comment", "--tracker"], f"Got: {recorder.cmd}"
    assert "jira" in recorder.cmd
    assert "--project" in recorder.cmd and recorder.cmd[recorder.cmd.index("--project") + 1] == "TC"
    assert "--number" in recorder.cmd and recorder.cmd[recorder.cmd.index("--number") + 1] == "321"
    assert "--marker" in recorder.cmd
    assert recorder.cmd[recorder.cmd.index("--marker") + 1] == execute_actions.STICKY_COMMENT_MARKER
    assert "--result" in recorder.cmd and recorder.cmd[recorder.cmd.index("--result") + 1] == "-"
    assert recorder.input == "hello **world**"


def test_post_jira_comment_native_maps_env():
    """The native CLI receives JIRA_BASE_URL/JIRA_USER_EMAIL/JIRA_TOKEN mapped from this script's vars."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-1", "body")
    finally:
        restore()

    assert recorder.env["JIRA_BASE_URL"] == "https://jira.example.com"
    assert recorder.env["JIRA_USER_EMAIL"] == "bot@example.com"
    assert recorder.env["JIRA_TOKEN"] == "s3cr3t"


def test_post_jira_comment_native_nonzero_exits():
    """A non-zero CLI exit aborts with sys.exit(1)."""
    recorder = _RunRecorder(returncode=1, stderr="boom")
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC-1", "body")
        assert False, "Should have exited"
    except SystemExit as e:
        assert e.code == 1
    finally:
        restore()


def test_post_jira_comment_native_invalid_key_exits():
    """A malformed issue key (no hyphen) aborts before invoking the CLI."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    try:
        execute_actions.post_jira_comment_native("TC123", "body")
        assert False, "Should have exited"
    except SystemExit as e:
        assert e.code == 1
    finally:
        restore()
    assert recorder.cmd is None, "CLI should not run for an invalid key"


def test_execute_post_comment_routes_to_native():
    """execute_post_comment resolves refs then posts body_md to the action's issue."""
    recorder = _RunRecorder()
    restore = _with_jira_env_and_recorder(recorder)
    registry = {"sub-1": {"key": "TC-500", "url": "https://jira.example.com/browse/TC-500"}}
    try:
        execute_actions.execute_post_comment(
            {"type": "post_comment", "issue": "{{sub-1.key}}", "body_md": "See {{sub-1.url}}"},
            registry,
        )
    finally:
        restore()

    assert recorder.cmd[recorder.cmd.index("--number") + 1] == "500"
    assert recorder.input == "See https://jira.example.com/browse/TC-500"


def test_execute_post_report_posts_github_then_jira():
    """execute_post_report posts the report to GitHub via gh, then to Jira via the native CLI."""
    calls = []

    def fake_run(cmd, input=None, text=None, capture_output=None, env=None):
        calls.append({"cmd": cmd, "input": input, "env": env})
        return _FakeCompleted(0, "")

    saved_run = execute_actions.subprocess.run
    saved_env = {k: os.environ.get(k) for k in _JIRA_ENV}
    execute_actions.subprocess.run = fake_run
    os.environ.update(_JIRA_ENV)
    try:
        report = {
            "pr_repo": "acme/widget",
            "pr_number": 42,
            "jira_issue_id": "TC-777",
            "report_md": "## Verify report\nAll good.",
        }
        execute_actions.execute_post_report({"type": "post_report"}, {}, report)
    finally:
        execute_actions.subprocess.run = saved_run
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    assert len(calls) == 2, f"Expected gh + native calls, got {len(calls)}"
    gh_call, jira_call = calls
    assert gh_call["cmd"][:3] == ["gh", "pr", "comment"]
    assert "acme/widget" in gh_call["cmd"]
    assert jira_call["cmd"][:3] == ["fullsend", "issues", "post-comment"]
    assert jira_call["cmd"][jira_call["cmd"].index("--number") + 1] == "777"
    assert jira_call["input"] == "## Verify report\nAll good."


if __name__ == "__main__":
    test_resolve_refs_replaces_key()
    test_resolve_refs_no_placeholders()
    test_resolve_refs_unknown_ref_raises()
    test_resolve_refs_in_adf()
    test_resolve_refs_multiple_different_refs()
    test_resolve_refs_repeated_placeholder()
    test_resolve_refs_mixed_key_url_same_ref()
    test_post_jira_comment_native_builds_argv()
    test_post_jira_comment_native_maps_env()
    test_post_jira_comment_native_nonzero_exits()
    test_post_jira_comment_native_invalid_key_exits()
    test_execute_post_comment_routes_to_native()
    test_execute_post_report_posts_github_then_jira()
    print("All tests passed.")
