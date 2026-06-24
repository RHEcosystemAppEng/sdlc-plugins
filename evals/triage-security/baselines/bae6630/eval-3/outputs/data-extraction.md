# Data Extraction (Step 1) -- TC-8003

## Step 0 -- Configuration Validation

The project CLAUDE.md (claude-md-security-config.md) contains all required sections:

- **Repository Registry**: rhtpa-backend (Rust backend service)
- **Jira Configuration**: Project key TC, Cloud ID 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Code Intelligence**: Serena instance `serena_backend` for rhtpa-backend with rust-analyzer
- **Security Configuration**: Complete with Product Lifecycle, Version Streams, and Source Repositories

### Extracted Configuration Values

| Config Field | Value |
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

## Step 1 -- Parsed CVE Data from TC-8003

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] (stream suffix) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: rhtpa-release.0.4.z). This issue is scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo** with:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Repository: backend

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- no external API calls made per eval instructions)

The Jira description states:
- Affected range: versions before 0.11.14
- Fixed version: 0.11.14

These values are used as the fix threshold for version impact analysis in Step 2.

## Step 2 -- Version Impact Analysis

### Supportability Matrix (2.2.x stream, from security-matrix-mock.md)

| Version | Build | Build Date | backend | Notes |
|---------|-------|------------|---------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### quinn-proto Versions by Tag (from mock lock file data)

| Tag | quinn-proto version |
|-----|---------------------|
| v0.4.5 | 0.11.9 |
| v0.4.8 | 0.11.12 |
| v0.4.9 | (retag of v0.4.8) |
| v0.4.11 | 0.11.14 |
| v0.4.12 | 0.11.14 |

### Version Impact Table (2.2.x stream -- issue scope)

Fix threshold: < 0.11.14 (versions before 0.11.14 are vulnerable)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Cross-stream Impact (2.1.x stream -- outside issue scope)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.11.9 | YES | < 0.11.14 |

The 2.1.x stream is also affected but is outside this issue's scope (the issue is scoped to [rhtpa-2.2]).
