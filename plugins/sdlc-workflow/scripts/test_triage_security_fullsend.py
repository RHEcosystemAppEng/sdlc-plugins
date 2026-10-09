#!/usr/bin/env python3
"""Deterministic boundary contracts; hosted evals prove actual skill execution."""

import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess

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


def _skill_bash(heading, index=0):
    """Read a literal delivered instruction block without duplicating its logic."""
    skill = (ROOT / "plugins/sdlc-workflow/skills/triage-security/SKILL.md").read_text()
    section = skill.split(heading, 1)[1].split("\n##", 1)[0]
    return re.findall(r"```bash\n(.*?)\n```", section, re.DOTALL)[index].replace(
        "${CLAUDE_PLUGIN_ROOT}", str(ROOT / "plugins/sdlc-workflow"))


def _run_instruction(source, gate):
    """Execute source contracts only, never an agent or a local skill eval."""
    environment = {key: value for key, value in os.environ.items()
                   if key != "FULLSEND_OUTPUT_DIR"}
    if gate is not None:
        environment["FULLSEND_OUTPUT_DIR"] = gate
    return subprocess.run(["bash", "-c", source], env=environment,
                          capture_output=True, text=True, check=False)


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
    """The literal input-validation contract emits only the exact abort result."""
    # Given the deliberately incomplete mounted JSON fixture
    document = (FIXTURE_DIR / "fullsend-invalid-trusted-input.md").read_text()
    malformed = document.split("```json\n", 1)[1].split("\n```", 1)[0]

    input_path = tmp_path / "trusted-input.json"
    input_path.write_text(malformed)
    output_path = tmp_path / "output"
    output_path.mkdir()
    source = _skill_bash("### Step 0.7 – Load Trusted Fullsend Input").replace(
        "/sandbox/workspace/.pre-script/triage-security-input.json", str(input_path))

    # When executing the literal instruction, not an agent execution
    result = _run_instruction(source, str(output_path))

    # Then it writes only the prescribed failure result
    assert result.returncode == 1
    assert "ERROR: trusted triage-security input is invalid JSON:" in result.stdout
    assert json.loads((output_path / "agent-result.json").read_text()) == {"error": "triage-security aborted: trusted input is missing, invalid JSON, or fails triage-security-input.schema.json; no interactive fallback is available in the sandbox."}
    assert sorted(path.name for path in output_path.iterdir()) == ["agent-result.json"]


@pytest.mark.parametrize("gate, exit_code, stdout, stderr", [
    (None, 0, "interactive mode\n", ""),
    ("", 1, "", "ERROR: FULLSEND_OUTPUT_DIR is set but empty\n"),
    ("/synthetic-output", 0, "sandbox mode: /synthetic-output\n", ""),
])
def test_literal_gate_instruction_distinguishes_presence(gate, exit_code, stdout, stderr):
    """Catch truthiness regressions in source; this is not proof the agent routed."""
    # Given the production instruction and separately supplied environment state
    source = _skill_bash("### Step 0.6 – Fullsend Mode Detection")

    # When a credential-free shell executes that exact gate instruction
    result = _run_instruction(source, gate)

    # Then presence, empty export and nonempty export have distinct outcomes
    assert (result.returncode, result.stdout, result.stderr) == (exit_code, stdout, stderr)


