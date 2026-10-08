# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Vulnerable Library | axios |
| Ecosystem | npm |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (fix threshold) | 1.8.2 |
| CVSS Score | 8.1 (High) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Labels | CVE-2026-44492, pscomponent:org/rhtpa-ui |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: 2.2.x / rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x only

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: Source dependency
- Remediation tasks per stream: 2 (dependency bump + downstream propagation, assuming fix available upstream)

## Existing Issue Links

No existing links on TC-8010.

## Comments

No existing comments on TC-8010.
