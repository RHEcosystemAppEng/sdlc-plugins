# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Vulnerable library | axios |
| Ecosystem | npm |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Vulnerability type | Server-Side Request Forgery (SSRF) via crafted URL |
| Component label | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Scope: **scoped** -- this issue covers only the 2.2.x stream

## Remote Links

| Title | URL | Type |
|-------|-----|------|
| GHSA-2026-ax91-r7pp | https://github.com/advisories/GHSA-2026-ax91-r7pp | GitHub Advisory |
| CVE-2026-44492 | https://www.cve.org/CVERecord?id=CVE-2026-44492 | CVE Record |

## Existing Issue Links

None -- no existing links on TC-8010.

## Existing Comments

None.

## Ecosystem Detection

- **axios** is an npm package (JavaScript/TypeScript HTTP client)
- Ecosystem: **npm** (source dependency)
- Per the ecosystem classification table, npm is a source dependency ecosystem
- Standard remediation would produce 2 tasks per stream (dependency bump + downstream propagation) when the upstream fix is available

## Deployment Context

- Affected repository from component label: rhtpa-ui
- Not found in Source Repositories table (only rhtpa-backend is configured)
- Default deployment context: **upstream**

## Notes

- The description states the vulnerability exists because axios does not properly validate hostnames in URLs when following redirects
- An attacker can craft a URL that initially resolves to an external host but redirects to an internal service
- The fix is in axios version 1.8.2 or later
