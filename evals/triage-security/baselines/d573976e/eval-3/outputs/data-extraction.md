# Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: Not configured
- **PS Component custom field**: Not configured
- **Stream custom field**: Not configured
- **ProdSec contact email**: Not configured
- **ProdSec Jira account ID**: Not configured
- **Embargo policy URL**: Not configured (Step 1.7 will be skipped)
- **Version Streams**:
  - 2.1.x: git.example.com/rhtpa/rhtpa-release.0.3.z (local: /home/dev/repos/rhtpa-release.0.3.z)
  - 2.2.x: git.example.com/rhtpa/rhtpa-release.0.4.z (local: /home/dev/repos/rhtpa-release.0.4.z)
- **Source Repositories**:
  - rhtpa-backend: https://github.com/rhtpa/rhtpa-backend (local: /home/dev/repos/rhtpa-backend)
  - Deployment Context column: absent -- defaulting all repos to `upstream`

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-07-01
Age: 3 days (within the 14-day default threshold)

Result: Matrix is fresh. Proceeding without staleness warning.

## Step 1 -- Data Extraction

### Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | Not provided in remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| CVSS | 7.5 (High) |

### Stream Scope Resolution

Summary suffix: `[rhtpa-2.2]` -- maps to stream **2.2.x** in the Version Streams table.
Issue stream scope: **2.2.x** (scoped to a single stream).

### Ecosystem Detection

Library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table includes **Cargo** as a configured ecosystem with lock file `Cargo.lock`.

Detected ecosystem: **Cargo**

### Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-server`, which maps to `rhtpa-backend` in the Source Repositories table. The Deployment Context column is absent from the Source Repositories table, so the deployment context defaults to `upstream`.

## Step 1.5 -- External CVE Data Enrichment

(Not executed in this eval -- external tool calls are prohibited. In a real triage, the MITRE CVE API and OSV.dev would be queried to cross-validate the fix threshold of 0.11.14.)

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Skipping this step silently.
