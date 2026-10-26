# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

Stream 2.2.x: upstream branch `release/0.4.z` already ships quinn-proto 0.11.14 (fixed).
Remediation path: dependency bump (`cargo update`) + downstream propagation.

Stream 2.1.x: upstream branch `release/0.3.z` ships quinn-proto 0.11.9 (still vulnerable).
Remediation path: upstream backport + downstream propagation.

## Summary

- **Stream 2.1.x**: ALL versions affected (2.1.0, 2.1.1). Upstream fix NOT available on release/0.3.z.
- **Stream 2.2.x**: Versions 2.2.0, 2.2.1, 2.2.2 affected. Versions 2.2.3+ ship the fix. Upstream fix IS available on release/0.4.z.
