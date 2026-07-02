# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

Configuration validated from project CLAUDE.md:

| Setting | Value |
|---------|-------|
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

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: 2026-06-28T10:00:00Z
Current date: 2026-07-02
Age: 4 days -- within the 14-day threshold. No staleness warning.

## Step 0.7 -- Assign and Transition

PROPOSAL: Assign TC-8002 to the current user and transition from New to Assigned status.

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
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

### Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x**.
This issue is **scoped** to the 2.2.x version stream only.

### Ecosystem Detection

Vulnerable library: serde_json (Rust crate)
Ecosystem: **Cargo**
Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
Upstream branch (2.1.x): `release/0.3.z`
Upstream branch (2.2.x): `release/0.4.z`

### Deployment Context

Repository rhtpa-backend: Deployment Context column absent from Source Repositories table, defaulting to **upstream**.

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- external API calls not executed in eval mode)

Based on the Jira description data:
- Affected range: serde_json < 1.0.135
- Fixed version: 1.0.135

These values are used as the fix threshold for version impact analysis.

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Step 1.7 skipped.

Additionally, CVSS is 5.3 (Medium), which is below the Critical/Important threshold (CVSS >= 7.0). Even if configured, this step would be skipped.
