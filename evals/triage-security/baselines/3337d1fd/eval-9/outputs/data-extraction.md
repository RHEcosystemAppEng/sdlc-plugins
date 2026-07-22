# Step 1 - Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Jira Issue Key | TC-8011 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |

## Custom Fields

| Field | Value |
|-------|-------|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Issue Links

No existing links on TC-8011.

## Remote Links

- [GHSA-2026-wk55-m3rr](https://github.com/advisories/GHSA-2026-wk55-m3rr) - GitHub Advisory
- [CVE-2026-45678](https://www.cve.org/CVERecord?id=CVE-2026-45678) - CVE Record

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table from Security Configuration. The issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

The vulnerable library is **webpack**, which is an **npm** ecosystem package (JavaScript/TypeScript). Reviewing the 2.2.x stream's Ecosystem Mappings table in security-matrix.md, the configured ecosystems are:

- Cargo (Rust crates)
- RPM (system packages)

The **npm ecosystem is not listed** in the Ecosystem Mappings table for any configured stream. Per the skill's ecosystem detection logic, this means automated lock file inspection cannot proceed for webpack. This would normally trigger:

> "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required."

However, cross-CVE overlap detection (Step 4.3) can still proceed independently since it operates on Jira issue data and remediation task descriptions, not on lock file inspection.

## Deployment Context

The component label `pscomponent:org/rhtpa-ui` does not match any repository in the Source Repositories table (which only lists `rhtpa-backend`). Deployment context defaults to `upstream`.
