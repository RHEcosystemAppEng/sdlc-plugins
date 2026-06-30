# Step 1 -- Data Extraction for TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version / fix threshold | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |
| Issue links | None |

## Custom Fields

| Field | Field ID | Value |
|-------|----------|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Parsed stream: 2.2.x
- Matched to Version Streams table: **2.2.x** stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- This issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: webpack
- Ecosystem: **npm** (webpack is a JavaScript/TypeScript build tool distributed via npm)
- Note: The security-matrix.md for streams 2.1.x and 2.2.x does not include an npm Ecosystem Mapping row. The configured ecosystems are Cargo and RPM only. This means there is no lock file path or check command configured for npm dependencies in the supportability matrix.
- The npm ecosystem would require a `package-lock.json` lock file for version inspection.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-45678 |

## Vulnerability Description Summary

The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.
