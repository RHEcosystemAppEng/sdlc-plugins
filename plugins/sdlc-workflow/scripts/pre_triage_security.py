#!/usr/bin/env python3
"""Build and validate trusted evidence bundles for triage-security."""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from jsonschema import FormatChecker, ValidationError, validate


_ISSUE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9]+-[0-9]+$")
_SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "triage-security-input.schema.json"


class EvidenceError(ValueError):
    """Raised when runner evidence is incomplete or inconsistent."""


def _markdown_section(document, heading, level):
    """Return a Markdown section body without its heading."""
    pattern = r"^{} {}\s*$\n?(.*?)(?=^#{{1,{}}}\s|\Z)".format(
        "#" * level, re.escape(heading), level)
    match = re.search(pattern, document, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise EvidenceError("missing {} heading".format(heading))
    return match.group(1)


def _markdown_table(section, heading):
    """Parse a named Markdown table into dictionaries keyed by its headers."""
    body = _markdown_section(section, heading, 3)
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in body.splitlines()
        if line.strip().startswith("|")
    ]
    if len(rows) < 3:
        raise EvidenceError("{} must contain a data table".format(heading))
    headers = rows[0]
    if not all(headers):
        raise EvidenceError("{} has an invalid table header".format(heading))
    data_rows = []
    for row in rows[2:]:
        if len(row) != len(headers) or any(not cell for cell in row):
            raise EvidenceError("{} has an incomplete table row".format(heading))
        data_rows.append(dict(zip(headers, row)))
    if not data_rows:
        raise EvidenceError("{} must contain at least one row".format(heading))
    return data_rows


def _markdown_table_rows(section, heading, level=2):
    """Parse a Markdown table while allowing empty informational cells."""
    body = _markdown_section(section, heading, level)
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in body.splitlines()
        if line.strip().startswith("|")
    ]
    if len(rows) < 3:
        raise EvidenceError("{} must contain a data table".format(heading))
    headers = rows[0]
    if not all(headers):
        raise EvidenceError("{} has an invalid table header".format(heading))
    values = []
    for row in rows[2:]:
        if len(row) != len(headers):
            raise EvidenceError("{} has an incomplete table row".format(heading))
        values.append(dict(zip(headers, row)))
    if not values:
        raise EvidenceError("{} must contain at least one row".format(heading))
    return headers, values


def parse_security_matrix(stream_name, matrix_path, content):
    """Parse a stream matrix into schema rows and trusted read instructions."""
    if not isinstance(content, str) or not content:
        raise EvidenceError("security matrix content is required")
    headers, rows = _markdown_table_rows(content, "Supportability Matrix")
    version_header = next((header for header in headers if "version" in header.lower()), None)
    if not version_header:
        raise EvidenceError("Supportability Matrix has no version column")
    ignored = {version_header, "Build", "Build Date", "Notes"}
    source_headers = [header for header in headers if header not in ignored]
    if not source_headers:
        raise EvidenceError("Supportability Matrix has no source commit columns")

    matrix_rows = []
    for row in rows:
        version = row[version_header]
        source_commits = {
            header: row[header].strip("`")
            for header in source_headers
            if row[header].strip("`")
        }
        retag = re.search(r"\bretag of\s+([^\s|]+)", row.get("Notes", ""), re.IGNORECASE)
        matrix_rows.append({
            "version": version,
            "source_commits": source_commits,
            "retag_of": retag.group(1) if retag else None,
        })

    _, ecosystem_rows = _markdown_table_rows(content, "Ecosystem Mappings")
    mappings = []
    for row in ecosystem_rows:
        try:
            mappings.append({
                "ecosystem": row["Ecosystem"],
                "repository": row["Repository"],
                "lock_file": row["Lock File"].strip("`"),
                "check_command": row["Check Command"].strip("`"),
                "upstream_branch": row["Upstream Branch"].strip("`"),
            })
        except KeyError as error:
            raise EvidenceError("Ecosystem Mappings is missing {}".format(error.args[0])) from error
    return {
        "name": stream_name,
        "matrix_source": content,
        "rows": matrix_rows,
    }, mappings


