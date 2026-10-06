# Step 1 -- Data Extraction for TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
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
| Existing comments | None |
| Upstream fix PR | Not provided in remote links |
| Issue status | New |
| Assignee | Unassigned |

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

- Library: axios (JavaScript/TypeScript HTTP client)
- Ecosystem: **npm**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)

## Vulnerability Summary

A Server-Side Request Forgery (SSRF) vulnerability in the axios package before version 1.8.2 allows an attacker to craft a URL that bypasses hostname validation when following redirects, enabling requests to internal services. The fix threshold is axios >= 1.8.2.
