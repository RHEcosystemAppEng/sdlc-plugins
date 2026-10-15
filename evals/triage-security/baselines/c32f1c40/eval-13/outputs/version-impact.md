# Step 2 — Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | — | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

All versions are checked using pinned commit tags from the supportability matrix — not branch HEAD (Rule 13). Version 2.2.2 is a retag of 2.2.1 (identical backend source commit `v0.4.8`), so the lock file check is skipped and the result carried forward (Rule 5).

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Status |
|--------|-----------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | To be checked via `git show release/0.4.z:Cargo.lock` |
| 2.1.x | Cargo | release/0.3.z | To be checked via `git show release/0.3.z:Cargo.lock` |

## Summary

- **Affected versions (2.2.x stream — in scope):** 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x stream):** 2.2.3, 2.2.4
- **Cross-stream impact:** 2.1.x stream (2.1.0, 2.1.1) is also affected — see Step 8 Case A
