# Data Extraction — TC-8002

## Step 0 — Configuration Validation

Configuration extracted from project CLAUDE.md:

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

## Step 1 — Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8002 |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Due date | 2026-07-30 |
| Assignee | Unassigned |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. This issue is **scoped** to the 2.2.x stream only.

However, per skill rules, all supported versions across all streams must still be checked for version impact analysis (Step 2). The stream scope affects Steps 3-4 (Affects Versions correction is scoped to 2.2.x only).

### Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate, detected as the **Cargo** ecosystem. From the Ecosystem Mappings in both streams:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

## Step 1.7 — Embargo Check

CVSS 5.3 is Medium severity (below the Critical/Important threshold of >= 7.0). No Embargo policy URL is configured in Security Configuration. Embargo check is **skipped**.
