# Step 2 — Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | **YES** | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | **YES** | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | **YES** | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | **YES** | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: source dependency (Cargo crate)
  Lock file: Cargo.lock
  Profile: production (runtime dependency)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | **NO** |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | **YES** |

## Analysis Summary

- **Stream 2.1.x**: All versions (2.1.0, 2.1.1) are affected. The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9 — the fix has **not** been backported to this stream.
- **Stream 2.2.x**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14). The upstream branch `release/0.4.z` has the fix — the fix is **already available** on this stream's upstream branch.

Since the issue is scoped to stream 2.2.x, the fix is already incorporated in the latest releases (2.2.3+). Cross-stream impact exists for the 2.1.x stream, where all versions remain affected and the upstream fix has not been backported.
