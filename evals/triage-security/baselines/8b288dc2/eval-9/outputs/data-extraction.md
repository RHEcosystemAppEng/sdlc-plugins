# Step 1 -- Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | -- (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Custom Fields

| Field | ID | Value |
|-------|----|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table in Security Configuration)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Vulnerable library: **webpack** -- this is an npm package (JavaScript/TypeScript bundler)
- Ecosystem: **npm**
- Lock file: `package-lock.json` (or equivalent npm lock file)
- Remediation pattern: **2 tasks** (upstream backport + downstream propagation) since npm is a source dependency ecosystem

## Deployment Context Lookup

- Affected repository from component label: rhtpa-ui (from `pscomponent:org/rhtpa-ui`)
- Source Repositories table lookup: rhtpa-ui is **not found** in the Source Repositories table (only rhtpa-backend is listed)
- Deployment context: **upstream** (default, since the repository is not in the table)

## Issue Links

No existing issue links on TC-8011.

## Remote Links

- GitHub Advisory: GHSA-2026-wk55-m3rr
- CVE Record: CVE-2026-45678
