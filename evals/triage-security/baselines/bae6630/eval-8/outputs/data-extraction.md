# Step 1 -- Data Extraction for TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Existing comments | None |
| Existing issue links | None |
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches the `rhtpa-release.0.4.z` Konflux release repo from Version Streams table)
- Scope: **Scoped** -- Steps 3-7 apply only to the 2.2.x stream

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (axios is a JavaScript/TypeScript HTTP client package)
- Lock file: `package-lock.json` (per npm ecosystem conventions)
- This is a source dependency ecosystem, so remediation would normally require two tasks (upstream backport + downstream propagation)

## Vulnerability Summary

A Server-Side Request Forgery (SSRF) vulnerability in axios before version 1.8.2. The package does not properly validate hostnames in URLs when following redirects, allowing an attacker to craft a URL that initially resolves to an external host but redirects to an internal service. Fix threshold: upgrade to axios >= 1.8.2.
