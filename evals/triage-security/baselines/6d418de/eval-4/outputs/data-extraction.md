# Step 1 -- Data Extraction

## Issue: TC-8004

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | `pscomponent:org/rhtpa-server` |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 (< 0.4.8) |
| Fixed version | 0.4.8 |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| CVSS | 7.5 (High) |
| Due date | 2026-08-01 |
| Existing comments | _(no comments)_ |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Therefore, this issue is **unscoped** -- it covers all configured version streams (2.1.x and 2.2.x). Steps 3 and 4 will apply to all streams.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings tables in both streams' security-matrix.md, the ecosystem is **Cargo**:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x) |

As a source dependency (Cargo), remediation will require **two tasks** per affected stream: an upstream backport task and a downstream propagation subtask with a Blocks dependency.

## Additional References

- RustSec advisory: https://rustsec.org/advisories/RUSTSEC-2026-0055.html
- The vulnerability allows memory exhaustion via excessive CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit. The fix (0.4.8) adds a configurable maximum header list size defaulting to 16 KiB.
- This is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library.
