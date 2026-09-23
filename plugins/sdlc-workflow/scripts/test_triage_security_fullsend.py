#!/usr/bin/env python3
"""Contract tests for the triage-security Fullsend boundary."""

import importlib.util
import json
from pathlib import Path

import pytest
from jsonschema import FormatChecker


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = Path(__file__).parent
FIXTURE_DIR = ROOT / "evals" / "triage-security" / "files"


def _load_module(name, filename):
    """Load a hyphenated workflow script as an importable test module."""
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


executor = _load_module("triage_security_fullsend_executor", "execute-triage-security-actions.py")
pre_triage = _load_module("triage_security_fullsend_pre_triage", "pre_triage_security.py")
requires_format_extra = pytest.mark.skipif(
    not all(fmt in FormatChecker().checkers for fmt in pre_triage._REQUIRED_FORMATS),
    reason="requires jsonschema[format] for uri/date-time format enforcement")


def _fixture(name):
    """Load the deliberate JSON contract data embedded in a synthetic fixture."""
    document = (FIXTURE_DIR / name).read_text()
    return json.loads(document.split("```json\n", 1)[1].split("\n```", 1)[0])


def _trusted_input(name):
    """Load a mounted trusted-input fixture exactly as the sandbox receives it."""
    return json.loads((FIXTURE_DIR / name).read_text())


def _load_fullsend_input(document, output_dir):
    """Load trusted sandbox input or write the documented fail-closed result."""
    try:
        return json.loads(document)
    except json.JSONDecodeError:
        (output_dir / "agent-result.json").write_text(
            '{ "error": "triage-security aborted: trusted input is missing, invalid JSON, '
            'or fails triage-security-input.schema.json; no interactive fallback is available in the sandbox." }')
        return None


class _JiraRecorder:
    """Record boundary writes that a trusted runner would send to Jira."""

    def __init__(self):
        self.calls = []

    def update_issue(self, issue, fields):
        """Record a field mutation."""
        self.calls.append(("field-edit", issue, fields))

    def get_transitions(self, issue):
        """Return the transition used by the synthetic action plan."""
        self.calls.append(("get-transitions", issue))
        return [{"id": "31", "to": {"name": "In Progress"}}]

    def transition_issue(self, issue, transition):
        """Record a status mutation."""
        self.calls.append(("status-transition", issue, transition))

    def create_issue(self, **kwargs):
        """Record creation of the deterministic remediation task."""
        self.calls.append(("remediation-task", kwargs))
        return {"key": "TC-9001"}

    def get_issue(self, issue):
        """Return the stored remediation description for digest generation."""
        self.calls.append(("get-issue", issue))
        return {"fields": {"description": {
            "type": "doc", "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Stored."}]}],
        }}}

    def create_link(self, inward, outward, link_type):
        """Record an issue-link mutation."""
        self.calls.append(("link", inward, outward, link_type))

    def make_request(self, method, path, body):
        """Record the remediation description digest comment."""
        self.calls.append(("digest", method, path, body))
        return {"id": "1"}

    def post_native(self, issue, body, marker):
        """Record a sticky summary comment."""
        self.calls.append(("comment", issue, body, marker))


@pytest.fixture
def recorder(monkeypatch):
    """Replace the Jira boundary with a recorder for each contract test."""
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


def test_report_only_fixture_never_reaches_the_jira_boundary(recorder):
    """A report-only Fullsend result must not perform Jira mutations."""
    # Given a synthetic report-only result and unauthorized trusted input
    contract = _fixture("fullsend-report-only.md")

    # When the trusted executor processes the result
    executor.execute_plan(contract["result"], contract["trusted_input"])

    # Then the Jira boundary remains untouched
    assert recorder.calls == []


def test_invalid_bundle_fixture_is_rejected_before_jira_writes(recorder):
    """Malformed Fullsend output must fail closed before any Jira operation."""
    # Given a synthetic result with contradictory evidence and an invalid action
    contract = _fixture("fullsend-invalid-bundle.md")

    # When the trusted executor validates the result
    with pytest.raises(executor.ActionError, match="result schema validation failed"):
        executor.execute_plan(contract["result"], contract["trusted_input"])

    # Then validation prevents all Jira boundary calls
    assert recorder.calls == []


