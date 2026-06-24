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
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: **webpack**
- Ecosystem: **npm** (JavaScript/TypeScript package)
- The security-matrix.md Ecosystem Mappings table would define the lock file path (`package-lock.json`) and check command for npm dependencies

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Remote Links

- GitHub Advisory: GHSA-2026-wk55-m3rr
- CVE Record: CVE-2026-45678

## Fix Threshold

The fix threshold for this CVE is **webpack >= 5.98.0**. Any version of webpack below 5.98.0 is considered vulnerable.
