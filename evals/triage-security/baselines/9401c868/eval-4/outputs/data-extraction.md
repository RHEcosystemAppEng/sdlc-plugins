# Step 1 -- Data Extraction: TC-8004

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Due date | 2026-08-01 |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is **unscoped** -- it covers all configured version streams (2.1.x and 2.2.x). Steps 3 and 8 will apply to all streams, and Case A (cross-stream impact) is skipped entirely since the issue is not scoped to a single stream.

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'`
- **Remediation tasks per stream**: 2 (dependency bump + downstream propagation, since the fix is already available in h2 0.4.8)

## Deployment Context

Repository `rhtpa-backend` has deployment context: `upstream` (default -- no explicit Deployment Context column in Source Repositories table).
