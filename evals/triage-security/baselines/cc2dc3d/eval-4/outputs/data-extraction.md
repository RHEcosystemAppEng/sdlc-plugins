# Step 1 -- Data Extraction: TC-8004

## Extracted Fields

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | No stream suffix (unscoped) |
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

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Therefore this issue is **unscoped** -- it covers all configured version streams.

Configured version streams from Security Configuration:
- **2.1.x** -- Konflux release repo: rhtpa-release.0.3.z
- **2.2.x** -- Konflux release repo: rhtpa-release.0.4.z

Both streams must be analyzed in Steps 2-7.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings in both streams' security-matrix.md, the relevant ecosystem is:

- **Ecosystem**: Cargo
- **Lock file**: Cargo.lock
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: backend

## Vulnerability Description

A vulnerability in the h2 crate allows memory exhaustion via excessive CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block. An attacker can send unbounded CONTINUATION frames to consume unlimited memory on the server. The fix (version 0.4.8) adds a configurable maximum header list size defaulting to 16 KiB.

This is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic.
