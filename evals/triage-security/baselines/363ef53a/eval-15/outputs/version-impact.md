# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Stream 2.1.x**: all versions affected (2.1.0, 2.1.1)
- **Stream 2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 not affected (ship quinn-proto 0.11.14)

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Source Repo |
|--------|-----------|-----------------|-------------|
| 2.1.x | Cargo | release/0.3.z | backend |
| 2.2.x | Cargo | release/0.4.z | backend |
