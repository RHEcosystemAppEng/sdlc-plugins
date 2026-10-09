#!/usr/bin/env python3
"""Tests for the trusted triage-security evidence transformer."""

import io
import json
import os
import subprocess
import sys
import time
from unittest.mock import MagicMock
from urllib.error import HTTPError
from urllib.request import Request

import pytest
from jsonschema import FormatChecker, validate


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import pre_triage_security


# jsonschema only enforces uri/date-time formats when the jsonschema[format]
# extra is installed (rfc3987 / rfc3339-validator). validate_bundle now fails
# closed without it, so format-dependent tests are skipped rather than failed on
# an environment lacking the extra; CI installs it and exercises them fully.
_HAS_FORMAT_EXTRA = all(
    fmt in FormatChecker().checkers for fmt in pre_triage_security._REQUIRED_FORMATS)
requires_format_extra = pytest.mark.skipif(
    not _HAS_FORMAT_EXTRA,
    reason="requires jsonschema[format] for uri/date-time format enforcement")


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
    """Matrix parsing normalizes source refs and accepts empty branch cells."""
    # Given a configured stream matrix with populated and empty upstream branches
    matrix_markdown = """## Supportability Matrix

| PRODUCT Version | Build | component | Notes |
|---|---|---|---|
| 1.0.0 | build-1 | `abc1234` (retag) | |
| 1.0.1 | build-2 | `abc1234` | retag of 1.0.0 |

## Ecosystem Mappings

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| Cargo | component | `Cargo.lock` | grep library | `release/0.6.z` (pending re-point to 0.7.z) |
| RPM | component | `rpms.lock.yaml` | grep library | main |
| Go | component | go.sum | grep library | |
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
        {"ecosystem": "Cargo", "repository": "component", "lock_file": "Cargo.lock", "check_command": "grep library", "upstream_branch": "release/0.6.z"},
        {"ecosystem": "RPM", "repository": "component", "lock_file": "rpms.lock.yaml", "check_command": "grep library", "upstream_branch": "main"},
        {"ecosystem": "Go", "repository": "component", "lock_file": "go.sum", "check_command": "grep library", "upstream_branch": ""},
    ]


@pytest.mark.parametrize("cell, expected", [
    ("`release/0.6.z` (pending re-point to 0.7.z)", "release/0.6.z"),
    ("release/0.5.z", "release/0.5.z"),
    ("`main` — current stable branch", "main"),
    ("(pending re-point) release/0.6.z", "release/0.6.z"),
    ("N/A - see release/0.6.z", "release/0.6.z"),
])
def test_ref_token_extracts_branch_from_annotated_matrix_cells(cell, expected):
    """A matrix branch cell yields its ref token despite surrounding prose."""
    assert pre_triage_security._ref_token(cell) == expected


@pytest.mark.parametrize("cell", ["", None, "   ", "``"])
def test_ref_token_returns_empty_for_blank_cells(cell):
    """A blank upstream-branch cell normalizes to an empty ref."""
    assert pre_triage_security._ref_token(cell) == ""


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


@requires_format_extra
def test_build_bundle_accepts_complete_source_dependency_evidence():
    """Complete source-dependency evidence produces schema-valid sandbox input."""
    assert _complete_bundle()["issue"]["key"] == "TC-42"


@requires_format_extra
def test_validate_bundle_rejects_malformed_uri():
    """A malformed remote-link URL cannot enter the sandbox bundle."""
    # Given an otherwise valid bundle with an invalid URI-format field
    bundle = _complete_bundle()
    bundle["remote_links"][0]["url"] = "not a URL"

    # When the bundle is schema-validated before the sandbox runs
    # Then format validation rejects the malformed URL
    with pytest.raises(pre_triage_security.EvidenceError, match="triage-security input validation failed"):
        pre_triage_security.validate_bundle(bundle)


@requires_format_extra
def test_validate_bundle_rejects_malformed_retrieval_timestamp():
    """A malformed evidence retrieval timestamp cannot enter the sandbox bundle."""
    # Given an otherwise valid bundle with an invalid date-time-format field
    bundle = _complete_bundle()
    bundle["external_evidence"]["mitre"]["retrieved_at"] = "not-a-timestamp"

    # When the bundle is schema-validated before the sandbox runs
    # Then format validation rejects the malformed timestamp
    with pytest.raises(pre_triage_security.EvidenceError, match="triage-security input validation failed"):
        pre_triage_security.validate_bundle(bundle)


def test_validate_bundle_fails_closed_without_format_extra(monkeypatch):
    """A runner missing jsonschema[format] aborts instead of skipping format checks."""
    # Given a FormatChecker with no uri/date-time checkers (jsonschema[format] absent)
    class _NoFormatChecker:
        checkers = {"regex": None}

    monkeypatch.setattr(pre_triage_security, "FormatChecker", _NoFormatChecker)

    # When a bundle is validated on that misprovisioned runner
    # Then it fails closed, naming the missing extra, rather than validating silently
    with pytest.raises(pre_triage_security.EvidenceError, match=r"jsonschema\[format\]"):
        pre_triage_security.validate_bundle({"any": "bundle"})


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


def test_fetch_url_sends_custom_user_agent(monkeypatch):
    """Evidence fetches send the configured User-Agent on a urllib Request."""
    # Given a successful HTTP response and an opener that records its request
    response = MagicMock()
    response.__enter__.return_value = response
    response.status = 200
    response.read.return_value = b'{"evidence": "ok"}'
    calls = []

    def open_url(request, timeout):
        calls.append((request, timeout))
        return response

    monkeypatch.setattr(pre_triage_security, "urlopen", open_url)

    # When evidence is fetched
    evidence = pre_triage_security._fetch_url("https://access.redhat.com/advisory")

    # Then urllib receives the custom User-Agent and the response is decoded
    request, timeout = calls[0]
    assert isinstance(request, Request)
    assert request.full_url == "https://access.redhat.com/advisory"
    assert request.get_header("User-agent") == pre_triage_security._EVIDENCE_USER_AGENT
    assert timeout == 30
    assert evidence["body"] == {"evidence": "ok"}


def _init_source_repository(path):
    """Create a clean source repository for read-only git evidence tests."""
    subprocess.run(
        ["git", "-C", str(path), "init", "--quiet", "--initial-branch=main"],
        check=True,
    )
    for key, value in (("user.name", "Test User"), ("user.email", "test@example.com")):
        subprocess.run(["git", "-C", str(path), "config", key, value], check=True)
    (path / "README.md").write_text("source evidence\n")
    subprocess.run(["git", "-C", str(path), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "--quiet", "-m", "fixture"], check=True)
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def test_resolve_ref_prefers_remotes_and_returns_none_when_missing(tmp_path):
    """Bare branches resolve to remote refs in precedence order, or None."""
    # Given a source repository with the same branch on several remotes
    repository = tmp_path / "source"
    repository.mkdir()
    commit = _init_source_repository(repository)
    branch = "release/0.5.z"
    for remote in ("backup-z", "backup-a", "origin", "upstream"):
        subprocess.run([
            "git", "-C", str(repository), "update-ref",
            "refs/remotes/{}/{}".format(remote, branch), commit,
        ], check=True)

    # When the bare branch is resolved with every remote available
    assert pre_triage_security._resolve_ref(repository, "main") == "main"
    assert pre_triage_security._resolve_ref(repository, branch) == (
        "refs/remotes/upstream/{}".format(branch))

    # Then origin wins after upstream is removed, followed by the first other remote
    subprocess.run([
        "git", "-C", str(repository), "update-ref", "-d",
        "refs/remotes/upstream/{}".format(branch),
    ], check=True)
    assert pre_triage_security._resolve_ref(repository, branch) == (
        "refs/remotes/origin/{}".format(branch))
    subprocess.run([
        "git", "-C", str(repository), "update-ref", "-d",
        "refs/remotes/origin/{}".format(branch),
    ], check=True)
    assert pre_triage_security._resolve_ref(repository, branch) == (
        "refs/remotes/backup-a/{}".format(branch))
    assert pre_triage_security._resolve_ref(repository, "missing-branch") is None


def test_git_show_records_resolved_ref_without_mutating_source_repository(tmp_path):
    """Remote-tracking evidence keeps the matrix ref and leaves the checkout intact."""
    # Given a clean source checkout with a remote-tracking development branch
    repository = tmp_path / "source"
    repository.mkdir()
    commit = _init_source_repository(repository)
    branch = "release/0.5.z"
    subprocess.run([
        "git", "-C", str(repository), "update-ref",
        "refs/remotes/upstream/{}".format(branch), commit,
    ], check=True)
    before_head = subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", "HEAD"], text=True).strip()
    before_status = subprocess.check_output(
        ["git", "-C", str(repository), "status", "--porcelain"], text=True)

    # When evidence is read from the bare matrix branch
    evidence = pre_triage_security._git_show(repository, branch, "README.md")

    # Then provenance records both refs and the source worktree remains unchanged
    assert evidence == {
        "ref": branch,
        "path": "README.md",
        "command": "git show refs/remotes/upstream/{}:README.md".format(branch),
        "content": "source evidence\n",
    }
    assert subprocess.check_output(
        ["git", "-C", str(repository), "rev-parse", "HEAD"], text=True).strip() == before_head
    assert subprocess.check_output(
        ["git", "-C", str(repository), "status", "--porcelain"], text=True) == before_status


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


def _release_issue(key, summary, issue_type, parent=None, links=None, component=None):
    """Build the relevant Jira release graph without external requests."""
    fields = {
        "summary": summary, "issuetype": {
            "name": issue_type, "id": {"Epic": "10000", "Task": "10014", "Vulnerability": "10016"}[issue_type]},
        "status": {"name": "New"}, "labels": ["existing-label"],
        "issuelinks": links or [],
    }
    if parent:
        fields["parent"] = {"key": parent}
    if component is not None:
        fields["customfield_12345"] = component
    return {"key": key, "fields": fields}


def test_collect_release_evidence_preserves_scoped_dedup_graph(monkeypatch):
    """Release collection retains the parent and originating CVE component once."""
    # Given two release families sharing a stream and a dedup graph in one family
    epic = _release_issue("TC-10", "PRODUCT 3.1.2 Release Tasks", "Epic")
    task = _release_issue("TC-11", "PRODUCT 3.1.2 CVE triage", "Task", "TC-10", [
        {"type": {"name": "Blocks"}, "inwardIssue": {"key": "TC-12"}},
        {"type": {"name": "Related"}, "outwardIssue": {"key": "TC-99"}},
    ])
    remediation = _release_issue("TC-12", "Update library", "Task", links=[
        {"type": {"name": "Depend"}, "outwardIssue": {"key": "TC-13"}},
    ])
    cve = _release_issue("TC-13", "CVE issue", "Vulnerability", component="library")
    fetched = {"TC-13": cve}
    calls = []

    def jira(command, *args):
        """Return scoped synthetic release search and linked issue results."""
        calls.append((command, args))
        if command == "search_jql":
            jql = args[args.index("--jql") + 1]
            if "parent" in jql:
                return {"issues": [task], "isLast": True}
            return {"issues": [epic], "isLast": True}
        return {"TC-12": remediation}[args[0]]

    monkeypatch.setattr(pre_triage_security, "_jira_client", jira)
    configuration = {"project_key": "TC", "jira_version_prefix": "PRODUCT",
                     "vulnerability_issue_type_id": "10016",
                     "upstream_affected_component_field": "customfield_12345"}
    streams = [{"rows": [{"version": "3.0.9"}, {"version": "3.1.1"}]}]

    # When collecting only the release/remediation/CVE relationship paths
    graph = pre_triage_security._collect_release_evidence(configuration, streams, fetched)

    # Then fuzzy-search false positives do not cross release families
    assert [entry["family"] for entry in graph] == ["3.0", "3.1"]
    assert graph[0]["epics"] == graph[0]["tasks"] == []
    release = graph[1]
    assert release["tasks"][0]["parent"] == "TC-10"
    assert release["remediation"][0]["issue_type"] == "Task"
    assert release["originating_cves"][0]["upstream_affected_component"] == "library"
    assert release["originating_cves"][0]["labels"] == ["existing-label"]
    assert [args[0] for command, args in calls if command == "get_issue"] == ["TC-12"]
    assert "TC-99" not in fetched


@pytest.mark.parametrize("response", [{}, {"issues": None}, {"issues": [None]}])
def test_collect_release_evidence_rejects_malformed_search(monkeypatch, response):
    """Malformed release searches never become trusted no-match evidence."""
    # Given a broken search response from the Jira client
    monkeypatch.setattr(pre_triage_security, "_jira_client", lambda *_args: response)
    configuration = {"project_key": "TC", "jira_version_prefix": "PRODUCT"}

    # When collecting a known release family, then collection fails closed
    with pytest.raises(pre_triage_security.EvidenceError):
        pre_triage_security._collect_release_evidence(
            configuration, [{"rows": [{"version": "3.1.1"}]}], {})


def test_collect_release_evidence_keeps_search_failure(monkeypatch):
    """Failed Jira queries cannot be mistaken for absent release structures."""
    # Given an infrastructure failure instead of an empty successful result
    def failing_client(*_args):
        """Simulate the existing fail-fast Jira process."""
        raise subprocess.CalledProcessError(1, ["jira-client"])

    monkeypatch.setattr(pre_triage_security, "_jira_client", failing_client)

    # When collecting release evidence, then the original failure propagates
    with pytest.raises(subprocess.CalledProcessError):
        pre_triage_security._collect_release_evidence(
            {"project_key": "TC", "jira_version_prefix": "PRODUCT"},
            [{"rows": [{"version": "3.1.1"}]}], {})


@pytest.mark.parametrize("defect", ["wrong-parent", "wrong-project", "missing-linked-issue"])
def test_collect_release_evidence_rejects_invalid_relationship(monkeypatch, defect):
    """Release graph collection rejects unproven or out-of-scope identities."""
    # Given a matching release Epic and an invalid child/linked identity
    epic = _release_issue("TC-10", "PRODUCT 3.1.2 Release Tasks", "Epic")
    task = _release_issue("TC-11", "PRODUCT 3.1.2 CVE triage", "Task", "TC-10")
    if defect == "wrong-parent":
        task["fields"]["parent"]["key"] = "TC-99"
    elif defect == "wrong-project":
        task["key"] = "OTHER-11"
    else:
        task["fields"]["issuelinks"] = [
            {"type": {"name": "Blocks"}, "inwardIssue": {"key": "TC-12"}}]

    def jira(command, *args):
        """Return malformed bounded relationship evidence."""
        if command == "get_issue":
            return {}
        return {"issues": [task if "parent" in args[1] else epic]}

    monkeypatch.setattr(pre_triage_security, "_jira_client", jira)

    # When collecting this family, then the invalid graph is rejected
    with pytest.raises(pre_triage_security.EvidenceError):
        pre_triage_security._collect_release_evidence(
            {"project_key": "TC", "jira_version_prefix": "PRODUCT"},
            [{"rows": [{"version": "3.1.1"}]}], {})


@pytest.mark.parametrize("target", ["release-task", "remediation-task"])
@pytest.mark.parametrize("missing", [True, False])
def test_collect_release_evidence_rejects_missing_link_evidence(monkeypatch, target, missing):
    """Missing or null links cannot prove there is no release remediation to reuse."""
    # Given a matching release with an incomplete Task relationship snapshot
    epic = _release_issue("TC-10", "PRODUCT 3.1.2 Release Tasks", "Epic")
    task = _release_issue("TC-11", "PRODUCT 3.1.2 CVE triage", "Task", "TC-10", [
        {"type": {"name": "Blocks"}, "inwardIssue": {"key": "TC-12"}}])
    remediation = _release_issue("TC-12", "Update library", "Task")
    fields = (task if target == "release-task" else remediation)["fields"]
    if missing:
        fields.pop("issuelinks")
    else:
        fields["issuelinks"] = None

    def jira(command, *args):
        """Return the selected incomplete snapshot without external calls."""
        if command == "get_issue":
            return remediation
        return {"issues": [task if "parent" in args[1] else epic]}

    monkeypatch.setattr(pre_triage_security, "_jira_client", jira)

    # When collecting the relationship graph, then incomplete evidence fails
    with pytest.raises(pre_triage_security.EvidenceError, match="release issue links"):
        pre_triage_security._collect_release_evidence(
            {"project_key": "TC", "jira_version_prefix": "PRODUCT"},
            [{"rows": [{"version": "3.1.1"}]}], {})


@pytest.mark.parametrize("decisions", [
    [{"family": "3.1", "version": "3.1.2", "create_epic": True, "create_task": False}],
    [{"family": "3.1", "skip": True}],
    [],
])
def test_release_decisions_preserve_explicit_trusted_choices(decisions):
    """Trusted choices are retained without inventing creation permission."""
    assert pre_triage_security._validate_release_decisions(decisions, {"3.1"}) == decisions


@pytest.mark.parametrize("decisions", [
    None, {}, [{"family": "3.1", "create_epic": True}],
    [{"family": "3.1", "version": "3.0.2", "create_epic": True, "create_task": True}],
    [{"family": "3.0", "skip": True}],
    [{"family": "3.1", "skip": True}, {"family": "3.1", "skip": True}],
    [{"family": "3.1", "skip": True, "create_task": True}],
    [{"family": "3.1", "version": "3.1.2", "create_epic": "yes", "create_task": True}],
])
def test_release_decisions_reject_unbound_or_malformed_permissions(decisions):
    """Invalid, duplicated or cross-family decisions cannot authorize creation."""
    with pytest.raises(pre_triage_security.EvidenceError):
        pre_triage_security._validate_release_decisions(decisions, {"3.1"})


@requires_format_extra
def test_release_bundle_schema_preserves_optional_evidence_and_decisions():
    """Optional release evidence and decisions coexist with the old bundle contract."""
    # Given a previously valid trusted input and explicit release decision
    bundle = _complete_bundle()
    bundle["jira_metadata"]["release_jira"] = [{
        "family": "1.0", "epics": [], "tasks": [], "remediation": [], "originating_cves": []}]
    bundle["authorization"]["release_decisions"] = [{
        "family": "1.0", "version": "1.0.2", "create_epic": True, "create_task": True}]

    # When the extended trusted contract is validated
    pre_triage_security.validate_bundle(bundle)

    # Then release creation decisions do not enable generic mutations
    assert bundle["authorization"]["mutation_authorized"] is False


def test_release_decisions_are_supplied_by_the_trusted_runner(monkeypatch, capsys):
    """The existing runner process can supply decisions without sandbox input."""
    # Given explicit decisions on the host that invokes the collector
    decisions = [{"family": "3.1", "skip": True}]
    monkeypatch.setenv("FULLSEND_RELEASE_DECISIONS", json.dumps(decisions))
    monkeypatch.setattr(pre_triage_security, "collect_bundle",
                        lambda issue, root, choices: {"issue": issue, "decisions": choices})

    # When the normal pre-script collection command runs
    assert pre_triage_security.main(["collect", "TC-42", "/project"]) == 0

    # Then host decisions reach the collector unchanged without authorizing writes
    assert json.loads(capsys.readouterr().out) == {"issue": "TC-42", "decisions": decisions}


@pytest.mark.parametrize("decision_text", ["{", "null", "{}", '"unexpected"'])
def test_release_decisions_invalid_json_stops_collection(monkeypatch, capsys, decision_text):
    """Malformed runner decisions fail before any evidence request."""
    # Given malformed decisions and a collector that must never be called
    monkeypatch.setenv("FULLSEND_RELEASE_DECISIONS", decision_text)
    collector = MagicMock(return_value={})
    monkeypatch.setattr(pre_triage_security, "collect_bundle", collector)

    # When the normal collection command starts
    assert pre_triage_security.main(["collect", "TC-42", "/project"]) == 1

    # Then no request is made and the command reports its configuration failure
    collector.assert_not_called()
    assert "ERROR:" in capsys.readouterr().err


@requires_format_extra
def test_collect_bundle_includes_release_evidence_without_authorizing_writes(tmp_path, monkeypatch):
    """Actual collection carries release decisions into a validated report-only bundle."""
    # Given complete mocked host evidence and a confirmed release creation decision
    original = _complete_bundle()
    (tmp_path / "CLAUDE.md").write_text("# Project Configuration\n")
    configuration = original["configuration"]
    stream = original["matrix"]["streams"][0]
    issue = {"key": original["issue"]["key"], "fields": original["issue"]["fields"]}
    decisions = [{"family": "1.0", "version": "1.0.2", "create_epic": True, "create_task": True}]
    monkeypatch.setattr(pre_triage_security, "_runner_configuration", lambda *_args: (
        configuration, "https://example.com/lifecycle",
        [{"Stream": "1.0.x", "Security Matrix Path": "matrix.md", "Local Path": str(tmp_path)}],
        {"component": tmp_path}))
    monkeypatch.setattr(pre_triage_security, "parse_security_matrix", lambda *_args: (
        stream, [{"repository": "component", "lock_file": "Cargo.lock", "upstream_branch": "main"}]))
    monkeypatch.setattr(pre_triage_security, "_git_show", lambda _repo, ref, path: {
        "ref": ref, "path": path, "command": "git show {}:{}".format(ref, path), "content": "evidence"})
    monkeypatch.setattr(pre_triage_security, "_fetch_url", lambda url, **_kwargs: next(
        item for item in original["external_evidence"].values() if item["source_url"] == url))

    def jira(command, *_args):
        """Return successful empty release searches alongside the primary CVE."""
        return {"get_issue": issue, "get_remote_links": original["remote_links"],
                "get_versions": [], "search_jql": {"issues": []}}[command]

    monkeypatch.setattr(pre_triage_security, "_jira_client", jira)

    # When the normal collector builds and validates the extended input
    bundle = pre_triage_security.collect_bundle("TC-42", tmp_path, decisions)

    # Then an empty release search is proven evidence, not authorization to mutate
    assert bundle["jira_metadata"]["release_jira"] == [{
        "family": "1.0", "epics": [], "tasks": [], "remediation": [], "originating_cves": []}]
    assert bundle["authorization"] == {"mutation_authorized": False, "release_decisions": decisions}
    assert bundle["jira_metadata"]["related_issues"] == []


@requires_format_extra
@pytest.mark.parametrize("decisions", [
    [{"family": "1.0", "version": "2.0.1", "create_epic": True, "create_task": True}],
    [{"family": "1.0", "skip": True}, {"family": "1.0", "skip": True}],
])
def test_validate_bundle_checks_release_decision_family_bindings(decisions):
    """Schema-valid but unbound decisions fail the trusted bundle validation."""
    # Given a complete bundle with conflicting trusted family decisions
    bundle = _complete_bundle()
    bundle["jira_metadata"]["release_jira"] = [{
        "family": "1.0", "epics": [], "tasks": [], "remediation": [], "originating_cves": []}]
    bundle["authorization"]["release_decisions"] = decisions

    # When validating the full bundle, then semantic conflicts fail closed
    with pytest.raises(pre_triage_security.EvidenceError):
        pre_triage_security.validate_bundle(bundle)
