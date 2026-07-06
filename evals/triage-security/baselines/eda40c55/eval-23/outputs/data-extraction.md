# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is stream-scoped to **2.2.x only**.

## Ecosystem Detection

quinn-proto is a Rust crate. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`. This is a **source dependency** ecosystem.

## Deployment Context Lookup

Source Repositories table from CLAUDE.md Security Configuration:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

The affected component (`pscomponent:org/rhtpa-server`) maps to source repository **rhtpa-backend**. Deployment context: **customer-shipped**.

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions. For `customer-shipped` components, remediation tasks must include guidance to coordinate with Product Security for CVE assignment, advisory preparation, and formal disclosure.

## Affects Versions Discrepancy

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, but there is no 2.0.x version stream configured. Based on the version impact analysis, the correct Affects Versions for the 2.2.x stream are **RHTPA 2.2.0**, **RHTPA 2.2.1**, and **RHTPA 2.2.2**. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14, which is the fixed version.

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

### Cross-Stream Impact

The issue is scoped to **2.2.x**, but the **2.1.x** stream is also affected (all versions ship quinn-proto 0.11.9 < 0.11.14). This triggers Case B (cross-stream impact) in Step 8 for proactive remediation of the 2.1.x stream.
