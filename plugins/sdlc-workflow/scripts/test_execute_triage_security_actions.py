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


def _trusted_input(authorized=True, markers=None, remediation=None, issue="TC-42", related=None, searches=None):
    """Build the trusted runner fields consumed by the executor."""
    return {
        "issue": {"key": issue},
        "configuration": {"project_key": "TC"},
        "jira_metadata": {"related_issues": related or [], "sibling_searches": searches or []},
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


def test_untrusted_field_target_is_rejected_before_any_jira_call(recorder):
    """A runner grant for TC-8100 cannot authorize a field edit on TC-42."""
    # Given a schema-valid result whose target differs from its trusted identity
    result = _plan([{
        "type": "field-edit", "marker": "triage-security:labels", "issue": "TC-42",
        "fields": {"labels": ["ai-cve-triaged"]},
    }])
    result["report"]["issue"] = "TC-8100"

    # When the executor checks the trusted runner grant
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, _trusted_input(issue="TC-8100"))

    # Then even read-before-write Jira calls are absent
    assert recorder.calls == []


def test_report_only_plan_never_mutates_jira(recorder):
    """A report-only result is preserved without invoking any Jira operation."""
    # Given a sandbox result that contains only the report-only sentinel
    result = _plan([{"type": "report-only", "marker": "triage-security:report"}], "report-only")
    trusted = _trusted_input(authorized=False)
    del trusted["issue"]

    # When the trusted runner executes it without mutation authorization
    executor.execute_plan(result, trusted)

    # Then no Jira operation was requested
    assert recorder.calls == []


@pytest.mark.parametrize("issue", [None, {}, {"key": None}, {"key": 42}, {"key": "invalid"}, {"key": "TC-43"}])
def test_missing_malformed_or_mismatched_trusted_identity_is_rejected(issue, recorder):
    """Mutation grants require a valid trusted identity matching the report."""
    # Given a valid action but absent, malformed, or contradictory trusted identity
    result = _plan([{"type": "field-edit", "marker": "triage-security:labels",
                     "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}}])
    trusted = _trusted_input()
    trusted["issue"] = issue

    # When validating the grant against the complete plan
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, trusted)

    # Then no Jira call occurs
    assert recorder.calls == []


def _remediation_action():
    """Build a synthetic remediation action for authorization regressions."""
    return {
        "type": "remediation-task", "marker": "triage-security:remediation",
        "ref": "remediation", "project": "TC", "summary": "Fix CVE",
        "description_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Synthetic triage."}]}]}, "labels": [],
    }


@pytest.mark.parametrize("marked", [False, True])
@pytest.mark.parametrize("definition", [None, {"targets": ()}, {}])
def test_new_action_without_target_declaration_fails_before_any_jira_call(definition, marked, recorder, monkeypatch):
    """A newly supported action cannot silently bypass target authorization."""
    # Given a future action recognized by validation but lacking target metadata
    monkeypatch.setitem(executor._REQUIRED_ACTION_FIELDS, "future-mutation", {"type", "marker", "issue"})
    if definition is not None:
        monkeypatch.setitem(executor._ACTION_DEFINITIONS, "future-mutation", definition)
    result = _plan([
        {"type": "status-transition", "marker": "triage-security:first", "issue": "TC-42", "status": "In Progress"},
        {"type": "future-mutation", "marker": "triage-security:future", "issue": "TC-43"},
    ])
    trusted = _trusted_input(markers=["triage-security:future"] if marked else [])

    # When the complete plan is preflighted before executing its valid prefix
    with pytest.raises(executor.ActionError, match="target fields"):
        executor._preflight_plan(result, trusted)

    # Then even read-before-write Jira calls are absent
    assert recorder.calls == []


