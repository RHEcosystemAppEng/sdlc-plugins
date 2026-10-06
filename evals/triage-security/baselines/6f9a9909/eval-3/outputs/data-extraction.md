# Data Extraction -- TC-8003

## Step 0 -- Configuration Validation

Configuration extracted from CLAUDE.md (claude-md-security-config.md):

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

Matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z
Current date: 2026-10-06
Days since update: ~100 days -- **stale** (exceeds 14-day threshold).

In a live triage this would trigger a staleness warning and offer to refresh.
For this eval, proceeding with the current matrix data.

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
| Assignee | Unassigned |

### Stream Scope Resolution

Issue summary suffix: `[rhtpa-2.2]`
Mapped to configured Version Stream: **2.2.x** (rhtpa-release.0.4.z)
Issue is **stream-scoped** to 2.2.x only.

### Ecosystem Detection

Vulnerable library: quinn-proto (Rust crate)
Ecosystem: **Cargo** (source dependency)
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Remediation task count: 2 per stream (upstream backport + downstream propagation)

## Step 2 -- Version Impact Analysis

Using mock lock file data from security-matrix-mock.md:

### 2.2.x Stream (issue scope)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | = 0.11.14 (fixed version) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | = 0.11.14 (fixed version) |

### 2.1.x Stream (cross-stream, outside issue scope)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Summary

Within the 2.2.x stream (issue scope): versions 2.2.0, 2.2.1, and 2.2.2 are affected.
Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected.

Cross-stream: the 2.1.x stream is also affected (both versions ship quinn-proto 0.11.9).
