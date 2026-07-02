# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8021 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only. Steps 3 and 4 will apply to 2.2.x versions; other streams (2.1.x) are handled via Case B cross-stream impact analysis.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. Both the 2.1.x and 2.2.x streams have Cargo ecosystem mappings configured in their security-matrix.md files.

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with no explicit Deployment Context column. Defaulting to `upstream`.

## Version Impact Analysis (Step 2)

Using the mock lock file data from security-matrix-mock.md, the quinn-proto versions at each pinned tag are:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES | same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Summary

- **2.2.x stream (in scope)**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14 and are NOT affected.
- **2.1.x stream (out of scope)**: all versions (2.1.0, 2.1.1) are affected -- this triggers Case B cross-stream impact handling.
- **Affects Versions correction needed**: PSIRT assigned `RHTPA 2.0.0` which does not correspond to any configured version. Should be corrected to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (scoped to 2.2.x, affected versions only).
