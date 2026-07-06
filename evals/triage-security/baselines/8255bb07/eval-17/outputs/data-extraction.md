# Step 1 -- Data Extraction

## Issue: TC-8001

Parsed CVE data from Vulnerability issue TC-8001:

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x. Steps 3-4 will apply only to the 2.2.x stream, but cross-stream impact on 2.1.x will be reported in Case B.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is listed in the Ecosystem Mappings tables for both streams. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`.

## Deployment Context

The affected repository `rhtpa-backend` has deployment context **upstream** (default, since no Deployment Context column is present in the Source Repositories table).

## Affects Versions Discrepancy

The current Affects Versions field contains `RHTPA 2.0.0`, which does not correspond to any configured version stream (2.1.x or 2.2.x). This value was assigned by PSIRT based on scan time and requires correction in Step 3 after version impact analysis.
