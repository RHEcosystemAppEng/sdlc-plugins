# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Affected Component | pscomponent:org/rhtpa-ui |
| Upstream Affected Component | axios (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-ui (customfield_10669) |
| Stream | rhtpa-2.2 (customfield_10832) |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (Fix Threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Labels | CVE-2026-44492, pscomponent:org/rhtpa-ui |

## Remote Links

| Title | URL |
|-------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Issue Links

No existing issue links on TC-8010.

## Comments

No existing comments on TC-8010.

## Stream Scope Resolution

- Summary stream suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Classification: Source dependency ecosystem
- Remediation task structure: 2 tasks per stream (dependency bump + downstream propagation) when upstream fix is available
