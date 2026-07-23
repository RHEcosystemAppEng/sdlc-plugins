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
| CVSS | 8.1 (High) |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to stream: **2.2.x** (matches Version Streams row: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: **axios** -- an npm package (JavaScript/TypeScript)
- Ecosystem: **npm**
- The security-matrix.md for the 2.2.x stream lists Cargo and RPM ecosystem mappings but does not include an npm ecosystem mapping for the rhtpa-ui component. Automated lock file inspection is not available for this ecosystem/component in the current matrix configuration.

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Remote Links

| Title | URL | Type |
|-------|-----|------|
| GHSA-2026-ax91-r7pp | https://github.com/advisories/GHSA-2026-ax91-r7pp | GitHub Advisory |
| CVE-2026-44492 | https://www.cve.org/CVERecord?id=CVE-2026-44492 | CVE Record |
