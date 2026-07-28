# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | |

All versions are checked using pinned commit tags from the supportability matrix,
not branch HEAD (per Important Rule 13). Retag version 2.2.2 carries forward the
result from 2.2.1 (per Important Rule 5).

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.2.x | Cargo | release/0.4.z | Upstream fix PR: quinn-rs/quinn#2048 |
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR: quinn-rs/quinn#2048 |

## Summary

- **2.2.x stream (in scope)**: versions 2.2.0, 2.2.1, 2.2.2 are affected; 2.2.3, 2.2.4 are not affected.
- **2.1.x stream (out of scope)**: versions 2.1.0, 2.1.1 are affected -- will be handled via Case A cross-stream impact.
