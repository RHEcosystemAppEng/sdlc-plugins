# Data Extraction -- TC-8002

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | versions before 1.0.135 |
| Fixed version | 1.0.135 |
| Upstream fix PR | (none in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | (none) |
| CVSS | 5.3 (Medium) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to configured Version Stream **2.2.x** (Konflux release repo: git.example.com/rhtpa/rhtpa-release.0.4.z).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to this stream only.

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Ecosystem: Cargo (source dependency)
- Lock File: Cargo.lock
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: release/0.4.z

Cargo is a source dependency ecosystem, which would normally produce 2 remediation tasks per stream (upstream backport + downstream propagation) if remediation were needed.

## Deployment Context

Repository `rhtpa-backend` is listed in Source Repositories. No Deployment Context column is present in the fixture, so the default is `upstream`.

## Configuration Extracted (Step 0)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
