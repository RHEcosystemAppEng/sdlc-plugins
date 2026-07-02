# Step 1 -- Data Extraction: TC-8004

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames"
contains **no stream suffix** in brackets. Per the skill's stream scope resolution
rules, this issue is treated as **unscoped** -- it covers all configured version
streams. Steps 2-8 will analyze all streams (2.1.x and 2.2.x) and apply corrections
across all of them.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings
tables in both streams' security-matrix.md files, the ecosystem is **Cargo**.

| Property | Value |
|----------|-------|
| Ecosystem | Cargo |
| Repository | backend |
| Lock File | Cargo.lock |
| Check Command | `git show <tag>:Cargo.lock` |
| Upstream Branch (2.1.x) | release/0.3.z |
| Upstream Branch (2.2.x) | release/0.4.z |

## Deployment Context

The affected repository (rhtpa-backend) is listed in Source Repositories without a
Deployment Context column. Per the skill's backward compatibility rule, deployment
context defaults to **upstream**.
