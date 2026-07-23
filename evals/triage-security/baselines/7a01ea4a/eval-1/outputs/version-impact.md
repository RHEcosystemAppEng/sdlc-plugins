# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix threshold**: quinn-proto >= 0.11.14
- **Fix first appeared in**: 2.2.3 (build 0.4.11, backend tag v0.4.11)

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: to be determined via lock file inspection
  Profile: production (quinn-proto is a QUIC transport runtime dependency)
  Ecosystem: Cargo
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Notes |
|--------|-----------|-----------------|-------|
| 2.1.x | Cargo | release/0.3.z | Upstream branch HEAD check required |
| 2.2.x | Cargo | release/0.4.z | Fix already present in v0.4.11+ (ships 0.11.14) |

The fix (quinn-proto 0.11.14) is already present in the 2.2.x stream starting from
build 0.4.11 (version 2.2.3). Versions 2.2.0, 2.2.1, and 2.2.2 shipped vulnerable
versions (0.11.9 and 0.11.12 respectively).

For the 2.1.x stream, both versions (2.1.0 and 2.1.1) ship quinn-proto 0.11.9 which
is within the affected range. Upstream branch release/0.3.z needs to be checked for
fix availability.
