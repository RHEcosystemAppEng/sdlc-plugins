# Data Extraction -- CVE-2026-28940 (Step 1)

## Project Configuration (Step 0)

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

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Matrix Staleness Check (Step 0.3)

Last-Updated timestamp: 2026-06-28T10:00:00Z (8 days ago as of 2026-07-06).
Within the 14-day freshness threshold -- no staleness warning required. Proceeding with current matrix.

## Parsed CVE Data (Step 1)

| Field | Value |
|-------|-------|
| Jira Issue Key | TC-8002 |
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the configured Version Streams table. This issue is **stream-scoped** to 2.2.x.

However, per the skill's rules (Step 2 and Important Rule #4: "Check ALL supported versions"), version impact analysis is performed across all streams (2.1.x and 2.2.x) to detect cross-stream impact for Case B evaluation.

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. The Ecosystem Mappings tables in both streams configure the **Cargo** ecosystem with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

## Embargo Check (Step 1.7)

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped.

Additionally, CVSS is 5.3 (Medium), which is below the Critical/Important threshold (CVSS >= 7.0), so the embargo gate would not trigger even if configured.
