# Step 1 -- Data Extraction

## Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to stream 2.2.x. Steps 3 and 4 will operate within this stream scope. Cross-stream impact on other streams (2.1.x) will be handled via Case A (cross-stream impact analysis).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is a **source dependency** ecosystem per the Ecosystem Mappings tables in both streams' security-matrix.md.

Per the ecosystem classification table:
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock`
Upstream branch (2.2.x stream): `release/0.4.z`
Upstream branch (2.1.x stream): `release/0.3.z`

## Deployment Context

The affected repository `rhtpa-backend` has deployment context **upstream** (default, as the Deployment Context column is absent from the Source Repositories table in the project CLAUDE.md).