@pytest.mark.parametrize("target_fields", [None, ()])
def test_mutation_with_missing_or_empty_targets_rejects_before_valid_prefix(target_fields, recorder, monkeypatch):
    """Even a schema-valid mutation must have an authorization target declaration."""
    # Given a known action whose target declaration was omitted or left empty
    definition = copy.deepcopy(executor._ACTION_DEFINITIONS["field-edit"])
    if target_fields is None:
        del definition["targets"]
    else:
        definition["targets"] = target_fields
    monkeypatch.setitem(executor._ACTION_DEFINITIONS, "field-edit", definition)
    result = _plan([
        {"type": "status-transition", "marker": "triage-security:first", "issue": "TC-42", "status": "In Progress"},
        {"type": "field-edit", "marker": "triage-security:labels", "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}},
    ])

    # When execution preflights the complete schema-valid plan
    with pytest.raises(executor.ActionError, match="target fields"):
        executor.execute_plan(result, _trusted_input())

    # Then the valid prefix did not read transitions or write Jira state
    assert recorder.calls == []


@pytest.mark.parametrize("issue", ["TC-42", "TC-43"])
def test_new_action_uses_its_declared_target_fields(issue, recorder, monkeypatch):
    """New action declarations authorize trusted targets and reject unrelated ones."""
    # Given a future action whose definition declares its mutation target
    monkeypatch.setitem(executor._REQUIRED_ACTION_FIELDS, "future-mutation", {"type", "marker", "issue"})
    monkeypatch.setitem(executor._ACTION_DEFINITIONS, "future-mutation", {"targets": ("issue",)})
    result = _plan([{"type": "future-mutation", "marker": "triage-security:future", "issue": issue}])

    # When preflight checks the new target declaration
    if issue == "TC-42":
        executor._preflight_plan(result, _trusted_input())
    else:
        with pytest.raises(executor.ActionError, match="unauthorized action target: TC-43"):
            executor._preflight_plan(result, _trusted_input())

    # Then preflight performs no Jira operation in either case
    assert recorder.calls == []


@pytest.mark.parametrize("action", [
    {"type": "field-edit", "marker": "triage-security:untrusted", "issue": "TC-43", "fields": {"labels": ["ai-cve-triaged"]}},
    {"type": "status-transition", "marker": "triage-security:untrusted", "issue": "TC-43", "status": "In Progress"},
    {"type": "comment", "marker": "triage-security:untrusted", "issue": "TC-43", "body_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Synthetic triage."}]}]}},
    {"type": "resolve-reference", "marker": "triage-security:untrusted", "ref": "alias", "issue": "TC-43"},
    {"type": "link", "marker": "triage-security:untrusted", "link_type": "Related", "inward": "TC-43", "outward": "TC-42"},
    {"type": "link", "marker": "triage-security:untrusted", "link_type": "Related", "inward": "TC-42", "outward": "TC-43"},
    {**_remediation_action(), "marker": "triage-security:untrusted", "project": "OTHER"},
])
@pytest.mark.parametrize("marked", [False, True])
def test_late_untrusted_actions_reject_the_entire_plan_before_retry_suppression(action, marked, recorder):
    """Neither a valid first action nor a retry marker permits unrelated targets."""
    # Given a valid first mutation and a late action outside the trusted scope
    result = _plan([
        {"type": "field-edit", "marker": "triage-security:first", "issue": "TC-42", "fields": {"labels": ["first-action"]}},
        action,
    ])
    if action["type"] == "resolve-reference":
        result["actions"].append({"type": "link", "marker": "triage-security:alias-link",
                                  "link_type": "Related", "inward": "TC-42", "outward": "{{alias.key}}"})
    trusted = _trusted_input(markers=["triage-security:untrusted"] if marked else [])
    trusted["issue"]["fields"] = {"labels": ["ai-cve-triaged"]}
    trusted["issue"]["status"] = "In Progress"

    # When the executor preflights all actions before markers or state suppress them
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, trusted)

    # Then no mutation or read occurred for the otherwise valid prefix
    assert recorder.calls == []


@pytest.mark.parametrize("marked", [False, True])
def test_invalid_follow_up_rejects_before_existing_remediation_digest_repair(marked, recorder):
    """An invalid late link prevents digest repair on an earlier retry action."""
    # Given existing remediation missing its digest and a link to an unknown ref
    result = _plan([_remediation_action(), {
        "type": "link", "marker": "triage-security:link", "link_type": "Depend",
        "inward": "TC-42", "outward": "{{unknown.key}}",
    }])
    trusted = _trusted_input(
        markers=["triage-security:remediation", "triage-security:link"] if marked else [],
        remediation=[{"key": "TC-777", "summary": "Fix CVE", "labels": ["ai-generated-jira"], "comments": []}],
    )

    # When complete preflight discovers the unresolved reference
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, trusted)

    # Then even digest reads and repair writes are absent
    assert recorder.calls == []


