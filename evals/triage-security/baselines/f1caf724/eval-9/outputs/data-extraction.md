# Step 1 -- Data Extraction for TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Status | New |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream in the Security Configuration's Version Streams table, which corresponds to the Konflux release repo `rhtpa-release.0.4.z`.

The issue is **stream-scoped** to 2.2.x only. Steps 3-4 will be scoped to this single stream.

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript package. This falls under the **npm** ecosystem.

Per the ecosystem classification table:
- **npm** is a **source dependency** ecosystem
- Remediation requires **2 tasks per stream**: upstream backport + downstream propagation

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
