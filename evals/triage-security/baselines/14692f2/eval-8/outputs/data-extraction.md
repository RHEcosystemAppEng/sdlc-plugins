# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8010 |
| **CVE ID** | CVE-2026-44492 |
| **Affected Component (label)** | pscomponent:org/rhtpa-ui |
| **Upstream Affected Component** (customfield_10632) | axios |
| **PS Component** (customfield_10669) | pscomponent:org/rhtpa-ui |
| **Stream** (customfield_10832) | rhtpa-2.2 |
| **Product version (PSIRT-claimed)** | [rhtpa-2.2] (from summary suffix) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable library** | axios |
| **Affected version range** | versions before 1.8.2 |
| **Fixed version (fix threshold)** | 1.8.2 |
| **CVSS** | 8.1 (High) |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| **Due Date** | 2026-08-01 |
| **Status** | New |
| **Assignee** | Unassigned |
| **Existing Issue Links** | None |
| **Existing Comments** | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to configured Version Stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- This is a source dependency ecosystem, so remediation (if needed) would require two tasks: upstream backport + downstream propagation

## Custom Fields Relevant to Step 4.3 (Cross-CVE Overlap)

All three fields required for cross-CVE overlap detection are present and populated:

- **Upstream Affected Component** (customfield_10632): `axios` -- will be used to search for related CVE Jiras
- **PS Component** (customfield_10669): `pscomponent:org/rhtpa-ui` -- will be used to filter results to same component
- **Stream** (customfield_10832): `rhtpa-2.2` -- will be used to filter results to same stream
