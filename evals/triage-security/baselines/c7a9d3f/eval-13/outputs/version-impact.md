# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions | Status |
|--------|-------------------|---------------------|--------|
| 2.1.x | 2.1.0, 2.1.1 | (none) | ALL versions affected |
| 2.2.x (scoped) | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 | Partially affected -- fixed starting from build v0.4.11 |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest build tag) | Fixed? |
|--------|-----------|-----------------|-------------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |

The upstream fix has already landed on `release/0.4.z` (2.2.x stream) as of build v0.4.11, but `release/0.3.z` (2.1.x stream) still carries the vulnerable version 0.11.9.

## Cross-Stream Impact

This issue is scoped to stream **2.2.x** (from the `[rhtpa-2.2]` suffix). However, stream **2.1.x** is also affected -- all versions (2.1.0, 2.1.1) ship quinn-proto 0.11.9 which is within the vulnerable range. This triggers **Case B** (cross-stream impact).

## Affects Versions Correction

The PSIRT-assigned Affects Versions of "RHTPA 2.0.0" is incorrect:
- There is no 2.0.x stream configured
- Within the scoped 2.2.x stream, the affected versions are: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- The Affects Versions field should be corrected to: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected (they ship quinn-proto 0.11.14)
