# Data Extraction -- TC-8004

## Parsed CVE Data

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
| Affects Versions (PSIRT-claimed) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Due Date | 2026-08-01 |
| Assignee | Unassigned |
| Existing Comments | None |

## Stream Scope Resolution

The issue summary has **no** stream suffix in brackets. This issue is treated as **unscoped** -- it covers all configured version streams. Steps 3 and 8 apply to all streams (2.1.x and 2.2.x).

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE Record | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Upstream Fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per affected stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`

## Deployment Context

The affected repository (rhtpa-backend) has deployment context: `upstream` (default -- no Deployment Context column in Source Repositories table).

## Notes

- This CVE is distinct from CVE-2024-2758 (httpd CONTINUATION flood) -- this CVE specifically affects the Rust h2 library's header accumulation logic.
- The fix adds a configurable maximum header list size that defaults to 16 KiB.
