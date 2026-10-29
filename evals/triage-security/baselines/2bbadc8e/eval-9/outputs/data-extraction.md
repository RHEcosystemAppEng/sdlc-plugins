# Step 1 -- Data Extraction: TC-8011

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Jira Issue Key | TC-8011 |
| Issue Type | Vulnerability |
| Status | New |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version (fix threshold) | 5.98.0 |
| CVSS Score | 7.8 (High) |
| Affects Versions (PSIRT-assigned) | RHTPA 2.2.0 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Labels | CVE-2026-45678, pscomponent:org/rhtpa-ui |
| Existing Issue Links | (none) |
| Existing Comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream in the Security Configuration Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to stream 2.2.x only.

## Remote Links

| Title | URL |
|-------|-----|
| GHSA-2026-wk55-m3rr | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE-2026-45678 | https://www.cve.org/CVERecord?id=CVE-2026-45678 |

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/TypeScript build tool -- an **npm** ecosystem package.

The security-matrix.md Ecosystem Mappings for stream 2.2.x list Cargo and RPM ecosystems. npm is not present in the configured Ecosystem Mappings table for this stream.

**Note:** If npm were configured, the ecosystem classification would be "Source dependency" requiring two remediation tasks per stream (dependency bump + downstream propagation, since the fix version 5.98.0 is a released upstream version).

## Vulnerability Details

The vulnerability exists because webpack does not properly sanitize loader paths when resolving the loader chain, allowing path traversal to execute arbitrary modules. An attacker with control over a project's webpack configuration can execute arbitrary code during the build process.
