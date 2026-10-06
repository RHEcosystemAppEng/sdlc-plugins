# Step 2 — Version Impact Analysis: CVE-2026-31812

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

- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1) — ships quinn-proto 0.11.9
- **Stream 2.2.x**: versions 2.2.0, 2.2.1, 2.2.2 affected; versions 2.2.3, 2.2.4 NOT affected (ship 0.11.14, the fix version)

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo ecosystem)
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (v0.4.12) | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **Stream 2.2.x**: Fixed upstream on release/0.4.z (v0.4.11+ ships 0.11.14). Remediation is a Konflux release repo change: bump the source tag to pick up the fix.
- **Stream 2.1.x**: NOT fixed upstream on release/0.3.z (still ships 0.11.9). Remediation requires an upstream PR first to bump quinn-proto on the 0.3.z branch, then a Konflux release repo update.
