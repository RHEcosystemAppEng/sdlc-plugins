# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Ecosystem | npm |
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
|--------------|----------|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- This is a source dependency ecosystem, so remediation would require **two tasks**: upstream backport + downstream propagation

## Labels

- `CVE-2026-45678` (CVE identifier)
- `pscomponent:org/rhtpa-ui` (component label matching pattern `pscomponent:`)
