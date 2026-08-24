# Step 2 — Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |

## Summary

- **Affected versions (2.2.x stream, issue scope)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions (2.2.x stream)**: 2.2.3, 2.2.4
- **Cross-stream impact (2.1.x)**: 2.1.0, 2.1.1 are also affected (all versions in 2.1.x ship quinn-proto 0.11.9)
- **Fix threshold**: quinn-proto >= 0.11.14

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present in Cargo.lock)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Tag at HEAD | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|-------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.11.14 | YES |

- **Stream 2.2.x**: Fix is already present upstream on `release/0.4.z` (quinn-proto 0.11.14 at v0.4.11+). Remediation is a downstream propagation to update the source reference for affected versions.
- **Stream 2.1.x**: Fix is NOT present upstream on `release/0.3.z`. Remediation requires an upstream backport PR first, then downstream propagation.
