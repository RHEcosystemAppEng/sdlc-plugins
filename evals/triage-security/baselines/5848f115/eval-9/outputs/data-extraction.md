# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Jira Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Ecosystem | npm (JavaScript/TypeScript package) |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Upstream fix PR | (none found in remote links) |
| Existing comments | (none) |
| Existing issue links | (none) |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (from Version Streams table in Security Configuration)
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z
- This issue is **stream-scoped** to the 2.2.x stream only.

## Ecosystem Detection

- Library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: **Source dependency**
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0
allows arbitrary code execution through a specially crafted loader chain
configuration. An attacker with control over a project's webpack configuration
can execute arbitrary code during the build process.

The vulnerability exists because webpack does not properly sanitize loader paths
when resolving the loader chain, allowing path traversal to execute arbitrary
modules.

## Deployment Context

- Affected repository: rhtpa-ui (derived from component label pscomponent:org/rhtpa-ui)
- Deployment context: Not found in Source Repositories table; defaulting to `upstream`

Note: The Source Repositories table in the project CLAUDE.md lists only
rhtpa-backend. The rhtpa-ui repository is not registered, so the deployment
context defaults to `upstream`.
