# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 versions **< 0.4.8** are affected (fix threshold: 0.4.8).

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Scoped Stream: 2.2.x

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fix version) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Cross-Stream: 2.1.x

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

## Summary

- **Scoped stream (2.2.x)**: Only version **2.2.0** is affected. Versions 2.2.1 and later ship h2 >= 0.4.8 and are NOT affected.
- **Cross-stream (2.1.x)**: Both versions **2.1.0** and **2.1.1** are affected (ship h2 0.4.5).

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (h2 is a Cargo dependency)
  Ecosystem: Cargo (crates.io)
  Profile: production (h2 is an HTTP/2 runtime dependency)
```

The h2 crate is a direct dependency of the backend workspace. Remediation is a straightforward version bump in Cargo.toml / Cargo.lock.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.2.x | Cargo | release/0.4.z | >= 0.4.8 | Fixed upstream (2.2.1+ already ship the fix) |
| 2.1.x | Cargo | release/0.3.z | >= 0.4.8 | Needs upstream backport (2.1.x ships h2 0.4.5) |

## Affects Versions Assessment

- **PSIRT-assigned Affects Versions**: RHTPA 2.2.0
- **Lock file evidence**: Only 2.2.0 ships h2 0.4.5 (affected); 2.2.1+ ship h2 >= 0.4.8 (not affected)
- **Assessment**: PSIRT's Affects Versions is **correct** for the 2.2.x scoped stream -- only RHTPA 2.2.0 is affected
