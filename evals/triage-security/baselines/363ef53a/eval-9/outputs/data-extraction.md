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
| Existing comments | None |

## Custom Fields

| Field | Value |
|-------|-------|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- This issue is **stream-scoped** to the 2.2.x stream only.

## Ecosystem Detection

- Vulnerable library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: Source dependency
- Remediation tasks per stream: 2 (dependency bump or upstream backport + downstream propagation)

## Deployment Context

- Repository: rhtpa-backend (from Source Repositories)
- Deployment context: not specified (defaults to `upstream`)