def parse_security_configuration(claude_md):
    """Parse target-project Jira and Security Configuration into schema fields."""
    if not isinstance(claude_md, str):
        raise EvidenceError("CLAUDE.md content must be text")
    jira = _markdown_section(claude_md, "Jira Configuration", 2)
    security = _markdown_section(claude_md, "Security Configuration", 2)
    lifecycle = _markdown_section(security, "Product Lifecycle", 3)
    values = {
        key: value.strip()
        for key, value in re.findall(r"^- ([^:]+):\s*(.+?)\s*$", lifecycle, re.MULTILINE)
        if not value.strip().startswith("{{")
    }
    project_key = re.search(r"^- Project key:\s*(\S+)\s*$", jira, re.MULTILINE)
    if not project_key:
        raise EvidenceError("Jira Configuration is missing Project key")

    required = {
        "Product pages URL": "product lifecycle URL",
        "Jira version prefix": "Jira version prefix",
        "Vulnerability issue type ID": "Vulnerability issue type ID",
        "Component label pattern": "Component label pattern",
    }
    for field, label in required.items():
        if not values.get(field):
            raise EvidenceError("Security Configuration is missing {}".format(label))

    streams = _markdown_table(security, "Version Streams")
    # Parse Source Repositories with the blank-cell-tolerant reader so an empty
    # (present but blank) Deployment Context cell can fall back to "upstream"
    # rather than being rejected as an incomplete row before the default applies.
    _, sources = _markdown_table_rows(security, "Source Repositories", level=3)
    try:
        version_streams = [{
            "name": row["Stream"],
            "matrix_path": row["Security Matrix Path"],
            "release_repository": row["Konflux Release Repo"],
        } for row in streams]
        source_repositories = []
        for row in sources:
            name = row["Repository"]
            url = row["URL"]
            if not name or not url:
                raise EvidenceError("Source Repositories row is missing Repository or URL")
            source_repositories.append({
                "name": name,
                "url": url,
                "deployment_context": row.get("Deployment Context") or "upstream",
            })
    except KeyError as error:
        raise EvidenceError("Security Configuration table is missing {}".format(error.args[0])) from error

    configuration = {
        "project_key": project_key.group(1),
        "jira_version_prefix": values["Jira version prefix"],
        "vulnerability_issue_type_id": values["Vulnerability issue type ID"],
        "component_label_pattern": values["Component label pattern"],
        "version_streams": version_streams,
        "source_repositories": source_repositories,
    }
    optional_fields = {
        "VEX Justification custom field": "vex_justification_field",
        "Upstream Affected Component custom field": "upstream_affected_component_field",
        "PS Component custom field": "ps_component_field",
        "Stream custom field": "stream_field",
        "ProdSec Jira account ID": "prodsec_account_id",
        "Embargo policy URL": "embargo_policy_url",
    }
    for source, destination in optional_fields.items():
        if values.get(source):
            configuration[destination] = values[source]
    return configuration


def _runner_configuration(claude_md, project_root):
    """Extract runner-only paths and URLs alongside the sandbox configuration."""
    configuration = parse_security_configuration(claude_md)
    security = _markdown_section(claude_md, "Security Configuration", 2)
    lifecycle = _markdown_section(security, "Product Lifecycle", 3)
    lifecycle_url = re.search(r"^- Product pages URL:\s*(\S+)\s*$", lifecycle, re.MULTILINE)
    if not lifecycle_url:
        raise EvidenceError("Security Configuration is missing Product pages URL")
    stream_rows = _markdown_table(security, "Version Streams")
    _, registry_rows = _markdown_table_rows(claude_md, "Repository Registry", level=2)
    paths = {
        row["Repository"]: Path(row["Path"])
        for row in registry_rows
        if "Repository" in row and "Path" in row
    }
    root = Path(project_root)
    return configuration, lifecycle_url.group(1), stream_rows, {
        name: path if path.is_absolute() else root / path
        for name, path in paths.items()
    }


