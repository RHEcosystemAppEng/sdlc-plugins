# Step 2 -- Version Impact Analysis

## Enriched Fix Threshold

Using the cross-validated fix threshold from Step 1.5: **h2 < 0.4.8** (affected), **>= 0.4.8** (not affected).

## Version Impact Table

Version Impact for CVE-2026-48901 (h2 < 0.4.8):

| Stream | Version | Build Tag | h2 version | Affected? | Notes |
|--------|---------|-----------|------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.x | 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as 2.2.1) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.x | 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

## Stream Impact Summary

| Stream | Versions Affected | Versions Not Affected | Stream Affected? |
|--------|-------------------|-----------------------|------------------|
| 2.1.x | 2.1.0, 2.1.1 | -- | YES |
| 2.2.x | -- | 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4 | NO |

## Dependency Chain Context

The h2 crate is a Cargo (Rust) dependency in the backend repository. Based on the ecosystem mappings:

- Ecosystem: Cargo
- Repository: backend
- Lock file: Cargo.lock
- Upstream branch (2.1.x): release/0.3.z
- Upstream branch (2.2.x): release/0.4.z

h2 is a source-level Cargo dependency. In stream 2.1.x, it ships version 0.4.5 which is within the affected range (< 0.4.8). In stream 2.2.x, even the earliest version (2.2.0) ships h2 0.4.8, which is at the fix threshold and therefore not affected.

## Scoped Stream Analysis (2.2.x)

This issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).

**Result: No 2.2.x versions are affected.** All five versions in the 2.2.x stream ship h2 >= 0.4.8, which meets or exceeds the fix threshold.

## Cross-Stream Impact (2.1.x)

Stream 2.1.x is **outside** this issue's scope but IS affected:

- 2.1.0 ships h2 0.4.5 (affected)
- 2.1.1 ships h2 0.4.5 (affected)

This cross-stream impact is relevant for Case A analysis in Step 8.

## Upstream Fix Status

Based on the mock lock file data, the latest versions in both streams already ship h2 >= 0.4.8:

| Stream | Ecosystem | Upstream Branch | Latest Tag | h2 at Latest | Fixed? |
|--------|-----------|-----------------|------------|--------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12 | 0.4.5 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12 | 0.4.9 | YES |

- Stream 2.2.x: upstream already ships the fix (h2 0.4.9 >= 0.4.8)
- Stream 2.1.x: upstream does NOT ship the fix (h2 0.4.5 < 0.4.8) -- upstream backport required
