# Step 2 -- Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 >= 0.4.8** (versions < 0.4.8 are affected).

## Version Impact Table

### Stream 2.2.x (issue scope: [rhtpa-2.2])

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (fixed) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

### Stream 2.1.x (cross-stream check)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

## Impact Summary

- **Stream 2.2.x** (issue scope): Only version **2.2.0** is affected. Versions 2.2.1 through 2.2.4 ship h2 >= 0.4.8 and are NOT affected. The fix was picked up starting with build v0.4.8 (version 2.2.1).
- **Stream 2.1.x** (cross-stream): **All versions** (2.1.0 and 2.1.1) are affected. Both ship h2 0.4.5 which is below the fix threshold.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: direct dependency (h2 found in Cargo.lock)
  Ecosystem: Cargo (crates.io)
  Profile: production (h2 is a runtime HTTP/2 implementation dependency)

Remediation: bump h2 to >= 0.4.8 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Threshold | Status |
|--------|-----------|-----------------|---------------|--------|
| 2.2.x | Cargo | release/0.4.z | h2 >= 0.4.8 | FIXED in stream (2.2.1+) |
| 2.1.x | Cargo | release/0.3.z | h2 >= 0.4.8 | NOT FIXED (latest 2.1.1 ships h2 0.4.5) |

## Affects Versions Correction

PSIRT-assigned Affects Versions: `RHTPA 2.2.0`

Based on lock file evidence, only version 2.2.0 is affected in the 2.2.x stream. The PSIRT assignment is **correct** -- no correction needed for the scoped stream.

Cross-stream note: Stream 2.1.x (versions 2.1.0 and 2.1.1) is also affected but is outside this issue's scope ([rhtpa-2.2]).
