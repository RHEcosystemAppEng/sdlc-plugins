# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

All required Security Configuration sections are present in the project CLAUDE.md.

| Configuration Field                | Value                                                        |
|------------------------------------|--------------------------------------------------------------|
| Project key                        | TC                                                           |
| Cloud ID                           | 2b9e35e3-6bd3-4cec-b838-f4249ee02432                        |
| Jira version prefix                | RHTPA                                                        |
| Vulnerability issue type ID        | 10024                                                        |
| Product pages URL                  | https://access.example.com/product-life-cycle/rhtpa          |
| Component label pattern            | pscomponent:                                                 |
| VEX Justification custom field     | customfield_12345                                            |
| Version Streams                    | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)   |
| Source Repositories                | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend)       |

Optional fields not configured: Upstream Affected Component, PS Component, Stream custom field, ProdSec contact, ProdSec Jira account ID, Embargo policy URL.

## Step 0.3 -- Matrix Staleness Check

The security matrix `Last-Updated` timestamp is `2026-06-28T10:00:00Z`. As of the triage date (2026-10-15), this is 109 days old, which exceeds the 14-day staleness threshold. In a live triage, the engineer would be prompted to refresh or proceed. For this analysis, we proceed with the available data.

## Step 1 -- Extracted CVE Data

| Field                       | Value                                                                 |
|-----------------------------|-----------------------------------------------------------------------|
| CVE ID                      | CVE-2026-28940                                                        |
| Affected component          | pscomponent:org/rhtpa-server                                          |
| Product version (PSIRT)     | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`)                        |
| Affects Versions (Jira)     | RHTPA 2.2.0                                                          |
| Vulnerable library          | serde_json                                                            |
| Affected version range      | versions before 1.0.135                                               |
| Fixed version               | 1.0.135                                                               |
| CVSS                        | 5.3 (Medium)                                                          |
| Upstream fix PR             | (none in remote links)                                                |
| Advisory URL                | https://github.com/advisories/GHSA-2026-j9r2-m5vk                    |
| CVE record URL              | https://www.cve.org/CVERecord?id=CVE-2026-28940                      |
| Due date                    | 2026-07-30                                                            |
| Existing comments           | (none)                                                                |
| Issue status                | New                                                                   |
| Assignee                    | Unassigned                                                            |

### Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

However, per the skill procedure, all supported streams (2.1.x and 2.2.x) are analyzed in the version impact table to determine cross-stream impact.

### Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. The Ecosystem Mappings table for both streams lists **Cargo** as a configured ecosystem with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x)

Ecosystem classification: **Source dependency (Cargo)** -- would normally produce 2 tasks per stream (upstream + downstream) if remediation were needed.

### Deployment Context Lookup

The repository `rhtpa-backend` is listed in Source Repositories. No Deployment Context column is present in the mock configuration, so the default context is `upstream`.
