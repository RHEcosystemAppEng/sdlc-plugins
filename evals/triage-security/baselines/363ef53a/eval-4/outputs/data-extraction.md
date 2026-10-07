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
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |

## Stream Scope Resolution

The issue summary is "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" with **no stream suffix** in brackets. This issue is therefore **unscoped** and covers all configured version streams (2.1.x and 2.2.x).

Steps 3 and 4 apply to all streams: Affects Versions correction will include all affected versions across all streams, and Case A (cross-stream impact) is skipped entirely since the issue is unscoped.

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate. Both streams' Ecosystem Mappings tables list **Cargo** as the ecosystem for the `backend` repository with lock file `Cargo.lock`.

Ecosystem classification: **Source dependency (Cargo)** — remediation produces 2 tasks per affected stream (upstream backport + downstream propagation), or dependency bump + downstream propagation if the upstream branch already ships the fix.

## Deployment Context Lookup

The affected repository `rhtpa-backend` is listed in the Source Repositories table but no Deployment Context column is present. Per backward compatibility rules, deployment context defaults to `upstream` but coordination guidance is omitted from remediation task descriptions.
