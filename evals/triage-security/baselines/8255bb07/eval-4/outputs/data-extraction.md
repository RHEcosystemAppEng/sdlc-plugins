# Data Extraction -- TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Vulnerable Library | h2 |
| Ecosystem | Cargo (Rust crate) |
| Affected Version Range | versions before 0.4.8 |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Affects Versions (PSIRT-claimed) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Stream Scope | Unscoped (no stream suffix in summary) -- analyze all streams |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Upstream Fix PR | https://github.com/hyperium/h2/pull/812 |

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable to memory exhaustion caused by a peer sending an excessive number of CONTINUATION frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame data without enforcing a size limit on the accumulated header block, allowing an attacker to consume unbounded memory on the server. The fix adds a configurable maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Both streams (2.1.x and 2.2.x) have Cargo ecosystem mappings configured:

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |
| 2.2.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## Deployment Context

The affected repository (rhtpa-backend) has no explicit Deployment Context column in the Source Repositories table. Defaulting to `upstream`.

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains no stream suffix in brackets. This issue is **unscoped** -- it covers all configured version streams. Both the 2.1.x and 2.2.x streams must be analyzed for impact.
