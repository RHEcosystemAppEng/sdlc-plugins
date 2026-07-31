# Step 2 -- Version Impact Analysis

## Version Impact Table for CVE-2026-31812 (quinn-proto < 0.11.14)

### Stream 2.2.x (issue scope)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

### Stream 2.1.x (cross-stream analysis)

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |

## Summary

- **Stream 2.2.x**: versions 2.2.0, 2.2.1, and 2.2.2 are affected (ship quinn-proto < 0.11.14). Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 and are NOT affected.
- **Stream 2.1.x**: versions 2.1.0 and 2.1.1 are affected (ship quinn-proto 0.11.9). This is a cross-stream impact finding -- the 2.1.x stream is outside the issue scope.

## Dependency Chain

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```
