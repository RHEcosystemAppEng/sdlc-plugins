# Step 2 - Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix threshold**: quinn-proto >= 0.11.14

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend

  quinn-proto is a QUIC protocol implementation crate.
  The vulnerability allows remote DoS via excessive stream counts in QUIC transport frames.

  Present in: all versions across both streams (2.1.x and 2.2.x)
  Fixed starting from: 2.2.3 (build v0.4.11, quinn-proto bumped to 0.11.14)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.12) | YES |

- **2.2.x stream**: Fixed upstream. The fix was introduced in build v0.4.11 (version 2.2.3). Remediation for versions 2.2.0-2.2.2 is a Konflux release repo change to update the backend source tag to pick up the already-available fix.
- **2.1.x stream**: NOT fixed upstream. The release/0.3.z branch still ships quinn-proto 0.11.9. Remediation requires an upstream PR to bump the dependency on the release/0.3.z branch first, then a Konflux release repo update.
