# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Scoped stream (2.2.x)**: versions 2.2.0, 2.2.1, and 2.2.2 are affected; versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are not affected.
- **Other stream (2.1.x)**: versions 2.1.0 and 2.1.1 are affected (quinn-proto 0.11.9 < 0.11.14). This cross-stream impact triggers Case B in Step 8.

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock at all build tags)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)

First appeared: present in all versions across both streams
```

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Available |
|--------|-----------|-----------------|---------------|
| 2.2.x | Cargo | release/0.4.z | YES (v0.4.11+ already ships 0.11.14) |
| 2.1.x | Cargo | release/0.3.z | NO (latest v0.3.12 still ships 0.11.9) |
