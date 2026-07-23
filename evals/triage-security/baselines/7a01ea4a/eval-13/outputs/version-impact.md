# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Stream Scope Summary

- **Issue scoped to stream 2.2.x** (per summary suffix `[rhtpa-2.2]`)
- Affected versions within scope (2.2.x): **2.2.0, 2.2.1, 2.2.2**
- Not affected within scope (2.2.x): 2.2.3, 2.2.4
- Cross-stream impact: **2.1.x** (2.1.0, 2.1.1) is also affected but outside this issue's scope

## Affects Versions Correction (Step 3)

- Current Affects Versions: `RHTPA 2.0.0` (incorrect -- no 2.0.x stream exists)
- Proposed Affects Versions (scoped to 2.2.x): `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`
- Correction: `[RHTPA 2.0.0]` -> `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Repository | Upstream Branch | Lock File | Fix Status |
|--------|-----------|------------|-----------------|-----------|------------|
| 2.1.x | Cargo | backend | release/0.3.z | Cargo.lock | Would check at branch HEAD |
| 2.2.x | Cargo | backend | release/0.4.z | Cargo.lock | Would check at branch HEAD |

Based on the supportability matrix data, the fix (quinn-proto 0.11.14) was picked up starting at build tag v0.4.11 (version 2.2.3). Versions 2.2.0 through 2.2.2 ship vulnerable versions (0.11.9 and 0.11.12). All 2.1.x versions ship 0.11.9 which is also vulnerable.
