# Step 1 -- Data Extraction

## Issue: TC-8004

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
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary ("CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames") contains **no stream suffix** in brackets. Therefore this issue is **unscoped** -- it covers all configured version streams.

Per the skill instructions for unscoped issues:
- Steps 2-8 analyze **all** streams (2.1.x and 2.2.x)
- Case A (cross-stream impact notice) is skipped entirely -- unscoped issues cover all streams by definition
- Affects Versions correction (Step 3) includes all affected versions across all streams
- Remediation tasks (Case B) are created only for actually affected streams

## Ecosystem Detection

- **Library**: h2 (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Remediation tasks per affected stream**: 2 (upstream backport + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` has no Deployment Context column in the Source Repositories table. Per backward compatibility rules, deployment context defaults to `upstream`. Coordination guidance subsection is omitted from remediation tasks since the column is absent.
