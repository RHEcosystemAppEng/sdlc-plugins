# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: not configured (Step 4.3 will be skipped)
- **PS Component custom field**: not configured
- **Stream custom field**: not configured
- **ProdSec contact email**: not configured (skip silently)
- **ProdSec Jira account ID**: not configured (skip @mentions silently)
- **Embargo policy URL**: not configured (Step 1.7 will be skipped)
- **Version Streams**: 2.1.x and 2.2.x
- **Source Repositories**: rhtpa-backend (no Deployment Context column -- defaulting all repos to `upstream`)

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md contains `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`.
Today's date is 2026-07-01. The matrix was last updated 3 days ago, which is within
the 14-day default threshold. Proceeding without staleness warning.

## Step 0.5 -- JIRA Access Initialization

(Skipped per eval rules -- no external API calls.)

---

# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8002

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Summary | CVE-2026-28940 serde_json - Stack overflow on deeply nested input [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 (< 1.0.135) |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | (not provided in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to stream **2.2.x** from the
Version Streams table. Triage is scoped to the 2.2.x stream. However, per Important
Rule 4, all supported versions across all streams will still be checked in the version
impact analysis.

### Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. Based on the Ecosystem Mappings
table in security-matrix.md, this maps to the **Cargo** ecosystem. Cargo is listed
in both streams' Ecosystem Mappings tables, so it is a supported ecosystem.

- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.3.z` (2.1.x), `release/0.4.z` (2.2.x)

### Deployment Context Lookup

The Source Repositories table does not have a Deployment Context column. Defaulting
rhtpa-backend to `upstream`.

## Step 1.5 -- External CVE Data Enrichment

(Skipped per eval rules -- no external API calls. Using Jira description data: affected
range < 1.0.135, fixed version 1.0.135.)

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Skipping Step 1.7
silently and proceeding to Step 2.
