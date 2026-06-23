# Step 1 -- Data Extraction for TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8010 |
| **CVE ID** | CVE-2026-44492 |
| **Summary** | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| **Issue Type** | Vulnerability (ID: 10024) |
| **Status** | New |
| **Affected Component (label)** | pscomponent:org/rhtpa-ui |
| **Product Version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable Library** | axios |
| **Affected Version Range** | versions before 1.8.2 |
| **Fixed Version** | 1.8.2 |
| **CVSS** | 8.1 (High) |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **Existing Comments** | None |
| **Existing Issue Links** | None |

## Custom Fields

| Custom Field | Field ID | Value |
|--------------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Parsed stream**: 2.2.x
- **Configured Version Streams**: 2.1.x, 2.2.x
- **Match**: YES -- suffix `rhtpa-2.2` maps to stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- **Issue stream scope**: 2.2.x only (Steps 3-7 are scoped to this stream)

## Ecosystem Detection

- **Library**: axios
- **Ecosystem**: npm (JavaScript/TypeScript package)
- The security-matrix.md for stream 2.2.x has Ecosystem Mappings for Cargo and RPM, but not explicitly for npm. The axios library is an npm package used by the `rhtpa-ui` component (as indicated by the PS Component label `pscomponent:org/rhtpa-ui`).

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-44492 |

## Vulnerability Description

axios before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects. An attacker can craft a URL that initially resolves to an external host but redirects to an internal service.
