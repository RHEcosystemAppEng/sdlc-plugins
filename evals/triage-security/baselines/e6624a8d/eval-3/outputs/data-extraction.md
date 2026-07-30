# Data Extraction — TC-8003

## Step 0 — Configuration Validation

The project CLAUDE.md contains all required sections:

- **Repository Registry**: rhtpa-backend (Rust backend service)
- **Jira Configuration**: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`
- **Code Intelligence**: Serena instance `serena_backend` for rhtpa-backend (rust-analyzer)
- **Security Configuration**: Present and complete

### Extracted Configuration

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | Not configured |
| PS Component custom field | Not configured |
| Stream custom field | Not configured |
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

## Step 0.3 — Matrix Staleness Check

The security matrix has a `Last-Updated` timestamp of `2026-06-28T10:00:00Z`.
That is 32 days ago (relative to today, 2026-07-30), which exceeds the 14-day staleness threshold.

A staleness warning would be raised:

> Security matrix was last updated on 2026-06-28 (32 days ago). The matrix may not reflect recent releases.

For the purposes of this eval, we proceed with the current matrix data.

## Step 1 — Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

### Stream Scope Resolution

The summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
This issue is **scoped** to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table
includes **Cargo** with:
- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

Ecosystem classification: **Source dependency** (Cargo) -- remediation produces 2 tasks per stream (upstream backport + downstream propagation).

### Deployment Context

The affected repository `rhtpa-backend` has deployment context: **upstream** (default, since no Deployment Context column is present in the Source Repositories table).

## Step 1.7 — Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped.

## Step 2 — Version Impact Analysis (2.2.x stream)

Using the supportability matrix and mock lock file data for the 2.2.x stream:

| Version | Build Tag | quinn-proto Version | Affected (< 0.11.14)? | Notes |
|---------|-----------|--------------------|-----------------------|-------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES | Vulnerable |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES | Vulnerable |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 — same as 2.2.1 |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO | Fixed (ships exact fix version) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO | Fixed (ships exact fix version) |

### Cross-stream check (2.1.x stream, for Case A assessment)

Since the issue is scoped to 2.2.x, we also check the 2.1.x stream:

| Version | Build Tag | quinn-proto Version | Affected (< 0.11.14)? | Notes |
|---------|-----------|--------------------|-----------------------|-------|
| RHTPA 2.1.0 | v0.3.8 | 0.11.9 | YES | Vulnerable |
| RHTPA 2.1.1 | v0.3.12 | 0.11.9 | YES | Vulnerable |

The 2.1.x stream is also affected. However, duplicate/sibling analysis (Step 4) takes priority before considering cross-stream remediation.

### Summary

- **Affected versions in scope (2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected versions in scope (2.2.x)**: RHTPA 2.2.3, RHTPA 2.2.4
- **Cross-stream (2.1.x)**: RHTPA 2.1.0, RHTPA 2.1.1 are also affected
