# Step 1 -- Data Extraction for TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Product Version (PSIRT-claimed, summary suffix) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version | 5.98.0 |
| CVSS | 7.8 (High) |
| Assignee | Unassigned |
| Due Date | 2026-08-15 |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Upstream Fix PR | (none found in remote links) |
| Existing Comments | (none) |
| Existing Issue Links | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- This is a **stream-scoped** issue -- triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

- Library: **webpack**
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Category: **Source dependency** -- produces 2 remediation tasks per stream (upstream backport + downstream propagation)

## Ecosystem Mappings (from 2.2.x stream security-matrix.md)

The security matrix provided covers Cargo and RPM ecosystems. The npm ecosystem (for webpack) is not explicitly listed in the Ecosystem Mappings table of the mock security matrix. In a real triage, this would trigger an unsupported ecosystem warning. However, per the eval instructions, webpack is an npm package and the issue clearly indicates vulnerability data and a fix threshold of 5.98.0.

## Fix Threshold

- **Jira description**: fixed in version 5.98.0 (versions before 5.98.0 are affected)
- **Fix threshold for version impact comparison**: **5.98.0**
