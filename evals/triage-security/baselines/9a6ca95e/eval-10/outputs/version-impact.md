# Step 2 -- Version Impact Analysis: CVE-2026-55123

## Version Impact Table

Version Impact for CVE-2026-55123 (tokio < 1.42.0):

| Version | Stream | Build Tag | tokio version | Affected? | Notes |
|---------|--------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | v0.3.8 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | v0.3.12 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | v0.4.5 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | v0.4.8 | 1.41.1 | YES | |

All four supported versions ship tokio < 1.42.0 and are therefore affected.

## Cross-Stream Summary

- **Stream 2.1.x** (rhtpa-2.1): Both versions (2.1.0, 2.1.1) ship tokio 1.40.0 -- AFFECTED
- **Stream 2.2.x** (rhtpa-2.2): Both versions (2.2.0, 2.2.1) ship tokio 1.41.1 -- AFFECTED

The current issue TC-8020 is scoped to stream rhtpa-2.2 (2.2.x). Stream rhtpa-2.1 (2.1.x) is also affected but falls outside the issue's scope.

## Dependency Chain Context

```
Dependency chain for tokio (Cargo):
  backend (workspace) -> tokio (runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (tokio is a runtime dependency)

  Stream 2.1.x: tokio 1.40.0 at tags v0.3.8, v0.3.12
  Stream 2.2.x: tokio 1.41.1 at tags v0.4.5, v0.4.8
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.1.x | Cargo | release/0.3.z | 1.42.0 | Requires upstream backport |
| 2.2.x | Cargo | release/0.4.z | 1.42.0 | Requires upstream backport |
