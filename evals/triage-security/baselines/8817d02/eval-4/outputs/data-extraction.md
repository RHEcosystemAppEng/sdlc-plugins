# Step 1 -- Data Extraction: TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **Issue Key** | TC-8004 |
| **CVE ID** | CVE-2026-33501 |
| **Summary** | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| **Issue Type** | Vulnerability |
| **Status** | New |
| **Affected Component** | `pscomponent:org/rhtpa-server` |
| **Product Version (PSIRT-claimed)** | _(none -- no stream suffix in summary)_ |
| **Affects Versions (Jira field)** | RHTPA 2.1.0, RHTPA 2.2.0 |
| **Vulnerable Library** | h2 (Rust crate) |
| **Affected Version Range** | versions before 0.4.8 |
| **Fixed Version** | 0.4.8 |
| **CVSS** | 7.5 (High) |
| **Upstream Fix PR** | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| **Advisory URL** | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| **CVE Record URL** | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| **Due Date** | 2026-08-01 |
| **Assignee** | Unassigned |
| **Existing Comments** | None |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Per the skill definition, this means the issue is **unscoped** -- it covers all configured version streams.

Configured streams from Security Configuration:
- **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)

Both streams will be analyzed in Step 2.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. This maps to the **Cargo** ecosystem. Both streams' Ecosystem Mappings tables confirm Cargo is configured with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branches: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

## Additional Context

The description notes this CVE is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic. The fix adds a configurable maximum header list size that defaults to 16 KiB.

References:
- https://github.com/advisories/GHSA-2026-kv8p-r3n7
- https://rustsec.org/advisories/RUSTSEC-2026-0055.html
