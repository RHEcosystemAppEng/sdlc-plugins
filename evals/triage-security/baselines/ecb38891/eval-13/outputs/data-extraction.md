# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this falls under the **Cargo** ecosystem.

Cargo is classified as a **source dependency** ecosystem in the ecosystem classification table. This means remediation will produce **2 tasks per affected stream**: an upstream backport task and a downstream propagation subtask (with Blocks dependency).

### Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`. Looking up the Source Repositories table, the Deployment Context column is absent (no column present). Per Step 0 backward compatibility rules, all repositories default to `upstream`.
