# Data Extraction -- TC-8004

## Parsed CVE Data

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

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has **no stream suffix** in brackets. Per the skill's stream scope resolution logic, this issue is treated as **unscoped** -- it covers all configured version streams (2.1.x and 2.2.x). Steps 3 and 4 apply to all streams.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Both stream matrices list a **Cargo** ecosystem mapping with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`

Ecosystem: **Cargo** (source dependency)

## Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` source repository. The Source Repositories table in the project CLAUDE.md does not include a Deployment Context column. Per the skill definition, the deployment context defaults to **upstream** when the column is absent.

Deployment context: **upstream** (default -- no Deployment Context column configured)
