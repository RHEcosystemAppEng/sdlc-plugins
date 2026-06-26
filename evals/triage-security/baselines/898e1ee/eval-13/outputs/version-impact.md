# Step 2 -- Version Impact Analysis: TC-8001

## Vulnerability Parameters

- **Library**: quinn-proto
- **Affected range**: < 0.11.14
- **Fixed version**: 0.11.14
- **Ecosystem**: Cargo (lock file: `Cargo.lock`)

## Version Impact Table -- Stream 2.2.x (issue scope)

| Product Version | Build Tag | Build Date | quinn-proto Version | Affected? | Evidence |
|-----------------|-----------|------------|---------------------|-----------|----------|
| 2.2.0 | v0.4.5 | 2025-12-03 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 2026-02-05 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.8 (retag) | 2026-02-23 | 0.11.12 | YES | same as 2.2.1 (retag of v0.4.8) |
| 2.2.3 | v0.4.11 | 2026-03-23 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 2026-05-04 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

**Scoped conclusion**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14). The fix was first picked up in build v0.4.11 (2.2.3, released 2026-03-23).

## Version Impact Table -- Stream 2.1.x (cross-stream check)

| Product Version | Build Tag | Build Date | quinn-proto Version | Affected? | Evidence |
|-----------------|-----------|------------|---------------------|-----------|----------|
| 2.1.0 | v0.3.8 | 2025-09-15 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 2025-11-20 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

**Cross-stream conclusion**: All versions in stream 2.1.x are affected. No version in this stream ships the fixed quinn-proto version. This triggers Case B (cross-stream impact notice).

## Affects Versions Correction (Step 3)

The current Affects Versions field ("RHTPA 2.0.0") is incorrect:
- There is no 2.0.x stream in the configuration.
- Based on lock file evidence, the affected versions within the 2.2.x scope are: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
- Versions 2.2.3 and 2.2.4 are NOT affected (already fixed).

Proposed correction: Remove "RHTPA 2.0.0", add "RHTPA 2.2.0", "RHTPA 2.2.1", "RHTPA 2.2.2".

## Upstream Fix Status (Step 2.5)

The upstream fix PR (quinn-rs/quinn#2048) introduced the fix in quinn-proto 0.11.14. The fix is already present in build tags v0.4.11+ (stream 2.2.x) but NOT in any 2.1.x build tags. The upstream branch for 2.2.x remediation is `release/0.4.z`; for 2.1.x it would be `release/0.3.z`.

## Remediation Determination

- **Case A applies**: Versions 2.2.0, 2.2.1, 2.2.2 in the scoped stream (2.2.x) are affected. However, since 2.2.3+ already ship the fix, the remediation for stream 2.2.x is already resolved in the latest builds. The Affects Versions correction documents the historical exposure.
- **Case B applies**: Cross-stream impact -- stream 2.1.x (all versions) is also affected. The 2.1.x stream has no version shipping the fix (all at quinn-proto 0.11.9). A cross-stream notice and potentially preemptive remediation tasks should be created for stream 2.1.x.
