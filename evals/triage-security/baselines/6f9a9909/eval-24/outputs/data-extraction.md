# Step 1 — Data Extraction: TC-8001

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
| Ecosystem | Cargo (Rust crate — source dependency) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- Issue is **scoped** to 2.2.x — Steps 3 and 4 apply only to this stream; Case A cross-stream check covers 2.1.x

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Classification: **Source dependency** — 2 remediation tasks per affected stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context

- Repository: rhtpa-backend
- Deployment Context column: **absent** from Source Repositories table (backward compatibility)
- Default: `upstream`
- Coordination guidance: **omitted** (column absent — per skill rules, do not add the subsection)

## Version Impact Analysis (Step 2)

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | — | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | fixed at 0.11.14 |

### Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `RHTPA 2.0.0` — **incorrect** (RHTPA 2.0.0 does not exist in any stream)
- Proposed (scoped to 2.2.x): `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2`
- Rationale: Lock file analysis at pinned commits shows quinn-proto < 0.11.14 in versions 2.2.0 through 2.2.2; versions 2.2.3+ ship quinn-proto 0.11.14 (fixed)

### Cross-Stream Impact (Case A)

- Issue is scoped to **2.2.x**
- Stream **2.1.x** is also affected: versions 2.1.0 and 2.1.1 both ship quinn-proto 0.11.9
- No sibling CVE Jira found for 2.1.x stream (no issue with `[rhtpa-2.1]` suffix)
- Action: Create **preemptive** remediation tasks for 2.1.x with `security-preemptive` label
