# Step 1 -- Data Extraction for TC-8011

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-45678 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-ui | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.2.0 | Jira `versions` field |
| Vulnerable library | webpack | Description text |
| Affected version range | versions before 5.98.0 | Description text |
| Fixed version | 5.98.0 | Description text |
| CVSS | 7.8 (High) | Description text |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 | Remote links |
| Due date | 2026-08-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |

## Custom Fields

| Field | ID | Value |
|-------|----|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table in Security Configuration)
- Issue is **stream-scoped** to stream 2.2.x only

## Ecosystem Detection

- Vulnerable library: **webpack** (npm package)
- Ecosystem: **npm** (JavaScript/TypeScript package manager)
- Classification: **Source dependency** ecosystem
- Task structure: 2 tasks per stream (dependency bump or upstream backport + downstream propagation)

Note: The security-matrix.md Ecosystem Mappings for stream 2.2.x list Cargo and RPM but do **not** include npm. This means automated lock file inspection via the matrix is not available for this ecosystem in the current configuration. The version impact analysis for webpack would need npm to be added to the Ecosystem Mappings, or manual assessment would be required.

## Deployment Context

- Affected repository from component label: org/rhtpa-ui
- The Source Repositories table in CLAUDE.md lists `rhtpa-backend` but not `rhtpa-ui`
- Deployment context: defaults to `upstream` (repository not found in Source Repositories table)
