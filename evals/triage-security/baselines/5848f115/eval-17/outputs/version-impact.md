# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|--------|---------|-------|-------------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | 0.3.8 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | 0.3.12 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | 0.4.5 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | 0.4.8 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | 0.4.9 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | 0.4.11 | `v0.4.11` | 0.11.14 | NO | fixed version shipped |
| 2.2.x | 2.2.4 | 0.4.12 | `v0.4.12` | 0.11.14 | NO | fixed version shipped |

**Fix threshold**: quinn-proto >= 0.11.14 (from Jira description and CVE data)

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime QUIC transport dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock
```

quinn-proto is a direct dependency of the backend workspace. Remediation is a straightforward version bump in `Cargo.toml` / `Cargo.lock`.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | (requires verification) | Unknown |
| 2.2.x | Cargo | release/0.4.z | (requires verification) | Unknown |

Based on the version impact table, the fix (quinn-proto 0.11.14) was first included in version 2.2.3 (build 0.4.11, tag `v0.4.11`). This suggests the upstream `release/0.4.z` branch has already been fixed. The `release/0.3.z` branch still ships 0.11.9 as of the latest release (2.1.1), so it likely requires an upstream backport.

## Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Issue stream scope**: 2.2.x only
- **Cross-stream impact**: 2.1.x stream is also affected (all versions)
- **PSIRT Affects Versions (current)**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Proposed Affects Versions (scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The Affects Versions field needs correction from `RHTPA 2.0.0` to the actual affected versions within the 2.2.x stream scope.
