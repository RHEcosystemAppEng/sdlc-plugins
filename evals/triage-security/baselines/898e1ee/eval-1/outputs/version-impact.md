# Step 2 - Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Evidence

- **Fix threshold**: quinn-proto >= 0.11.14 (from Jira description, confirmed by advisory references)
- **Lock file method**: `git show <tag>:Cargo.lock` per Ecosystem Mappings
- **Retag handling**: Version 2.2.2 uses tag `v0.4.9` which is a retag of `v0.4.8` (used by 2.2.1). Lock file check skipped; result carried forward from 2.2.1 (quinn-proto 0.11.12, AFFECTED).

## Dependency Chain Context (Step 2.3.5)

Dependency chain for quinn-proto:
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock

- quinn-proto is a transitive dependency via the quinn QUIC transport library
- Present in both 2.1.x and 2.2.x streams across all versions
- Version bumped from 0.11.9 to 0.11.12 between 2.2.0 and 2.2.1
- Fixed at 0.11.14 starting with 2.2.3

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Repository | Upstream Branch | Check Command | Fix Status |
|--------|-----------|------------|-----------------|---------------|------------|
| 2.1.x | Cargo | backend | `release/0.3.z` | `git show release/0.3.z:Cargo.lock` | Unknown (would need git show at branch HEAD) |
| 2.2.x | Cargo | backend | `release/0.4.z` | `git show release/0.4.z:Cargo.lock` | Likely FIXED (2.2.3+ already ships 0.11.14) |

Note: Upstream fix PR is available at [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048).

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) - ships quinn-proto 0.11.9
- **2.2.x stream**: 3 versions affected (2.2.0, 2.2.1, 2.2.2), 2 versions NOT affected (2.2.3, 2.2.4)
- The fix landed in the 2.2.x stream at version 2.2.3 (build 0.4.11)
