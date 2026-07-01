# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 (< 1.8.2) |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | (not listed in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Custom Fields

| Custom Field | Value |
|--------------|-------|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams configuration. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, a JavaScript/TypeScript npm package. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the supported ecosystems are **Cargo** and **RPM**. The **npm** ecosystem is not listed in the Ecosystem Mappings table.

However, the issue data explicitly identifies axios as the upstream affected component, and the fix threshold (1.8.2) is available from the Jira description. The cross-CVE overlap check (Step 4.3) will use this component information to search for related remediation tasks regardless of whether the npm ecosystem has a full lock file mapping configured.

## Issue Links

No existing issue links on TC-8010.

## Reporter

Reporter field: (PSIRT auto-created issue -- reporter information from Jira issue metadata)
