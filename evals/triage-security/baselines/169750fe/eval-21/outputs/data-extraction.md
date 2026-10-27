# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| Status | New | Issue status |
| Assignee | Unassigned | Issue assignee |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`)
- This is a **scoped** issue -- triage Steps 3-4 apply only to 2.2.x versions, but version impact analysis (Step 2) covers all streams to detect cross-stream impact.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport or dependency bump + downstream propagation)

## Version Impact Analysis (Step 2)

Using the security matrix data and lock file evidence for quinn-proto at each pinned commit:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- Issue Stream Scope

| Version | Build Tag | quinn-proto Version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | Meets fix threshold (>= 0.11.14) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | Meets fix threshold (>= 0.11.14) |

### Summary

- **Fix threshold**: quinn-proto >= 0.11.14
- **Versions affected in issue scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Versions not affected in issue scope (2.2.x)**: 2.2.3, 2.2.4 (already ship fixed version)
- **Cross-stream impact**: 2.1.x stream is also fully affected (all versions ship quinn-proto 0.11.9)
- **PSIRT Affects Versions mismatch**: PSIRT assigned "RHTPA 2.0.0" which does not correspond to any configured version stream -- correction needed in Step 3

## Affects Versions Correction (Step 3)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (scoped to 2.2.x stream)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Rationale**: RHTPA 2.0.0 is not a valid version in any configured stream. Lock file analysis shows quinn-proto 0.11.9/0.11.12 (affected) in versions 2.2.0-2.2.2, and fixed (0.11.14) in 2.2.3+.
- Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed quinn-proto version.
