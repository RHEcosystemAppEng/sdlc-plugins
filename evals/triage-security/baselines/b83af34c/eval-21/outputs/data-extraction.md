# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z). This issue is scoped to the 2.2.x stream.

## Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo** (source dependency). Per the ecosystem classification table, source dependency ecosystems produce 2 remediation tasks per stream (upstream backport + downstream propagation).

## Version Impact Table

Based on lock file data from security-matrix-mock.md:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0   | 0.11.9      | YES       |       |
| 2.1.1   | 0.11.9      | YES       |       |
| 2.2.0   | 0.11.9      | YES       |       |
| 2.2.1   | 0.11.12     | YES       |       |
| 2.2.2   | --          | YES       | retag of 2.2.1 |
| 2.2.3   | 0.11.14     | NO        | ships fixed version |
| 2.2.4   | 0.11.14     | NO        | ships fixed version |

Versions affected within this issue's scope (2.2.x stream): 2.2.0, 2.2.1, 2.2.2
Versions not affected within this issue's scope: 2.2.3, 2.2.4

Cross-stream impact: 2.1.x stream versions (2.1.0, 2.1.1) are also affected but outside this issue's scope.
