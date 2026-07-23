# Step 1 -- Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | (none) |
| Status | New |
| Assignee | Unassigned |

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **scoped** to stream 2.2.x only

## Ecosystem Detection

- Vulnerable library: webpack
- Detected ecosystem: **npm** (JavaScript/TypeScript package)
- Note: The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists Cargo and RPM ecosystems but does not list npm. Automated lock file inspection is not configured for npm in this stream. Manual assessment or ecosystem configuration update may be required.

## Vulnerability Description

A vulnerability was found in webpack. The webpack package before version 5.98.0 allows arbitrary code execution through a specially crafted loader chain configuration. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules.

## Issue Links

No existing issue links.

## Remote Links

- [GHSA-2026-wk55-m3rr](https://github.com/advisories/GHSA-2026-wk55-m3rr) -- GitHub Advisory
- [CVE-2026-45678](https://www.cve.org/CVERecord?id=CVE-2026-45678) -- CVE Record
