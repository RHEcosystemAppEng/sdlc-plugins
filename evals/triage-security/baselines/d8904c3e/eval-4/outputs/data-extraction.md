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

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames"
has **no stream suffix** in brackets. This issue is **unscoped** -- it covers all
configured version streams:

- 2.1.x (Konflux: rhtpa-release.0.3.z)
- 2.2.x (Konflux: rhtpa-release.0.4.z)

All streams must be analyzed in Step 2. Steps 3 and 8 apply to all affected streams
(not scoped to a single stream).

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. Per the Ecosystem Mappings tables in
both streams' security-matrix.md files, this falls under the **Cargo** ecosystem:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Category: **Source dependency** -- produces 2 remediation tasks per affected stream
  (upstream backport + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with no
Deployment Context column. Default deployment context: **upstream**.