@pytest.mark.parametrize("binding", [
    {"type": "resolve-reference", "marker": "triage-security:rebind", "ref": "remediation", "issue": "TC-43"},
    {**_remediation_action(), "marker": "triage-security:rebind"},
])
def test_reference_rebinding_cannot_redirect_generated_remediation(binding, recorder):
    """Generated reference names cannot be rebound by a later sandbox action."""
    # Given a valid creation followed by a conflicting reference definition
    result = _plan([_remediation_action(), binding, {
        "type": "link", "marker": "triage-security:link", "link_type": "Depend",
        "inward": "TC-42", "outward": "{{remediation.key}}",
    }])

    # When preflight tracks reference definitions in order
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, _trusted_input(related=[{"key": "TC-43"}]))

    # Then the invalid plan cannot create or digest its first task
    assert recorder.calls == []


@pytest.mark.parametrize("context", [
    {"related": [{"key": "TC-43"}]},
    {"searches": [{"purpose": "same-cve-siblings", "issues": [{"key": "TC-43"}]}]},
    {"searches": [{"purpose": "cross-cve-overlap", "issues": [{"key": "TC-43"}]}]},
    {"searches": [{"purpose": "preemptive-remediation", "issues": [{"key": "TC-43"}]}]},
    {"remediation": [{"key": "TC-43", "labels": ["ai-generated-jira"]}]},
])
def test_prefetched_triage_relationships_authorize_related_targets(context, recorder):
    """Trusted related targets support reconciliation, comments, and both link ends."""
    # Given a prefetched companion or remediation and actions targeting it
    result = _plan([
        {"type": "resolve-reference", "marker": "triage-security:related-ref", "ref": "related", "issue": "TC-43"},
        {"type": "field-edit", "marker": "triage-security:related-labels", "issue": "TC-43", "fields": {"labels": ["ai-cve-triaged"]}},
        {"type": "status-transition", "marker": "triage-security:related-status", "issue": "{{related.key}}", "status": "In Progress"},
        {"type": "comment", "marker": "triage-security:related-comment", "issue": "{{related.key}}", "body_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Synthetic triage."}]}]}},
        {"type": "link", "marker": "triage-security:related-link", "link_type": "Related", "inward": "{{related.key}}", "outward": "TC-42"},
    ])
    trusted = _trusted_input(**context)
    trusted["issue"]["fields"] = {"labels": ["ai-cve-triaged"]}
    trusted["issue"]["status"] = "In Progress"

    # When trusted relationships establish membership independently of the plan
    executor.execute_plan(result, trusted)

    # Then reconciliation and cross-stream operations retain their targets and order
    assert recorder.calls[0] == ("field-edit", "TC-43", {"labels": ["ai-cve-triaged"]})
    assert recorder.calls[1:3] == [("get-transitions", "TC-43"), ("transition", "TC-43", "31")]
    assert recorder.calls[3][0:2] == ("comment", "TC-43")
    assert recorder.calls[4] == ("link", "TC-43", "TC-42", "Related")


