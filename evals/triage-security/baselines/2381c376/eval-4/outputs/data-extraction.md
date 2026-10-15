# Step 1 -- Data Extraction: TC-8004

## Extracted CVE Data

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
| Existing comments | _(no comments)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Per the skill procedure, the issue is treated as **unscoped** -- it covers all configured version streams.

Configured Version Streams:
- **2.1.x** -- Konflux release repo: rhtpa-release.0.3.z
- **2.2.x** -- Konflux release repo: rhtpa-release.0.4.z

Both streams will be analyzed in the version impact analysis (Step 2).

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Remediation task count per stream**: 2 (dependency bump + downstream propagation, when upstream fix is available)

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic.
