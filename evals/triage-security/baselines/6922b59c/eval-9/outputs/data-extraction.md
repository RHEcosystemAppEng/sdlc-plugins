# Step 1 -- Data Extraction for TC-8011

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Jira Issue Key | TC-8011 |
| CVE ID | CVE-2026-45678 |
| Summary | CVE-2026-45678 webpack - Arbitrary Code Execution via loader chain [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component (label) | pscomponent:org/rhtpa-ui |
| Upstream Affected Component (customfield_10632) | webpack |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |
| Product version (PSIRT-claimed, from summary suffix) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 |
| Fixed version (fix threshold) | 5.98.0 |
| CVSS | 7.8 (High) |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Existing Issue Links | None |
| Existing Comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to the 2.2.x stream only

## Ecosystem Detection

- Library: webpack
- Ecosystem: **npm** (JavaScript/TypeScript package)
- Classification: **Source dependency** ecosystem
- Remediation task count per stream: **2** (dependency bump + downstream propagation, assuming upstream fix is available)

## Deployment Context

- Affected repository (from component label pscomponent:org/rhtpa-ui): rhtpa-ui
- Deployment context: upstream (default, since rhtpa-ui is not explicitly listed in Source Repositories)

## Version Impact Analysis (Step 2)

Based on the security matrix for the 2.2.x stream (rhtpa-release.0.4.z), webpack is an npm dependency. The security matrix mock does not include npm lock file data for webpack -- in a real triage the lock files at each pinned commit would be inspected. However, the issue description states webpack versions before 5.98.0 are affected, and the related CVE TC-8012's remediation task TC-8013 confirms the product was shipping webpack (bumped from 5.95.0 to 5.96.1 for that CVE). Since the bump to 5.96.1 is below the 5.98.0 fix threshold, all 2.2.x versions remain affected by CVE-2026-45678.

| Version | webpack (estimated) | Affected? | Notes |
|---------|---------------------|-----------|-------|
| 2.2.0 | <= 5.95.0 | YES | Before TC-8013 bump |
| 2.2.1 | <= 5.95.0 | YES | Before TC-8013 bump |
| 2.2.2 | -- | YES | Retag of 2.2.1 |
| 2.2.3 | 5.96.1 | YES | After TC-8013 bump, still below 5.98.0 |
| 2.2.4 | 5.96.1 | YES | After TC-8013 bump, still below 5.98.0 |

All 2.2.x versions ship webpack below 5.98.0 and are therefore affected.
