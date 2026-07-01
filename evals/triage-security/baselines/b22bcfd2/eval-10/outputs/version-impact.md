# Step 2 -- Version Impact Analysis

## Version Impact Table

The version impact analysis covers **all streams** (not just the issue's scoped stream 2.2.x) to detect cross-stream impact. Dependency versions are extracted from `Cargo.lock` at each version's pinned source commit tag, as specified in the supportability matrix.

### Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | Source Tag | tokio version | Affected? | Notes |
|---------|--------|------------|---------------|-----------|-------|
| RHTPA 2.1.0 | 2.1.x | `v0.3.8` | 1.40.0 | **YES** | < 1.42.0 |
| RHTPA 2.1.1 | 2.1.x | `v0.3.12` | 1.40.0 | **YES** | < 1.42.0 |
| RHTPA 2.2.0 | 2.2.x | `v0.4.5` | 1.41.1 | **YES** | < 1.42.0 |
| RHTPA 2.2.1 | 2.2.x | `v0.4.8` | 1.41.1 | **YES** | < 1.42.0 |
| RHTPA 2.2.2 | 2.2.x | `v0.4.9` | -- | **YES** | retag of 2.2.1 (same as RHTPA 2.2.1) |
| RHTPA 2.2.3 | 2.2.x | `v0.4.11` | 1.41.1 | **YES** | < 1.42.0 |
| RHTPA 2.2.4 | 2.2.x | `v0.4.12` | 1.41.1 | **YES** | < 1.42.0 |

**All versions across both streams ship tokio < 1.42.0 and are affected.**

## Cross-Stream Impact Summary

| Stream | Versions Checked | Affected? | tokio range shipped |
|--------|-----------------|-----------|---------------------|
| 2.1.x | 2.1.0, 2.1.1 | **YES** -- all versions affected | 1.40.0 |
| 2.2.x | 2.2.0 through 2.2.4 | **YES** -- all versions affected | 1.41.1 |

**Cross-stream impact detected**: Stream rhtpa-2.1 is also affected (tokio 1.40.0, fix threshold 1.42.0). This issue is scoped to rhtpa-2.2, so stream rhtpa-2.1 requires separate attention (see Step 8 Case B).

## Dependency Chain Context

```
Dependency chain for tokio (Cargo):
  rhtpa-server (workspace) -> tokio (runtime dependency)
  Profile: production (tokio is a core runtime dependency)
  
  Present in: all versions across both streams (2.1.x and 2.2.x)
  All versions ship tokio < 1.42.0 (vulnerable)
```

## Retag Handling

- **RHTPA 2.2.2**: retag of RHTPA 2.2.1 (backend source tag `v0.4.8` is identical). Lock file check skipped; result carried forward from RHTPA 2.2.1: tokio 1.41.1, **YES** (affected).
