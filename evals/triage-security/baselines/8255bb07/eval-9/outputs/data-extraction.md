# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Jira Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Existing comments | None |
| Existing issue links | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. Mapping to the Version Streams table from Security Configuration:

- Suffix `rhtpa-2.2` maps to stream **2.2.x**
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **stream-scoped** to 2.2.x only. Steps 3-8 will be scoped to this single stream.

## Ecosystem Detection

The vulnerable library is **webpack**, which is an npm (JavaScript/TypeScript) package. The ecosystem is **npm**.

Note: The security-matrix.md Ecosystem Mappings table for stream 2.2.x lists Cargo and RPM ecosystems but does not list npm. In a real triage, this would trigger an "Unsupported ecosystem" warning for automated lock file inspection. However, the vulnerability data is clear from the Jira description and external sources, so the fix threshold (5.98.0) and affected range (< 5.98.0) are well-established.

## Deployment Context Lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-ui` is `rhtpa-ui`. Looking up the Source Repositories table in Security Configuration, only `rhtpa-backend` is listed. The `rhtpa-ui` repository is not found in the Source Repositories table, so the deployment context defaults to **upstream**.

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
