# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix [rhtpa-2.2]) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version | 1.8.2 |
| CVSS | 8.1 (High) |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Upstream Fix PR | Not available (no PR link in remote links) |
| Existing Comments | None |
| Existing Issue Links | None |

## Custom Fields

| Field ID | Field Name | Value |
|----------|------------|-------|
| customfield_10632 | Upstream Affected Component | axios |
| customfield_10669 | PS Component | pscomponent:org/rhtpa-ui |
| customfield_10832 | Stream | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- **Ecosystem**: npm (axios is a JavaScript/TypeScript package)
- Lock file: `package-lock.json` (standard npm lock file)
- The security matrix Ecosystem Mappings table would define the exact lock file path and check command for npm dependencies

## Vulnerability Description

The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
