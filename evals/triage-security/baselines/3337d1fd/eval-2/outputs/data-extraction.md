# Data Extraction -- TC-8002

## Step 0 -- Configuration Validation

Configuration validated from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (https://github.com/rhtpa/rhtpa-backend)

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z (24 days ago).
The matrix is older than the 14-day threshold. In a live triage, the user would be warned and given the option to refresh, proceed, or stop.

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
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| CVSS | 5.3 (Medium) |
| Due date | 2026-07-30 |
| Existing comments | None |
| Issue status | New |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **serde_json**, a Rust crate. The ecosystem is **Cargo**, which is listed in the Ecosystem Mappings tables for both streams.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.2.x stream): `release/0.4.z`

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table. No Deployment Context column is present in the table (backward compatibility), so the default deployment context is **upstream**.

## Step 1.7 -- Embargo Check

CVE-2026-28940 has a CVSS of 5.3 (Medium severity). The embargo check threshold is CVSS >= 7.0 (Critical/Important). Since 5.3 < 7.0, the embargo check is **skipped**.
