# Step 2 -- Version Impact Analysis: CVE-2026-31812 (quinn-proto < 0.11.14)

## Version Impact Table

All supported version streams are analyzed, even though the issue is scoped to 2.2.x, to detect cross-stream impact.

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue-scoped stream

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

## Combined Version Impact Table

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> [dependency chain through QUIC stack] -> quinn -> quinn-proto
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

  Present in: all versions across both streams (0.11.9 in 2.1.x, 0.11.9-0.11.14 in 2.2.x)
  Fixed starting from: 2.2.3 (build v0.4.11, quinn-proto 0.11.14)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

- **Stream 2.2.x**: Fix is already on `release/0.4.z` -- versions 2.2.3+ ship quinn-proto 0.11.14. Remediation is a downstream propagation to ensure the Konflux release repo reference reflects the fix.
- **Stream 2.1.x**: Fix is NOT on `release/0.3.z` -- all versions still ship quinn-proto 0.11.9. Remediation requires an upstream PR first to bump the dependency on `release/0.3.z`, then a downstream propagation.

## Cross-Stream Impact Summary

- **Scoped stream (2.2.x)**: Versions 2.2.0, 2.2.1, 2.2.2 are affected. Versions 2.2.3, 2.2.4 are already fixed. This is **Case A** (affected, create remediation tasks).
- **Other stream (2.1.x)**: All versions (2.1.0, 2.1.1) are affected. This triggers **Case B** (cross-stream impact, create preemptive remediation tasks for 2.1.x if no CVE Jira exists for that stream).

## Affects Versions Correction (Step 3)

Current Affects Versions: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)

Corrected Affects Versions for the scoped 2.2.x stream: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Action: Remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
