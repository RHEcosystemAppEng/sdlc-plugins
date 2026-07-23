# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Existing comments | None |
| Existing issue links | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams row: `2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (axios is a JavaScript/TypeScript package)
- The security matrix Ecosystem Mappings for the 2.2.x stream list Cargo and RPM ecosystems. npm is not listed in the Ecosystem Mappings table for this stream.
- Note: Since the Upstream Affected Component custom field (customfield_10632) is set to `axios`, Step 4.3 cross-CVE overlap detection applies before ecosystem-level lock file analysis would be needed.

## Custom Fields

- **customfield_10632** (Upstream Affected Component): axios
- **customfield_10669** (PS Component): pscomponent:org/rhtpa-ui
- **customfield_10832** (Stream): rhtpa-2.2

## Remote Links

- [GHSA-2026-ax91-r7pp](https://github.com/advisories/GHSA-2026-ax91-r7pp) -- GitHub Advisory
- [CVE-2026-44492](https://www.cve.org/CVERecord?id=CVE-2026-44492) -- CVE Record

## Vulnerability Description

A vulnerability was found in axios. The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services.
