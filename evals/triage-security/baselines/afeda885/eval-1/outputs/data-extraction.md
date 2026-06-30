# Step 1 - Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | 2.2.x (mapped from `[rhtpa-2.2]` to Version Streams table) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Ecosystem Detection

| Attribute | Value |
|-----------|-------|
| Ecosystem | Cargo |
| Lock file | Cargo.lock |
| Check command | `git show <tag>:Cargo.lock \| grep -A2 'name = "quinn-proto"'` |
| Source repository | backend |
| Upstream branch (2.1.x) | release/0.3.z |
| Upstream branch (2.2.x) | release/0.4.z |

## Stream Scope Resolution

The issue summary contains suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is scoped to the 2.2.x stream only. Steps 3 and 4 will apply only to versions within this stream.

The 2.1.x stream will be analyzed for cross-stream impact (Step 7 Case B) but is not in scope for Affects Versions correction on this issue.
