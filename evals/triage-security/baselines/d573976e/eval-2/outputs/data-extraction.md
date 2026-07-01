# Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured (Step 4.3 and Step 7 will be skipped)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured (skip silently)
- **ProdSec Jira account ID**: not configured (skip @mentions silently)
- **Embargo policy URL**: not configured (Step 1.7 will be skipped)
- **Deployment Context column**: absent from Source Repositories table (default all repos to `upstream`; omit Coordination Guidance)

**Version Streams:**

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

**Source Repositories:**

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default) |

# Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated: 2026-06-28T10:00:00Z`. Current date: 2026-07-01.
Days since last update: 3 days. Threshold: 14 days.
Result: Matrix is fresh. Proceeding without warning.

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8002 |
| **CVE ID** | CVE-2026-28940 |
| **Summary** | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| **Status** | New |
| **Affected component** | pscomponent:org/rhtpa-server |
| **Product version (PSIRT-claimed)** | [rhtpa-2.2] |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable library** | serde_json |
| **Affected version range** | < 1.0.135 |
| **Fixed version** | 1.0.135 |
| **CVSS** | 5.3 (Medium) |
| **Due date** | 2026-07-30 |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| **CVE record URL** | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| **Upstream fix PR** | (none in remote links) |
| **Existing comments** | (none) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`. Mapping to configured Version Streams:
- `[rhtpa-2.2]` maps to stream **2.2.x**

The issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 8 will be scoped to this stream only. Step 2 will check all versions across all streams per Important Rule 4.

## Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. Checking the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

serde_json is a Rust crate -> ecosystem: **Cargo**. Cargo is listed in the Ecosystem Mappings table. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`.

## Deployment Context Lookup

Affected component label: `pscomponent:org/rhtpa-server`. The Source Repositories table does not have a Deployment Context column. Default deployment context: **upstream**.

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Skipping Step 1.7 silently.
