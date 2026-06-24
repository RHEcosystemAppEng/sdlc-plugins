# Step 2 -- Version Impact Analysis: CVE-2026-55123 (tokio < 1.42.0)

## Version Impact Table

| Version | Stream | tokio version | Affected? | Notes |
|---------|--------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.1.1 | rhtpa-2.1 | 1.40.0 | YES | |
| RHTPA 2.2.0 | rhtpa-2.2 | 1.41.1 | YES | |
| RHTPA 2.2.1 | rhtpa-2.2 | 1.41.1 | YES | |

All four supported versions ship tokio below the fix threshold of 1.42.0 and are affected by CVE-2026-55123.

## Cross-Stream Impact Summary

- **rhtpa-2.2 (this issue's stream):** Both versions (2.2.0, 2.2.1) ship tokio 1.41.1 -- AFFECTED
- **rhtpa-2.1 (other stream):** Both versions (2.1.0, 2.1.1) ship tokio 1.40.0 -- AFFECTED

The vulnerability affects versions across **both** configured version streams.

## Dependency Chain Context

```
Dependency chain for tokio:
  backend (workspace) -> tokio (direct runtime dependency)
  Profile: production (tokio is a core async runtime dependency)
  Ecosystem: Cargo (Cargo.lock)
```

tokio is a direct dependency of the backend service. It is the async runtime used throughout the application, meaning this is a direct dependency bump -- no transitive chain complexity.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| rhtpa-2.2 | Cargo | release/0.4.z | 1.42.0 | Requires upstream PR to bump tokio |
| rhtpa-2.1 | Cargo | release/0.3.z | 1.42.0 | Requires upstream PR to bump tokio |
