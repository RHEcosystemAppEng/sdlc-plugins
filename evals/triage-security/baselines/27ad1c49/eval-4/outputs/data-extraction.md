# Data Extraction — TC-8004

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(none — no stream suffix in summary)_ |
| Stream scope | **Unscoped** — no stream suffix present; issue covers all streams |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Ecosystem | Cargo (Rust crate) |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Per the skill logic, this issue is treated as **unscoped** -- it covers all configured version streams (2.1.x and 2.2.x). Steps 3 and 4 will apply to all streams. Case A (cross-stream impact) is skipped for unscoped issues.

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport/dependency bump + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- **Affected repository**: rhtpa-backend (matched from pscomponent:org/rhtpa-server)
- **Deployment context**: upstream (Source Repositories table has no Deployment Context column; defaulting to `upstream`)

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
| Upstream Affected Component field | _(not configured -- Steps 4.3 and 7 skipped)_ |
| PS Component field | _(not configured)_ |
| Stream custom field | _(not configured)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured -- @mentions skipped)_ |
| Embargo policy URL | _(not configured -- Step 1.7 skipped)_ |

## Step 1.5: External CVE Data Enrichment

_(Simulated -- not calling external APIs in eval mode)_

Fix threshold from Jira description: h2 < 0.4.8 (fixed in 0.4.8).

Using Jira description data as the authoritative fix threshold for version impact analysis, since external API calls are not performed in this eval.

## Step 1.7: Embargo Check

Skipped -- no Embargo policy URL configured in Security Configuration.
