# Data Extraction -- TC-8004

## Step 1 -- Parsed CVE Data

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
| Existing comments | _(no comments)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" has
**no stream suffix** in brackets. The issue is treated as **unscoped** -- it covers all
configured version streams (2.1.x and 2.2.x). Steps 2-8 will analyze all streams and
create remediation only for actually affected streams.

## Ecosystem Detection

The vulnerable library `h2` is a Rust crate. Based on the Ecosystem Mappings tables in
both streams' security-matrix.md files, the applicable ecosystem is **Cargo**.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`
- Ecosystem category: **Source dependency** -- remediation produces 2 tasks per affected
  stream (upstream backport + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` has deployment context **upstream** (default,
since the Deployment Context column is absent from the Source Repositories table).