def test_related_status_transition_retry_skips_completed_transition_and_continues(recorder, monkeypatch):
    """Replaying a completed related transition does not block later actions."""
    # Given an authorized related target whose transition disappears after success
    result = _plan([
        {"type": "status-transition", "marker": "triage-security:related-status", "issue": "TC-43", "status": "In Progress"},
        {"type": "field-edit", "marker": "triage-security:labels", "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}},
    ])
    trusted = _trusted_input(related=[{"key": "TC-43"}])
    executor.execute_plan(result, trusted)
    assert recorder.calls == [
        ("get-transitions", "TC-43"), ("transition", "TC-43", "31"),
        ("field-edit", "TC-42", {"labels": ["ai-cve-triaged"]}),
    ]
    recorder.calls.clear()

    def get_transitions(issue):
        """Return no transition once the related target has reached its status."""
        recorder.calls.append(("get-transitions", issue))
        return []

    def get_issue(issue, fields="*all"):
        """Return the related issue's current Jira status on replay."""
        recorder.calls.append(("get-issue", issue, fields))
        return {"fields": {"status": {"name": "In Progress"}}}

    monkeypatch.setattr(executor._jira_mod, "get_transitions", get_transitions)
    monkeypatch.setattr(executor._jira_mod, "get_issue", get_issue)

    # When the identical unmarked plan is replayed
    executor.execute_plan(result, trusted)

    # Then Jira confirms the target state, no transition is written, and execution continues
    assert recorder.calls == [
        ("get-transitions", "TC-43"), ("get-issue", "TC-43", "status"),
        ("field-edit", "TC-42", {"labels": ["ai-cve-triaged"]}),
    ]


def test_related_unavailable_transition_in_different_status_still_fails(recorder, monkeypatch):
    """A missing transition is not a no-op unless its target status is reached."""
    # Given an authorized target with no transition and a different current status
    result = _plan([
        {"type": "status-transition", "marker": "triage-security:related-status", "issue": "TC-43", "status": "In Progress"},
        {"type": "field-edit", "marker": "triage-security:labels", "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}},
    ])

    def get_transitions(issue):
        """Record the unavailable transition lookup."""
        recorder.calls.append(("get-transitions", issue))
        return []

    def get_issue(issue, fields="*all"):
        """Return a related issue still awaiting the requested transition."""
        recorder.calls.append(("get-issue", issue, fields))
        return {"fields": {"status": {"name": "New"}}}

    monkeypatch.setattr(executor._jira_mod, "get_transitions", get_transitions)
    monkeypatch.setattr(executor._jira_mod, "get_issue", get_issue)

    # When the missing transition cannot be justified by the current Jira state
    with pytest.raises(executor.ActionError, match="no transition named In Progress for TC-43"):
        executor.execute_plan(result, _trusted_input(related=[{"key": "TC-43"}]))

    # Then execution fails before any mutation or later action
    assert recorder.calls == [
        ("get-transitions", "TC-43"), ("get-issue", "TC-43", "status"),
    ]


def test_unrelated_search_purpose_cannot_expand_trusted_scope(recorder):
    """An arbitrary prefetched search is not a documented triage relationship."""
    # Given a target present only in a search unrelated to triage
    result = _plan([{"type": "field-edit", "marker": "triage-security:labels",
                     "issue": "TC-43", "fields": {"labels": ["ai-cve-triaged"]}}])
    trusted = _trusted_input(searches=[{"purpose": "all-project-issues", "issues": [{"key": "TC-43"}]}])

    # When validating documented relationships
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, trusted)

    # Then the search does not authorize a mutation
    assert recorder.calls == []


@pytest.mark.parametrize("configuration", [None, {}, {"project_key": ""}, {"project_key": "OTHER"}])
def test_remediation_creation_requires_the_trusted_project(configuration, recorder):
    """Missing or contradictory project context cannot authorize task creation."""
    # Given a schema-valid creation with no matching trusted project
    result = _plan([_remediation_action()])
    trusted = _trusted_input()
    trusted["configuration"] = configuration

    # When the runner authorizes the proposed creation
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, trusted)

    # Then neither creation nor digest reads reach Jira
    assert recorder.calls == []


def test_cli_rejects_untrusted_targets_with_nonzero_status(tmp_path, recorder, capsys):
    """Real CLI validation exits non-zero without Jira calls for invalid targets."""
    # Given readable runner files with an unauthorized mutation target
    result = _plan([{"type": "field-edit", "marker": "triage-security:labels",
                     "issue": "TC-43", "fields": {"labels": ["ai-cve-triaged"]}}])
    result_path, input_path = tmp_path / "result.json", tmp_path / "input.json"
    result_path.write_text(json.dumps(result))
    input_path.write_text(json.dumps(_trusted_input()))

    # When the CLI executes its real authorization path
    status = executor.main([str(result_path), str(input_path)])

    # Then it fails loudly without reporting success or making Jira calls
    assert status == 1
    output = capsys.readouterr()
    assert "unauthorized action target" in output.err
    assert "successfully" not in output.out
    assert recorder.calls == []


