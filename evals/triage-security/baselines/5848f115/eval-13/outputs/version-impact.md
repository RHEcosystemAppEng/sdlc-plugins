# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (quinn-proto found directly in Cargo.lock)
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Fix Source |
|--------|-----------|-----------------|-----------|
| 2.1.x | Cargo | release/0.3.z | Upstream fix PR: [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| 2.2.x | Cargo | release/0.4.z | Already fixed at branch HEAD (v0.4.11+ ships 0.11.14) |

- Stream 2.2.x: The upstream branch `release/0.4.z` already contains the fix at v0.4.11 (quinn-proto 0.11.14). Remediation for 2.2.0, 2.2.1, and 2.2.2 requires updating the backend source reference in the Konflux release repo to pick up a tag at or after v0.4.11.
- Stream 2.1.x: The upstream branch `release/0.3.z` ships quinn-proto 0.11.9 at its latest tag (v0.3.12). Remediation requires an upstream backport to bump quinn-proto on the release/0.3.z branch.

## Affects Versions Correction (Step 3)

**Current Affects Versions (PSIRT-assigned):** RHTPA 2.0.0

**Problem:** RHTPA 2.0.0 does not correspond to any configured version stream. There is no 2.0.x stream in the Version Streams table.

**Proposed Affects Versions (scoped to 2.2.x stream):** RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Correction: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Based on lock file analysis at pinned commits from security-matrix.md. Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`. Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14, which is at or above the fix threshold.

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but the version impact analysis reveals that stream **2.1.x** is also affected:

- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

Cross-stream impact comment (would be posted to TC-8001):
> Cross-stream impact: quinn-proto versions before 0.11.14 also affects stream 2.1.x based on lock file analysis. This stream is tracked by a companion issue (see Related links) or may require separate PSIRT triage.

Preemptive remediation tasks should be created for stream 2.1.x if no existing CVE Jira covers that stream (see remediation.md).