def extract_cve_id(issue):
    """Return the required CVE identifier from an issue's labels or summary."""
    issue = _require_mapping(issue, "issue")
    fields = _require_mapping(issue.get("fields"), "issue.fields")
    values = list(_require_list(fields.get("labels"), "issue.fields.labels", allow_empty=True))
    values.append(fields.get("summary", ""))
    for value in values:
        match = re.search(r"\bCVE-\d{4}-\d{4,}\b", value or "", re.IGNORECASE)
        if match:
            return match.group(0).upper()
    raise EvidenceError("issue does not contain a CVE identifier")


def _require_mapping(value, name):
    """Return a required mapping or raise a descriptive evidence error."""
    if not isinstance(value, dict):
        raise EvidenceError("{} must be an object".format(name))
    return value


def _require_list(value, name, allow_empty=False):
    """Return a required list or raise a descriptive evidence error."""
    if not isinstance(value, list) or (not allow_empty and not value):
        qualifier = "a non-empty list" if not allow_empty else "a list"
        raise EvidenceError("{} must be {}".format(name, qualifier))
    return value


def normalize_issue(issue):
    """Extract the schema-required audit fields from a full Jira issue response."""
    issue = _require_mapping(issue, "issue")
    key = issue.get("key", "")
    if not isinstance(key, str) or not _ISSUE_KEY_RE.fullmatch(key):
        raise EvidenceError("issue.key must be a Jira issue key")

    fields = _require_mapping(issue.get("fields"), "issue.fields")
    status = _require_mapping(fields.get("status"), "issue.fields.status")
    reporter = _require_mapping(fields.get("reporter"), "issue.fields.reporter")
    comments = _require_mapping(fields.get("comment"), "issue.fields.comment")
    description = fields.get("description")
    if not isinstance(description, dict):
        raise EvidenceError("issue.fields.description must be an ADF object")

    summary = fields.get("summary")
    if not isinstance(summary, str) or not summary:
        raise EvidenceError("issue.fields.summary is required")
    status_name = status.get("name")
    if not isinstance(status_name, str) or not status_name:
        raise EvidenceError("issue.fields.status.name is required")

    account_id = reporter.get("accountId")
    display_name = reporter.get("displayName")
    if not isinstance(account_id, str) or not account_id:
        raise EvidenceError("issue.fields.reporter.accountId is required")
    if not isinstance(display_name, str) or not display_name:
        raise EvidenceError("issue.fields.reporter.displayName is required")

    return {
        "key": key,
        "summary": summary,
        "description": description,
        "status": status_name,
        "labels": _require_list(fields.get("labels"), "issue.fields.labels", allow_empty=True),
        "versions": normalize_versions(fields.get("versions")),
        "reporter": {"account_id": account_id, "display_name": display_name},
        "comments": _require_list(comments.get("comments"), "issue.fields.comment.comments", allow_empty=True),
        "fields": fields,
    }


def normalize_versions(versions):
    """Reduce Jira version objects to the schema's stable audit fields."""
    versions = _require_list(versions, "versions", allow_empty=True)
    normalized = []
    for index, version in enumerate(versions):
        version = _require_mapping(version, "versions[{}]".format(index))
        for field in ("id", "name", "released"):
            if field not in version:
                raise EvidenceError("versions[{}].{} is required".format(index, field))
        entry = {
            "id": str(version["id"]),
            "name": version["name"],
            "released": version["released"],
        }
        if "archived" in version:
            entry["archived"] = version["archived"]
        normalized.append(entry)
    return normalized


def normalize_remote_links(remote_links):
    """Convert Jira remote links into the narrow sandbox link contract."""
    links = _require_list(remote_links, "remote_links")
    normalized = []
    for index, link in enumerate(links):
        link = _require_mapping(link, "remote_links[{}]".format(index))
        source = link.get("object", link)
        source = _require_mapping(source, "remote_links[{}].object".format(index))
        url = source.get("url")
        title = source.get("title")
        if not isinstance(url, str) or not url:
            raise EvidenceError("remote_links[{}] is missing object.url".format(index))
        if not isinstance(title, str) or not title:
            raise EvidenceError("remote_links[{}] is missing object.title".format(index))
        normalized.append({"url": url, "title": title})
    return normalized


