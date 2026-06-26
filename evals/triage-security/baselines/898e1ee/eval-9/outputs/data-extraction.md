# Step 1 -- Data Extraction: TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8011 |
| CVE ID | CVE-2026-45678 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Stream Suffix | [rhtpa-2.2] |
| Stream Scope | 2.2.x (mapped to Konflux release repo rhtpa-release.0.4.z) |
| Affects Versions (PSIRT-assigned) | RHTPA 2.2.0 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |

## Vulnerability Details

| Field | Value |
|-------|-------|
| Vulnerable Library | webpack |
| Affected Version Range | versions before 5.98.0 |
| Fixed Version (fix threshold) | 5.98.0 |
| CVSS Score | 7.8 (High) |
| Ecosystem | npm |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-45678 |

## Issue Links

No existing issue links.

## Comments

No existing comments.

## Stream Scope Resolution

The summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration's Version Streams table. The corresponding Konflux release repo is `git.example.com/rhtpa/rhtpa-release.0.4.z` at local path `/home/dev/repos/rhtpa-release.0.4.z`.

This issue is **stream-scoped** to 2.2.x only. Steps 3-7 will be scoped to this single stream.

## Ecosystem Detection

The vulnerable library is **webpack**, which is a JavaScript/npm package. The ecosystem is **npm**. Lock file inspection will use the npm lock file (e.g., `package-lock.json` or `yarn.lock`) as configured in the stream's `security-matrix.md` Ecosystem Mappings table.
