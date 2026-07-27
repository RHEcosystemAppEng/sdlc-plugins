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
  Ecosystem: Cargo
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at Tag | Fixed? |
|--------|-----------|-----------------|----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |

The upstream fix is already present on the `release/0.4.z` branch (since build tag v0.4.11). Remediation for stream 2.2.x is a downstream propagation to update the source reference in the Konflux release repo to pick up the fix from a tag at or after v0.4.11.

Stream 2.1.x (`release/0.3.z`) has NOT been fixed upstream -- quinn-proto remains at 0.11.9 on that branch.

## Summary

- **Stream 2.2.x (issue scope)**: versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix.
- **Stream 2.1.x (cross-stream)**: versions 2.1.0 and 2.1.1 are affected. This stream is outside the issue's scope but will be flagged as cross-stream impact (Case A).
