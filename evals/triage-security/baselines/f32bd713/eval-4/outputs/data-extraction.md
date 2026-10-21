# Data Extraction — TC-8004

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(none — unscoped issue, no stream suffix in summary)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |
| Deployment context | upstream (default — no Deployment Context column in Source Repositories) |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** and covers all configured version streams:

- **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

All streams must be analyzed in Step 2 (Version Impact Analysis). Steps 3 and 4 apply to all streams.

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. The Ecosystem Mappings tables for both streams list **Cargo** as a configured ecosystem with:

- **Repository**: backend
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`

Ecosystem classification: **Source dependency** (Cargo) -- remediation produces 2 tasks per affected stream: upstream backport (or dependency bump) + downstream propagation.

## Configuration Extracted (Step 0)

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Embargo policy URL | _(not configured -- Step 1.7 skipped)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Upstream Affected Component field | _(not configured -- Step 4.3 and Step 7 skipped)_ |

## Matrix Staleness Check (Step 0.3)

Matrix Last-Updated timestamp: 2026-06-28T10:00:00Z
Days since update: ~115 days (as of 2026-10-21)
Status: **STALE** (exceeds 14-day threshold)

In an interactive triage, the engineer would be prompted to refresh or proceed. For this analysis, proceeding with the current matrix data.
