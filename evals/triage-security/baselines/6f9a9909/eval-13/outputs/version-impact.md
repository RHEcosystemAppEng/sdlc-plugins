# Step 2 -- Version Impact Analysis for CVE-2026-31812

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

## Lock File Evidence

Dependency versions extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` for each pinned commit in the supportability matrix:

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| v0.3.8 | 0.11.9 | Cargo.lock at backend tag v0.3.8 |
| v0.3.12 | 0.11.9 | Cargo.lock at backend tag v0.3.12 |
| v0.4.5 | 0.11.9 | Cargo.lock at backend tag v0.4.5 |
| v0.4.8 | 0.11.12 | Cargo.lock at backend tag v0.4.8 |
| v0.4.9 | _(retag of v0.4.8)_ | Skipped -- same source as v0.4.8 |
| v0.4.11 | 0.11.14 | Cargo.lock at backend tag v0.4.11 |
| v0.4.12 | 0.11.14 | Cargo.lock at backend tag v0.4.12 |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (not checked -- 2.1.x not in issue scope, but cross-stream impact detected) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (per v0.4.11/v0.4.12 evidence) | YES |

The upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (the fixed version) as of tag v0.4.11. The fix was incorporated between v0.4.8 (0.11.12) and v0.4.11 (0.11.14).

## Affects Versions Correction

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not exist as a configured version. Based on lock file analysis, the corrected Affects Versions (scoped to stream 2.2.x per the issue suffix) are:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT included because they ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Impact

The issue is scoped to stream **2.2.x**, but the version impact analysis reveals that stream **2.1.x** is also affected:

- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This triggers **Case A** (cross-stream impact -- proactive remediation) for the 2.1.x stream.
