# Step 2 -- Version Impact Analysis for CVE-2026-33501

## CVE Details

- **Library**: h2
- **Affected range**: < 0.4.8
- **Fixed version**: 0.4.8

## Version Impact Table

Since the issue is **unscoped** (no stream suffix), ALL versions across ALL streams are analyzed.

### Version Impact for CVE-2026-33501 (h2 < 0.4.8):

| Version | Stream | Pinned Tag | h2 version | Affected? | Notes |
|---------|--------|------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | **YES** | 0.4.5 < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Summary

- **Stream 2.1.x**: All versions are **AFFECTED** (ship h2 0.4.5, which is below the fix threshold 0.4.8)
- **Stream 2.2.x**: All versions are **NOT AFFECTED** (ship h2 0.4.8 or later, which meets or exceeds the fix threshold)

The version impact is **mixed across streams**: 2.1.x versions are affected while 2.2.x versions already ship the patched dependency.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> hyper -> h2
  Ecosystem: Cargo (source dependency)
  Profile: production (h2 is a runtime HTTP/2 dependency via hyper)

  Present in: all versions across both streams
  Affected in: 2.1.x only (h2 0.4.5)
  Fixed in: 2.2.x (h2 >= 0.4.8 since version 2.2.0)
```

## Evidence

All version impact assessments use pinned commit tags from the supportability matrix, not branch HEAD. The h2 dependency versions were extracted via `git show <tag>:Cargo.lock | grep -A2 'name = "h2"'` for each pinned tag.
