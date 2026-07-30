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

## Summary by Stream

| Stream | Affected Versions | Unaffected Versions |
|--------|-------------------|---------------------|
| 2.1.x | 2.1.0, 2.1.1 | (none) |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 |

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Lock File | Notes |
|--------|-----------|-----------------|-----------|-------|
| 2.1.x | Cargo | release/0.3.z | Cargo.lock | Upstream branch fix status unknown -- must check `git show release/0.3.z:Cargo.lock` |
| 2.2.x | Cargo | release/0.4.z | Cargo.lock | Fix already present in v0.4.11+ (quinn-proto 0.11.14) |

## Affects Versions Correction (Step 3)

Issue is scoped to stream **2.2.x**.

- **Current Affects Versions (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

PSIRT assigned RHTPA 2.0.0 which does not correspond to any supported version in the supportability matrix. The corrected Affects Versions include only the 2.2.x stream versions that ship quinn-proto < 0.11.14 (versions 2.2.0, 2.2.1, and 2.2.2 which is a retag of 2.2.1).

Note: Versions 2.2.3 and 2.2.4 are NOT affected -- they ship quinn-proto 0.11.14 (the fixed version).

## Cross-Stream Impact (Case A)

The 2.1.x stream is also affected (2.1.0 and 2.1.1 both ship quinn-proto 0.11.9), but this issue is scoped to 2.2.x only. Cross-stream impact is reported via comment on TC-8001 and preemptive remediation tasks are created for the 2.1.x stream if no companion CVE Jira exists.
