# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 (< 1.8.2) |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | (not provided in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Custom Fields

| Field | Field ID | Value |
|-------|----------|-------|
| Upstream Affected Component | customfield_10632 | axios |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Version Streams configuration. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **axios**, a JavaScript/TypeScript npm package. The ecosystem is **npm** based on the library name and component context. The Ecosystem Mappings in the security-matrix.md would be used to determine the lock file path (e.g., `package-lock.json`) and check command for npm dependencies.

Note: The security-matrix.md for the 2.2.x stream currently lists Cargo and RPM ecosystem mappings. If an npm ecosystem mapping is not present, the engineer should be consulted on where npm dependencies are tracked for this product (e.g., in a separate UI repository).