@pytest.mark.parametrize("action", [
    {
        "type": "link",
        "marker": "triage-security:unsupported-link-type",
        "link_type": "Unsupported",
        "inward": "TC-42",
        "outward": "TC-43",
    },
    {
        "type": "field-edit",
        "marker": "triage-security:empty-field-edit",
        "issue": "TC-42",
        "fields": {},
    },
    {
        "type": "comment",
        "marker": "triage-security:malformed-adf-content",
        "issue": "TC-42",
        "body_adf": {"type": "doc", "version": 1, "content": [{}]},
    },
])
def test_schema_invalid_plan_is_rejected_before_any_jira_operation(action, recorder):
    """The trusted runner rejects schema-invalid sandbox output before mutation."""
    # Given a result that passed only the sandbox's untrusted validation path
    result = _plan([action])

    # When the trusted runner receives the invalid result with authorization
    with pytest.raises(executor.ActionError, match="result schema validation failed"):
        executor.execute_plan(result, _trusted_input())

    # Then it makes no Jira request, including read-before-write operations
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
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Fix CVE."}]}]}, "labels": ["security-preemptive"], "priority": "Major", "fix_versions": ["1.2"]},
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
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Fix CVE."}]}]}, "labels": []},
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
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Fix CVE."}]}]}, "labels": []},
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
    registry = executor.execute_plan(result, _trusted_input(markers=["triage-security:known-task"], related=[{"key": "TC-777"}]))

    # Then the binding survives and the dependent link uses the Jira key
    assert registry["known-task"]["key"] == "TC-777"
    assert recorder.calls == [("link", "TC-42", "TC-777", "Related")]


def test_existing_remediation_without_digest_is_digested_before_follow_up_actions(recorder):
    """A retry repairs a partial creation by posting its missing digest before linking."""
    # Given a prior remediation task that was created before its digest could post
    result = _plan([
        {"type": "remediation-task", "marker": "triage-security:create-remediation", "ref": "remediation-1", "project": "TC", "summary": "Fix CVE", "description_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Fix CVE."}]}]}, "labels": []},
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
    trusted = _trusted_input(related=[{"key": "TC-9001"}])
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
    trusted["issue"]["fields"] = {
        "assignee": {"accountId": "owner", "displayName": "Owner"},
        "resolution": {"id": "10000", "name": "Done"},
    }

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


# SYNTHETIC TEST DATA — release issues and decisions are fictional host evidence.
def _release_trusted():
    trusted = _trusted_input()
    trusted['configuration']['jira_version_prefix'] = 'Product'
    trusted['authorization']['release_decisions'] = [
        {'family': '3.1', 'version': '3.1.2', 'create_epic': True, 'create_task': True}]
    trusted['jira_metadata']['release_jira'] = [
        {'family': '3.1', 'epics': [], 'tasks': [], 'remediation': [], 'originating_cves': []}]
    return trusted


def _release_action(kind='release-epic'):
    action = _remediation_action()
    action.update(type=kind, marker='triage-security:' + kind, ref=kind,
                  family='3.1', version='3.1.2',
                  summary='Product 3.1.2 ' + ('Release Tasks' if kind == 'release-epic' else 'CVE triage'))
    if kind == 'release-task':
        action['parent'] = '{{release-epic.key}}'
    return action


def _release_snapshot(key, kind, parent=None):
    item = {'key': key, 'issue_type': kind, 'summary': 'Product 3.1.2 ' + (
        'Release Tasks' if kind == 'Epic' else 'CVE triage'), 'labels': ['keep-me'],
        'comments': [], 'links': [], 'description': {'type': 'doc', 'version': 1, 'content': []}}
    if parent:
        item['parent'] = parent
    return item