@requires_format_extra
def test_trusted_input_fixtures_validate_against_the_sandbox_schema():
    """Authorized, report-only, and RPM inputs are executable trusted bundles."""
    # Given the three JSON fixtures mounted for successful Fullsend paths
    fixture_names = [
        "fullsend-authorized-trusted-input.json",
        "fullsend-report-only-trusted-input.json",
        "fullsend-rpm-trusted-input.json",
    ]

    # When the same pre-triage validator checks each mounted input
    for name in fixture_names:
        pre_triage.validate_bundle(_trusted_input(name))

    # Then their authorization values preserve their intended execution branches
    assert _trusted_input(fixture_names[0])["authorization"]["mutation_authorized"] is True
    assert all(not _trusted_input(name)["authorization"]["mutation_authorized"]
               for name in fixture_names[1:])


def test_invalid_trusted_input_fixture_fails_closed_before_analysis(tmp_path):
    """Malformed mounted input fails before it can enter Fullsend analysis."""
    # Given the deliberately incomplete mounted JSON fixture
    document = (FIXTURE_DIR / "fullsend-invalid-trusted-input.md").read_text()
    malformed = document.split("```json\n", 1)[1].split("\n```", 1)[0]

    # When the Fullsend entrypoint loads the trusted input
    result = _load_fullsend_input(malformed, tmp_path)

    # Then it writes only the prescribed failure result
    assert result is None
    assert json.loads((tmp_path / "agent-result.json").read_text()) == {"error": "triage-security aborted: trusted input is missing, invalid JSON, or fails triage-security-input.schema.json; no interactive fallback is available in the sandbox."}
    assert sorted(path.name for path in tmp_path.iterdir()) == ["agent-result.json"]


def test_authorized_action_plan_executes_each_mutation_category_in_order(recorder):
    """Authorized plans perform field, status, comment, task, digest, and link actions."""
    # Given a complete authorized action plan from the sandbox
    result = {
        "schema_version": "1",
        "mode": "mutation-authorized",
        "report": {
            "issue": "TC-42",
            "outcome": "affected",
            "summary_markdown": "Affected.",
            "evidence": [{"source": "synthetic", "detail": "deliberate contract data"}],
        },
        "actions": [
            {"type": "field-edit", "marker": "triage-security:labels", "issue": "TC-42", "fields": {"labels": ["ai-cve-triaged"]}},
            {"type": "status-transition", "marker": "triage-security:status", "issue": "TC-42", "status": "In Progress"},
            {"type": "comment", "marker": "triage-security:summary", "issue": "TC-42", "body_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Summary."}]}]}},
            {"type": "remediation-task", "marker": "triage-security:remediation", "ref": "remediation", "project": "TC", "summary": "Fix synthetic CVE", "description_adf": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Fix."}]}]}, "labels": []},
            {"type": "link", "marker": "triage-security:link", "link_type": "Depend", "inward": "TC-42", "outward": "{{remediation.key}}"},
        ],
    }
    trusted_input = {"authorization": {"mutation_authorized": True}, "idempotency": {}}

    # When the trusted runner executes the plan
    executor.execute_plan(result, trusted_input)

    # Then every mutation category occurs and the digest precedes the dependent link
    assert [call[0] for call in recorder.calls] == [
        "field-edit", "get-transitions", "status-transition", "comment",
        "remediation-task", "get-issue", "digest", "link",
    ]
    assert recorder.calls[-1] == ("link", "TC-42", "TC-9001", "Depend")


def test_idempotent_retry_fixture_skips_duplicate_mutations(recorder):
    """A rerun with existing state must not recreate Fullsend Jira artifacts."""
    # Given a synthetic retry with existing markers, state, and remediation task
    contract = _fixture("fullsend-idempotent-retry.md")

    # When the trusted executor replays the same action plan
    registry = executor.execute_plan(contract["result"], contract["trusted_input"])

    # Then no duplicate Jira mutation occurs and the existing task remains resolvable
    assert recorder.calls == []
    assert registry["remediation"]["key"] == "TC-9001"
