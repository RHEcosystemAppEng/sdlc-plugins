# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| CVSS | 8.1 (High) |
| Existing comments | _(none)_ |

## Custom Fields

| Custom Field | Value |
|--------------|-------|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: **Source dependency**
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)

## Vulnerability Description

A vulnerability was found in axios. The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
