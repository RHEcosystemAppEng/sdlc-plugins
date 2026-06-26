# Step 2 -- Version Impact Analysis: CVE-2026-48901 (h2)

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 < 0.4.8** is affected. Versions >= 0.4.8 are not affected.

## Issue Stream Scope

This issue is scoped to the **2.2.x** stream (from summary suffix `[rhtpa-2.2]`). The primary version impact table covers the 2.2.x stream. The 2.1.x stream is included for cross-stream impact analysis.

## Version Impact Table -- Scoped Stream (2.2.x)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | h2 0.4.8 >= 0.4.8 (fix threshold) |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1, same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (fix threshold) |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | h2 0.4.9 >= 0.4.8 (fix threshold) |

**Result**: No versions in the 2.2.x stream are affected. All versions ship h2 >= 0.4.8.

## Version Impact Table -- Cross-Stream (2.1.x)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | h2 0.4.5 < 0.4.8 (fix threshold) |

**Result**: All versions in the 2.1.x stream are affected. Both versions ship h2 0.4.5, which is below the fix threshold of 0.4.8.

## Summary

- **Scoped stream (2.2.x)**: NOT affected -- all versions ship h2 >= 0.4.8
- **Cross-stream (2.1.x)**: AFFECTED -- all versions ship h2 0.4.5 (< 0.4.8)

Since no versions in the scoped 2.2.x stream are affected, this issue qualifies for **Case C** (close as Not a Bug) for the 2.2.x stream. However, cross-stream impact exists in the 2.1.x stream, which should be noted in the triage (Case B cross-stream impact comment).

## Dependency Chain Context

h2 is a Cargo (Rust) dependency. In the 2.1.x stream where it is affected:
- The vulnerable h2 crate (version 0.4.5) is present in the `Cargo.lock` at the pinned source commits (v0.3.8 and v0.3.12).
- Ecosystem: Cargo (source dependency)
- Lock file: `Cargo.lock`
- Upstream branch for 2.1.x: `release/0.3.z`
