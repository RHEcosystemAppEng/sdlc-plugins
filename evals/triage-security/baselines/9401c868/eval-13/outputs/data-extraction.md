# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

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

Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

Library **quinn-proto** is a Rust crate. Ecosystem: **Cargo** (source dependency ecosystem). Per the ecosystem classification table, this produces **2 tasks per affected stream**: dependency bump (or upstream backport) + downstream propagation.

## Deployment Context

Repository `rhtpa-backend` has deployment context: **upstream** (default, since no Deployment Context column is present in the Source Repositories table).
