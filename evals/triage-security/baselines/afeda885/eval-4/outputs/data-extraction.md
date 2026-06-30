# Data Extraction — TC-8004

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | _(none — no stream suffix in summary; issue is unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable Library | h2 |
| Ecosystem | Cargo |
| Affected Version Range | versions before 0.4.8 (< 0.4.8) |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0055.html

## Stream Scope Resolution

The issue summary has **no** stream suffix in brackets. This is an **unscoped** issue
covering all configured version streams. Steps 2-7 will analyze all streams:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. Both streams configure the **Cargo**
ecosystem in their Ecosystem Mappings tables:

| Stream | Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|--------|-----------|------------|-----------|---------------|-----------------|
| 2.1.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.3.z |
| 2.2.x | Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

## Vulnerability Description

A vulnerability was found in the h2 crate. Versions of h2 before 0.4.8 are vulnerable
to memory exhaustion caused by a peer sending an excessive number of CONTINUATION
frames following a HEADERS frame. The h2 library accumulates all CONTINUATION frame
data without enforcing a size limit on the accumulated header block, allowing an
attacker to consume unbounded memory on the server. The fix adds a configurable
maximum header list size that defaults to 16 KiB.

This issue is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE
specifically affects the Rust h2 library's header accumulation logic.
