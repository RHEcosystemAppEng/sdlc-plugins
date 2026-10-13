# Step 1 - Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Deployment context | upstream (default -- no Deployment Context column in Source Repositories) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. This issue is scoped to stream 2.2.x only. Steps 3 and 4 will be scoped accordingly.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate (Cargo ecosystem). The Ecosystem Mappings table for both streams confirms Cargo is a configured ecosystem with:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

As a source dependency ecosystem, remediation requires **2 tasks per affected stream**: upstream backport (or dependency bump) + downstream propagation.
