# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Source Evidence

Lock file data extracted via `git show <tag>:Cargo.lock` for each pinned source commit:

| Version | Backend Tag | Command | quinn-proto Version |
|---------|-------------|---------|---------------------|
| 2.1.0 | v0.3.8 | `git show v0.3.8:Cargo.lock` | 0.11.9 |
| 2.1.1 | v0.3.12 | `git show v0.3.12:Cargo.lock` | 0.11.9 |
| 2.2.0 | v0.4.5 | `git show v0.4.5:Cargo.lock` | 0.11.9 |
| 2.2.1 | v0.4.8 | `git show v0.4.8:Cargo.lock` | 0.11.12 |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | (same as 2.2.1) |
| 2.2.3 | v0.4.11 | `git show v0.4.11:Cargo.lock` | 0.11.14 |
| 2.2.4 | v0.4.12 | `git show v0.4.12:Cargo.lock` | 0.11.14 |

## Fix Threshold

- Jira description: fixed in 0.11.14
- Affected range: versions before 0.11.14
- Fix threshold used for comparison: **>= 0.11.14**

## Stream Impact Summary

| Stream | Affected Versions | Not Affected Versions |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 | (none) |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |

- **Stream 2.2.x**: The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fixed version). Remediation is a dependency bump (`cargo update`) + downstream propagation.
- **Stream 2.1.x**: The upstream branch `release/0.3.z` still has quinn-proto 0.11.9. Remediation requires an upstream backport (bump quinn-proto on release/0.3.z) + downstream propagation.

## Affects Versions Correction (Step 3)

The issue is scoped to stream 2.2.x. PSIRT assigned `RHTPA 2.0.0` which does not correspond to any configured version stream.

- Current Affects Versions: `[RHTPA 2.0.0]`
- Proposed Affects Versions (scoped to 2.2.x): `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Version 2.2.2 is a retag of 2.2.1 (ships the same quinn-proto 0.11.12 which is within the affected range), so it is included as affected.

Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but version impact analysis reveals that stream **2.1.x** is also affected:
- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

Cross-stream impact comment would be posted per Case A, and preemptive remediation tasks would be created for stream 2.1.x if no sibling CVE Jira exists for that stream.
