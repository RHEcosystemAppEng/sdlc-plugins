# Step 2 -- Version Impact Analysis: CVE-2026-31812

## Matrix Staleness Check

- Matrix Last-Updated: 2026-06-28T10:00:00Z
- Current date: 2026-10-07
- Age: 101 days (exceeds 14-day threshold)
- Status: **STALE** -- would warn user and ask whether to refresh, proceed, or stop
- Assumed action: proceed anyway (eval mode)

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | 0.11.14 | NO | |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency for QUIC transport)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

## Stream-Scoped Summary

This issue is scoped to stream **2.2.x** (from summary suffix `[rhtpa-2.2]`).

**Within scope (2.2.x):** versions 2.2.0, 2.2.1, and 2.2.2 are affected.
Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14).

**Cross-stream impact (2.1.x):** versions 2.1.0 and 2.1.1 are also affected.
This triggers Case A (cross-stream impact -- proactive remediation for 2.1.x).

## Affects Versions Correction (Step 3)

- Current Affects Versions: [RHTPA 2.0.0] (incorrect -- RHTPA 2.0.0 does not exist)
- Proposed Affects Versions (scoped to 2.2.x): [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
- Rationale: Lock file analysis at pinned commits shows quinn-proto < 0.11.14 in versions 2.2.0, 2.2.1, and 2.2.2 only. Versions 2.2.3+ ship the fixed version (0.11.14).
