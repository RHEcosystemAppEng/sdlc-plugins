# Step 1 -- Data Extraction: TC-8021

## Step 0 -- Configuration Validation

Configuration validated from CLAUDE.md:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md file has a `Last-Updated: 2026-06-28T10:00:00Z` timestamp. As of the current date (2026-07-29), this is 31 days old, which exceeds the 14-day staleness threshold. In a live triage, the engineer would be warned and asked whether to refresh, proceed, or stop. For this eval, we proceed with the current matrix data.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Jira Issue Key | TC-8021 |
| CVE ID | CVE-2026-31812 |
| Affected component label | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed, from summary suffix) | [rhtpa-2.2] |
| Affects Versions (Jira field, PSIRT-assigned) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS score | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| RustSec advisory | [RUSTSEC-2026-0042](https://rustsec.org/advisories/RUSTSEC-2026-0042.html) |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`. This maps to the **2.2.x** version stream in the configured Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x (scoped to a single stream)

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings tables in the security matrix, the ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.2.x stream): `release/0.4.z`
- Ecosystem category: **Source dependency** -- produces 2 remediation tasks per affected stream (upstream backport + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories. No Deployment Context column is present in the configuration, so the default deployment context is **upstream**.

## Step 2 -- Version Impact Analysis

Using the lock file data from the security matrix, the following version impact table was constructed by comparing each version's pinned quinn-proto version against the fix threshold (0.11.14):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Product Version | Build Tag | quinn-proto Version | Affected? | Notes |
|-----------------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Product Version | Build Tag | quinn-proto Version | Affected? | Notes |
|-----------------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Summary

- **Stream 2.2.x (issue scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14).
- **Stream 2.1.x (outside issue scope)**: All versions (2.1.0, 2.1.1) are affected. This triggers Case A (cross-stream impact).

### Step 3 -- Affects Versions Correction

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`. This is incorrect -- there is no 2.0.x stream in the configured Version Streams. Based on the version impact analysis scoped to the 2.2.x stream:

- **Current (PSIRT-assigned)**: `[RHTPA 2.0.0]`
- **Proposed (lock-file-verified)**: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14 (the fixed version). The correction is scoped to stream 2.2.x per the issue's `[rhtpa-2.2]` suffix.
