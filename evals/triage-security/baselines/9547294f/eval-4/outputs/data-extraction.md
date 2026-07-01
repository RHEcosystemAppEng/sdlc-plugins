# Step 1 -- Data Extraction for TC-8004

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(none -- no stream suffix in summary)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate -- h2 is a Rust HTTP/2 implementation) |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Therefore, this issue is treated as **unscoped** -- it covers all configured version streams.

Per the Version Streams table in Security Configuration:
- Stream 2.1.x (rhtpa-release.0.3.z)
- Stream 2.2.x (rhtpa-release.0.4.z)

Both streams will be analyzed in Step 2.

## Ecosystem Detection

The library `h2` is a Rust crate (HTTP/2 protocol implementation). Based on the Ecosystem Mappings tables in both streams' security-matrix.md, the ecosystem is **Cargo**. The lock file to inspect is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.