def _validate_matrix(matrix):
    """Reject a matrix that cannot support deterministic version analysis."""
    matrix = _require_mapping(matrix, "matrix")
    for stream_index, stream in enumerate(_require_list(matrix.get("streams"), "matrix.streams")):
        stream = _require_mapping(stream, "matrix.streams[{}]".format(stream_index))
        rows = _require_list(stream.get("rows"), "matrix.streams[{}].rows".format(stream_index))
        for row_index, row in enumerate(rows):
            row = _require_mapping(row, "matrix.streams[{}].rows[{}]".format(stream_index, row_index))
            if not row.get("version") or not isinstance(row.get("source_commits"), dict):
                raise EvidenceError("matrix row {}:{} is malformed".format(stream_index, row_index))
            if row.get("retag_of") is None:
                if not row["source_commits"]:
                    raise EvidenceError("matrix row {}:{} has no source commits".format(stream_index, row_index))
    return matrix


def _validate_source_evidence(source_evidence):
    """Reject missing lock-file or development-stream runner evidence."""
    source_evidence = _require_mapping(source_evidence, "source_evidence")
    for name in ("lock_files", "development_streams"):
        reads = _require_list(source_evidence.get(name), "source_evidence.{}".format(name))
        for index, read in enumerate(reads):
            read = _require_mapping(read, "source_evidence.{}[{}]".format(name, index))
            for field in ("repository", "ref", "path", "command", "content"):
                if not isinstance(read.get(field), str) or not read[field]:
                    raise EvidenceError("source_evidence.{}[{}].{} is required".format(name, index, field))
            if not read["command"].startswith("git show "):
                raise EvidenceError("source evidence commands must use git show")
    return source_evidence


def validate_bundle(bundle, schema_path=None):
    """Validate a completed bundle against the sandbox's exact JSON schema."""
    path = Path(schema_path or os.environ.get("FULLSEND_INPUT_SCHEMA", _SCHEMA_PATH))
    try:
        with path.open() as schema_file:
            schema = json.load(schema_file)
        validate(instance=bundle, schema=schema, format_checker=FormatChecker())
    except (OSError, json.JSONDecodeError, ValidationError) as error:
        raise EvidenceError("triage-security input validation failed: {}".format(error)) from error


def build_bundle(issue, remote_links, configuration, external_evidence, matrix,
                 source_evidence, jira_metadata, idempotency,
                 mutation_authorized):
    """Build a schema-validated, credential-free triage-security input bundle."""
    configuration = _require_mapping(configuration, "configuration")
    external_evidence = _require_mapping(external_evidence, "external_evidence")
    jira_metadata = _require_mapping(jira_metadata, "jira_metadata")
    idempotency = _require_mapping(idempotency, "idempotency")

    bundle = {
        "schema_version": "1",
        "issue": normalize_issue(issue),
        "remote_links": normalize_remote_links(remote_links),
        "configuration": configuration,
        "external_evidence": external_evidence,
        "matrix": _validate_matrix(matrix),
        "source_evidence": _validate_source_evidence(source_evidence),
        "jira_metadata": jira_metadata,
        "idempotency": idempotency,
        "authorization": {"mutation_authorized": bool(mutation_authorized)},
    }
    validate_bundle(bundle)
    return bundle


