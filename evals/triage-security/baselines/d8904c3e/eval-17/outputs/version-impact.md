# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.3.12 | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.4.5 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.4.8 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.4.9 | v0.4.8 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.4.11 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | 0.4.12 | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary by Stream

| Stream | Affected Versions | Unaffected Versions | Stream Affected? |
|--------|-------------------|---------------------|------------------|
| 2.1.x | 2.1.0, 2.1.1 | (none) | YES -- all versions affected |
| 2.2.x | 2.2.0, 2.2.1, 2.2.2 | 2.2.3, 2.2.4 | YES -- partially affected (fixed in 2.2.3+) |

## Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency (Cargo)
  Profile: production (quinn-proto is a runtime QUIC transport dependency)
  Ecosystem: Cargo
  Lock file: Cargo.lock

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.toml
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | quinn-proto at v0.4.11+ | Fixed? |
|--------|-----------|-----------------|-------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | (needs verification at branch HEAD) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11) | YES |

The 2.2.x stream already has the fix in versions 2.2.3+ (backend tag v0.4.11 ships quinn-proto 0.11.14). The upstream branch `release/0.4.z` already includes the fix.

For the 2.1.x stream, the upstream branch `release/0.3.z` needs to be checked at HEAD to determine if the fix has been merged.

## Affects Versions Correction

The Jira issue currently has **Affects Versions: RHTPA 2.0.0**. Based on the version impact analysis:

- RHTPA 2.0.0 is **not** a configured version stream (no 2.0.x stream exists in Security Configuration).
- The issue is scoped to the 2.2.x stream. Affected versions in scope: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
- Correction needed: remove RHTPA 2.0.0, add RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.

## Cross-Stream Impact (Case A)

This issue is scoped to stream 2.2.x, but the 2.1.x stream is also affected (all versions ship quinn-proto 0.11.9). This triggers **Case A: Cross-stream impact** in Step 8.
