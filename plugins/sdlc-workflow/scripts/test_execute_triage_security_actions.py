#!/usr/bin/env python3
"""Tests for trusted triage-security action execution."""

import copy
import hashlib
import importlib.util
import json
import os
import subprocess

import pytest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SPEC = importlib.util.spec_from_file_location(
    "execute_triage_security_actions",
    os.path.join(SCRIPT_DIR, "execute-triage-security-actions.py"),
)
executor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(executor)


def _plan(actions, mode="mutation-authorized"):
    """Build a minimally valid triage-security result plan."""
    return {
        "schema_version": "1",
        "mode": mode,
        "report": {
            "issue": "TC-42",
            "outcome": "affected",
            "summary_markdown": "Affected by the vulnerability.",
            "evidence": [{"source": "test", "detail": "deliberate fixture"}],
        },
        "actions": actions,
    }


def _trusted_input(authorized=True, markers=None, remediation=None):
    """Build the trusted runner fields consumed by the executor."""
    return {
        "authorization": {"mutation_authorized": authorized},
        "idempotency": {
            "action_markers": markers or [],
            "existing_remediation": remediation or [],
        },
    }


class _JiraRecorder:
    """Capture Jira client calls without issuing network requests."""

    def __init__(self):
        self.calls = []
        self.created = 0

    def update_issue(self, issue, fields):
        """Record a Jira field update."""
        self.calls.append(("field-edit", issue, fields))

    def get_transitions(self, issue):
        """Provide a catalog whose action name differs from its target status."""
        self.calls.append(("get-transitions", issue))
        return [{"id": "31", "name": "Start Progress", "to": {"name": "In Progress"}}]

    def transition_issue(self, issue, transition):
        """Record a Jira transition."""
        self.calls.append(("transition", issue, transition))

    def create_issue(self, **kwargs):
        """Record remediation creation and return a deterministic Jira key."""
        self.created += 1
        self.calls.append(("remediation-task", kwargs))
        return {"key": "TC-900{}".format(self.created), "self": "https://jira.example/issue/900{}".format(self.created)}

    def get_issue(self, issue):
        """Return the stored description Jira would return after normalization."""
        self.calls.append(("get-issue", issue))
        return {"fields": {"description": {
            "type": "doc", "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Stored by Jira."}]}],
        }}}

    def create_link(self, inward, outward, link_type):
        """Record an issue-link operation."""
        self.calls.append(("link", inward, outward, link_type))

    def make_request(self, method, path, body):
        """Record direct ADF digest comments."""
        self.calls.append(("digest", method, path, body))
        return {"id": "1"}

    def post_native(self, issue, body, marker):
        """Record a native sticky Jira comment."""
        self.calls.append(("comment", issue, body, marker))


@pytest.fixture
def recorder(monkeypatch):
    """Replace Jira client calls with a recorder for each test."""
    value = _JiraRecorder()
    monkeypatch.setattr(executor._jira_mod, "update_issue", value.update_issue)
    monkeypatch.setattr(executor._jira_mod, "get_transitions", value.get_transitions)
    monkeypatch.setattr(executor._jira_mod, "transition_issue", value.transition_issue)
    monkeypatch.setattr(executor._jira_mod, "create_issue", value.create_issue)
    monkeypatch.setattr(executor._jira_mod, "get_issue", value.get_issue)
    monkeypatch.setattr(executor._jira_mod, "create_link", value.create_link)
    monkeypatch.setattr(executor._jira_mod, "make_request", value.make_request)
    monkeypatch.setattr(executor._action_helpers, "post_jira_comment_native", value.post_native)
    return value


def test_report_only_plan_never_mutates_jira(recorder):
    """A report-only result is preserved without invoking any Jira operation."""
    # Given a sandbox result that contains only the report-only sentinel
    result = _plan([{"type": "report-only", "marker": "triage-security:report"}], "report-only")

    # When the trusted runner executes it without mutation authorization
    executor.execute_plan(result, _trusted_input(authorized=False))

    # Then no Jira operation was requested
    assert recorder.calls == []


def test_unauthorized_mutating_plan_fails_without_jira_calls(recorder):
    """A mutating result cannot bypass an absent trusted authorization grant."""
    # Given a plan with a valid-looking mutation but no runner authorization
    result = _plan([{
        "type": "field-edit", "marker": "triage-security:labels", "issue": "TC-42",
        "fields": {"labels": ["ai-cve-triaged"]},
    }])

    # When execution checks the trusted bundle
    with pytest.raises(executor.ActionError, match="not authorized"):
        executor.execute_plan(result, _trusted_input(authorized=False))

    # Then authorization fails before any Jira operation
    assert recorder.calls == []