def _jira_client(command, *arguments):
    """Run the existing Jira client and decode its JSON response."""
    client = Path(__file__).with_name("jira-client.py")
    result = subprocess.run(
        [sys.executable, str(client), command, *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise EvidenceError("jira-client returned invalid JSON for {}".format(command)) from error


def _fetch_url(url, allow_missing=False):
    """Fetch required external evidence and retain its retrieval provenance.

    When ``allow_missing`` is set, a 404 is treated as legitimate evidence (the
    CVE is not tracked by this source, e.g. an OSV gap or a reserved/embargoed
    MITRE record) and recorded with its status and body instead of aborting the
    whole bundle. Every other non-2xx status still fails loudly.
    """
    try:
        with urlopen(url, timeout=30) as response:
            body = response.read().decode("utf-8")
            status = response.status
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        status = error.code
    except URLError as error:
        raise EvidenceError("could not retrieve {}: {}".format(url, error.reason)) from error
    if status < 200 or status >= 300:
        if not (allow_missing and status == 404):
            raise EvidenceError("required evidence {} returned HTTP {}".format(url, status))
    try:
        body = json.loads(body)
    except json.JSONDecodeError:
        pass
    return {
        "source_url": url,
        "retrieved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,
        "body": body,
    }


def _git_show(repository_path, ref, path):
    """Read source evidence with the permitted read-only git show command."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repository_path), "show", "{}:{}".format(ref, path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip()
        raise EvidenceError("git show failed for {}:{}: {}".format(ref, path, detail)) from error
    return {
        "ref": ref,
        "path": path,
        "command": "git show {}:{}".format(ref, path),
        "content": result.stdout,
    }


def _related_issue(issue):
    """Normalize a fetched related Jira issue for audit and idempotency checks."""
    fields = _require_mapping(issue.get("fields"), "related issue fields")
    status = _require_mapping(fields.get("status"), "related issue status")
    return {
        "key": issue.get("key", ""),
        "summary": fields.get("summary", ""),
        "status": status.get("name", ""),
        "labels": fields.get("labels", []) or [],
        "description": fields.get("description", {}) or {},
        "comments": (fields.get("comment") or {}).get("comments", []) or [],
        "links": fields.get("issuelinks", []) or [],
    }


def _related_keys(issue):
    """Return each directly related Jira key once, in stable order."""
    fields = _require_mapping(issue.get("fields"), "issue.fields")
    keys = {entry.get("key") for entry in fields.get("subtasks", []) if entry.get("key")}
    for link in fields.get("issuelinks", []) or []:
        related = link.get("inwardIssue") or link.get("outwardIssue") or {}
        if related.get("key"):
            keys.add(related["key"])
    return sorted(keys)


def _action_markers(issue):
    """Extract stable triage action markers from the current issue's comments."""
    markers = []
    for comment in (issue.get("fields", {}).get("comment") or {}).get("comments", []) or []:
        text = json.dumps(comment.get("body", {}))
        markers.extend(re.findall(r"triage-security:[A-Za-z0-9_-]+", text))
    return sorted(set(markers))


def _jql_escape(value):
    """Escape a value embedded in a quoted JQL literal."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def collect_bundle(issue_key, project_root):
    """Collect all credentialed evidence for one poller-dispatched security issue."""
    # Validate the key before it is interpolated into any JQL. A conforming key
    # carries no JQL metacharacters, so this is a self-contained injection defense
    # that does not rely on the pre-triage-security.sh regex gate upstream of us.
    if not isinstance(issue_key, str) or not _ISSUE_KEY_RE.fullmatch(issue_key):
        raise EvidenceError("issue_key must be a Jira issue key")
    root = Path(project_root)
    claude_path = root / "CLAUDE.md"
    if not claude_path.is_file():
        raise EvidenceError("target project CLAUDE.md is required")
    configuration, lifecycle_url, stream_rows, repository_paths = _runner_configuration(
        claude_path.read_text(), root)
    issue = _jira_client("get_issue", issue_key, "--fields", "*all")
    cve_id = extract_cve_id(issue)
    escaped_project_key = _jql_escape(configuration["project_key"])
    escaped_cve_id = _jql_escape(cve_id)
    remote_links = _jira_client("get_remote_links", issue_key)
    versions = _jira_client("get_versions", configuration["project_key"])

    sibling_jql = (
        'project = "{}" AND labels = "{}" AND issuetype = {} AND key != "{}"'
        .format(escaped_project_key, escaped_cve_id, configuration["vulnerability_issue_type_id"], issue_key)
    )
    searches = [("same-cve-siblings", sibling_jql)]
    component_field = configuration.get("upstream_affected_component_field")
    component = issue.get("fields", {}).get(component_field, "") if component_field else ""
    component_field_number = re.search(r"(\d+)$", component_field or "")
    if isinstance(component, str) and component and component_field_number:
        overlap_jql = (
            'project = "{}" AND issuetype = {} AND cf[{}] ~ "{}" AND key != "{}"'
            .format(
                escaped_project_key,
                configuration["vulnerability_issue_type_id"],
                component_field_number.group(1),
                _jql_escape(component),
                issue_key,
            )
        )
        searches.append(("cross-cve-overlap", overlap_jql))
    preemptive_jql = (
        'project = "{}" AND issuetype = Task AND labels = "security-preemptive" '
        'AND labels = "{}" ORDER BY created DESC'
        .format(escaped_project_key, escaped_cve_id)
    )
    searches.append(("preemptive-remediation", preemptive_jql))

    fetched = {}
    search_results = []
    for purpose, jql in searches:
        search = _jira_client("search_jql", "--jql", jql, "--fields", "*all", "--all")
        items = search.get("issues", [])
        for item in items:
            if item.get("key"):
                fetched[item["key"]] = item
        search_results.append((purpose, jql, items))
    for key in _related_keys(issue):
        fetched.setdefault(key, _jira_client("get_issue", key, "--fields", "*all"))
    related = [_related_issue(fetched[key]) for key in sorted(fetched)]

    external_evidence = {
        "mitre": _fetch_url("https://cveawg.mitre.org/api/cve/{}".format(cve_id), allow_missing=True),
        "osv": _fetch_url("https://api.osv.dev/v1/vulns/{}".format(cve_id), allow_missing=True),
        "lifecycle": _fetch_url(lifecycle_url),
    }

    matrix_streams = []
    lock_files = []
    development_streams = []
    for stream_row in stream_rows:
        try:
            stream_name = stream_row["Stream"]
            matrix_path = stream_row["Security Matrix Path"]
            local_release = Path(stream_row["Local Path"])
        except KeyError as error:
            raise EvidenceError(
                "Version Streams table is missing {}".format(error.args[0])) from error
        matrix_file = root / matrix_path
        if matrix_file.is_file():
            matrix_content = matrix_file.read_text()
        else:
            matrix_content = _git_show(local_release, "main", matrix_path)["content"]
        matrix, mappings = parse_security_matrix(stream_name, matrix_path, matrix_content)
        matrix_streams.append(matrix)
        for mapping in mappings:
            repository = mapping["repository"]
            if repository not in repository_paths:
                raise EvidenceError("Repository Registry has no path for {}".format(repository))
            for row in matrix["rows"]:
                ref = row["source_commits"].get(repository)
                if ref:
                    read = _git_show(repository_paths[repository], ref, mapping["lock_file"])
                    lock_files.append({"repository": repository, **read})
            read = _git_show(repository_paths[repository], mapping["upstream_branch"], mapping["lock_file"])
            development_streams.append({"repository": repository, **read})

    jira_metadata = {
        "versions": normalize_versions(versions),
        "sibling_searches": [{
            "purpose": purpose,
            "jql": jql,
            "issues": [_related_issue(item) for item in items],
        } for purpose, jql, items in search_results],
        "related_issues": related,
    }
    return build_bundle(
        issue=issue,
        remote_links=remote_links,
        configuration=configuration,
        external_evidence=external_evidence,
        matrix={"streams": matrix_streams},
        source_evidence={"lock_files": lock_files, "development_streams": development_streams},
        jira_metadata=jira_metadata,
        idempotency={
            "action_markers": _action_markers(issue),
            "existing_remediation": related,
        },
        mutation_authorized=False,
    )


def main(argv=None):
    """Run a requested deterministic transform or trusted collection command."""
    parser = argparse.ArgumentParser(prog="pre_triage_security.py")
    subparsers = parser.add_subparsers(dest="command", required=True)
    collect = subparsers.add_parser("collect")
    collect.add_argument("issue_key")
    collect.add_argument("project_root")
    config = subparsers.add_parser("parse-configuration")
    config.add_argument("claude_md")
    args = parser.parse_args(argv)
    try:
        if args.command == "collect":
            result = collect_bundle(args.issue_key, args.project_root)
        else:
            result = parse_security_configuration(Path(args.claude_md).read_text())
    except (EvidenceError, subprocess.CalledProcessError) as error:
        print("ERROR: {}".format(error), file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
