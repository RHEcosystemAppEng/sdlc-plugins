# Step 1 -- Data Extraction: TC-8010

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Jira Issue Key | TC-8010 |
| Summary | CVE-2026-44492 axios - Server-Side Request Forgery via crafted URL [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
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
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Existing Comments | None |
| Existing Issue Links | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`.

- Parsed suffix: `rhtpa-2.2` -> stream `2.2.x`
- Matched to Version Streams table: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript package)
- The security-matrix.md for the 2.2.x stream includes Cargo and RPM ecosystem mappings. npm is not listed in the Ecosystem Mappings table for this stream.

Note: Although the npm ecosystem is not configured in the stream's Ecosystem Mappings, the cross-CVE overlap analysis (Step 4.3) can still proceed based on the Upstream Affected Component field, which identifies `axios` as the shared component across CVE Jiras.

## Deployment Context

The affected repository (`rhtpa-ui`) is identified from the component label `pscomponent:org/rhtpa-ui`. Looking up the Source Repositories table, `rhtpa-ui` is not explicitly listed (only `rhtpa-backend` is configured). Deployment context defaults to `upstream`.
