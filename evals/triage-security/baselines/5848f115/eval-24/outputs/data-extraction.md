# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (source dependency) |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Existing comments | None |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z).

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context

Source Repositories table does not have a Deployment Context column. Per backward-compatibility rules, all repos default to `upstream` for internal mapping. Coordination Guidance subsection is omitted from remediation task descriptions.

## Version Impact Table

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= fix version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= fix version |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

## Affects Versions Correction

**Current (PSIRT-assigned):** RHTPA 2.0.0

PSIRT-assigned Affects Version is incorrect -- RHTPA 2.0.0 does not correspond to any version in the supportability matrix.

**Proposed (scoped to 2.2.x stream):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Rationale: Lock file analysis confirms quinn-proto < 0.11.14 is present in versions 2.2.0 (0.11.9), 2.2.1 (0.11.12), and 2.2.2 (retag of 2.2.1). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but version impact analysis reveals stream **2.1.x** is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

The upstream fix has NOT landed on release/0.3.z (the 2.1.x upstream branch). Preemptive remediation tasks are required for the 2.1.x stream.

## Triage Outcome Summary

- **2.2.x (scoped stream):** Affected in 2.2.0, 2.2.1, 2.2.2 but already fixed in 2.2.3+ (quinn-proto 0.11.14). No new remediation tasks needed for this stream. Affects Versions corrected.
- **2.1.x (cross-stream):** Affected in 2.1.0, 2.1.1 with no fix in the stream. Preemptive remediation tasks created (see remediation.md).
