# Step 1 -- Data Extraction for TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (scoped) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (source dependency) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Deployment Context Lookup

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | customer-shipped |

The affected component `pscomponent:org/rhtpa-server` maps to the `rhtpa-backend` source repository. The Source Repositories table in CLAUDE.md includes a Deployment Context column with the value `customer-shipped` for rhtpa-backend.

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is scoped to stream 2.2.x only.

## Ecosystem Detection

quinn-proto is a Rust crate -- ecosystem is **Cargo** (source dependency). Per the ecosystem classification table, source dependency ecosystems produce **2 remediation tasks per stream** (upstream backport + downstream propagation).

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed version |

## Affects Versions Correction

PSIRT assigned **RHTPA 2.0.0** as the Affects Version, but there is no 2.0.x stream configured. Based on lock file analysis:

- **Affected in 2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 (quinn-proto < 0.11.14)
- **Not affected in 2.2.x**: versions 2.2.3, 2.2.4 (quinn-proto = 0.11.14, fixed)
- **Affected in 2.1.x**: versions 2.1.0, 2.1.1 (quinn-proto = 0.11.9)

The Affects Versions field should be corrected to reflect the actual affected versions: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (for the scoped 2.2.x stream). Stream 2.1.x is also affected (cross-stream impact -- Case A).

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but version impact analysis shows that stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9). Since the issue is scoped, Case A applies -- post cross-stream impact comment and create preemptive remediation tasks for stream 2.1.x.
