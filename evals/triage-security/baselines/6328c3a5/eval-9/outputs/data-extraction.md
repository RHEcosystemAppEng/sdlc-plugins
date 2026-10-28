# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Jira Issue Key | TC-8011 |
| CVE ID | CVE-2026-45678 |
| Affected component (label) | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Status | New |
| Assignee | Unassigned |
| Existing issue links | None |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: **webpack**
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: **Source dependency**
- Remediation task structure: 2 tasks per stream -- dependency bump + downstream propagation (since fix version 5.98.0 is available)

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
