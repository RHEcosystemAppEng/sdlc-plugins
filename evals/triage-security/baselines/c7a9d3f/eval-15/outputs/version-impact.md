# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

| Version | Stream | Build Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Analysis Summary

- **Fix threshold**: quinn-proto >= 0.11.14 (from Jira description, cross-validated)
- **Affected versions**: 2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2
- **Not affected versions**: 2.2.3, 2.2.4
- **Fix introduced in**: 2.2.3 (build 0.4.11), which first ships quinn-proto 0.11.14

## Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn (QUIC transport) -> quinn-proto
  Ecosystem: Cargo (Cargo.lock)
  Profile: production (runtime dependency)

Present in: all versions across both streams (2.1.x and 2.2.x)
Fix first appears: 2.2.3 (tag v0.4.11)
```

## Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | (unknown -- would need git show) | Unknown |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (inferred from v0.4.11+) | YES |

## Cross-Stream Impact

This issue is scoped to stream **2.2.x** (per summary suffix `[rhtpa-2.2]`).

However, version impact analysis shows that stream **2.1.x** is also affected:
- 2.1.0 ships quinn-proto 0.11.9 (affected)
- 2.1.1 ships quinn-proto 0.11.9 (affected)

This triggers **Case B** (cross-stream impact) in Step 7 for the 2.1.x stream.
