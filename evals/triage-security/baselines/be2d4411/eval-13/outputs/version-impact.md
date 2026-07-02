# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.3.12 | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.4.5 | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.4.8 | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.4.9 | `v0.4.8` | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.4.11 | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.4.12 | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Stream Impact Summary

| Stream | Affected Versions | Unaffected Versions |
|--------|-------------------|---------------------|
| 2.1.x | 2.1.0, 2.1.1 | -- |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (would check via `git -C /home/dev/repos/rhtpa-backend show release/0.3.z:Cargo.lock`) | TBD |
| 2.2.x | Cargo | release/0.4.z | (would check via `git -C /home/dev/repos/rhtpa-backend show release/0.4.z:Cargo.lock`) | TBD |

Note: Since the eval prohibits actual git commands, upstream fix status cannot be determined from mock data. In a real triage, `git show` would be run against each upstream branch HEAD.

## Affects Versions Correction (Step 3)

The issue is scoped to stream **2.2.x** (per `[rhtpa-2.2]` suffix). Only 2.2.x versions are included in the Affects Versions correction.

- **Current**: RHTPA 2.0.0 (incorrect -- RHTPA 2.0.0 does not exist in any configured stream)
- **Proposed**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, which is the fixed version) and are excluded.

## Cross-Stream Impact (Case B)

Stream **2.1.x** is also affected (all versions ship quinn-proto 0.11.9 < 0.11.14). This issue is scoped to 2.2.x, so 2.1.x impact triggers Case B (cross-stream proactive remediation). Preemptive remediation tasks would be created for the 2.1.x stream if no sibling CVE Jira exists for that stream.
