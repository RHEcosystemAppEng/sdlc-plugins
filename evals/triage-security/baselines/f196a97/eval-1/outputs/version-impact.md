# Step 2 - Version Impact Analysis

## Supportability Matrix (Aggregated)

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 |

## Dependency Extraction (quinn-proto via Cargo.lock)

Extracted from `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` for each pinned commit:

| Tag | quinn-proto version |
|-----|---------------------|
| v0.3.8 | 0.11.9 |
| v0.3.12 | 0.11.9 |
| v0.4.5 | 0.11.9 |
| v0.4.8 | 0.11.12 |
| v0.4.9 | (retag of v0.4.8) |
| v0.4.11 | 0.11.14 |
| v0.4.12 | 0.11.14 |

## Version Impact Table

CVE-2026-31812 affects quinn-proto versions before 0.11.14. Fixed version: 0.11.14.

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn (QUIC transport) -> quinn-proto
  Ecosystem: Cargo (source dependency)
  Profile: production (quinn-proto is a runtime dependency for QUIC protocol handling)

Present in: all versions across both streams (0.11.9 in 2.1.x and 2.2.0, upgraded to 0.11.12 in 2.2.1-2.2.2, fixed at 0.11.14 in 2.2.3+)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (not checked - outside issue scope) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (based on latest tag v0.4.11+) | YES |

The upstream fix for the 2.2.x stream is already present on `release/0.4.z` -- the latest tags (v0.4.11, v0.4.12) already ship quinn-proto 0.11.14. This means remediation for affected 2.2.x versions (2.2.0, 2.2.1, 2.2.2) would involve bumping the backend reference in the Konflux release repo to a tag that includes the fix (v0.4.11 or later).

## Summary

- **2.2.x stream (issue scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix.
- **2.1.x stream (outside issue scope)**: Both 2.1.0 and 2.1.1 are affected (ship quinn-proto 0.11.9). This is a cross-stream impact that should be noted but not actioned by this issue (Case B).
