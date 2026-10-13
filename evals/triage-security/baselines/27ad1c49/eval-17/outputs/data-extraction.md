# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

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

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the configured Version Streams table. This issue is **stream-scoped** to 2.2.x only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. This maps to the **Cargo** ecosystem as defined in the stream's Ecosystem Mappings table. Cargo is a source dependency ecosystem, which produces **two remediation tasks per stream** (upstream fix + downstream propagation), or dependency bump + downstream propagation when the upstream fix is already available.

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table. The Deployment Context column is absent from the table, so the deployment context defaults to **upstream**.

## Affects Versions Mismatch (Preliminary)

PSIRT assigned Affects Versions: **RHTPA 2.0.0**
There is no `2.0.x` stream in the configured Version Streams. This is an incorrect PSIRT assignment that will be corrected in Step 3 based on lock file evidence from the version impact analysis.
