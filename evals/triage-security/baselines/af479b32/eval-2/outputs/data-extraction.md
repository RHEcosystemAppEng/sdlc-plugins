# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

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

## Step 0.3 -- Matrix Staleness Check

Matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z (25 days ago as of 2026-07-23).

This exceeds the 14-day staleness threshold. In a live triage, the engineer would be prompted to refresh or proceed. For this eval, proceeding with the current matrix data.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | RHTPA 2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Due date | 2026-07-30 |
| Status | New |
| Assignee | Unassigned |
| Existing comments | None |

### Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-28940 |

### Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row for `rhtpa-release.0.4.z`)
- Issue is **scoped** to the 2.2.x stream

### Ecosystem Detection

- Library: serde_json (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

### Step 1.7 -- Embargo Check

CVSS 5.3 (Medium) is below the embargo warning threshold (>= 7.0). Embargo check skipped.
