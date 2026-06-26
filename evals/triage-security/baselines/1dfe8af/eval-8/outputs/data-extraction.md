# Step 1 -- Data Extraction: TC-8010

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8010 |
| **CVE ID** | CVE-2026-44492 |
| **Summary** | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | pscomponent:org/rhtpa-ui |
| **Upstream Affected Component** (customfield_10632) | axios |
| **PS Component** (customfield_10669) | pscomponent:org/rhtpa-ui |
| **Stream** (customfield_10832) | rhtpa-2.2 |
| **Product Version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable Library** | axios |
| **Affected Version Range** | versions before 1.8.2 |
| **Fixed Version (fix threshold)** | 1.8.2 |
| **CVSS** | 8.1 (High) |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| **CVE Record URL** | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| **Existing Issue Links** | None |
| **Existing Comments** | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry: stream 2.2.x at rhtpa-release.0.4.z)
- Issue stream scope: **rhtpa-2.2 / 2.2.x only**

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Lock file: determined by the stream's security-matrix.md Ecosystem Mappings table
- Note: The security-matrix-mock.md does not include an npm ecosystem mapping (it only has Cargo and RPM), but axios is unambiguously an npm package

## Custom Fields for Cross-CVE Search

- **customfield_10632** (Upstream Affected Component): `axios` -- used in Step 4.3 for cross-CVE overlap detection
- **customfield_10669** (PS Component): `pscomponent:org/rhtpa-ui` -- used for filtering related CVE results
- **customfield_10832** (Stream): `rhtpa-2.2` -- used for filtering related CVE results
