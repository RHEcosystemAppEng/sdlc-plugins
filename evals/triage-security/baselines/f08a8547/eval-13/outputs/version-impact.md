# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

Dependency chain for quinn-proto:
- Ecosystem: Cargo (source dependency)
- Lock file: `Cargo.lock`
- The dependency chain would be determined by inspecting `Cargo.lock` and `Cargo.toml` in the backend repository. Based on the Cargo ecosystem mapping, quinn-proto is a dependency of the backend workspace.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | `release/0.3.z` | (would need git show to confirm) | Unknown |
| 2.2.x | Cargo | `release/0.4.z` | (would need git show to confirm) | Unknown |

Note: Based on the supportability matrix, the latest tags in each stream show:
- 2.1.x latest (`v0.3.12`): quinn-proto 0.11.9 -- still vulnerable
- 2.2.x latest (`v0.4.12`): quinn-proto 0.11.14 -- fixed in latest release

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions field is **RHTPA 2.0.0**, which is incorrect -- no 2.0.x stream exists in the Version Streams configuration.

Since the issue is scoped to the **2.2.x** stream, the corrected Affects Versions should include only 2.2.x versions that are affected:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT included because they ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Impact (Case A)

The issue is scoped to **2.2.x**, but the version impact analysis reveals that the **2.1.x** stream is also affected:
- 2.1.0: quinn-proto 0.11.9 (AFFECTED)
- 2.1.1: quinn-proto 0.11.9 (AFFECTED)

Cross-stream impact comment would be posted:

> Cross-stream impact: quinn-proto < 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by companion issues (see Related links) or may require separate PSIRT triage.
