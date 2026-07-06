# Step 1 — Data Extraction: TC-8001

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x**.
This issue is **stream-scoped** to the 2.2.x stream.

## Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.
Cargo is configured in both streams' Ecosystem Mappings tables with:
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch (2.1.x): `release/0.3.z`
- Upstream branch (2.2.x): `release/0.4.z`

## Deployment Context

Source Repositories table does **not** have a Deployment Context column.
Per backward compatibility rules, all repositories default to `upstream`.
Coordination Guidance subsection is omitted from remediation tasks.

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

## Affects Versions Correction

PSIRT-assigned Affects Versions: **RHTPA 2.0.0** (incorrect -- no 2.0.x stream exists).

Correct Affects Versions based on lock file evidence (scoped to 2.2.x):
- **RHTPA 2.2.0** (quinn-proto 0.11.9 -- affected)
- **RHTPA 2.2.1** (quinn-proto 0.11.12 -- affected)
- **RHTPA 2.2.2** (retag of 2.2.1 -- affected)

Remove: RHTPA 2.0.0 (no such stream configured).

## Cross-Stream Impact

Stream 2.1.x is **also affected** (all versions ship quinn-proto 0.11.9).
This is outside the issue's scope (`[rhtpa-2.2]`) and triggers Case B
(preemptive remediation for streams without their own CVE Jira).
