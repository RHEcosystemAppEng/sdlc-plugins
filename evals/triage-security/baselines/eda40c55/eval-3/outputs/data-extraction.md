# Data Extraction -- TC-8003

## Step 0 -- Configuration Validation

Validated the following from CLAUDE.md (claude-md-security-config.md):

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has a `Last-Updated: 2026-06-28T10:00:00Z` timestamp. Current date is 2026-07-06, which is 8 days ago -- within the 14-day threshold. Matrix is not stale. Proceed without warning.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2]) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate) |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Deployment context | upstream (default -- repo not found by component label in Source Repositories) |

### Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`. This maps to the configured Version Stream `2.2.x` (Konflux release repo `rhtpa-release.0.4.z`). The issue is **stream-scoped** to 2.2.x only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table in the security matrix for stream 2.2.x includes `Cargo` with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. Ecosystem is **Cargo**.

### Embargo Check (Step 1.7)

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped entirely.

## Step 2 -- Version Impact Analysis

### Stream 2.2.x (scoped stream -- rhtpa-release.0.4.z)

Lock file: `Cargo.lock` in repository `backend`
Check command: `git show <tag>:Cargo.lock`

| Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|-------------|---------------------|-----------|----------|
| RHTPA 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 (fix threshold) |
| RHTPA 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 (fix threshold) |
| RHTPA 2.2.2 | 0.4.9 | v0.4.8 (retag) | 0.11.12 | **YES** | Same as 2.2.1 (retag of v0.4.8) |
| RHTPA 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (at fix threshold) |
| RHTPA 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (at fix threshold) |

### Stream 2.1.x (cross-stream check -- rhtpa-release.0.3.z)

| Version | Build | Backend Tag | quinn-proto Version | Affected? | Evidence |
|---------|-------|-------------|---------------------|-----------|----------|
| RHTPA 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 (fix threshold) |
| RHTPA 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 (fix threshold) |

### Summary

- Stream 2.2.x: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 are NOT affected (fixed in 0.4.11 build)
- Stream 2.1.x: versions 2.1.0 and 2.1.1 are affected (cross-stream impact -- outside this issue's scope)
- The fix was introduced in build 0.4.11 (tag v0.4.11), which ships quinn-proto 0.11.14
