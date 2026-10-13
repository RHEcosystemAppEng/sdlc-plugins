# Data Extraction — TC-8002

## Step 0 — Configuration Validation

Configuration validated from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: `pscomponent:`
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured (Step 4.3 and Step 7 skipped)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured
- **Embargo policy URL**: not configured (Step 1.7 skipped)

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default — no Deployment Context column) |

## Step 0.3 — Matrix Staleness Check

Security matrix last updated: 2026-06-28T10:00:00Z (107 days ago as of 2026-10-13).
Matrix is stale (exceeds 14-day threshold). In interactive mode, the user would be prompted to refresh or proceed. For this eval, proceeding with current matrix data.

## Step 1 — Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Mapped source repository | rhtpa-backend |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | **2.2.x** (scoped issue) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 (< 1.0.135) |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | not provided |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | none |

### Ecosystem Detection

- **Library**: serde_json (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock`

### Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default, no Deployment Context column in Source Repositories table)

## Step 1.5 — External CVE Data Enrichment

External CVE databases would be queried for cross-validation (not executed in eval mode):

- **MITRE CVE API**: https://cveawg.mitre.org/api/cve/CVE-2026-28940
- **OSV.dev API**: https://api.osv.dev/v1/vulns/CVE-2026-28940

Using Jira description data for fix threshold: **serde_json < 1.0.135**, fixed in **1.0.135**.

## Step 1.7 — Embargo Check

Embargo policy URL is not configured in Security Configuration. Skipping embargo check.

(Note: Even if configured, CVE-2026-28940 has CVSS 5.3 / Medium severity, which is below the Critical/Important threshold of CVSS >= 7.0. The embargo gate would not trigger.)