def test_release_creation_parent_and_digest_order(recorder):
    """Given authorized releases, create Epic then child with digests before linking."""
    actions = [_release_action(), _release_action('release-task'), {
        'type': 'link', 'marker': 'triage-security:release-link', 'link_type': 'Depend',
        'inward': 'TC-42', 'outward': '{{release-task.key}}'}]
    registry = executor.execute_plan(_plan(actions), _release_trusted())
    creates = [call[1] for call in recorder.calls if call[0] == 'remediation-task']
    assert [call['issue_type'] for call in creates] == ['Epic', 'Task']
    assert creates[1]['parent'] == 'TC-9001'
    assert registry['release-task']['key'] == 'TC-9002'
    assert [call[0] for call in recorder.calls] == [
        'remediation-task', 'get-issue', 'digest', 'remediation-task', 'get-issue', 'digest', 'link']


@pytest.mark.parametrize('defect', ['decision', 'project', 'family', 'version', 'summary',
                                  'permission', 'future-parent', 'rebound', 'untrusted'])
def test_release_preflight_rejects_entire_plan(defect, recorder):
    """Given a valid prefix and unsafe release suffix, reject before any Jira call."""
    trusted = _release_trusted()
    actions = [_release_action(), _release_action('release-task')]
    if defect == 'decision':
        trusted['authorization'].pop('release_decisions')
    elif defect == 'permission':
        trusted['authorization']['release_decisions'][0]['create_task'] = False
    elif defect == 'future-parent':
        actions.reverse()
    elif defect == 'rebound':
        actions[1]['ref'] = actions[0]['ref']
    elif defect == 'untrusted':
        actions.append({'type': 'comment', 'marker': 'triage-security:bad', 'issue': 'TC-999',
                        'body_adf': actions[0]['description_adf']})
    else:
        actions[1][defect] = {'project': 'OTHER', 'family': '4.0', 'version': '3.1.3',
                              'summary': 'unrelated'}[defect]
    with pytest.raises(executor.ActionError):
        executor.execute_plan(_plan(actions), trusted)
    assert recorder.calls == []


@pytest.mark.parametrize('kind', ['release-epic', 'release-task'])
def test_release_report_only_rejects_new_actions(kind, recorder):
    """Given a report-only plan, release creation never runs."""
    with pytest.raises(executor.ActionError):
        executor.execute_plan(_plan([_release_action(kind)], mode='report-only'), _release_trusted())
    assert recorder.calls == []


def test_release_retry_reuses_and_repairs_digests(recorder):
    """Given a partially created graph, retry repairs digests without duplicating issues."""
    trusted = _release_trusted()
    graph = trusted['jira_metadata']['release_jira'][0]
    graph['epics'] = [_release_snapshot('TC-70', 'Epic')]
    graph['tasks'] = [_release_snapshot('TC-71', 'Task', 'TC-70')]
    trusted['idempotency']['action_markers'] = ['triage-security:release-epic', 'triage-security:release-task']
    registry = executor.execute_plan(_plan([_release_action(), _release_action('release-task')]), trusted)
    assert registry['release-task']['key'] == 'TC-71'
    assert [call[0] for call in recorder.calls] == ['get-issue', 'digest', 'get-issue', 'digest']


@pytest.mark.parametrize('defect', ['wrong-type', 'wrong-parent', 'wrong-project', 'wrong-family',
                                  'ambiguous', 'missing-marked'])
def test_release_retry_invalid_snapshot_fails_before_calls(defect, recorder):
    """Given inconsistent retry evidence, fail closed before repair or creation."""
    trusted = _release_trusted()
    graph = trusted['jira_metadata']['release_jira'][0]
    graph['epics'] = [_release_snapshot('TC-70', 'Epic')]
    graph['tasks'] = [_release_snapshot('TC-71', 'Task', 'TC-70')]
    if defect == 'wrong-type':
        graph['tasks'][0]['issue_type'] = 'Epic'
    elif defect == 'wrong-parent':
        graph['tasks'][0]['parent'] = 'TC-88'
    elif defect == 'wrong-project':
        graph['epics'][0]['key'] = 'OTHER-70'
    elif defect == 'wrong-family':
        graph['family'] = '4.0'
    elif defect == 'ambiguous':
        graph['epics'].append(_release_snapshot('TC-72', 'Epic'))
    else:
        graph['epics'] = []
        graph['tasks'] = []
        trusted['idempotency']['action_markers'] = ['triage-security:release-epic']
    with pytest.raises(executor.ActionError):
        executor.execute_plan(_plan([_release_action(), _release_action('release-task')]), trusted)
    assert recorder.calls == []


