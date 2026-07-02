# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | pinned commit v0.3.8 |
| 2.1.1 | 2.1.x | 0.11.9 | YES | pinned commit v0.3.12 |
| 2.2.0 | 2.2.x | 0.11.9 | YES | pinned commit v0.4.5 |
| 2.2.1 | 2.2.x | 0.11.12 | YES | pinned commit v0.4.8 |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | pinned commit v0.4.11; ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | pinned commit v0.4.12; ships fixed version |

## Lock File Evidence

Dependency versions extracted via `git show <tag>:Cargo.lock` for the backend repository:

| Tag | quinn-proto version | Comparison to fix threshold (0.11.14) |
|-----|---------------------|---------------------------------------|
| v0.3.8 | 0.11.9 | < 0.11.14 -- VULNERABLE |
| v0.3.12 | 0.11.9 | < 0.11.14 -- VULNERABLE |
| v0.4.5 | 0.11.9 | < 0.11.14 -- VULNERABLE |
| v0.4.8 | 0.11.12 | < 0.11.14 -- VULNERABLE |
| v0.4.9 | (retag of v0.4.8) | same as v0.4.8 -- VULNERABLE |
| v0.4.11 | 0.11.14 | >= 0.11.14 -- FIXED |
| v0.4.12 | 0.11.14 | >= 0.11.14 -- FIXED |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag | Version at Latest Tag | Fixed? |
|--------|-----------|-----------------|------------|-----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

### Stream 2.2.x

The upstream branch `release/0.4.z` already carries the fix. The latest tags (v0.4.11, v0.4.12) ship quinn-proto 0.11.14. Versions 2.2.3 and 2.2.4 already include the fixed dependency. No upstream backport is needed for this stream.

### Stream 2.1.x

The upstream branch `release/0.3.z` does NOT carry the fix. The latest tag v0.3.12 ships quinn-proto 0.11.9. An upstream backport is required to bump quinn-proto to >= 0.11.14 on release/0.3.z.

## Summary

- **2.2.x stream** (issue scope): 3 affected versions (2.2.0, 2.2.1, 2.2.2), 2 already fixed (2.2.3, 2.2.4). Upstream fix is already present on release/0.4.z.
- **2.1.x stream** (cross-stream): 2 affected versions (2.1.0, 2.1.1). Upstream fix is NOT present on release/0.3.z. This stream requires separate remediation.
