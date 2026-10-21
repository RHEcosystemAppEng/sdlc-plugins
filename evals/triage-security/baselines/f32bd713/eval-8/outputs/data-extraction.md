# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-44492 |
| **Issue Key** | TC-8010 |
| **Summary** | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | pscomponent:org/rhtpa-ui |
| **Vulnerable Library** | axios |
| **Affected Version Range** | versions before 1.8.2 |
| **Fixed Version (Fix Threshold)** | 1.8.2 |
| **CVSS Score** | 8.1 (High) |
| **PSIRT-Claimed Product Version** | [rhtpa-2.2] |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |

## Custom Fields

| Custom Field | Field ID | Value |
|-------------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Remote Links

| Title | URL | Type |
|-------|-----|------|
| GHSA-2026-ax91-r7pp | https://github.com/advisories/GHSA-2026-ax91-r7pp | GitHub Advisory |
| CVE-2026-44492 | https://www.cve.org/CVERecord?id=CVE-2026-44492 | CVE Record |

## Existing Issue Links

No existing issue links on TC-8010.

## Existing Comments

No comments on TC-8010.

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.2]`
- **Mapped stream**: 2.2.x
- **Stream scope**: Scoped -- this issue is scoped to the 2.2.x version stream only
- **Matching Version Stream**: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`

## Ecosystem Detection

- **Vulnerable library**: axios
- **Ecosystem**: npm (JavaScript/TypeScript package)
- **Category**: Source dependency
- **Note**: The security-matrix.md for stream 2.2.x lists Cargo and RPM ecosystems in its Ecosystem Mappings table. The npm ecosystem is not listed in the matrix's Ecosystem Mappings. However, the cross-CVE overlap check (Step 4.3) takes precedence before ecosystem-specific remediation would be needed.

## Deployment Context Lookup

- **Affected repository** (from component label `pscomponent:org/rhtpa-ui`): rhtpa-ui
- **Source Repositories table**: rhtpa-backend is listed, rhtpa-ui is not explicitly listed
- **Deployment context**: upstream (default, since rhtpa-ui is not found in the Source Repositories table)

## Vulnerability Description

A vulnerability was found in axios. The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
