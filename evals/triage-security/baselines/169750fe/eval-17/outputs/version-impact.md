# Step 2 -- Version Impact Analysis

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8: 0.11.12) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

## Summary

- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix threshold**: quinn-proto >= 0.11.14

The fix was introduced in build tag v0.4.11 (product version 2.2.3). All versions before that ship quinn-proto versions within the affected range (< 0.11.14).

## Stream Impact Summary

| Stream | Versions Affected | Versions Not Affected |
|--------|-------------------|-----------------------|
| 2.1.x | 2.1.0, 2.1.1 (all versions) | -- |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Retag Handling

- **2.2.2** (build v0.4.9) is a retag of 2.2.1 (build v0.4.8). The lock file check was skipped and the result carried forward from 2.2.1: quinn-proto 0.11.12 (affected).

## Affects Versions Correction

The PSIRT-assigned Affects Versions field currently contains **RHTPA 2.0.0**, which does not match any configured version stream. Based on lock file evidence:

- The issue is scoped to stream **2.2.x** (from the `[rhtpa-2.2]` suffix).
- Within stream 2.2.x, the affected versions are: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
- Versions 2.2.3 and 2.2.4 ship the fixed version and should NOT be in Affects Versions.

The Affects Versions field should be corrected to: **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2** (removing RHTPA 2.0.0 which is not a valid version).

## Cross-Stream Impact (Case A)

Since this is a stream-scoped issue (scoped to 2.2.x), and the 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9), the cross-stream impact comment would note:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. All 2.1.x versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9, which is within the affected range.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | -- | Unknown (not in mock data for branch HEAD) |
| 2.2.x | Cargo | release/0.4.z | -- | Unknown (not in mock data for branch HEAD) |

Note: The mock data provides quinn-proto versions at specific build tags only. For upstream fix status at branch HEAD, the actual `git show` commands on the upstream branches would be needed. However, since build v0.4.11 and v0.4.12 already ship quinn-proto 0.11.14 (the fixed version), it is likely that the upstream branch `release/0.4.z` has the fix at HEAD.
