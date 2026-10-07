# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | (none extracted from remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | (none) |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches the 2.2.x row in the Version Streams table)
- Issue stream scope: **scoped to 2.2.x only**

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: Source dependency
- Remediation tasks per stream (if needed): 2 (dependency bump + downstream propagation)

## Custom Fields

| Custom Field | Value |
|--------------|-------|
| customfield_10632 (Upstream Affected Component) | axios |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |

## Deployment Context

- Repository rhtpa-backend mapped from Source Repositories table
- Deployment context: upstream (default -- no explicit Deployment Context column in Source Repositories)
