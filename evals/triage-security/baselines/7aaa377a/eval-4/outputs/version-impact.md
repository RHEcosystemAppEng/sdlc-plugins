# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-33501 (h2 < 0.4.8)

All versions from all configured streams are included because this issue is
**unscoped** (no stream suffix). No versions are skipped.

| Version | Stream | Pinned Commit | h2 Version | Affected? | Notes |
|---------|--------|---------------|------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.4.5 | YES | < 0.4.8 |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.4.5 | YES | < 0.4.8 |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.4.8 | NO | >= 0.4.8 (ships fixed version) |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.4.8 | NO | >= 0.4.8 (ships fixed version) |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.4.9 | NO | >= 0.4.8 |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.4.9 | NO | >= 0.4.8 |

## Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1 both ship h2 0.4.5)
- **2.2.x stream**: NO versions affected (all ship h2 >= 0.4.8, the fixed version)

Mixed impact across streams: remediation is needed only for the 2.1.x stream.

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (h2 is listed in Cargo.lock as a direct dependency)
  Profile: production (h2 is a runtime dependency used for HTTP/2 support)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | h2 at branch HEAD | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | _(to be verified via git show)_ | _(pending)_ |
| 2.2.x | Cargo | `release/0.4.z` | 0.4.8+ | YES |

The 2.2.x upstream branch already ships the fix. For the 2.1.x stream, the
upstream branch `release/0.3.z` must be checked to determine whether the fix
has been backported.