def test_authorized_actions_execute_in_order_with_footnoted_comments(recorder):
    """Authorized field, transition, and comment actions retain plan order and footer."""
    # Given an authorized plan with all non-creation mutation forms
    result = _plan([
        {"type": "field-edit", "marker": "triage-security:fields", "issue": "TC-42", "fields": {"assignee": {"id": "owner"}, "labels": ["ai-cve-triaged"], "resolution": {"name": "Done"}}},
        {"type": "status-transition", "marker": "triage-security:status", "issue": "TC-42", "status": "In Progress"},
        {"type": "comment", "marker": "triage-security:summary", "issue": "TC-42", "body_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Triage complete."}]}]}},
    ])

    # When the trusted runner executes the plan
    executor.execute_plan(result, _trusted_input())

    # Then the operations run deterministically and the comment has its audit footer
    assert [call[0] for call in recorder.calls] == ["field-edit", "get-transitions", "transition", "comment"]
    comment = recorder.calls[-1]
    assert comment[3] == "<!-- triage-security:summary -->"
    assert "---" in comment[2]
    assert "sdlc-workflow/triage-security" in comment[2]
    assert "v{}".format(executor._plugin_version()) in comment[2]


def test_remediation_digest_precedes_links_and_resolves_references(recorder):
    """Created remediation tasks are registered and digested before dependent links."""
    # Given a remediation task followed by a link to its generated reference
    result = _plan([
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": []}, "labels": ["security-preemptive"], "priority": "Major", "fix_versions": ["1.2"]},
        {"type": "link", "marker": "triage-security:link-remediation", "link_type": "Depend", "inward": "TC-42", "outward": "{{remediation-1.key}}"},
    ])

    # When the authorized actions run
    executor.execute_plan(result, _trusted_input())

    # Then task creation carries inherited metadata, its digest is first, and its key resolves in the link
    assert recorder.calls[0][0] == "remediation-task"
    assert recorder.calls[0][1]["labels"] == ["ai-generated-jira", "security-preemptive"]
    assert recorder.calls[0][1]["priority"] == "Major"
    assert recorder.calls[0][1]["fix_versions"] == ["1.2"]
    assert recorder.calls[1] == ("get-issue", "TC-9001")
    assert recorder.calls[2][0] == "digest"
    stored = recorder.get_issue("TC-9001")["fields"]["description"]
    expected = hashlib.sha256(json.dumps(stored, separators=(",", ":")).encode("utf-8")).hexdigest()
    assert "Description digest: sha256-adf:{}".format(expected) in json.dumps(recorder.calls[2][3])
    assert recorder.calls[3] == ("link", "TC-42", "TC-9001", "Depend")


