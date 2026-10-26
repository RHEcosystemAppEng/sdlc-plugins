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
| Affected Version Range | versions before 1.8.2 |
| Fixed Version | 1.8.2 |
| CVSS | 8.1 (High) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Labels | CVE-2026-44492, pscomponent:org/rhtpa-ui |
| Existing Issue Links | (none) |
| Existing Comments | (none) |

## Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: 2.2.x -> git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Ecosystem category: Source dependency
- Remediation task structure: 2 tasks per stream (dependency bump or upstream backport + downstream propagation)

## Fix Threshold

- Jira description fix threshold: **1.8.2**
- The fix threshold from the Jira description is used for version impact comparisons in Step 2.3 and overlap detection in Step 4.3
