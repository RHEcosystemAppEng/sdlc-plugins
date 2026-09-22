#!/usr/bin/env python3
"""Tests for the trusted triage-security evidence transformer."""

import io
import json
import os
import subprocess
import sys
import time
from urllib.error import HTTPError

import pytest
from jsonschema import validate


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import pre_triage_security


def test_parse_security_configuration_extracts_required_runner_values():
    """A complete project configuration becomes the sandbox configuration object."""
    # Given a target project's populated Security Configuration
    claude_md = """# Project Configuration

## Jira Configuration

- Project key: TC

## Security Configuration

### Product Lifecycle

- Product pages URL: https://example.com/lifecycle
- Jira version prefix: PRODUCT
- Vulnerability issue type ID: 10016
- Component label pattern: pscomponent:
- ProdSec Jira account ID: account-1

### Version Streams

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 1.0.x | release-repo | /repos/release | docs/matrix.md |

### Source Repositories

| Repository | URL | Deployment Context |
|---|---|---|
| component | https://github.com/org/component | customer-shipped |
"""

    # When the runner parses the configuration before fetching evidence
    configuration = pre_triage_security.parse_security_configuration(claude_md)

    # Then all schema-required values and optional security settings are retained
    assert configuration == {
        "project_key": "TC",
        "jira_version_prefix": "PRODUCT",
        "vulnerability_issue_type_id": "10016",
        "component_label_pattern": "pscomponent:",
        "prodsec_account_id": "account-1",
        "version_streams": [{
            "name": "1.0.x",
            "matrix_path": "docs/matrix.md",
            "release_repository": "release-repo",
        }],
        "source_repositories": [{
            "name": "component",
            "url": "https://github.com/org/component",
            "deployment_context": "customer-shipped",
        }],
    }


def test_collect_bundle_escapes_configured_values_in_jql_literals(tmp_path, monkeypatch):
    """JQL searches preserve quote and backslash-containing configured values."""
    # Given configured project and CVE values containing JQL metacharacters
    project_key = 'TC"\\OPS'
    cve_id = 'CVE-2026-"\\12345'
    issue = {
        "key": "TC-42",
        "fields": {
            "summary": "security issue",
            "labels": [],
            "comment": {"comments": []},
            "issuelinks": [],
            "customfield_12345": "component",
        },
    }
    configuration = {
        "project_key": project_key,
        "vulnerability_issue_type_id": "10016",
        "upstream_affected_component_field": "customfield_12345",
    }
    searched_jql = []
    (tmp_path / "CLAUDE.md").write_text("# Project Configuration\n")

    def jira_client(command, *arguments):
        """Return minimal runner evidence while retaining each JQL search."""
        if command == "get_issue":
            return issue
        if command == "get_remote_links":
            return []
        if command == "get_versions":
            return []
        if command == "search_jql":
            searched_jql.append(arguments[arguments.index("--jql") + 1])
            return {"issues": []}
        raise AssertionError("unexpected Jira command: {}".format(command))

    monkeypatch.setattr(
        pre_triage_security,
        "_runner_configuration",
        lambda _content, _root: (configuration, "https://example.com/lifecycle", [], {}),
    )
    monkeypatch.setattr(pre_triage_security, "_jira_client", jira_client)
    monkeypatch.setattr(pre_triage_security, "extract_cve_id", lambda _issue: cve_id)
    monkeypatch.setattr(pre_triage_security, "_fetch_url", lambda _url, **_kwargs: {})
    monkeypatch.setattr(pre_triage_security, "build_bundle", lambda **bundle: bundle)

    # When the trusted runner builds its JQL searches
    pre_triage_security.collect_bundle("TC-42", tmp_path)

    # Then every quoted configured value is escaped before interpolation
    escaped_project_key = 'TC\\"\\\\OPS'
    escaped_cve_id = 'CVE-2026-\\"\\\\12345'
    assert searched_jql == [
        'project = "{}" AND labels = "{}" AND issuetype = 10016 AND key != "TC-42"'.format(
            escaped_project_key, escaped_cve_id),
        'project = "{}" AND issuetype = 10016 AND cf[12345] ~ "component" AND key != "TC-42"'.format(
            escaped_project_key),
        'project = "{}" AND issuetype = Task AND labels = "security-preemptive" '
        'AND labels = "{}" ORDER BY created DESC'.format(escaped_project_key, escaped_cve_id),
    ]


