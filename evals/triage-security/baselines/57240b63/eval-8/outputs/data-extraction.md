# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-01 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Existing comments | None |
| Existing issue links | None |

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x**
- Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z
- Local path: /home/dev/repos/rhtpa-release.0.4.z
- This issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Note: The 2.2.x stream's security-matrix.md Ecosystem Mappings table lists Cargo and RPM ecosystems but does not list npm. In a live triage this would trigger: "Unsupported ecosystem: npm is not yet supported for automated triage. Manual assessment is required." However, the cross-CVE overlap analysis (Step 4.3) can still proceed using the Upstream Affected Component field to find related CVE Jiras and their remediation tasks.

## Deployment Context Lookup

- Affected repository from component label: rhtpa-ui (derived from pscomponent:org/rhtpa-ui)
- Source Repositories table lists: rhtpa-backend
- rhtpa-ui is not found in the Source Repositories table -- defaulting deployment context to: **upstream**

## Vulnerability Description

A vulnerability was found in axios. The axios package before version 1.8.2 is vulnerable to Server-Side Request Forgery (SSRF) via a crafted URL that bypasses hostname validation. An attacker can exploit this to make requests to internal services. The vulnerability exists because axios does not properly validate the hostname in URLs when following redirects.
