# Data Extraction — TC-8003

## Step 0 — Configuration Validation

Project configuration validated from `claude-md-security-config.md`:

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Step 0.3 — Matrix Staleness Check

Matrix `Last-Updated: 2026-06-28T10:00:00Z` — 120 days ago (as of 2026-10-26). This exceeds the 14-day threshold, so a staleness warning would be raised in interactive mode. For this eval, we proceed with the current matrix data.

## Step 1 — Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream `2.2.x`. This issue is **stream-scoped** to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table includes Cargo with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem classification: **Source dependency** (Cargo) — would normally produce 2 remediation tasks per stream (upstream backport or dependency bump + downstream propagation).

## Step 2 — Version Impact Analysis

Using the mock lock file data from `security-matrix-mock.md`:

### 2.2.x Stream (issue scope)

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### 2.1.x Stream (cross-stream check — outside issue scope)

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are fixed
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected (relevant for Case A cross-stream impact)
- The fix was introduced at tag v0.4.11 (quinn-proto 0.11.14) which corresponds to version 2.2.3

### Step 2.5 — Upstream Fix Status

The fix version is 0.11.14. The latest releases in the 2.2.x stream (2.2.3 and 2.2.4) already ship quinn-proto 0.11.14, confirming the upstream fix is available. This means remediation tasks would use the "dependency bump" variant rather than "upstream backport."