def test_pre_triage_script_rejects_missing_poller_work_item_url():
    """The runner fails before collection when the poller supplied no work item."""
    # Given runner credentials but no work item dispatched by the poller
    script = os.path.join(SCRIPT_DIR, "pre-triage-security.sh")
    environment = {
        "PATH": os.environ["PATH"],
        "JIRA_SERVER_URL": "https://jira.example.com",
        "JIRA_EMAIL": "runner@example.com",
        "JIRA_API_TOKEN": "token",
    }

    # When the trusted pre-script starts
    result = subprocess.run(["bash", script], env=environment, capture_output=True, text=True)

    # Then it rejects the missing poller contract before creating a bundle
    assert result.returncode != 0
    assert "FULLSEND_WORK_ITEM_URL" in result.stderr


def test_pre_triage_script_rejects_missing_runner_credentials():
    """The runner fails before collection when its Jira credential is absent."""
    # Given a poller work item but no Jira API token on the trusted runner
    script = os.path.join(SCRIPT_DIR, "pre-triage-security.sh")
    environment = {
        "PATH": os.environ["PATH"],
        "FULLSEND_WORK_ITEM_URL": "https://jira.example.com/browse/TC-42",
        "JIRA_SERVER_URL": "https://jira.example.com",
        "JIRA_EMAIL": "runner@example.com",
    }

    # When the trusted pre-script starts
    result = subprocess.run(["bash", script], env=environment, capture_output=True, text=True)

    # Then no collection runs without the credential required by jira-client.py
    assert result.returncode != 0
    assert "JIRA_API_TOKEN" in result.stderr


