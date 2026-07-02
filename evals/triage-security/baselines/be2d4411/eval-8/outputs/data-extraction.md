# Step 1 -- Data Extraction for TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Vulnerable Library | axios |
| Affected Version Range | versions before 1.8.2 |
| Fixed Version (fix threshold) | 1.8.2 |
| CVSS | 8.1 (High) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Labels | CVE-2026-44492, pscomponent:org/rhtpa-ui |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Existing Issue Links | None |
| Existing Comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row: 2.2.x at git.example.com/rhtpa/rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Vulnerable library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- The security-matrix.md Ecosystem Mappings for stream 2.2.x list Cargo and RPM ecosystems. npm is not listed in the configured Ecosystem Mappings table for this stream.
- Note: Since the issue involves axios (an npm package), and the component is `rhtpa-ui`, the version impact analysis would normally require npm lock file configuration. However, the triage proceeds through Step 4.3 cross-CVE overlap detection which operates on Jira metadata rather than lock file inspection.

## Custom Fields Relevant to Step 4.3

- **customfield_10632** (Upstream Affected Component): `axios` -- used for cross-CVE overlap JQL search
- **customfield_10669** (PS Component): `pscomponent:org/rhtpa-ui` -- used for filtering overlap results
- **customfield_10832** (Stream): `rhtpa-2.2` -- used for filtering overlap results
