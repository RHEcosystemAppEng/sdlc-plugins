# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

CVE-2026-31812: quinn-proto versions before 0.11.14 (fix threshold: >= 0.11.14)

### Stream 2.2.x (issue-scoped stream)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | at fix threshold |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | at fix threshold |

### Stream 2.1.x (cross-stream)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | |

## Summary

- **Stream 2.2.x**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fix threshold) and are NOT affected.
- **Stream 2.1.x**: All versions (2.1.0, 2.1.1) are affected. Both ship quinn-proto 0.11.9 which is below the fix threshold of 0.11.14.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

- **2.2.x**: The upstream branch `release/0.4.z` already has quinn-proto 0.11.14. Remediation is a downstream propagation only -- update the source reference in the Konflux release repo to a commit/tag that includes the fix.
- **2.1.x**: The upstream branch `release/0.3.z` still ships quinn-proto 0.11.9. Remediation requires an upstream backport PR first to bump quinn-proto on the `release/0.3.z` branch, then a downstream propagation.

## Affects Versions Correction (Step 3)

The current Affects Versions field contains **RHTPA 2.0.0**, which does not match any supported version. Based on lock file evidence:

- **Remove**: RHTPA 2.0.0 (no such version stream exists)
- **Add for 2.2.x stream** (issue-scoped): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Note**: RHTPA 2.2.3 and RHTPA 2.2.4 are NOT affected (ship fixed quinn-proto 0.11.14)
- **Cross-stream note**: 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a different stream scope -- handled via Case B cross-stream impact comment
