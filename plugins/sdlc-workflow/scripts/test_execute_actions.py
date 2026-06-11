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
