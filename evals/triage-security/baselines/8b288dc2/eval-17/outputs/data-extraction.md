# Step 1 -- Data Extraction

**Issue**: TC-8001
**Summary**: CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |
| Deployment context | upstream (default -- repository rhtpa-backend found in Source Repositories but no Deployment Context column present) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in Security Configuration. This issue is **stream-scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate, placing it in the **Cargo** ecosystem. The lock file to inspect is `Cargo.lock`, and the check command is `git show <tag>:Cargo.lock`. This is a source dependency ecosystem, so remediation will require two tasks: an upstream backport task and a downstream propagation subtask.
