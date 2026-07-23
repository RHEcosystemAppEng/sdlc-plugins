# Step 1 -- Data Extraction: TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| Ecosystem | Cargo |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Reporter | psirt-analyst (account ID: 557058:psirt-analyst-mock-id) |
| Deployment context | upstream (default -- Source Repositories table has no Deployment Context column) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream from the Version Streams table in Security Configuration.

Issue stream scope: **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`)

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem from the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend

Since this is a source dependency ecosystem (Cargo), remediation will require **two tasks**: an upstream backport task and a downstream propagation subtask.

## Security Configuration Extracted (Step 0)

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Jira version prefix: RHTPA
- Vulnerability issue type ID: 10024
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- Component label pattern: pscomponent:
- VEX Justification custom field: customfield_12345
- ProdSec contact email: prodsec-team@example.com
- ProdSec Jira account ID: 557058:prodsec-mock-account-id
