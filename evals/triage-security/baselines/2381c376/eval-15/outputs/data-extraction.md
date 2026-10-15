# Step 1 — Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Stream scope | **2.2.x** (scoped — matches Version Streams table entry `2.2.x`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Ecosystem | Cargo (Rust crate) |
| Deployment context | upstream (default — no Deployment Context column in Source Repositories) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** — Steps 3 and 8 apply only to the 2.2.x stream, while Step 2 analyzes all streams for cross-stream impact detection.

## Ecosystem Detection

quinn-proto is a Rust crate. The Ecosystem Mappings table for both streams lists **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. This is a **source dependency** ecosystem, which produces two remediation tasks per stream (upstream fix + downstream propagation) when remediation is needed.