def test_release_labels_preserve_snapshot_labels(recorder):
    """Given a bounded release target, a label addition preserves existing labels."""
    trusted = _release_trusted()
    trusted['jira_metadata']['release_jira'][0]['epics'] = [_release_snapshot('TC-70', 'Epic')]
    executor.execute_plan(_plan([{'type': 'field-edit', 'marker': 'triage-security:release-labels',
                                 'issue': 'TC-70', 'fields': {'labels': ['ai-cve-triaged']}}]), trusted)
    assert recorder.calls == [('field-edit', 'TC-70', {'labels': ['keep-me', 'ai-cve-triaged']})]


@pytest.mark.parametrize('failure', ['epic-digest', 'task-create', 'task-digest'])
def test_release_partial_failure_then_retry(failure, recorder, monkeypatch):
    """Given interrupted creation, refreshed host snapshots reuse issues and repair digests."""
    trusted = _release_trusted()
    actions = [_release_action(), _release_action('release-task')]
    original_create = recorder.create_issue
    original_digest = recorder.make_request

    def create(**kwargs):
        if failure == 'task-create' and kwargs['issue_type'] == 'Task':
            raise RuntimeError('synthetic create interruption')
        return original_create(**kwargs)

    def digest(method, path, body):
        if path == ('issue/TC-9001/comment' if failure == 'epic-digest' else 'issue/TC-9002/comment'):
            raise RuntimeError('synthetic digest interruption')
        return original_digest(method, path, body)

    monkeypatch.setattr(executor._jira_mod, 'create_issue', create)
    monkeypatch.setattr(executor._jira_mod, 'make_request', digest)
    with pytest.raises(RuntimeError):
        executor.execute_plan(_plan(actions), trusted)
    graph = trusted['jira_metadata']['release_jira'][0]
    graph['epics'] = [_release_snapshot('TC-9001', 'Epic')]
    if failure == 'task-digest':
        graph['tasks'] = [_release_snapshot('TC-9002', 'Task', 'TC-9001')]
    monkeypatch.setattr(executor._jira_mod, 'create_issue', original_create)
    monkeypatch.setattr(executor._jira_mod, 'make_request', original_digest)
    registry = executor.execute_plan(_plan(actions), trusted)
    assert recorder.created == 2
    assert registry['release-task']['key'] == 'TC-9002'


@pytest.mark.parametrize('defect', ['orphan-remediation', 'orphan-cve', 'wrong-parent-type'])
def test_arbitrary_release_metadata_does_not_authorize(defect, recorder):
    """Given unrelated issues inserted in release metadata, fail before any Jira operation."""
    trusted = _release_trusted()
    graph = trusted['jira_metadata']['release_jira'][0]
    graph['epics'] = [_release_snapshot('TC-70', 'Epic')]
    if defect == 'orphan-remediation':
        graph['remediation'] = [_release_snapshot('TC-72', 'Task')]
    elif defect == 'orphan-cve':
        graph['originating_cves'] = [_release_snapshot('TC-72', 'Vulnerability')]
    else:
        graph['epics'][0]['issue_type'] = 'Task'
    with pytest.raises(executor.ActionError):
        executor.execute_plan(_plan([{'type': 'field-edit', 'marker': 'triage-security:bad-graph',
                                     'issue': 'TC-70', 'fields': {'labels': ['triaged']}}]), trusted)
    assert recorder.calls == []


