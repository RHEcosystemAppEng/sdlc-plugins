# Data Extraction -- Step 1

## Issue Summary

| Field | Value |
|-------|-------|
| Issue Key | TC-8020 |
| CVE ID | CVE-2026-55123 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream `2.2.x` (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to rhtpa-2.2.

## Ecosystem Detection

The vulnerable library `tokio` is a Rust crate. Based on the Ecosystem Mappings in the security matrix for both streams, the ecosystem is **Cargo**.

| Property | Value |
|----------|-------|
| Ecosystem | Cargo |
| Repository | backend |
| Lock File | `Cargo.lock` |
| Check Command | `git show <tag>:Cargo.lock` |
| Classification | Source dependency |
| Tasks per stream | 2 (upstream backport/dependency bump + downstream propagation) |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0088.html

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table. No Deployment Context column is present in the configuration, so the default deployment context is `upstream`.

## Security Configuration Extracted (Step 0)

| Config Field | Value |
|--------------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | customfield_10632 |
| PS Component custom field | customfield_10669 |
| Stream custom field | customfield_10832 |
