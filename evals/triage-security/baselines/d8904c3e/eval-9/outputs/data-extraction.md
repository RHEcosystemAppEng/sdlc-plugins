# Step 1 -- Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Jira Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected Component | pscomponent:org/rhtpa-ui |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | webpack |
| Ecosystem | npm |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version | 5.98.0 |
| CVSS Score | 7.8 (High) |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Upstream Fix PR | (none found in remote links) |
| Existing Comments | (none) |
| Existing Issue Links | (none) |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`
- This is a **scoped** issue -- triage Steps 3-4 apply only to the 2.2.x stream.

## Ecosystem Detection

- Library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: **Source dependency**
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)

## Vulnerability Details

The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
