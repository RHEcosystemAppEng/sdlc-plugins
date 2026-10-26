# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured |

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

The security matrix has a Last-Updated timestamp of `2026-06-28T10:00:00Z`.
Compared to the current date (2026-10-26), this is approximately 120 days old,
which exceeds the 14-day staleness threshold. In an interactive session, the
engineer would be warned and asked to refresh or proceed.

For this eval, we proceed with the available data.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
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
| Upstream fix PR | Not provided in remote links |
| Due date | 2026-07-30 |
| Existing comments | None |
| Status | New |
| Assignee | Unassigned |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** version stream (Konflux release repo: rhtpa-release.0.4.z). This
issue is scoped to stream 2.2.x only.

However, because all streams must be checked for version impact analysis
(Step 2), both 2.1.x and 2.2.x streams are analyzed.

### Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. The ecosystem mappings
for both streams list **Cargo** as the ecosystem, with `Cargo.lock` as the
lock file and `git show <tag>:Cargo.lock` as the check command. This is a
**source dependency ecosystem**, which normally produces 2 remediation tasks
per stream (upstream backport/bump + downstream propagation).

### Deployment Context

The source repository `rhtpa-backend` has deployment context defaulting to
`upstream` (Deployment Context column is absent from the Source Repositories table).

## Step 1.5 -- External CVE Data Enrichment

In this eval, external CVE databases (MITRE, OSV) are not queried. The fix
threshold from the Jira description is used:

- **Affected range**: versions before 1.0.135
- **Fixed version**: 1.0.135

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. This step is
skipped entirely. Additionally, the CVE severity is Medium (CVSS 5.3), which
is below the Critical/Important threshold (CVSS >= 7.0), so the embargo gate
would not trigger even if configured.
