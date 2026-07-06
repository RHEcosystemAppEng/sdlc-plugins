# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (Fix Threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Existing Comments | None |

## Custom Fields

| Custom Field | Field ID | Value |
|-------------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Labels

- CVE-2026-44492
- pscomponent:org/rhtpa-ui

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-ax91-r7pp | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE-2026-44492 | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Existing Issue Links

None.

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- This is a source dependency ecosystem, so remediation would normally require two tasks (upstream backport + downstream propagation).
