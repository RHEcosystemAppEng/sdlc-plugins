# Step 1 -- Data Extraction: TC-8004

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | Unscoped (no stream suffix in summary) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. The issue is therefore **unscoped** -- it covers all configured version streams.

Configured version streams:
- **2.1.x** -- Konflux release repo: rhtpa-release.0.3.z
- **2.2.x** -- Konflux release repo: rhtpa-release.0.4.z

All streams will be analyzed in Step 2.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings tables in both streams' security matrices:

- **Ecosystem**: Cargo
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Source repository**: backend (rhtpa-backend)

This is a **source dependency** ecosystem, meaning remediation requires two tasks per affected stream: an upstream backport task and a downstream propagation subtask.

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |

## Additional References

- https://rustsec.org/advisories/RUSTSEC-2026-0055.html
