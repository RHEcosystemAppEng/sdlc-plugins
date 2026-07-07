# Step 1 -- Data Extraction: TC-8004

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Vulnerable Library | h2 |
| Ecosystem | Cargo |
| Affected Version Range | versions before 0.4.8 |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| Affects Versions (PSIRT-assigned) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Stream Scope Resolution

The issue summary has **no** stream suffix in brackets -- this is an **unscoped** issue. It covers all configured version streams. Steps 2-8 analyze all streams (2.1.x and 2.2.x) and create remediation only for actually affected streams.

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Description Analysis

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB. This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood).
