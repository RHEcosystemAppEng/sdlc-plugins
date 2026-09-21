#!/usr/bin/env python3
"""Tests for the trusted triage-security evidence transformer."""

import json
import os
import subprocess
import sys

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


def test_build_bundle_accepts_complete_source_dependency_evidence():
    """Complete source-dependency evidence produces schema-valid sandbox input."""
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
