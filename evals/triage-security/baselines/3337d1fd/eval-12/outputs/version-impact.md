# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5:
- **Library**: h2
- **Affected range**: < 0.4.8
- **Fix threshold**: >= 0.4.8

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Build Tag | h2 version | Affected? | Notes |
|--------|---------|-----------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 |

## Impact Summary

### In-scope stream (2.2.x)

**No versions affected.** All 2.2.x versions ship h2 >= 0.4.8, which meets or exceeds the fix threshold. The earliest 2.2.x version (2.2.0, build v0.4.5) already ships h2 0.4.8, the exact fix version.

### Out-of-scope stream (2.1.x)

**All versions affected.** Both 2.1.x versions (2.1.0 and 2.1.1) ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Dependency Chain Context

Dependency chain for h2 (Cargo):
- Ecosystem: Cargo (crates.io)
- Library: h2
- Type: source dependency (Rust crate)
- Lock file: Cargo.lock
- Repository: backend (rhtpa-backend)

The h2 crate is an HTTP/2 implementation used as a dependency in the backend service. Remediation requires bumping h2 to >= 0.4.8 in Cargo.lock via the upstream source repository.

## Cross-Stream Impact

This issue is scoped to stream 2.2.x via the `[rhtpa-2.2]` suffix, but the version impact analysis reveals:

- **2.2.x (in-scope)**: NOT affected -- all versions ship h2 >= 0.4.8
- **2.1.x (out-of-scope)**: AFFECTED -- all versions ship h2 0.4.5 (< 0.4.8)

This triggers Case B (cross-stream impact) and Case C (no in-scope versions affected) in Step 8.
