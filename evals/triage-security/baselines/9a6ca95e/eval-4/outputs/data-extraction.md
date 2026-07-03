# Step 1 -- Data Extraction

## Issue: TC-8004

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | `pscomponent:org/rhtpa-server` |
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

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is therefore **unscoped** -- it covers all configured version streams (2.1.x and 2.2.x). Steps 2-8 will analyze all streams and scope remediation to actually affected streams only.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. The ecosystem is **Cargo**. Both version streams have Cargo configured in their Ecosystem Mappings tables:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with deployment context defaulting to `upstream` (no Deployment Context column present).
