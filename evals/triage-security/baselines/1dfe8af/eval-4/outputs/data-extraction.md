# Step 1 -- Data Extraction

## Issue Details

| Field | Value |
|-------|-------|
| Issue Key | TC-8004 |
| Summary | CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames |
| Issue Type | Vulnerability |
| Status | New |
| Assignee | Unassigned |
| Due Date | 2026-08-01 |

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected Component | pscomponent:org/rhtpa-server |
| Vulnerable Library | h2 |
| Ecosystem | Cargo |
| Affected Version Range | versions before 0.4.8 |
| Fixed Version | 0.4.8 |
| CVSS | 7.5 (High) |
| Stream Scope | Unscoped (no stream suffix in summary -- analyze all streams) |

## PSIRT-Assigned Affects Versions

- RHTPA 2.1.0
- RHTPA 2.2.0

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Upstream Fix PR | https://github.com/hyperium/h2/pull/812 |

## Labels

- CVE-2026-33501
- pscomponent:org/rhtpa-server

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0055.html

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** and covers all configured version streams (2.1.x and 2.2.x). The version impact analysis must check all versions across all streams.

## Ecosystem Detection

The vulnerable library is `h2`, a Rust crate. The Ecosystem Mappings tables in both streams' security-matrix.md files list Cargo as an ecosystem with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)
