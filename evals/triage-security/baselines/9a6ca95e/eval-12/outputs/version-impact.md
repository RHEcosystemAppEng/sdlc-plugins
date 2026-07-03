# Step 2 -- Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

## Enriched Fix Threshold

From Step 1.5 cross-validation: h2 versions **< 0.4.8** are affected. The fix threshold is **0.4.8** (confirmed by both MITRE CVE API and OSV.dev).

## Version Impact Table

### Stream 2.2.x (scoped stream -- issue TC-8030 is scoped to [rhtpa-2.2])

| Version | Build | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.2.0   | 0.4.5 | v0.4.5      | 0.4.5      | **YES**   | 0.4.5 < 0.4.8 |
| 2.2.1   | 0.4.8 | v0.4.8      | 0.4.8      | NO        | ships fix version (0.4.8 >= 0.4.8) |
| 2.2.2   | 0.4.9 | v0.4.9      | --         | NO        | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3   | 0.4.11| v0.4.11     | 0.4.9      | NO        | 0.4.9 >= 0.4.8 |
| 2.2.4   | 0.4.12| v0.4.12     | 0.4.9      | NO        | 0.4.9 >= 0.4.8 |

**Scoped stream summary**: Only version **2.2.0** is affected. The fix was picked up in **2.2.1** (h2 bumped from 0.4.5 to 0.4.8). All subsequent versions (2.2.2--2.2.4) ship h2 >= 0.4.8 and are not affected.

### Stream 2.1.x (cross-stream impact)

| Version | Build | Backend Tag | h2 Version | Affected? | Notes |
|---------|-------|-------------|------------|-----------|-------|
| 2.1.0   | 0.3.8 | v0.3.8      | 0.4.5      | **YES**   | 0.4.5 < 0.4.8 |
| 2.1.1   | 0.3.12| v0.3.12     | 0.4.5      | **YES**   | 0.4.5 < 0.4.8 |

**Cross-stream summary**: **All** 2.1.x versions ship h2 0.4.5, which is vulnerable. No version in the 2.1.x stream includes the fix.

## Dependency Chain Context

```
Dependency chain for h2 (Cargo):
  backend (workspace) -> h2 (HTTP/2 protocol implementation)
  Ecosystem: Cargo (crates.io)
  Lock file: Cargo.lock

  Stream 2.2.x:
    - 2.2.0 (v0.4.5): h2 0.4.5 -- VULNERABLE
    - 2.2.1+ (v0.4.8+): h2 0.4.8+ -- FIXED (dependency bumped in this build)

  Stream 2.1.x:
    - All versions (v0.3.8, v0.3.12): h2 0.4.5 -- VULNERABLE
    - No fix available in this stream
```

## Cross-Stream Impact Summary

| Stream | Versions Affected | Latest Version Fixed? | Remediation Needed? |
|--------|-------------------|----------------------|---------------------|
| 2.2.x (scoped) | 2.2.0 only | Yes (2.2.1+) | No -- fix already shipped in 2.2.1 |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 (all) | No | Yes -- upstream backport + downstream propagation required |
