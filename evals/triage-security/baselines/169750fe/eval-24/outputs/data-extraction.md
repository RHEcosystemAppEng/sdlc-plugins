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

## Stream Scope

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream. This issue is **stream-scoped** to 2.2.x only.

## Ecosystem

**Cargo** (Rust crate: quinn-proto). The Ecosystem Mappings for both streams list Cargo with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

## Deployment Context

The Source Repositories table in CLAUDE.md does **not** have a Deployment Context column. Per backward-compatibility rules, all repositories default to `upstream`. Because the column is absent, coordination guidance is omitted entirely from remediation task descriptions.

## Version Impact Analysis

### Stream 2.2.x (rhtpa-release.0.4.z) -- in scope

| Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------|-------------|-------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.11.12 | YES | retag of 2.2.1, same as v0.4.8 |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | = fixed version |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | = fixed version |

**Stream 2.2.x result**: Affected in versions 2.2.0--2.2.2. Already fixed starting from version 2.2.3 (backend tag v0.4.11 ships quinn-proto 0.11.14). The upstream branch `release/0.4.z` already contains the fix. No remediation tasks needed for this stream.

### Stream 2.1.x (rhtpa-release.0.3.z) -- cross-stream

| Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------|-------------|-------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

**Stream 2.1.x result**: All versions affected. The upstream branch `release/0.3.z` does NOT ship the fix (latest tag v0.3.12 has quinn-proto 0.11.9). Remediation is required.

## Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Corrected (based on lock file evidence)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 is not a valid version in either configured stream. The actual affected versions within the issue's 2.2.x scope are 2.2.0, 2.2.1, and 2.2.2 based on lock file evidence showing quinn-proto < 0.11.14. Versions 2.2.3 and 2.2.4 ship the fixed version and are not affected.

## Cross-Stream Impact (Case A)

Stream 2.1.x is also affected (all versions ship quinn-proto 0.11.9). Since the issue is scoped to 2.2.x, preemptive remediation tasks are created for stream 2.1.x (see remediation.md).

## Triage Outcome Summary

- **Stream 2.2.x**: Already fixed in 2.2.3+. Affects Versions correction needed. No remediation tasks.
- **Stream 2.1.x**: All versions affected. Preemptive remediation tasks needed (upstream backport + downstream propagation).
