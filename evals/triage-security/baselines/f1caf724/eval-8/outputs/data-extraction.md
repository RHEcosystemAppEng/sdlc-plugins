# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Jira Issue Key | TC-8010 |
| CVE ID | CVE-2026-44492 |
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
| CVSS Score | 8.1 (High) |
| Ecosystem | npm |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary stream suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x**
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local Path: /home/dev/repos/rhtpa-release.0.4.z
- This issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Ecosystem category: **Source dependency**
- Remediation task pattern: 2 tasks per stream (upstream backport + downstream propagation)

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Existing Issue Links

No existing links on TC-8010.

## Existing Comments

No comments on TC-8010.

## Vulnerability Description

A vulnerability was found in axios. The axios package before version 1.8.2 is
vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses
hostname validation. An attacker can exploit this to make requests to internal
services. The vulnerability exists because axios does not properly validate the
hostname in URLs when following redirects. An attacker can craft a URL that
initially resolves to an external host but redirects to an internal service.
