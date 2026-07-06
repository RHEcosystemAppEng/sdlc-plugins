# Data Extraction -- TC-8003

## Step 0 -- Configuration Validation

The following configuration was extracted from the project CLAUDE.md (claude-md-security-config.md):

| Setting | Value |
|---------|-------|
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

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

All required Security Configuration sections are present. Proceeding with triage.

## Step 0.3 -- Matrix Staleness Check

The security matrix has a `Last-Updated` timestamp of `2026-06-28T10:00:00Z` (8 days ago as of 2026-07-06). This is within the 14-day staleness threshold. No staleness warning needed.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8003 |
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
| Status | New |

### Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z). This issue is **stream-scoped** to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a supported ecosystem with:
- Repository: backend
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

### Deployment Context

The affected repository `rhtpa-backend` has deployment context: **upstream** (default, since no Deployment Context column is present in Source Repositories).

## Step 2 -- Version Impact Analysis (Stream 2.2.x)

Using the security matrix data for stream rhtpa-release.0.4.z (2.2.x), the following dependency versions were extracted for quinn-proto at each pinned commit:

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as RHTPA 2.2.1 |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed version) |

**Summary**: RHTPA 2.2.0, 2.2.1, and 2.2.2 are affected. RHTPA 2.2.3 and 2.2.4 are not affected (they ship the fixed version 0.11.14).

The fix was introduced in build tag v0.4.11 (RHTPA 2.2.3), which first picked up quinn-proto 0.11.14.
