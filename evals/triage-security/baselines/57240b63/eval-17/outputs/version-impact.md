# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Supportability Matrix (Aggregated)

Data loaded from two version streams configured in Security Configuration:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build | Build Date | backend tag | quinn-proto version |
|---------|-------|------------|-------------|---------------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 | 0.11.9 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 | 0.11.9 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build | Build Date | backend tag | quinn-proto version |
|---------|-------|------------|-------------|---------------------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | 0.11.9 |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | 0.11.12 |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | (retag of 2.2.1) |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | 0.11.14 |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | 0.11.14 |

## Version Impact Table

CVE-2026-31812 affects quinn-proto versions before 0.11.14 (fixed in 0.11.14).

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto (Cargo):
  backend (workspace) -> quinn -> quinn-proto
  Ecosystem: Cargo (source dependency)
  Lock file: Cargo.lock
  Profile: production (runtime dependency)

  Present in: all versions across both streams (0.11.9 through 0.11.14)
  Fix threshold: >= 0.11.14
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (not checked -- outside issue scope, but relevant for cross-stream) | TBD |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (based on latest tag v0.4.11+) | YES |

The upstream fix is already present on the `release/0.4.z` branch (versions 2.2.3+ ship quinn-proto 0.11.14). Remediation for the affected 2.2.x versions (2.2.0, 2.2.1, 2.2.2) requires a downstream propagation -- the upstream source already has the fix on later tags.

## Cross-Stream Impact Summary

- **Issue scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are AFFECTED; versions 2.2.3, 2.2.4 are NOT affected
- **2.1.x stream**: versions 2.1.0, 2.1.1 are AFFECTED (cross-stream impact -- Case B in Step 8)

## Affects Versions Correction (Step 3 Preview)

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (scoped to 2.2.x stream)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

RHTPA 2.0.0 does not correspond to any configured version stream. The correct Affects Versions for the 2.2.x-scoped issue are the affected versions within that stream.

Versions 2.2.3 and 2.2.4 are NOT affected (they ship the fixed quinn-proto 0.11.14) and should NOT be included in Affects Versions.

The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a different stream -- they would be tracked by a companion CVE Jira for stream 2.1.x (or via preemptive remediation tasks if no companion exists).
