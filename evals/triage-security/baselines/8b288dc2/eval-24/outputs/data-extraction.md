# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x only.

## Deployment Context

The Source Repositories table in CLAUDE.md does not have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`.

- rhtpa-backend: `upstream` (default -- no Deployment Context column present)

## Version Impact Analysis

Using mock lock file data for quinn-proto across stream 2.2.x:

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

## Cross-Stream Impact (outside issue scope)

Stream 2.1.x is also affected but outside this issue's scope:

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

## Affects Versions Correction

PSIRT-assigned Affects Versions (`RHTPA 2.0.0`) is incorrect. No `2.0.x` stream is configured. Within the scoped stream (2.2.x), versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are not affected.

Proposed correction: Replace `RHTPA 2.0.0` with `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`.
