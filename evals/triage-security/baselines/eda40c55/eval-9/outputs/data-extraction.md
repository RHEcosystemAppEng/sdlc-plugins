# Step 1 -- Data Extraction

## Parsed CVE Data for TC-8011

| Field | Value |
|-------|-------|
| Jira Issue Key | TC-8011 |
| CVE ID | CVE-2026-45678 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version (fix threshold) | 5.98.0 |
| CVSS Score | 7.8 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Upstream Fix PR | (none found in remote links) |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
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
- Mapped to configured Version Stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Remediation pattern: 2 tasks (upstream backport + downstream propagation)

## Deployment Context

- Affected repository (from component label pscomponent:org/rhtpa-ui): rhtpa-backend
- Deployment context: upstream (from Source Repositories table)
