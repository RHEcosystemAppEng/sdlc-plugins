# Step 2 -- Version Impact Analysis

## Supportability Matrix (Aggregated)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.1.0 | 0.3.8 | 2025-09-15 | `v0.3.8` | |
| 2.1.1 | 0.3.12 | 2025-11-20 | `v0.3.12` | |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | `v0.4.5` | |
| 2.2.1 | 0.4.8 | 2026-02-05 | `v0.4.8` | |
| 2.2.2 | 0.4.9 | 2026-02-23 | `v0.4.8` | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | `v0.4.11` | |
| 2.2.4 | 0.4.12 | 2026-05-04 | `v0.4.12` | |

## Dependency Version Extraction

Lock file check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

Fix threshold: **0.11.14** (versions before 0.11.14 are vulnerable)

| Tag | quinn-proto version | Source |
|-----|---------------------|--------|
| `v0.3.8` | 0.11.9 | Cargo.lock |
| `v0.3.12` | 0.11.9 | Cargo.lock |
| `v0.4.5` | 0.11.9 | Cargo.lock |
| `v0.4.8` | 0.11.12 | Cargo.lock |
| `v0.4.9` | _(retag of v0.4.8)_ | same as v0.4.8 |
| `v0.4.11` | 0.11.14 | Cargo.lock |
| `v0.4.12` | 0.11.14 | Cargo.lock |

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- both ship quinn-proto 0.11.9
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14)
- The fix was picked up in the 2.2.x stream starting with build 0.4.11 (version 2.2.3)

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Backend Tag at HEAD | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 (latest) | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 (latest) | 0.11.14 | YES |

The upstream fix is present on `release/0.4.z` (2.2.x stream) but NOT on `release/0.3.z` (2.1.x stream). The 2.1.x stream requires an upstream backport before the fix can be propagated.
