# Data Extraction -- TC-8003

## Step 0 -- Configuration Validation

| Setting | Value |
|---------|-------|
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

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | upstream (default) |

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md has a `Last-Updated: 2026-06-28T10:00:00Z` timestamp. As of today (2026-07-02), this is 4 days old, which is within the 14-day staleness threshold. No staleness warning required.

## Step 1 -- Parsed CVE Data

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
| Assignee | Unassigned |
| Existing comments | None |

### Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table. This issue is scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem: **Cargo** (source dependency)

### Deployment Context

The component label `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`. Deployment context: **upstream** (default, no Deployment Context column present).

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Step 1.7 is skipped.

## Step 2 -- Version Impact Analysis

### Version Impact Table (scoped to stream 2.2.x)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Cross-stream reference (2.1.x -- outside issue scope)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

Note: 2.1.x versions are outside the scope of TC-8003 (scoped to [rhtpa-2.2]) and would be tracked by a separate CVE issue for the 2.1.x stream.

### Affected versions within issue scope (2.2.x)

RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 are affected. RHTPA 2.2.3 and RHTPA 2.2.4 are not affected (ship quinn-proto 0.11.14, which is the fixed version).
