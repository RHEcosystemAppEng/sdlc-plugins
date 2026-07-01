# Step 0 -- Validate Project Configuration

## Configuration Extracted

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured
- **Embargo policy URL**: not configured (Step 1.7 will be skipped)
- **Upstream Affected Component custom field**: not configured (Step 4.3 will be skipped)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

**Deployment Context column**: absent from the Source Repositories table. Per backward compatibility rules, all repositories default to `upstream`. The Coordination Guidance subsection will be omitted from remediation task descriptions.

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md file has `Last-Updated: 2026-06-28T10:00:00Z`. Today is 2026-07-01. That is 3 days ago, which is within the 14-day default threshold. No staleness warning is needed. Proceeding silently.

## Step 0.5 -- JIRA Access Initialization

(Skipped for eval -- no external tools called.)

## Step 1 -- Data Extraction

### Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Affected component** | pscomponent:org/rhtpa-server |
| **Product version (PSIRT-claimed)** | [rhtpa-2.2] |
| **Affects Versions (Jira field)** | RHTPA 2.0.0 |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | < 0.11.14 |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Upstream fix PR** | https://github.com/quinn-rs/quinn/pull/2048 |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| **CVE record URL** | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| **Due date** | 2026-07-15 |
| **Existing comments** | (none) |
| **Issue status** | New |
| **Reporter** | (not specified in fixture) |
| **Assignee** | Unassigned |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapping:
- `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table.
- **Issue stream scope**: 2.2.x
- Steps 3 and 4 will be scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`
- **Repository**: backend

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend** in the Source Repositories table. The Source Repositories table does **not** have a Deployment Context column. Per the skill protocol (backward compatibility), the deployment context defaults to `upstream`. However, because the Deployment Context column is entirely absent from the table, the Coordination Guidance subsection will be **omitted** from remediation task descriptions rather than using the `upstream` template.

## Step 1.5 -- External CVE Data Enrichment

(Skipped for eval -- no external tools called. Using Jira description data: affected range < 0.11.14, fixed version 0.11.14.)

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Skipping this step silently.
