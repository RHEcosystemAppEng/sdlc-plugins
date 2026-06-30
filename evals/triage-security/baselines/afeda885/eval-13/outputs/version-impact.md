# Step 2 -- Version Impact Analysis for TC-8001

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

## Dependency Chain Context (Step 2.3.5)

quinn-proto is a Cargo (Rust) source dependency in the `backend` repository. It is shipped as a compiled-in dependency via the Cargo dependency tree. The library handles QUIC transport protocol framing -- it is a production/runtime dependency (not dev-only).

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD (v0.4.12) | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

The upstream branch `release/0.4.z` already carries the fix (quinn-proto 0.11.14 at the latest tag v0.4.12). For the 2.2.x stream, remediation is a Konflux release repo change: the upstream source already has the fix at newer tags.

The upstream branch `release/0.3.z` does NOT carry the fix -- quinn-proto is still at 0.11.9 at tag v0.3.12. For the 2.1.x stream, remediation requires an upstream PR first to bump the dependency on `release/0.3.z`, then a Konflux release repo update.

## Cross-Stream Impact Summary

- **2.2.x stream (in scope)**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix.
- **2.1.x stream (out of scope)**: ALL versions (2.1.0, 2.1.1) are affected. This stream is outside the issue's scope (`[rhtpa-2.2]`) and will be handled via cross-stream impact notice and preemptive remediation tasks (Step 7 Case B).

## Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Versions is `RHTPA 2.0.0`, but no `2.0.x` stream exists in the Version Streams configuration. The issue is scoped to the 2.2.x stream.

Based on the version impact table, the correct Affects Versions (scoped to 2.2.x) are:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

This correction would be applied via `jira.edit_issue(TC-8001, fields={"versions": [{"id": "<id-for-RHTPA-2.2.0>"}, {"id": "<id-for-RHTPA-2.2.1>"}, {"id": "<id-for-RHTPA-2.2.2>"}]})` using dynamically discovered Jira version IDs from Step 3.1.
