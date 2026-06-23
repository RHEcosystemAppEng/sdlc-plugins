# Data Extraction - TC-8004

## Step 0 - Configuration Validated

| Config Item | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |

## Step 1 - Parsed CVE Data

| Field | Value |
|---|---|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | Unscoped (no stream suffix in summary) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Ecosystem | Cargo |
| Affected version range | versions before 0.4.8 (< 0.4.8) |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has **no stream suffix** in brackets. This issue is treated as **unscoped** -- it covers all configured streams (2.1.x and 2.2.x). Steps 2-7 will analyze all streams and scope remediation to actually affected streams only.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings in both streams' security-matrix.md files, this maps to the **Cargo** ecosystem:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- Source repository: backend
- Upstream branches: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)