def test_literal_valid_input_instruction_continues_without_abort(tmp_path):
    """Valid input must not write the failure object; analysis remains untested here."""
    # Given the same retained trusted bundle used by the hosted success scenario
    source = _skill_bash("### Step 0.7 – Load Trusted Fullsend Input").replace(
        "/sandbox/workspace/.pre-script/triage-security-input.json",
        str(FIXTURE_DIR / "fullsend-report-only-trusted-input.json"))

    # When the literal input-validation instruction executes
    result = _run_instruction(source, str(tmp_path))

    # Then it continues without writing any failure or fabricated analysis result
    assert result.returncode == 0
    assert result.stdout == "Trusted triage-security input available\n"
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("result_mode", ["valid", "invalid-json", "error-only"])
def test_literal_final_validator_contract(tmp_path, result_mode):
    """Check the inline validator's exits, independently of actual agent execution."""
    # Given deliberately synthetic output, not an agent-produced analysis
    documents = {
        "valid": json.dumps(_fixture("fullsend-report-only.md")["result"]),
        "invalid-json": '{"schema_version":',
        "error-only": '{"error":"synthetic abort"}',
    }
    (tmp_path / "agent-result.json").write_text(documents[result_mode])
    source = _skill_bash("### Fullsend final output (successful analysis only)", 1)

    # When the real inline instruction validates these contract inputs
    result = _run_instruction(source, str(tmp_path))

    # Then malformed/error outputs fail rather than falling back interactively
    assert result.returncode == (0 if result_mode == "valid" else 1)
    expected = ("Final Fullsend result validated" if result_mode == "valid" else
                "ERROR: final Fullsend result failed JSON/schema validation:")
    assert expected in result.stdout
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
def test_conditional_fullsend_inputs_are_valid_and_subject_bound(source_id):
    """Every retained Fullsend unit fixture has valid input, identity and authorization."""
    # Given independent trusted-input fixtures retained for deterministic unit coverage
    bundle = _trusted_input("fullsend-eval-{}-trusted-input.json".format(source_id))

    # When the production validator checks the input directly
    pre_triage.validate_bundle(bundle)

    # Then identity and authorization belong to this scenario, not a generic sample
    subjects = {1: "TC-8001", 2: "TC-8002", 3: "TC-8003", 4: "TC-8004",
                5: "TC-8005", 8: "TC-8010", 9: "TC-8011", 11: "TC-8021",
                12: "TC-8030", 18: "TC-8001"}
    assert bundle["issue"]["key"] == subjects[source_id]
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


def test_release_instructions_bind_trusted_decisions_and_actions():
    """Delivered Fullsend procedures bind release orchestration to host decisions."""
    skill = (ROOT / 'plugins/sdlc-workflow/skills/triage-security/SKILL.md').read_text()
    operations = (ROOT / 'plugins/sdlc-workflow/skills/triage-security/jira-triage-operations.md').read_text()
    for term in ['authorization.release_decisions', 'jira_metadata.release_jira',
                 'release-epic', 'release-task']:
        assert term in skill and term in operations
    assert 'manual release decision required' in operations
    assert 'create_epic' in operations and 'create_task' in operations
    assert 'originating_cves' in operations


def test_release_fixture_matches_prefetch_schema():
    """Synthetic native release evidence uses the actual trusted input contract."""
    bundle = _trusted_input('fullsend-release-trusted-input.json')
    pre_triage.validate_bundle(bundle)
    assert bundle['issue']['key'] == 'TC-8101'
    assert bundle['authorization']['mutation_authorized'] is True
    assert {entry['family'] for entry in bundle['jira_metadata']['release_jira']} == {'2.2', '2.3'}


def _release_result(actions):
    """SYNTHETIC TEST DATA — proposed sandbox output, not actual model analysis."""
    return {'schema_version': '1', 'mode': 'mutation-authorized', 'report': {
        'issue': 'TC-8101', 'outcome': 'affected',
        'summary_markdown': '2.2.1 dedup TC-9202; 2.3.1 release/remediation proposals.',
        'evidence': [{'source': 'jira_metadata.release_jira', 'detail': 'Synthetic typed host graph'}]},
        'actions': actions}


def _release_create(kind, ref, **extra):
    """Build an explicit reviewed-family release proposal."""
    return dict(type=kind, marker='triage-security:tc-8101:' + ref, ref=ref, project='TC',
                family='2.3', version='2.3.1', labels=['release-test'],
                summary='RHTPA 2.3.1 ' + ('Release Tasks' if kind == 'release-epic' else 'CVE triage'),
                description_adf={'type': 'doc', 'version': 1, 'content': [
                    {'type': 'paragraph', 'content': [{'type': 'text', 'text': 'SYNTHETIC TEST DATA — release tracking'}]}]},
                **extra)


