# Data Extraction — TC-8004

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | _(none — unscoped, no stream suffix in summary)_ |
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

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** — it covers all configured version streams (2.1.x and 2.2.x). Steps 3 and 8 will apply to all streams; Case A (cross-stream impact) is not applicable for unscoped issues.

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- **Remediation tasks per affected stream**: 2 (upstream backport or dependency bump + downstream propagation)

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) — this CVE specifically affects the Rust h2 library's header accumulation logic.

## References

- https://github.com/advisories/GHSA-2026-kv8p-r3n7
- https://rustsec.org/advisories/RUSTSEC-2026-0055.html
