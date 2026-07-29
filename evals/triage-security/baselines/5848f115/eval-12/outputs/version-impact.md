# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 **< 0.4.8** is vulnerable. Versions >= 0.4.8
are not affected (0.4.8 is the fix version per both MITRE CVE API and OSV.dev).

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

### Stream 2.1.x (out of scope -- included for cross-stream analysis)

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0 | 0.3.8 | `v0.3.8` | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | 0.3.12 | `v0.3.12` | 0.4.5 | YES | 0.4.5 < 0.4.8 |

### Stream 2.2.x (in scope -- issue suffix [rhtpa-2.2])

| Version | Build | Backend Tag | h2 version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0 | 0.4.5 | `v0.4.5` | 0.4.8 | NO | 0.4.8 >= 0.4.8 (ships fix version) |
| 2.2.1 | 0.4.8 | `v0.4.8` | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.2 | 0.4.9 | `v0.4.8` | 0.4.8 | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | `v0.4.11` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | 0.4.12 | `v0.4.12` | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Summary

- **In-scope stream (2.2.x)**: 0 of 5 versions affected. All versions in the
  2.2.x stream ship h2 >= 0.4.8 (the fix version). The earliest 2.2.x release
  (2.2.0) already ships h2 0.4.8.
- **Out-of-scope stream (2.1.x)**: 2 of 2 versions affected. Both versions in
  the 2.1.x stream ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

```
Dependency chain for h2:
  backend (workspace) -> h2
  Type: source dependency (Cargo ecosystem)
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock
  Profile: production (h2 is a runtime HTTP/2 dependency)

  Stream 2.1.x: h2 0.4.5 at both versions (v0.3.8, v0.3.12)
  Stream 2.2.x: h2 0.4.8+ at all versions (already fixed)
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | h2 version at tag | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.4.5 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.4.8+ (at v0.4.5+) | YES |

The 2.1.x upstream branch (`release/0.3.z`) still ships h2 0.4.5, which is
vulnerable. The 2.2.x upstream branch (`release/0.4.z`) ships h2 >= 0.4.8,
which includes the fix.

## Cross-Stream Impact

This issue is scoped to stream **2.2.x**, which is **not affected** (all
versions ship h2 >= 0.4.8). However, stream **2.1.x** is affected (both
versions ship h2 0.4.5 < 0.4.8).

This triggers **Case A** (cross-stream impact) and **Case C** (no in-scope
versions affected) for the scoped stream.
