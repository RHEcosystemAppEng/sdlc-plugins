# Step 2 -- Version Impact Analysis for CVE-2026-31812

## Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same source commit v0.4.8) |
| 2.2.3 | 2.2.x | `v0.4.11` | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 0.11.14 | NO | ships fixed version |

## Dependency Chain Context

```
Dependency chain for quinn-proto (Cargo):
  Ecosystem: Cargo (Rust crate)
  Lock file: Cargo.lock
  Repository: backend

  Affected versions ship quinn-proto < 0.11.14 (fix threshold).
  Versions 2.2.3+ (v0.4.11+) ship quinn-proto 0.11.14 -- at or above fix threshold.
```

## Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Source Tag at HEAD | quinn-proto at HEAD | Fixed? |
|--------|-----------|-----------------|--------------------|--------------------|--------|
| 2.2.x | Cargo | `release/0.4.z` | `v0.4.12` | 0.11.14 | YES |
| 2.1.x | Cargo | `release/0.3.z` | `v0.3.12` | 0.11.9 | NO |

The upstream fix has already landed on the `release/0.4.z` branch (stream 2.2.x) as of tag `v0.4.11`. The `release/0.3.z` branch (stream 2.1.x) has NOT been fixed -- it still ships quinn-proto 0.11.9.

## Cross-Stream Impact Summary

- **Stream 2.2.x** (this issue's scope): versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fix.
- **Stream 2.1.x** (outside this issue's scope): ALL versions (2.1.0, 2.1.1) are affected. This stream requires separate remediation -- either via a companion CVE Jira or proactive remediation tasks (Case B).
