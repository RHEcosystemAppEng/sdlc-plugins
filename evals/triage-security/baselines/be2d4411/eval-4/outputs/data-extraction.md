# Step 1 -- Data Extraction

## Issue Details

| Field | Value |
|-------|-------|
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(none -- unscoped issue, no stream suffix)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** -- it covers all configured version streams.

Configured Version Streams:
- **2.1.x** -- rhtpa-release.0.3.z
- **2.2.x** -- rhtpa-release.0.4.z

Both streams will be analyzed in Step 2 (Version Impact Analysis).

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. The Ecosystem Mappings tables in both streams' security-matrix.md files include **Cargo** as a supported ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

Ecosystem: **Cargo** (source dependency)

## Deployment Context

The Source Repositories table does not include a Deployment Context column. Defaulting to: **upstream**.
