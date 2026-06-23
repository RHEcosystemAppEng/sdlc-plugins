# Step 2 -- Version Impact Analysis

## Cross-Stream Version Impact Table

The version impact analysis covers ALL configured Version Streams (2.1.x and 2.2.x), not just the issue's scoped stream (2.2.x). This enables cross-stream impact detection in Step 7 Case B.

| Version | Stream | Build Tag | tokio version | Affected? | Notes |
|---------|--------|-----------|---------------|-----------|-------|
| RHTPA 2.1.0 | rhtpa-2.1 (2.1.x) | `v0.3.8` | 1.40.0 | **YES** | < 1.42.0 fix threshold |
| RHTPA 2.1.1 | rhtpa-2.1 (2.1.x) | `v0.3.12` | 1.40.0 | **YES** | < 1.42.0 fix threshold |
| RHTPA 2.2.0 | rhtpa-2.2 (2.2.x) | `v0.4.5` | 1.41.1 | **YES** | < 1.42.0 fix threshold |
| RHTPA 2.2.1 | rhtpa-2.2 (2.2.x) | `v0.4.8` | 1.41.1 | **YES** | < 1.42.0 fix threshold |

## Impact Summary

- **Issue stream (rhtpa-2.2)**: Both versions (RHTPA 2.2.0, RHTPA 2.2.1) are affected. tokio 1.41.1 is below the fix threshold of 1.42.0.
- **Other stream (rhtpa-2.1)**: Both versions (RHTPA 2.1.0, RHTPA 2.1.1) are also affected. tokio 1.40.0 is below the fix threshold of 1.42.0.

## Cross-Stream Impact Detection

Stream rhtpa-2.1 is **outside** this issue's scope (TC-8020 is scoped to rhtpa-2.2) but is also affected by CVE-2026-55123. This triggers **Step 7 Case B** (cross-stream impact / proactive remediation).

## Ecosystem Details

- **Ecosystem**: Cargo (source dependency)
- **Source repository**: rhtpa-backend (backend)
- **Upstream branch for 2.1.x**: `release/0.3.z`
- **Upstream branch for 2.2.x**: `release/0.4.z`
- **Konflux release repo for 2.1.x**: `rhtpa-release.0.3.z`
- **Konflux release repo for 2.2.x**: `rhtpa-release.0.4.z`
- **Source pinning method (2.1.x)**: `artifacts.lock.yaml` (download URL contains tag)
- **Source pinning method (2.2.x)**: `artifacts.lock.yaml` (download URL contains tag)
