# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Issue Type | Vulnerability |
| Status | New |
| Vulnerable Library | axios |
| Ecosystem | npm |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version | 1.8.2 |
| CVSS | 8.1 (High) |
| Vulnerability Type | Server-Side Request Forgery (SSRF) |
| Affects Versions (PSIRT) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Component Label | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local path: `/home/dev/repos/rhtpa-release.0.4.z`
- Issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

- Library `axios` is a JavaScript/TypeScript npm package.
- Ecosystem: **npm** (source dependency category).
- Per ecosystem classification: source dependency ecosystems produce **2 remediation tasks** per stream (upstream backport + downstream propagation).

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Existing Issue Links

None (no existing links on TC-8010).

## Existing Comments

None.

## Description Summary

The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation when following redirects. An attacker can exploit this to make requests to internal services.

## Deployment Context

The affected repository (rhtpa-ui) was not found in the Source Repositories table (which only lists rhtpa-backend). Default deployment context: **upstream**.
