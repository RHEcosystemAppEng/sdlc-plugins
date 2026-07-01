# Step 2 -- Version Impact Analysis: CVE-2026-48901 (h2 < 0.4.8)

## Enriched Fix Threshold

Using enriched fix threshold from Step 1.5: **h2 < 0.4.8** (MITRE and OSV.dev agree).

Versions shipping h2 < 0.4.8 are **affected**. Versions shipping h2 >= 0.4.8 are **not affected**.

## Issue Stream Scope

This issue is stream-scoped to **2.2.x** (from summary suffix `[rhtpa-2.2]`). The version impact table covers the scoped stream (2.2.x) and includes cross-stream analysis of 2.1.x for Case B evaluation.

## Version Impact Table -- Stream 2.2.x (scoped)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.2.1 | v0.4.8 | 0.4.8 | NO | 0.4.8 >= 0.4.8 (at fix threshold) |
| 2.2.2 | v0.4.8 | -- | NO | retag of 2.2.1 (same source commits) |
| 2.2.3 | v0.4.11 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |
| 2.2.4 | v0.4.12 | 0.4.9 | NO | 0.4.9 >= 0.4.8 |

**Summary (2.2.x)**: 1 of 5 versions affected (2.2.0 only). Versions 2.2.1+ ship h2 >= 0.4.8 and are not affected.

## Version Impact Table -- Stream 2.1.x (cross-stream)

| Version | Build Tag | h2 version | Affected? | Notes |
|---------|-----------|------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.4.5 | YES | 0.4.5 < 0.4.8 |
| 2.1.1 | v0.3.12 | 0.4.5 | YES | 0.4.5 < 0.4.8 |

**Summary (2.1.x)**: All 2 versions affected. Both ship h2 0.4.5 which is below the fix threshold.

## Dependency Chain Context (Step 2.3.5)

Ecosystem: Cargo (source dependency)

The h2 crate is a Rust HTTP/2 implementation. In a typical Rust backend service, the dependency chain is:

```
rhtpa-backend (workspace) -> hyper / reqwest -> h2
Profile: production (h2 is a runtime dependency for HTTP/2 support)
```

h2 is present across all versions in both streams, indicating it was introduced early as a core HTTP/2 dependency.

## Cross-Stream Impact Summary

| Stream | Versions Affected | Versions Not Affected | Status |
|--------|-------------------|-----------------------|--------|
| 2.2.x (scoped) | 2.2.0 | 2.2.1, 2.2.2, 2.2.3, 2.2.4 | Partially affected |
| 2.1.x (cross-stream) | 2.1.0, 2.1.1 | -- | Fully affected |

Cross-stream impact detected: stream 2.1.x is also affected and falls under Case B handling in Step 8.
