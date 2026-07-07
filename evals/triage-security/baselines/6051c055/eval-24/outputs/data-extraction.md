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
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3--8 apply primarily to this stream. Cross-stream impact on 2.1.x is handled via Case B.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings tables in both streams list **Cargo** with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

Ecosystem: **Cargo** (source dependency)

## Deployment Context

The Source Repositories table in CLAUDE.md does **not** have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`.

| Repository | Deployment Context |
|------------|--------------------|
| rhtpa-backend | upstream (default -- column absent) |

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14, fixed in 0.11.14):

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fix present |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fix present |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed at HEAD? |
|--------|-----------|-----------------|-------------------|----------------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

## Affects Versions Correction

The PSIRT-assigned Affects Versions field contains **RHTPA 2.0.0**, which does not correspond to any configured version stream. Based on lock file evidence:

- **Affected versions in scoped stream (2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected in scoped stream**: RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14)
- **Cross-stream affected (2.1.x)**: RHTPA 2.1.0, RHTPA 2.1.1

Proposed correction: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (scoped stream only; 2.1.x tracked via companion issues).