def test_existing_marker_and_remediation_skip_retry_duplicates(recorder):
    """Stable runner markers and existing remediation state make retries idempotent."""
    # Given actions already applied by a previous trusted runner attempt
    result = _plan([
        {"type": "field-edit", "marker": "triage-security:fields", "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}},
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": []}, "labels": []},
    ])
    trusted = _trusted_input(
        markers=["triage-security:fields"],
        remediation=[{"key": "TC-777", "summary": "Fix CVE", "labels": ["ai-generated-jira"], "description": {"type": "doc", "version": 1, "content": []}, "comments": [{"body": "[sdlc-workflow] Description digest: sha256-adf:already"}]}],
    )

    # When the same plan is retried
    registry = executor.execute_plan(result, trusted)

    # Then no duplicate writes occur and the existing task resolves the reference
    assert recorder.calls == []
    assert registry["remediation-1"]["key"] == "TC-777"


def test_marked_remediation_still_populates_references_for_dependent_actions(recorder):
    """A skipped remediation action still resolves its reference before later links."""
    # Given a retry marker and the prior task recorded in trusted idempotency state
    result = _plan([
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": []}, "labels": []},
        {"type": "link", "marker": "triage-security:link", "link_type": "Depend", "inward": "TC-42", "outward": "{{remediation-1.key}}"},
    ])
    trusted = _trusted_input(
        markers=["triage-security:create-remediation"],
        remediation=[{"key": "TC-777", "summary": "Fix CVE", "labels": ["ai-generated-jira"], "description": {"type": "doc", "version": 1, "content": []}, "comments": [{"body": "[sdlc-workflow] Description digest: sha256-adf:already"}]}],
    )

    # When the marked plan is retried
    registry = executor.execute_plan(result, trusted)

    # Then its generated reference remains usable by the dependent link
    assert registry["remediation-1"]["key"] == "TC-777"
    assert recorder.calls == [("link", "TC-42", "TC-777", "Depend")]


def test_marked_reference_binding_still_resolves_dependent_actions(recorder):
    """A marker never suppresses an in-memory reference binding needed by later actions."""
    # Given a reference binding whose marker was persisted by an earlier attempt
    result = _plan([
        {"type": "resolve-reference", "marker": "triage-security:known-task", "ref": "known-task", "issue": "TC-777"},
        {"type": "link", "marker": "triage-security:link", "link_type": "Related", "inward": "TC-42", "outward": "{{known-task.key}}"},
    ])

    # When the retry skips persisted mutations
    registry = executor.execute_plan(result, _trusted_input(markers=["triage-security:known-task"]))

    # Then the binding survives and the dependent link uses the Jira key
    assert registry["known-task"]["key"] == "TC-777"
    assert recorder.calls == [("link", "TC-42", "TC-777", "Related")]


def test_existing_remediation_without_digest_is_digested_before_follow_up_actions(recorder):
    """A retry repairs a partial creation by posting its missing digest before linking."""
    # Given a prior remediation task that was created before its digest could post
    result = _plan([
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": []}, "labels": []},
        {"type": "link", "marker": "triage-security:link", "link_type": "Depend", "inward": "TC-42", "outward": "{{remediation-1.key}}"},
    ])
    trusted = _trusted_input(remediation=[{"key": "TC-777", "summary": "Fix CVE", "labels": ["ai-generated-jira"], "description": {"type": "doc", "version": 1, "content": []}, "comments": []}])

    # When retry execution discovers the prior task
    executor.execute_plan(result, trusted)

    # Then it posts the stored-description digest before the dependent link
    assert [call[0] for call in recorder.calls] == ["get-issue", "digest", "link"]


def test_existing_issue_state_skips_retried_field_status_and_link_actions(recorder):
    """A real-shaped Jira link snapshot prevents duplicate retry mutations."""
    # Given a later pre-script snapshot with existing state and Jira's single far-end link shape
    result = _plan([
        {"type": "field-edit", "marker": "triage-security:fields", "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}},
        {"type": "status-transition", "marker": "triage-security:status", "issue": "TC-42", "status": "In Progress"},
        {"type": "link", "marker": "triage-security:link", "link_type": "Depend", "inward": "TC-42", "outward": "TC-9001"},
    ])
    trusted = _trusted_input()
    trusted["issue"] = {
        "key": "TC-42",
        "status": "In Progress",
        "fields": {
            "labels": ["ai-cve-triaged"],
            "issuelinks": [{
                "type": {"name": "Depend"},
                "outwardIssue": {"key": "TC-9001"},
            }],
        },
    }

    # When the identical plan is retried without markers
    executor.execute_plan(result, trusted)

    # Then the current Jira state still prevents duplicate mutations
    assert recorder.calls == []


def test_existing_object_fields_skip_retried_field_edits(recorder):
    """Full Jira field objects match compact assignee and resolution retry values."""
    # Given a retry action and its full Jira snapshot field representations
    result = _plan([{
        "type": "field-edit", "marker": "triage-security:fields", "issue": "TC-42",
        "fields": {"assignee": {"id": "owner"}, "resolution": {"name": "Done"}},
    }])
    trusted = _trusted_input()
    trusted["issue"] = {"fields": {
        "assignee": {"accountId": "owner", "displayName": "Owner"},
        "resolution": {"id": "10000", "name": "Done"},
    }}

    # When the same object-valued field edit is retried
    executor.execute_plan(result, trusted)

    # Then the executor avoids clobbering the current Jira field values
    assert recorder.calls == []


def test_empty_field_edit_is_not_treated_as_already_applied():
    """An empty field map never becomes idempotent through all([])."""
    # Given an otherwise valid field-edit action with no values to compare
    action = {"type": "field-edit", "marker": "triage-security:empty", "issue": "TC-42", "fields": {}}

    # When idempotency evaluates the empty map
    already_applied = executor._already_applied(action, _trusted_input())

    # Then it remains eligible for validation rather than appearing applied
    assert already_applied is False


def test_other_object_fields_require_an_exact_snapshot_match():
    """Compact matching does not hide changed values in unrelated object fields."""
    # Given an object-valued custom field whose value differs from the snapshot
    action = {
        "type": "field-edit", "marker": "triage-security:custom", "issue": "TC-42",
        "fields": {"customfield_12345": {"name": "Risk", "value": "new"}},
    }
    trusted = _trusted_input()
    trusted["issue"] = {"fields": {"customfield_12345": {"name": "Risk", "value": "old"}}}

    # When idempotency compares the custom object field
    already_applied = executor._already_applied(action, trusted)

    # Then the changed value remains eligible for an update
    assert already_applied is False


def test_unresolved_or_malformed_actions_fail_before_writes(recorder):
    """Unknown references and malformed actions cannot reach Jira as mutations."""
    # Given independently invalid plans
    unresolved = _plan([{"type": "link", "marker": "triage-security:bad-link", "link_type": "Related", "inward": "TC-42", "outward": "{{unknown.key}}"}])
    malformed = _plan([{"type": "field-edit", "marker": "triage-security:bad-fields", "issue": "TC-42"}])

    # When execution validates each action plan
    with pytest.raises(executor.ActionError):
        executor.execute_plan(unresolved, _trusted_input())
    with pytest.raises(executor.ActionError):
        executor.execute_plan(malformed, _trusted_input())

    # Then no partial mutation is emitted for invalid input
    assert recorder.calls == []


def test_partial_failure_propagates_without_success_message(recorder, monkeypatch, capsys):
    """A failed Jira write aborts execution and never prints a completion claim."""
    # Given an authorized update whose Jira client operation fails
    result = _plan([{"type": "field-edit", "marker": "triage-security:fields", "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}}])
    monkeypatch.setattr(executor._jira_mod, "update_issue", lambda *_args: (_ for _ in ()).throw(RuntimeError("network down")))

    # When the executor receives the operational error
    with pytest.raises(RuntimeError, match="network down"):
        executor.execute_plan(result, _trusted_input())

    # Then it does not incorrectly report success
    assert "successfully" not in capsys.readouterr().out.lower()


def test_main_returns_nonzero_for_executor_failures(tmp_path, monkeypatch, capsys):
    """The command entry point reports an executor failure with a non-zero status."""
    # Given readable runner files whose execution raises an operational error
    result_path = tmp_path / "result.json"
    input_path = tmp_path / "input.json"
    result_path.write_text(json.dumps(_plan([{"type": "report-only", "marker": "triage-security:report"}], "report-only")))
    input_path.write_text(json.dumps(_trusted_input(False)))
    monkeypatch.setattr(executor, "execute_plan", lambda *_args: (_ for _ in ()).throw(RuntimeError("Jira unavailable")))

    # When the CLI runs the executor
    status = executor.main([str(result_path), str(input_path)])

    # Then it exposes failure rather than claiming completion
    assert status == 1
    assert "Jira unavailable" in capsys.readouterr().err


def test_post_script_rejects_an_iteration_result_outside_its_run_directory(tmp_path):
    """The trusted post-script refuses a symlinked result that escapes the run directory."""
    # Given a runner directory whose selected iteration result resolves elsewhere
    script = os.path.join(SCRIPT_DIR, "post-triage-security.sh")
    run_directory = tmp_path / "run"
    (run_directory / "pre").mkdir(parents=True)
    (run_directory / "pre" / "triage-security-input.json").write_text(json.dumps(_trusted_input(False)))
    iteration_output = run_directory / "iteration-1" / "output"
    iteration_output.mkdir(parents=True)
    outside_result = tmp_path / "outside-result.json"
    outside_result.write_text(json.dumps(_plan([{"type": "report-only", "marker": "triage-security:report"}], "report-only")))
    (iteration_output / "agent-result.json").symlink_to(outside_result)

    # When the runner attempts to select the post-validation result
    result = subprocess.run(
        ["bash", script], cwd=run_directory,
        env={"PATH": os.environ["PATH"], "FULLSEND_RUN_DIR": str(run_directory)},
        capture_output=True, text=True,
    )

    # Then it fails before handing an untrusted path to the executor
    assert result.returncode != 0
    assert "escapes" in result.stderr


def test_post_script_selects_an_in_run_result_from_a_different_working_directory(tmp_path):
    """The post-script resolves validated output from FULLSEND_RUN_DIR, not its CWD."""
    # Given the validated output and matching pre-script authorization in one run
    script = os.path.join(SCRIPT_DIR, "post-triage-security.sh")
    run_directory = tmp_path / "run"
    (run_directory / "pre").mkdir(parents=True)
    (run_directory / "pre" / "triage-security-input.json").write_text(json.dumps(_trusted_input(False)))
    iteration_output = run_directory / "iteration-1" / "output"
    iteration_output.mkdir(parents=True)
    (iteration_output / "agent-result.json").write_text(
        json.dumps(_plan([{"type": "report-only", "marker": "triage-security:report"}], "report-only")))

    # When the trusted post-script runs outside its Fullsend run directory
    result = subprocess.run(
        ["bash", script], cwd=tmp_path,
        env={"PATH": os.environ["PATH"], "FULLSEND_RUN_DIR": str(run_directory)},
        capture_output=True, text=True,
    )

    # Then it completes without needing Jira credentials or performing a mutation
    assert result.returncode == 0, result.stderr
    assert "completed successfully" in result.stdout
