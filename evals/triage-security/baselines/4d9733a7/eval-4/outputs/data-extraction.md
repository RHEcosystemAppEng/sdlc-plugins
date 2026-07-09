# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has **no stream suffix** in brackets. This issue is treated as **unscoped** -- it covers all streams. Steps 3 and 8 will apply to all streams, and ALL versions across all streams are checked (Step 1 stream scope resolution, unscoped path).

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Based on the Ecosystem Mappings table in security-matrix.md, the ecosystem is **Cargo**. The lock file is `Cargo.lock` and the check command is `git show <tag>:Cargo.lock`.
