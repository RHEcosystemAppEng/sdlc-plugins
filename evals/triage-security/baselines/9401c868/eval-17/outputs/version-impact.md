# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Stream-Scoped Summary (issue scoped to 2.2.x)

Within the issue's stream (2.2.x):
- **Affected**: 2.2.0, 2.2.1, 2.2.2 (quinn-proto 0.11.9 -- 0.11.12, all < 0.11.14)
- **Not affected**: 2.2.3, 2.2.4 (quinn-proto 0.11.14, at or above fix threshold)

## Cross-Stream Impact (outside issue scope)

Stream 2.1.x is also affected:
- **Affected**: 2.1.0, 2.1.1 (both ship quinn-proto 0.11.9, below fix threshold 0.11.14)

This triggers **Case A** (cross-stream impact) in Step 8 -- proactive remediation for the 2.1.x stream.

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|---------------------|--------|
| 2.1.x | Cargo | release/0.3.z | v0.3.12: 0.11.9 | NO |
| 2.2.x | Cargo | release/0.4.z | v0.4.12: 0.11.14 | YES |

- **2.2.x**: Fix is already available upstream (v0.4.11+ ships quinn-proto 0.11.14). Remediation uses the **dependency bump** variant (`cargo update -p quinn-proto`) rather than a full upstream backport.
- **2.1.x**: Fix is **not** available upstream on release/0.3.z (latest v0.3.12 still ships 0.11.9). Remediation requires an **upstream backport** to bump quinn-proto on the release/0.3.z branch.

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo ecosystem)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
  Lock file: Cargo.lock

Remediation: bump quinn-proto to >= 0.11.14
```

## Affects Versions Correction (Step 3)

Current (PSIRT-assigned): `RHTPA 2.0.0` (incorrect -- no 2.0.x stream exists)

Proposed (scoped to 2.2.x stream per issue suffix `[rhtpa-2.2]`):
- `RHTPA 2.2.0`
- `RHTPA 2.2.1`
- `RHTPA 2.2.2`

Correction: `Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Note: Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed quinn-proto 0.11.14. The 2.1.x versions are excluded from this issue's Affects Versions because the issue is scoped to stream 2.2.x -- the 2.1.x stream is tracked by its own companion CVE Jira (or preemptive tasks if none exists).
