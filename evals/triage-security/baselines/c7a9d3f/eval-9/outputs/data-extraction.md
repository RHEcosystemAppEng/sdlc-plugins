# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8011

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Issue Key | TC-8011 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-ui |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Existing Comments | None |
| Existing Issue Links | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: **webpack** -- this is an npm package (JavaScript/TypeScript)
- Ecosystem: **npm**
- Lock file: determined by the Ecosystem Mappings table in the stream's `security-matrix.md`
- Remediation pattern: **2 tasks** (upstream backport + downstream propagation) since npm is a source dependency ecosystem

## Labels

- `CVE-2026-45678` -- CVE identifier
- `pscomponent:org/rhtpa-ui` -- PS Component label

## Vulnerability Details

The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process. The fix requires upgrading webpack to version 5.98.0 or later.