def test_release_fixture_executes_reuse_dedup_and_creation(recorder, monkeypatch):
    """Typed prefetch input and schema output cross the real host executor boundary."""
    bundle = _trusted_input('fullsend-release-trusted-input.json')
    pre_triage.validate_bundle(bundle)
    # Generated keys are distinct across Epic/child/remediation creation.
    created = []

    def create(**kwargs):
        created.append(kwargs)
        recorder.calls.append(('create', kwargs))
        return {'key': 'TC-' + str(9500 + len(created))}

    monkeypatch.setattr(executor._jira_mod, "create_issue", create)
    actions = [
        {'type': 'resolve-reference', 'marker': 'triage-security:existing-release',
         'ref': 'existing-release', 'issue': 'TC-9201'},
        {'type': 'field-edit', 'marker': 'triage-security:dedup-label', 'issue': 'TC-9202',
         'fields': {'labels': ['CVE-2026-8101']}},
        {'type': 'link', 'marker': 'triage-security:dedup-depend', 'link_type': 'Depend',
         'inward': 'TC-8101', 'outward': 'TC-9202'},
        {'type': 'link', 'marker': 'triage-security:dedup-related', 'link_type': 'Related',
         'inward': '{{existing-release.key}}', 'outward': 'TC-8101'},
        _release_create('release-epic', 'new-epic'),
        _release_create('release-task', 'new-release', parent='{{new-epic.key}}'),
    ]
    registry = executor.execute_plan(_release_result(actions), bundle)
    assert created[0]['issue_type'] == 'Epic'
    assert created[1]['issue_type'] == 'Task' and created[1]['parent'] == 'TC-9501'
    assert len(created) == 2  # Existing 2.2 remediation/release is not recreated.
    assert registry['existing-release']['key'] == 'TC-9201'
    assert registry['new-release']['key'] == 'TC-9502'
    assert recorder.calls[0] == ('field-edit', 'TC-9202', {'labels': ['existing-label', 'CVE-2026-8101']})
    assert ('link', 'TC-8101', 'TC-9202', 'Depend') in recorder.calls
    assert ('link', 'TC-9201', 'TC-8101', 'Related') in recorder.calls


@pytest.mark.parametrize('decision', ['missing', 'skip', 'wrong-family', 'unauthorized'])
def test_release_fixture_missing_or_withheld_permission_never_writes(decision, recorder):
    """Explicit decisions cannot be inferred from a release proposal."""
    bundle = _trusted_input('fullsend-release-trusted-input.json')
    if decision == 'missing':
        bundle['authorization'].pop('release_decisions')
    elif decision == 'skip':
        bundle['authorization']['release_decisions'] = [{'family': '2.3', 'skip': True}]
    elif decision == 'wrong-family':
        bundle['authorization']['release_decisions'][0]['family'] = '2.2'
    else:
        bundle['authorization']['mutation_authorized'] = False
    with pytest.raises(executor.ActionError):
        executor.execute_plan(_release_result([_release_create('release-epic', 'new-epic')]), bundle)
    assert recorder.calls == []


def test_release_report_only_withheld_and_manual_decisions(recorder):
    """Report-only release analysis names unresolved decisions without writes."""
    bundle = _trusted_input('fullsend-release-trusted-input.json')
    bundle['authorization'] = {'mutation_authorized': False}
    result = _release_result([{'type': 'report-only', 'marker': 'triage-security:release-report'}])
    result['mode'] = 'report-only'
    result['report']['outcome'] = 'blocked'
    result['report']['summary_markdown'] = '2.2.1 release references TC-9200/TC-9201, dedup TC-9202; 2.3 manual release decision required. Creation, links and label edits withheld.'
    executor.execute_plan(result, bundle)
    assert recorder.calls == []


def test_release_dedup_instructions_preserve_fallback_and_dependency_bump():
    """Instructions keep released match/fallback/nonmatch and dependency-bump semantics."""
    operations = (ROOT / 'plugins/sdlc-workflow/skills/triage-security/jira-triage-operations.md').read_text()
    assert 'no configured field means skip dedup' in operations
    assert 'present nonmatching component never authorizes a summary fallback' in operations
    templates = (ROOT / 'plugins/sdlc-workflow/skills/triage-security/remediation-templates.md').read_text()
    assert 'dependency bump uses the' in templates
    assert 'followed by its downstream' in templates


def test_release_output_strips_unexpected_properties_before_execution(tmp_path, recorder):
    """The actual host stripper retains release fields while removing injected extras."""
    result = _release_result([_release_create('release-epic', 'new-epic')])
    result['unexpected'] = 'ADVERSARIAL TEST FIXTURE — unauthorized output'
    result['actions'][0]['unexpected'] = 'ADVERSARIAL TEST FIXTURE — unauthorized action'
    path = tmp_path / 'result.json'
    path.write_text(json.dumps(result))
    process = subprocess.run(['python3', str(SCRIPT_DIR / 'strip_extra_properties.py'), str(path),
                              str(SCRIPT_DIR.parent / 'schemas/triage-security-result.schema.json')],
                             capture_output=True, text=True, check=False)
    assert process.returncode == 0
    cleaned = json.loads(path.read_text())
    assert 'unexpected' not in cleaned and 'unexpected' not in cleaned['actions'][0]
    assert cleaned['actions'][0]['family'] == '2.3' and cleaned['actions'][0]['version'] == '2.3.1'
    executor.execute_plan(cleaned, _trusted_input('fullsend-release-trusted-input.json'))
    assert recorder.calls[0][1]['issue_type'] == 'Epic'


