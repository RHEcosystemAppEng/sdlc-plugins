# Data Extraction — TC-8003

## Step 0 — Configuration Validation

Configuration validated from CLAUDE.md:

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

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

Deployment context: `upstream` (default — no Deployment Context column in Source Repositories table).

## Step 0.3 — Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (3 days ago). Within the 14-day freshness threshold. Proceeding.

## Step 1 — Extracted CVE Data

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
| Ecosystem | Cargo (Rust crate) |

### Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to the 2.2.x stream only.

### Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

### Deployment Context

Repository `rhtpa-backend` has deployment context: **upstream** (default, no Deployment Context column configured).
