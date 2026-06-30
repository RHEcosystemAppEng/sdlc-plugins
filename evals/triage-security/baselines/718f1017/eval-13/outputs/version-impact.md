# Step 2 - Version Impact Analysis for TC-8001

## 2.1 - Supportability Matrix

Loaded from two streams configured in Security Configuration Version Streams table:

- **Stream 2.1.x**: `security-matrix.md` at rhtpa-release.0.3.z path
- **Stream 2.2.x**: `security-matrix.md` at rhtpa-release.0.4.z path

## 2.2 - Development Stream

Would query Jira for unreleased versions with prefix `RHTPA` to identify the current development stream. The development stream is checked at branch HEAD (not a pinned commit).

## 2.3 - Dependency Version Extraction

Lock file inspection results for quinn-proto at each pinned source commit:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | Command | quinn-proto version | Affected? |
|---------|-----|---------|---------------------|-----------|
| 2.1.0 | `v0.3.8` | `git show v0.3.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.9 | YES (< 0.11.14) |
| 2.1.1 | `v0.3.12` | `git show v0.3.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.9 | YES (< 0.11.14) |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Tag | Command | quinn-proto version | Affected? |
|---------|-----|---------|---------------------|-----------|
| 2.2.0 | `v0.4.5` | `git show v0.4.5:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.9 | YES (< 0.11.14) |
| 2.2.1 | `v0.4.8` | `git show v0.4.8:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.12 | YES (< 0.11.14) |
| 2.2.2 | `v0.4.9` | _(retag of v0.4.8 -- skipped, same as 2.2.1)_ | 0.11.12 | YES (same as 2.2.1) |
| 2.2.3 | `v0.4.11` | `git show v0.4.11:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.14 | NO (>= 0.11.14) |
| 2.2.4 | `v0.4.12` | `git show v0.4.12:Cargo.lock \| grep -A2 'name = "quinn-proto"'` | 0.11.14 | NO (>= 0.11.14) |

## 2.4 - Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

### Dependency Chain Context (Step 2.3.5)

Dependency chain for quinn-proto (Cargo):
- quinn-proto is part of the quinn QUIC transport library
- It is a transitive dependency brought in through the QUIC networking stack
- Ecosystem: Cargo (source-level dependency)
- Profile: production (runtime dependency, not dev-only)

The dependency is present in all versions from both streams, indicating it was introduced early in the project's dependency tree.

## 2.5 - Upstream Fix Check

Upstream fix status per stream:

| Stream | Ecosystem | Upstream Branch | Check Command | Notes |
|--------|-----------|-----------------|---------------|-------|
| 2.1.x | Cargo | `release/0.3.z` | `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock \| grep -A2 'quinn-proto'` | Would check branch HEAD |
| 2.2.x | Cargo | `release/0.4.z` | `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock \| grep -A2 'quinn-proto'` | Would check branch HEAD |

Upstream fix PR is available: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048)

## Summary

- **Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Affected versions in scope (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions in scope (2.2.x)**: 2.2.3, 2.2.4
- **Cross-stream impact**: 2.1.x stream is also affected (2.1.0, 2.1.1) -- this triggers Case B (cross-stream impact)
- **Affects Versions correction needed**: PSIRT assigned `RHTPA 2.0.0` which does not match any supported version. Correct to `RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2` (scoped to 2.2.x stream only).
