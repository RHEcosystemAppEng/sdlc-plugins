# Data Extraction — TC-8004

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix — unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. This issue is **unscoped** — it covers all configured version streams (2.1.x and 2.2.x). Steps 2-8 will analyze all streams, and Affects Versions correction will include all affected versions across all streams.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Ecosystem: **Cargo**.

Both streams' Ecosystem Mappings tables configure:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Repository: backend

## Deployment Context

The Source Repositories table in the project CLAUDE.md does not include a Deployment Context column. Default: `upstream`. However, since the column is absent (backward compatibility), coordination guidance will be omitted from remediation task descriptions.
