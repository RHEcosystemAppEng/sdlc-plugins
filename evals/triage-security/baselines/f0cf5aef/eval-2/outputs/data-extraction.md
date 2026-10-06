# Data Extraction — TC-8002

## Step 0 — Configuration Validated

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
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

Matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z (100 days ago as of 2026-10-06).

The matrix is older than the 14-day staleness threshold. In a live triage, the user would be prompted to refresh, proceed, or stop. For this eval, proceeding with the current matrix data.

## Step 1 — Extracted CVE Data

| Field | Value |
|---|---|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| Upstream fix PR | Not available in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| CVSS | 5.3 (Medium) |
| Due date | 2026-07-30 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams configuration. This issue is **scoped** to stream 2.2.x.

However, since this is a version impact analysis across all supported versions, both the 2.1.x and 2.2.x streams are analyzed to determine cross-stream impact.

### Ecosystem Detection

- **Library**: serde_json (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation) -- if remediation were needed

### Deployment Context

Repository `rhtpa-backend` has no explicit Deployment Context column configured. Default: **upstream**.

## Step 1.7 — Embargo Check

Embargo policy URL is not configured in Security Configuration. Step skipped.

Additionally, CVE severity is Medium (CVSS 5.3), which is below the Critical/Important threshold (CVSS >= 7.0). Even if an embargo policy were configured, this step would be skipped due to low severity.
