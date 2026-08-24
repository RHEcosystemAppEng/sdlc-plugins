# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto versions before 0.11.14):

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (present directly in Cargo.lock)
  Profile: production (quinn-proto is a runtime QUIC protocol dependency)
  Ecosystem: Cargo

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (v0.4.12) | Fixed? |
|--------|-----------|-----------------|---------------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |

- **2.2.x stream**: The upstream fix is already present on the `release/0.4.z` branch at the latest tags (v0.4.11+). Versions 2.2.3 and 2.2.4 already ship the fix. Versions 2.2.0, 2.2.1, and 2.2.2 are affected.
- **2.1.x stream**: The upstream `release/0.3.z` branch still ships quinn-proto 0.11.9, which is vulnerable. The fix has NOT been backported to this branch.

## Affects Versions Correction (Step 3)

The issue is scoped to stream 2.2.x. Affected versions within this stream are: 2.2.0, 2.2.1, 2.2.2.

**Current Affects Versions**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
**Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

This correction is scoped to the 2.2.x stream per the issue's `[rhtpa-2.2]` suffix. The 2.1.x stream versions (2.1.0, 2.1.1) are also affected but belong to a separate stream and will be handled via cross-stream impact (Case A).

## Cross-Stream Impact Summary

The issue is scoped to 2.2.x, but the 2.1.x stream is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (vulnerable)
- 2.1.1 ships quinn-proto 0.11.9 (vulnerable)

This triggers Case A: cross-stream impact with proactive remediation for the 2.1.x stream.
