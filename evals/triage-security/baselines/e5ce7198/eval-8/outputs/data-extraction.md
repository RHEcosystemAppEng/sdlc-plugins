# Step 1 -- Data Extraction for TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Labels | CVE-2026-44492, pscomponent:org/rhtpa-ui |
| Affects Versions (PSIRT-claimed) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream in the Version Streams table from Security Configuration.

- Issue stream scope: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Steps 3-7 will be scoped to this stream only.

## Ecosystem Detection

The vulnerable library is `axios`, which is a JavaScript/TypeScript npm package. The ecosystem is **npm**.

Note: The security-matrix.md for the 2.2.x stream has Ecosystem Mappings for Cargo and RPM only -- npm is not listed. However, the component label `pscomponent:org/rhtpa-ui` suggests a UI component (likely a separate source repository from the `rhtpa-backend` Rust service). The lock file for npm dependencies would be `package-lock.json` in the rhtpa-ui source repository.

## Remote Links

- [GHSA-2026-ax91-r7pp](https://github.com/advisories/GHSA-2026-ax91-r7pp) -- GitHub Advisory
- [CVE-2026-44492](https://www.cve.org/CVERecord?id=CVE-2026-44492) -- CVE Record

## Existing Comments

None.

## Existing Issue Links

None.