def test_release_dependency_bump_and_propagation_use_existing_task_action(recorder, monkeypatch):
    """Release parents, source dependency bumps and downstream propagation form one ordered plan."""
    created = []

    def create(**kwargs):
        created.append(kwargs)
        return {'key': 'TC-' + str(9600 + len(created))}

    monkeypatch.setattr(executor._jira_mod, 'create_issue', create)
    actions = [_release_create('release-epic', 'new-epic'),
               _release_create('release-task', 'new-release', parent='{{new-epic.key}}')]
    for ref, description in [('bump', 'SYNTHETIC TEST DATA — bump source dependency to upstream fixed version'),
                             ('propagation', 'SYNTHETIC TEST DATA — propagate merged source reference downstream')]:
        actions.extend([
            {'type': 'remediation-task', 'marker': 'triage-security:' + ref, 'ref': ref,
             'project': 'TC', 'summary': description, 'labels': ['CVE-2026-8101'],
             'description_adf': {'type': 'doc', 'version': 1, 'content': [
                 {'type': 'paragraph', 'content': [{'type': 'text', 'text': description}]}]}},
            {'type': 'link', 'marker': 'triage-security:' + ref + ':depend', 'link_type': 'Depend',
             'inward': 'TC-8101', 'outward': '{{' + ref + '.key}}'},
            {'type': 'link', 'marker': 'triage-security:' + ref + ':release', 'link_type': 'Blocks',
             'inward': '{{' + ref + '.key}}', 'outward': '{{new-release.key}}'},
        ])
    actions.append({'type': 'link', 'marker': 'triage-security:propagation-blocked', 'link_type': 'Blocks',
                    'inward': '{{bump.key}}', 'outward': '{{propagation.key}}'})
    registry = executor.execute_plan(_release_result(actions), _trusted_input('fullsend-release-trusted-input.json'))
    assert [item['issue_type'] for item in created] == ['Epic', 'Task', 'Task', 'Task']
    assert created[1]['parent'] == 'TC-9601'
    assert registry['bump']['key'] == 'TC-9603' and registry['propagation']['key'] == 'TC-9604'
    assert ('link', 'TC-9603', 'TC-9604', 'Blocks') in recorder.calls
    assert ('link', 'TC-9603', 'TC-9602', 'Blocks') in recorder.calls
    assert ('link', 'TC-9604', 'TC-9602', 'Blocks') in recorder.calls


def test_release_partial_retry_reuses_prefetched_hierarchy_and_repairs_digest(recorder):
    """A refreshed trusted input safely rehydrates both created release references."""
    bundle = _trusted_input('fullsend-release-trusted-input.json')
    entry = bundle['jira_metadata']['release_jira'][1]
    for kind, bucket, key, parent in [('release-epic', 'epics', 'TC-9501', None),
                                    ('release-task', 'tasks', 'TC-9502', 'TC-9501')]:
        action = _release_create(kind, bucket)
        snapshot = {'key': key, 'summary': action['summary'], 'issue_type': 'Epic' if parent is None else 'Task',
                    'status': 'New', 'description': action['description_adf'],
                    'labels': ['ai-generated-jira'], 'comments': [], 'links': []}
        if parent:
            snapshot['parent'] = parent
        entry[bucket] = [snapshot]
    pre_triage.validate_bundle(bundle)
    actions = [_release_create('release-epic', 'new-epic'),
               _release_create('release-task', 'new-release', parent='{{new-epic.key}}'),
               {'type': 'link', 'marker': 'triage-security:retry-related', 'link_type': 'Related',
                'inward': '{{new-release.key}}', 'outward': 'TC-8101'}]
    registry = executor.execute_plan(_release_result(actions), bundle)
    assert registry['new-release']['key'] == 'TC-9502'
    assert [call[0] for call in recorder.calls] == ['get-issue', 'digest', 'get-issue', 'digest', 'link']
