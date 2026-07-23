# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

Fix threshold: quinn-proto >= 0.11.14 (from CVE description and advisory data).

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Ecosystem: Cargo
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
  Lock file: Cargo.lock

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml / Cargo.lock
```

## Stream Impact Summary

### Stream 2.2.x (issue scope)

- **Affected versions**: 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- quinn-proto was updated to 0.11.14 starting from build v0.4.11 (version 2.2.3)

### Stream 2.1.x (cross-stream)

- **Affected versions**: 2.1.0, 2.1.1
- All versions in this stream ship quinn-proto 0.11.9, which is vulnerable

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Source Repo | Notes |
|--------|-----------|-----------------|-------------|-------|
| 2.2.x | Cargo | release/0.4.z | backend | Fix present in v0.4.11+ (quinn-proto 0.11.14) |
| 2.1.x | Cargo | release/0.3.z | backend | Fix NOT present in latest tag (v0.3.12 ships 0.11.9) |

- **2.2.x stream**: The upstream fix is already available in later builds (v0.4.11+).
  Remediation for affected versions (2.2.0-2.2.2) would require a downstream update
  to reference a build tag that includes quinn-proto >= 0.11.14.
- **2.1.x stream**: The upstream branch `release/0.3.z` does not yet include the fix.
  Remediation requires an upstream backport to bump quinn-proto on that branch first.

## Affects Versions Correction Preview

Current PSIRT-assigned Affects Versions: `RHTPA 2.0.0`

This is incorrect -- RHTPA 2.0.0 does not correspond to any configured version stream.
Based on lock file evidence and the issue's stream scope (2.2.x), the corrected
Affects Versions should be:

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

(Only 2.2.x versions are included because the issue is scoped to stream 2.2.x via
the `[rhtpa-2.2]` suffix. The 2.1.x versions are tracked separately via cross-stream
impact in Case B.)
