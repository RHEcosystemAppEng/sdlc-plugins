# Data Extraction -- TC-8004

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | `pscomponent:org/rhtpa-server` |
| Product Version (PSIRT-claimed) | _(none -- no stream suffix in summary)_ |
| Stream Scope | **Unscoped** -- no bracket suffix; analyze all configured streams |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable Library | h2 (Rust crate) |
| Affected Version Range | versions before 0.4.8 (< 0.4.8) |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Existing Comments | _(none)_ |

## Ecosystem Detection

| Property | Value |
|----------|-------|
| Ecosystem | Cargo |
| Lock File | `Cargo.lock` |
| Check Command | `git show <tag>:Cargo.lock \| grep -A2 'name = "h2"'` |
| Upstream Branch (2.1.x) | `release/0.3.z` |
| Upstream Branch (2.2.x) | `release/0.4.z` |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Per the skill protocol, this issue is **unscoped** and must be analyzed across all configured version streams (2.1.x and 2.2.x).

## External CVE References

| Source | URL |
|--------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| RustSec Advisory | https://rustsec.org/advisories/RUSTSEC-2026-0055.html |
| Upstream Fix PR | https://github.com/hyperium/h2/pull/812 |

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic.