def test_pre_triage_script_isolates_bundles_per_fullsend_run(tmp_path, request):
    """Separate Fullsend runs publish isolated bundles through their own handoff paths."""
    # Given a harmless collector and two poller-dispatched issues on one runner
    script = os.path.join(SCRIPT_DIR, "pre-triage-security.sh")
    project_root = tmp_path / "project"
    project_root.mkdir()
    (project_root / "CLAUDE.md").write_text("# Project Configuration\n")
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    collector = fake_bin / "python3"
    collector.write_text(
        "#!/usr/bin/env bash\n"
        "touch \"${COLLECTOR_READY_DIR}/$3\"\n"
        "while [[ ! -f \"${COLLECTOR_RELEASE}\" ]]; do sleep 0.01; done\n"
        "printf '{\"issue\":\"%s\"}\\n' \"$3\"\n"
    )
    collector.chmod(0o755)
    shared_output = tmp_path / "shared"
    ready_directory = tmp_path / "ready"
    ready_directory.mkdir()
    release_file = tmp_path / "release"
    processes = []

    def release_collectors():
        release_file.touch()
        for process in processes:
            if process.poll() is None:
                process.terminate()
                process.communicate(timeout=5)

    request.addfinalizer(release_collectors)

    def environment_for(issue_key, run_directory):
        return {
            "PATH": "{}{}{}".format(fake_bin, os.pathsep, os.environ["PATH"]),
            "FULLSEND_WORK_ITEM_URL": "https://jira.example.com/browse/{}".format(issue_key),
            "FULLSEND_PROJECT_ROOT": str(project_root),
            "FULLSEND_RUN_DIR": str(run_directory),
            "PRE_DIR": str(shared_output),
            "COLLECTOR_READY_DIR": str(ready_directory),
            "COLLECTOR_RELEASE": str(release_file),
            "JIRA_SERVER_URL": "https://jira.example.com",
            "JIRA_EMAIL": "runner@example.com",
            "JIRA_API_TOKEN": "token",
        }

    first_run = tmp_path / "run-one"
    second_run = tmp_path / "run-two"

    # When two runs collect their dispatched issues concurrently
    first_process = subprocess.Popen(
        ["bash", script], env=environment_for("TC-42", first_run), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    processes.append(first_process)
    second_process = subprocess.Popen(
        ["bash", script], env=environment_for("TC-43", second_run), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    processes.append(second_process)
    first_output = first_run / "pre" / "triage-security-input.json"
    second_output = second_run / "pre" / "triage-security-input.json"
    deadline = time.monotonic() + 5
    while len(list(ready_directory.iterdir())) < 2 and time.monotonic() < deadline:
        time.sleep(0.01)

    # Then neither blocked collector can expose a partial final bundle
    assert len(list(ready_directory.iterdir())) == 2
    assert not first_output.exists()
    assert not second_output.exists()
    release_file.touch()
    first_stdout, first_stderr = first_process.communicate(timeout=5)
    second_stdout, second_stderr = second_process.communicate(timeout=5)

    # And both bundles are separately and atomically published for their run
    assert first_process.returncode == 0, first_stderr
    assert second_process.returncode == 0, second_stderr
    assert first_output.read_text() == '{"issue":"TC-42"}\n'
    assert second_output.read_text() == '{"issue":"TC-43"}\n'
    assert sorted(path.name for path in first_output.parent.iterdir()) == ["triage-security-input.json"]
    assert sorted(path.name for path in second_output.parent.iterdir()) == ["triage-security-input.json"]
    assert not shared_output.exists()
    with open(os.path.join(SCRIPT_DIR, "..", "..", "..", "harness", "triage-security.yaml")) as harness_file:
        assert "src: ${FULLSEND_RUN_DIR}/pre/triage-security-input.json" in harness_file.read()


def test_normalize_issue_rejects_missing_reporter_metadata():
    """A Jira response without reporter evidence cannot enter the sandbox bundle."""
    # Given a malformed Jira issue response without its required reporter
    issue = {"key": "TC-42", "fields": {
        "summary": "CVE-2026-12345", "description": {}, "status": {"name": "New"},
        "labels": [], "versions": [], "comment": {"comments": []},
    }}

    # When the runner normalizes the issue for the schema
    # Then it fails loudly rather than emit incomplete audit evidence
    with pytest.raises(pre_triage_security.EvidenceError, match="reporter"):
        pre_triage_security.normalize_issue(issue)


def test_normalize_remote_links_rejects_missing_evidence():
    """A security issue without remote-link evidence is rejected before sandbox creation."""
    # Given a Jira issue whose required remote-link prefetch returned no links
    # When the runner normalizes the evidence
    # Then it rejects the incomplete input rather than silently continue
    with pytest.raises(pre_triage_security.EvidenceError, match="remote_links"):
        pre_triage_security.normalize_remote_links([])


def test_matrix_validation_rejects_non_retag_without_pinned_commit():
    """A released matrix row without a pinned source commit is rejected."""
    # Given a non-retag release row with no source commit evidence
    matrix = {"streams": [{
        "name": "1.0.x", "matrix_source": "matrix", "rows": [{
            "version": "1.0.0", "source_commits": {}, "retag_of": None,
        }],
    }]}

    # When the runner validates the matrix before reading source repositories
    # Then it fails instead of asking the sandbox to infer a ref
    with pytest.raises(pre_triage_security.EvidenceError, match="no source commits"):
        pre_triage_security._validate_matrix(matrix)


def test_source_evidence_accepts_rpm_system_package_reads():
    """RPM lock-file evidence is retained for system-package CVE analysis."""
    # Given read-only git-show evidence for a released and development RPM lock file
    evidence = {"lock_files": [{
        "repository": "component", "ref": "abc1234", "path": "rpms.lock.yaml",
        "command": "git show abc1234:rpms.lock.yaml", "content": "openssl: 3.0.7",
    }], "development_streams": [{
        "repository": "component", "ref": "main", "path": "rpms.lock.yaml",
        "command": "git show main:rpms.lock.yaml", "content": "openssl: 3.0.8",
    }]}

    # When the runner validates the system-package evidence
    result = pre_triage_security._validate_source_evidence(evidence)

    # Then it preserves the RPM reads for the sandbox rather than assuming Cargo or npm
    assert result["lock_files"][0]["path"] == "rpms.lock.yaml"
    assert result["development_streams"][0]["content"] == "openssl: 3.0.8"


def test_action_markers_collect_prior_trusted_runner_actions():
    """Existing triage action markers are preserved for idempotency decisions."""
    # Given comment history containing a prior trusted-runner action marker
    issue = {"fields": {"comment": {"comments": [{"body": {
        "type": "doc", "content": [{"type": "text", "text": "triage-security:created-remediation"}],
    }}]}}}

    # When idempotency evidence is extracted
    # Then the sandbox receives the prior action marker exactly once
    assert pre_triage_security._action_markers(issue) == ["triage-security:created-remediation"]


def test_parse_security_matrix_preserves_rows_retags_and_ecosystem_commands():
    """A matrix retains pinned commits, retags, and lock-file inspection metadata."""
    # Given a configured stream matrix with a source-dependency and RPM mapping
    matrix_markdown = """## Supportability Matrix

| PRODUCT Version | Build | component | Notes |
|---|---|---|---|
| 1.0.0 | build-1 | `abc1234` | |
| 1.0.1 | build-2 | `abc1234` | retag of 1.0.0 |

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | component | `Cargo.lock` | grep library | main |
| RPM | component | `rpms.lock.yaml` | grep library | main |
"""

    # When parsing the matrix on the trusted runner
    matrix, mappings = pre_triage_security.parse_security_matrix(
        stream_name="1.0.x", matrix_path="docs/matrix.md", content=matrix_markdown)

    # Then the sandbox receives both product rows and all configured read commands
    assert matrix == {
        "name": "1.0.x",
        "matrix_source": matrix_markdown,
        "rows": [
            {"version": "1.0.0", "source_commits": {"component": "abc1234"}, "retag_of": None},
            {"version": "1.0.1", "source_commits": {"component": "abc1234"}, "retag_of": "1.0.0"},
        ],
    }
    assert mappings == [
        {"ecosystem": "Cargo", "repository": "component", "lock_file": "Cargo.lock", "check_command": "grep library", "upstream_branch": "main"},
        {"ecosystem": "RPM", "repository": "component", "lock_file": "rpms.lock.yaml", "check_command": "grep library", "upstream_branch": "main"},
    ]


def _complete_bundle():
    """Build complete source-dependency evidence for bundle validation tests."""
    # Given a CVE issue and all evidence gathered by the trusted runner
    issue = {
        "key": "TC-42",
        "fields": {
            "summary": "CVE-2026-12345 component: library issue",
            "description": {"type": "doc", "content": []},
            "status": {"name": "New"},
            "labels": ["CVE-2026-12345", "pscomponent:org/component"],
            "versions": [{"id": "1", "name": "1.0", "released": False, "self": "https://jira.example.com/version/1"}],
            "reporter": {"accountId": "reporter-1", "displayName": "Reporter"},
            "comment": {"comments": []},
            "issuelinks": [],
        },
    }
    configuration = {
        "project_key": "TC",
        "jira_version_prefix": "PRODUCT",
        "vulnerability_issue_type_id": "10016",
        "component_label_pattern": "pscomponent:",
        "version_streams": [{
            "name": "1.0.x",
            "matrix_path": "security-matrix.md",
            "release_repository": "release-repo",
        }],
        "source_repositories": [{
            "name": "component",
            "url": "https://github.com/org/component",
            "deployment_context": "upstream",
        }],
    }
    external_evidence = {
        name: {
            "source_url": url,
            "retrieved_at": "2026-09-21T12:00:00Z",
            "status": 200,
            "body": {"id": "CVE-2026-12345"},
        }
        for name, url in {
            "mitre": "https://cveawg.mitre.org/api/cve/CVE-2026-12345",
            "osv": "https://api.osv.dev/v1/vulns/CVE-2026-12345",
            "lifecycle": "https://example.com/lifecycle",
        }.items()
    }
    matrix = {"streams": [{
        "name": "1.0.x",
        "matrix_source": "security-matrix.md",
        "rows": [{"version": "1.0", "source_commits": {"component": "abc1234"}, "retag_of": None}],
    }]}
    source_evidence = {
        "lock_files": [{
            "repository": "component",
            "ref": "abc1234",
            "path": "Cargo.lock",
            "command": "git show abc1234:Cargo.lock",
            "content": 'name = "library"\\nversion = "1.2.3"',
        }],
        "development_streams": [{
            "repository": "component",
            "ref": "main",
            "path": "Cargo.lock",
            "command": "git show main:Cargo.lock",
            "content": 'name = "library"\\nversion = "1.2.3"',
        }],
    }

    # When transforming the runner evidence for the sandbox
    bundle = pre_triage_security.build_bundle(
        issue=issue,
        remote_links=[{"object": {"url": "https://github.com/org/component/pull/1", "title": "Fix"}}],
        configuration=configuration,
        external_evidence=external_evidence,
        matrix=matrix,
        source_evidence=source_evidence,
        jira_metadata={"versions": [], "sibling_searches": [], "related_issues": []},
        idempotency={"action_markers": [], "existing_remediation": []},
        mutation_authorized=False,
    )

    # Then the exact sandbox contract accepts the resulting bundle
    with open(os.path.join(SCRIPT_DIR, "..", "schemas", "triage-security-input.schema.json")) as schema_file:
        schema = json.load(schema_file)
    validate(instance=bundle, schema=schema)
    assert bundle["issue"]["key"] == "TC-42"
    assert bundle["issue"]["versions"] == [{"id": "1", "name": "1.0", "released": False}]
    assert bundle["remote_links"] == [{"url": "https://github.com/org/component/pull/1", "title": "Fix"}]
    return bundle


def test_build_bundle_accepts_complete_source_dependency_evidence():
    """Complete source-dependency evidence produces schema-valid sandbox input."""
    assert _complete_bundle()["issue"]["key"] == "TC-42"


def test_validate_bundle_rejects_malformed_uri():
    """A malformed remote-link URL cannot enter the sandbox bundle."""
    # Given an otherwise valid bundle with an invalid URI-format field
    bundle = _complete_bundle()
    bundle["remote_links"][0]["url"] = "not a URL"

    # When the bundle is schema-validated before the sandbox runs
    # Then format validation rejects the malformed URL
    with pytest.raises(pre_triage_security.EvidenceError, match="triage-security input validation failed"):
        pre_triage_security.validate_bundle(bundle)


def test_validate_bundle_rejects_malformed_retrieval_timestamp():
    """A malformed evidence retrieval timestamp cannot enter the sandbox bundle."""
    # Given an otherwise valid bundle with an invalid date-time-format field
    bundle = _complete_bundle()
    bundle["external_evidence"]["mitre"]["retrieved_at"] = "not-a-timestamp"

    # When the bundle is schema-validated before the sandbox runs
    # Then format validation rejects the malformed timestamp
    with pytest.raises(pre_triage_security.EvidenceError, match="triage-security input validation failed"):
        pre_triage_security.validate_bundle(bundle)


def _http_error_opener(status, body=b'{"message": "gone"}'):
    """Return a urlopen replacement that raises an HTTPError with the given status."""
    def opener(url, timeout=30):
        raise HTTPError(url, status, "error", {}, io.BytesIO(body))
    return opener


def test_fetch_url_records_missing_external_evidence(monkeypatch):
    """A 404 from an incomplete evidence source is recorded, not fatal, when allowed."""
    # Given an OSV/MITRE source that does not track this CVE (a routine 404)
    monkeypatch.setattr(pre_triage_security, "urlopen", _http_error_opener(404))

    # When the runner fetches it as tolerable-missing evidence
    evidence = pre_triage_security._fetch_url(
        "https://api.osv.dev/v1/vulns/CVE-2026-12345", allow_missing=True)

    # Then the 404 is preserved as evidence rather than aborting the whole bundle
    assert evidence["status"] == 404
    assert evidence["body"] == {"message": "gone"}

    # And a 404 on required (non-missing-tolerant) evidence still fails loudly
    with pytest.raises(pre_triage_security.EvidenceError, match="HTTP 404"):
        pre_triage_security._fetch_url("https://api.osv.dev/v1/vulns/CVE-2026-12345")

    # And any non-404 failure stays fatal even when misses are tolerated
    monkeypatch.setattr(pre_triage_security, "urlopen", _http_error_opener(500))
    with pytest.raises(pre_triage_security.EvidenceError, match="HTTP 500"):
        pre_triage_security._fetch_url(
            "https://api.osv.dev/v1/vulns/CVE-2026-12345", allow_missing=True)


def test_jira_client_decodes_empty_collection(monkeypatch):
    """An empty Jira collection is decoded as [] rather than a misleading JSON error."""
    # Given jira-client.py that now prints an empty collection as valid JSON
    class _Result:
        stdout = "[]\n"

    monkeypatch.setattr(pre_triage_security.subprocess, "run", lambda *a, **k: _Result())

    # When the runner reads a command with no results (e.g. get_versions)
    # Then it returns the empty list, not an "invalid JSON" evidence error
    assert pre_triage_security._jira_client("get_versions", "TC") == []


def test_parse_security_configuration_defaults_blank_deployment_context():
    """A present-but-blank Deployment Context cell falls back to 'upstream'."""
    # Given a Source Repositories table whose Deployment Context cell is left blank
    claude_md = """# Project Configuration

## Jira Configuration

- Project key: TC

## Security Configuration

### Product Lifecycle

- Product pages URL: https://example.com/lifecycle
- Jira version prefix: PRODUCT
- Vulnerability issue type ID: 10016
- Component label pattern: pscomponent:

### Version Streams

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 1.0.x | release-repo | /repos/release | docs/matrix.md |

### Source Repositories

| Repository | URL | Deployment Context |
|---|---|---|
| component | https://github.com/org/component |  |
"""

    # When the runner parses the configuration
    configuration = pre_triage_security.parse_security_configuration(claude_md)

    # Then the blank cell defaults instead of being rejected as an incomplete row
    assert configuration["source_repositories"] == [{
        "name": "component",
        "url": "https://github.com/org/component",
        "deployment_context": "upstream",
    }]


def test_parse_security_configuration_rejects_blank_repository():
    """A blank required Source Repositories cell still fails loudly."""
    # Given a Source Repositories table missing the Repository value
    claude_md = """# Project Configuration

## Jira Configuration

- Project key: TC

## Security Configuration

### Product Lifecycle

- Product pages URL: https://example.com/lifecycle
- Jira version prefix: PRODUCT
- Vulnerability issue type ID: 10016
- Component label pattern: pscomponent:

### Version Streams

| Stream | Konflux Release Repo | Local Path | Security Matrix Path |
|---|---|---|---|
| 1.0.x | release-repo | /repos/release | docs/matrix.md |

### Source Repositories

| Repository | URL | Deployment Context |
|---|---|---|
|  | https://github.com/org/component | upstream |
"""

    # When the runner parses the configuration
    # Then it rejects the row rather than emit a nameless source repository
    with pytest.raises(pre_triage_security.EvidenceError, match="Repository or URL"):
        pre_triage_security.parse_security_configuration(claude_md)


def _minimal_jira_client():
    """Return a _jira_client stub sufficient to reach collect_bundle's stream loop."""
    def jira_client(command, *arguments):
        if command == "get_issue":
            return {"key": "TC-42", "fields": {}}
        if command in ("get_remote_links", "get_versions"):
            return []
        if command == "search_jql":
            return {"issues": []}
        raise AssertionError("unexpected Jira command: {}".format(command))
    return jira_client


def test_collect_bundle_reports_missing_version_streams_column(tmp_path, monkeypatch):
    """A Version Streams table missing a column raises a clear error, not a traceback."""
    # Given a runner configuration whose stream row lacks the Local Path column
    (tmp_path / "CLAUDE.md").write_text("# Project Configuration\n")
    configuration = {"project_key": "TC", "vulnerability_issue_type_id": "10016"}
    stream_rows = [{"Stream": "1.0.x", "Security Matrix Path": "docs/matrix.md"}]
    monkeypatch.setattr(
        pre_triage_security, "_runner_configuration",
        lambda _content, _root: (configuration, "https://example.com/lifecycle", stream_rows, {}))
    monkeypatch.setattr(pre_triage_security, "_jira_client", _minimal_jira_client())
    monkeypatch.setattr(pre_triage_security, "extract_cve_id", lambda _issue: "CVE-2026-12345")
    monkeypatch.setattr(pre_triage_security, "_fetch_url", lambda *a, **k: {})

    # When the runner reaches the stream loop
    # Then the missing column surfaces as an EvidenceError naming it
    with pytest.raises(pre_triage_security.EvidenceError, match="Local Path"):
        pre_triage_security.collect_bundle("TC-42", tmp_path)


def test_related_issue_handles_null_comment_field():
    """A related issue whose comment field is JSON null yields no comments, not a crash."""
    # Given a related issue with restricted comment visibility (comment field is null)
    issue = {"key": "TC-9", "fields": {"status": {"name": "New"}, "comment": None}}

    # When the runner normalizes it for audit and idempotency
    # Then the null comment field degrades to an empty list rather than raising
    assert pre_triage_security._related_issue(issue)["comments"] == []
    assert pre_triage_security._action_markers(issue) == []


def test_collect_bundle_rejects_malformed_issue_key(tmp_path):
    """A non-conforming issue key is rejected before any JQL is constructed."""
    # Given a poller-supplied value that is not a valid Jira issue key
    (tmp_path / "CLAUDE.md").write_text("# Project Configuration\n")

    # When the runner begins collection
    # Then it fails on the key before interpolating it into any JQL
    with pytest.raises(pre_triage_security.EvidenceError, match="issue_key"):
        pre_triage_security.collect_bundle("not-a-key", tmp_path)
