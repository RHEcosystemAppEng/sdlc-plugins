# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will operate within that stream scope, but version impact analysis (Step 2) covers all streams to enable cross-stream impact detection (Case A).

## Ecosystem Detection

- **Ecosystem**: Cargo (quinn-proto is a Rust crate)
- **Category**: Source dependency
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)

## Deployment Context Lookup

The affected repository (rhtpa-backend) is listed in Source Repositories. The Deployment Context column is absent from the Source Repositories table in the mock configuration, so the deployment context defaults to `upstream`.

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but no `2.0.x` stream exists in the Version Streams configuration. The streams configured are 2.1.x and 2.2.x. This is a clear mismatch that will be corrected in Step 3 after version impact analysis confirms which 2.2.x versions are actually affected.

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md:

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 both ship quinn-proto 0.11.9)
- **2.2.x stream**: versions 2.2.0-2.2.2 affected; versions 2.2.3-2.2.4 ship the fixed version (0.11.14)
- The fix was picked up starting at build tag v0.4.11 (version 2.2.3)