def test_release_dedup_targets_require_genuine_links(recorder):
    """Given a bounded release graph, linked remediation and CVE accept dedup updates."""
    trusted = _release_trusted()
    graph = trusted['jira_metadata']['release_jira'][0]
    graph['epics'] = [_release_snapshot('TC-70', 'Epic')]
    graph['tasks'] = [_release_snapshot('TC-71', 'Task', 'TC-70')]
    graph['remediation'] = [_release_snapshot('TC-72', 'Task')]
    graph['originating_cves'] = [_release_snapshot('TC-73', 'Vulnerability')]
    graph['tasks'][0]['links'] = [{'type': {'name': 'Blocks'}, 'inwardIssue': {'key': 'TC-72'}}]
    graph['remediation'][0]['links'] = [{'type': {'name': 'Depend'}, 'outwardIssue': {'key': 'TC-73'}}]
    executor.execute_plan(_plan([
        {'type': 'field-edit', 'marker': 'triage-security:dedup-labels', 'issue': 'TC-72',
         'fields': {'labels': ['ai-cve-triaged']}},
        {'type': 'link', 'marker': 'triage-security:dedup-link', 'link_type': 'Related',
         'inward': 'TC-42', 'outward': 'TC-73'}]), trusted)
    assert recorder.calls == [('field-edit', 'TC-72', {'labels': ['keep-me', 'ai-cve-triaged']}),
                              ('link', 'TC-42', 'TC-73', 'Related')]


def test_shared_remediation_across_release_families(recorder):
    """Given two release families sharing remediation, authorize the same linked issue."""
    trusted = _release_trusted()
    entries = trusted['jira_metadata']['release_jira']
    for family, epic_key, task_key in [('3.1', 'TC-70', 'TC-71'), ('3.2', 'TC-80', 'TC-81')]:
        entry = {'family': family, 'epics': [_release_snapshot(epic_key, 'Epic')],
                 'tasks': [_release_snapshot(task_key, 'Task', epic_key)],
                 'remediation': [_release_snapshot('TC-72', 'Task')], 'originating_cves': []}
        for member in entry['epics'] + entry['tasks']:
            member['summary'] = member['summary'].replace('3.1.2', family + '.2')
        entry['tasks'][0]['links'] = [{'type': {'name': 'Blocks'}, 'inwardIssue': {'key': 'TC-72'}}]
        if family == '3.1':
            entries[0] = entry
        else:
            entries.append(entry)
    executor.execute_plan(_plan([{'type': 'field-edit', 'marker': 'triage-security:shared-label',
                                 'issue': 'TC-72', 'fields': {'labels': ['triaged']}}]), trusted)
    assert recorder.calls == [('field-edit', 'TC-72', {'labels': ['keep-me', 'triaged']})]


def test_sequential_release_label_additions_preserve_each_other(recorder):
    """Given two label additions, the second preserves both original and newly added labels."""
    trusted = _release_trusted()
    trusted['jira_metadata']['release_jira'][0]['epics'] = [_release_snapshot('TC-70', 'Epic')]
    executor.execute_plan(_plan([
        {'type': 'field-edit', 'marker': 'triage-security:label-' + label,
         'issue': 'TC-70', 'fields': {'labels': [label]}} for label in ['one', 'two']]), trusted)
    assert recorder.calls[-1] == ('field-edit', 'TC-70', {'labels': ['keep-me', 'one', 'two']})


def test_created_release_labels_survive_followup_edit(recorder):
    """Given a new Epic, a following label edit preserves its creation labels."""
    action = _release_action()
    action['labels'] = ['release-owned']
    executor.execute_plan(_plan([action, {
        'type': 'field-edit', 'marker': 'triage-security:created-label',
        'issue': '{{release-epic.key}}', 'fields': {'labels': ['triaged']}}]), _release_trusted())
    assert recorder.calls[-1] == ('field-edit', 'TC-9001',
                                 {'labels': ['ai-generated-jira', 'release-owned', 'triaged']})


@pytest.mark.parametrize('kind', ['release-epic', 'release-task'])
def test_duplicate_planned_release_identity_fails_before_calls(kind, recorder):
    """Given distinct refs for the same release identity, preflight rejects duplicate creation."""
    first = _release_action(kind)
    second = copy.deepcopy(first)
    second.update(ref='another-release', marker='triage-security:another-release')
    actions = [first, second] if kind == 'release-epic' else [_release_action(), first, second]
    with pytest.raises(executor.ActionError):
        executor.execute_plan(_plan(actions), _release_trusted())
    assert recorder.calls == []
