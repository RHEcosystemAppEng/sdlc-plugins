# Step 1 -- Data Extraction

## CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
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

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream
(Konflux release repo: `rhtpa-release.0.4.z`).

The issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will be scoped to this stream.
Cross-stream impact on 2.1.x will be handled by Case A in Step 8.

## Ecosystem Detection

The vulnerable library **quinn-proto** is a Rust crate. Based on the Ecosystem Mappings
table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

Cargo is a **source dependency** ecosystem per the classification table. Remediation will
produce **two tasks** per affected stream: upstream backport + downstream propagation.

## Deployment Context Lookup

The component label `pscomponent:org/rhtpa-server` maps to repository **rhtpa-backend**.
The Source Repositories table in CLAUDE.md does not include a Deployment Context column,
so the deployment context defaults to **upstream**.
