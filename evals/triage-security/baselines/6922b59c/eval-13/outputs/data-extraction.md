# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Issue Key | TC-8001 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x. Steps 3 and 8 will apply only to versions within this stream; cross-stream impact on 2.1.x is handled via Case A (proactive remediation).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings tables in both stream matrices list **Cargo** as a configured ecosystem with:

- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x)

Ecosystem classification: **Source dependency (Cargo)** -- produces 2 remediation tasks per stream (dependency bump or upstream backport + downstream propagation).

## Deployment Context

The source repository `rhtpa-backend` is listed in Source Repositories but has no explicit Deployment Context column. Default deployment context: **upstream**.
