# Step 2 -- Version Impact Analysis

## Version Impact Table

CVE-2026-31812 affects quinn-proto versions < 0.11.14. Fixed version: 0.11.14.

All versions from the security-matrix.md supportability matrices are included
(Important Rule 4). Dependency versions are extracted using the pinned commit
tags from the supportability matrix for each version (Important Rule 13), not
branch HEAD.

| Version | Stream | Pinned Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1; backend tag v0.4.8 reused) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | 0.11.14 >= 0.11.14 (at fix threshold) |

**Evidence source:** Each version's quinn-proto dependency version was extracted
via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'` using the
pinned backend tag from the supportability matrix. Version 2.2.2 was skipped
(Important Rule 5) because it is a retag of 2.2.1 (identical backend source
commit v0.4.8); its affected status is carried forward from 2.2.1.

## Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Streams affected**: 2.1.x (all versions), 2.2.x (versions 2.2.0-2.2.2 only)

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock as a direct workspace dependency)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Evidence |
|--------|-----------|-----------------|----------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR quinn-rs/quinn#2048 available |
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR quinn-rs/quinn#2048 available |

The upstream fix PR (quinn-rs/quinn#2048) is referenced in the CVE advisory.
Remediation tasks should verify the fix is included on the relevant upstream
branches.
