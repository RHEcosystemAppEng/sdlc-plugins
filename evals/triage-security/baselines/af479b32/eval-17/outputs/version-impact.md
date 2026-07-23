# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Stream Summary

| Stream | Affected Versions | Unaffected Versions | Status |
|--------|-------------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | -- | All versions affected |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 | Partially fixed (fixed from 2.2.3 onward) |

## Issue Scope

This issue is **scoped to stream 2.2.x** (per summary suffix `[rhtpa-2.2]`).

- **In-scope affected versions**: 2.2.0, 2.2.1, 2.2.2
- **In-scope unaffected versions**: 2.2.3, 2.2.4 (already ship quinn-proto 0.11.14)
- **Cross-stream impact**: Stream 2.1.x is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9) -- this triggers Case B cross-stream handling.

## Dependency Chain

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Type: (to be determined via lock file / manifest inspection)
  Profile: production (quinn-proto is a runtime QUIC transport dependency)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | quinn-proto at Tag | Fixed? |
|--------|-----------|-----------------|--------------------|--------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

- **Stream 2.2.x**: The upstream fix is already present. Tags v0.4.11 and v0.4.12 ship quinn-proto 0.11.14 (the fixed version). No upstream backport is needed for this stream -- the fix was picked up starting from build 0.4.11 (version 2.2.3).
- **Stream 2.1.x**: The upstream branch `release/0.3.z` does NOT have the fix. The latest tag (v0.3.12) ships quinn-proto 0.11.9, which is vulnerable. An upstream backport would be needed if remediation is required for this stream.

## Affects Versions Correction (Step 3 preview)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, which does not correspond to any version in the supportability matrix. The correct Affects Versions for the scoped stream (2.2.x) should be:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Versions 2.2.3 and 2.2.4 are NOT included because they ship quinn-proto 0.11.14 (the fixed version).
