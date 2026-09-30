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


def _authorized_action_plan():
    """Build a synthetic plan covering all Jira mutation categories."""
    return {
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


def test_authorized_action_plan_executes_each_mutation_category_in_order(recorder):
    """Authorized plans perform field, status, comment, task, digest, and link actions."""
    # Given a complete authorized action plan and explicit trusted identity
    result = _authorized_action_plan()
    trusted_input = {
        "issue": {"key": "TC-42"},
        "configuration": {"project_key": "TC"},
        "authorization": {"mutation_authorized": True}, "idempotency": {},
    }

    # When the trusted runner executes the plan
    executor.execute_plan(result, trusted_input)

    # Then every mutation category occurs and the digest precedes the dependent link
    assert [call[0] for call in recorder.calls] == [
        "field-edit", "get-transitions", "status-transition", "comment",
        "remediation-task", "get-issue", "digest", "link",
    ]
    assert recorder.calls[-1] == ("link", "TC-42", "TC-9001", "Depend")


def test_authorized_contract_rejects_mismatched_runner_identity(recorder):
    """A schema-valid Fullsend plan cannot redirect another issue's runner grant."""
    # Given the complete TC-42 plan under a trusted TC-8100 authorization grant
    result = _authorized_action_plan()
    trusted_input = {
        "issue": {"key": "TC-8100"},
        "configuration": {"project_key": "TC"},
        "authorization": {"mutation_authorized": True}, "idempotency": {},
    }

    # When trusted identity differs from the sandbox report and its targets
    with pytest.raises(executor.ActionError):
        executor.execute_plan(result, trusted_input)

    # Then no mutation category or read reaches Jira
    assert recorder.calls == []


def test_idempotent_retry_fixture_skips_duplicate_mutations(recorder):
    """A rerun with existing state must not recreate Fullsend Jira artifacts."""
    # Given a synthetic retry with existing markers, state, and remediation task
    contract = _fixture("fullsend-idempotent-retry.md")
    contract["trusted_input"]["configuration"] = {"project_key": "TC"}

    # When the trusted executor replays the same action plan
    registry = executor.execute_plan(contract["result"], contract["trusted_input"])

    # Then no duplicate Jira mutation occurs and the existing task remains resolvable
    assert recorder.calls == []
    assert registry["remediation"]["key"] == "TC-9001"


def test_retry_snapshot_suppresses_existing_field_and_link_actions():
    """Trusted Jira state suppresses replayed field and resolved-link actions."""
    # Given a retry fixture with both markers and a populated Jira snapshot
    contract = _fixture("fullsend-idempotent-retry.md")
    field_action, _, _, _, link_action = contract["result"]["actions"]
    resolved_link = {**link_action, "outward": "TC-9001"}

    # When marker suppression is bypassed for actions represented in the snapshot
    field_snapshot = {**contract["trusted_input"], "idempotency": {"action_markers": [], "existing_remediation": []}}

    # Then _already_applied independently detects both existing operations
    assert executor._already_applied(field_action, field_snapshot)
    assert executor._already_applied(resolved_link, field_snapshot)


@pytest.mark.parametrize("source_id", [1, 2, 3, 4, 5, 8, 9, 11, 12, 18])
@requires_format_extra
def test_conditional_fullsend_evals_have_matching_executable_inputs(source_id):
    """Every conditional contract gets an independent gated, subject-bound JSON input."""
    # Given the executable eval cases, rather than grader-only assertions
    evals = json.loads((FIXTURE_DIR.parent / "evals.json").read_text())["evals"]
    fixture = "files/fullsend-eval-{}-trusted-input.json".format(source_id)
    matches = [case for case in evals if fixture in case.get("files", [])]

    # When the executor receives its prompt and mounted input
    assert len(matches) == 1, "conditional contract lacks a matching Fullsend invocation"
    case = matches[0]
    assert case["id"] > 36
    assert "FULLSEND_OUTPUT_DIR" in case["prompt"]
    assert ".pre-script/triage-security-input.json" in case["prompt"]
    assert "invocation.json" in case["prompt"]
    bundle = _trusted_input(Path(fixture).name)
    pre_triage.validate_bundle(bundle)

    # Then identity and authorization belong to this scenario, not a generic sample
    subjects = {1: "TC-8001", 2: "TC-8002", 3: "TC-8003", 4: "TC-8004",
                5: "TC-8005", 8: "TC-8010", 9: "TC-8011", 11: "TC-8021",
                12: "TC-8030", 18: "TC-8001"}
    assert bundle["issue"]["key"] == subjects[source_id]
    assert subjects[source_id] in case["prompt"]
    assert bundle["authorization"]["mutation_authorized"] is (source_id not in [2, 5, 12])
    assert "SYNTHETIC TEST DATA" in bundle["issue"]["fields"]["fixture_purpose"]


def test_conditional_retry_input_has_an_existing_task_without_a_digest():
    """The new partial retry is distinct from the retained fully triaged interactive case."""
    # Given a trusted snapshot of an interrupted remediation creation
    bundle = _trusted_input("fullsend-eval-18-trusted-input.json")
    existing = bundle["idempotency"]["existing_remediation"]

    # When existing remediation identity and ordinary markers are inspected
    assert [item["key"] for item in existing] == ["TC-8100", "TC-8101"]
    assert existing[0]["comments"] == []
    assert executor._has_description_digest(existing[0]) is False
    assert executor._has_description_digest(existing[1]) is True

    # Then the digest repair path retains its stable task reference and retry markers
    assert "triage-security:tc-8001:remediation:upstream" in bundle["idempotency"]["action_markers"]
    assert bundle["issue"]["status"] == "In Progress"
    assert "ai-cve-triaged" in bundle["issue"]["labels"]


def test_conditional_inputs_supply_each_scenarios_distinct_evidence():
    """Scenario inputs retain actual impact, duplicate, overlap, RPM and enrichment facts."""
    # Given independent JSON inputs rather than a shared generic evidence sample
    bundles = {source_id: _trusted_input("fullsend-eval-{}-trusted-input.json".format(source_id))
               for source_id in [1, 2, 3, 4, 5, 8, 9, 11, 12, 18]}

    # When trusted pins are joined with their actual lock evidence
    for bundle in bundles.values():
        reads = {(read["repository"], read["ref"]): read
                 for read in bundle["source_evidence"]["lock_files"]}
        for stream in bundle["matrix"]["streams"]:
            for row in stream["rows"]:
                assert all((repo, ref) in reads for repo, ref in row["source_commits"].items())

    # Then each scenario's decision is supported by its own supplied facts
    assert bundles[1]["issue"]["fields"]["affected_package"] == "quinn-proto"
    assert bundles[1]["issue"]["fields"]["current_user"]["accountId"] == "synthetic-engineer"
    assert all('version = "1.0.13' in read["content"]
               for read in bundles[2]["source_evidence"]["lock_files"])
    assert bundles[3]["jira_metadata"]["sibling_searches"][0]["issues"][0]["key"] == "TC-7999"
    split_reads = bundles[4]["source_evidence"]["lock_files"]
    assert [read["content"].split('version = "')[1].split('"')[0] for read in split_reads] == [
        "0.4.5", "0.4.5", "0.4.8", "0.4.8", "0.4.9", "0.4.9"]
    assert bundles[5]["issue"]["fields"]["sbom_evidence"]["packages"] == [
        {"name": "openssl-libs", "version": version, "release": release}
        for release, version in [("2.2.0", "3.0.7-25.el9_3"), ("2.2.1", "3.0.7-27.el9_4"),
                                 ("2.2.2", "3.0.7-27.el9_4"), ("2.2.3", "3.0.7-28.el9_4"),
                                 ("2.2.4", "3.0.7-28.el9_4")]]
    assert "1.9.0" in bundles[8]["jira_metadata"]["related_issues"][1]["summary"]
    assert bundles[8]["issue"]["fields"]["fixed_version"] == "1.8.2"
    assert bundles[8]["idempotency"]["action_markers"] == ["triage-security:tc-8010:link:related:tc-8008"]
    assert "5.96.1" in bundles[9]["jira_metadata"]["related_issues"][1]["summary"]
    assert bundles[9]["issue"]["fields"]["fixed_version"] == "5.98.0"
    preemptive = bundles[11]["jira_metadata"]["sibling_searches"][0]["issues"][0]
    assert preemptive["key"] == "TC-8022"
    assert "security-preemptive" in preemptive["labels"]
    mitre = bundles[12]["external_evidence"]["mitre"]["body"]
    assert mitre["containers"]["cna"]["affected"][0]["versions"][0]["lessThan"] == "0.4.8"
    assert bundles[12]["external_evidence"]["osv"]["status"] == 503
    assert bundles[12]["external_evidence"]["osv"]["body"] == {}


def test_conditional_retry_fixture_repairs_digest_before_resolving_new_link(recorder):
    """The real partial-retry input repairs one digest and resolves its unapplied link."""
    # Given the mounted partial-retry scenario and its existing task identities
    bundle = _trusted_input("fullsend-eval-18-trusted-input.json")
    tasks = bundle["idempotency"]["existing_remediation"]
    actions = [
        {"type": "remediation-task", "marker": "triage-security:tc-8001:remediation:" + ref,
         "ref": ref, "project": "TC", "summary": task["summary"],
         "description_adf": task["description"], "labels": task["labels"]}
        for ref, task in zip(["upstream", "downstream"], tasks)
    ]
    actions.append({"type": "link", "marker": "triage-security:tc-8001:link:depend:downstream",
                    "link_type": "Depend", "inward": "TC-8001", "outward": "{{downstream.key}}"})
    result = {"schema_version": "1", "mode": "mutation-authorized",
              "report": {"issue": "TC-8001", "outcome": "affected", "summary_markdown": "Partial retry.",
                         "evidence": [{"source": "trusted-input", "detail": "Existing tasks, one missing digest."}]},
              "actions": actions}

    # When the trusted executor processes the repair against a recorded Jira boundary
    registry = executor.execute_plan(result, bundle)

    # Then task creation is skipped, one digest precedes the resolved downstream link
    assert [call[0] for call in recorder.calls] == ["get-issue", "digest", "link"]
    assert recorder.calls[0] == ("get-issue", "TC-8100")
    assert recorder.calls[-1] == ("link", "TC-8001", "TC-8101", "Depend")
    assert {ref: value["key"] for ref, value in registry.items()} == {"upstream": "TC-8100", "downstream": "TC-8101"}

    # Given a refreshed snapshot after the repair, the next retry performs no writes
    tasks[0]["comments"] = [{"body": recorder.calls[1][3]}]
    bundle["idempotency"]["action_markers"].append(actions[-1]["marker"])
    recorder.calls.clear()
    assert executor.execute_plan(result, bundle) == registry
    assert recorder.calls == []
