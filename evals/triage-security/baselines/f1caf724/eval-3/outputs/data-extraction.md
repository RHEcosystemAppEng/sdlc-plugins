# Data Extraction -- TC-8003

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

| Parameter | Value |
|-----------|-------|
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

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has a `Last-Updated` timestamp of `2026-06-28T10:00:00Z`.
Current date: 2026-08-24. That is 57 days ago, which exceeds the 14-day staleness threshold.

Staleness warning would be presented to the user before proceeding. For this evaluation, we proceed with the current matrix data.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to the **2.2.x** version stream.
This issue is **scoped** to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table includes **Cargo** with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem classification: **Source dependency (Cargo)** -- remediation would require 2 tasks per stream (upstream backport + downstream propagation).

## Step 2 -- Version Impact Analysis

Using mock lock file data from security-matrix-mock.md:

### Version Impact Table for CVE-2026-31812 (quinn-proto < 0.11.14)

**Stream 2.2.x (issue scope):**

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | = 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | = 0.11.14 (fixed version) |

**Stream 2.1.x (cross-stream, outside issue scope):**

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Summary

- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3+ ship the fix.
- **2.1.x stream**: Both versions 2.1.0 and 2.1.1 are affected (cross-stream impact, outside this issue's scope).
- The fix was introduced at build tag v0.4.11 (quinn-proto 0.11.14), which corresponds to product version RHTPA 2.2.3.
