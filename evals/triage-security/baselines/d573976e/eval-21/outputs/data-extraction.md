# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: customfield_10632 (configured)
- **ProdSec contact email**: not configured
- **ProdSec Jira account ID**: not configured
- **Embargo policy URL**: not configured (Step 1.7 skipped)
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (upstream by default -- no Deployment Context column)

All required configuration sections are present. Proceeding.

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: `2026-06-28T10:00:00Z`
Current date: 2026-07-01
Days since update: 3 days
Threshold: 14 days

The matrix is within the 14-day freshness threshold. Proceeding without warning.

## Step 1 -- Data Extraction

**Issue Key**: TC-8020
**Issue Data Source**: vuln-issue-standard.md fixture (adapted for TC-8020)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server (from labels) |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (i.e., < 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`.
Mapped to configured Version Stream: **2.2.x** (rhtpa-release.0.4.z).
Issue stream scope: **2.2.x only**.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate.
The Ecosystem Mappings table for stream 2.2.x lists **Cargo** as a supported ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Detected ecosystem: **Cargo** (source dependency).

### Deployment Context Lookup

The Source Repositories table has no Deployment Context column.
Per Step 0 configuration extraction, all repositories default to `upstream`.
Deployment context for rhtpa-backend: **upstream** (default).

## Step 1.5 -- External CVE Data Enrichment

(External API calls are not permitted in this eval. Using Jira description data.)

The Jira description provides a clear fix threshold:
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14

In a live triage, MITRE CVE API and OSV.dev would be queried to cross-validate. For this eval, the Jira description data is used as the authoritative fix threshold.

**Enriched fix threshold**: **0.11.14** (from Jira description).

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped silently.
